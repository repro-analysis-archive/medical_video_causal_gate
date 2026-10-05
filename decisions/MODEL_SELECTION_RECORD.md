# SS protocol DS203: model selection record (§14 step 3)

* **Task:** `CC_TASK_SS_step3_model_selection_v1.md`. Executed 2026-10-05.
* **Protocol:** `docs/SS_PROTOCOL_DS203.md`, frozen at 4c86dc5.
* **Code base:** final code lock 98cba1e (SDR implementation commit af56777). No repository code was changed. All measurements were made from scratch scripts outside the repository that only import the locked `ss_benchmark` code, run in the locked extraction environment (`/home/user/.venvs/ss_extract`).
* **Hard limits kept:**
  * no DS203 frame was decoded and no representation was extracted;
  * no analysis code changed;
  * no DS203 output, representation quality or causal result entered any decision;
  * the Cosmos weights were not downloaded.
* **Decision needed (see §5):** the two top-ranked primary checkpoints failed the load check because of an architecture mismatch in the locked SurgeNet adapter, not because of the checkpoints. Under the task's rule this counts as a documented feasibility failure, so the mechanical selection moved to the next-ranked checkpoint.

## 1. Conventions used to apply the frozen rules mechanically

| rule (§4.1.4) | how it was applied |
|---|---|
| eligible set | the manifest `docs/codelock_checkpoint_manifest.json`: its 21 selectable, ranking-reachable checkpoints (6 primary, 15 secondary) |
| primary rank 1: clip-level before frame-level | every eligible primary checkpoint is frame-level (§4.1.5), so this criterion ties all of them |
| secondary rank 1: video VAE / tokenizer before masked autoencoder | LeanVAE, WF-VAE-L, LARP and OmniTokenizer come before VideoMAE |
| rank 2: most recent release | Release = the UTC calendar date of the earliest commit, in the official repository's history (a level-2 file listing), that contains the checkpoint file (Hugging Face) or its download link (GitHub README / MODEL_ZOO). The same date is a tie. Evidence is in §2. |
| rank 3: lowest compute | the documented compute (eligibility facts / paper or README tables); equal documented values tie |
| tie-break 1: authors' level-1 default or recommended checkpoint | Only a statement in the paper that recommends one of the tied checkpoints counts. README statements (level 2) do not. "If none is stated, none is inferred." None was found for any tie (§3). |
| tie-break 2: lower protocol-relevant compute | FLOPs of the locked adapter's `encode` at the protocol input size and clip length (batch 1), counted with `torch.utils.flop_counter.FlopCounterMode` under `no_grad`. Random initialisation, float32 on CPU; FLOPs depend only on the architecture. For adapters whose `encode` is decorated with `torch.inference_mode` (which bypasses the counter), the counter ran on the unchanged undecorated body (`__wrapped__`). |
| tie-break 3: lower measured synthetic-input peak memory | the rule-4 test (`feasibility.gpu_memory_test`: bf16, CUDA, batch 1, protocol input), in bytes |
| tie-break 4: lexical order of the identifier | Python string order of the manifest `checkpoint_id` |

## 2. Release evidence (first official listing)

