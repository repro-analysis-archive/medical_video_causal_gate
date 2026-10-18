# §14 step 7 record (written by scripts/run_step7.sh)

* Step 6: launch commit `7adaf133f8eaac9cf790d5320c2dd4b48d0b05cc`; 73200 unit shards, digest `cccba345778652c1fdc7a1a2604a5b800b2eb088d8f24a6aa2738b025362da49`
  (`results/step6/shard_sha256.txt.gz`, `results/step6/run_record.json`).
* Aggregation: the locked `ss_benchmark.grid_driver.main` from the step-6 code snapshot with the step-6 arguments
  (`step7_manifest.json`); every shard existed, none was recomputed (digest and run plan unchanged).
* `families.json`: §12.3 family verdicts (primary set; §10.3 sets reported separately, never entering verdicts).
* `cell_metrics.csv`: §11 metrics per set, cell and arm. `replicates.csv` stays with the step-6 output (SHA-256 in
  `step7_manifest.json`).
* Committed automatically, records only, before the report is written. §13 claim ceilings: `results/step5/section13.json`
  and the deferred rules, applied by `make_report.py`.

