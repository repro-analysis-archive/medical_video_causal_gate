import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, prev_candidate, term_search, MED_TERMS, A300_TERMS

API = "opensora_hpcai-tech__OpenSora-VAE-v1.2_hfapi.json"
CR = "opensora_OpenSora-VAE-v1.2_README.md"; CV = "opensora_OpenSora-VAE-v1.2_config.json"
LIC = "opensora_github_main_LICENSE.txt"; R = "opensora_github_v1.2.0_report_03.md"; D = "opensora_github_v1.2.0_datasets.md"
P1 = "opensora_arxiv_2412.20404_fulltext.txt"; VT = "opensora_github_v1.2.0_vae_temporal.py.txt"
VP = "opensora_github_v1.2.0_vae.py.txt"; INF = "opensora_github_v1.2.0_inference_sample.py.txt"
DATA_FILES = [R, D, P1]

v1 = prev_candidate("06a_opensora_vae_v1_2")
rec = {
 "id": "06a_opensora_vae_v1_2",
 "name": v1["name"],
 "version": "hpcai-tech/OpenSora-VAE-v1.2, model.safetensors (HF repo sha 33d153e9b5a9f771a8a84f98bd3f46458a8ed0bf, created 2024-06-17); released with Open-Sora v1.2 (code tag v1.2.0)",
 "paper": v1["paper"],
 "weights_location": {
  "urls": ["https://huggingface.co/hpcai-tech/OpenSora-VAE-v1.2"],
  "files_listed": {"model.safetensors": 1573430548},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; nothing downloaded",
  "note": "config pulls the 2D VAE from PixArt-alpha/pixart_sigma_sdxlvae_T5_diffusers (SDXL VAE).",
  "quote_ids": ["w_file", "w_gated", "w_release"]
 },
 "licence": {
  "id": "Apache-2.0",
  "url": "https://huggingface.co/hpcai-tech/OpenSora-VAE-v1.2 ; https://github.com/hpcaitech/Open-Sora/blob/main/LICENSE",
  "commercial": "permitted", "non_commercial_only": False,
  "restrictions": "none beyond Apache-2.0 (SDXL VAE component carries its own upstream licence, not audited here)",
  "gating": "none", "quote_ids": ["lic_card", "lic_text"]
 },
 "domain": {
  "value": "video VAE (stacked 2D SDXL VAE + causal 3D temporal VAE) of the open text-to-video model Open-Sora 1.2; trained on general stock-footage video (Pexels, Pixabay)",
  "quote_ids": ["dom_repo", "arch_4x", "data_vae"]
 },
 "architecture": {
  "type": v1["architecture"]["type"],
  "representation": v1["architecture"]["representation"]
 },
 "pretraining_data": {
  "summary": v1["pretraining_data"]["summary"],
  "form": v1["pretraining_data"]["form"]
 },
 "pretraining_data_quote": {"quote_ids": ["data_vae", "data_vae_paper", "data_open", "data_list_intro", "data_third_stage"]},
 "medical_video_in_data": {
  "answer": v1["medical_video_in_data"]["answer"],
  "basis": v1["medical_video_in_data"]["basis"],
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}
 },
 "appendix300_possible": v1["appendix300_possible"],
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "named_open_web_sources",
  "basis": "VAE video data = Pexels + Pixabay (free-licence stock-footage sites; the Open-Sora 1.2 list adds 'Mixkit, etc.'): named, but open-ended at item level, so the documentation does not allow the Appendix300 source recordings to be excluded. Timing: VAE released 2024-06-17, before the OPARA issue 2026-04-29.",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_vae", "data_third_stage"]
 },
 "input": {
  "frame_size": {"value": "VAE trained mainly at 256x256; Open-Sora 1.2 generates 144p-720p (default inference config 240p, 9:16)", "quote_ids": ["data_vae", "in_res_cfg"]},
  "frame_rate_or_sampling": {"value": "consecutive frames at the original fps (no frame skipping); training-data fps not documented; Open-Sora 1.2 default inference fps = 24, frame_interval = 1", "quote_ids": ["in_fps_report", "in_fps_cfg", "in_interval_cfg"]},
  "clip_length_frames": {"value": "17-frame micro-clips (micro_frame_size 17; longer inputs split into 17-frame clips); stage-3 training used random lengths within 34 frames", "quote_ids": ["arch_micro", "in_split17", "in_stage3"]},
  "temporal_compression": {"value": "4x (frames padded to a multiple of 4: 17 -> 5 latent frames)", "quote_ids": ["arch_4x", "in_tdown", "in_tpad"]},
  "spatial_compression": {"value": "8x8 (2D SDXL VAE, patch_size (1, 8, 8))", "quote_ids": ["arch_4x", "in_patch"]}
 },
 "embedding_dim": {
  "value": "4 latent channels x 5 x 32 x 32 = 20,480 values per 17-frame 256x256 micro-clip; generally 4 x ceil(T/4) x H/8 x W/8 per 17-frame micro-clip",
  "derivation": "latent_embed_dim=4 (VAE_Temporal_SD); 4 per-channel scale/shift entries in config.json; time padding to a multiple of 4; spatial 8x8",
  "quote_ids": ["in_tdown", "in_scale", "in_tpad", "in_patch"]
 },
 "params": {
  "value": "384M for the whole video compression network (83M 2D VAE + 300M 3D VAE); encoder-only count not documented",
  "scope": "whole autoencoder (encoder + decoder)",
  "quote_ids": ["arch_384"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs/MACs statement in the saved report, paper, card or config (searched FLOP|MAC)",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists model.safetensors, gated=False", "quote_ids": ["w_file", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "Apache-2.0", "quote_ids": ["lic_card", "lic_text"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE of an open text-to-video model trained on general (stock) video", "quote_ids": ["dom_repo", "data_vae"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": v1["eligibility"]["C4_documented_pretraining_data"]["basis"], "quote_ids": ["data_vae", "data_vae_paper", "data_list_intro"]},
  "eligible": v1["eligibility"]["eligible"]
 },
 "changes_vs_v1": [
  "sources re-fetched into /home fm_sources/secondary (raw sha256 compared with v1 per quote)",
  "added structured fields (version, weights_location, domain, pretraining_data_quote, appendix300_check, input, embedding_dim, params, flops) with new quotes from the v1.2.0 code (vae_temporal.py, vae.py) and inference config",
  "no change to any eligibility status or Appendix300 answer"
 ],
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"model.safetensors\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "w_release", "quote": "The weights are released together with Open-Sora v1.2.", "source_file": CR},
  {"id": "dom_repo", "quote": "This repository stores the weights of the VAE released by the Open-Sora team.", "source_file": CR},
  {"id": "lic_card", "quote": "license: apache-2.0", "source_file": CR},
  {"id": "lic_text", "quote": "Apache License Version 2.0, January 2004", "source_file": LIC},
  {"id": "arch_384", "quote": "For the 3D VAE, we adopt the structure of VAE in [Magvit-v2](https://magvit.cs.cmu.edu/v2/), which contains 300M parameters. Along with 83M 2D VAE, the total parameters of the video compression network is 384M.", "source_file": R},
  {"id": "arch_4x", "quote": "we propose a simple video compression network, which first compress the video in the spatial dimension by 8x8 times, then compress the video in the temporal dimension by 4x times.", "source_file": R},
  {"id": "arch_micro", "quote": "\"micro_frame_size\": 17,", "source_file": CV},
  {"id": "arch_sdxl", "quote": "We initialize the 2D VAE with [SDXL's VAE](https://huggingface.co/stabilityai/sdxl-vae), which is better than our previously used one.", "source_file": R},
  {"id": "in_scale", "quote": "\"scale\": [ 3.85, 2.32, 2.33, 3.06 ],", "source_file": CV},
  {"id": "in_tdown", "quote": "in_out_channels=4, latent_embed_dim=4, embed_dim=4, filters=128, num_res_blocks=4, channel_multipliers=(1, 2, 2, 4), temporal_downsample=(False, True, True),", "source_file": VT},
  {"id": "in_tpad", "quote": "lsize = (input_size[i] + time_padding) // self.patch_size[i]", "source_file": VT},
  {"id": "in_patch", "quote": "self.patch_size = (1, 8, 8)", "source_file": VP},
  {"id": "in_split17", "quote": "We also split the input videos input several 17 frames clips to make the inference more efficient.", "source_file": R},
  {"id": "in_stage3", "quote": "Thus, in stage 3, we use a random number within 34 frames for mixed video length training", "source_file": R},
  {"id": "in_fps_report", "quote": "With a 4 times compression in the temporal dimension, we do not need to extract frames and can generate videos with the original fps.", "source_file": R},
  {"id": "in_fps_cfg", "quote": "fps = 24", "source_file": INF},
  {"id": "in_interval_cfg", "quote": "frame_interval = 1", "source_file": INF},
  {"id": "in_res_cfg", "quote": "resolution = \"240p\"", "source_file": INF},
  {"id": "data_vae", "quote": "The training data is videos from pixels and pixabay, and the training video size is mainly 17 frames, 256x256 resolution.", "source_file": R},
  {"id": "data_vae_paper", "quote": "The 3D VAE was trained for 1.2M steps with a local batch size of 1, using videos from Pexels and Pixabay. The training data primarily consisted of 17-frame clips at a resolution of 256×256.", "source_file": P1},
  {"id": "data_open", "quote": "2.1 Data Source The dataset used is all open-sourced to make the model training fully reproducible.", "source_file": P1},
  {"id": "data_list_intro", "quote": "For Open-Sora 1.2, we conduct mixed training with both images and videos. The main datasets we use are listed below.", "source_file": D},
  {"id": "data_third_stage", "quote": "Free-license videos, sourced from Pexels, Pixabay, Mixkit, etc.", "source_file": R}
 ]
}
prev_q = {q["id"]: q for q in v1["quotes"]}
save_record(rec, prev_quotes=prev_q)
