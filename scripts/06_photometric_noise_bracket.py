#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util
import numpy as np, pandas as pd
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
val=pd.read_csv(DATA/"gtco_e12c_validation_sample_3000.csv",dtype={"source_id":"string"})
host_path=args.host_flags or (OUT/"hostcut_flags.csv.gz")
if not host_path.exists(): host_path=DATA/"gtco_e17e_hostcut_flags_v2.csv.gz"
host=pd.read_csv(host_path,dtype={"source_id":"string"})
hp=val[["source_id"]].merge(host[["source_id","pass_hostcuts_w1000"]],on="source_id",how="left")["pass_hostcuts_w1000"].fillna(False).to_numpy(bool)

library=np.vstack([e12.ds_absolute_mags(templates,T,g).astype(np.float32)
                   for T in e12.T_LIBRARY for g in e12.G_LIBRARY])
tree=cKDTree(library)
Fbase,sigma0=e12.baseline_flux_and_sigma(val)
dm=5*np.log10(val["distance_invparallax_pc"].to_numpy(float)/10.0)

models=["baseline_absolute","poisson_scaled","conservative_floor_poisson","constant_fractional"]
rows=[]; surfaces=[]
for model in models:
    rng=np.random.default_rng(e12.SEED); cell=[]
    for T in e12.T_TRUTH:
        for g in e12.G_TRUTH:
            Mtrue=e12.ds_absolute_mags(val,T,g); mtrue=Mtrue+dm[:,None]
            Ftrue=e12.ZERO_JY[None,:]*10**(-0.4*mtrue)
            ratio=np.maximum(Ftrue/Fbase,1e-8)
            if model=="baseline_absolute": sig=sigma0
            elif model=="poisson_scaled": sig=sigma0*np.sqrt(ratio)
            elif model=="conservative_floor_poisson": sig=sigma0*np.sqrt(np.maximum(1.0,ratio))
            else: sig=sigma0*ratio
            snr=Ftrue/np.maximum(sig,1e-300)
            gate=(np.isfinite(mtrue).all(axis=1)&(mtrue[:,0]<=21.0)&
                  (snr[:,3:6]>2.0).all(axis=1)&(snr[:,8:10]>3.5).all(axis=1))
            Fobs=Ftrue+rng.normal(size=Ftrue.shape)*sig
            survival=gate&(Fobs>0).all(axis=1)
            mobs=np.full_like(Fobs,np.nan); mask=Fobs>0
            zpb=np.broadcast_to(e12.ZERO_JY,Fobs.shape)
            mobs[mask]=-2.5*np.log10(Fobs[mask]/zpb[mask]); Mobs=mobs-dm[:,None]
            rmse=np.full(len(val),np.inf); q=survival&np.isfinite(Mobs).all(axis=1)
            if q.any():
                dist,_=tree.query(Mobs[q],k=1,workers=-1); rmse[q]=dist/np.sqrt(10.0)
            rec=survival&(rmse<=0.2); joint=rec&hp
            cell.append(dict(noise_model=model,T_DS_K=T,gamma=g,
                             survival=survival.mean(),recovery=rec.mean(),
                             joint_baseline_host=joint.mean()))
    c=pd.DataFrame(cell); surfaces.append(c)
    rows.append(dict(noise_model=model,mean_survival=c.survival.mean(),
                     mean_recovery=c.recovery.mean(),
                     mean_joint_baseline_host=c.joint_baseline_host.mean(),
                     delta_recovery_vs_frozen=c.recovery.mean()-0.910537037037037))
summary=pd.DataFrame(rows); surface=pd.concat(surfaces,ignore_index=True)
summary.to_csv(OUT/"noise_model_bracket_summary.csv",index=False)
surface.to_csv(OUT/"noise_model_bracket_surface.csv",index=False)
print(summary.to_string(index=False))
