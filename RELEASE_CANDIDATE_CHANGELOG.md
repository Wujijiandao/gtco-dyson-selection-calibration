# Release-candidate changelog

Changes since the initially uploaded GitHub snapshot:

- manuscript expanded from the early 6-page draft to a 10-page MNRAS Paper;
- literature expanded to 28 cited references;
- abstract reduced to MNRAS Paper guidance (<250 words);
- explicit selection-conditioning table and discussion added;
- LOHO host-level figure and score-change figure replace emulator-era image figures;
- pseudo-chi-square terminology corrected for correlated AllWISE pixels;
- metric/threshold ablation added as `scripts/05_image_metric_threshold_robustness.py`;
- claim boundaries updated;
- referee precheck and manuscript changelog added.

Push these changes to the existing public GitHub repository before creating `v1.0.0-submission` and before enabling/archiving the release in Zenodo.

- added `scripts/02b_e12c_e17f_source_level_reconstruction.py`, closing the remaining headline-result reproducibility gap;
- added source-level case table, reconstruction surface, constants, and audit outputs;
- `run_all` now rebuilds E12c/E17f catalogue results before the real-image stages.
