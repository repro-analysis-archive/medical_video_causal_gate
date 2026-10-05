# SS protocol DS203: frozen extraction specification (code lock)

* **Scope:** every currently eligible model (§4.1.5; facts in force d3563e7) and the Cosmos reference (Decision 005).
* **Machine-readable version:** `docs/codelock_extraction_spec.json`, one entry per registry key of `ss_benchmark/feasibility.py`. Where this file and the JSON differ, the JSON and the adapter code govern.
* **Checkpoint manifest:** `docs/codelock_checkpoint_manifest.json` (summary in `docs/CODELOCK_CHECKPOINT_MANIFEST.md`) maps every selectable checkpoint to exactly one entry. `tests/test_codelock_coverage.py` enforces this.
* **Consistency tests** (`tests/test_codelock_extra.py`, run in the extraction venv):
  * `test_extraction_spec_matches_adapters` checks each JSON entry against its adapter;
  * `test_adapter_random_init_gpu_memory` checks each representation dimension against the adapter's actual output.
* **What is frozen:** every choice below is a code-lock implementation choice. None may be changed after the code-lock gate.

## 1. Source priority

* **R1.** For executable model configuration, the official released inference / reproduction code or released config (levels 2–3) takes precedence over prose in the paper (level 1) when they conflict, unless the protocol specifies otherwise. Protocol rules (§3, §4.2) always take precedence over model documentation.
* **R2.** No alternative is ever chosen by DS203 output quality, real-frame throughput or any causal result.

## 2. Common to all models

* **Preprocessing** (§3.1, standardized acquisition):
  1. centre square crop;
  2. bilinear antialiased resize to the input size;
  3. circular mask at r × side. r = 0.45 unless the §14 step 4a mechanical check changes it. The lowest 3 % of rows are also set to 0.
* **Native arm** (§3.2; FM-P-nat, primary model only): the full frame resized to the input size, with no crop and no mask.
* **Temporal sampling:**
  * Frame models (§4.2): each 2-fps grid frame is embedded. A step's representation is the mean over grid frames 10t…10t+9.
  * Clip models (§4.2): the model's documented clip length L is used. The clip is the L most recent grid frames, ending at grid frame 10t+9; at the video start the first grid frame is repeated. The model's documented frame rate is not kept: the 2-fps grid standardizes acquisition across centres at the cost of temporal fidelity (§4.2 [v0.4-final2]).
* **Inference:**
  * `model.eval()` and `torch.inference_mode()`.
  * bf16 on CUDA (§4.1.4 rule 4).
  * No sampling, no quantisation and no token masking.

## 3. Per model

| registry key(s) | checkpoint | kind | input | L | normalisation after crop/mask | representation tensor | pooling | D |
|---|---|---|---|---|---|---|---|---|
| SurgeNetCholec; SurgeNetRARP | TimJaspersTue/SurgeNetModels @ cc21f4a1: `CHOLEC_checkpoint_epoch0050_teacher.pth`; `RARP_checkpoint_epoch0050_teacher.pth` (README "Teacher Backbone" column) | frame | 224² | — | x/255, ImageNet mean/std | **(CODELOCK_CORRECTION_001)** the official `caformer_s18(pretrained='SurgeNet')` of SurgeNet's `metaformer.py` @ 54831cfa (CAFormer-S18 with plain ReLU in SepConv / Mlp), head = Identity, strict load; `forward_features(x)[0]` = `self.norm(x.mean([1, 2]))` | spatial global average (7×7); ten-frame step mean | 512 |
| SelfSupSurg-ResNet50:{moco_v2, simclr, swav, dino} (one entry per checkpoint) | CAMMA SelfSupSurg `model_final_checkpoint_{moco_v2,simclr,swav,dino}_surg.torch` (one architecture; VISSL trunk) | frame | 224² | — | x/255, ImageNet mean/std (configs) | torchvision ResNet-50, fc = Identity: global average pool after layer4 | 7×7 average; ten-frame step mean | 2048 |
| VideoMAE:{k400-vit-s-1600, k400-vit-b-800, k400-vit-b-1600, k400-vit-l-1600, k400-vit-h-1600, ssv2-vit-s-2400, ssv2-vit-b-800, ssv2-vit-b-2400, ucf101-vit-b-3200} | the nine official MODEL_ZOO pre-training checkpoints (Google-Drive file ids in the JSON); HF MCG-NJU copies are aliases, not used | clip | 224² | 16 | RGB x/255, mean (0.485, 0.456, 0.406) / std (0.229, 0.224, 0.225) (pre-training pipeline `DataAugmentationForVideoMAE`) | encoder `forward_features` with no token masked = final LayerNorm (eps 1e-6) of the last block; transformers VideoMAEModel configured from `pretrain_videomae_{small,base,large,huge}_patch16_224` (checked against the official code) | mean over all 1,568 patch tokens (8 × 14 × 14); no CLS token exists | 384 (S) / 768 (B) / 1024 (L) / 1280 (H) |
| OmniTokenizer-imagenet_k600 | Daniel0724/OmniTokenizer @ 9ebde216 `imagenet_k600.ckpt`; code 701b6190 | clip | 256² | 17 | x/255 − 0.5 | `F.normalize(pre_vq_conv(encoder(x)), dim=1)` = codebook-lookup input (not quantised) | mean over latent time (5); 8×32×32 | 8192 |
| OmniTokenizer-imagenet_k600_vae | Daniel0724/OmniTokenizer @ 9ebde216 `imagenet_k600_vae.ckpt`; code 701b6190 | clip | 256² | 17 | x/255 − 0.5 | posterior mean = first 8 of the 16 `pre_vq_conv(encoder(x))` channels (`use_vae` branch; DiagonalGaussianDistribution); no sampling | mean over latent time (5); 8×32×32 | 8192 |
| WF-VAE-L-16ch | chestnutlzj/WF-VAE-L-16Chn @ 8c0aa9ce; code d858bee8 | clip | 256² | 33 | 2·x/255 − 1 | `encode(x).latent_dist.mode()` = posterior mean; scale/shift not applied | mean over latent time (9); 16×32×32 | 16384 |
| LARP-L-Long | hywang66/LARP-L-long-tokenizer @ c93a7e2d; code 8aaed633 | clip | 128² | 16 | x/255 | `F.normalize(bottleneck.project_in(Z), dim=-1)`, Z = encoder outputs at 1,024 holistic queries = codebook-lookup input (no SVQ sampling) | no latent time axis; 1024×16 flattened | 16384 |
| LeanVAE-16ch; LeanVAE-4ch | Yumic/LeanVAE @ 4585e461 `LeanVAE-dim16.ckpt` / `LeanVAE-dim4.ckpt`; code 62f7c7d5 | clip | 256² | 17 | x/255 − 0.5 | `LeanVAE.encode(x)`, no tiling = posterior mean | mean over latent time (5); d×32×32 | 16384 / 4096 |
| Cosmos-CV8x8x8 (reference) | nvidia/Cosmos-1.0-Tokenizer-CV8x8x8 @ 5110dbb3, subfolder `vae` (gated; licence before step 4) | native clip | 320² | ≤ 121 native frames of [5t, 5t+5) | crop and mask at native resolution, then resize; /127.5 − 1 | `post_quant_conv(encode(video).latent_dist.mode())` | mean over latent time; 16×40×40 | 25600 |

