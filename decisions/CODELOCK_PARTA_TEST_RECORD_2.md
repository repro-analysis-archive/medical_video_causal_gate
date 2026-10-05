# Code lock Part A: test record for the coverage-fix pre-gate implementation commit

* **Scope:** this record is committed in the pre-gate implementation commit produced under `CC_TASK_SS_code_lock_coverage_fix.md` and its addendum. That commit's hash is the SDR_IMPLEMENTATION_CANDIDATE_COMMIT; it is reported outside this file.
* **Tested tree:** every result below was obtained on the working tree committed in that commit. The only addition after the runs is this file.
* **Supersession:**
  * `338768c` is superseded before any Part B run. The reason is in `docs/CODELOCK_NOTES.md` §5.
  * The earlier record `CODELOCK_PARTA_TEST_RECORD.md` (for 338768c) is kept unchanged as history.
* **Date:** 2026-10-05.

## Changed and unchanged code (against 338768c)

* **Changed:**
  * extraction adapters: `models/sec_videomae.py`, `models/sec_omnitokenizer.py`, `models/prim_resnet50.py` (checkpoint naming only);
  * `feasibility.py` (registry);
  * `scripts/fetch_third_party.sh` (authorisation 002);
  * `tests/test_codelock_extra.py`, plus the new `tests/test_codelock_coverage.py`;
  * docs and records.
* **Unchanged (byte-identical):**
  * `sdr.py`, `learners.py`, `dgp.py`, `grid.py`, `arms.py`, `seeds.py`, `constants.py`, `design.py`, `placeholder.py`, `reduce.py`, `checks.py`, `codelock_gate.py`, `grid_driver.py`, `pipeline.py`, `dryrun.py`, `preprocess.py`, `extract.py`;
  * `scripts/run_codelock_gate.sh`;
  * `tests/test_codelock_fast.py` and `tests/test_codelock_reporting.py`.

## Results (no criterion changed)

| suite | result |
|---|---|
| A2 fast tests (`tests/test_codelock_fast.py`, base environment) | 17 / 17 passed (all seven tests), 422.7 s. Values identical to the 338768c run: truth vs MC worst 0.88 SE; SDR smoke mean bias −0.6 % with empirical coverage 1.00, reported only; LEACE accuracy 0.999 → 0.250; folds, time order and determinism pass; G-SITE η² 0.001412. |
| reporting-path and small-truth tests (`tests/test_codelock_reporting.py`) | 6 / 6 passed |
| engineering checks (`tests/test_codelock_extra.py`, extraction venv) | 32 / 32 passed. Includes: all 22 registry entries build with random weights at the frozen output dimension; spec-vs-adapter consistency; and the VideoMAE adapter reproducing the official encoder code for ViT-S / B / L / H on shared random weights (max abs diff ≤ 1e-4 asserted; observed ≤ 3.1e-6). |
| checkpoint coverage (`tests/test_codelock_coverage.py`, extraction venv) | 26 / 26 passed. Structural checks: the manifest covers every eligible candidate in d3563e7; one adapter and one spec entry per reachable checkpoint; every adapter checkpoint is in the manifest; no ambiguous identifier or alias; the VideoMAE class line is verbatim. Then each of the 21 reachable checkpoints builds with random weights and returns its documented shape. |
| adapter source quotes | 104 / 104 quotes found in their cited files |
| runner smoke test (throwaway clone) | wrong commit refused (exit 3); detached run; status showed progress only; stages (a), (b), (c), (c2) and (d) completed with exit 0; resume skipped finished units; outputs deleted; stage values not inspected |
