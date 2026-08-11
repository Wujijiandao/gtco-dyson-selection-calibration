# Submission claim boundaries — v2.4 PRE-ZENODO

## Supported

1. The 10-band experiment measures a **conditional SED-recognition response**, not final survey completeness.
2. Frozen baseline response is 0.910537; a conservative flux-dependent noise bracket gives 0.910309.
3. W2/template correction-aware variants give approximately 0.911–0.917. A literal four-band nominal-onset hard-cut stress test gives 0.696488 and is not the preferred reconstruction because it changes template coverage strongly.
4. Applying published WISE blackbody colour corrections and WISE isophotal wavelengths gives 0.911568; the 0.91 grid-average response is stable to this broad-band sensitivity test.
5. Restricting the validation population to 1,458 stars fainter than all four nominal WISE saturation onsets gives 0.947213. This is a **conditioning sensitivity**, not a replacement for the baseline result.
6. The 0.414222 quantity is the same-source coupling between injected photometric recovery and the **baseline observed host gate**, not counterfactual host completeness.
7. The joint-minus-factorised difference is 0.011765 with source-cluster bootstrap 95% interval [0.008859, 0.014732] in the frozen validation design.
8. For the 23 tested baseline-clean, unsaturated W3 hosts, morphology retention remains complete under the stated metric/threshold and PSF-mismatch challenge family; the one-sided 95% host-level lower bound is approximately 0.878 for this tested family.
9. W4 matched-PSF grid-cell retention is 1.0 but is strongly PSF/operator dependent; W4 is an operator-sensitivity result, not a robust completeness scalar.
10. Image-stage response is represented conditionally as `C_image = P(E) P(L|E) P(M|E,L,O_image)`.

## Not supported / must not be claimed

1. A measured all-star Dyson-sphere occurrence rate.
2. A measured Hephaistos-II final-pipeline completeness.
3. Full counterfactual Gaia/WISE host completeness.
4. Survey-population field-environment completeness.
5. A robust W4 or joint W3+W4 morphology-completeness lower bound.
6. `C_image = 1` for the WISE survey population.
7. Exact reconstruction of the original Hephaistos-II template identities, CNN state, or final manual visual operator.
8. Exact original-pipeline full response-curve synthetic photometry; the WISE colour-correction run is a published-system sensitivity test.
9. Independent-trial interpretation of repeated `(T_DS, gamma)` grid cells on the same host.
10. Unconditional external validity from the 100-pc calibration sample to the 300-pc Hephaistos-II candidate population.
