#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, sys

ROOT=Path(__file__).resolve().parents[1]
DATA=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT.parent
manifest=ROOT/"input_manifest.csv"

bad=0
with manifest.open(encoding="utf-8",newline="") as f:
    rows=list(csv.DictReader(f))

print("GTCO submission reproduction — input verification")
print("Data root:",DATA)
for r in rows:
    p=DATA/r["filename"]
    if not p.exists():
        print("MISSING",r["logical_name"],p)
        bad+=1; continue
    sha=hashlib.sha256(p.read_bytes()).hexdigest()
    ok=(not r["sha256"]) or sha==r["sha256"]
    print(("OK" if ok else "HASH_MISMATCH"),r["logical_name"],p.name,sha)
    bad+=0 if ok else 1

wise_manifest=ROOT/"wise_fits_product_manifest.csv"
if wise_manifest.exists():
    import csv as _csv
    with wise_manifest.open(encoding="utf-8",newline="") as f:
        ws=list(_csv.DictReader(f))
    found=0
    for r in ws:
        # Search common extraction location or flat data root.
        candidates=[DATA/Path(r["path"]).name,
                    DATA/"GTCO_E17_WISE_cutouts"/Path(r["path"]).name,
                    DATA/"e17i_real_fits_full"/"GTCO_E17_WISE_cutouts"/Path(r["path"]).name]
        p=next((x for x in candidates if x.exists()),None)
        if p is None:
            continue
        found+=1
        sha=hashlib.sha256(p.read_bytes()).hexdigest()
        if sha!=r["sha256"]:
            print("WISE_HASH_MISMATCH",p); bad+=1
    print("WISE FITS located:",found,"/",len(ws))
    if found not in (0,len(ws)):
        print("WARNING: partial WISE FITS set found.")
if bad:
    raise SystemExit(f"Input verification failed: {bad} problem(s)")
print("Input verification passed.")
