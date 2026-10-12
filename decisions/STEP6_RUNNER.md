# STEP6_RUNNER: §14 step 6 runner (orchestration only) and the step 5 → 6 transition

* **Drafted:** 2026-10-07, in `/srv/ss_step6_prep/` while computation A (the step 4–5 runner, launch commit `9e1aa71`) was running. The repository was not touched.
* **Authority:** `CC_TASK_SS_step6_chain_prep_v1.md`. The investigator is the sole approver.
* **Base:** frozen protocol `4c86dc5`; SDR implementation commit `af56777`; final code lock `98cba1e`; step 4–5 runner `9e1aa71`.

## 1. Can steps 5 → 6 be chained without human judgement?

**Answer: yes.**
* Step-5 outcomes and §13 change only interpretation, claims and which families are tested at §14 step 7.
* They never change which arms, cells, replicates or learners step 6 computes.
* §13 can be applied mechanically from the locked pass fields.

**Q1. Do E1–E3 or §13 change what step 6 computes?** No.
* What step 6 computes is fixed by:
  * §10.1: "K ∈ {1, 2, 5, 15}; P ∈ {0, 5, 30}; W ∈ {0, 5, 30}; α ∈ {0, 0.5, 1}; γ ∈ {0.5, 1}. That is 216 cells", plus the 24 φ_A cells;
  * §10.2: "M = 200 synthetic replicates per cell";
  * §8: the arms;
  * §9: the learners;
  * §10.3: the sensitivity sets;
  * §10.4: the only reductions are tied to the code-lock projection, which passed with none (`results/codelock_gate/projection_PLACEHOLDER.json`: `"projection_pass": true`, `"reductions_applied": []`).
* Every §13 consequence is a reporting or claim rule. Examples:
  * "FM-vs-FM−C comparisons are reported descriptively only";
  * "FM−C arms are not interpreted";
  * "P1b-FM / P2-FM are not tested";
  * "P2-SITE and P2-ORACLE become P3".
* "Not tested" concerns family verdicts (§12.3), which are computed from the same grid. The §12.2 family conditions name E1 / E3 / G-SITE; the cells and arms of every family are computed regardless ("P3 | all other cells and comparisons").
* §15 forbids "Adding arms, models or cells after step 5" and "Re-running extraction or the grid with different settings after seeing results".
* **In the locked code:** `grid_driver.build_units(reductions, available_arms, …)` depends only on the projection record's reductions and on which representation arms are present. The E1 / E3 conditions (`--conditions`) are read only by `grid_driver.aggregate`, i.e. by the family verdicts.

**Q2. What does "apply §13 before any causal run" require, and is it mechanical?** It means evaluating each §13 rule against the step-5 record and fixing the resulting claim ceilings and family-test conditions before the grid runs. Every rule's condition is a criterion of §5 that the locked checks already decide:

| §13 condition | locked field (`checks.json`) |
|---|---|
| "E1 fails (standardized, 278-case set)" | `E1_278.pass` (P, S, REF) |
| "E2 fails" | `E2_primary.pass` (§5.2 primary) |
| "E3-site fails on the 278-case set" | `E3_site_278.pass` |
| "E1 and E3-site pass on the 278-case set but fail on the 158-case set" | `E1_278`, `E3_site_278`, `E1_primary`, `E3_site_primary` pass fields; "fail on the 158-case set" is read as "do not both pass", as in the §12.2 conditions and the locked `fm_conditions` |
| "E3-site passes but the MLP probe exceeds the margin" | `E3_site_<set>.pass` and `.mlp_exceeds_margin` (post-removal MLP probe in `checks.e3_site`) |
| "E3-state-retention fails" / "not applicable" | `E3_state_primary.applicable`, `.pass_` |
| "G-SITE fails" | `gsite_record.json` `gate_pass_primary` (code lock: passed, η² = 0.0014) |
| P1b-FM / P2-FM conditions (§12.2) | `fm_conditions_primary` (key P) |

* Two §13 items need the family verdicts and are recorded as deferred to step 7:
  * "E1 and E3 … pass but P1b-FM and P2-FM are INCONCLUSIVE";
  * the family-verdict wording.
