# COMPILE_QA — MNRAS draft v2.4 PRE-ZENODO

- Target: MNRAS Paper.
- Final PDF: **11 pages**.
- Abstract: approximately **248 words** by the local token-count audit; within the current MNRAS normal 250-word guidance for Papers.
- Cited references: **28**.
- `pdflatex + bibtex8 + pdflatex x2`: passed.
- Undefined citations/cross-references: none detected in final log.
- Overfull boxes: none detected in final log.
- PDF preflight:
  - openable: yes
  - encrypted: no
  - likely scanned: no
  - XFA: no
- Final PDF rendered at 170 dpi using the PDF skill renderer: **11/11 pages**.
- Full contact sheet inspected; page 1 and page 11 inspected separately at full rendered size.
- No blocking clipping, overlap, missing figure, broken glyph, or empty spill page remains.
- Render comparison against v2.3 completed; the changed pages correspond to the expected colour-correction/saturation text, table changes, reference/endmatter updates, and resulting reflow.

## Scientific hardening represented in this build

- Baseline conditional SED response: 0.910537.
- Conservative flux-dependent noise: 0.910309.
- W2/template correction-aware variants: 0.911–0.917.
- WISE blackbody colour correction + isophotal wavelengths: 0.911568.
- All-WISE-unsaturated validation subset: 0.947213 (conditioning sensitivity only).
- Same-source coupling to baseline observed host gate: 0.414222.
- Joint-minus-factorised source-cluster bootstrap 95% interval: [0.008859, 0.014732].
- W3 tested challenge-family host-level lower bound: >0.878 (one-sided 95%).
- W4: explicitly PSF/operator dependent; no robust W4 or joint W3+W4 morphology-completeness bound claimed.

## Remaining non-scientific pre-submission items

- freeze GitHub release `v1.0.0-submission` after the v2.4 repository update;
- mint Zenodo DOI;
- insert DOI and formal software citation;
- author confirmation of conflict-of-interest status;
- author confirmation of funding status;
- final ScholarOne-generated PDF inspection.
