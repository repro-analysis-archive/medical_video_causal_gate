# SS protocol DS203: checkpoint manifest (code lock)

* **Machine-readable version:** `docs/codelock_checkpoint_manifest.json`; it governs.
* **Enforced by:** `tests/test_codelock_coverage.py`. Each reachable checkpoint has exactly one adapter / registry entry and one extraction-spec entry, builds with random weights and returns the documented shape. Every adapter checkpoint is in the manifest, and no identifier or alias is ambiguous.
* **Scope:** every checkpoint of every eligible candidate (§4.1.5) that the §4.1.4 rules could select, ignoring the post-freeze memory and throughput tests (rules 4-5 / secondary 3-4), which cannot exclude anything now.
* **Release dates:** 'release' records only what the saved level-2 API metadata show; the rank criterion 'first public availability of the checkpoint per a level-1-3 source' is applied at §14 step 3.
* **Totals:** 21 selectable (ranking-reachable) checkpoints, 10 excluded rows, 22 files that are not checkpoints of an eligible candidate, and 1 reference.

## VideoMAE class line (verbatim)

"VideoMAE eligibility applies to official pre-training checkpoints of the masked-autoencoder model; supervised fine-tuned classification/action-recognition checkpoints are outside the secondary reconstructive/generative class."

## VideoMAE input normalisation

* **All nine pre-training checkpoints:** mean (0.485, 0.456, 0.406), std (0.229, 0.224, 0.225), on RGB frames / 255.
* **Source:** the pre-training data pipeline (`datasets.py` `DataAugmentationForVideoMAE` @ 14ef8d85; `decisions/CODELOCK_AUTH_003_videomae_datasets.md`).
* **Note:** modeling_finetune.py::_cfg() reports mean/std 0.5 as model default_cfg metadata, but the pre-training data pipeline is the source that trained the pre-training checkpoints, and it governs under the source-priority rule. Fine-tuned checkpoints remain outside the secondary class.
* Every row's frozen `normalisation` is in the JSON.

## 1. Selectable checkpoints (can enter the frozen ranking)

