# TEST STATUS — v2.4 PRE-ZENODO

## Baseline catalogue reconstruction
- mean survival: 0.986302
- conditional SED recovery: 0.910537
- baseline observed host pass: 0.442
- same-source SED + baseline-host coupling: 0.414222
- factorised stage-average estimate: 0.402457

## Source-cluster uncertainty (20,000 replicates)
- joint-minus-factorised: 0.011765
- 95% interval: [0.008859, 0.014732]

## Template / W2 / saturation sensitivity
- frozen templates + W2 correction: 0.911086
- correction-aware reselected templates: 0.916605
- literal four-band nominal-onset hard-cut stress test: 0.696488

## Photometric-noise sensitivity
- baseline absolute-error model: 0.910537
- conservative floor+Poisson bracket: 0.910309
- Poisson-scaled extreme: 0.955685
- constant-fractional extreme: 0.701735

## WISE broad-band colour-correction sensitivity
- frozen reference wavelengths + published WISE blackbody colour correction: 0.912309
- WISE isophotal wavelengths + colour correction: 0.911568
- baseline: 0.910537

## Validation-saturation conditioning
- W1 brighter than nominal onset: 1542/3000 = 51.4%
- W2: 436/3000 = 14.53%
- W3: 3/3000 = 0.1%
- W4: 0
- all-four-band-unsaturated validation subset: N=1458
- conditional recovery in that subset: 0.947213

## W3 PSF challenge
Matched, mild blur, moderate blur, 0.1/0.25/0.5-pixel offsets, and disjoint empirical-PSF split all retain grid-cell response 1.000 in the tested clean/unsaturated sample. Host-level one-sided 95% lower summary: ~0.878 for 23 tested hosts.

## W4 PSF challenge
- matched grid-cell retention: 1.000
- mild blur: 0.451342
- moderate blur: 0.171141
- 0.1-pixel offset: 0.362416
- 0.25-pixel offset: 0.135906
- 0.5-pixel offset: 0.041946
- disjoint empirical split: ~0.030201
No robust W4 or joint W3+W4 completeness bound is claimed.

## Portable scripts
- scripts 01–12 syntax checked (10 is an alternative-template helper and is not part of the default run_all workflow).
- scripts 11 and 12 were actually smoke-tested against the frozen workspace and reproduced the values above.

## Manuscript QA
- v2.4 PRE-ZENODO PDF: 11 pages
- abstract: ~248 words
- cited references: 28
- undefined references/citations: none detected
- overfull boxes: none detected
- PDF preflight: passed
- 11-page render inspection: passed
- simulated second referee outcome: Minor / Minor-Accept-after-minor
