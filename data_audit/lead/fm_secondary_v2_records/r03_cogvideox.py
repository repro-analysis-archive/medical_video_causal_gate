import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, prev_candidate, term_search, MED_TERMS, A300_TERMS

API2 = "cogvideox_zai-org__CogVideoX-2b_hfapi.json"; API5 = "cogvideox_zai-org__CogVideoX-5b_hfapi.json"
R = "cogvideox_CogVideoX-2b_README.md"; LIC2 = "cogvideox_CogVideoX-2b_LICENSE.txt"; LIC5 = "cogvideox_CogVideoX-5b_LICENSE.txt"
VC = "cogvideox_CogVideoX-2b_vae_config.json"; TC = "cogvideox_CogVideoX-2b_transformer_config.json"
P = "cogvideox_arxiv_2408.06072_fulltext.txt"; PIPE = "cogvideox_diffusers_v0.30.0_pipeline_cogvideox.py.txt"
COS = "cosmos_Cosmos-Tokenize1-CV8x8x8-720p_README.md"
DATA_FILES = [P, R]
FMAP = {"cogvideox_CogVideoX-5b_LICENSE": LIC5, "cogvideox_arxiv_2408.06072_fulltext.html": P}

v1 = prev_candidate("03_cogvideox_vae")
v1q = [{"id": q["id"], "quote": q["quote"], "source_file": FMAP.get(q["source_file"], q["source_file"])} for q in v1["quotes"]]