| candidate | checkpoint | stage | data | architecture | documented compute | registry key | D |
|---|---|---|---|---|---|---|---|
| SurgeNetCholec (CAFormer-S18) | `TimJaspersTue/SurgeNetModels@cc21f4a158f3a17260d8304e9d2b24b580a6ea35/CHOLEC_checkpoint_epoch0050_teacher.pth` (aliases: TimJaspersTue/SurgeNetModels@cc21f4a158f3a17260d8304e9d2b24b580a6ea35/CHOLEC_checkpoint0050.pth) | pre-train (DINO self-supervised) | Cholec80, HeiChole, hSDB-Chole; ImageNet-1k initialisation | CAFormer-S18 | CaFormerS18, 24.3M parameters (eligibility facts) | `SurgeNetCholec` | 512 |
| SurgeNetRARP (CAFormer-S18) | `TimJaspersTue/SurgeNetModels@cc21f4a158f3a17260d8304e9d2b24b580a6ea35/RARP_checkpoint_epoch0050_teacher.pth` (aliases: TimJaspersTue/SurgeNetModels@cc21f4a158f3a17260d8304e9d2b24b580a6ea35/RARP_checkpoint0050.pth) | pre-train (DINO self-supervised) | ESAD, PSI-AVA, RARP-AvL; ImageNet-1k initialisation | CAFormer-S18 | CaFormerS18, 24.3M parameters (eligibility facts) | `SurgeNetRARP` | 512 |
| SelfSupSurg (ResNet-50; MoCo v2 / SimCLR / SwAV / DINO) | `CAMMA-public/SelfSupSurg/model_final_checkpoint_moco_v2_surg.torch` | pre-train (moco_v2 self-supervised) | Cholec80; ImageNet supervised initialisation | ResNet-50 | ResNet-50, 3.8 billion FLOPs (eligibility facts) | `SelfSupSurg-ResNet50:moco_v2` | 2048 |
| SelfSupSurg (ResNet-50; MoCo v2 / SimCLR / SwAV / DINO) | `CAMMA-public/SelfSupSurg/model_final_checkpoint_simclr_surg.torch` | pre-train (simclr self-supervised) | Cholec80; ImageNet supervised initialisation | ResNet-50 | ResNet-50, 3.8 billion FLOPs (eligibility facts) | `SelfSupSurg-ResNet50:simclr` | 2048 |
| SelfSupSurg (ResNet-50; MoCo v2 / SimCLR / SwAV / DINO) | `CAMMA-public/SelfSupSurg/model_final_checkpoint_swav_surg.torch` | pre-train (swav self-supervised) | Cholec80; ImageNet supervised initialisation | ResNet-50 | ResNet-50, 3.8 billion FLOPs (eligibility facts) | `SelfSupSurg-ResNet50:swav` | 2048 |
| SelfSupSurg (ResNet-50; MoCo v2 / SimCLR / SwAV / DINO) | `CAMMA-public/SelfSupSurg/model_final_checkpoint_dino_surg.torch` | pre-train (dino self-supervised) | Cholec80; ImageNet supervised initialisation | ResNet-50 | ResNet-50, 3.8 billion FLOPs (eligibility facts) | `SelfSupSurg-ResNet50:dino` | 2048 |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO pre-train gdrive:1nU-H1u3eJ-VuyCveU7v-WIOcAVxs5Hww` | pre-train (masked autoencoder, 1600 epochs) | Kinetics-400 | ViT-S (pretrain_videomae_small_patch16_224) | 57 GFLOPs per 16-frame view, 22M parameters (paper Table 7) | `VideoMAE:k400-vit-s-1600` | 384 |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO pre-train gdrive:1JfrhN144Hdg7we213H1WxwR3lGYOlmIn` (aliases: MCG-NJU/videomae-base-short) | pre-train (masked autoencoder, 800 epochs) | Kinetics-400 | ViT-B (pretrain_videomae_base_patch16_224) | 180 GFLOPs per view, 87M parameters (paper Table 7) | `VideoMAE:k400-vit-b-800` | 768 |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO pre-train gdrive:1tEhLyskjb755TJ65ptsrafUG2llSwQE1` (aliases: MCG-NJU/videomae-base) | pre-train (masked autoencoder, 1600 epochs) | Kinetics-400 | ViT-B (pretrain_videomae_base_patch16_224) | 180 GFLOPs per view, 87M parameters (paper Table 7) | `VideoMAE:k400-vit-b-1600` | 768 |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO pre-train gdrive:1qLOXWb_MGEvaI7tvuAe94CV7S2HXRwT3` (aliases: MCG-NJU/videomae-large) | pre-train (masked autoencoder, 1600 epochs) | Kinetics-400 | ViT-L (pretrain_videomae_large_patch16_224) | 597 GFLOPs per view, 305M parameters (paper Table 7) | `VideoMAE:k400-vit-l-1600` | 1024 |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO pre-train gdrive:1AJQR1Rsi2N1pDn9tLyJ8DQrUREiBA1bO` | pre-train (masked autoencoder, 1600 epochs) | Kinetics-400 | ViT-H (pretrain_videomae_huge_patch16_224) | 1192 GFLOPs per view, 633M parameters (paper Table 7) | `VideoMAE:k400-vit-h-1600` | 1280 |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO pre-train gdrive:1p_I1aaONOeUvRmRQw1UT3-L2H8XJClHu` | pre-train (masked autoencoder, 2400 epochs) | Something-Something V2 | ViT-S (pretrain_videomae_small_patch16_224) | 57 GFLOPs per 16-frame view, 22M parameters (paper Table 7) | `VideoMAE:ssv2-vit-s-2400` | 384 |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO pre-train gdrive:181hLvyrrPW2IOGA46fkxdJk0tNLIgdB2` | pre-train (masked autoencoder, 800 epochs) | Something-Something V2 | ViT-B (pretrain_videomae_base_patch16_224) | 180 GFLOPs per view, 87M parameters (paper Table 7) | `VideoMAE:ssv2-vit-b-800` | 768 |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO pre-train gdrive:1I18dY_7rSalGL8fPWV82c0-foRUDzJJk` (aliases: MCG-NJU/videomae-base-ssv2) | pre-train (masked autoencoder, 2400 epochs) | Something-Something V2 | ViT-B (pretrain_videomae_base_patch16_224) | 180 GFLOPs per view, 87M parameters (paper Table 7) | `VideoMAE:ssv2-vit-b-2400` | 768 |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO pre-train gdrive:1BHev4meNgKM0o_8DMRbuzAsKSP3IpQ3o` | pre-train (masked autoencoder, 3200 epochs) | UCF101 | ViT-B (pretrain_videomae_base_patch16_224) | 180 GFLOPs per view, 87M parameters (paper Table 7) | `VideoMAE:ucf101-vit-b-3200` | 768 |
| OmniTokenizer (ImageNet + K600) | `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/imagenet_k600.ckpt` | pre-train (tokenizer, VQVAE) | ImageNet, Kinetics-600 | OmniTokenizer encoder (spatial-temporal ViT, 512-d), VQVAE head | 'Ours 51 262 1.28' (paper; eligibility facts) | `OmniTokenizer-imagenet_k600` | 8192 |
| OmniTokenizer (ImageNet + K600) | `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/imagenet_k600_vae.ckpt` | pre-train (tokenizer, VAE) | ImageNet, Kinetics-600 | OmniTokenizer encoder (spatial-temporal ViT, 512-d), VAE head | 'Ours 51 262 1.28' (paper; eligibility facts) | `OmniTokenizer-imagenet_k600_vae` | 8192 |
| WF-VAE-L 16ch | `chestnutlzj/WF-VAE-L-16Chn@8c0aa9ce3aee55121d71ce06b1d179471b1d0531/diffusion_pytorch_model.safetensors` | pre-train (video VAE) | Kinetics-400 | WF-VAE-L, 16 latent channels | 316M parameters (README; eligibility facts) | `WF-VAE-L-16ch` | 16384 |
| LARP-L-Long tokenizer | `hywang66/LARP-L-long-tokenizer@c93a7e2d9ea2eb21b8f84f38484ccc348b3347ea/model.safetensors` | pre-train (video tokenizer) | Kinetics-600, UCF101 | LARP-L (ViT-B-sized encoder, 1024 holistic queries) | 173M parameters (README; eligibility facts) | `LARP-L-Long` | 16384 |
| LeanVAE | `Yumic/LeanVAE@4585e461c697919a452a99191ebf455b991c13fb/LeanVAE-dim16.ckpt` | pre-train (video VAE) | Kinetics-600 | LeanVAE, latent_dim 16 | 39.8M parameters (README; eligibility facts) | `LeanVAE-16ch` | 16384 |
| LeanVAE | `Yumic/LeanVAE@4585e461c697919a452a99191ebf455b991c13fb/LeanVAE-dim4.ckpt` | pre-train (video VAE) | Kinetics-600 | LeanVAE, latent_dim 4 | 39.8M parameters (README; eligibility facts) | `LeanVAE-4ch` | 4096 |

Representation tensors and pooling: see `docs/CODELOCK_EXTRACTION_SPEC.md` / the JSON (`representation`, `pooling`).

## 2. Excluded (cannot enter the ranking)

| candidate | checkpoint | stage | reason |
|---|---|---|---|
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO fine-tune gdrive:1ygjLRm1kvs9mwGsP3lLxUExhRo6TWnrx` | fine-tune (supervised classification after 1600-epoch pre-training) | class line (§4.1.3) |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO fine-tune gdrive:18EEgdXY9347yK3Yb28O-GxFMbk41F6Ne` | fine-tune (supervised classification after 800-epoch pre-training) | class line (§4.1.3) |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO fine-tune gdrive:1MzwteHH-1yuMnFb8vRBQDvngV1Zl-d3z` | fine-tune (supervised classification after 1600-epoch pre-training) | class line (§4.1.3) |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO fine-tune gdrive:1jX1CiqxSkCfc94y8FRW1YGHy-GNvHCuD` | fine-tune (supervised classification after 1600-epoch pre-training) | class line (§4.1.3) |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO fine-tune gdrive:104ouJZxSVPSAm0LwJXd6IzjdA_RGLqZi` | fine-tune (supervised classification after 1600-epoch pre-training) | class line (§4.1.3) |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO fine-tune gdrive:1ajlMrT06jiiM-5YjNI2X_UFyzsuYbbtZ` | fine-tune (supervised classification after 2400-epoch pre-training) | class line (§4.1.3) |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO fine-tune gdrive:1xZCiaPF4w7lYmLt5o1D5tIZyDdLtJAvH` | fine-tune (supervised classification after 800-epoch pre-training) | class line (§4.1.3) |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO fine-tune gdrive:1dt_59tBIyzdZd5Ecr22lTtzs_64MOZkT` | fine-tune (supervised classification after 2400-epoch pre-training) | class line (§4.1.3) |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/VideoMAE MODEL_ZOO fine-tune gdrive:1MSyon6fPpKz7oqD6WDGPFK4k_Rbyb6fw` | fine-tune (supervised classification after 3200-epoch pre-training) | class line (§4.1.3) |
| VideoMAE (K400 / SSv2 / UCF101 checkpoints) | `MCG-NJU/videomae-*-finetuned-* (Hugging Face)` | fine-tune | class line (§4.1.3) |

