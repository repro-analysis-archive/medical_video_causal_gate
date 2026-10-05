# SS protocol DS203: code-lock record (§14 step 2)

* **Task:** `CC_TASK_SS_code_lock_after_partB_v3.md`.
* **Protocol:** `docs/SS_PROTOCOL_DS203.md`, frozen at 4c86dc5 (unchanged; sha256 cd7e1402…d748926).
* **This commit:** the commit that adds this file is the **final code-lock commit**. It contains run records, notes and this record only, with no code change.

## 1. Exact SDR implementation commit (§9)

* **Commit:** `af56777e0f52b5c350dd7ba557d55b2394cbd4bf`, the pre-gate implementation commit / SDR_IMPLEMENTATION_CANDIDATE_COMMIT.
* **Superseded, never Part B run:** `16af878`, `338768c` and `05822ee` (reasons: `docs/CODELOCK_NOTES.md` §5).
* **Before the causal grid:** the run record of §14 step 6 must reference this commit.

## 2. Verification

* **HEAD:** af56777; tracked files unmodified. The only untracked files were the Part B outputs in `results/codelock_gate/`.
* **Part B timing:** one run, 2026-10-05 15:33:36 → 15:57:17 +0900, runner exit 0, 20 workers. Stages ended in order: gate 15:49:24, projection 15:57:16, G-SITE, small truth, then the record at 15:57:16.
* **Units:** 1,200 / 1,200 gate units and 1,026 / 1,026 timing units; no partial files.
* **No code changed during Part B:**
  * The executed snapshot `results/codelock_gate/code_snapshot` (COMMIT = af56777) is byte-identical to `git archive af56777` of `ss_benchmark/`, `scripts/` and the three design files.
  * The reflog shows no commit or checkout after 15:25:58.
  * No code file was modified after 15:11.

## 3. Results

**(a) Estimator gate (§9):**
* Setup: FULL arm, learner mode "select", fully synthetic PLACEHOLDER design (n = 158, synthetic centres / offsets), M = 200 per cell, W = 5, α = 0.5, γ = 1, φ_A = 0.
* Criteria: coverage ∈ [0.90, 0.99], |bias| < 5 % of the mean true contrast, and every replicate finite.

| cell | K | P | coverage | mean truth | bias | \|bias\| / truth | finite | verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 9 | 1 | 0 | 0.930 | 0.07428 | −0.00040 | 0.0054 | 200 / 200 | PASS |
| 27 | 1 | 5 | 0.925 | 0.07385 | −0.00146 | 0.0197 | 200 / 200 | PASS |
| 117 | 5 | 0 | 0.950 | 0.38781 | +0.00216 | 0.0056 | 200 / 200 | PASS |
| 135 | 5 | 5 | 0.905 | 0.39186 | +0.01152 | 0.0294 | 200 / 200 | PASS |
| 171 | 15 | 0 | 0.915 | 1.29948 | +0.02364 | 0.0182 | 200 / 200 | PASS |
| 189 | 15 | 5 | 0.935 | 1.29961 | +0.00598 | 0.0046 | 200 / 200 | PASS |

* **Gate: PASS.** The metrics were recomputed independently from the 1,200 replicate rows and reproduce the aggregated file.

**(b) Compute projection (§10.4):**
* Method: 1,026 PLACEHOLDER SDR timing fits (every K, W, arm and learner mode, plus the §10.3 configurations), measured with all 20 workers busy. The projection covers the full grid plus §10.3: 700,800 SDR fits.
* Projected wall time:

  | reductions | days |
  |---|---:|
  | none | 5.99 |
  | (a) | 4.54 |
  | (a)+(b) | 3.20 |
  | (a)+(b)+(c) | 3.17 |

* **Projection: PASS (5.99 ≤ 7 days); no frozen reduction applied.** Recomputed independently from the timing table: 5.990 days.

**(c) G-SITE (§5.4; real centre + offset only):**
* η² of S at the window start on C: primary 0.00141 (0.0014), W0 0.00366, W5 0.00449. All ≤ 0.01.
* PASS; the per-W P2 sensitivity results are instrument-like.

**(c2) Small-truth design check (§11):**
* Rule: flag if min over the 24 site-loading permutations of |Ψ(δ) − Ψ(1)| < 0.025.
* **0 flagged cells**:

  | set | cells | flagged |
  |---|---:|---:|
  | primary | 240 | 0 |
  | single-file | 66 | 0 |
  | W0 | 54 | 0 |
  | W5 | 6 | 0 |

* The exact truth values are only in `results/codelock_gate/provenance_small_truth_values.json`.

**(d) Pass / fail record:** `results/codelock_gate/codelock_passfail_record.json`:
* `a_estimator_gate.pass_` = true;
* `b_compute_projection.pass_` = true, reductions_applied = [];
* `c_gsite.pass_primary` = true, per_W W0 / W5 = true;
* `c2_small_truth.n_flagged_total` = 0;
* `code_lock_may_proceed` = true.

## 4. Code-lock status

* **Code lock (§14 step 2) is complete.** The implementation, synthetic dry run, estimator gate, compute projection, G-SITE and the small-truth flag are all recorded.
* **Checkpoint coverage:** verified at af56777 (21 reachable checkpoints; `docs/codelock_checkpoint_manifest.json`).
* **Retrieval rule:** the no-third-party-retrieval rule of CODELOCK_INCIDENT_001 ends with this commit. Any later retrieval still uses the weight-free mechanism of `scripts/fetch_third_party.sh`.
* **Next:** §14 step 3 (ranking, GPU-memory feasibility and extraction projection, with no DS203 frame) is not started. It begins only when instructed.
