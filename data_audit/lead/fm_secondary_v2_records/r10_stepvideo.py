import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "stepvideo_stepfun-ai__stepvideo-t2v_hfapi.json"; CARD = "stepvideo_stepvideo-t2v_README.md"
GH = "stepvideo_github_README.md"; LIC = "stepvideo_github_LICENSE.txt"; P = "stepvideo_arxiv_2502.10248_fulltext.txt"
VAE = "stepvideo_github_vae.py.txt"; SRV = "stepvideo_github_call_remote_server.py.txt"; CFG = "stepvideo_github_config.py.txt"
TC = "stepvideo_stepvideo-t2v_transformer_config.json"
DATA_FILES = [P, CARD, GH]

rec = {
 "id": "10_stepvideo_vae",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "name": "Step-Video-T2V Video-VAE (StepFun; deep-compression causal VAE, 8x16x16, 64 channels; vae_v2.safetensors)",
 "version": "stepfun-ai/stepvideo-t2v vae/vae_v2.safetensors (version=2, z_channels=64; the default in the official VAE server) (HF repo sha 7a2b639ca2685350e87a4df7e4026285309f7fb6, created 2025-02-14); the repo also ships vae/vae.safetensors (version 1, z_channels 16)",
 "paper": {"title": "Step-Video-T2V Technical Report: The Practice, Challenges, and Future of Video Foundation Model", "year": 2025, "arxiv": "2502.10248", "version_read": "arXiv HTML v3 (2025-02-24)"},
 "weights_location": {
  "urls": ["https://huggingface.co/stepfun-ai/stepvideo-t2v/tree/main/vae"],
  "files_listed": {"vae/vae_v2.safetensors": 1995304052, "vae/vae.safetensors": 1035340564},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; nothing downloaded",
  "quote_ids": ["w_v2", "w_v1", "w_gated", "w_srv_default", "w_srv_files"]
 },
 "licence": {
  "id": "MIT (HF card license: mit; GitHub LICENSE 'MIT License, Copyright (c) 2025 stepfun-ai')",
  "url": "https://huggingface.co/stepfun-ai/stepvideo-t2v ; https://github.com/stepfun-ai/Step-Video-T2V/blob/main/LICENSE",
  "commercial": "permitted", "non_commercial_only": False,
  "restrictions": "none beyond MIT",
  "gating": "none",
  "quote_ids": ["lic_card", "lic_text", "lic_grant"]
 },
 "domain": {
  "value": "deep-compression video VAE of the Step-Video-T2V 30B text-to-video diffusion model; trained jointly on images and videos from the authors' large-scale general web-video dataset (sources not named)",
  "quote_ids": ["dom_intro", "dom_vae", "arch_train"]
 },
 "architecture": {
  "type": "causal 3D-conv VAE with dual-path (conv + pixel-unshuffle channel-averaging) latent fusion; 8x16x16 down-scaling; trained in stages from a 4x8x8 VAE; KL + GAN losses",
  "representation": "encoder latents: 64 channels per latent voxel (v2); the encoder processes 17-frame chunks, each -> 3 latent frames"
 },
 "pretraining_data": {
  "summary": "Pre-training dataset of 2B video-text pairs and 3.8B image-text pairs built from 'raw videos' by a segmentation / quality / motion / captioning / concept-balancing pipeline (captions partly reuse 'original titles from the raw videos'); VAE trained 'jointly on images and videos'. No datasets or providers named.",
  "form": "described only"
 },
 "pretraining_data_quote": {"quote_ids": ["data_main", "data_raw", "data_titles", "arch_train"]},
 "medical_video_in_data": {
  "answer": "NOT MENTIONED",
  "basis": "Automated search of the saved paper text, HF card and GitHub README for medical|surgical|surgery|endoscop|laparoscop|clinical|health|hospital: only 'healthy nodes' / 'health checks' (training-cluster infrastructure); no data statement.",
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}
 },
 "appendix300_possible": {
  "answer": "UNKNOWN", "basis_class": "undisclosed",
  "basis": "raw-video sources undisclosed (web-like: original titles reused as captions). Timing: released 2025-02-14/17, before the OPARA issue 2026-04-29; prior circulation of the source recordings not documented.",
  "quote_ids": ["data_main", "data_titles"]
 },
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "undisclosed",
  "basis": "no source list for the 2B video-text pairs exists, so the Appendix300 source recordings cannot be excluded.",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_main", "data_raw"]
 },
 "input": {
  "frame_size": {"value": "540p model; default 544x992 (inference config); card benchmark 544px992px204f", "quote_ids": ["in_res", "in_height", "in_width", "in_table"]},
  "frame_rate_or_sampling": {"value": "not documented (no fps statement in the saved card, README, paper or config)", "quote_ids": []},
  "clip_length_frames": {"value": "up to 204 frames (default num_frames 204); the VAE encodes in 17-frame chunks (frame_len 17)", "quote_ids": ["dom_intro", "in_frames", "arch_frame_len", "arch_chunk"]},
  "temporal_compression": {"value": "8x (causal; per 17-frame chunk -> 3 latent frames in version 2)", "quote_ids": ["dom_vae", "arch_8x16x16", "arch_causal", "arch_frame_len"]},
  "spatial_compression": {"value": "16x16", "quote_ids": ["dom_vae", "arch_8x16x16"]}
 },
 "embedding_dim": {
  "value": "64 latent channels x 3 x 34 x 62 = 404,736 values per 17-frame 544x992 chunk; a 204-frame 544x992 clip (12 chunks) -> 64 x 36 x 34 x 62 = 4,856,832 (inferred from the released code's chunking)",
  "derivation": "z_channels 64 for vae_v2 (server code; DiT in_channels 64); latent_len 3 per frame_len 17 chunk (version 2); spatial /16; 544/16 = 34, 992/16 = 62",
  "quote_ids": ["w_srv_files", "arch_dit_in", "arch_frame_len", "arch_chunk", "arch_8x16x16", "in_height", "in_width"]
 },
 "params": {
  "value": "not documented for the VAE (paper/card give only the 30B DiT). Inferred only: vae_v2.safetensors 1,995,304,052 bytes ~ 499M parameters if fp32 (encoder + decoder; dtype not stated)",
  "scope": "not documented",
  "quote_ids": ["w_v2"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "the paper's FLOPs table (Table 3, 'FLOPs per sample of different resolutions') refers to DiT training samples, not to the VAE encoder; no VAE FLOPs/MACs are documented",
 "flops_context": {"value": "DiT-level FLOPs only (not VAE)", "quote_ids": ["flops_dit"]},
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists vae/vae_v2.safetensors and vae/vae.safetensors, gated=False", "quote_ids": ["w_v2", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "MIT", "quote_ids": ["lic_card", "lic_text"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE of a general text-to-video diffusion model", "quote_ids": ["dom_intro", "dom_vae"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": "data described only as 2B video-text pairs from 'raw videos'; no datasets or named sources", "quote_ids": ["data_main", "data_raw"]},
  "eligible": "NO (fails C4)"
 },
 "quotes": [
  {"id": "w_v2", "quote": "\"rfilename\": \"vae/vae_v2.safetensors\",", "source_file": API},
  {"id": "w_v1", "quote": "\"rfilename\": \"vae/vae.safetensors\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "w_srv_default", "quote": "def __init__(self, vae_dir, version=2):", "source_file": SRV},
  {"id": "w_srv_files", "quote": "(model_name, z_channels) = (\"vae_v2.safetensors\", 64) if version == 2 else (\"vae.safetensors\", 16)", "source_file": SRV},
  {"id": "lic_card", "quote": "license: mit", "source_file": CARD},
  {"id": "lic_text", "quote": "MIT License Copyright (c) 2025 stepfun-ai", "source_file": LIC},
  {"id": "lic_grant", "quote": "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction", "source_file": LIC},
  {"id": "dom_intro", "quote": "We present **Step-Video-T2V**, a state-of-the-art (SoTA) text-to-video pre-trained model with 30 billion parameters and the capability to generate videos up to 204 frames.", "source_file": CARD},
  {"id": "dom_vae", "quote": "A deep compression Variational Autoencoder (VideoVAE) is designed for video generation tasks, achieving 16x16 spatial and 8x temporal compression ratios while maintaining exceptional video reconstruction quality.", "source_file": CARD},
  {"id": "arch_8x16x16", "quote": "This design achieves 8 × 16 × 16 8{\\times}16{\\times}16 downscaling through the synergistic use of 3D convolutions and optimized pixel unshuffling operations.", "source_file": P},
  {"id": "arch_causal", "quote": "To enable joint image and video modeling, we employ temporal causal 3D convolution.", "source_file": P},
  {"id": "arch_train", "quote": "In the first stage, we train a VAE with a 4x8x8 compression ratio without employing a dual-path structure. This initial training is conducted jointly on images and videos of varying frame counts, adhering to a preset ratio.", "source_file": P},
  {"id": "arch_frame_len", "quote": "self.frame_len = 17 self.latent_len = 3 if version == 2 else 5", "source_file": VAE},
  {"id": "arch_chunk", "quote": "chunks = list(x.split(self.frame_len, dim=1))", "source_file": VAE},
  {"id": "arch_dit_in", "quote": "\"in_channels\": 64,", "source_file": TC},
  {"id": "in_res", "quote": "\"--model_resolution\", type=str, default=\"540p\",", "source_file": CFG},
  {"id": "in_frames", "quote": "\"--num_frames\", type=int, default=204,", "source_file": CFG},
  {"id": "in_height", "quote": "\"--height\", type=int, default=544,", "source_file": CFG},
  {"id": "in_width", "quote": "\"--width\", type=int, default=992,", "source_file": CFG},
  {"id": "in_table", "quote": "| Step-Video-T2V | 544px992px204f | 77.64 GB | 743 s | 1232 s |", "source_file": CARD},
  {"id": "data_main", "quote": "7.1 Pre-training Data We constructed a large-scale video dataset comprising 2B video-text pairs and 3.8B image-text pairs.", "source_file": P},
  {"id": "data_raw", "quote": "Leveraging a comprehensive data pipeline, we transformed raw videos into high-quality video-text pairs suitable for model pre-training.", "source_file": P},
  {"id": "data_titles", "quote": "Original Title : We also included a variety of caption styles by incorporating a portion of the original titles from the raw videos, adding diversity to the captions.", "source_file": P},
  {"id": "flops_dit", "quote": "Table 3 outlines the FLOPs per sample of different resolutions.", "source_file": P}
 ]
}
save_record(rec)
