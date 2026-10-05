# Code-lock authorisation 003: source-only retrieval of the VideoMAE pre-training data pipeline

* **Recorded:** 2026-10-05, before the new pre-gate implementation commit. Part B had not been run.
* **Authorisation:** the investigator, in `CC_TASK_SS_code_lock_videomae_norm.md` item 1, as the second source-only exception:
  > from the official MCG-NJU/VideoMAE repository at the same pinned commit (14ef8d85), retrieve by raw `curl` only
  > `datasets.py`, plus any source file it imports that defines the pre-training transforms or the normalization
  > constants. No clone, archive, LFS object, or file with a weight extension.
* **Status:** after this retrieval, the no-retrieval rule of `CODELOCK_INCIDENT_001` is restored until the final code-lock commit.

## Retrieval

| item | value |
|---|---|
| repository | https://github.com/MCG-NJU/VideoMAE (official) |
| pinned commit | `14ef8d856287c94ef1f985fe30f958eb4ec2c55d` (the same commit as CODELOCK_AUTH_002) |
| command | `bash scripts/fetch_third_party.sh --authorized-videomae-datasets` |
| what that command runs, for each listed file f | `curl -fsSL --max-filesize 1048576 -o third_party/VideoMAE/f.part https://raw.githubusercontent.com/MCG-NJU/VideoMAE/14ef8d856287c94ef1f985fe30f958eb4ec2c55d/f` |
| what the script refuses | names not on the list or not `*.py`, files with NUL bytes, and SHA-256 mismatches against pinned values |
| executions | 1. 15:09:34 +0900: `datasets.py` (the list then held only this file); its imports were read. 2. 15:09:58 +0900: `transforms.py` was added to the list. `datasets.py`, already present with its pinned SHA-256, was not fetched again. |
| mechanism | raw single-file HTTP retrieval; no clone, archive, LFS object or weight |

| file (in `third_party/VideoMAE/`) | bytes | SHA-256 | why |
|---|---:|---|---|
| `datasets.py` | 6,267 | `3bfa677831615a95f835f7c4b235eb18ba0cb29d6acd42ff335f334f75ee9f7e` | authorised by name. It defines `DataAugmentationForVideoMAE` (the pre-training transform) and `build_pretraining_dataset`. |
| `transforms.py` | 7,260 | `f7f37f8e628bb65c08d9c6bf1f9f88dcc4c13557613895cb2db401a51fae5d54` | imported by `datasets.py` (`from transforms import *`). It defines `GroupNormalize`, `ToTorchFormatTensor`, `Stack` and `GroupMultiScaleCrop`, the pre-training transforms. |

**Imports of `datasets.py` not retrieved:**
* `masking_generator` (`TubeMaskingGenerator`): token masking, not a transform or normalisation.
* `kinetics` (`VideoClsDataset`, `VideoMAE`): dataset and loader classes.
* `ssv2` (`SSVideoClsDataset`): a fine-tuning dataset.
* `torchvision.transforms`: an installed library.

**Pinning.** All SHA-256 values are pinned in `scripts/fetch_third_party.sh`.

## Post-fetch scan

```
third_party/VideoMAE/datasets.py:          Python script, ASCII text executable
third_party/VideoMAE/modeling_finetune.py: Python script, ASCII text executable
third_party/VideoMAE/modeling_pretrain.py: Python script, ASCII text executable
third_party/VideoMAE/transforms.py:        Python script, ASCII text executable
weight-type files under third_party/ (*.pt *.pth *.ckpt *.bin *.safetensors *.pkl *.npz *.onnx *.h5 *.torch): 0
```

## What the retrieved pipeline determines

**`datasets.py`, `DataAugmentationForVideoMAE.__init__`:**

```
        self.input_mean = [0.485, 0.456, 0.406]  # IMAGENET_DEFAULT_MEAN
        self.input_std = [0.229, 0.224, 0.225]  # IMAGENET_DEFAULT_STD
        normalize = GroupNormalize(self.input_mean, self.input_std)
        self.train_augmentation = GroupMultiScaleCrop(args.input_size, [1, .875, .75, .66])
        self.transform = transforms.Compose([
            self.train_augmentation,
            Stack(roll=False),
            ToTorchFormatTensor(div=True),
            normalize,
        ])
```

**`build_pretraining_dataset(args)`:** `transform = DataAugmentationForVideoMAE(args)`, with no dataset- or size-specific branch.

**`transforms.py`:**
* `Stack(roll=False)`: for `img_group[0].mode == 'RGB'`, the channels are concatenated unchanged (`roll=True` would reverse them to BGR).
* `ToTorchFormatTensor(div=True)`: `return (img.float().div(255.) ...)`.
* `GroupNormalize`: `for t, m, s in zip(tensor, rep_mean, rep_std): t.sub_(m).div_(s)`, with mean / std repeated per frame.

**Result:**
* The values are literals; their comments name the timm constants `IMAGENET_DEFAULT_MEAN` / `IMAGENET_DEFAULT_STD`, but no external constant is read.
* Pre-training inputs were RGB / 255, normalised per channel with mean (0.485, 0.456, 0.406) and std (0.229, 0.224, 0.225).
* The same transform is used for every pre-training dataset, so the values are the same for all nine checkpoints.
* Cross-check (task item 3a): the retrieved copy confirms the audit's quoted lines exactly, so the values were adopted.
