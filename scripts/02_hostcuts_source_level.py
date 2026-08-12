#!/usr/bin/env python3
from pathlib import Path
import sys, numpy as np, pandas as pd

DATA=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True,exist_ok=True)

patch=pd.read_csv(DATA/"df8660d8-9564-11f1-b807-bc97e148b76b-O-result.csv",dtype={"source_id":"string"})
master=pd.read_csv(DATA/"gtco_e12_real_100pc_master_with_msflags.csv.gz",
                   usecols=["source_id","ruwe","wise_ext_flag","heph_cmd_main_sequence"],
                   dtype={"source_id":"string"})
df=master.merge(patch,on="source_id",how="left",validate="one_to_one")

df["pass_halpha"]=~(
    df.ew_espels_halpha.notna() &
    df.ew_espels_halpha_uncertainty.notna() &
    ((df.ew_espels_halpha+3*df.ew_espels_halpha_uncertainty)<0)
)
df["pass_ruwe"]=df.ruwe.notna()&(df.ruwe<=1.4)
df["pass_extflag"]=df.wise_ext_flag.notna()&(df.wise_ext_flag==0)
df["pass_starprob"]=df.classprob_dsc_combmod_star.notna()&(df.classprob_dsc_combmod_star>0.9)

ok=(df.phot_g_mean_mag.notna()&df.phot_g_n_obs.notna()&
    df.phot_g_mean_flux_over_error.notna()&
    (df.phot_g_n_obs>0)&(df.phot_g_mean_flux_over_error>0))
df["nu_g"]=np.nan
df.loc[ok,"nu_g"]=np.sqrt(df.loc[ok,"phot_g_n_obs"].astype(float))/df.loc[ok,"phot_g_mean_flux_over_error"].astype(float)

z=df.loc[ok,["source_id","phot_g_mean_mag","nu_g"]].sort_values("phot_g_mean_mag").copy()
for w in (500,1000,5000):
    ref=z.nu_g.rolling(w,center=True,min_periods=max(50,w//5)).median()
    ref=ref.fillna(z.nu_g.rolling(min(w,len(z)),center=True,min_periods=20).median())
    z[f"gvar_w{w}"]=z.nu_g/ref
g=z.set_index("source_id")[[f"gvar_w{w}" for w in (500,1000,5000)]]
df=df.join(g,on="source_id")
for w in (500,1000,5000):
    df[f"pass_gvar_w{w}"]=df[f"gvar_w{w}"].notna()&(df[f"gvar_w{w}"]<=2)
    df[f"pass_hostcuts_w{w}"]=(
        df.pass_halpha & df[f"pass_gvar_w{w}"] & df.pass_ruwe &
        df.pass_extflag & df.pass_starprob
    )

ms=df[df.heph_cmd_main_sequence.fillna(False)]
summary=pd.DataFrame([{
    "scope":"CMD_main_sequence","N":len(ms),
    "host_pass_w500":ms.pass_hostcuts_w500.mean(),
    "host_pass_w1000":ms.pass_hostcuts_w1000.mean(),
    "host_pass_w5000":ms.pass_hostcuts_w5000.mean(),
    "Halpha_available":ms.ew_espels_halpha.notna().mean(),
    "starprob_available":ms.classprob_dsc_combmod_star.notna().mean(),
}])
summary.to_csv(OUT/"hostcut_summary.csv",index=False)
df[["source_id","pass_hostcuts_w500","pass_hostcuts_w1000","pass_hostcuts_w5000"]].to_csv(
    OUT/"hostcut_flags.csv.gz",index=False,compression="gzip")
print(summary.to_string(index=False))
