#!/usr/bin/env bash
set -euo pipefail
DATA="${1:-..}"
python scripts/01_verify_inputs.py "$DATA"
python scripts/02_hostcuts_source_level.py "$DATA" reproduced_results
python scripts/02b_e12c_e17f_source_level_reconstruction.py "$DATA" reproduced_results
python scripts/03_loho_real_image.py "$DATA" reproduced_results
python scripts/04_host_cluster_statistics.py reproduced_results
python scripts/05_image_metric_threshold_robustness.py "$DATA" reproduced_results
python scripts/06_photometric_noise_bracket.py "$DATA" reproduced_results
python scripts/07_psf_disjoint_split_challenge.py "$DATA" reproduced_results
python scripts/08_psf_continuous_mismatch.py "$DATA" reproduced_results
python scripts/09_source_level_cluster_bootstrap.py reproduced_results/e12c_e17f_reconstructed_cases.csv.gz reproduced_results
python scripts/11_wise_blackbody_color_correction_sensitivity.py "$DATA" reproduced_results
python scripts/12_validation_wise_unsaturated_sensitivity.py "$DATA" reproduced_results
echo "Core submission checks and referee-hardening sensitivities reproduced successfully."