| checkpoint(s) | first commit containing the file or link | UTC date |
|---|---|---|
| LeanVAE-dim4.ckpt, LeanVAE-dim16.ckpt | Yumic/LeanVAE `dd190287` ("Upload 2 files"; both files in one commit) | 2025-03-18 |
| WF-VAE-L-16Chn `diffusion_pytorch_model.safetensors` | chestnutlzj/WF-VAE-L-16Chn `da63ad47` | 2024-11-24 |
| LARP-L-long-tokenizer `model.safetensors` | hywang66/LARP-L-long-tokenizer `a8982ac9` | 2024-10-23 |
| SurgeNetModels CHOLEC / RARP `_checkpoint_epoch0050_teacher.pth` | TimJaspersTue/SurgeNetModels `d67c8fab` (10:55:57) / `022a01be` (10:57:28): consecutive rename commits, the same day | 2024-06-19 |
| OmniTokenizer `imagenet_k600.ckpt`, `imagenet_k600_vae.ckpt` | Daniel0724/OmniTokenizer `337629d5` ("first"; both in one commit) | 2024-06-13 |
| SelfSupSurg `model_final_checkpoint_{moco_v2,simclr,swav,dino}_surg.torch` | CAMMA-public/SelfSupSurg README `988751f6` ("init"; all four) | 2023-02-10 |
| VideoMAE K400 ViT-S 1600, K400 ViT-H 1600, SSv2 ViT-S 2400 | MCG-NJU/VideoMAE MODEL_ZOO.md `5cefe18c` ("add ViT-Sand ViT-H") | 2022-10-20 |
| VideoMAE UCF101 ViT-B 3200 | `cece3888` ("support UCF101") | 2022-10-19 |
| VideoMAE SSv2 ViT-B 800 | `26abf539` | 2022-05-13 |
| VideoMAE K400 ViT-B 800, K400 ViT-B 1600, K400 ViT-L 1600, SSv2 ViT-B 2400 | `ed5ce1f2` ("code release") | 2022-04-24 |

How the evidence was obtained:
* **Hugging Face:** `https://huggingface.co/api/models/<repo>/commits/main`, then the file tree at each commit.
* **GitHub:** `https://api.github.com/repos/<repo>/commits?path=<file>`, then the raw file at each commit.
* Metadata and source text only.

## 3. Ranked lists with tie-break trace

**Measured tie-break quantities** (random initialisation; FLOPs per protocol input; rule-4 peak reserved bytes):

| registry key | GFLOPs | peak bytes |
|---|---:|---:|
| SurgeNetCholec / SurgeNetRARP | 7.750 / 7.750 | 75,497,472 / 75,497,472 |
| SelfSupSurg moco_v2 / simclr / swav / dino | 8.174 each | 79,691,776 each |
| LeanVAE-4ch / -16ch | **115.970 / 116.032** | 666,894,336 / 666,894,336 |
| WF-VAE-L-16ch | 4,424.590 | 1,373,634,560 |
| LARP-L-Long | 349.125 | 471,859,200 |
| OmniTokenizer VQ / VAE | **263.312 / 263.354** | 226,492,416 / 226,492,416 |
| VideoMAE ViT-S (K400, SSv2) | 68.438 | 119,537,664 |
| VideoMAE ViT-B (K400 800, K400 1600, SSv2 800, SSv2 2400, UCF101 3200) | 270.054 | 255,852,544 |
| VideoMAE ViT-L K400 1600 | 951.973 | 706,740,224 |
| VideoMAE ViT-H K400 1600 | 1,979.166 | 1,486,880,768 |
| Cosmos-CV8x8x8 (reference; not ranked) | 3,399.314 | 2,139,095,040 |

**Primary arm** (all frame-level, so rank 1 ties):

