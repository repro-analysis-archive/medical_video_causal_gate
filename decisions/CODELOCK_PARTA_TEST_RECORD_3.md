# Code lock Part A: test record for the VideoMAE-normalisation pre-gate implementation commit

* **Scope:** this record is committed in the pre-gate implementation commit produced under `CC_TASK_SS_code_lock_videomae_norm.md`. That commit's hash is the SDR_IMPLEMENTATION_CANDIDATE_COMMIT; it is reported outside this file.
* **Tested tree:** every result below was obtained on the working tree committed in that commit. The only addition after the runs is this file.
* **Supersession:**
  * `05822ee` is superseded before any Part B run. The reason is in `docs/CODELOCK_NOTES.md` §5.
  * Earlier records are kept unchanged as history.
* **Date:** 2026-10-05.

## Changed and unchanged code (against 05822ee)

* **Changed:**
  * `ss_benchmark/models/sec_videomae.py`: mean / std (0.485, 0.456, 0.406) / (0.229, 0.224, 0.225) from the pre-training pipeline, plus sources and note;
  * `scripts/fetch_third_party.sh`: authorisation 003 mode and pinned hashes;
  * `tests/test_codelock_extra.py`: one new check;
  * docs and records.
* **Unchanged (byte-identical):** every estimator, gate, projection, G-SITE, small-truth and runner file, the registry (`feasibility.py`), `tests/test_codelock_fast.py`, `tests/test_codelock_reporting.py` and `tests/test_codelock_coverage.py`.

## Results (no criterion changed)

| suite | result |
|---|---|
| A2 fast tests | 17 / 17 passed (all seven), 427.8 s. Values identical to earlier runs: truth vs MC worst 0.88 SE; SDR smoke mean bias −0.6 % with coverage 1.00, reported only; LEACE 0.999 → 0.250; G-SITE η² 0.001412. |
| reporting-path and small-truth tests | 6 / 6 passed |
| engineering checks (extraction venv) | 33 / 33 passed. Includes the new `test_videomae_normalisation_matches_pretraining_pipeline`: the adapter's mean / std equal the literals of `DataAugmentationForVideoMAE` in the retrieved, hash-pinned `datasets.py`. |
| checkpoint coverage (extraction venv) | 26 / 26 passed (21 reachable checkpoints) |
| adapter source quotes | 112 / 112 quotes found in their cited files |
| runner smoke test (throwaway clone) | wrong commit refused (exit 3); detached run; status showed progress only; stages (a), (b), (c), (c2) and (d) completed with exit 0; resume OK; outputs deleted; values not inspected |
