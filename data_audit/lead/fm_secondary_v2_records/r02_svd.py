import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, prev_candidate, term_search, MED_TERMS, A300_TERMS

APIX = "svd_stabilityai__stable-video-diffusion-img2vid-xt_hfapi.json"
API14 = "svd_stabilityai__stable-video-diffusion-img2vid_hfapi.json"
R = "svd_xt_README.md"; R14 = "svd_14_README.md"; LIC = "svd_xt_LICENSE.md"; VC = "svd_xt_vae_config.json"
MI = "svd_xt_model_index.json"; P = "svd_arxiv_2311.15127.txt"
GM = "svd_github_generative-models_simple_video_sample.py.txt"
DF = "svd_diffusers_v0.24.0_pipeline_stable_video_diffusion.py.txt"
DATA_FILES = [P, R]
FMAP = {"svd_arxiv_2311.15127.pdf": P}

v1 = prev_candidate("02_stable_video_diffusion")
v1q = [{"id": q["id"], "quote": q["quote"], "source_file": FMAP.get(q["source_file"], q["source_file"])} for q in v1["quotes"]]

rec = {
 "id": "02_stable_video_diffusion",
 "name": v1["name"],
 "version": "stabilityai/stable-video-diffusion-img2vid-xt (SVD-XT, 25 frames; HF repo sha 9e43909513c6714f1bc78bcb44d96e733cd242aa, created 2023-11-20, last modified 2024-07-10) and stabilityai/stable-video-diffusion-img2vid (SVD, 14 frames; sha 9cf024d5bfa8f56622af86c884f26a52f6676f2e); VAE = vae/diffusion_pytorch_model.safetensors (AutoencoderKLTemporalDecoder, identical file size in both repos)",
 "paper": v1["paper"],
 "weights_location": {
  "urls": v1["weights"]["urls"],
  "files_listed_xt": v1["weights"]["files_listed_xt"],
  "files_listed_14": {"vae/diffusion_pytorch_model.safetensors": 391017740, "unet/diffusion_pytorch_model.fp16.safetensors": 3049435868, "svd.safetensors": 9559625980},
  "gated": False, "private": False,
  "verified_how": "HF API model listings (metadata only) saved as " + APIX + ", " + API14 + "; nothing downloaded",
  "note": v1["weights"]["note"],
  "quote_ids": ["w_vae_xt", "w_gated_xt", "w_vae_14", "w_gated_14"]
 },
 "licence": {
  "id": v1["licence"]["id"], "url": v1["licence"]["url"], "commercial": v1["licence"]["commercial"],
  "non_commercial_only": False, "restrictions": v1["licence"]["restrictions"], "gating": v1["licence"]["gating"],
  "quote_ids": ["lic_research", "lic_grant", "lic_aup"]
 },
 "domain": {
  "value": "generative image-to-video latent diffusion model (UNet with temporal layers) trained on general web-scale video (internal LVD); its VAE encoder is frame-wise (image f8 KL encoder), only the decoder is temporal",
  "quote_ids": ["dom_type", "arch_decoder", "arch_vae_class", "data_collect"]
 },
 "architecture": {"type": v1["architecture"]["type"], "representation": v1["architecture"]["representation"]},
 "pretraining_data": {"summary": v1["pretraining_data"]["summary"], "form": v1["pretraining_data"]["form"]},
 "pretraining_data_quote": {"quote_ids": ["data_collect", "data_lvd", "data_hq", "data_appendix", "arch_sd21"]},
 "medical_video_in_data": {
  "answer": v1["medical_video_in_data"]["answer"], "basis": v1["medical_video_in_data"]["basis"],
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}
 },
 "appendix300_possible": v1["appendix300_possible"],
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "undisclosed",
  "basis": v1["appendix300_possible"]["basis"],
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_collect"]
 },
 "input": {
  "frame_size": {"value": "576x1024 (generation / high-res finetune); base video pretraining 256x384 then 320x576; VAE config sample_size 768", "quote_ids": ["arch_frames", "in_base_res", "in_hires", "in_vae_sample"]},
  "frame_rate_or_sampling": {"value": "frame rate is a conditioning input (micro-conditioning on the training video's frame rate and motion score); default inference conditioning fps = 7 (diffusers pipeline) / fps_id = 6 (Stability sampling script); training-clip fps not documented", "quote_ids": ["in_fps_cond", "in_fps_cond_train", "in_fps_diffusers", "in_fps_gm"]},
  "clip_length_frames": {"value": "25 frames (SVD-XT) / 14 frames (SVD); base model trained on 14 frames", "quote_ids": ["arch_frames", "in_frames14", "in_base_res"]},
  "temporal_compression": {"value": "none (1x): the VAE encoder is frame-wise; only the decoder has temporal layers", "quote_ids": ["arch_decoder", "arch_vae_class", "in_framewise"]},
  "spatial_compression": {"value": "8x8 (f8 KL autoencoder)", "quote_ids": ["arch_decoder", "in_blocks"]}
 },
 "embedding_dim": {
  "value": "VAE latents: 4 channels x 72 x 128 per 576x1024 frame; 25-frame SVD-XT clip = 4 x 25 x 72 x 128 = 921,600 values (14-frame SVD: 516,096). Alternative representation = UNet intermediate features (dimension depends on the chosen block; not a single documented embedding).",
  "derivation": "latent_channels 4; 4 encoder blocks (3 downsamplings -> f8); frame-wise encoder so latent frames = input frames",
  "quote_ids": ["arch_vae_latent", "in_blocks", "arch_decoder"]
 },
 "params": {
  "value": "UNet: 1521M (paper; 656M temporal parameters added to the SD2.1 UNet). VAE encoder/decoder parameters not documented (inferred only: vae fp32 safetensors 391,017,740 bytes ~ 97.8M parameters incl. temporal decoder).",
  "scope": "UNet (generative backbone) documented; VAE not documented",
  "quote_ids": ["in_unet_params", "w_vae_xt"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs/MACs statement in the saved paper, cards, configs or sampling code (searched FLOP|MAC)",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": v1["eligibility"]["C1_open_weights"]["basis"], "quote_ids": ["w_vae_xt", "w_gated_xt"]},
  "C2_licence_research_use": {"status": "PASS", "basis": v1["eligibility"]["C2_licence_research_use"]["basis"], "quote_ids": ["lic_research", "lic_grant", "lic_aup"]},
  "C3_domain_secondary": {"status": "PASS", "basis": v1["eligibility"]["C3_domain_secondary"]["basis"], "quote_ids": ["dom_type", "arch_decoder"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": v1["eligibility"]["C4_documented_pretraining_data"]["basis"], "quote_ids": ["data_collect", "data_lvd"]},
  "eligible": v1["eligibility"]["eligible"]
 },
 "changes_vs_v1": [
  "sources re-fetched into /home fm_sources/secondary (all raw sha256 equal to v1)",
  "correction (architecture.params): v1 said 'not stated in card/paper text searched; unet ... ~1.5B params, inferred'. The paper states the UNet size: 656M new temporal parameters bringing the total to 1521M parameters. New params field quotes it; VAE parameters remain undocumented (inferred ~98M). Eligibility unaffected.",
  "added structured fields with new quotes (HF listings of both repos, model_index, frame-rate micro-conditioning, default fps in the official diffusers pipeline and Stability sampling script, base/hi-res training resolutions)",
  "no change to any eligibility status or Appendix300 answer"
 ],
 "quotes": v1q + [
  {"id": "w_vae_xt", "quote": "\"rfilename\": \"vae/diffusion_pytorch_model.safetensors\",", "source_file": APIX},
  {"id": "w_gated_xt", "quote": "\"gated\": false,", "source_file": APIX},
  {"id": "w_vae_14", "quote": "\"rfilename\": \"vae/diffusion_pytorch_model.safetensors\",", "source_file": API14},
  {"id": "w_gated_14", "quote": "\"gated\": false,", "source_file": API14},
  {"id": "dom_type", "quote": "- **Model type:** Generative image-to-video model", "source_file": R},
  {"id": "in_frames14", "quote": "This model was trained to generate 14 frames at resolution 576x1024 given a context frame of the same size.", "source_file": R14},
  {"id": "in_base_res", "quote": "After inserting temporal layers, we then train the model on LVD-F on 14 frames at resolution 256 × 384.", "source_file": P},
  {"id": "in_hires", "quote": "Next, we finetune the model to generate 14 320 × 576 frames for 100k iterations using batch size 768.", "source_file": P},
  {"id": "in_vae_sample", "quote": "\"sample_size\": 768,", "source_file": VC},
  {"id": "in_blocks", "quote": "\"down_block_types\": [ \"DownEncoderBlock2D\", \"DownEncoderBlock2D\", \"DownEncoderBlock2D\", \"DownEncoderBlock2D\" ],", "source_file": VC},
  {"id": "in_framewise", "quote": "For convenience, we additionally provide the model with the standard frame-wise decoder", "source_file": R},
  {"id": "in_fps_cond", "quote": "Additionally, we introduce micro-conditioning [64] on frame rate.", "source_file": P},
  {"id": "in_fps_cond_train", "quote": "During training, the base model and the high-resolution Text/Image-to-Video models are all conditioned on the input video’s frame rate and motion score.", "source_file": P},
  {"id": "in_fps_diffusers", "quote": "fps: int = 7,", "source_file": DF},
  {"id": "in_fps_gm", "quote": "fps_id: int = 6,", "source_file": GM},
  {"id": "in_unet_params", "quote": "inserting a total of 656M new parameters into the UNet bumping its total size (spatial and temporal layers) to 1521M parameters.", "source_file": P}
 ]
}
prev_q = {q["id"]: q for q in v1["quotes"]}
save_record(rec, prev_quotes=prev_q)
