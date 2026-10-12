# §14 step 4 record (written by scripts/run_step4_5.sh)

* Code: expected commit `9e1aa715af3067a912bb69733ab79df106877b53` (run from a code snapshot; `run_meta.json`).
* 4a mask check: `mask_check.json` (locked `pipeline mask-check`; validity checked against the frozen rule).
* 4b extraction: four arms x 278 cases; `representation_manifest.json` lists 1668 files (path, shape,
  dtype, SHA-256), relative to `/media/user/LaCie/medvideo_gate/ss_step4_5`; the locked per-arm manifests are in `extract_manifests/`.
* Near-uniform: `near_uniform.json` (locked `pipeline near-uniform` on the primary standardized arm); per-frame flags
  are the `*.near_uniform.npy` files in the manifest.
* Staging: `staged_manifest.json` (archive members byte-copied, CRC-32 checked; no re-encoding).
* This record is committed before step 5 starts (execution-order safeguard).
