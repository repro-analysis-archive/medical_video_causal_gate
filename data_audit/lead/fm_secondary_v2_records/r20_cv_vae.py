import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "cvvae_AILab-CVC__CV-VAE_hfapi.json"; HF = "cvvae_hf_README.md"; C = "cvvae_hf_vae3d_config.json"
C11 = "cvvae_hf_vae3d_v1-1_config.json"; RM = "cvvae_github_README.md"; P = "cvvae_arxiv_2405.20279_fulltext.txt"
DATA_FILES = [P, RM]

rec = {
 "id": "20_cv_vae",
 "name": "CV-VAE (AILab-CVC / Tencent AI Lab; HF AILab-CVC/CV-VAE: vae3d, vae3d_v1-1, vae3d_sd3)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "AILab-CVC/CV-VAE vae3d/ (original 4-channel CV-VAE, released 2024-06-03; diffusion_pytorch_model.safetensors + cv_vae.ckpt); also vae3d_v1-1/ ('updated ... with better performance', 2024-10-14) and vae3d_sd3/ (16-channel, SD3-compatible); paper arXiv:2405.20279 (NeurIPS 2024)",
 "paper": {"title": "CV-VAE: A Compatible Video VAE for Latent Generative Video Models", "year": 2024, "arxiv": "2405.20279"},
 "weights_location": {
  "urls": ["https://huggingface.co/AILab-CVC/CV-VAE/tree/main/vae3d", "https://huggingface.co/AILab-CVC/CV-VAE/tree/main/vae3d_v1-1", "https://huggingface.co/AILab-CVC/CV-VAE/tree/main/vae3d_sd3"],
  "files_listed": {"vae3d/diffusion_pytorch_model.safetensors": 729812244, "vae3d/cv_vae.ckpt": 904840525,
                   "vae3d_v1-1/diffusion_pytorch_model.safetensors": 364919214, "vae3d_sd3/diffusion_pytorch_model.safetensors": 727597660},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; nothing downloaded",
  "quote_ids": ["w_file", "w_gated", "w_release", "w_v11"]
 },
 "licence": {
  "id": "Apache-2.0 (HF card); the GitHub repository has no LICENSE file (GitHub API license: null)",
  "url": "https://huggingface.co/AILab-CVC/CV-VAE",
  "commercial": "permitted (Apache-2.0)", "non_commercial_only": False,
  "restrictions": "none beyond Apache-2.0 (derived from the SD image VAE, upstream licence not audited)", "gating": "none",
  "quote_ids": ["lic_card"]
 },
 "domain": {"value": "3D (2D+3D) causal-encoder video VAE whose latent space is compatible with SD2.1 / SVD, for latent generative video models; trained on WebVid-10M video + LAION-COCO / Unsplash images", "quote_ids": ["dom_tldr", "data_train"]},
 "architecture": {"type": "KL video VAE inflated from the Stable Diffusion image VAE (half 2D, half 3D convolutions), temporal downsampling by strides, latent-space regularisation to the SD image VAE",
                  "representation": "encoder latents, 4 channels (z_channels 4), 4x temporal x 8x8 spatial; vae3d_sd3 variant 16 channels"},
 "pretraining_data": {"summary": "Images: LAION-COCO, Unsplash; video: WebVid-10M (9x256x256 and 17x192x192 clips). Initialised from the SD image VAE. The v1-1 and SD3 variants' data are not separately documented.",
                      "form": "dataset list (named)"},
 "pretraining_data_quote": {"quote_ids": ["data_train", "data_video", "data_init"]},
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "WebVid-10M is scraped stock footage (Shutterstock), open-ended content; term search of the paper and README finds no medical/surgical data statement",
                           "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "named_open_web_sources",
  "basis": "video data = WebVid-10M (named, but scraped from stock-footage sites, open-ended at item level), so the documentation does not allow the Appendix300 source recordings to be excluded. Timing: 2024-06 / 2024-10, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_train"]},
 "appendix300_check": {
  "answer": "UNKNOWN", "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "named_open_web_sources", "basis": "WebVid-10M (stock footage, open-ended)",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_train"]
 },
 "input": {
  "frame_size": {"value": "video training 256x256 (9 frames) and 192x192 (17 frames); images 256 and 512; tiled encoding (tile_spatial_size 576) for larger inputs", "quote_ids": ["data_video", "in_tile"]},
  "frame_rate_or_sampling": {"value": "training fps/stride not stated; evaluation clips sampled with a frame stride of 3", "quote_ids": ["in_eval"]},
  "clip_length_frames": {"value": "9 or 17 training frames (causal 1 + 4k); evaluation 33 frames; temporal tiling encodes 16 frames at a time", "quote_ids": ["data_video", "in_eval", "in_nframes"]},
  "temporal_compression": {"value": "4x (causal encoder)", "quote_ids": ["in_tc", "in_causal"]},
  "spatial_compression": {"value": "8x8", "quote_ids": ["in_sc"]}
 },
 "embedding_dim": {"value": "4 latent channels x (1 + (T-1)/4) x H/8 x W/8; e.g. 17 x 192 x 192 -> 4 x 5 x 24 x 24 = 11,520; 33 x 256 x 256 -> 4 x 9 x 32 x 32 = 36,864 values (vae3d_sd3: 16 channels)",
                   "derivation": "z_channels 4, time_n_compress 4, spatial_n_compress 8, causal encoder", "quote_ids": ["in_z", "in_tc", "in_sc", "in_causal", "p_sd3"]},
 "params": {"value": "encoder 68M + decoder 114M (CV-VAE 2D+3D, paper Table 1); CVVAE-SD3 also 68M + 114M", "scope": "encoder 68M", "quote_ids": ["p_main", "p_sd3"]},
 "flops_per_input_if_documented": None,
 "flops_note": "paper says the 2D+3D design reduces parameters and computation by ~30% vs full 3D, but gives no FLOPs per input (searched FLOP)",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists vae3d/diffusion_pytorch_model.safetensors, gated=False", "quote_ids": ["w_file", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "Apache-2.0 on the HF card (no LICENSE file in the GitHub repo)", "quote_ids": ["lic_card"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE for latent generative video models, trained on general video", "quote_ids": ["dom_tldr"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "paper names the training datasets (WebVid-10M video; LAION-COCO, Unsplash images); caveat: v1-1 / SD3 variants' data not separately documented; SD image-VAE initialisation", "quote_ids": ["data_train"]},
  "eligible": "YES (all four criteria PASS for vae3d; Appendix300 UNKNOWN; caveats on variant data and SD initialisation)"
 },
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"vae3d/diffusion_pytorch_model.safetensors\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "w_release", "quote": "We have released the [inference code](cvvae_inference_video.py) and [model weights](https://huggingface.co/AILab-CVC/CV-VAE/tree/main/vae3d) of CV-VAE.", "source_file": RM},
  {"id": "w_v11", "quote": "We have updated the CV-VAE with better performance, please check [cv-vae-v1-1](https://huggingface.co/AILab-CVC/CV-VAE/tree/main/vae3d_v1-1).", "source_file": RM},
  {"id": "lic_card", "quote": "license: apache-2.0", "source_file": HF},
  {"id": "dom_tldr", "quote": "A video VAE for latent generative video models, which is compatible with pretrained image and video models, e.g., SD 2.1 and SVD", "source_file": RM},
  {"id": "data_train", "quote": "Training Details. We train our CV-VAE model using image datasets including LAION-COCO [ 9 ] and Unsplash [ 23 ] , as well as the video dataset Webvid-10M [ 3 ] .", "source_file": P},
  {"id": "data_video", "quote": "In the case of video datasets, we use two settings of frames and resolutions: 9 × 256 × 256 9 256 256 9\\times 256\\times 256 9 × 256 × 256 and 17 × 192 × 192 17 192 192 17\\times 192\\times 192 17 × 192 × 192 .", "source_file": P},
  {"id": "data_init", "quote": "The architecture of CV-VAE is primarily derived from the VAE in Stable Diffusion [ 28 ] , with several notable differences: (1) Some or all 2D convolutions within the network are transformed into 3D convolutions, while retaining their weights.", "source_file": P},
  {"id": "in_eval", "quote": "Each video is sampled with 33 frames and a frame stride of 3.", "source_file": P},
  {"id": "in_tile", "quote": "\"tile_spatial_size\": 576,", "source_file": C},
  {"id": "in_nframes", "quote": "\"en_de_n_frames_a_time\": 16,", "source_file": C},
  {"id": "in_tc", "quote": "\"time_n_compress\": 4,", "source_file": C},
  {"id": "in_sc", "quote": "\"spatial_n_compress\": 8,", "source_file": C},
  {"id": "in_causal", "quote": "\"causal_encoder\": true,", "source_file": C},
  {"id": "in_z", "quote": "\"z_channels\": 4", "source_file": C},
  {"id": "p_main", "quote": "Ours(2D+3D) 68M + 114M 4x", "source_file": P},
  {"id": "p_sd3", "quote": "CVVAE-SD3 68M + 114M 4x", "source_file": P}
 ]
}
save_record(rec)
