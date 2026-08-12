# GTCO Dyson-Sphere Selection Calibration

Reproducibility repository for the MNRAS manuscript:

**From Dyson-sphere candidates to population constraints: calibrating selection and conditional real-image response in Gaia–2MASS–WISE searches**

Author: **Yuzhan Zhang**  
ORCID: https://orcid.org/0009-0000-3121-7972  
Independent Researcher, Beijing, China

## Frozen submission release

The submission-critical software/reproduction snapshot is permanently archived as:

- Version: `v1.0.0-submission`
- Zenodo DOI: https://doi.org/10.5281/zenodo.21896997
- DOI: `10.5281/zenodo.21896997`
- GitHub repository: https://github.com/Wujijiandao/gtco-dyson-selection-calibration

The GitHub tag `v1.0.0-submission` is frozen and should not be moved or overwritten. The `main` branch may continue to receive documentation or post-submission updates.

## Scientific state

- conditional ten-band SED response remains ~0.91 under noise, W2/template and WISE broad-band colour-correction sensitivities;
- 0.414 is coupling to the **baseline observed host gate**, not counterfactual host completeness;
- W3 remains robust over the stated real-image PSF challenge family;
- W4 is explicitly PSF/operator sensitive and is not assigned a robust completeness scalar;
- representative field-environment completeness and final Hephaistos-II operator completeness remain unmeasured;
- no Dyson-sphere occurrence rate is reported.

See `CLAIM_BOUNDARIES.md` and `TEST_STATUS.md` before citing numerical values.

## Reproduction

```bash
python run_all.py /path/to/frozen_data_root
```

Large public survey inputs are not redistributed; manifests, hashes and regeneration paths are provided.

## Citation

Please cite the frozen Zenodo release for the software/reproduction package. The repository root also contains `CITATION.cff` for machine-readable citation metadata.
