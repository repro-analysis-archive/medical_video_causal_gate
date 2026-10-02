import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "vidtok_microsoft__VidTok_hfapi.json"
C = "vidtok_hf_README.md"; G = "vidtok_github_README.md"; LIC = "vidtok_github_LICENSE.txt"; P = "vidtok_arxiv_2412.13061_fulltext.txt"
DATA_FILES = [C, G, P]

rec = {
 "id": "16_vidtok",
 "name": "VidTok (Microsoft; family of causal / non-causal video tokenizers, KL-continuous and FSQ-discrete)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "microsoft/VidTok checkpoints/vidtok_v1_1/vidtok_kl_causal_488_16chn_v1_1.ckpt (VidTok v1.1, March 2025: causal KL-16chn, 4x8x8) as the representative variant; the v1.0 family (12 checkpoints: KL 4/8/16chn and FSQ 4,096-262,144, 4x8x8 / 4x16x16 / 2x8x8, causal and non-causal) and 4 further v1.1 checkpoints are in the same repo; HF repo sha 97eb9fb68314830f2fb62d899f3ce7ff15bc9929; paper arXiv 2412.13061v1",
 "checkpoints_by_training_data": {
  "all v1.0 checkpoints": "self-collected video dataset (Training Set 1 low-res, Training Set 2 high-res); no dataset names",
  "all v1.1 checkpoints": "v1.0 causal models fine-tuned on long videos; the source of the long videos is not documented"
 },
 "paper": {"title": "VidTok: A Versatile and Open-Source Video Tokenizer", "year": 2024, "arxiv": "2412.13061", "versions": "v1 2024-12-17 (HTML rendering saved)"},
 "weights_location": {
  "urls": ["https://huggingface.co/microsoft/VidTok/tree/main/checkpoints"],
  "files_listed": {"checkpoints/vidtok_v1_1/vidtok_kl_causal_488_16chn_v1_1.ckpt": 701935377,
                   "checkpoints/vidtok_kl_causal_488_16chn.ckpt": 701945558,
                   "checkpoints/vidtok_kl_causal_488_4chn.ckpt": 699954234,
                   "checkpoints/vidtok_fsq_causal_488_262144.ckpt": 699955790},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + " (23 checkpoint files listed); nothing downloaded",
  "quote_ids": ["w_file", "w_gated"]
 },
 "licence": {
  "id": "MIT (HF card licence: mit; LICENSE in microsoft/VidTok)",
  "url": "https://github.com/microsoft/VidTok/blob/main/LICENSE",
  "commercial": "permitted by the MIT licence; the card adds that VidTok 'was developed for research and experimental purposes' (advisory, not a licence restriction)",
  "non_commercial_only": False,
  "restrictions": "none beyond MIT notice",
  "gating": "none",
  "quote_ids": ["lic_card", "lic_card2", "lic_text", "lic_grant", "lic_research_note"]
 },
 "domain": {
  "value": "video tokenizer family (3D/2D conv autoencoder with AlphaBlender temporal sampling; KL or FSQ regularizer) for video generation / world models; trained on a self-collected set of natural videos",
  "quote_ids": ["dom_family", "dom_downstream", "data_card1"]
 },
 "architecture": {
  "type": "convolutional video autoencoder: separate spatial (2D) and temporal (AlphaBlender + 1D/3D conv) down/up-sampling; causal or non-causal; KL (continuous) or FSQ (discrete) bottleneck",
  "representation": "encoder latents: C channels (4/8/16 for KL; FSQ codes for discrete) on a (1+(T-1)/4) x H/8 x W/8 grid for 4x8x8 causal variants"
 },
 "pretraining_data": {
  "summary": "Self-collected natural-video dataset in two subsets: model card says Training Set 1 ~400K low-res (480p) videos and Training Set 2 ~10K high-res (1080p) videos; the paper says ~10 million and ~6 million videos respectively (inconsistent counts between card and paper, recorded as found). No dataset or provider named. Evaluation on MCL-JCV and a web-video validation set (WebVid-Val) only.",
  "form": "described only"
 },
 "pretraining_data_quote": {"quote_ids": ["data_paper", "data_card1", "data_card2", "data_v11"]},
 "medical_video_in_data": {
  "answer": "NOT MENTIONED",
  "basis": "data are self-collected and described only as 'natural videos with diverse lighting, motions, and scenarios'; term search of card, GitHub README and paper finds no medical/surgical term.",
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}
 },
 "appendix300_possible": {
  "answer": "UNKNOWN",
  "basis_class": "undisclosed",
  "basis": "self-collected video dataset with no source list. Timing: released 2024-12 (v1.1 2025-03), before the OPARA issue 2026-04-29; prior circulation of the source recordings cannot be excluded from the documentation.",
  "quote_ids": ["data_paper"]
 },
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "undisclosed",
  "basis": "undisclosed self-collected data -> the documentation does not allow the Appendix300 source recordings to be excluded.",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_paper", "data_card1"]
 },
 "input": {
  "frame_size": {"value": "training: 128x128 (stage 1), 256x256 (stage 2, decoder fine-tune); evaluation/inference 256x256 (input size 17x256x256 causal, 16x256x256 non-causal)", "quote_ids": ["in_stage1", "in_stage2", "in_eval_size"]},
  "frame_rate_or_sampling": {"value": "training data sampled at 3 fps; evaluation at 30 fps ('sample fps of 30'); v1.1 inference examples use --sample_fps 30", "quote_ids": ["in_fps_train", "in_eval_size", "in_v11_infer"]},
  "clip_length_frames": {"value": "17 frames (causal) / 16 frames (non-causal); v1.1 causal models: arbitrary length, processed in chunks (recommended chunk size 16)", "quote_ids": ["in_eval_size", "data_v11", "in_v11_infer"]},
  "temporal_compression": {"value": "4x for the version (also 2x and 8x variants); 17 -> 5 latent frames (causal)", "quote_ids": ["in_row_16chn"]},
  "spatial_compression": {"value": "8x8 for the version (also 4x4 and 16x16 variants)", "quote_ids": ["in_row_16chn"]}
 },
 "embedding_dim": {
  "value": "16 channels x 5 x 32 x 32 = 81,920 values per 17-frame 256x256 clip (KL-16chn, 4x8x8 causal); other variants e.g. KL-4chn 4 x 5 x 32 x 32 = 20,480",
  "derivation": "Table 5 latent size 5x32x32 for 17x256x256 input at 4x8x8; channel count from the regularizer name KL-16chn",
  "quote_ids": ["in_row_16chn", "in_v11_row"]
 },
 "params": {
  "value": "157M (whole tokenizer, KL-16chn causal 4x8x8; same for KL-4chn/8chn and FSQ 4x8x8 causal); 199M for 4x16x16 variants; encoder-only count not documented",
  "scope": "whole autoencoder (encoder + decoder), per paper Table 5",
  "quote_ids": ["in_row_16chn"]
 },
 "flops_per_input_if_documented": {
  "value": "10.35 TFLOPs for the proposed architecture with the KL-4chn regularizer (paper Table 2, 'Ours', 157M); input size not stated in the table (inferred 17x256x256, the Table 5 input for this 157M model); scope (encoder+decoder) not stated",
  "quote_ids": ["flops", "flops_reg"]
 },
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists the v1.0 and v1.1 checkpoint files, gated=False", "quote_ids": ["w_file", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "MIT licence (card + LICENSE)", "quote_ids": ["lic_card2", "lic_grant"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video tokenizer (autoencoder) for video generation / world models, trained on general natural video", "quote_ids": ["dom_family", "dom_downstream"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": "training data = 'self-collected video dataset' described only by size, resolution and content in general terms; no datasets or named sources", "quote_ids": ["data_paper", "data_card1"]},
  "eligible": "NO (fails C4)"
 },
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"checkpoints/vidtok_v1_1/vidtok_kl_causal_488_16chn_v1_1.ckpt\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "lic_card", "quote": "license: mit license_link: https://github.com/microsoft/VidTok/blob/main/LICENSE", "source_file": C},
  {"id": "lic_card2", "quote": "The model is released under the [MIT license](https://github.com/microsoft/VidTok/blob/main/LICENSE).", "source_file": C},
  {"id": "lic_text", "quote": "MIT License Copyright (c) Microsoft Corporation.", "source_file": LIC},
  {"id": "lic_grant", "quote": "Permission is hereby granted, free of charge, to any person obtaining a copy", "source_file": LIC},
  {"id": "lic_research_note", "quote": "VidTok was developed for research and experimental purposes. Further testing and validation are needed before considering its application in commercial or real-world scenarios.", "source_file": C},
  {"id": "dom_family", "quote": "VidTok is a cutting-edge family of video tokenizers that delivers state-of-the-art performance in both continuous and discrete tokenizations with various compression rates.", "source_file": C},
  {"id": "dom_downstream", "quote": "* Video generation on the continuous / discrete latent tokens.", "source_file": C},
  {"id": "data_card1", "quote": "1. Training Set 1 consists of approximately 400K of low-resolution videos (e.g., 480p). The videos are natural videos with diverse lightning, motions, and scenarios.", "source_file": C},
  {"id": "data_card2", "quote": "2. Training Set 2 includes approximately 10K of high-resolution videos (e.g., 1080p). The videos are natural videos with diverse lightning, motions, and scenarios.", "source_file": C},
  {"id": "data_paper", "quote": "For training, we utilize a self-collected video dataset, divided into two subsets based on video quality: (1) Training Set 1, comprising approximately 10 10 million low-resolution videos (e.g., 480p); and (2) Training Set 2, consisting of approximately 6 6 million high-resolution videos (e.g., 1080p). All videos in the dataset are natural videos characterized by diverse lighting conditions, motion patterns, and scenarios.", "source_file": P},
  {"id": "data_v11", "quote": "VidTok v1.1 is an update for causal models. We fine-tuned all causal models on long videos to support tokenization and reconstruction of videos of arbitrary length with fine temporal smoothness.", "source_file": G},
  {"id": "in_stage1", "quote": "In the first training stage, Training Set 1 is resized to a resolution of 128 × 128 128\\times 128 and used for initial model training.", "source_file": P},
  {"id": "in_stage2", "quote": "In the second stage, Training Set 2 is resized to 256 × 256 256\\times 256 and employed for fine-tuning. We fine-tune the decoder for another 30,000 30,000 steps with batch size 8 8 .", "source_file": P},
  {"id": "in_fps_train", "quote": "The frame rate of the training data is maintained at 3 3 frames per second (FPS) during both stages.", "source_file": P},
  {"id": "in_eval_size", "quote": "with a sample fps of 30. The input size is `17x256x256` for causal models and `16x256x256` for non-causal models.", "source_file": C},
  {"id": "in_v11_infer", "quote": "--input_height 256 --input_width 256 --sample_fps 30 --chunk_size CHUNK_SIZE --output_video_dir OUTPUT_DIR --read_long_video # Set `CHUNK_SIZE` according to your GPU memory, recommendly 16.", "source_file": G},
  {"id": "in_row_16chn", "quote": "KL - 16chn ✓ 17 × 256 × 256 17\\times 256\\times 256 4 × 8 × 8 4\\times 8\\times 8 5 × 32 × 32 5\\times 32\\times 32 157M 35.04 0.942 0.047 78.9", "source_file": P},
  {"id": "in_v11_row", "quote": "| [vidtok_kl_causal_488_16chn_v1_1](https://huggingface.co/microsoft/VidTok/blob/main/checkpoints/vidtok_v1_1/vidtok_kl_causal_488_16chn_v1_1.ckpt) | KL-16chn | ✔️ | 4x8x8 | 35.13 | 0.941 | 0.049 | 87.4 |", "source_file": G},
  {"id": "flops", "quote": "Method Param. FLOPs PSNR ↑ \\uparrow SSIM ↑ \\uparrow LPIPS ↓ \\downarrow FVD ↓ \\downarrow Variant 1 245M 16.98 T 29.39 0.847 0.117 176.9 Variant 2 142M 7.17 T 29.36 0.846 0.119 185.7 Variant 3 126M 10.18 T 29.26 0.846 0.120 200.6 Ours 157M 10.35 T 29.64 0.852 0.114 194.2", "source_file": P},
  {"id": "flops_reg", "quote": "Table 2: Ablation study on the model architecture. Variant 1: fully 3D architecture. Variant 2: w/o AlphaBlender. Variant 3: w/o 3D architecture. We use ‘KL - 4chn’ as regularizer for all settings.", "source_file": P}
 ]
}
save_record(rec)
