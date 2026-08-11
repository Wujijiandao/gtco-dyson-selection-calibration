# COMPILE_QA — MNRAS draft v2.3

- Target: MNRAS Paper.
- Final compiled PDF: 11 pages.
- Abstract: approximately 245 words.
- Cited references in compiled bibliography: 28.
- `pdflatex + bibtex8 + pdflatex x2`: passed.
- Undefined citations/cross-references: none detected in the final log.
- Overfull boxes: none detected in the final log.
- PDF preflight: openable, unencrypted, non-scanned.
- All 11 pages were rendered and visually inspected.
- Page 1 and page 11 were separately inspected at full rendered size.
- No blocking clipping, overlap, missing figure, or broken-glyph defect was found.

## Scientific hardening incorporated in v2.3

- WISE template-saturation and W2-correction sensitivity is explicit.
- Conservative flux-dependent photometric-noise bracket is reported.
- The 0.414 quantity is relabelled as coupling to the **baseline observed host gate**, not counterfactual host completeness.
- Source-cluster bootstrap quantifies the 0.414-versus-0.402 difference.
- W3 remains the robust real-image morphology result.
- W4 matched-PSF retention is explicitly downgraded after injection/scoring PSF mismatch challenges.
- The paper no longer reports a robust W4 or joint W3+W4 morphology-completeness bound.

Pending publication metadata:
- Zenodo DOI for the frozen GitHub release.
- Author confirmation of conflict-of-interest status.
- Submission-date recheck of 2026 preprint publication status.
