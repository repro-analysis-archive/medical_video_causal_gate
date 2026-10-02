import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "ltx_Lightricks__LTX-Video_hfapi.json"; TREE = "ltx_Lightricks__LTX-Video_hfapi_tree_vae.json"
CARD = "ltx_LTX-Video_README.md"; VC = "ltx_LTX-Video_vae_config.json"; GH = "ltx_github_LTX-Video_README.md"
L09 = "ltx_ltx-video-2b-v0.9.license.txt"; LOW = "ltx_LTX-Video-Open-Weights-License-0.X.txt"
P = "ltx_arxiv_2501.00103_fulltext.txt"
API2 = "ltx_Lightricks__LTX-2_hfapi.json"; CARD2 = "ltx_LTX-2_README.md"; VC2 = "ltx_LTX-2_vae_config.json"
L2 = "ltx_LTX-2_LICENSE.txt"; P2 = "ltx_arxiv_2601.03233_fulltext.txt"
DATA_FILES = [P, P2, CARD, CARD2]

rec = {
 "id": "07_ltx_video_vae",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "name": "LTX-Video Video-VAE (Lightricks; AutoencoderKLLTXVideo, 32x32x8, 128 channels); family note: LTX-2 VAE",
 "version": "Lightricks/LTX-Video vae/diffusion_pytorch_model.safetensors (diffusers-format VAE committed 2024-12-11, i.e. the v0.9.0 release of 2024-11-21; HF repo sha 8984fa25007f376c1a299016d0957a37a2f797bb). Later single-file checkpoints (ltx-video-2b-v0.9.1/0.9.5, ltxv-2b/13b-0.9.6-0.9.8) embed their own VAE; v0.9.5 announces an 'Improved VAE'.",
 "family_note": "LTX-2 (Lightricks/LTX-2, arXiv 2601.03233, audio-video model, license LTX-2 Community License 2026-01-05) ships a new video VAE (AutoencoderKLLTX2Video, 128 channels, spatial 32 / temporal 8) at vae/diffusion_pytorch_model.safetensors, HF gated=False. Its training data are 'a subset of the same dataset employed in LTX-Video', i.e. equally undisclosed -> same C4 FAIL and Appendix300 UNKNOWN; licence differs (free below USD 10M annual revenue). Not recorded as a separate entry because the eligibility outcome and data documentation are identical. LTX-2 card names a newer 'Lightricks/LTX-2.3' (not audited).",
 "paper": {"title": "LTX-Video: Realtime Video Latent Diffusion", "year": 2024, "arxiv": "2501.00103", "version_read": "arXiv HTML v1 (2024-12-30)",
           "also": "LTX-2: Efficient Joint Audio-Visual Foundation Model, arXiv 2601.03233"},
 "weights_location": {
  "urls": ["https://huggingface.co/Lightricks/LTX-Video/tree/main/vae",
           "https://huggingface.co/Lightricks/LTX-2/tree/main/vae (LTX-2 VAE, family note)"],
  "files_listed": {"LTX-Video vae/diffusion_pytorch_model.safetensors": 1676798532, "LTX-Video vae/config.json": 501,
                   "LTX-2 vae/diffusion_pytorch_model.safetensors": 2444982370},
  "gated": False, "private": False,
  "verified_how": "HF API model listings (metadata only) saved as " + API + ", " + TREE + " (per-file last commit) and " + API2 + "; nothing downloaded",
  "quote_ids": ["w_file", "w_gated", "w_commit", "w_release090", "w_095vae", "w2_file", "w2_gated"]
 },
 "licence": {
  "id": "LTX Video 0.9 RAIL-M License (2024-11-22) for the v0.9 VAE in vae/ (academic or research purposes only); later versions: v0.9.5 OpenRAIL-M (commercial use), v0.9.6+ 'LTXV Open Weights License 0.X' (2025-04-15; free use, entities with >= USD 10M annual revenue may obtain a paid commercial licence); LTX-2: LTX-2 Community License (2026-01-05; entities with >= USD 10M revenue must obtain a paid commercial licence)",
  "url": "https://huggingface.co/Lightricks/LTX-Video/blob/main/ltx-video-2b-v0.9.license.txt ; https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt ; https://github.com/Lightricks/LTX-2/blob/main/LICENSE",
  "commercial": "v0.9 VAE: not permitted (research/academic only); 0.9.5+: permitted with revenue-threshold terms",
  "non_commercial_only": True,
  "restrictions": "RAIL-style use restrictions (Attachment A), including a ban on providing medical advice and medical results interpretation (0.X and LTX-2 licences); v0.9 licence: Permitted Purpose = academic or research only",
  "gating": "none (HF gated=False)",
  "quote_ids": ["lic_card_list", "lic_rail_title", "lic_permitted", "lic_grant", "lic_ow_title", "lic_ow_revenue", "lic_ow_medical", "lic2_title", "lic2_revenue"]
 },
 "domain": {
  "value": "Video-VAE (causal 3D conv encoder, denoising decoder) of the LTX-Video DiT text/image-to-video diffusion model; trained on a large-scale general video dataset (undisclosed)",
  "quote_ids": ["dom_card", "dom_trained", "arch_1192", "arch_first_frame"]
 },
 "architecture": {
  "type": "3D causal convolutional VAE with patchify (4x4) at the VAE input, KL latent, timestep-conditioned denoising decoder; compression 32x32x8 with 128 latent channels (1:192)",
  "representation": "encoder latents: 128 channels per latent voxel, each voxel = 8 frames x 32 x 32 pixels (first frame encoded as its own latent frame)"
 },
 "pretraining_data": {
  "summary": "Paper: 'publicly available data, supplemented with licensed material', filtered by an internal aesthetic model, motion filter, black-bar cropping, internal re-captioning; no datasets or providers named. LTX-2 uses a subset of the same dataset.",
  "form": "described only"
 },
 "pretraining_data_quote": {"quote_ids": ["data_main", "data_blackbars", "data_ltx2"]},
 "medical_video_in_data": {
  "answer": "NOT MENTIONED",
  "basis": "Automated search of the saved LTX-Video and LTX-2 paper texts and both model cards for medical|surgical|surgery|endoscop|laparoscop|clinical|health|hospital: no hits. (The 0.X / LTX-2 licences prohibit giving medical advice; that is a use restriction, not a data statement.)",
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}
 },
 "appendix300_possible": {
  "answer": "UNKNOWN", "basis_class": "undisclosed",
  "basis": "training data = undisclosed 'publicly available data, supplemented with licensed material'. Timing: v0.9 released 2024-11-21 (paper 2024-12-30), LTX-2 2026-01, both before the OPARA issue 2026-04-29; prior circulation of the source recordings is not documented.",
  "quote_ids": ["data_main"]
 },
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "undisclosed",
  "basis": "no data list exists: the sources are characterised only as 'publicly available data, supplemented with licensed material', so the Appendix300 source recordings cannot be excluded.",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_main", "data_ltx2"]
 },
 "input": {
  "frame_size": {"value": "any resolution divisible by 32 (padded otherwise); works best under 720x1280; paper reference 768x512; card headline 1216x704", "quote_ids": ["in_tips", "in_best", "in_24fps", "dom_card"]},
  "frame_rate_or_sampling": {"value": "generates 24 fps (paper) / 30 fps (card); original FPS is fed to the temporal RoPE embedding; VAE itself has no fps parameter (consecutive frames)", "quote_ids": ["in_24fps", "dom_card", "in_fps_rope"]},
  "clip_length_frames": {"value": "8k+1 frames (e.g. 121, 257); works best below 257 frames; paper reference 121 frames", "quote_ids": ["in_tips", "in_best", "in_121"]},
  "temporal_compression": {"value": "8x (first frame encoded separately: T -> 1 + (T-1)/8)", "quote_ids": ["arch_1192", "arch_first_frame"]},
  "spatial_compression": {"value": "32x32 (patch_size 4 x three 2x spatio-temporal downsamplings)", "quote_ids": ["arch_1192", "arch_patch", "arch_scaling"]}
 },
 "embedding_dim": {
  "value": "128 latent channels x 16 x 16 x 24 = 786,432 values for a 121-frame 768x512 clip; generally 128 x (1+(T-1)/8) x H/32 x W/32",
  "derivation": "latent_channels 128; 32x32x8 compression with the first frame as its own latent frame; reference input from the paper (121 frames at 768x512)",
  "quote_ids": ["arch_latent", "arch_1192", "arch_first_frame", "in_121"]
 },
 "params": {
  "value": "not documented for the VAE (paper: transformer 1.9B 'Base model size'; VAE size not stated). Inferred only: vae safetensors 1,676,798,532 bytes ~ 419M parameters if fp32 (encoder + decoder; dtype not stated)",
  "scope": "not documented",
  "quote_ids": ["w_file"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs/MACs statement in the saved LTX-Video / LTX-2 paper texts, card or config (searched FLOP|MAC; only reference titles hit)",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists vae/diffusion_pytorch_model.safetensors, gated=False (also for LTX-2)", "quote_ids": ["w_file", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "v0.9 RAIL-M licence grants use for the Permitted Purpose = academic or research (non-commercial restriction recorded); later licences allow use for any purpose subject to Attachment A restrictions", "quote_ids": ["lic_permitted", "lic_grant", "lic_ow_revenue"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE of a text/image-to-video diffusion model trained on general video", "quote_ids": ["dom_card", "dom_trained"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": "video data described only as 'publicly available data, supplemented with licensed material'; no datasets or named sources (LTX-2: subset of the same data)", "quote_ids": ["data_main", "data_ltx2"]},
  "eligible": "NO (fails C4)"
 },
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"vae/diffusion_pytorch_model.safetensors\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "w_commit", "quote": "\"path\": \"vae/diffusion_pytorch_model.safetensors\", \"lastCommit\": { \"id\": \"05be24f065a268e3b7881b63a114dbf52ce68fd1\", \"title\": \"Diffusers weights test (#32)\", \"date\": \"2024-12-11T09:21:08.000Z\" },", "source_file": TREE},
  {"id": "w_release090", "quote": "## November 21th, 2024: Initial release v0.9.0", "source_file": GH},
  {"id": "w_095vae", "quote": "- Release a new checkpoint v0.9.5 with improved quality - Support keyframes and video extension - Support higher resolutions - Improved prompt understanding - Improved VAE", "source_file": GH},
  {"id": "w2_file", "quote": "\"rfilename\": \"vae/diffusion_pytorch_model.safetensors\",", "source_file": API2},
  {"id": "w2_gated", "quote": "\"gated\": false,", "source_file": API2},
  {"id": "lic_card_list", "quote": "- 2B version 0.9: [license](https://huggingface.co/Lightricks/LTX-Video/blob/main/ltx-video-2b-v0.9.license.txt)", "source_file": CARD},
  {"id": "lic_rail_title", "quote": "LTX Video 0.9 (“LTXV”) By Lightricks Ltd. (“Lightricks”) RAIL-M License dated November 22, 2024", "source_file": L09},
  {"id": "lic_permitted", "quote": "“Permitted Purpose” means for academic or research purposes only, and explicitly excludes commercialization such as downstream selling of the Model or Derivatives of the Model.", "source_file": L09},
  {"id": "lic_grant", "quote": "each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare, publicly display, publicly perform, sublicense, and distribute the Model and Derivatives of the Model, only for the Permitted Purpose.", "source_file": L09},
  {"id": "lic_ow_title", "quote": "LTXV Open Weights License 0.X License date: April 15, 2025 (This license is applicable to all LTXV model versions released since April 15, 2025 (v0.9.6))", "source_file": LOW},
  {"id": "lic_ow_revenue", "quote": "provided however, that entities with annual revenues of at least $10,000,000 (the \"Commercial Entities\") are eligible to obtain a paid commercial use license", "source_file": LOW},
  {"id": "lic_ow_medical", "quote": "To provide medical advice and medical results interpretation;", "source_file": LOW},
  {"id": "lic2_title", "quote": "LTX-2 Community License Agreement License date: January 5, 2026", "source_file": L2},
  {"id": "lic2_revenue", "quote": "that Entities with annual revenues of at least $10,000,000 (the \"Commercial Entities\") are required to obtain a paid commercial use license in order to use LTX-2 and Derivatives of LTX-2", "source_file": L2},
  {"id": "dom_card", "quote": "LTX-Video is the first DiT-based video generation model capable of generating high-quality videos in real-time. It produces 30 FPS videos at a 1216×704 resolution faster than they can be watched.", "source_file": CARD},
  {"id": "dom_trained", "quote": "Trained on a large-scale dataset of diverse videos, the model generates high-resolution videos with realistic and varied content.", "source_file": CARD},
  {"id": "arch_vae_class", "quote": "\"_class_name\": \"AutoencoderKLLTXVideo\",", "source_file": VC},
  {"id": "arch_latent", "quote": "\"latent_channels\": 128,", "source_file": VC},
  {"id": "arch_patch", "quote": "\"patch_size\": 4, \"patch_size_t\": 1,", "source_file": VC},
  {"id": "arch_enc_causal", "quote": "\"encoder_causal\": true,", "source_file": VC},
  {"id": "arch_scaling", "quote": "\"spatio_temporal_scaling\": [ true, true, true, false ]", "source_file": VC},
  {"id": "arch_1192", "quote": "our Video-VAE applies a spatio-temporal compression of 32 × 32 × 8 32\\times 32\\times 8 with 128 channels, resulting in a total compression of 1:192", "source_file": P},
  {"id": "arch_first_frame", "quote": "Causal Encoder utilizing 3D Causal Convolutions, applying 32 × 32 × 8 32\\times 32\\times 8 compression (except the first frame, which is encoded as a separate latent frame).", "source_file": P},
  {"id": "arch2_class", "quote": "\"_class_name\": \"AutoencoderKLLTX2Video\",", "source_file": VC2},
  {"id": "arch2_ratios", "quote": "\"spatial_compression_ratio\": 32,", "source_file": VC2},
  {"id": "arch2_tratio", "quote": "\"temporal_compression_ratio\": 8,", "source_file": VC2},
  {"id": "arch2_latent", "quote": "\"latent_channels\": 128,", "source_file": VC2},
  {"id": "dom2_card", "quote": "LTX-2 is a DiT-based audio-video foundation model designed to generate synchronized video and audio within a single model.", "source_file": CARD2},
  {"id": "in_tips", "quote": "The model works on resolutions that are divisible by 32 and number of frames that are divisible by 8 + 1 (e.g. 257).", "source_file": CARD},
  {"id": "in_best", "quote": "The model works best on resolutions under 720 x 1280 and number of frames below 257.", "source_file": CARD},
  {"id": "in_24fps", "quote": "producing 5 seconds of 24 fps video at 768×512 resolution in just 2 seconds on an Nvidia H100 GPU", "source_file": P},
  {"id": "in_121", "quote": "2 seconds to generate 121 frames at 768 × 512 768\\times 512 pixels and 20 diffusion steps on an Nvidia H100 GPU", "source_file": P},
  {"id": "in_fps_rope", "quote": "Incorporating the original FPS into the temporal embedding allows the model to generate more natural-looking motion.", "source_file": P},
  {"id": "data_main", "quote": "3 Data Preparation Our training dataset comprises a robust collection of publicly available data, supplemented with licensed material, ensuring a diverse and comprehensive training environment and enabling our model to generate a wide variety of visual content.", "source_file": P},
  {"id": "data_blackbars", "quote": "Videos are also processed to crop out any black bars, thus standardizing the aspect ratios and enhancing the usable visual data.", "source_file": P},
  {"id": "data_ltx2", "quote": "5 Training Data We used a subset of the same dataset employed in LTX-Video [ 11 ] , focusing on video clips that contained significant and informative audio components.", "source_file": P2}
 ]
}
save_record(rec)
