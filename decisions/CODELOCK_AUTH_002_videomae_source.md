# Code-lock authorisation 002: source-only retrieval of the official VideoMAE architecture definitions

* **Recorded:** 2026-10-05, before the new pre-gate implementation commit. Part B had not been run.
* **Authorisation:** the investigator, in `CC_TASK_SS_code_lock_coverage_fix.md` item 1.1 and its addendum item 1:
  > fetch, from the official VideoMAE repository at a pinned commit, only the source file(s) that define the original
  > ViT-S / ViT-H model architecture. Sparse/filtered fetch only; no weight blob may be materialized.
  >
  > Prefer retrieving the exact raw source file(s) directly from the official VideoMAE repository at the pinned
  > commit, rather than a clone or archive. Never retrieve checkpoints, LFS objects, archives, or files with
  > extensions .pth, .pt, .ckpt, .bin, .safetensors, or any evaluation weights.
* **Status:** this is the single exception to the no-retrieval rule of `CODELOCK_INCIDENT_001`. After this retrieval, the rule is restored until the final code-lock commit.

## Retrieval

| item | value |
|---|---|
| repository | https://github.com/MCG-NJU/VideoMAE (official) |
| pinned commit | `14ef8d856287c94ef1f985fe30f958eb4ec2c55d` (HEAD = refs/heads/main on 2026-10-05) |
| commit resolution | `git ls-remote https://github.com/MCG-NJU/VideoMAE.git HEAD refs/heads/main refs/heads/master` (ref names and hashes only; no objects) |
| retrieval command | `bash scripts/fetch_third_party.sh --authorized-videomae-source` |
| what that command runs, for each file f | `curl -fsSL --max-filesize 1048576 -o third_party/VideoMAE/f.part https://raw.githubusercontent.com/MCG-NJU/VideoMAE/14ef8d856287c94ef1f985fe30f958eb4ec2c55d/f` |
| what the script refuses | any name not on its two-file list or not `*.py`, and any file with a NUL byte |
| executed | 2026-10-05 14:35:38 +0900, once |
| mechanism | raw single-file HTTP retrieval; no clone, no archive, no LFS object, no checkpoint |

| file (in `third_party/VideoMAE/`) | bytes | SHA-256 | why it is needed |
|---|---:|---|---|
| `modeling_pretrain.py` | 13,810 | `5689f93f72d7764d13e27f17ca3a6a096c89e7ee0e3fd8e63dffde6ab11ad593` | defines the pre-training models `pretrain_videomae_{small,base,large,huge}_patch16_224` |
| `modeling_finetune.py` | 13,303 | `ce9a11ff05c7a1b5085addf6c73b71ffb68933564164f7b250dedad91f6e29b8` | defines `Block`, `Attention` (q / v biases), `PatchEmbed`, `get_sinusoid_encoding_table` and `_cfg`, which `modeling_pretrain.py` imports; the encoder architecture is not defined without it |

* **Hash pinning.** The two SHA-256 values are pinned in `scripts/fetch_third_party.sh`. Any re-run verifies them, and a mismatch is refused.
* **Not committed.** The files live in the git-ignored `third_party/` and are not committed. They are reproducible with the command above.

## Post-fetch scan

```
third_party/VideoMAE/modeling_finetune.py: Python script, ASCII text executable
third_party/VideoMAE/modeling_pretrain.py: Python script, ASCII text executable
weight-type files under third_party/ (*.pt *.pth *.ckpt *.bin *.safetensors *.pkl *.npz *.onnx *.h5 *.torch): 0
```

## Use

* **What was read from the files** (rule R1):
  * the architecture of the four sizes: embed / depth / heads = S 384 / 12 / 6, B 768 / 12 / 12, L 1024 / 24 / 16, H 1280 / 32 / 16;
  * mlp_ratio 4; q and v biases; LayerNorm eps 1e-6; no layer scale; patch 16; tubelet 2; 16 frames; sinusoid positions;
  * the model `default_cfg` normalisation, mean / std (0.5, 0.5, 0.5).
* **Adapter.** `ss_benchmark/models/sec_videomae.py` implements these values with transformers' VideoMAEModel. It does not import the retrieved files.
* **Equivalence.** `tests/test_codelock_extra.py::test_videomae_adapter_matches_official_encoder` executes the retrieved code on random weights and checks that the adapter reproduces the official encoder for ViT-S / B / L / H (max |diff| ≤ 3.1e-6).
* **No weights involved.** No VideoMAE checkpoint was downloaded or used.
