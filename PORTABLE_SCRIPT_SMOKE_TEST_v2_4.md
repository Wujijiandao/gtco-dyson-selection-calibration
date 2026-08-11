# PORTABLE SCRIPT SMOKE TEST — v2.4 PRE-ZENODO

The new second-review hardening scripts were executed from the repository copy against the frozen workspace inputs.

## Script 11 — WISE blackbody colour-correction sensitivity

`11_wise_blackbody_color_correction_sensitivity.py` passed and reproduced:

- baseline: 0.910537
- frozen wavelengths + WISE blackbody colour correction: 0.912309
- WISE isophotal wavelengths + colour correction: 0.911568

The script rebuilds the 220,745-model library for each response mode and reruns all 54 truth cells; it does not read these summary numbers as inputs.

## Script 12 — all-WISE-unsaturated validation conditioning

`12_validation_wise_unsaturated_sensitivity.py` passed and reproduced:

- W1 nominal-onset-bright: 1542 / 3000
- W2: 436 / 3000
- W3: 3 / 3000
- W4: 0 / 3000
- all-four-band-unsaturated validation sample: 1458
- recovery in that conditional subset: 0.947213

The result is labelled a conditioning sensitivity, not a corrected end-to-end completeness.

## Syntax / frozen-result validation

- `run_all.py`: syntax passed.
- all scripts `01` through `12`: syntax passed.
- `quick_validate_frozen.py`: passed all frozen checks, including the new colour-correction and validation-conditioning outputs.

## Interpretation

These scripts close the second simulated referee's WISE broad-band and validation-saturation reproducibility concerns. They do not claim an exact reconstruction of the unpublished/internal Hephaistos-II pipeline state.