* The remaining items are standing wording rules with no step-5 condition.
* `scripts/apply_section13.py` implements this table. It reads booleans only (it STOPs on a non-boolean), introduces no threshold, and writes `results/step5/{SECTION13_RECORD.md, section13.json, grid_conditions.json}`. `grid_conditions.json` is the locked driver's `--conditions` input, used at step 7.

**Q3. Does §14 require anything between steps 5 and 6 beyond committing the step-5 record and applying §13?** No.
* Step 5: "Run E1–E3 on the 278-case and 158-case sets, commit, and apply §13 before any causal run."
* Step 6: "Confirm that the SDR commit recorded at step 2 is the one in use, then run the causal grid (and §10.3) and commit."
* The SDR confirmation is part of step 6 itself; the runner performs it (§3).

## 2. Worker count

**How the code-lock projection was obtained** (`results/codelock_gate/projection_PLACEHOLDER.json`, `CODELOCK_FINAL_RECORD.md`):
* 1,026 PLACEHOLDER SDR timing fits, "measured with all 20 workers busy": 20 pool workers, no CPU pinning, on all 20 logical CPUs (6 P-cores × 2 threads + 8 E-cores).
* Method: "Σ over cells, arms and §10.3 runs of M × mean measured wall time per SDR fit …, divided by the number of worker processes".
* Result: 517,549 s = **5.99 days** for the full grid plus §10.3 (700,800 SDR fits), with no reduction.

**Projection for 16, 18 and 20 workers.** Two assumptions:
* (i) per-fit time unchanged from the 20-busy measurement, so wall time ∝ 1 / workers;
* (ii) a capacity model: a P-core counts 1.0, its second hardware thread +0.3, an E-core 0.6. 20 workers = 12.6 units. The workers are pinned to the first N logical CPUs (P-core threads first, then E-cores).

| workers | CPUs | (i) | (ii) |
|---:|---|---:|---:|
| 20 | 0–19 | 5.99 d | 5.99 d (measured) |
| **18** | 0–17 (CPUs 18–19 reserved) | 6.66 d | 6.62 d |
| 16 | 0–15 | 7.49 d | 7.40 d |

* Fewer busy workers may shorten each fit a little (less memory-bandwidth contention), so both models lean long.
* The 7-day budget is the §10.4 code-lock projection criterion, already passed; it is not a run-time stop rule.

