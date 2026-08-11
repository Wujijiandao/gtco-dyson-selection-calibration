# PORTABLE SCRIPT SMOKE TEST — v2.3

The newly added referee-hardening scripts were executed from the repository copy against the frozen workspace inputs.

## 06_photometric_noise_bracket.py
Passed. Reproduced:
- baseline 0.910537
- conservative floor+Poisson 0.910309
- Poisson-scaled 0.955685
- constant-fractional 0.701735

## 07_psf_disjoint_split_challenge.py
Passed. Reproduced:
- W3 split retention 1.000
- W4 split retention 0.030201

A benign `All-NaN slice` warning can occur at cutout-edge pixels during median PSF stacking; non-finite stack pixels are explicitly replaced before PSF normalization.

## 08_psf_continuous_mismatch.py
Passed. Reproduced:
- W3: 1.000 for all tested variants
- W4 mild blur: 0.451342
- W4 0.1-pixel offset: 0.362416

## 09_source_level_cluster_bootstrap.py
Passed. Reproduced:
- joint-minus-factorized 0.011765
- 95% source-cluster interval [0.008859, 0.014732]

## 10_variant_template_reconstruction.py
Passed on both frozen sensitivity variants:
- correction-aware variant: recovery 0.916605, joint baseline-host 0.431290
- literal hard-onset stress variant: recovery 0.696488, joint baseline-host 0.324648

The sensitivity-table script reproduces response conditional on the frozen alternative template/validation tables. It intentionally does not claim to reconstruct an unambiguous literature-to-table selection algorithm where the published saturation wording is insufficiently specific.
