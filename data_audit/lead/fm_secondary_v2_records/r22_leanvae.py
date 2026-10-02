import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "leanvae_Yumic__LeanVAE_hfapi.json"; HF = "leanvae_hf_README.md"; RM = "leanvae_github_README.md"
P = "leanvae_arxiv_2503.14325_fulltext.txt"
DATA_FILES = [P, RM, HF]

rec = {
 "id": "22_leanvae",
 "name": "LeanVAE (westlake-repl/LeanVAE; HF Yumic/LeanVAE: LeanVAE-dim4.ckpt, LeanVAE-dim16.ckpt)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "Yumic/LeanVAE LeanVAE-dim4.ckpt (4-channel) and LeanVAE-dim16.ckpt (16-channel) (HF repo created 2025-03-18); paper arXiv:2503.14325. The repo also holds Latte generator checkpoints (sky-/ucf-dim*.pt), not recorded",
 "paper": {"title": "LeanVAE: An Ultra-Efficient Reconstruction VAE for Video Diffusion Models", "year": 2025, "arxiv": "2503.14325"},
 "weights_location": {
  "urls": ["https://huggingface.co/Yumic/LeanVAE"],
  "files_listed": {"LeanVAE-dim4.ckpt": 159125886, "LeanVAE-dim16.ckpt": 159199850},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; the official GitHub README (westlake-repl/LeanVAE) links these files; nothing downloaded",
  "quote_ids": ["w_file4", "w_file16", "w_gated", "w_gh_link"]
 },
 "licence": {
  "id": "MIT (HF card; GitHub README)",
  "url": "https://huggingface.co/Yumic/LeanVAE ; https://github.com/westlake-repl/LeanVAE",
  "commercial": "permitted", "non_commercial_only": False, "restrictions": "none beyond MIT", "gating": "none",
  "quote_ids": ["lic_card", "lic_readme"]
 },
 "domain": {"value": "lightweight causal video VAE for latent video diffusion models; trained on Kinetics-600", "quote_ids": ["dom_card", "data_k600"]},
 "architecture": {"type": "non-overlapping patchify (4x8x8) + Neighborhood-Aware Feedforward (NAF) backbone, wavelet input enrichment, compressed-sensing (ISTA-Net+) latent channel bottleneck; causal latent",
                  "representation": "encoder latents, d = 4 or 16 channels, (T/4+1) x H/8 x W/8 for T+1 input frames"},
 "pretraining_data": {"summary": "Kinetics-600, resized/cropped to 96x128 ... 352x288 keeping aspect ratio, random 17 consecutive frames per step (paper 5.1). No other training data named.",
                      "form": "dataset list (named: Kinetics-600)"},
 "pretraining_data_quote": {"quote_ids": ["data_k600"]},
 "medical_video_in_data": {"answer": "NO", "basis": "single closed human-action dataset (Kinetics-600); term search: one hit only in background text ('wavelet transform is widely used in fields such as medical imaging'), no data statement",
                           "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}},
 "appendix300_possible": {"answer": "NO", "basis_class": "closed_curated_list",
  "basis": "Kinetics-600 only (closed fixed action-class research dataset -> NO under conventions_v2). Caveat: the paper's statement, not checkpoint-specific. Timing: 2025-03, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_k600"]},
 "appendix300_check": {
  "answer": "NO", "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "closed_curated_list", "basis": "Kinetics-600 only",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_k600"]
 },
 "input": {
  "frame_size": {"value": "trained at 96x128 to 352x288 (aspect preserved); card: encodes a 17-frame 1080p video without tiling", "quote_ids": ["data_k600", "in_1080"]},
  "frame_rate_or_sampling": {"value": "17 consecutive frames at the source frame rate (no fps stated)", "quote_ids": ["data_k600"]},
  "clip_length_frames": {"value": "17 in training; any 4n+1 frames at inference", "quote_ids": ["data_k600", "in_4n1"]},
  "temporal_compression": {"value": "4x (causal: T+1 -> T/4+1)", "quote_ids": ["in_latent"]},
  "spatial_compression": {"value": "8x8", "quote_ids": ["in_latent"]}
 },
 "embedding_dim": {"value": "d x (T/4+1) x H/8 x W/8 with d = 4 or 16; e.g. 17 x 256 x 256 -> 16 x 5 x 32 x 32 = 81,920 values (16-ch) or 20,480 (4-ch)",
                   "derivation": "README encode signature", "quote_ids": ["in_latent"]},
 "params": {"value": "39.8M (whole VAE, both 4ch and 16ch; encoder-only count not documented)", "scope": "whole autoencoder", "quote_ids": ["p_flops4", "p_flops16"]},
 "flops_per_input_if_documented": {"value": "0.203 TFLOPs listed for each checkpoint in the card table; the input size (and whether encode+decode) is not stated in the table; the paper's Fig. 3 TFLOPs are for 17-frame videos at several resolutions (values only in the figure)",
                                   "quote_ids": ["p_flops4", "p_flops16", "in_fig3"]},
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists LeanVAE-dim4.ckpt / LeanVAE-dim16.ckpt, gated=False; linked from the official README", "quote_ids": ["w_file4", "w_gated", "w_gh_link"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "MIT", "quote_ids": ["lic_card", "lic_readme"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE for latent video diffusion (generative) models, trained on general video", "quote_ids": ["dom_card"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "paper names the training dataset (Kinetics-600)", "quote_ids": ["data_k600"]},
  "eligible": "YES (all four criteria PASS; Appendix300 NO)"
 },
 "quotes": [
  {"id": "w_file4", "quote": "\"rfilename\": \"LeanVAE-dim4.ckpt\",", "source_file": API},
  {"id": "w_file16", "quote": "\"rfilename\": \"LeanVAE-dim16.ckpt\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "w_gh_link", "quote": "[LeanVAE-chn16.ckpt](https://huggingface.co/Yumic/LeanVAE/resolve/main/LeanVAE-dim16.ckpt?download=true)", "source_file": RM},
  {"id": "lic_card", "quote": "license: mit", "source_file": HF},
  {"id": "lic_readme", "quote": "This project is released under the **MIT License**.", "source_file": RM},
  {"id": "dom_card", "quote": "We present **LeanVAE**, a lightweight Video VAE designed for ultra-efficient video compression and scalable generation in Latent Video Diffusion Models (LVDMs).", "source_file": HF},
  {"id": "data_k600", "quote": "Training Details We train the model using Kinetics-600 dataset [ 7 ] . The videos are resized and cropped to resolutions ranging from 96 × 128 96\\times 128 to 352 × 288 352\\times 288 , with their original aspect ratios preserved. For each training step, we randomly sample 17 consecutive frames from a video.", "source_file": P},
  {"id": "in_1080", "quote": "Encodes and decodes a **17-frame 1080p video** in **3 seconds** using only **15GB of GPU memory** *(without tiling inference)*", "source_file": HF},
  {"id": "in_4n1", "quote": "video, video_rec = model.inference(video) ## Frame count must be 4n+1 (e.g., 5, 9, 13, 17...)", "source_file": RM},
  {"id": "in_latent", "quote": "latent = model.encode(video) # (B, C, T+1, H, W) → (B, d, T/4+1, H/8, W/8), where d=4 or 16", "source_file": RM},
  {"id": "p_flops4", "quote": "| **LeanVAE-4ch** | 26.04 | 0.0899 | 39.8M | 0.203 |", "source_file": HF},
  {"id": "p_flops16", "quote": "| **LeanVAE-16ch** | 30.15 | 0.0461 | 39.8M | 0.203 |", "source_file": HF},
  {"id": "in_fig3", "quote": "(a) Computational cost in terms of TFLOPs(bar plots, labeled in black) and encoding-decoding time (line plots, labeled in red). (b) Reconstruction quality metrics. All evaluations were conducted on 17-frame videos using a single NVIDIA A40 (48GB) GPU.", "source_file": P}
 ]
}
save_record(rec)
