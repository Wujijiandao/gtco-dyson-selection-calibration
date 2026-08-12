# GitHub + Zenodo publishing checklist

1. Create a **public** GitHub repository named:
   `gtco-dyson-selection-calibration`

2. Upload the contents of this folder, not the enclosing folder itself.

3. Replace:
   `Wujijiandao`
   in `CITATION.cff` with your GitHub username.

4. Commit and push.

5. On GitHub, create release/tag:
   `v1.0.0-submission`

6. Connect the repository to Zenodo and archive that release.

7. Zenodo will mint a DOI. Add that DOI to:
   - the manuscript Data Availability statement;
   - this README;
   - `CITATION.cff` as `identifiers`;
   - the final bibliography/software citation if desired.

8. Do not modify the archived `v1.0.0-submission` release. Future changes should use a new version, e.g. `v1.0.1` or `v1.1.0`.

Author identity:
- Yuzhan Zhang
- ORCID https://orcid.org/0009-0000-3121-7972
- Independent Researcher
