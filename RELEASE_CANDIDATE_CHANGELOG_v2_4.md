# MANUSCRIPT v2.4 CHANGELOG — second-review / pre-Zenodo hardening

v2.4 is the pre-Zenodo manuscript produced after a second adversarial referee pass.

## Scientific additions

1. **WISE broad-band colour-correction sensitivity**
   - Full 220,745-model / 54-cell rerun using the published WISE blackbody colour-correction factors.
   - Frozen reference wavelengths + colour correction: `0.912309`.
   - WISE isophotal wavelengths + colour correction: `0.911568`.
   - Baseline remains `0.910537`; the grid-average response is stable at the ~1e-3 level.

2. **Validation-sample WISE saturation conditioning**
   - W1 brighter than nominal onset: 1542/3000 = 51.4%.
   - W2: 436/3000 = 14.53%.
   - W3: 3/3000 = 0.1%.
   - W4: 0.
   - Restricting validation to the 1,458 stars fainter than all four nominal onsets gives recovery `0.947213`.
   - This is explicitly a conditioning sensitivity, not a replacement headline value.

## Editorial/statistical corrections

3. Abstract now says **source-cluster bootstrap**, not host-cluster bootstrap.
4. W4 mismatch values are explicitly labelled **grid-cell retention**; repeated phenotypes are not independent Bernoulli trials.
5. The current title consistently uses **conditional real-image response** rather than the earlier stronger “real-image completeness” wording.
6. MNRAS endmatter order corrected to:
   - Acknowledgements
   - Data Availability
   - References
   - Appendices
7. Reference status updated:
   - Ren et al. 2026: `MNRAS, in press` (arXiv reports accepted by MNRAS).
   - Korn et al. 2026: `preprint (arXiv:2607.25701)`.
   - Zackrisson et al. 2026: `preprint (arXiv:2607.09460)`.
8. Cover letter title updated to match the manuscript and retains the required AI-use disclosure without summarising the results.
9. Reproducibility section now names the WISE colour-correction and all-band-unsaturated validation-subset scripts/outputs.
10. Redundant Appendix B was removed after its content had been integrated into the main text; the final paper returns to 11 pages without changing scientific claims.

## Second simulated referee outcome

- Referee A (selection/statistics): **Minor Revision**.
- Referee B (WISE/technosignatures): **Minor Revision / Accept after minor corrections**.
- Simulated editor: **Minor Revision / scientifically acceptable in principle pending final technical metadata**.

No new P0 scientific blocker was identified in the second review.
