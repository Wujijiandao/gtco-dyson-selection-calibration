# GTCO MNRAS referee-hardening interim audit

## Status

The long-running hardening job was interrupted after the first photometric and host-response sensitivity runs. The workspace was recovered and the remaining noise-model and PSF-mismatch challenges were executed separately.

## P0-1 — WISE saturation / W2 correction semantics

Frozen-template baseline:
- mean photometric recovery: 0.910537
- mean joint with baseline host gate: 0.414222

Current frozen templates + W2 correction:
- recovery: 0.911086

Correction-aware reselected templates + W2 correction:
- recovery: 0.916605

Literal hard AllWISE onset-threshold selection:
- recovery: 0.696488

Interpretation:
- A literal W1/W2/W3/W4 onset-threshold exclusion removes the bright end of the template sequence and is not a useful emulation of the stated 0 <= M_G <= 13.6 template coverage.
- W2-correction-aware variants change the headline recovery only modestly.
- The hard-cut result is retained as a stress test, not as the preferred reconstruction.

## P0-2 — counterfactual host semantics

Exploratory empirical KNN host-response model:
- actual validation baseline host pass: 0.442000
- KNN baseline-predicted host pass: 0.429399
- mean counterfactual host pass over the grid: 0.480165
- expected photometric + counterfactual-KNN joint: 0.435434

Decision:
- This KNN model is not promoted to the headline analysis because dimmed partial-Dyson sources move off the ordinary main-sequence training manifold.
- The existing 0.414222 quantity will be renamed as the source-level coupling of injected photometric recovery with the **baseline observed host gate**, not as full counterfactual host completeness.

## P0-3 — photometric-noise model sensitivity

| noise_model                |   mean_survival |   mean_recovery |   mean_joint_baseline_host |   delta_recovery_vs_frozen |
|:---------------------------|----------------:|----------------:|---------------------------:|---------------------------:|
| baseline_absolute          |        0.986302 |        0.910537 |                   0.414222 |                1.11022e-16 |
| poisson_scaled             |        0.996648 |        0.955685 |                   0.433543 |                0.0451481   |
| conservative_floor_poisson |        0.986302 |        0.910309 |                   0.414154 |               -0.000228395 |
| constant_fractional        |        0.74029  |        0.701735 |                   0.330852 |               -0.208802    |

Key result:
- The conservative floor+Poisson bracket gives recovery 0.910309, differing from the frozen baseline by only -0.000228.
- Pure Poisson-scaled and constant-fractional models are retained as intentionally extreme bracketing cases, not preferred detector models.
- The earlier empirical magnitude-error interpolation attempt is rejected because most injected cases required out-of-support clamping/extrapolation.

## P0-4 — injection/scoring PSF mismatch

### Disjoint empirical PSF subsets

| band   | variant           |   N_hosts |   N_valid |   retention |   hosts_with_any_failure |
|:-------|:------------------|----------:|----------:|------------:|-------------------------:|
| W3     | split             |        23 |       332 |   1         |                        0 |
| W3     | split_blur        |        23 |       332 |   1         |                        0 |
| W3     | split_blur_offset |        23 |       332 |   1         |                        0 |
| W3     | split_offset      |        23 |       332 |   1         |                        0 |
| W4     | split             |        23 |       596 |   0.0302013 |                       23 |
| W4     | split_blur        |        23 |       596 |   0.0201342 |                       23 |
| W4     | split_blur_offset |        23 |       596 |   0.011745  |                       23 |
| W4     | split_offset      |        23 |       596 |   0.0268456 |                       23 |

### Controlled PSF mismatch

| band   | variant        |   N_hosts |   N_valid |   retention |   host_allpass_fraction |   hosts_with_any_failure |   median_score_change |
|:-------|:---------------|----------:|----------:|------------:|------------------------:|-------------------------:|----------------------:|
| W3     | blur_mild      |        23 |       332 |   1         |                1        |                        0 |             -0.539115 |
| W3     | blur_moderate  |        23 |       332 |   1         |                1        |                        0 |              0.41604  |
| W3     | matched        |        23 |       332 |   1         |                1        |                        0 |             -0.538548 |
| W3     | offset_0p1pix  |        23 |       332 |   1         |                1        |                        0 |              0.320284 |
| W3     | offset_0p25pix |        23 |       332 |   1         |                1        |                        0 |              1.54209  |
| W3     | offset_0p5pix  |        23 |       332 |   1         |                1        |                        0 |              2.78193  |
| W4     | blur_mild      |        23 |       596 |   0.451342  |                0.173913 |                       19 |             13.554    |
| W4     | blur_moderate  |        23 |       596 |   0.171141  |                0        |                       23 |             22.6595   |
| W4     | matched        |        23 |       596 |   1         |                1        |                        0 |             -0.50334  |
| W4     | offset_0p1pix  |        23 |       596 |   0.362416  |                0.130435 |                       20 |             15.7336   |
| W4     | offset_0p25pix |        23 |       596 |   0.135906  |                0        |                       23 |             23.2495   |
| W4     | offset_0p5pix  |        23 |       596 |   0.0419463 |                0        |                       23 |             28.971    |

Key result:
- W3 remains fully retained across the tested split-PSF, moderate-broadening and subpixel-offset challenges.
- W4 is strongly operator-sensitive: matched-PSF retention is 1.0, but even mild PSF mismatch substantially reduces retention.
- Therefore the previous W4 23/23 matched-operator result must not remain a strong headline completeness statement.
- The revised paper should retain W3 as the robust conditional morphology result and report W4 PSF sensitivity as a limitation/result in its own right.

## Required manuscript changes

1. Rename the 0.414222 host quantity to baseline-host-gated source-level coupling.
2. Add saturation/W2-correction sensitivity and explicitly distinguish correction-aware from literal hard saturation cuts.
3. Add the conservative photometric-noise bracket.
4. Remove W4/joint 0.878/0.873 from the abstract-level robust morphology claim.
5. Add a W4 PSF-sensitivity subsection and figure/table.
6. Narrow the title/abstract wording from generic 'real-image completeness' to conditional image/morphology response.
7. Preserve the matched-PSF W4 result as an operator-conditional diagnostic, not as a population or robust conditional completeness measurement.
