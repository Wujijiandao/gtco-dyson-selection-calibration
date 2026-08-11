#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys

ROOT=Path(__file__).resolve().parent
S=ROOT/"scripts"
DATA=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT.parent
RES=ROOT/"reproduced_results"
RES.mkdir(exist_ok=True)

def run(cmd):
    print("\n>>>"," ".join(map(str,cmd)))
    subprocess.run([str(x) for x in cmd],check=True)

run([sys.executable,S/"01_verify_inputs.py",DATA])
run([sys.executable,S/"02_hostcuts_source_level.py",DATA,RES])
run([sys.executable,S/"02b_e12c_e17f_source_level_reconstruction.py",DATA,RES])
run([sys.executable,S/"03_loho_real_image.py",DATA,RES])
run([sys.executable,S/"04_host_cluster_statistics.py",RES])
run([sys.executable,S/"05_image_metric_threshold_robustness.py",DATA,RES])
run([sys.executable,S/"06_photometric_noise_bracket.py",DATA,RES])
run([sys.executable,S/"07_psf_disjoint_split_challenge.py",DATA,RES])
run([sys.executable,S/"08_psf_continuous_mismatch.py",DATA,RES])
run([sys.executable,S/"09_source_level_cluster_bootstrap.py",RES/"e12c_e17f_reconstructed_cases.csv.gz",RES])
run([sys.executable,S/"11_wise_blackbody_color_correction_sensitivity.py",DATA,RES])
run([sys.executable,S/"12_validation_wise_unsaturated_sensitivity.py",DATA,RES])
print("\nCore submission checks and referee-hardening sensitivities reproduced successfully.")
