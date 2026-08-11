#!/usr/bin/env python3
from pathlib import Path
import argparse, numpy as np, pandas as pd
ap=argparse.ArgumentParser()
ap.add_argument("case_file",type=Path)
ap.add_argument("output_dir",type=Path)
ap.add_argument("--replicates",type=int,default=20000)
ap.add_argument("--seed",type=int,default=20261008)
args=ap.parse_args()
OUT=args.output_dir.resolve(); OUT.mkdir(parents=True,exist_ok=True)
cases=pd.read_csv(args.case_file,dtype={"source_id":"string"})
g=(cases.groupby("source_id").agg(
    photometric_recovery=("photometric_recovered","mean"),
    baseline_host_pass=("host_pass_w1000","first"),
    joint_recovery=("joint_recovered_host","mean")).reset_index())
arr=g[["photometric_recovery","baseline_host_pass","joint_recovery"]].to_numpy(float)
rng=np.random.default_rng(args.seed); n=len(g); boot=np.empty((args.replicates,4))
for b in range(args.replicates):
    z=arr[rng.integers(0,n,n)]
    ph=z[:,0].mean(); hp=z[:,1].mean(); jo=z[:,2].mean()
    boot[b]=[ph,hp,jo,jo-ph*hp]
point=[g.photometric_recovery.mean(),g.baseline_host_pass.mean(),g.joint_recovery.mean(),
       g.joint_recovery.mean()-g.photometric_recovery.mean()*g.baseline_host_pass.mean()]
names=["mean_photometric_recovery","baseline_host_pass_fraction",
       "mean_joint_baseline_host","joint_minus_factorized"]
summary=pd.DataFrame([dict(metric=name,point_estimate=point[j],
    cluster_bootstrap_q025=float(np.quantile(boot[:,j],.025)),
    cluster_bootstrap_median=float(np.quantile(boot[:,j],.5)),
    cluster_bootstrap_q975=float(np.quantile(boot[:,j],.975)),
    N_independent_hosts=n,bootstrap_replicates=args.replicates,seed=args.seed)
    for j,name in enumerate(names)])
summary.to_csv(OUT/"source_level_joint_cluster_bootstrap.csv",index=False)
print(summary.to_string(index=False))