rec = {
 "id": "03_cogvideox_vae",
 "name": v1["name"],
 "version": "zai-org/CogVideoX-2b vae/diffusion_pytorch_model.safetensors (HF repo sha 1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01, created 2024-08-05, last modified 2024-11-23); the CogVideoX-5b repo (sha 8fc5b281006c82b82d34fd2543d2f0ebb4e7e321) lists the same VAE file (identical LFS sha256 a410e48d...995e; vae config differs only in scaling_factor 1.15258426 vs 0.7)",
 "paper": v1["paper"],
 "weights_location": {
  "urls": v1["weights"]["urls"],
  "files_listed": v1["weights"]["files_listed"],
  "vae_lfs_sha256_both_repos": "a410e48d988c8224cef392b68db0654485cfd41f345f4a3a81d3e6b765bb995e",
  "gated": False, "private": False,
  "verified_how": "HF API model listings (metadata only) saved as " + API2 + ", " + API5 + "; nothing downloaded",
  "note": v1["weights"]["note"],
  "quote_ids": ["w_vae2", "w_lfs2", "w_gated2", "w_lfs5", "w_gated5"]
 },
 "licence": {
  "id": v1["licence"]["id"], "url": v1["licence"]["url"], "commercial": v1["licence"]["commercial"],
  "non_commercial_only": False, "restrictions": v1["licence"]["restrictions"], "gating": v1["licence"]["gating"],
  "quote_ids": ["lic_2b", "lic_2b_text", "lic_5b_research", "lic_5b_restr"]
 },
 "domain": {
  "value": "3D causal video VAE of the CogVideoX text-to-video diffusion transformer; trained on general video (~35M filtered clips) with image data from LAION-5B / COYO-700M for the generative model",
  "quote_ids": ["arch_8x8x4", "arch_vae_class", "data_main"]
 },
 "architecture": {"type": v1["architecture"]["type"], "representation": v1["architecture"]["representation"]},
 "pretraining_data": {"summary": v1["pretraining_data"]["summary"], "form": v1["pretraining_data"]["form"]},
 "pretraining_data_quote": {"quote_ids": ["data_main", "arch_vae_train", "in_vae_fps"]},
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
  "quote_ids": ["data_main"]
 },
 "input": {
  "frame_size": {"value": "720x480 for CogVideoX-2b/5b generation (vae config sample 480x720); VAE trained at 256x256 and encodes larger frames without retraining", "quote_ids": ["arch_res", "in_sample_hw", "arch_vae_train"]},
  "frame_rate_or_sampling": {"value": "VAE training: fps randomly 8 or 16; CogVideoX-2b/5b generation at 8 fps (49 frames = 6 s)", "quote_ids": ["in_vae_fps", "in_fps_card", "in_len_card"]},
  "clip_length_frames": {"value": "49 frames for CogVideoX-2b/5b; VAE trained on 17-frame clips then finetuned on 161-frame videos (context parallel); causal, latent frames = (T-1)/4 + 1", "quote_ids": ["in_frames_card", "in_sample_frames", "arch_vae_train", "in_vae_161"]},
  "temporal_compression": {"value": "4x (causal; 49 frames -> 13 latent frames)", "quote_ids": ["arch_tcomp", "arch_8x8x4", "in_latent_t"]},
  "spatial_compression": {"value": "8x8", "quote_ids": ["arch_8x8x4", "in_latent_hw"]}
 },
 "embedding_dim": {
  "value": "49 frames x 480x720: 16 channels x 13 x 60 x 90 = 1,123,200 values; generally 16 x ((T-1)/4 + 1) x H/8 x W/8",
  "derivation": "latent_channels 16; latent frames (num_frames - 1) // 4 + 1 (diffusers pipeline); transformer config sample_height 60 / sample_width 90 latent grid for 480x720",
  "quote_ids": ["arch_latent", "in_latent_t", "in_latent_hw", "in_sample_frames"]
 },
 "params": {
  "value": "216M for the CogVideoX 4x8x8 tokenizer (whole VAE), documented only by NVIDIA's Cosmos card / paper runtime table (third-party); not stated by the CogVideoX authors. Encoder-only count not documented (vae fp32 file 862 MB is consistent with ~216M).",
  "scope": "whole VAE (encoder + decoder), third-party documentation",
  "quote_ids": ["arch_params"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs/MACs in the saved CogVideoX paper, card or configs. Third-party runtime proxy (Cosmos card): 414 ms per video frame for the CogVideoX 4x8x8 tokenizer at 720x1280 on one A100-80GB (encode+decode).",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": v1["eligibility"]["C1_open_weights"]["basis"], "quote_ids": ["w_vae2", "w_gated2"]},
  "C2_licence_research_use": {"status": "PASS", "basis": v1["eligibility"]["C2_licence_research_use"]["basis"], "quote_ids": ["lic_2b", "lic_5b_research"]},
  "C3_domain_secondary": {"status": "PASS", "basis": v1["eligibility"]["C3_domain_secondary"]["basis"], "quote_ids": ["arch_8x8x4", "data_main"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": v1["eligibility"]["C4_documented_pretraining_data"]["basis"], "quote_ids": ["data_main"]},
  "eligible": v1["eligibility"]["eligible"]
 },
 "changes_vs_v1": [
  "sources re-fetched into /home fm_sources/secondary (all raw sha256 equal to v1); added the CogVideoX-2b Apache-2.0 LICENSE text, CogVideoX-5b vae config, 2b transformer config and the diffusers v0.30.0 pipeline code",
  "clarification (architecture.frames_per_clip): v1 said 'VAE first trained on 17 frames'; the paper adds that the VAE is then finetuned by context parallel on 161-frame videos and that VAE training randomly selects 8 or 16 fps. Recorded in input fields; eligibility unaffected.",
  "clarification (params): the 216M figure is third-party (NVIDIA Cosmos card/paper), not a CogVideoX-authored statement; v1 already cited the Cosmos card, now stated explicitly",
  "added: the VAE file is byte-identical (same LFS sha256) in the 2b and 5b repos, so the Apache-2.0 2B licence statement covers the same weights",
  "no change to any eligibility status or Appendix300 answer"
 ],
 "quotes": v1q + [
  {"id": "w_vae2", "quote": "\"rfilename\": \"vae/diffusion_pytorch_model.safetensors\",", "source_file": API2},
  {"id": "w_lfs2", "quote": "\"sha256\": \"a410e48d988c8224cef392b68db0654485cfd41f345f4a3a81d3e6b765bb995e\",", "source_file": API2},
  {"id": "w_gated2", "quote": "\"gated\": false,", "source_file": API2},
  {"id": "w_lfs5", "quote": "\"sha256\": \"a410e48d988c8224cef392b68db0654485cfd41f345f4a3a81d3e6b765bb995e\",", "source_file": API5},
  {"id": "w_gated5", "quote": "\"gated\": false,", "source_file": API5},
  {"id": "lic_2b_text", "quote": "Apache License", "source_file": LIC2},
  {"id": "in_sample_hw", "quote": "\"sample_height\": 480, \"sample_width\": 720,", "source_file": VC},
  {"id": "in_vae_fps", "quote": "Randomly select 8 or 16 fps to enhance the model’s robustness.", "source_file": P},
  {"id": "in_vae_161", "quote": "Therefore, we conduct a two-stage training by first training on 17-frame videos and finetuning by context parallel on 161-frame videos.", "source_file": P},
  {"id": "in_fps_card", "quote": "<td style=\"text-align: center;\">Frame Rate</td> <td colspan=\"2\" style=\"text-align: center;\">8 Frames per Second</td>", "source_file": R},
  {"id": "in_len_card", "quote": "<td style=\"text-align: center;\">Video Length</td> <td colspan=\"2\" style=\"text-align: center;\">6 Seconds</td>", "source_file": R},
  {"id": "in_frames_card", "quote": "num_frames=49,", "source_file": R},
  {"id": "in_sample_frames", "quote": "\"sample_frames\": 49, \"sample_height\": 60, \"sample_width\": 90,", "source_file": TC},
  {"id": "in_latent_t", "quote": "(num_frames - 1) // self.vae_scale_factor_temporal + 1,", "source_file": PIPE},
  {"id": "in_latent_hw", "quote": "height // self.vae_scale_factor_spatial, width // self.vae_scale_factor_spatial,", "source_file": PIPE}
 ]
}
prev_q = {q["id"]: q for q in v1["quotes"]}
save_record(rec, prev_quotes=prev_q)
