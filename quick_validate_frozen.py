#!/usr/bin/env python3
from pathlib import Path
import json, math, pandas as pd

ROOT=Path(__file__).resolve().parent
EXP=json.loads((ROOT/"expected_key_results.json").read_text())
R=ROOT/"results"

checks=[]

def add(name,value,expected,tol=1e-6):
    ok=abs(float(value)-float(expected))<=tol
    checks.append((name,float(value),float(expected),tol,ok))

u=pd.read_csv(R/"gtco_submission_host_cluster_uncertainty.csv")
for band in ("W3","W4"):
    r=u[u.band==band].iloc[0]
    add(f"LOHO_{band}_one_sided_95_lower",r.exact_one_sided_95pct_lower_bound,
        EXP[f"LOHO_{band}_one_sided_95_lower"],1e-6)

s=pd.read_csv(R/"gtco_submission_loho_summary.csv")
for band in ("W3","W4"):
    r=s[s.band==band].iloc[0]
    add(f"LOHO_{band}_retention",r.conditional_image_retention,1.0,1e-12)
    add(f"LOHO_{band}_independent_hosts",r.N_independent_hosts,
        EXP[f"LOHO_{band}_independent_clean_hosts"],0)

j=pd.read_csv(R/"gtco_submission_joint_host_confidence.csv").iloc[0]
add("LOHO_joint_one_sided_95_lower",j.exact_one_sided_95pct_lower_bound,
    EXP["LOHO_joint_one_sided_95_lower"],1e-6)

e=pd.read_csv(R/"gtco_e17f_e12c_reconstruction_audit.csv").iloc[0]
add("E12c_reconstructed_phot_recovery",e.reconstructed_mean_photometric_recovery,0.910543,5e-6)


rec=R/"e12c_e17f_reconstructed_summary.csv"
if rec.exists():
    rr=pd.read_csv(rec).iloc[0]
    add("standalone_E12cE17f_photometric",rr.mean_photometric_recovery,0.9105432098765432,5e-4)
    add("standalone_E12cE17f_joint",rr.mean_joint_photometry_plus_host,0.4142222222222222,5e-4)


cc=R/"wise_color_correction_summary.csv"
if cc.exists():
    c=pd.read_csv(cc)
    r=c[c["mode"]=="wise_iso_fc"].iloc[0]
    add("WISE_colour_correction_isophotal_recovery",r.mean_recovery,
        EXP["wise_color_correction_isophotal_recovery"],1e-6)

vu=R/"validation_unsaturated_summary.csv"
if vu.exists():
    v=pd.read_csv(vu).iloc[0]
    add("validation_allWISE_unsaturated_recovery",v.mean_recovery,
        EXP["validation_allwise_unsaturated_recovery"],1e-6)
    add("validation_allWISE_unsaturated_N",v.N_validation_unsaturated,
        EXP["validation_allwise_unsaturated_N"],0)

print("GTCO frozen-result quick validation")
for name,value,expected,tol,ok in checks:
    print(("PASS" if ok else "FAIL"),name,"value=",value,"expected=",expected,"tol=",tol)
if not all(x[-1] for x in checks):
    raise SystemExit("Frozen-result validation failed")

ab=R/"gtco_submission_image_metric_threshold_robustness_summary.csv"
if ab.exists():
    a=pd.read_csv(ab)
    bad=a.loc[abs(a.injection_retention-1.0)>1e-12]
    if len(bad):
        raise SystemExit("Image metric/threshold robustness validation failed")
    print("PASS image metric/threshold ablation: all",len(a),"summary configurations retain 1.0")

print("All frozen-result checks passed.")
