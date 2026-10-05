# CODELOCK_CORRECTION_001: SurgeNet adapter (post-code-lock correction)

* **Recorded:** 2026-10-05.
* **Authority:** `CC_TASK_SS_step3_adapter_fix_v2.md` (supersedes v1).
* **Context:**
  * The final code lock (98cba1e) and the SDR implementation commit (af56777) are immutable; this correction is a separate commit on top of them.
  * The frozen protocol (4c86dc5) is unchanged.

## 1. The defect

* **What the code-lock adapter did.** The SurgeNetCholec / SurgeNetRARP adapter (`ss_benchmark/models/prim_caformer.py` at af56777) built timm 1.0.15 `caformer_s18`, whose SepConv token mixers and MLPs use learnable StarReLU (`s·relu(x)² + b`).
* **What the released checkpoints are.** They were trained with SurgeNet's own model code, `caformer_s18(pretrained='SurgeNet')` in `metaformer.py`, which uses plain ReLU:
  * `token_mixers=[partial(SepConv, act1_layer=nn.ReLU), partial(SepConv, act1_layer=nn.ReLU), Attention, Attention]`;
  * `mlps=partial(Mlp, act_layer=nn.ReLU)`.
* **How it showed.** At §14 step 3, the verified files (SHA-256 equal to the published values) failed the adapter's missing-key check (`…token_mixer.act1.scale` etc.). The files contain no activation parameters: 152 keys in the official naming.
* **What it was.** An adapter error, not an objective checkpoint failure. Under the frozen source-priority rule (R1: official released model code governs executable configuration), the adapter was non-compliant.

## 2. Why it was undetectable at code lock

* The code-lock hard limits forbade downloading any model weights. Adapters were tested only with randomly initialised architectures.
* With random weights, timm's CAFormer-S18 builds, runs and returns the documented 512-d shape. A mismatch in activation type only appears when real weights are loaded.
* The coverage and engineering tests, which assert build, shape, memory and spec consistency, therefore passed by design.

## 3. The change (restores compliance with a frozen rule)

* **Adapter.** `prim_caformer.build` now imports the official model-definition file unmodified as a module, builds `caformer_s18(num_classes=0, pretrained='SurgeNet')`, and replaces the classification head with `nn.Identity` (the head is not part of the representation, and the released backbone files contain no head parameters). The released file is then loaded with `strict=True`, using the official parameter names.
  * Official file: `third_party/SurgeNet/metaformer.py`, TimJaspers0801/SurgeNet @ `54831cfacf3a6cac0bbf5119f72b9cb9c31c3e82`, 31,549 bytes, SHA-256 `94ef2937bb2b9c8d8b8d53dcfcff49374c6130d805ebd26de4c76ecda5c36718`. This is identical to the copy saved on 2026-10-02.
  * The import has no side effect: `caformer_s18` carries no `@register_model`.
* **What did not change:**
  * the representation definition: `forward_features(x)[0]` = `self.norm(x.mean([1, 2]))`, 512-d;
  * the input size (224 × 224), the ImageNet normalisation, and the registry keys.
* **No forbidden fix was used:** no `strict=False`, no dropped or renamed keys, no approximate architecture.

## 4. Source retrieval (raw files only; no weights)

```
+ curl -fsSL --max-filesize 1048576 -o third_party/SurgeNet/metaformer.py   https://raw.githubusercontent.com/TimJaspers0801/SurgeNet/54831cfacf3a6cac0bbf5119f72b9cb9c31c3e82/metaformer.py   (31,549 B, sha256 94ef2937bb2b9c8d8b8d53dcfcff49374c6130d805ebd26de4c76ecda5c36718)
+ curl -fsSL --max-filesize 1048576 -o third_party/SurgeNet/load_models.py  https://raw.githubusercontent.com/TimJaspers0801/SurgeNet/54831cfacf3a6cac0bbf5119f72b9cb9c31c3e82/load_models.py  (2,227 B, sha256 3d8fd6bc1714ff227172d71cfabf58f04bb6a30da460ac6f781689ed8871f3fe)
  (commit resolved with: git ls-remote https://github.com/TimJaspers0801/SurgeNet.git HEAD; 2026-10-05 16:30:16 +0900)
```

For the SelfSupSurg equivalence test only (the official VISSL trunk), `facebookresearch/vissl` @ `09270ed25a6c2cf71263d955b64cbe076d34ac45`, raw files, 2026-10-05 16:31:52 +0900:

| file (in `third_party/vissl_src/`) | VISSL path | bytes | SHA-256 |
|---|---|---:|---|
| `resnext.py` | `vissl/models/trunks/resnext.py` | 7,288 | `05cecd0685edd0ff3327ce8d9188d348b48d451e5102b02c1b7c72f5d95d6682` |
| `model_helpers.py` | `vissl/models/model_helpers.py` | 24,970 | `b93d1460a79cc18f980237c0c02e723e227019ce1851835ac5df18e03f66a13a` |
| `defaults.yaml` | `vissl/config/defaults.yaml` | 83,472 | `6561e0d7d6546a9cf2a3547e9cdd39a5eef2addf3657d3c4143fb695c38c8474` |

* **Post-fetch scan:** all files are ASCII text, and there are 0 weight-type files under `third_party/`.
* **Not committed:** `third_party/` is git-ignored.
* **Weights:** no additional weights were downloaded. The tests use the files already verified at §14 step 3 (`decisions/MODEL_SELECTION_RECORD.md`).

## 5. Validation (criteria fixed by the task)

* **Test file:** `tests/test_codelock_correction_001.py`, run in the extraction venv.
* **Equivalence settings:** float32; input seed 99990002; inputs normalised as each adapter specifies; criterion max |difference| ≤ 1e-4.

| model | architecture | strict load | official loads the file? | equivalence vs official |
|---|---|---|---|---|
| SurgeNetCholec | identical names / shapes to the official backbone; activations = ReLU | "All keys matched successfully" (152 / 152; 0 missing, 0 unexpected) | yes: the official `load_pretrained_weights` (head removed, strict=False) gives no unexpected key; only `head.*` is missing | max abs diff **0.0** |
| SurgeNetRARP | as above | as above | as above | **0.0** |
| SelfSupSurg ResNet-50 DINO | official VISSL `ResNeXt` (depth 50, width multiplier 1, BatchNorm; SelfSupSurg configs + VISSL defaults) | the checkpoint trunk loads strictly into the official trunk | yes | **0.0** (official trunk output key `"flatten"`) |
| LeanVAE-4ch | official `LeanVAE` class (`load_from_checkpoint` with the stored args) | the checkpoint state dict matches the official model exactly | yes | **0.0** (official `encode` with the official inference normalisation; latent averaged over time and flattened) |

The remeasured memory and extraction projections are in `decisions/MODEL_SELECTION_RECORD.md` §8.

## 6. Scope confirmations

* **No DS203 data used:** no DS203 frame was decoded and no representation was extracted.
* **Estimator and gate untouched:** sdr, learners, DGP, grid, checks, gate, projection, G-SITE, small truth, runner, constants, seeds, ranking rules and thresholds are byte-identical to 98cba1e. The diff stat is in the commit message and the report.
* **Files changed:** only the SurgeNet adapter, a new test file, the SurgeNet extraction-spec and manifest entries, and this record.
* **Part B results stand:** they do not depend on the adapters.
