import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "magi1_sand-ai__MAGI-1_hfapi.json"; HF = "magi1_hf_README.md"; C = "magi1_hf_vae_config.json"
P = "magi1_arxiv_2505.13211_fulltext.txt"
DATA_FILES = [P, HF]

rec = {
 "id": "24_magi1_vae",
 "name": "MAGI-1 transformer VAE (Sand AI; HF sand-ai/MAGI-1 ckpt/vae, ViTVAE)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "sand-ai/MAGI-1 ckpt/vae/diffusion_pytorch_model.safetensors + config.json (HF repo created 2025-04-18); paper arXiv:2505.13211",
 "paper": {"title": "MAGI-1: Autoregressive Video Generation at Scale", "year": 2025, "arxiv": "2505.13211"},
 "weights_location": {
  "urls": ["https://huggingface.co/sand-ai/MAGI-1/tree/main/ckpt/vae"],
  "files_listed": {"ckpt/vae/diffusion_pytorch_model.safetensors": 2455072868, "ckpt/vae/config.json": 438},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; nothing downloaded",
  "quote_ids": ["w_file", "w_gated", "w_card_row"]
 },
 "licence": {"id": "Apache-2.0", "url": "https://huggingface.co/sand-ai/MAGI-1 ; https://github.com/SandAI-org/MAGI-1", "commercial": "permitted", "non_commercial_only": False,
             "restrictions": "none beyond Apache-2.0", "gating": "none", "quote_ids": ["lic_card", "lic_text"]},
 "domain": {"value": "transformer-based video VAE of the autoregressive video diffusion world model MAGI-1; trained on a large internal pool of web-scale videos/images", "quote_ids": ["dom_card", "dom_vae"]},
 "architecture": {"type": "ViT VAE: 3D conv patch embedding (8x8x4 kernel/stride, 1024 channels) + 24 transformer blocks; KL bottleneck",
                  "representation": "encoder latents, 16 channels (z_chans 16), T/4 x H/8 x W/8"},
 "pretraining_data": {"summary": "VAE trained on 16-frame 256x256 clips (stage 1), then joint image/video with variable resolution (stage 2); the MAGI-1 training data are built from 'tens of petabytes of raw videos and images collected from a wide range of sources' -- no dataset or provider named.",
                      "form": "described only"},
 "pretraining_data_quote": {"quote_ids": ["data_pool", "data_vae_train"]},
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "sources undisclosed; term search hits only in a reference title (U-Net, MICCAI), no data statement",
                           "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "undisclosed",
  "basis": "raw videos 'collected from a wide range of sources', not itemised. Timing: 2025-04/05, before the OPARA issue 2026-04-29.", "quote_ids": ["data_pool"]},
 "appendix300_check": {
  "answer": "UNKNOWN", "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "undisclosed", "basis": "undisclosed sources",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_pool"]
 },
 "input": {
  "frame_size": {"value": "stage 1: 256x256; stage 2: variable, ~256^2 or 384^2 pixels, aspect 0.25-4.0", "quote_ids": ["data_vae_train", "in_stage2"]},
  "frame_rate_or_sampling": {"value": "VAE training fps not stated; MAGI-1 generation chunks are 24 frames = 1 s at 24 FPS", "quote_ids": ["in_chunk"]},
  "clip_length_frames": {"value": "16-frame clips (VAE training; config video_length 16)", "quote_ids": ["data_vae_train", "in_len"]},
  "temporal_compression": {"value": "4x", "quote_ids": ["dom_card", "in_plen"]},
  "spatial_compression": {"value": "8x8", "quote_ids": ["dom_card", "in_psize"]}
 },
 "embedding_dim": {"value": "16 channels x T/4 x H/8 x W/8; 16 x 256 x 256 clip -> 16 x 4 x 32 x 32 = 65,536 values; encoder transformer width 1024",
                   "derivation": "z_chans 16, patch_length 4, patch_size 8, embed_dim 1024 (config.json)", "quote_ids": ["in_z", "in_plen", "in_psize", "in_embed"]},
 "params": {"value": "614M (whole VAE, paper Table 1); encoder-only not documented", "scope": "whole autoencoder", "quote_ids": ["p_614"]},
 "flops_per_input_if_documented": None,
 "flops_note": "paper gives encode/decode times (Table 1) but no VAE FLOPs per input",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists ckpt/vae/diffusion_pytorch_model.safetensors, gated=False", "quote_ids": ["w_file", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "Apache-2.0", "quote_ids": ["lic_card", "lic_text"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE of a video generative model trained on general video", "quote_ids": ["dom_card"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": "sources described only as raw videos and images 'collected from a wide range of sources'; no datasets or named sources", "quote_ids": ["data_pool"]},
  "eligible": "NO (fails C4)"
 },
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"ckpt/vae/diffusion_pytorch_model.safetensors\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "w_card_row", "quote": "| MAGI-1-VAE | [MAGI-1-VAE](https://huggingface.co/sand-ai/MAGI-1/tree/main/ckpt/vae) | - |", "source_file": HF},
  {"id": "lic_card", "quote": "license: apache-2.0", "source_file": HF},
  {"id": "lic_text", "quote": "This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.", "source_file": HF},
  {"id": "dom_card", "quote": "Variational autoencoder (VAE) with transformer-based architecture, 8x spatial and 4x temporal compression.", "source_file": HF},
  {"id": "dom_vae", "quote": "In the encoder, the input is first processed by an embedding module based on a 3D convolution with a kernel size of 8 × 8 × 4 8\\times 8\\times 4", "source_file": P},
  {"id": "data_pool", "quote": "we have developed a scalable data processing system that constructs the training dataset for Magi-1 from tens of petabytes of raw videos and images collected from a wide range of sources.", "source_file": P},
  {"id": "data_vae_train", "quote": "In the first stage, we use a fixed input resolution during training: 16-frame short clips with a spatial resolution of 256 × 256 256\\times 256 pixels, to maximize training efficiency by avoiding unnecessary padding.", "source_file": P},
  {"id": "in_stage2", "quote": "Specifically, we constrain the total number of pixels (height × \\times width) is approximately 256 2 256^{2} or 384 2 384^{2} , while sampling the aspect ratio uniformly from the range [0.25, 4.0].", "source_file": P},
  {"id": "in_chunk", "quote": "each chunk contains 24 raw frames (equivalent to one second video clip at 24 FPS)", "source_file": P},
  {"id": "in_len", "quote": "\"video_length\": 16,", "source_file": C},
  {"id": "in_plen", "quote": "\"patch_length\": 4,", "source_file": C},
  {"id": "in_psize", "quote": "\"patch_size\": 8,", "source_file": C},
  {"id": "in_z", "quote": "\"z_chans\": 16", "source_file": C},
  {"id": "in_embed", "quote": "\"embed_dim\": 1024,", "source_file": C},
  {"id": "p_614", "quote": "Ours 36.55 614 36.68 12.28", "source_file": P}
 ]
}
save_record(rec)
