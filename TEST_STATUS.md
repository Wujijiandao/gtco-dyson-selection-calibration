# TEST / QA STATUS — v1.1.0-rasti-transfer

## Numerical analysis provenance

No numerical experiment was rerun or altered for the RASTI transfer. The current manuscript uses the frozen outputs from `v1.0.0-submission` (Zenodo DOI `10.5281/zenodo.21896997`). The frozen headline checks include:

- mean catalogue survival: 0.986302
- conditional SED recovery: 0.910537
- baseline observed host pass: 0.442
- same-source SED + baseline-host coupling: 0.414222
- factorised stage-average estimate: 0.402457
- source-cluster joint-minus-factorised difference: 0.011765, 95% interval [0.008859, 0.014732]
- W3 tested clean/unsaturated host-level lower summary: approximately 0.878 for 23 hosts
- W4 remains PSF/operator sensitive and is not assigned a robust completeness scalar

The detailed frozen sensitivity results remain in `results/`, `expected_key_results.json`, and the historical v2.4 syntax/status records.

## RASTI manuscript QA — 2026-09-21

- title/abstract reframed for RASTI methods scope: PASS
- abstract word count: 230 (<=250): PASS
- keywords: 6 total, includes mandatory `Data Methods`: PASS
- main-text figures: 5
- figure alt-text blocks: 5: PASS
- Data availability: PASS
- software bug-reporting route: PASS
- Funding statement: PASS
- Conflict of Interest statement: PASS
- AI-use disclosure in manuscript: PASS
- `\pdfminorversion=5`: PASS
- LaTeX compile: PASS (`pdflatex`, `bibtex8`, `pdflatex`, `pdflatex`)
- undefined citation/reference warnings: none detected
- overfull boxes: none detected
- manuscript PDF: 12 pages, <10 MB
- page-by-page render/visual inspection: PASS
