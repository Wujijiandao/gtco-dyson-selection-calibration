# REFEREE PRECHECK — MNRAS submission draft v2.1

## Main potential objections and current status

### 1. “The probability identity is trivial; where is the novelty?”
**Addressed.** The manuscript explicitly says the identity is elementary probability. Novelty is operational/empirical: matched source-level selection calibration, real-image injection, LOHO validation, and decomposition of unmeasured selection terms.

### 2. “0.910 is not survey completeness.”
**Addressed.** It is `C_phot|V`, conditional on the validation-eligible ten-band pool. The strict ten-band-with-errors engineering pool is 72,716/250,909 = 28.98%, exposed separately rather than silently folded into a final-pipeline completeness.

### 3. “Stage-average efficiencies were multiplied as independent.”
**Directly tested.** Same-source joint recovery is 0.414222 versus 0.402460 from multiplying stage averages.

### 4. “Image test leaks the test host into PSF/calibration.”
**Addressed.** LOHO excludes each test host from both empirical PSF construction and morphology calibration.

### 5. “Hundreds of injection cells are pseudo-replication.”
**Addressed.** Host is the independent unit. One-sided 95% exact lower bounds: W3 0.877877 (23/23), W4 0.877877 (23/23), joint 0.872695 (22/22).

### 6. “AllWISE pixel noise is correlated; chi-square is not formal.”
**Addressed.** The term is called pseudo-chi-square. Ablations remove it; retention remains 1.000.

### 7. “Morphology threshold is arbitrary.”
**Addressed by sensitivity analysis.** 90th percentile, 95th percentile, and maximum training-score envelopes all retain every valid injection for every tested feature set.

### 8. “The 24 image fields are unrepresentatively clean.”
**Explicit limitation.** They constrain conditional `R_morph`, not population `C_environment`.

### 9. “Bright injected sources violate linear image response.”
**Bounded, not solved.** Saturation-risk cases are excluded from the linear-response claim; non-linearity remains an explicit uncalibrated term.

### 10. “Gaia/WISE epoch mismatch biases centroids.”
**Addressed.** Gaia 2016.0 positions are propagated to approximate WISE epoch 2010.5. Median displacement 0.479 arcsec; q95 1.433 arcsec; maximum 2.814 arcsec.

### 11. “This is not an exact Hephaistos-II reproduction.”
**Explicitly acknowledged.** Exact template identities, internal grid/passband details, original CNN weights, and final visual operator are not reconstructed. No final-candidate occurrence inversion is attempted.

### 12. “100 pc calibration differs from the 300 pc candidate search.”
**Explicit limitation.** External validity to the 300-pc final-candidate population is not assumed.

### 13. “Gvar neighbourhood is not uniquely specified.”
**Sensitivity tested.** Windows 500/1000/5000 give CMD-MS host-pass fractions 0.522819/0.522875/0.522994.

### 14. “Literature context is too thin.”
**Substantially addressed.** Current manuscript cites 28 works covering Dyson-search history, G-HAT, Gaia/WISE foundations, survey selection functions, confusion, Hephaistos I/II, and candidate follow-up.

## Remaining author-level actions before Submit

- Mint Zenodo DOI and insert it into Data Availability / software citation.
- Re-check 2026 preprint publication status on the actual submission date.
- Author personally confirms conflict-of-interest status.
- Human read-through of every claim/equation/reference.
- Inspect the ScholarOne-generated review PDF before submission.