## 3a. VideoMAE class line (verbatim)

"VideoMAE eligibility applies to official pre-training checkpoints of the masked-autoencoder model; supervised fine-tuned classification/action-recognition checkpoints are outside the secondary reconstructive/generative class."

## 3b. VideoMAE normalisation note

modeling_finetune.py::_cfg() reports mean/std 0.5 as model default_cfg metadata, but the pre-training data pipeline is the source that trained the pre-training checkpoints, and it governs under the source-priority rule. Fine-tuned checkpoints remain outside the secondary class.

## 4. Judgement calls (frozen prospectively)

| model | choice | alternative | reason |
|---|---|---|---|
| SurgeNet (both) | input 224², ImageNet normalisation | 224×399 (downstream fine-tuning) | No level-1–3 SurgeNet source states the pretraining input size or normalisation. 224 is the CAFormer-S18 / ImageNet-1k initialisation resolution (the timm pretrained_cfg). |
| SurgeNet (both) | the official SurgeNet ReLU MetaFormer (CODELOCK_CORRECTION_001) | timm `caformer_s18` (StarReLU), as used at code lock | R1: the official released model code defines the executable architecture. The code-lock adapter was non-compliant, and the error was found only when weights were first loaded at §14 step 3. |
| WF-VAE-L 16ch | clip length 33 | 25 or 49 (training stages) | 33 is the authors' evaluation and measurement clip (paper and TRAIN_AND_VALIDATE.md). The training stage of the released checkpoint is not stated. 1 + 4k holds. |
| OmniTokenizer | encoder blocks "ttww" | 4 window layers (paper prose) | R1: the released evaluation script for `imagenet_k600.ckpt`. |
| LARP | bottleneck_dim 16 | d′ = 8 (paper) | R1: the released `config.json`. |
| OmniTokenizer (VQ checkpoint), LARP | the L2-normalised codebook-lookup input | raw pre-normalisation projection | One rule for both VQ tokenizers: use the tensor the quantiser compares with its codebook. |
| VideoMAE | the original MODEL_ZOO pre-training files, with the official architecture definitions (LayerNorm eps 1e-6) | the HF MCG-NJU converted copies (eps 1e-12 in their configs) | R1: the authors' released checkpoints and model code. The HF copies are aliases of four of the nine checkpoints. |
| VideoMAE | input normalisation mean (0.485, 0.456, 0.406) / std (0.229, 0.224, 0.225), the same for all nine checkpoints | (0.5, 0.5, 0.5) from `modeling_finetune.py::_cfg()` (the choice in the superseded 05822ee) | R1: the pre-training data pipeline (`datasets.py` `DataAugmentationForVideoMAE`, retrieved under CODELOCK_AUTH_003) defines the executable input normalisation of the pre-training checkpoints. Quoted: `self.input_mean = [0.485, 0.456, 0.406]  # IMAGENET_DEFAULT_MEAN`, `self.input_std = [0.229, 0.224, 0.225]  # IMAGENET_DEFAULT_STD`, `normalize = GroupNormalize(self.input_mean, self.input_std)` after `ToTorchFormatTensor(div=True)`. `build_pretraining_dataset` applies it to every pre-training dataset. |
| Cosmos | random initialisation uses the diffusers default config (= CV8x8x8) | the gated HF config | The gated config was not read at code lock. With weights (step 4), `from_pretrained` uses the checkpoint's own `vae/config.json`. |

## 5. Not covered

* Supervised fine-tuned VideoMAE checkpoints: excluded by the class line (§3a; §4.1.3, investigator confirmation 2026-10-05).
* Files in the same repositories that are not checkpoints of an eligible candidate: other OmniTokenizer data combinations, language models and generators, and the LeanVAE Latte generators. See the manifest's `out_of_candidate` list.
