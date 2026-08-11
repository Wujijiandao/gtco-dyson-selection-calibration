# GTCO Dyson-Sphere Selection Calibration — v2.3 release candidate

This release candidate contains the referee-hardened MNRAS analysis.

The most important change from the earlier snapshot is scientific, not cosmetic:
- W3 remains the robust tested conditional morphology result.
- W4 is explicitly PSF/operator sensitive and is **not** assigned a robust morphology-completeness bound.
- the 0.414 result is explicitly coupling to baseline observed host state, not counterfactual host completeness.

Additional hardening scripts:
- `06_photometric_noise_bracket.py`
- `07_psf_disjoint_split_challenge.py`
- `08_psf_continuous_mismatch.py`
- `09_source_level_cluster_bootstrap.py`
- `10_variant_template_reconstruction.py`

See `CLAIM_BOUNDARIES.md`, `TEST_STATUS.md`, and `manuscript/`.

After these files are pushed to the existing public repository, freeze the exact GitHub release as `v1.0.0-submission`, then archive that release with Zenodo.
