# Code lock Part A: test and dry-run record (remediated pre-gate implementation)

* **Scope:** this record is committed in the remediated pre-gate implementation commit. That commit's hash is the SDR_IMPLEMENTATION_CANDIDATE_COMMIT; it is reported outside this file, because a commit cannot contain its own hash.
* **Tested tree:** every result below was obtained on the working tree committed in that commit. The only addition after the runs is this file.
* **History:**
  * The superseded candidate `16af878b802b2d838461101b57b2427ed29fa5ea` is historical; its Part B was never launched.
  * The remediation follows `SS_CODELOCK_PARTA_AUDIT_REMEDIATION.md` (HOLD PART B).
* **Date:** 2026-10-05.

## 1. The seven A2 fast tests

* **Run:** `tests/test_codelock_fast.py`, base environment, OPENBLAS/OMP/MKL threads = 1.
* **Result:** 17 parametrised cases, all PASSED, in 422.6 s.
* **Criteria:** unchanged from `CC_TASK_SS_code_lock_v2.md`; seeds and N are recorded in the test file.

| test | result |
|---|---|
| 1. Truth vs Monte Carlo (6 cells, N = 10⁶ each) | PASS. \|truth − MC\| / SE = 0.47, 0.23, 0.88, 0.39, 0.09, 0.27 (limit 4 SE + 1e-8). |
| 2. SDR smoke test (2,000 cases, M = 20, FULL arm) | PASS. Everything finite; SEs > 0; density ratios in [0.584, 2.543]; mean bias −0.0022 = −0.6 % of the mean truth 0.3969 (limit 10 %). Empirical 95 % coverage 1.00 (20 / 20); reported only, not a criterion and not a second gate. |
| 3. LEACE | PASS. Balanced accuracy 0.999 before removal and 0.250 after; identities ≤ 2.2e-15; rank 3. |
| 4. Folds | PASS. The primary, W0, W5 and single-file sets equal the 278-case labels restricted (real case IDs only). |
| 5. Time order | PASS. Six synthetic timestamp sets; L ∈ {1, 8, 10, 16, 17, 33, 64}; the Cosmos native selection checked too. |
| 6. Determinism | PASS. Byte-identical outputs from two runs (3 and 5 workers) of: the gate stage (smoke: 6 cells × 2 replicates); G-SITE; the small-truth design check; and the PLACEHOLDER dry run. The dry run includes every reporting-only path through `pipeline.run_checks` / `pipeline.near_uniform`. |
| 7. G-SITE | PASS. η² = 0.001412 → 0.0014. |

## 2. Synthetic dry run (§14 step 2)

**`python -m ss_benchmark.dryrun`** (PLACEHOLDER; no DS203 frame, representation or metadata). It executed to completion on the PLACEHOLDER 278 / 158 / 123-case sets:
* fold-wise PCA (64) and LEACE;
* E1, E2, E3-site (linear and MLP), E3-state-retention and the FM conditions;
* the reporting-only paths: pre-removal MLP site probe, E2 on all 278 videos, E2 with past actions (reference cell K = 5, P = 0, W = 5, α = 0.5, γ = 1, first replicate), and the normalised-time reference;
* the near-uniform summary on synthetic flags;
* a six-arm causal run with the §12.3 aggregation.

Its output was byte-identical across two runs (fast test 6).

**Runner projection stage:** an all-arm SDR dry run on PLACEHOLDER features. It executed in the runner smoke test (§5 below).

## 3. Remediation tests

* **Run:** `tests/test_codelock_reporting.py`, base environment.
* **Result:** 6 passed.
* **What is covered:**
  * the exact near-uniform summary on a hand-computed example;
  * E2 rows and normalised time;
  * the history (lag) matrix against a direct computation;
  * the reporting marker that drops `pass`;
  * small truth: the permutation truth equals the replicate truth, the check is deterministic, and the flag both triggers and stays clear when it should.

## 4. Extra engineering checks

* **Run:** `tests/test_codelock_extra.py`, extraction venv.
* **Result:** 25 passed.
* **What is covered:**
  * all 19 registry entries build with random initialisation and encode synthetic input on CUDA in bf16, and their output dimension equals the frozen extraction specification. These are code-path checks only, not the §4.1.4 rule-4 determination;
  * the specification covers exactly the registry and agrees with every adapter;
  * the extraction-projection code path;
  * the decode, grid, standardize and extract path on a synthetic lavfi video;
  * the pipeline glue: streaming extraction on a synthetic multi-file case matches the direct computation; the Cosmos path; build-reps, then checks (including every reporting-only key, which carries no `pass` field), then loading by the grid driver.

## 5. Runner smoke test (A3)

* **Where:** run in a throwaway local clone, so the project repository got no extra commit. Smoke outputs deleted afterwards.
* **Refusal:** it refuses a wrong `--expect-commit` (exit 3).
* **Detached run:** `setsid nohup` launch; status showed progress only.
* **Stages:** (a) gate, (b) projection, (c) G-SITE, (c2) small-truth design check and (d) record all completed, exit 0.
* **Resume:** a resumed run skipped every finished unit.
* **Smoke values:** the stage values from the smoke run were not inspected, beyond confirming that the files and keys exist.