| rank | checkpoint (manifest id) | trace |
|---:|---|---|
| 1 | `TimJaspersTue/SurgeNetModels@cc21f4a1…/CHOLEC_checkpoint_epoch0050_teacher.pth` | release 2024-06-19 (newest). Tied with RARP on release and on documented compute (CAFormer-S18, 24.3M). TB1: none (the SurgeNet papers recommend no checkpoint between the two). TB2: equal. TB3: equal. TB4: `…/CHOLEC…` < `…/RARP…`. |
| 2 | `…/RARP_checkpoint_epoch0050_teacher.pth` | as above |
| 3 | `CAMMA-public/SelfSupSurg/model_final_checkpoint_dino_surg.torch` | release 2023-02-10. Four-way tie on release and documented compute (ResNet-50, 3.8 GFLOPs). TB1: none (the paper's "Recommended" row in Table 1 recommends hyperparameter values, not a checkpoint). TB2: equal. TB3: equal. TB4: `…dino…` < `…moco_v2…` < `…simclr…` < `…swav…`. |
| 4 | `…/model_final_checkpoint_moco_v2_surg.torch` | as above |
| 5 | `…/model_final_checkpoint_simclr_surg.torch` | as above |
| 6 | `…/model_final_checkpoint_swav_surg.torch` | as above |

**Secondary arm.** Ranks 1–6 are video VAE / tokenizers; ranks 7–15 are the masked autoencoder (VideoMAE).

| rank | checkpoint | trace |
|---:|---|---|
| 1 | `Yumic/LeanVAE@4585e461…/LeanVAE-dim4.ckpt` | release 2025-03-18 (newest). Tied with dim16 on release and on documented compute (README: 39.8M, 0.203 TFLOPs each). TB1: none (the LeanVAE paper recommends no checkpoint). **TB2: 115.970 < 116.032 GFLOPs.** |
| 2 | `Yumic/LeanVAE@4585e461…/LeanVAE-dim16.ckpt` | as above |
| 3 | `chestnutlzj/WF-VAE-L-16Chn@8c0aa9ce…/diffusion_pytorch_model.safetensors` | release 2024-11-24 |
| 4 | `hywang66/LARP-L-long-tokenizer@c93a7e2d…/model.safetensors` | release 2024-10-23 |
| 5 | `Daniel0724/OmniTokenizer@9ebde216…/imagenet_k600.ckpt` | release 2024-06-13. Tied with VAE on release and documented compute. TB1: none in the paper (the README recommendation is level 2). **TB2: 263.312 < 263.354 GFLOPs.** |
| 6 | `…/imagenet_k600_vae.ckpt` | as above |
| 7 | VideoMAE K400 ViT-S 1600 (`gdrive:1nU-H1u3eJ…`) | release 2022-10-20. Documented compute 57 GFLOPs (ViT-S) < ViT-H 1192. Tied with SSv2 ViT-S. TB1: none. TB2: equal. TB3: equal. TB4: `…1nU…` < `…1p_…`. |
| 8 | VideoMAE SSv2 ViT-S 2400 (`gdrive:1p_I1aaONO…`) | as above |
| 9 | VideoMAE K400 ViT-H 1600 (`gdrive:1AJQR1Rsi2…`) | release 2022-10-20; 1192 GFLOPs |
| 10 | VideoMAE UCF101 ViT-B 3200 (`gdrive:1BHev4meNg…`) | release 2022-10-19 |
| 11 | VideoMAE SSv2 ViT-B 800 (`gdrive:181hLvyrrP…`) | release 2022-05-13 |
| 12 | VideoMAE SSv2 ViT-B 2400 (`gdrive:1I18dY_7rS…`) | release 2022-04-24. ViT-B (180) < ViT-L (597). Three-way ViT-B tie. TB1: none (the paper's "default ViT-B backbone" is an architecture, shared by all three). TB2: equal. TB3: equal. TB4: `1I18…` < `1Jfr…` < `1tEh…`. |
| 13 | VideoMAE K400 ViT-B 800 (`gdrive:1JfrhN144H…`) | as above |
| 14 | VideoMAE K400 ViT-B 1600 (`gdrive:1tEhLyskjb…`) | as above |
| 15 | VideoMAE K400 ViT-L 1600 (`gdrive:1qLOXWb_MG…`) | release 2022-04-24; 597 GFLOPs |

## 4. Feasibility attempts (top-down, per arm)

**Weight files.** All were downloaded with plain `curl -fL --retry 5` and stored outside the repository on LaCie. The log is `/media/user/LaCie/medvideo_gate/weights/download_step3.log`.

| file | URL | bytes | SHA-256 | published checksum | path |
|---|---|---:|---|---|---|
| CHOLEC_checkpoint_epoch0050_teacher.pth | https://huggingface.co/TimJaspersTue/SurgeNetModels/resolve/cc21f4a158f3a17260d8304e9d2b24b580a6ea35/CHOLEC_checkpoint_epoch0050_teacher.pth | 93,022,798 | `9bc446addbf92e8c4e8b237eb3ec8917dbbc526ca5af042d657340ea8bb945d4` | HF LFS sha256 at the revision: **equal**; size equal | `…/weights/surgenet/` |
| RARP_checkpoint_epoch0050_teacher.pth | https://huggingface.co/TimJaspersTue/SurgeNetModels/resolve/cc21f4a158f3a17260d8304e9d2b24b580a6ea35/RARP_checkpoint_epoch0050_teacher.pth | 93,022,798 | `1a68cc45450907415628de7834e479d4defb9a0bef67f0a28ba3df4596c49644` | HF LFS sha256: **equal**; size equal | `…/weights/surgenet/` |
| model_final_checkpoint_dino_surg.torch | https://s3.unistra.fr/camma_public/github/selfsupsurg/models/model_final_checkpoint_dino_surg.torch | 352,288,944 | `6e374717dc036470dee1a6131ff44d10b507badb1031df2d6e2ff5aee8ca2c93` | No checksum is published. Size equals the server Content-Length. Last-Modified is Mon, 06 Feb 2023. The S3 multipart ETag (`ce7b6a7e…-42`) is not a content hash. | `…/weights/selfsupsurg/` |
| LeanVAE-dim4.ckpt | https://huggingface.co/Yumic/LeanVAE/resolve/4585e461c697919a452a99191ebf455b991c13fb/LeanVAE-dim4.ckpt | 159,125,886 | `cd54560ca3e713e8aee69fddca21519a19d6bf9a46ee380e523e12f716aa5963` | HF LFS sha256: **equal**; size equal | `…/weights/leanvae/` |

**Primary arm:**

1. **SurgeNetCholec: FAIL at (a), the load check.**
   * `prim_caformer.build(weights=…)` raised `checkpoint mismatch: missing ['stages.0.blocks.0.token_mixer.act1.scale', 'stages.0.blocks.0.token_mixer.act1.bias', 'stages.0.blocks.0.mlp.act.scale', …]`.
   * Diagnosis: see §5.
2. **SurgeNetRARP: FAIL at (a).** It failed with the identical missing keys. It is the same released architecture.
3. **SelfSupSurg DINO: PASS.**
   * (a) Load: `prim_resnet50.build(weights=…)` loaded the VISSL trunk with no missing or unexpected keys (23,508,032 parameters). The CPU output is (1, 2048) and finite.
   * (b) Memory: rule-4 peak reserved **0.0797 GB** ≤ 20.0, so feasible.
   * (c) Extraction compute: synthetic throughput **2,251 frames/s** (bf16, batch 64, the pipeline default). Model hours 0.27 (standardized plus native passes over 2,164,752 grid frames); decode 3.06 h and I/O 3.81 h (2012acd). Serial total **7.14 h = 0.30 days** ≤ 7, so feasible.
   * **Selected (primary): `CAMMA-public/SelfSupSurg/model_final_checkpoint_dino_surg.torch`**, under the mechanical rule; see §5.

**Secondary arm:**

1. **LeanVAE-4ch: PASS.**
   * (a) Load: `sec_leanvae.build(weights=…, variant="4ch")` loaded; the adapter's check of the stored args against the coded configuration passed (39,767,496 parameters). The CPU output is (1, 4096) and finite.
   * (b) Memory: rule-4 peak reserved **0.262 GB** ≤ 20.0, so feasible.
   * (c) Extraction compute: synthetic throughput **228 clips/s** (bf16, batch 1; the pipeline encodes one 17-frame clip per step). Model hours 0.13 over 108,238 steps; decode 3.06 h, I/O 3.81 h. Serial total **7.00 h = 0.29 days**, so feasible.
   * **Selected (secondary): `Yumic/LeanVAE@4585e461…/LeanVAE-dim4.ckpt`.**

**Cosmos reference** (random initialisation; weights not downloaded):
* (b) Memory: rule-4 peak reserved **2.14 GB** (1 × 3 × 121 × 320 × 320, bf16).
* (c) Extraction compute: throughput **5.49 clips/s**. Model hours 5.48 over 108,238 steps; sequential decode 3.31 h, I/O 3.81 h. Serial total **12.6 h = 0.52 days** ≤ 7.

**Method.** The calls were `feasibility.gpu_memory_test(key, weights)`, `feasibility.synthetic_throughput(key, batch, n_batches, weights)` (n_batches 20 / 50 / 10) and `feasibility.extraction_projection(key, inputs_per_second)`. These are the frozen §10.4 procedure: video hours of all 403 DS203 files (150.33 h, a superset of the extraction set), and the serial sum of I/O, decode and model.

## 5. Investigator decision needed: SurgeNet adapter defect (not a checkpoint defect)

**Cause.**
* SurgeNet's own model code (`fm_sources/primary/surgenet_metaformer_py.txt`, `caformer_s18(pretrained='SurgeNet')`) builds its token mixers and MLPs with ReLU:
  * `token_mixers=[partial(SepConv, act1_layer=nn.ReLU), partial(SepConv, act1_layer=nn.ReLU), Attention, Attention]`;
  * `mlps=partial(Mlp, act_layer=nn.ReLU)`.
* The locked adapter uses timm's `caformer_s18`, whose SepConv and MLP activations are StarReLU (`s·relu(x)² + b`, learnable `scale` / `bias`).
* The released checkpoints therefore contain no activation parameters: 152 keys in the original MetaFormer naming.
* The locked loader's missing-key check raised correctly. Even a non-strict load would compute a different function from SurgeNet's network.
* Both files are intact: their SHA-256 values equal the published values.

**Status under the task rule.** "An objective load failure (… missing keys required by the adapter) is a documented feasibility failure; move to the next-ranked checkpoint." The selection above follows that rule.

**Note.** The failure comes from the code-lock adapter's architecture choice (CODELOCK_EXTRACTION_SPEC: "timm 1.0.15 `caformer_s18`"), not from the released checkpoints. The estimator, gate, projection and Part B results are unaffected, because those stages do not use the adapters.

**Options for the investigator:**
* **(i)** Accept the mechanical selection (SelfSupSurg DINO).
* **(ii)** Treat this as a code-lock defect and authorise a corrected SurgeNet adapter: SurgeNet's ReLU MetaFormer, matching the released checkpoints. That is a post-lock extraction-code change. Ranks 1–2 would then be re-tested.

CC did not choose between these options.

## 6. Projected wall time of §14 step 4 (all arms)

There are five decode passes:
* 4a, the mask check;
* the primary model, standardized;
* the primary model, native (FM-P-nat);
* the secondary model;
* the Cosmos reference, which needs every native frame.

| pass | (A) frozen §10.4 components (h) | (B) as implemented: single-stream ffmpeg CPU decode, plus CPU preprocessing measured on synthetic frames (h) |
|---|---:|---:|
| 4a mask check | 6.87 (decode 3.06 + I/O 3.81) | 6.67 |
| primary SelfSupSurg DINO, standardized | 7.00 | 8.93 (decode 6.67 + crop / mask / resize and near-uniform 2.13 + model 0.13) |
| primary, native | 7.00 | 8.19 (6.67 + 1.39 + 0.13) |
| secondary LeanVAE-4ch | 7.00 | 8.94 (6.67 + 2.14 + 0.13) |
| Cosmos reference | 12.60 | 41.94 (6.67 + 29.79 + 5.48) |
| **total** | **40.5 h ≈ 1.7 days** | **74.7 h ≈ 3.1 days** |

* **Bottleneck in (A):** decode plus disk I/O, 34.4 of the 40.5 h.
* **Bottleneck in (B):** the Cosmos pass's CPU preprocessing of about 13.1 M native frames (≤ 121 per 5-s step): 3.9 ms per 1080p frame and 29.1 ms per 4K frame, measured on synthetic frames. The 4K centre-3 videos account for 18.0 of its 29.8 h.
* **Inputs to (B):**
  * single-stream CPU sequential decode speeds per format (2012acd), giving 6.67 h per pass;
  * I/O (3.23 h sequential) assumed to overlap with the slower decode;
  * preprocessing times measured with the locked `preprocess.standardize`, `native`, `near_uniform_flags` and `extract.cosmos_prepare_frames` on random 1080p / 2160p frames (14 torch threads).
* **Status:** neither total is a protocol criterion. Rule 5 was applied per model with the frozen procedure, as in §4.

## 7. Not done

* §14 step 4 (extraction) has not started.
* No Cosmos weights were downloaded; they wait for the investigator's Hugging Face token and licence acceptance (§17).
