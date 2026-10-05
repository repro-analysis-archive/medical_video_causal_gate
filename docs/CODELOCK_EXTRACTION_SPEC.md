# SS protocol DS203: frozen extraction specification (code lock)

* **Scope:** every currently eligible model (§4.1.5; facts in force d3563e7) and the Cosmos reference (Decision 005).
* **Machine-readable version:** `docs/codelock_extraction_spec.json`, one entry per registry key of `ss_benchmark/feasibility.py`. Where this file and the JSON differ, the JSON and the adapter code govern.
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
| SurgeNetCholec; SurgeNetRARP | TimJaspersTue/SurgeNetModels @ cc21f4a1: `CHOLEC_checkpoint_epoch0050_teacher.pth`; `RARP_checkpoint_epoch0050_teacher.pth` (README "Teacher Backbone" column) | frame | 224² | — | x/255, ImageNet mean/std | timm `caformer_s18` → `forward_head(pre_logits=True)`: LayerNorm of the stage-4 map averaged over H, W (= SurgeNet `self.norm(x.mean([1, 2]))`) | spatial global average (7×7); ten-frame step mean | 512 |
| SelfSupSurg-ResNet50 | CAMMA SelfSupSurg `model_final_checkpoint_{moco_v2,simclr,swav,dino}_surg.torch` (one architecture; VISSL trunk) | frame | 224² | — | x/255, ImageNet mean/std (configs) | torchvision ResNet-50, fc = Identity: global average pool after layer4 | 7×7 average; ten-frame step mean | 2048 |
| VideoMAE:hf-base-k400-1600 / -800, hf-base-ssv2-2400, hf-large-k400-1600; VideoMAE:orig-{base-k400-800, base-k400-1600, large-k400-1600, base-ssv2-800, base-ssv2-2400, base-ucf101-3200} | MCG-NJU/videomae-base @ dc740ced, -base-short @ 9fa00797, -base-ssv2 @ 644bd7ac, -large @ 12da269a; original MODEL_ZOO pre-training checkpoints (state dict mapped with transformers' encoder rules) | clip | 224² | 16 | x/255; HF `preprocessor_config.json` mean/std, else ImageNet mean/std | `VideoMAEModel.last_hidden_state` = final encoder layer after the final LayerNorm (`videomae.layernorm`; `use_mean_pooling` false); encoder only | mean over all 1,568 patch tokens (8 × 14 × 14); no CLS token exists | 768 (B) / 1024 (L) |
| OmniTokenizer-imagenet_k600 | Daniel0724/OmniTokenizer @ 9ebde216 `imagenet_k600.ckpt`; code 701b6190 | clip | 256² | 17 | x/255 − 0.5 | `F.normalize(pre_vq_conv(encoder(x)), dim=1)` = codebook-lookup input (not quantised) | mean over latent time (5); 8×32×32 | 8192 |
| WF-VAE-L-16ch | chestnutlzj/WF-VAE-L-16Chn @ 8c0aa9ce; code d858bee8 | clip | 256² | 33 | 2·x/255 − 1 | `encode(x).latent_dist.mode()` = posterior mean; scale/shift not applied | mean over latent time (9); 16×32×32 | 16384 |
| LARP-L-Long | hywang66/LARP-L-long-tokenizer @ c93a7e2d; code 8aaed633 | clip | 128² | 16 | x/255 | `F.normalize(bottleneck.project_in(Z), dim=-1)`, Z = encoder outputs at 1,024 holistic queries = codebook-lookup input (no SVQ sampling) | no latent time axis; 1024×16 flattened | 16384 |
| LeanVAE-16ch; LeanVAE-4ch | Yumic/LeanVAE @ 4585e461 `LeanVAE-dim16.ckpt` / `LeanVAE-dim4.ckpt`; code 62f7c7d5 | clip | 256² | 17 | x/255 − 0.5 | `LeanVAE.encode(x)`, no tiling = posterior mean | mean over latent time (5); d×32×32 | 16384 / 4096 |
| Cosmos-CV8x8x8 (reference) | nvidia/Cosmos-1.0-Tokenizer-CV8x8x8 @ 5110dbb3, subfolder `vae` (gated; licence before step 4) | native clip | 320² | ≤ 121 native frames of [5t, 5t+5) | crop and mask at native resolution, then resize; /127.5 − 1 | `post_quant_conv(encode(video).latent_dist.mode())` | mean over latent time; 16×40×40 | 25600 |

## 4. Judgement calls (frozen prospectively)

| model | choice | alternative | reason |
|---|---|---|---|
| SurgeNet (both) | input 224², ImageNet normalisation | 224×399 (downstream fine-tuning) | No level-1–3 SurgeNet source states the pretraining input size or normalisation. 224 is the CAFormer-S18 / ImageNet-1k initialisation resolution (the timm pretrained_cfg). |
| WF-VAE-L 16ch | clip length 33 | 25 or 49 (training stages) | 33 is the authors' evaluation and measurement clip (paper and TRAIN_AND_VALIDATE.md). The training stage of the released checkpoint is not stated. 1 + 4k holds. |
| OmniTokenizer | encoder blocks "ttww" | 4 window layers (paper prose) | R1: the released evaluation script for `imagenet_k600.ckpt`. |
| LARP | bottleneck_dim 16 | d′ = 8 (paper) | R1: the released `config.json`. |
| OmniTokenizer, LARP | the L2-normalised codebook-lookup input | raw pre-normalisation projection | One rule for both VQ tokenizers: use the tensor the quantiser compares with its codebook. |
| VideoMAE | sizes ViT-B and ViT-L only | ViT-S, ViT-H | These are the sizes whose compute the eligibility facts quote and whose configs are saved. ViT-S / ViT-H checkpoints are not covered by the adapter. |
| Cosmos | random initialisation uses the diffusers default config (= CV8x8x8) | the gated HF config | The gated config was not read at code lock. With weights (step 4), `from_pretrained` uses the checkpoint's own `vae/config.json`. |

## 5. Not covered

* VideoMAE ViT-S and ViT-H checkpoints, for the reason given in §4.
* Fine-tuned (supervised) VideoMAE checkpoints: they are not self-supervised pre-training representations.
