# GTCO Dyson-Sphere Selection Calibration

Current manuscript target: **RAS Techniques and Instruments (RASTI)**.

Current working manuscript title:

**Selection-function calibration for Gaia-2MASS-WISE partial-Dyson searches: source-level coupling and real-image response**

Author: **Yuzhan Zhang**  
ORCID: https://orcid.org/0009-0000-3121-7972  
Independent Researcher, Beijing, China

## Current repository state

This `main`-branch package is the **v1.1.0-rasti-transfer** working authority prepared after MNRAS manuscript **MN-26-2504-P** was declined for journal-scope reasons and explicitly recommended for transfer to RASTI. The analysis, frozen numerical outputs, figures, and scientific claim boundaries are unchanged; the manuscript has been reframed to foreground the methodological contribution.

The current paper focuses on:

- selection-function calibration for a multistage rare-object pipeline;
- real-star SED injection-recovery;
- source-level coupling between photometric recovery and baseline host-quality state;
- leave-one-host-out real AllWISE image injection;
- W3 robustness and W4 PSF/operator sensitivity;
- explicit separation of measured conditional responses from uncalibrated end-to-end terms.

No Dyson-sphere occurrence rate is reported.

## Frozen numerical-reproduction release

The submission-critical numerical snapshot remains permanently archived as:

- Version: `v1.0.0-submission`
- Zenodo DOI: https://doi.org/10.5281/zenodo.21896997
- GitHub repository: https://github.com/Wujijiandao/gtco-dyson-selection-calibration

**Do not move or overwrite the historical `v1.0.0-submission` tag.** The RASTI transfer manuscript is a later textual/journal-target update built on the same frozen analysis.

## Reproduction

```bash
python run_all.py /path/to/frozen_data_root
```

Large public survey inputs are not redistributed; manifests, hashes, and regeneration paths are supplied. See `CLAIM_BOUNDARIES.md` and `TEST_STATUS.md` before citing numerical values.

## Manuscript and submission materials

- `manuscript/manuscript.tex` - current RASTI-transfer manuscript source
- `manuscript/manuscript.pdf` - compiled review PDF

## Bug reports / reproducibility questions

Please use the repository issue tracker:

https://github.com/Wujijiandao/gtco-dyson-selection-calibration/issues

## Citation

For the frozen numerical-reproduction snapshot underlying the reported results, cite Zenodo DOI `10.5281/zenodo.21896997`. A new archival release should only be created after the RASTI submission version is formally frozen.