**Recommendation: 18** (the investigator's default).
* About 6.6–6.7 days.
* Leaves two E-cores to the OS, the orchestrator and its memory guard.
* 20 saves about 0.6 day but leaves no headroom; 16 projects past 7 days.

**Worker count does not change results.**
* Code-lock determinism test (`decisions/CODELOCK_PARTA_TEST_RECORD.md`, test 6): "Byte-identical outputs from two runs (3 and 5 workers) of: the gate stage …; G-SITE; the small-truth design check; and the PLACEHOLDER dry run".
* The grid driver has the same structure: one SeedSequence(20261007, (cell, replicate)) per unit, one BLAS thread per process, one shard per unit.
* Confirmed directly for the driver in the smoke test (§5): shards from 2 workers (interrupted and resumed) and from 1 worker (uninterrupted) were byte-identical.

## 3. The runner (orchestration only)

**Files:**
* `scripts/run_step6.sh`: entry point, run lock, `--status`, `--stop`.
* `scripts/step6_orchestrate.py`: preconditions, snapshot, retries, memory guard, logging, record, status.
* `scripts/step6_grid_units.py`: runs the locked `grid_driver.main` unchanged, after replacing the module attribute `grid_driver.aggregate` by a logging no-op.
* `scripts/apply_section13.py`: mechanical §13 (§1).
* `tests/test_step6_runner.py`: 8 fast tests.

**What it runs.** The locked `ss_benchmark.grid_driver`:
* real design, replicate root 20261007;
* 240 primary cells × all arms × M = 200, plus §10.3 single-file, W0 and W5;
* each (set, cell, replicate) unit written as one shard; a resume skips finished shards.

**§14 step 7 is never run.** `replicates.csv`, `cell_metrics.csv` and `families.json` (family verdicts) are produced only by `aggregate`, which is suppressed. Step 7 later runs the locked `main` with the same arguments: every shard exists, so it only aggregates.

**Preconditions** (refused with exit 3, nothing changed; the same on resume):
* HEAD = `--expect-commit`, and HEAD contains the runner;
* clean tree, with no untracked file either;
* step-5 record and §13 record committed;
* **SDR commit in use:** `ss_benchmark/` is byte-identical to `af56777` except `ss_benchmark/models/prim_caformer.py` (CODELOCK_CORRECTION_001, an extraction adapter the grid does not import);
* the reps file matches the SHA-256 in the committed `step5_manifest.json`;
* the projection record shows a pass with no reduction;
* no process of an earlier step-6 run is alive;
* a completed run is refused.

**Settings:**
* code-lock thread settings: `OPENBLAS / OMP / MKL / NUMEXPR_NUM_THREADS=1`, `PYTHONHASHSEED=0`, `/home/user/miniconda3/bin/python3`;
* `--workers 18` pinned to CPUs 0–17; the orchestrator runs on CPUs 18–19;
* resident-memory cap: 80 % of 125.6 GiB.

**Memory guard:**
* Pressure means any of:
  * `MemAvailable` < 5 % of RAM;
  * PSI `/proc/pressure/memory` "full avg60" ≥ 10 %;
  * the run's resident memory exceeds the cap.
* Three consecutive 15-s checks with pressure stop the runner (resumable).
* Swap-out is not a criterion: the step 4–5 guard's swap-out rule stopped A on 6 Oct with about 80 GiB available (`OPERATIONS_LOG_STEP4_5.md`). A unit test pins that situation as "no pressure".

**Stability and logging:**
* Failures are retried with backoff of 60, 300 and 900 s; three consecutive failures without progress STOP the runner.
* `logs/progress.log` gets events plus a `RES` sample every 10 min: CPU, load, RAM, PSI, run RSS, swap, GPU, CPU temperature, disk.
* The driver's own output goes to `logs/grid.log`.
* `--status` shows unit counts and the last resource sample only, never an estimate, metric or verdict.

**Completion record:** `step6_record/run_record.json` and `shard_sha256.txt` under the output directory. The runner never commits.

**Paths:** output `/media/user/LaCie/medvideo_gate/ss_step6/`; reps from `/media/user/LaCie/medvideo_gate/ss_step4_5/step5/reps.npz`.

## 4. Launch

```
cd /home/user/projects/medical_video_causal_gate
setsid nohup scripts/run_step6.sh --expect-commit <commit containing this record> > /dev/null 2>&1 < /dev/null &
scripts/run_step6.sh --status
scripts/run_step6.sh --stop        # resumable with the launch command
```

## 5. Smoke tests (2026-10-07; throwaway copy of the repository; FIXTURE / PLACEHOLDER only)

**Setup.**
* The repository was copied with `cp -a`. No git command was run in the original.
* In the copy, FIXTURE commits stood in for A's step-4 commit, a FIXTURE step-5 record (locked `checks.json` layout), the §13 record (written by `apply_section13.py`) and the runner files.
* Limits: 2 CPUs (18, 19), 1 BLAS thread per process. Peak summed RSS of the run was 3.35 GiB (≤ 4 GB; shared pages counted twice).

| # | scenario | result |
|---|---|---|
| R1 | `--expect-commit` ≠ HEAD | refused, exit 3 |
| R2 | untracked file / modified tracked file | refused, exit 3 (both) |
| R3 | §13 record not committed | refused, exit 3; no state created by R1–R3 |
| R4 | PLACEHOLDER grid (cell 9, 1 replicate: 3 units), 2 workers; `--stop` after the first shard | stopped ("interrupted by signal 15"), 1 / 3 units, no process left |
| R5 | resume with the same command | snapshot reused; 3 / 3 units; state `complete`; `grid/` holds only `run_plan.json` and `work/` (no `replicates.csv`, `cell_metrics.csv` or `families.json`): step 7 not run |
| R6 | relaunch after completion | refused, exit 3 ("already complete") |
| R7 | fresh 1-worker run of the same units | shards byte-identical to R4 + R5 |

* The status output showed unit counts and the resource line only.
* All smoke outputs and the copy were deleted.

## 6. Chain from step 5 (`chain_5_to_6.sh`)

**Authority.** Authorised explicitly by the investigator on 2026-10-07, including testing in throwaway copies.

**Files** (staging directory, not in the repository; the hashes are also written into the chain's commit message):

| file | SHA-256 |
|---|---|
| `/srv/ss_step6_prep/chain_5_to_6.sh` | `8a7cc80bbc2d7d2957b0b6c4c5c3d145d60115856428d9198ccfd26ae50e2309` |
| `/srv/ss_step6_prep/chain_5_to_6.py` | `ba1a0c004fe93b18c649b9da6cc998d74dd5fb7166b20a4ad3a96df569851992` |

**While A runs:**
* The chain reads only A's `state.json`, polling every 10 min, and runs no git command.
* It waits while A is running, or while A is stopped with "memory pressure".
* It exits without action (exit 2) in any of these cases:
  * A stopped for any other reason;
  * A's process is dead while its state says running (two polls);
  * A's state file is missing.

**On A's success:**
* (a) **Verify:**
  * HEAD = A's step-4 commit;
  * its parent = `9e1aa71`;
  * its prefix and its diff = exactly the ten step-4 record files;
  * the untracked files = exactly A's four step-5 record files, byte-identical to A's own copies.
* (b) Commit the step-5 record.
* (c) Run `apply_section13.py` and commit its three files.
* (d) Copy the seven runner and record files, never overwriting; the operations log gets a mechanically extracted evidence appendix. Commit them.
* Every commit is checked for parent, message prefix, exact file set and a clean tree afterwards.
* (e) Launch `run_step6.sh --expect-commit <commit (d)>`.
* (f) Verify that it is running.
* A restarted chain recognises its own commits and continues. It does not relaunch a step-6 run that is already running or complete for the same commit. It never starts §14 step 7.

**Smoke tests** (2026-10-07):
* Throwaway `cp -a` copies of the repository, each with a FIXTURE version of A's step-4 commit and FIXTURE step-5 record files; FIXTURE A states. No git command was run in the original repository.
* Step-6 launches used a tiny PLACEHOLDER grid with 1 worker on CPU 18; everything ran on CPUs 18–19.

| # | A's end state / setup | result |
|---|---|---|
| S1 | stopped, "interrupted by signal 15" | HALT, exit 2, no action; the repository copy was unchanged (HEAD, index, files) |
| S2 | state "running", process dead | HALT after two polls, exit 2, no action, copy unchanged |
| S3 | no state file | HALT, exit 2, no action, copy unchanged |
| S4 | "memory pressure" stop → relaunched (running) → complete | Waited through both states with no change in the copy (0 entries modified). Then: verified; step-5 commit (4 files, parent = A's step-4 commit); §13 commit (3 files); runner commit (7 files); each correctly parented, with the investigator's repository identity and a clean tree. The step-6 runner was launched and verified running; `run_step6.sh --stop` stopped it with no process left. |
| S5 | complete, plus an unexpected untracked file | HALT before any commit |
| S6 | complete, but a step-5 record file differs from A's copy | HALT before any commit |
| S7 | chain stopped after its first commit, then restarted; then rerun after completion | It recognised its step-5 commit and continued (§13 and runner commits, launch). The rerun made no new commit and did not relaunch the running step-6 runner (3 commits, 1 launch). |

* In an extra harness case (a "memory pressure" stop followed by a "running" state whose pid was dead), the chain halted after two polls, as specified.
* All smoke copies and outputs were deleted.

**Note.** The watchdog `~/ops/runner_watchdog_v1.sh` is not present on the machine (2026-10-07). After a "memory pressure" stop the chain keeps waiting until A is relaunched by anyone.
