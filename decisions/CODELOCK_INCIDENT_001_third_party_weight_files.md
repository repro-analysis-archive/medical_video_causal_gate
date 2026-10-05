# Code-lock incident 001: evaluation-tool weight files delivered with third-party source code

* **Classification:** procedural hard-limit incident. The code-lock task (`CC_TASK_SS_code_lock_v2.md`, hard limit 1) says "No model weights are downloaded".
* **Scientific materiality:** none identified (see "Consequence").
* **Recorded:** 2026-10-05, before Part B and before the remediated pre-gate implementation commit. This record is not edited after it is committed; any correction goes in a separate record.

## What happened

* **Retrieval.** On 2026-10-05, during code-lock Part A, the source code of four secondary-model repositories was retrieved with `git clone --depth 1`. The purpose was to build randomly initialised architectures for the extraction adapters:

  | repository | commit |
  |---|---|
  | FoundationVision/OmniTokenizer | 701b619003b3e941e769269c7626dbf111d0377e |
  | PKU-YuanGroup/WF-VAE | d858bee85324341388f2dd1a51a9bd76a4cda4e2 |
  | hywang66/LARP | 8aaed63354c8c0fabcb8a86a2e31c34320e6db86 |
  | westlake-repl/LeanVAE | 62f7c7d560b83f408b5041f799d70317d9b37713 |

* **What arrived with the code.** Three of these repositories keep weight files for their evaluation tools under version control. The shallow clones therefore delivered them, bundled with the code:

  | size (bytes) | file (relative to the clone) | type |
  |---:|---|---|
  | 50,939,526 | OmniTokenizer/OmniTokenizer/fvd/i3d_pretrained_400.pt | I3D network for the FVD metric |
  | 50,939,526 | OmniTokenizer/evaluation/common_metrics_on_video_quality/fvd/videogpt/i3d_pretrained_400.pt | I3D (FVD) |
  | 51,235,320 | OmniTokenizer/evaluation/common_metrics_on_video_quality/fvd/styleganv/i3d_torchscript.pt | I3D TorchScript (FVD) |
  | 7,289 | OmniTokenizer/OmniTokenizer/modules/cache/vgg.pth | LPIPS linear-layer weights |
  | 51,235,320 | LARP/utils/fvd/i3d_torchscript.pt | I3D TorchScript (FVD) |
  | 50,939,526 | LeanVAE/evaluation/eval/fvd/videogpt/i3d_pretrained_400.pt | I3D (FVD) |
  | 51,235,320 | LeanVAE/evaluation/eval/fvd/styleganv/i3d_torchscript.pt | I3D TorchScript (FVD) |
  | 7,289 | LeanVAE/LeanVAE/modules/cache/vgg.pth | LPIPS linear-layer weights |
  | 7,289 | LeanVAE/generation/Latte/LeanVAE/modules/cache/vgg.pth | LPIPS linear-layer weights |

  * Total: 306,546,405 bytes in 9 files.
  * The same blobs were also inside each clone's `.git` object store.
  * WF-VAE contained no such file.
* **None of the files is a weight file of an eligible model or of the Cosmos reference.**
  * They are fixed networks used only by the authors' evaluation metrics (FVD, LPIPS).
  * Their nature, not just their naming, was checked against the paths: they sit in `fvd/` and `modules/cache/` directories.

## Deletion

* **Timing.** In the shell command immediately after the clones, every weight-type file was deleted (extensions .pt, .pth, .ckpt, .safetensors, .bin, .pkl, .npz, .onnx, .h5). The `.git` directories, which held the same blobs, were deleted as well. This happened before any adapter was written or any third-party code was imported.
* **Evidence.** The deletion list was printed in the session and saved in the session scratchpad (`third_party_weight_files_deleted.txt`).

## Consequence

* **Never used.** The files were never loaded, imported or executed.
  * The adapters import only the encoder modules.
  * They deliberately avoid the LPIPS and FVD modules: the LeanVAE and OmniTokenizer adapters bypass the package `__init__`s that would import LPIPS, and LARP's `models/__init__.py` is not used.
* **No DS203 data involved.** No DS203 frame was decoded and no DS203 data were processed at any point during code lock.
* **No outputs from them.** No representation, estimate or other output was produced from these files.
* **No eligible weights downloaded.** No weights of any eligible model or of the reference were downloaded. All adapters were tested with random initialisation only.
* **Other caches.** `~/.cache/huggingface` and `~/.cache/torch` contain no file created on 2026-10-05 other than the transformers cache-format marker `version.txt`.

## Current repository scan

The scan ran just before this record was committed:

```
weight-type files in the working tree, including git-ignored third_party/, excluding .git
  (*.pt *.pth *.ckpt *.safetensors *.bin *.pkl *.pickle *.npz *.npy *.onnx *.h5 *.hdf5 *.torch *.pb *.tflite *.msgpack): 0
tracked weight-type files (git ls-files): 0
files > 5 MB in third_party/:
  13,943,841  third_party/OmniTokenizer/Diffusion/Latte/visuals/latte.gif   (README animation)
  31,039,176  third_party/LARP/data/metadata/k600_train.csv                  (dataset index, text)
third_party/ total: 67 MB, source code only
```

## Prevention

1. **No further retrieval before the final code lock.** No third-party retrieval of any kind is permitted until the final code-lock commit. None is needed: `third_party/` as used at code lock is present.
2. **The fetch script no longer downloads and then strips.** `scripts/fetch_third_party.sh` has been rewritten:
   * It refuses to run without `--after-final-code-lock`.
   * It fetches the pinned commit at depth 1 with `--filter=blob:none` (partial clone) and checks out through a non-cone sparse checkout that excludes every weight-type pattern. The blobs of excluded files are therefore never fetched or written.
   * It then confirms with `git rev-list --missing=print`, which does not fetch, that every weight-type blob of the commit is absent from the object store, and that no weight-type file exists in the tree. If either check fails, it deletes the directory and aborts.
3. **Verification of the mechanism.** It was verified offline against a synthetic local repository containing a 2 MB `.pt` and a 0.1 MB `.pth` file of random bytes:
   * neither blob was fetched;
   * the checkout contained only the two text files;
   * the script refused to run without the flag.
4. **Limitation.** A server that ignores `--filter` would deliver every blob. Git prints a warning in that case, and the post-checkout check aborts and deletes the directory. GitHub supports the filter.

## Pointer added 2026-10-05 at the investigator's instruction (`CC_TASK_SS_code_lock_coverage_fix_addendum.md` item 1)

* This section is appended only. No text above it was changed.
* **Approved exception.** The investigator approved one source-only exception to the prevention rule (point 1 above): two raw `.py` files (VideoMAE architecture definitions) from MCG-NJU/VideoMAE at `14ef8d856287c94ef1f985fe30f958eb4ec2c55d`.
* **How it was done.** They were retrieved with `curl` from raw.githubusercontent.com, with no clone, archive, LFS object or weight. The record is `decisions/CODELOCK_AUTH_002_videomae_source.md`.
* **Script change.** `scripts/fetch_third_party.sh --authorized-videomae-source` permits exactly that retrieval and verifies the pinned SHA-256 values.
* **Rule restored.** After it, the no-third-party-retrieval rule is restored until the final code-lock commit.
