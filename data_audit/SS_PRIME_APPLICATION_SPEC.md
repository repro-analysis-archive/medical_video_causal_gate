# SS' Application Spec (Amendment 1 with Amendment 2; Decision 001)

Committed before the single application of the SS' arm, after the Semantic Scholar arms of gate §6 and §3 have run
and before any filtering or ranking of the candidate pool. It fixes only mechanics that the amendments leave open.

## 1. Candidate pool

* Every dataset in the `dd142f6` audit log (`data_audit/DATASETS.json`, 194 entries).
* Plus every **new** C-COL or C-SURG dataset found by the Semantic Scholar dataset arm (`runs/dataset_records_s2.json`,
  screened in `screening/ds_s2_batch_decisions.json` with `existing_id` null).
* Each new dataset is audited under v4 D1–D7 with the same template and instructions as the 194 entries
  (`AUDIT_TEMPLATE.md`, `audits/AGENT_INSTRUCTIONS.md`), **before** this application runs.

## 2. Requirements (Amendment 1 SS' arm, plus Amendment 2)

* **v4 criteria:** D3 PASS, D5 PASS, D6 PASS, D7 PASS, and ≥ 200 trajectories PASS.
  * For DS024, the lead verification (`dd142f6`) applies: 162 contiguous cases, so ≥200 FAIL.
* **Amendment 2:** "video recorded in vivo from human patients during clinical procedures". Judged **only for
  datasets passing the v4 part**, from documentation or saved files, with a verbatim quote and its source.
  * PASS only if the documentation states clinical procedures on human patients for the trajectories counted.
  * Simulation, phantom, ex vivo, animal, or undocumented → not PASS (UNKNOWN is not PASS).
  * A dataset that mixes clinical and non-clinical recordings counts only its documented clinical trajectories toward
    ≥ 200. If they cannot be separated from the documentation, it does not pass.
* **D4 and D8** are replaced by the synthetic factor (Amendment 1), so they are not required.

## 3. Ranking (Amendment 1), applied once

1. Total trajectories: the counted trajectories under §2.
2. Then D7 annotation density: the fraction of frames carrying the D7 variable, from the documentation or the saved
   annotation files. Used only if step 1 ties.
3. Then access without registration (no registration ranks above registration).
4. A remaining tie goes to human decision.

* **None passes:** STOP for human decision.
* **Not done here:** no video download beyond one sample per dataset, no computation on video, no representation
  extraction. The Amendment 1 encoding check is not run (it needs a representation, which needs a protocol).

## 4. Record

`data_audit/SS_PRIME_RESULT.md`: every pool member's v4-part verdicts and, where reached, the Amendment 2 verdict with
its quote; then the ranking and either the selected dataset or STOP.
