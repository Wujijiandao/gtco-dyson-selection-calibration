#!/usr/bin/env python3
from pathlib import Path
import sys, numpy as np, pandas as pd
from scipy.stats import beta

RES=Path(sys.argv[1]).resolve()
df=pd.read_csv(RES/"loho_real_image_injections.csv.gz",dtype={"source_id":"string"})
rows=[]
for band in ("W3","W4"):
    d=df[(df.band==band)&df.baseline_pass&~df.catalog_saturation_risk]
    h=d.groupby("source_id").injected_pass.all()
    n=len(h); k=int(h.sum())
    rows.append({
        "band":band,"N_independent_hosts":n,"N_host_successes":k,
        "observed_host_success_fraction":k/n,
        "one_sided_95pct_exact_lower":float(beta.ppf(.05,k,n-k+1)) if k else 0.
    })
pd.DataFrame(rows).to_csv(RES/"host_level_confidence.csv",index=False)
print(pd.DataFrame(rows).to_string(index=False))
