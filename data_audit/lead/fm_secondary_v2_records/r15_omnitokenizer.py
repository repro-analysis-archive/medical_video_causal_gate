import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "omnitok_Daniel0724__OmniTokenizer_hfapi.json"
G = "omnitok_github_README.md"; LIC = "omnitok_github_LICENSE.txt"; P = "omnitok_arxiv_2406.09399_fulltext.txt"
TR = "omnitok_github_scripts_recons_train.sh.txt"; EV = "omnitok_github_scripts_recons_eval_video.sh.txt"
K6 = "kinetics600_arxiv_1808.01340.txt"; K4 = "kinetics400_arxiv_1705.06950.txt"
DATA_FILES = [G, P]
CLASS_FILES = [K4, K6]

rec = {
 "id": "15_omnitokenizer",
 "name": "OmniTokenizer (FoundationVision; joint image-video transformer tokenizer, VQVAE and VAE versions)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "Daniel0724/OmniTokenizer imagenet_k600.ckpt (VQVAE, ImageNet + K600; the authors' recommended checkpoint) and imagenet_k600_vae.ckpt (VAE, ImageNet + K600); HF repo sha 9ebde216ba19b3eeaeec4e2960ebc2d0551c8b3d (2024-06-13); paper arXiv 2406.09399v1",
 "checkpoints_by_training_data": {
  "imagenet_k600.ckpt (VQVAE)": "ImageNet + Kinetics-600",
  "imagenet_k600_vae.ckpt (VAE)": "ImageNet + Kinetics-600",
  "imagenet_ucf.ckpt (VQVAE) / imagenet_ucf_vae.ckpt (VAE)": "ImageNet + UCF-101",
  "imagenet_mit.ckpt (VQVAE)": "ImageNet + Moments-in-Time",
  "imagenet_sthv2.ckpt (VQVAE)": "ImageNet + Something-Something v2",
  "celebahq_ucf / celebahq_k600 / ffhq_ucf / ffhq_k600 (VQVAE)": "face images + UCF-101 or K600",
  "imagenet_only / celebahq / ffhq (VQVAE)": "images only (not video tokenizers in the sense of C3)",
  "note": "the entry is judged on the version checkpoints (ImageNet + K600); every video checkpoint listed uses a closed curated video benchmark"
 },
 "paper": {"title": "OmniTokenizer: A Joint Image-Video Tokenizer for Visual Generation", "year": 2024, "arxiv": "2406.09399", "versions": "v1 2024-06-13 (HTML rendering saved)"},
 "weights_location": {
  "urls": ["https://huggingface.co/Daniel0724/OmniTokenizer/resolve/main/imagenet_k600.ckpt",
           "https://huggingface.co/Daniel0724/OmniTokenizer/resolve/main/imagenet_k600_vae.ckpt"],
  "files_listed": {"imagenet_k600.ckpt": 742455697, "imagenet_k600_vae.ckpt": 742471379, "imagenet_ucf.ckpt": 742455761,
                   "imagenet_ucf_vae.ckpt": 742473102, "imagenet_mit.ckpt": 853078893, "imagenet_sthv2.ckpt": 742455442},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; the official GitHub README links these files; nothing downloaded",
  "note": "repo is under the personal HF account Daniel0724, linked from the official FoundationVision/OmniTokenizer README (official release); HF repo has no licence tag",
  "quote_ids": ["w_file", "w_file_vae", "w_gated", "w_readme_link"]
 },
 "licence": {
  "id": "MIT (project licence stated in the official GitHub README + LICENSE; no separate weights licence; no licence tag on the HF repo)",
  "url": "https://github.com/FoundationVision/OmniTokenizer/blob/main/LICENSE",
  "commercial": "permitted (MIT)", "non_commercial_only": False,
  "restrictions": "none beyond MIT notice; training datasets (ImageNet, Kinetics) carry their own terms (not audited)",
  "gating": "none",
  "quote_ids": ["lic_readme", "lic_text", "lic_grant"]
 },
 "domain": {
  "value": "joint image-video tokenizer (spatial window attention + causal temporal attention transformer; VQVAE for LM generation, KL-finetuned VAE for diffusion) used for language-model and diffusion video generation; trained on general video (Kinetics-600 human-action clips) + ImageNet",
  "quote_ids": ["dom_intro", "dom_gen", "data_progressive"]
 },
 "architecture": {
  "type": "transformer autoencoder: patch embedding (first frame p x p, following frames t x p x p), 4 window-attention spatial layers + 4 causal temporal layers, hidden 512; VQ codebook 8192 x dim 8 (VQVAE) or Gaussian latent (VAE)",
  "representation": "encoder latents: 8-dim per token on a (1 + T/4) x H/8 x W/8 grid (VQ indices from an 8192-entry codebook for the VQVAE)"
 },
 "pretraining_data": {
  "summary": "Progressive training: image-only stage (fixed 256x256) then joint image-video stage; released video checkpoints are each trained on ImageNet + one named video benchmark (K600, UCF-101, MiT or SSv2); paper results default to ImageNet + UCF-101. Version checkpoints: ImageNet + Kinetics-600.",
  "form": "dataset list (named, per checkpoint)"
 },
 "pretraining_data_quote": {"quote_ids": ["data_ckpt_k600", "data_ckpt_k600_vae", "data_recommend", "data_progressive", "data_datasets", "data_default", "k600_def", "k600_youtube"]},
 "medical_video_in_data": {
  "answer": "NO",
  "basis": "closed list of named datasets (ImageNet + Kinetics-600) none of which is medical; term search of the OmniTokenizer README/paper and of the Kinetics-400 class list and Kinetics-600 new-class list finds no medical/surgical term (K600 does contain non-surgical everyday classes such as 'using inhaler').",
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES + CLASS_FILES, MED_TERMS)}
 },
 "appendix300_possible": {
  "answer": "NO",
  "basis_class": "closed_curated_list",
  "basis": "video pretraining data of the version checkpoints = Kinetics-600 (fixed 600 human-action classes; YouTube-sourced clips), images = ImageNet; closed curated list whose documented content scope excludes surgical recordings (conventions_v2 Kinetics clarification). Timing: released 2024-06-13, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_ckpt_k600", "k600_def"]
 },
 "appendix300_check": {
  "answer": "NO",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "closed_curated_list",
  "basis": "ImageNet + Kinetics-600 (closed fixed action-class benchmark); the Kinetics class lists saved contain no surgical/medical class.",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES + CLASS_FILES, A300_TERMS)},
  "quote_ids": ["data_ckpt_k600", "k600_def", "k400_def"]
 },
 "input": {
  "frame_size": {"value": "256x256 (image stage fixed 256; joint stage random 128-384; video evaluation scripts use 256)", "quote_ids": ["in_res", "in_eval"]},
  "frame_rate_or_sampling": {"value": "not documented in the paper; training script passes '--fps -1' (semantics not documented; inferred: no fps resampling, consecutive frames)", "quote_ids": ["in_fps"]},
  "clip_length_frames": {"value": "17 frames (first frame encoded separately + 16 following frames)", "quote_ids": ["in_res", "in_first", "in_fps"]},
  "temporal_compression": {"value": "4x after the first frame (temporal_patch_size 4): 1 + T -> 1 + T/4 latent frames (17 -> 5)", "quote_ids": ["in_patch", "in_compress"]},
  "spatial_compression": {"value": "8x8 (patch_size 8)", "quote_ids": ["in_patch", "in_compress"]}
 },
 "embedding_dim": {
  "value": "8-dim latent per token x (1 + 16/4) x 32 x 32 = 5 x 32 x 32 = 5,120 tokens -> 40,960 values per 17-frame 256x256 clip (VQVAE: 5,120 indices into an 8,192-entry codebook); VAE latent dim 8 assumed equal to codebook_dim (inferred from the shared training flags)",
  "derivation": "latent dimension 8 (paper, codebook_dim 8 in scripts), compression (1+T)xHxW -> (1+T/t)xH/p xW/p with t=4, p=8",
  "quote_ids": ["emb_dim", "emb_codes", "in_compress", "in_patch"]
 },
 "params": {
  "value": "not documented for the tokenizer (the parameter counts in the paper's tables are for the generation LMs: 227M / 650M); architecture documented as 4 spatial + 4 temporal layers, hidden 512; checkpoint file 742 MB (contents not documented)",
  "scope": "not documented",
  "quote_ids": ["emb_dim"]
 },
 "flops_per_input_if_documented": {
  "value": "51 GFLOPs per image input and 262 GFLOPs per video input (paper Table 8, 'Ours'); input size not stated in the table (inferred: 256x256 image / 17-frame 256x256 video, matching the training/eval settings and the 'VQGAN 167 x 17' entry); whether encoder-only or encoder+decoder is not stated",
  "quote_ids": ["flops"]
 },
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists imagenet_k600.ckpt / imagenet_k600_vae.ckpt, gated=False; linked from the official README", "quote_ids": ["w_file", "w_gated", "w_readme_link"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "MIT licence for the project (README + LICENSE); no separate weights licence", "quote_ids": ["lic_readme", "lic_grant"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "image-video tokenizer (VQVAE/VAE, pixel reconstruction) built for LM and diffusion video generation, trained on general (Kinetics) video", "quote_ids": ["dom_intro", "dom_gen"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "README model zoo names the training datasets per checkpoint (ImageNet + K600 for the version); paper names the datasets", "quote_ids": ["data_ckpt_k600", "data_ckpt_k600_vae", "data_datasets"]},
  "eligible": "YES (all four criteria PASS; caveats: licence is the project MIT licence with no separate weights statement; tokenizer params not documented)"
 },
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"imagenet_k600.ckpt\",", "source_file": API},
  {"id": "w_file_vae", "quote": "\"rfilename\": \"imagenet_k600_vae.ckpt\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "w_readme_link", "quote": "We release both VQVAE and VAE version of OmniTokenizer, that are pretrained on a wide range of image and video datasets:", "source_file": G},
  {"id": "lic_readme", "quote": "This project is licensed under the MIT license, as found in the LICENSE file.", "source_file": G},
  {"id": "lic_text", "quote": "MIT License Copyright (c) 2024 FoundationVision", "source_file": LIC},
  {"id": "lic_grant", "quote": "Permission is hereby granted, free of charge, to any person obtaining a copy", "source_file": LIC},
  {"id": "dom_intro", "quote": "We introduce OmniTokenizer, a joint image-video tokenizer which features the following properties:", "source_file": G},
  {"id": "dom_gen", "quote": "Equipped with it, both **language model** and **diffusion model** could achieve competitive visual generation results.", "source_file": G},
  {"id": "data_ckpt_k600", "quote": "| VQVAE | ImageNet + K600 | 1.23 | 25.97 | [imagenet_k600.ckpt](https://huggingface.co/Daniel0724/OmniTokenizer/resolve/main/imagenet_k600.ckpt) |", "source_file": G},
  {"id": "data_ckpt_k600_vae", "quote": "| VAE | ImageNet + K600 | 0.78 | 13.02 | [imagenet_k600_vae.ckpt](https://huggingface.co/Daniel0724/OmniTokenizer/resolve/main/imagenet_k600_vae.ckpt) |", "source_file": G},
  {"id": "data_recommend", "quote": "We recommand you to try [imagenet_k600.ckpt](https://huggingface.co/Daniel0724/OmniTokenizer/resolve/main/imagenet_k600.ckpt) as it is trained on large-scale image and video data.", "source_file": G},
  {"id": "data_progressive", "quote": "The training of VQVAE includes two stages: image-only training on a fixed resolution, and image-video joint training on multiple resolutions. After this, finetune the VQVAE model w/ KL loss to obtain a VAE model.", "source_file": G},
  {"id": "data_datasets", "quote": "We evaluate the visual tokenization performance of OmniTokenizer on both image and video datasets, including ImageNet [ 9 ] , CelebA-HQ [ 21 ] , FFHQ [ 22 ] , Kinetics [ 23 , 6 ] , UCF-101 [ 44 ] , Moments-in-Time (MiT) [ 29 ] , and Something-Something v2 (SSV2) [ 15 ] .", "source_file": P},
  {"id": "data_default", "quote": "Unless otherwise stated, the results reported in this paper are jointly trained on ImageNet and UCF-101.", "source_file": P},
  {"id": "k600_def", "quote": "We describe an extension of the DeepMind Kinetics human action dataset from 400 classes, each with at least 400 video clips, to 600 classes, each with at least 600 video clips.", "source_file": K6},
  {"id": "k600_youtube", "quote": "The clips are from YouTube video, last 10s, and have a variable resolution and frame rate;", "source_file": K6},
  {"id": "k400_def", "quote": "The dataset contains 400 human action classes, with at least 400 video clips for each action. Each clip lasts around 10s and is taken from a different YouTube video.", "source_file": K4},
  {"id": "in_res", "quote": "During the image training stage, we train the model with a fixed image resolution of 256 × \\times 256. For the joint training stage, we forward the model with image and video data iteratively, with the video sequence length being 17 frames. The spatial resolutions are randomly chosen from 128, 192, 256, 320, and 384.", "source_file": P},
  {"id": "in_eval", "quote": "--vqgan_ckpt \"./ckpts_pub/imagenet_k600.ckpt\"", "source_file": EV},
  {"id": "in_fps", "quote": "--resolution 256 --sequence_length 17 --fps -1", "source_file": TR},
  {"id": "in_first", "quote": "we always process the first frame x 0 ∈ ℝ 1 × H × W × 3 x_{0}\\in\\mathbb{R}^{1\\times H\\times W\\times 3} and following frames x 1 : T ∈ ℝ T × H × W × 3 x_{1:T}\\in\\mathbb{R}^{T\\times H\\times W\\times 3} separately for the joint encoding of videos and static images", "source_file": P},
  {"id": "in_patch", "quote": "--patch_embed 'linear' --patch_size 8 --temporal_patch_size 4 --spatial_depth 4 --temporal_depth 4 --embedding_dim 512", "source_file": TR},
  {"id": "in_compress", "quote": "In this way, we compress the input resolution from ( 1 + T ) × H × W (1+T)\\times H\\times W to ( 1 + T t ) × H p × W p (1+\\frac{T}{t})\\times\\frac{H}{p}\\times\\frac{W}{p} .", "source_file": P},
  {"id": "emb_dim", "quote": "OmniTokenizer adopts a decoupled spatial-temporal architecture consisting of 4 window attention-based spatial layers (window size = 8) and 4 causal attention-based temporal layers. The hidden dimension is 512 and the latent dimension is 8, following ViT-VQGAN [ 62 ] .", "source_file": P},
  {"id": "emb_codes", "quote": "--n_codes 8192 --codebook_dim 8 --l2_code", "source_file": TR},
  {"id": "flops", "quote": "Table 8: Inference cost and rFID. iGFLOPs/vGFLOPs: GFLOPs for image and video inputs. Method iGFLOPs vGFLOPs FID VQGAN 167 167 × \\times 17 1.49 JointAttn 72 358 1.89 DePlainAttn 72 299 1.33 Ours 51 262 1.28", "source_file": P}
 ]
}
save_record(rec)
