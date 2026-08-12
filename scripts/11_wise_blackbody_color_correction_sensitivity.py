#!/usr/bin/env python3
"""WISE broad-band blackbody colour-correction sensitivity.

This is a robustness analysis, not an exact reconstruction of the original
Hephaistos-II synthetic-photometry implementation. It applies the published
WISE blackbody colour-correction factors (Wright et al. 2010) to the added
waste-heat component and optionally uses the published WISE isophotal
wavelengths, then reruns the full 220,745-model / 54-cell validation analysis.
"""
from pathlib import Path
import argparse, importlib.util
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

ap=argparse.ArgumentParser()
ap.add_argument("data_root", type=Path)
ap.add_argument("output_dir", type=Path)
ap.add_argument("--host-flags", type=Path, default=None)
args=ap.parse_args()
DATA=args.data_root.resolve(); OUT=args.output_dir.resolve(); OUT.mkdir(parents=True, exist_ok=True)

core=Path(__file__).with_name("02b_e12c_e17f_source_level_reconstruction.py")
spec=importlib.util.spec_from_file_location("e12", core)
e12=importlib.util.module_from_spec(spec); spec.loader.exec_module(e12)

templates=pd.read_csv(DATA/"gtco_e12c_265_real_templates.csv", dtype={"source_id":"string"})
val=pd.read_csv(DATA/"gtco_e12c_validation_sample_3000.csv", dtype={"source_id":"string"})
host_path=args.host_flags
if host_path is None:
    for candidate in [OUT/"hostcut_flags.csv.gz", DATA/"gtco_e17e_hostcut_flags_v2.csv.gz"]:
        if candidate.exists():
            host_path=candidate; break
if host_path is None or not Path(host_path).exists():
    raise SystemExit("Host-cut flags not found; run 02_hostcuts_source_level.py or pass --host-flags")
host=pd.read_csv(host_path, dtype={"source_id":"string"})
hp=(val[["source_id"]].merge(host[["source_id","pass_hostcuts_w1000"]],on="source_id",how="left")
    ["pass_hostcuts_w1000"].fillna(False).to_numpy(bool))

# Wright et al. (2010), Table 1: blackbody colour-correction factors.
T_TAB=np.array([100.,141.,200.,283.,400.,566.,800.])
FC_TAB=np.array([
 [17.2062,3.9096,2.6588,1.0032],
 [4.0882,1.9739,1.4002,0.9852],
 [2.0577,1.3448,1.0006,0.9833],
 [1.3917,1.1124,0.8791,0.9865],
 [1.1316,1.0229,0.8622,0.9903],
 [1.0263,0.9919,0.8833,0.9935],
 [0.9884,0.9853,0.9125,0.9958],
])
WISE_ISO=np.array([3.3526,4.6028,11.5608,22.0883])

def fc_bb(T):
    x=np.log(T_TAB); xt=np.log(float(T))
    return np.array([np.exp(np.interp(xt,x,np.log(FC_TAB[:,j]))) for j in range(4)])

def ds_abs(df,T,gamma,mode="frozen"):
    Mstar=e12.absolute_mags(df)
    Fstar=e12.ZERO_JY[None,:]*10**(-0.4*Mstar)
    d=df["distance_invparallax_pc"].to_numpy(float)
    Fbol10=df["Fbol_fit_Wm2"].to_numpy(float)*(d/10.0)**2
    lam=e12.LAMBDA_UM.copy()
    if mode=="wise_iso_fc": lam[-4:]=WISE_ISO
    Fds=Fbol10[:,None]*e12.bb_shape_nu(lam,T)[None,:]/e12.JY
    if mode in ("frozen_fc","wise_iso_fc"):
        Fds[:,-4:]*=fc_bb(T)[None,:]
    return -2.5*np.log10(((1-gamma)*Fstar+gamma*Fds)/e12.ZERO_JY[None,:])

def run(mode):
    library=np.vstack([ds_abs(templates,T,g,mode).astype(np.float32)
                       for T in e12.T_LIBRARY for g in e12.G_LIBRARY])
    tree=cKDTree(library)
    Fbase,sigma=e12.baseline_flux_and_sigma(val)
    dm=5*np.log10(val["distance_invparallax_pc"].to_numpy(float)/10.0)
    rng=np.random.default_rng(e12.SEED)
    rows=[]
    for T in e12.T_TRUTH:
        for g in e12.G_TRUTH:
            M=ds_abs(val,T,g,mode); m=M+dm[:,None]
            F=e12.ZERO_JY[None,:]*10**(-0.4*m); ratio=F/Fbase
            snr=e12.expected_snr(val,ratio)
            gate=(np.isfinite(m).all(axis=1)&(m[:,0]<=21)&
                  (snr[:,3:6]>2).all(axis=1)&(snr[:,8:10]>3.5).all(axis=1))
            Fo=F+rng.normal(size=F.shape)*sigma
            surv=gate&(Fo>0).all(axis=1)
            mo=np.full_like(Fo,np.nan); mask=Fo>0; z=np.broadcast_to(e12.ZERO_JY,Fo.shape)
            mo[mask]=-2.5*np.log10(Fo[mask]/z[mask]); Mo=mo-dm[:,None]
            rmse=np.full(len(val),np.inf); q=surv&np.isfinite(Mo).all(axis=1)
            if q.any():
                dist,_=tree.query(Mo[q],k=1,workers=-1); rmse[q]=dist/np.sqrt(10.0)
            rec=surv&(rmse<=0.2)
            rows.append(dict(mode=mode,T_DS_K=T,gamma=g,survival=surv.mean(),
                             recovery=rec.mean(),joint_baseline_host=(rec&hp).mean()))
    return pd.DataFrame(rows)

surfaces=[]
for mode in ["frozen","frozen_fc","wise_iso_fc"]:
    print("running",mode,flush=True); surfaces.append(run(mode))
surf=pd.concat(surfaces,ignore_index=True)
summ=(surf.groupby("mode").agg(mean_survival=("survival","mean"),
       mean_recovery=("recovery","mean"),
       mean_joint_baseline_host=("joint_baseline_host","mean"),
       min_cell_recovery=("recovery","min")).reset_index())
base=summ.loc[summ["mode"]=="frozen","mean_recovery"].iloc[0]
summ["delta_recovery_vs_frozen"]=summ.mean_recovery-base
byT=(surf.groupby(["mode","T_DS_K"]).agg(mean_survival=("survival","mean"),
     mean_recovery=("recovery","mean"),mean_joint=("joint_baseline_host","mean")).reset_index())
fcrows=[]
for T in e12.T_TRUTH:
    f=fc_bb(T); fcrows.append(dict(T_DS_K=T,W1_fc=f[0],W2_fc=f[1],W3_fc=f[2],W4_fc=f[3]))
fcdf=pd.DataFrame(fcrows)
summ.to_csv(OUT/"wise_color_correction_summary.csv",index=False)
surf.to_csv(OUT/"wise_color_correction_surface.csv",index=False)
byT.to_csv(OUT/"wise_color_correction_by_temperature.csv",index=False)
fcdf.to_csv(OUT/"wise_blackbody_fc_truth_grid.csv",index=False)
print(summ.to_string(index=False))
