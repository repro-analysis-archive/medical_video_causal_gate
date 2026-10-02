import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_lib import save_record
C2 = "cogvideox_CogVideoX-2b_README.md"; L5 = "cogvideox_CogVideoX-5b_LICENSE"; V = "cogvideox_CogVideoX-2b_vae_config.json"
P = "cogvideox_arxiv_2408.06072_fulltext.html"; CC = "cosmos_Cosmos-Tokenize1-CV8x8x8-720p_README.md"
rec = {
 "id": "03_cogvideox_vae",
 "name": "CogVideoX 3D causal VAE (AutoencoderKLCogVideoX; shipped in CogVideoX-2b / CogVideoX-5b)",
 "paper": {"title": "CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer", "year": 2024, "arxiv": "2408.06072"},
 "weights": {
   "urls": ["https://huggingface.co/zai-org/CogVideoX-2b (formerly THUDM/CogVideoX-2b; subfolder vae/)", "https://huggingface.co/zai-org/CogVideoX-5b"],
   "hf_api_evidence": ["cogvideox_CogVideoX-2b_hfapi_blobs.json", "cogvideox_CogVideoX-5b_hfapi_blobs.json"],
   "files_listed": {"CogVideoX-2b vae/diffusion_pytorch_model.safetensors": 862388596, "CogVideoX-5b vae/diffusion_pytorch_model.safetensors": 862388596},
   "gated": False, "private": False,
   "note": "THUDM/* redirects to zai-org/*. Same VAE file size in both repos. Not downloaded."
 },
 "licence": {
   "id": "Apache-2.0 (CogVideoX-2B incl. its VAE module); 'The CogVideoX License' (CogVideoX-5B transformer)",
   "url": "https://huggingface.co/zai-org/CogVideoX-2b/blob/main/LICENSE ; https://huggingface.co/THUDM/CogVideoX-5b/blob/main/LICENSE",
   "commercial": "Apache-2.0 for the 2B VAE; 5B licence requires registration for commercial use", "non_commercial_only": False,
   "restrictions": "5B licence: no military/illegal use, and a clause on China's national security; Apache-2.0 for the VAE as distributed with 2B",
   "gating": "none",
   "quote_ids": ["lic_2b", "lic_5b_research", "lic_5b_restr"]
 },
 "architecture": {
   "type": "3D causal convolutional VAE (KL), temporally causal conv",
   "params": "216M (Cosmos card runtime table, 'CogVideoX' 4x8x8 tokenizer); VAE fp32 file 862 MB is consistent (~216M)",
   "representation": "VAE encoder latents (16 channels), 8x8 spatial x 4x temporal",
   "input_resolution": "720x480 for CogVideoX-2b/5b generation (VAE trained at 256x256, encodes larger frames without retraining)",
   "frames_per_clip": "49 frames (6 s @ 8 fps) for generation; VAE first trained on 17 frames",
   "temporal_compression": "4x", "spatial_compression": "8x8",
   "quote_ids": ["arch_vae_class", "arch_latent", "arch_tcomp", "arch_8x8x4", "arch_res", "arch_vae_train", "arch_params"]
 },
 "pretraining_data": {
   "summary": "~35M filtered single-shot video clips (source not named) + 2B images from LAION-5B and COYO-700M. VAE training data not separately stated beyond 256x256, 17-frame video training.",
   "form": "described only for video (images: named datasets)",
   "quote_ids": ["data_main"]
 },
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "Search of saved paper HTML full text for medic|surg|endoscop|laparoscop|clinic|hospital|health: no hits. Negative-label filters remove editing, lectures, text-dominated, screenshots."},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "undisclosed", "basis": "video source of the 35M clips not disclosed. Context: paper v1 2024-08-12, weights 2024-08, before the OPARA issue 2026-04-29.", "quote_ids": ["data_main"]},
 "eligibility": {
   "C1_open_weights": {"status": "PASS", "basis": "HF API lists vae/diffusion_pytorch_model.safetensors, gated=False"},
   "C2_licence_research_use": {"status": "PASS", "basis": "Apache-2.0 for the 2B VAE; 5B licence explicitly allows academic research"},
   "C3_domain_secondary": {"status": "PASS", "basis": "3D video VAE of a text-to-video diffusion model trained on general video"},
   "C4_documented_pretraining_data": {"status": "FAIL", "basis": "video data described only as a filtered collection of ~35M clips; only the image datasets (LAION-5B, COYO-700M) are named"},
   "eligible": "NO (fails C4 for the video data)"
 },
 "quotes": [
  {"id": "lic_2b", "quote": "The CogVideoX-2B model (including its corresponding Transformers module and VAE module) is released under the [Apache 2.0 License](LICENSE).", "source_file": C2},
  {"id": "lic_5b_research", "quote": "This license allows you to freely use all open-source models in this repository for academic research.", "source_file": L5},
  {"id": "lic_5b_restr", "quote": "You will not use, copy, modify, merge, publish, distribute, reproduce, or create derivative works of the Software, in whole or in part, for any military, or illegal purposes.", "source_file": L5},
  {"id": "arch_vae_class", "quote": "\"_class_name\": \"AutoencoderKLCogVideoX\",", "source_file": V},
  {"id": "arch_latent", "quote": "\"latent_channels\": 16,", "source_file": V},
  {"id": "arch_tcomp", "quote": "\"temporal_compression_ratio\": 4,", "source_file": V},
  {"id": "arch_8x8x4", "quote": "It comprises an encoder, a decoder and a latent space regularizer, achieving a 8 × \\times 8 × \\times 4 compression from pixels to the latents.", "source_file": P},
  {"id": "arch_res", "quote": "720 x 480, no support for other resolutions (including fine-tuning)", "source_file": C2},
  {"id": "arch_vae_train", "quote": "During training, we first train a 3D VAE at 256 × 256 256\\times 256 resolution and 17 17 frames to save computation.", "source_file": P},
  {"id": "arch_params", "quote": "| CogVideoX      | 720x1280   | 4×8×8            | 216M       | 414       |", "source_file": CC},
  {"id": "data_main", "quote": "3.4 Data We construct a collection of relatively high-quality video clips with text descriptions with video filters and recaption models. After filtering, approximately 35M single-shot clips remain, with each clip averaging about 6 seconds. We additionally use 2B images filtered with aesthetics score from LAION-5B ( Schuhmann et al., 2022 ) and COYO-700M ( Byeon et al., 2022 ) datasets to assist training.", "source_file": P}
 ]
}
save_record(rec)
