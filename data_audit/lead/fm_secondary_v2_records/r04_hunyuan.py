import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, prev_candidate, term_search, MED_TERMS, A300_TERMS

API = "hunyuan_tencent__HunyuanVideo_hfapi.json"
LIC = "hunyuan_LICENSE.txt"; RD = "hunyuan_README.md"; CV = "hunyuan_hunyuan-video-t2v-720p_vae_config.json"
P = "hunyuan_arxiv_2412.03603_fulltext.txt"; SV = "hunyuan_github_main_sample_video.py.txt"
DATA_FILES = [P, RD]

v1 = prev_candidate("04_hunyuanvideo_vae")
rec = {
 "id": "04_hunyuanvideo_vae",
 "name": v1["name"],
 "version": "tencent/HunyuanVideo, hunyuan-video-t2v-720p/vae/pytorch_model.pt + vae/config.json (HF repo sha 6204ad6aea1a77ff5aba337c88278bb9500eb37d, repo created 2024-12-01, last modified 2025-03-06); VAE id in the official code: '884-16c-hy'",
 "paper": v1["paper"],
 "weights_location": {
  "urls": ["https://huggingface.co/tencent/HunyuanVideo/tree/main/hunyuan-video-t2v-720p/vae"],
  "files_listed": {"hunyuan-video-t2v-720p/vae/pytorch_model.pt": 986000558, "hunyuan-video-t2v-720p/vae/config.json": 785},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; nothing downloaded",
  "quote_ids": ["w_file", "w_gated"]
 },
 "licence": {
  "id": v1["licence"]["id"], "url": v1["licence"]["url"],
  "commercial": v1["licence"]["commercial"], "non_commercial_only": v1["licence"]["non_commercial_only"],
  "restrictions": v1["licence"]["restrictions"], "gating": v1["licence"]["gating"],
  "quote_ids": ["lic_card", "lic_territory", "lic_grant", "lic_outside", "lic_mau", "lic_aup_med"]
 },
 "domain": {
  "value": "causal 3D video VAE of the HunyuanVideo text-to-video diffusion model, trained from scratch on video:image 4:1 from an internal general-domain data pool (people, animals, plants, landscapes, vehicles, objects, buildings, animation)",
  "quote_ids": ["arch_card", "arch_scratch", "data_pool"]
 },
 "architecture": {"type": v1["architecture"]["type"], "representation": v1["architecture"]["representation"]},
 "pretraining_data": {"summary": v1["pretraining_data"]["summary"], "form": v1["pretraining_data"]["form"]},
 "pretraining_data_quote": {"quote_ids": ["data_pool", "data_sources", "data_gdpr", "arch_scratch"]},
 "medical_video_in_data": {
  "answer": v1["medical_video_in_data"]["answer"],
  "basis": v1["medical_video_in_data"]["basis"],
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}
 },
 "appendix300_possible": v1["appendix300_possible"],
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "undisclosed",
  "basis": "the raw data pool is described only by content domains ('raw data from different sources'); no datasets or providers are named, so the documentation does not allow the Appendix300 source recordings to be excluded. Timing: paper v1 2024-12-03, weights 2024-12, before the OPARA issue 2026-04-29.",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_pool", "data_sources"]
 },
 "input": {
  "frame_size": {"value": "generation default 720x1280 (also 544x960); VAE trained by a curriculum from low-resolution short to high-resolution long video; spatial-temporal tiling encodes arbitrary resolutions", "quote_ids": ["in_size", "arch_res", "in_curriculum", "in_tiling"]},
  "frame_rate_or_sampling": {"value": "VAE training: frames sampled evenly with a random sampling interval of 1-8; the DiT is trained at the original frame rate; official sampling script saves at 24 fps", "quote_ids": ["in_interval", "in_orig_fps", "in_fps_save"]},
  "clip_length_frames": {"value": "causal (T+1)-frame input; generation default 129 frames (= 1 + 4x32); tiling allows arbitrary durations", "quote_ids": ["in_shape_in", "in_len", "in_tiling"]},
  "temporal_compression": {"value": "4x (latent frames T/4 + 1)", "quote_ids": ["arch_card", "arch_tcomp", "in_shape_out"]},
  "spatial_compression": {"value": "8x8", "quote_ids": ["arch_card", "in_shape_out"]}
 },
 "embedding_dim": {
  "value": "16 latent channels x 33 x 90 x 160 = 7,603,200 values for a 129-frame 720x1280 clip; generally 16 x (T/4 + 1) x H/8 x W/8 for a (T+1)-frame clip",
  "derivation": "latent_channels 16 (config; card 'channel ... 16'); shape (T/c_t + 1) x C x H/c_s x W/c_s with c_t 4, c_s 8 (paper)",
  "quote_ids": ["arch_latent", "arch_card", "in_shape_in", "in_shape_out"]
 },
 "params": {
  "value": "not documented in the saved card, config, paper or code; (inferred, not documentation: pytorch_model.pt 986,000,558 bytes ~ 246M params if fp32)",
  "scope": "not documented",
  "quote_ids": ["w_file"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "the paper's only FLOPs statement concerns DiT scaling-law compute ('C has a unit of Peta FLOPs'); no VAE FLOPs per input documented",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": v1["eligibility"]["C1_open_weights"]["basis"], "quote_ids": ["w_file", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": v1["eligibility"]["C2_licence_research_use"]["basis"], "quote_ids": ["lic_territory", "lic_grant", "lic_outside"]},
  "C3_domain_secondary": {"status": "PASS", "basis": v1["eligibility"]["C3_domain_secondary"]["basis"], "quote_ids": ["arch_card", "data_pool"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": v1["eligibility"]["C4_documented_pretraining_data"]["basis"], "quote_ids": ["data_pool", "data_sources"]},
  "eligible": v1["eligibility"]["eligible"]
 },
 "changes_vs_v1": [
  "sources re-fetched into /home fm_sources/secondary (raw sha256 compared with v1 per quote)",
  "added structured fields (version, weights_location, domain, pretraining_data_quote, appendix300_check, input, embedding_dim, params, flops) with new quotes from the card, VAE config, paper sec. 4.1 and the official sample_video.py",
  "no change to any eligibility status or Appendix300 answer"
 ],
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"hunyuan-video-t2v-720p/vae/pytorch_model.pt\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "lic_card", "quote": "license_name: tencent-hunyuan-community", "source_file": RD},
  {"id": "lic_territory", "quote": "THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA AND IS EXPRESSLY LIMITED TO THE TERRITORY, AS DEFINED BELOW.", "source_file": LIC},
  {"id": "lic_grant", "quote": "We grant You, for the Territory only, a non-exclusive, non-transferable and royalty-free limited license under Tencent’s intellectual property or other rights owned by Us embodied in or utilized by the Materials to use, reproduce, distribute, create derivative works of (including Model Derivatives), and make modifications to the Materials, only in accordance with the terms of this Agreement and the Acceptable Use Policy", "source_file": LIC},
  {"id": "lic_outside", "quote": "You must not use, reproduce, modify, distribute, or display the Tencent Hunyuan Works, Output or results of the Tencent Hunyuan Works outside the Territory.", "source_file": LIC},
  {"id": "lic_mau", "quote": "greater than 100 million monthly active users in the preceding calendar month, You must request a license from Tencent", "source_file": LIC},
  {"id": "lic_aup_med", "quote": "To make high-stakes automated decisions in domains that affect an individual’s safety, rights or wellbeing (e.g., law enforcement, migration, medicine/health, management of critical infrastructure, safety components of products, essential services, credit, employment, housing, education, social scoring, or insurance);", "source_file": LIC},
  {"id": "arch_card", "quote": "HunyuanVideo trains a 3D VAE with CausalConv3D to compress pixel-space videos and images into a compact latent space. We set the compression ratios of video length, space, and channel to 4, 8, and 16 respectively.", "source_file": RD},
  {"id": "arch_vae_class", "quote": "\"_class_name\": \"AutoencoderKLCausal3D\",", "source_file": CV},
  {"id": "arch_tcomp", "quote": "\"time_compression_ratio\": 4,", "source_file": CV},
  {"id": "arch_latent", "quote": "\"latent_channels\": 16,", "source_file": CV},
  {"id": "arch_res", "quote": "* **Minimum**: The minimum GPU memory required is 60GB for 720px1280px129f and 45G for 544px960px129f.", "source_file": RD},
  {"id": "arch_scratch", "quote": "we do not rely on a pre-trained image VAE for parameter initialization; instead, we train our model from scratch. To balance the reconstruction quality of videos and images, we mix video and image data at a ratio of 4 : 1", "source_file": P},
  {"id": "in_shape_in", "quote": "For a video of shape ( T + 1 ) × 3 × H × W", "source_file": P},
  {"id": "in_shape_out", "quote": "our 3DVAE compresses it into latent features with shape ( T c t + 1 ) × C × ( H c s ) × ( W c s )", "source_file": P},
  {"id": "in_curriculum", "quote": "we employ a curriculum learning strategy, gradually training from low-resolution short video to high-resolution long video.", "source_file": P},
  {"id": "in_interval", "quote": "we randomly choose a sampling interval from the range 1 ∼ 8", "source_file": P},
  {"id": "in_tiling", "quote": "This tiling strategy allows us to encode/decode videos in arbitrary resolutions and durations on a single GPU.", "source_file": P},
  {"id": "in_orig_fps", "quote": "allowing us to train videos at the original resolution and frame rate.", "source_file": RD},
  {"id": "in_size", "quote": "| `--video-size` | 720 1280 | The size of the generated video |", "source_file": RD},
  {"id": "in_len", "quote": "| `--video-length` | 129 | The length of the generated video |", "source_file": RD},
  {"id": "in_fps_save", "quote": "save_videos_grid(sample, cur_save_path, fps=24)", "source_file": SV},
  {"id": "data_pool", "quote": "Our raw data pool initially comprised videos spanning a wide range of domains including people, animals, plants, landscapes, vehicles, objects, buildings, and animation.", "source_file": P},
  {"id": "data_sources", "quote": "Our raw data from different sources exhibits varying durations and levels of quality.", "source_file": P},
  {"id": "data_gdpr", "quote": "Our data acquisition process is rigorously governed by the principles outlined in the General Data Protection Regulation (GDPR) [ 39 ] framework.", "source_file": P}
 ]
}
prev_q = {q["id"]: q for q in v1["quotes"]}
save_record(rec, prev_quotes=prev_q)
