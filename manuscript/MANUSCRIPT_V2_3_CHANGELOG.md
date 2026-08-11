# MANUSCRIPT v2.3 CHANGELOG — referee hardening

This revision follows a two-referee adversarial simulation and four P0 robustness checks.

## P0-1 — WISE template saturation / W2 semantics
The frozen 265-star emulation does not exactly reproduce the published W1/W2 saturation semantics. A W2-correction-only sensitivity changes mean recovery from 0.910537 to 0.911086; a correction-aware reselected-template variant gives 0.916605. A literal four-band onset-threshold exclusion gives 0.696488 but collapses the bright end of the template sequence and is retained only as a stress test.

## P0-2 — host-response semantics
The 0.414222 quantity is no longer described as full photometric-plus-host completeness. It is the same-source coupling of injected photometric recovery to the **baseline observed** Gaia/WISE host gate. Full counterfactual host completeness remains uncalibrated.

## P0-3 — photometric-noise model
A conservative floor-plus-Poisson bracket gives mean recovery 0.910309, only -0.000228 from the frozen baseline. Extreme Poisson-only and constant-fractional brackets are retained as stress bounds, not preferred detector models.

## P0-4 — PSF mismatch
The previous matched-PSF W3/W4 symmetry does not survive challenge.

- W3 remains fully retained across the tested disjoint empirical-PSF split, moderate broadening, and 0.1–0.5 pixel offsets.
- W4 is strongly PSF-model dependent:
  - matched: 1.000
  - mild blur: 0.451
  - 0.1-pixel offset: 0.362
  - disjoint empirical PSFs: 0.030

Therefore only W3 retains the one-sided 95% host-level lower bound (>0.878) as a robust conditional morphology statement. W4 is now reported as an operator-sensitivity result.

## Additional statistical hardening
A 20,000-replicate source-cluster bootstrap gives:
- joint baseline-host coupling: 0.414222, 95% [0.397740, 0.431167]
- joint-minus-factorized difference: 0.011765, 95% [0.008859, 0.014732]
