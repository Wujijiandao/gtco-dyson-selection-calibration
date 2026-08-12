#!/usr/bin/env python3
"""
Re-run the E12c response given a frozen alternative template/validation table.
This reproduces the response of a sensitivity variant; it does not reconstruct
the ambiguous literature-to-table selection algorithm itself.
"""
from pathlib import Path
import argparse, importlib.util, numpy as np, pandas as pd
from scipy.spatial import cKDTree
ap=argparse.ArgumentParser()
ap.add_argument("templates",type=Path); ap.add_argument("validation",type=Path)
ap.add_argument("host_flags",type=Path); ap.add_argument("output_csv",type=Path)
args=ap.parse_args()
core=Path(__file__).with_name("02b_e12c_e17f_source_level_reconstruction.py")
spec=importlib.util.spec_from_file_location("e12",core)
e12=importlib.util.module_from_spec(spec); spec.loader.exec_module(e12)
templates=pd.read_csv(args.templates,dtype={"source_id":"string"})
val=pd.read_csv(args.validation,dtype={"source_id":"string"})
host=pd.read_csv(args.host_flags,dtype={"source_id":"string"})
hp=val[["source_id"]].merge(host[["source_id","pass_hostcuts_w1000"]],on="source_id",how="left")["pass_hostcuts_w1000"].fillna(False).to_numpy(bool)
library=np.vstack([e12.ds_absolute_mags(templates,T,g).astype(np.float32)
                   for T in e12.T_LIBRARY for g in e12.G_LIBRARY])
tree=cKDTree(library); Fbase,sigma=e12.baseline_flux_and_sigma(val)
dm=5*np.log10(val["distance_invparallax_pc"].to_numpy(float)/10.0)
rng=np.random.default_rng(e12.SEED); rows=[]
for T in e12.T_TRUTH:
    for g in e12.G_TRUTH:
        M=e12.ds_absolute_mags(val,T,g); m=M+dm[:,None]
        F=e12.ZERO_JY[None,:]*10**(-0.4*m); ratio=F/Fbase
        snr=e12.expected_snr(val,ratio)
        gate=(np.isfinite(m).all(axis=1)&(m[:,0]<=21)&
              (snr[:,3:6]>2).all(axis=1)&(snr[:,8:10]>3.5).all(axis=1))
        Fo=F+rng.normal(size=F.shape)*sigma; surv=gate&(Fo>0).all(axis=1)
        mo=np.full_like(Fo,np.nan); mask=Fo>0; z=np.broadcast_to(e12.ZERO_JY,Fo.shape)
        mo[mask]=-2.5*np.log10(Fo[mask]/z[mask]); Mo=mo-dm[:,None]
        rmse=np.full(len(val),np.inf); q=surv&np.isfinite(Mo).all(axis=1)
        if q.any():
            dist,_=tree.query(Mo[q],k=1,workers=-1); rmse[q]=dist/np.sqrt(10)
        rec=surv&(rmse<=.2)
        rows.append(dict(T_DS_K=T,gamma=g,survival=surv.mean(),recovery=rec.mean(),
                         baseline_host=hp.mean(),joint_baseline_host=(rec&hp).mean()))
surface=pd.DataFrame(rows)
summary=pd.DataFrame([dict(N_templates=len(templates),N_validation=len(val),
    mean_survival=surface.survival.mean(),mean_recovery=surface.recovery.mean(),
    baseline_host=hp.mean(),mean_joint_baseline_host=surface.joint_baseline_host.mean())])
args.output_csv.parent.mkdir(parents=True,exist_ok=True); summary.to_csv(args.output_csv,index=False)
print(summary.to_string(index=False))