## 3. Files in the same repositories that are not checkpoints of an eligible candidate

| file | reason |
|---|---|
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/imagenet_only.ckpt` | tokenizer trained on other data (README model zoo row): not a checkpoint of the eligible candidate 'OmniTokenizer (ImageNet + K600)'; that data combination is not an eligible candidate in d3563e7 |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/imagenet_ucf.ckpt` | tokenizer trained on other data (README model zoo row): not a checkpoint of the eligible candidate 'OmniTokenizer (ImageNet + K600)'; that data combination is not an eligible candidate in d3563e7 |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/imagenet_mit.ckpt` | tokenizer trained on other data (README model zoo row): not a checkpoint of the eligible candidate 'OmniTokenizer (ImageNet + K600)'; that data combination is not an eligible candidate in d3563e7 |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/imagenet_sthv2.ckpt` | tokenizer trained on other data (README model zoo row): not a checkpoint of the eligible candidate 'OmniTokenizer (ImageNet + K600)'; that data combination is not an eligible candidate in d3563e7 |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/imagenet_ucf_vae.ckpt` | tokenizer trained on other data (README model zoo row): not a checkpoint of the eligible candidate 'OmniTokenizer (ImageNet + K600)'; that data combination is not an eligible candidate in d3563e7 |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/celebahq.ckpt` | tokenizer trained on other data (README model zoo row): not a checkpoint of the eligible candidate 'OmniTokenizer (ImageNet + K600)'; that data combination is not an eligible candidate in d3563e7 |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/celebahq_k600.ckpt` | tokenizer trained on other data (README model zoo row): not a checkpoint of the eligible candidate 'OmniTokenizer (ImageNet + K600)'; that data combination is not an eligible candidate in d3563e7 |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/celebahq_ucf.ckpt` | tokenizer trained on other data (README model zoo row): not a checkpoint of the eligible candidate 'OmniTokenizer (ImageNet + K600)'; that data combination is not an eligible candidate in d3563e7 |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/ffhq.ckpt` | tokenizer trained on other data (README model zoo row): not a checkpoint of the eligible candidate 'OmniTokenizer (ImageNet + K600)'; that data combination is not an eligible candidate in d3563e7 |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/ffhq_k600.ckpt` | tokenizer trained on other data (README model zoo row): not a checkpoint of the eligible candidate 'OmniTokenizer (ImageNet + K600)'; that data combination is not an eligible candidate in d3563e7 |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/ffhq_ucf.ckpt` | tokenizer trained on other data (README model zoo row): not a checkpoint of the eligible candidate 'OmniTokenizer (ImageNet + K600)'; that data combination is not an eligible candidate in d3563e7 |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/imagenet_class_lm.ckpt` | language model / diffusion generator / data file, not a tokenizer checkpoint (README: LM checkpoints for scripts/lm_train) |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/ucf_class_lm.ckpt` | language model / diffusion generator / data file, not a tokenizer checkpoint (README: LM checkpoints for scripts/lm_train) |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/k600_fp_lm.ckpt` | language model / diffusion generator / data file, not a tokenizer checkpoint (README: LM checkpoints for scripts/lm_train) |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/dit.pt` | language model / diffusion generator / data file, not a tokenizer checkpoint (README: LM checkpoints for scripts/lm_train) |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/latte_17frms.pt` | language model / diffusion generator / data file, not a tokenizer checkpoint (README: LM checkpoints for scripts/lm_train) |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/imagenet.npz` | language model / diffusion generator / data file, not a tokenizer checkpoint (README: LM checkpoints for scripts/lm_train) |
| `Daniel0724/OmniTokenizer@9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d/annotations.zip` | language model / diffusion generator / data file, not a tokenizer checkpoint (README: LM checkpoints for scripts/lm_train) |
| `Yumic/LeanVAE@4585e461c697919a452a99191ebf455b991c13fb/sky-dim16.pt` | Latte generator trained on LeanVAE latents (README 'Latte Model' table: 'Latte + LeanVAE-chn*'), not a LeanVAE checkpoint |
| `Yumic/LeanVAE@4585e461c697919a452a99191ebf455b991c13fb/sky-dim4.pt` | Latte generator trained on LeanVAE latents (README 'Latte Model' table: 'Latte + LeanVAE-chn*'), not a LeanVAE checkpoint |
| `Yumic/LeanVAE@4585e461c697919a452a99191ebf455b991c13fb/ucf-dim16.pt` | Latte generator trained on LeanVAE latents (README 'Latte Model' table: 'Latte + LeanVAE-chn*'), not a LeanVAE checkpoint |
| `Yumic/LeanVAE@4585e461c697919a452a99191ebf455b991c13fb/ucf-dim4.pt` | Latte generator trained on LeanVAE latents (README 'Latte Model' table: 'Latte + LeanVAE-chn*'), not a LeanVAE checkpoint |

## 4. Reference

* `nvidia/Cosmos-1.0-Tokenizer-CV8x8x8@5110dbb3c94a9eb6648eabbbccc19c76180fe426/vae` (registry `Cosmos-CV8x8x8`): fixed reference arm, not subject to the §4.1.4 rules or ranking.
