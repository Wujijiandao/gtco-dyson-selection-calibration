# GTCO Dyson-Sphere Selection Calibration — v2.4 PRE-ZENODO

Reproducibility repository for the MNRAS manuscript:

**From Dyson-sphere candidates to population constraints: calibrating selection and conditional real-image response in Gaia–2MASS–WISE searches**

Author: **Yuzhan Zhang**  
ORCID: https://orcid.org/0009-0000-3121-7972  
Independent Researcher, Beijing, China

## Scientific state

The current release candidate is deliberately narrower than earlier drafts:

- conditional ten-band SED response remains ~0.91 under noise, W2/template and WISE broad-band colour-correction sensitivities;
- 0.414 is coupling to the **baseline observed host gate**, not counterfactual host completeness;
- W3 remains robust over the stated real-image PSF challenge family;
- W4 is explicitly PSF/operator sensitive and is not assigned a robust completeness scalar;
- representative field-environment completeness and final Hephaistos-II operator completeness remain unmeasured;
- no Dyson-sphere occurrence rate is reported.

See `CLAIM_BOUNDARIES.md` and `TEST_STATUS.md` before citing numerical values.

## Reproduction

Core + referee-hardening workflow:

```bash
python run_all.py /path/to/frozen_data_root
```

The default workflow includes:

- input/hash verification;
- deterministic baseline host cuts;
- full 220,745-model / 54-cell catalogue reconstruction;
- real-image LOHO analysis;
- host-level statistics;
- metric/threshold ablation;
- photometric-noise bracket;
- disjoint and continuous PSF-mismatch challenges;
- source-cluster bootstrap;
- WISE blackbody colour-correction/isophotal-wavelength sensitivity;
- all-band-unsaturated validation-subset sensitivity.

`10_variant_template_reconstruction.py` is a helper for the frozen alternative template/validation tables and is run explicitly because its input tables must be named.

Large public survey inputs are not redistributed; manifests, hashes and regeneration paths are provided.

## Manuscript

The current pre-Zenodo manuscript and second simulated referee review are under `manuscript/`.

## Release sequence

1. Push this v2.4 update to the existing public GitHub repository.
2. Inspect the public snapshot.
3. Create release/tag `v1.0.0-submission`.
4. Archive that exact release with Zenodo.
5. Insert the minted DOI into README/CITATION/manuscript Data Availability and add the formal software citation.

Do not archive an older repository state as the submission DOI.
