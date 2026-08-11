# Submission claim boundaries — v2.3 referee-hardened

## Supported
1. The 10-band experiment measures a **conditional SED-recognition response**, not final survey completeness.
2. Baseline recovery is ~0.9105; a conservative flux-dependent noise bracket gives ~0.9103.
3. W2/template-selection sensitivity gives ~0.911–0.917 for correction-aware variants; a literal four-band onset-threshold stress test gives ~0.696 and is not the preferred reconstruction.
4. The 0.414222 quantity is the same-source coupling between injected photometric recovery and the **baseline observed host gate**.
5. The difference from stage-average factorization is 0.011765 with source-cluster bootstrap 95% interval [0.008859, 0.014732].
6. For the tested 23 baseline-clean, unsaturated W3 hosts, morphology retention remains complete under metric/threshold ablations, disjoint empirical PSFs, moderate PSF broadening, and subpixel offsets up to 0.5 Atlas pixel. The one-sided 95% host-level lower bound for this tested challenge family is ~0.878.
7. W4 matched-PSF retention is 1.0 but is strongly PSF-model dependent; it is an operator-sensitivity result, not a robust completeness bound.
8. The image stage is represented conditionally as `C_image = P(E) * P(L|E) * P(M|E,L,O_image)`.

## Not supported
1. A measured all-star Dyson-sphere occurrence rate.
2. A measured Hephaistos-II final-pipeline completeness.
3. Full counterfactual Gaia/WISE host completeness.
4. Survey-population environment completeness.
5. A robust W4 or joint W3+W4 morphology-completeness bound.
6. `C_image = 1`.
7. Exact original Hephaistos-II template identities, CNN weights, or final visual operator.
8. Independent-trial interpretation of hundreds of repeated injection-grid cells.
