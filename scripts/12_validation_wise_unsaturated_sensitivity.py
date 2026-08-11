#!/usr/bin/env python3
"""Conditioning sensitivity for validation stars fainter than nominal WISE saturation onsets.

The restricted sample is intentionally NOT treated as a correction to the
baseline result because the restriction changes the luminosity/host
conditioning of the validation population.
"""
from pathlib import Path
import argparse, importlib.util
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

ap=argparse.ArgumentParser()
ap.add_argument("data_root",type=Path)
ap.add_argument("output_dir",type=Path)
ap.add_argument("--host-flags",type=Path,default=None)
args=ap.parse_args()
DATA=args.data_root.resolve(); OUT=args.output_dir.resolve(); OUT.mkdir(parents=True,exist_ok=True)
core=Path(__file__).with_name("02b_e12c_e17f_source_level_reconstruction.py")
spec=importlib.util.spec_from_file_location("e12",core)
e12=importlib.util.module_from_spec(spec); spec.loader.exec_module(e12)

templates=pd.read_csv(DATA/"gtco_e12c_265_real_templates.csv",dtype={"source_id":"string"})
vall=pd.read_csv(DATA/"gtco_e12c_validation_sample_3000.csv",dtype={"source_id":"string"})
thresholds={"W1":8.1,"W2":6.7,"W3":3.8,"W4":-0.4}
audit=pd.DataFrame([{
    "N_validation":len(vall),
    "W1_brighter_than_onset":int((vall.w1mpro<thresholds["W1"]).sum()),
    "W2_brighter_than_onset":int((vall.w2mpro<thresholds["W2"]).sum()),
    "W3_brighter_than_onset":int((vall.w3mpro<thresholds["W3"]).sum()),
    "W4_brighter_than_onset":int((vall.w4mpro<thresholds["W4"]).sum()),
}])
for b in ["W1","W2","W3","W4"]:
    audit[f"{b}_fraction_brighter_than_onset"]=audit[f"{b}_brighter_than_onset"]/len(vall)
mask=(vall.w1mpro>=8.1)&(vall.w2mpro>=6.7)&(vall.w3mpro>=3.8)&(vall.w4mpro>=-0.4)
val=vall.loc[mask].reset_index(drop=True)

host_path=args.host_flags
if host_path is None:
    for candidate in [OUT/"hostcut_flags.csv.gz",DATA/"gtco_e17e_hostcut_flags_v2.csv.gz"]:
        if candidate.exists(): host_path=candidate; break
if host_path is None or not Path(host_path).exists():
    raise SystemExit("Host-cut flags not found; run 02_hostcuts_source_level.py or pass --host-flags")
host=pd.read_csv(host_path,dtype={"source_id":"string"})
hp=val[["source_id"]].merge(host[["source_id","pass_hostcuts_w1000"]],on="source_id",how="left")["pass_hostcuts_w1000"].fillna(False).to_numpy(bool)

library=np.vstack([e12.ds_absolute_mags(templates,T,g).astype(np.float32)
                   for T in e12.T_LIBRARY for g in e12.G_LIBRARY])
tree=cKDTree(library)
Fbase,sig=e12.baseline_flux_and_sigma(val)
dm=5*np.log10(val.distance_invparallax_pc.to_numpy(float)/10.0)
rng=np.random.default_rng(e12.SEED)
rows=[]
for T in e12.T_TRUTH:
    for g in e12.G_TRUTH:
        M=e12.ds_absolute_mags(val,T,g); m=M+dm[:,None]
        F=e12.ZERO_JY[None,:]*10**(-0.4*m); ratio=F/Fbase; snr=e12.expected_snr(val,ratio)
        gate=(np.isfinite(m).all(axis=1)&(m[:,0]<=21)&
              (snr[:,3:6]>2).all(axis=1)&(snr[:,8:10]>3.5).all(axis=1))
        Fo=F+rng.normal(size=F.shape)*sig; surv=gate&(Fo>0).all(axis=1)
        mo=np.full_like(Fo,np.nan); qf=Fo>0; z=np.broadcast_to(e12.ZERO_JY,Fo.shape)
        mo[qf]=-2.5*np.log10(Fo[qf]/z[qf]); Mo=mo-dm[:,None]
        rmse=np.full(len(val),np.inf); q=surv&np.isfinite(Mo).all(axis=1)
        if q.any():
            dist,_=tree.query(Mo[q],k=1,workers=-1); rmse[q]=dist/np.sqrt(10.0)
        rec=surv&(rmse<=0.2)
        rows.append(dict(T_DS_K=T,gamma=g,survival=surv.mean(),recovery=rec.mean(),
                         joint_baseline_host=(rec&hp).mean()))
surface=pd.DataFrame(rows)
summary=pd.DataFrame([dict(N_validation_all=len(vall),N_validation_unsaturated=len(val),
    fraction_unsaturated=len(val)/len(vall),mean_survival=surface.survival.mean(),
    mean_recovery=surface.recovery.mean(),baseline_host_pass=hp.mean(),
    mean_joint_baseline_host=surface.joint_baseline_host.mean())])
audit.to_csv(OUT/"validation_saturation_audit.csv",index=False)
surface.to_csv(OUT/"validation_unsaturated_surface.csv",index=False)
summary.to_csv(OUT/"validation_unsaturated_summary.csv",index=False)
print(audit.to_string(index=False)); print(summary.to_string(index=False))
