import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API12 = "osplan_LanguageBind__Open-Sora-Plan-v1.2.0_hfapi.json"; API13 = "osplan_LanguageBind__Open-Sora-Plan-v1.3.0_hfapi.json"
APIWF = "osplan_chestnutlzj__WF-VAE-L-16Chn_hfapi.json"
R11 = "osplan_github_Report-v1.1.0.md"; R12 = "osplan_github_Report-v1.2.0.md"; R13 = "osplan_github_Report-v1.3.0.md"
LIC = "osplan_github_LICENSE.txt"; HF12 = "osplan_hf_v1.2.0_README.md"; C12 = "osplan_hf_v1.2.0_vae_config.json"
C13 = "osplan_hf_v1.3.0_vae_config.json"; HFWF = "osplan_hf_WF-VAE-L-16Chn_README.md"; CWF = "osplan_hf_WF-VAE-L-16Chn_config.json"
WRM = "wfvae_github_README.md"; WLIC = "wfvae_github_LICENSE.txt"; WP = "wfvae_arxiv_2411.17459_fulltext.txt"
ZW = "​"

# ---------------------------------------------------------------- 19a Open-Sora-Plan v1.2.0 CausalVideoVAE (OD-VAE)
DATA_A = [R12, R11]
recA = {
 "id": "19a_opensora_plan_v1_2_causalvideovae",
 "name": "Open-Sora-Plan v1.2.0 CausalVideoVAE (a.k.a. OD-VAE; LanguageBind/Open-Sora-Plan-v1.2.0 vae/checkpoint.ckpt, CausalVAEModel)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "LanguageBind/Open-Sora-Plan-v1.2.0, vae/checkpoint.ckpt + vae/config.json (HF repo created 2024-07-24); technical report docs/Report-v1.2.0.md. Other releases not recorded here: v1.1.0 vae (diffusion_pytorch_model.safetensors), v1.3.0 vae = 8-channel WF-VAE-S distilled from OD-VAE (see 19b)",
 "paper": {"title": "Open-Sora Plan technical report v1.2.0 (GitHub docs/Report-v1.2.0.md); Open-Sora Plan: Open-Source Large Video Generation Model (arXiv:2412.00131) not fetched", "year": 2024},
 "weights_location": {
  "urls": ["https://huggingface.co/LanguageBind/Open-Sora-Plan-v1.2.0/tree/main/vae"],
  "files_listed": {"vae/checkpoint.ckpt": 956837970, "vae/config.json": 1673},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API12 + "; nothing downloaded",
  "quote_ids": ["w_file", "w_gated", "w_report_model"]
 },
 "licence": {
  "id": "MIT (HF card license: mit; GitHub LICENSE MIT)",
  "url": "https://huggingface.co/LanguageBind/Open-Sora-Plan-v1.2.0 ; https://github.com/PKU-YuanGroup/Open-Sora-Plan/blob/main/LICENSE",
  "commercial": "permitted", "non_commercial_only": False,
  "restrictions": "none beyond MIT (initialised from the SD2.1 VAE, whose upstream licence is not audited here)",
  "gating": "none", "quote_ids": ["lic_card", "lic_text"]
 },
 "domain": {"value": "3D causal video VAE of the open text-to-video model Open-Sora Plan v1.2; trained on general video (Kinetics-400, then stock footage collected in v1.1.0)", "quote_ids": ["dom_vae", "data_train"]},
 "architecture": {"type": "causal 3D convolutional KL-VAE (CausalVAEModel) inflated from the SD2.1 image VAE ('tail initialization'); 2D ResNet blocks in the first encoder stages, 3D in the later ones",
                  "representation": "encoder latents, 4 channels (z_channels 4), 4x temporal x 8x8 spatial compression"},
 "pretraining_data": {
  "summary": "Stage 1: Kinetics-400 (200k steps); stage 2: 'high-quality data (collected in v1.1.0)' (450k steps) = the Open-Sora-Plan v1.1.0 video set of ~3k hours from Mixkit, Pixabay and Pexels; all on 25-frame 256x256 clips. Initialised from the SD2.1 image VAE (image data not documented here).",
  "form": "dataset/source list (named: Kinetics-400 + Mixkit/Pixabay/Pexels)"
 },
 "pretraining_data_quote": {"quote_ids": ["data_train", "data_table", "data_v11_hours", "data_mixkit", "data_pixabay", "data_pexel", "data_init"]},
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "named sources include open-ended stock-footage sites (Mixkit, Pixabay, Pexels); term search of the v1.2.0 and v1.1.0 reports finds no medical/surgical data statement",
                           "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_A, MED_TERMS)}},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "named_open_web_sources",
  "basis": "stage-2 data = videos from Mixkit, Pixabay, Pexels (named but open-ended stock-footage sites), so the documentation does not allow the Appendix300 source recordings to be excluded; stage-1 Kinetics-400 alone would be NO. Timing: released 2024-07, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_train", "data_pexel"]},
 "appendix300_check": {
  "answer": "UNKNOWN", "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "named_open_web_sources",
  "basis": "Kinetics-400 (closed) + Mixkit/Pixabay/Pexels stock footage (named, open-ended)",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_A, A300_TERMS)},
  "quote_ids": ["data_train", "data_mixkit", "data_pixabay", "data_pexel"]
 },
 "input": {
  "frame_size": {"value": "trained on 256x256 (config resolution 256); Open-Sora Plan v1.2 generates up to 93x1280x720", "quote_ids": ["data_train", "in_res", "in_gen"]},
  "frame_rate_or_sampling": {"value": "not documented for the VAE in the saved sources", "quote_ids": []},
  "clip_length_frames": {"value": "25-frame training clips (causal: 1 + 4k frames)", "quote_ids": ["data_train"]},
  "temporal_compression": {"value": "4x (two Spatial2xTime2x3DDownsample stages)", "quote_ids": ["in_cr", "in_down"]},
  "spatial_compression": {"value": "8x8", "quote_ids": ["in_cr", "in_down"]}
 },
 "embedding_dim": {"value": "4 latent channels x (1 + (T-1)/4) x H/8 x W/8; e.g. 25 x 256 x 256 -> 4 x 7 x 32 x 32 = 28,672 values",
                   "derivation": "z_channels 4; 4x8x8 compression ratio; causal first frame (inferred from the causal design)", "quote_ids": ["in_z", "in_cr", "in_class"]},
 "params": {"value": "encoder 94M + decoder 144M (OD-VAE = the v1.2.0 VAE, per the v1.3.0 report table)", "scope": "encoder 94M", "quote_ids": ["p_odvae"]},
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs statement for the VAE (the v1.2.0 report gives A100 encode time only)",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists vae/checkpoint.ckpt, gated=False", "quote_ids": ["w_file", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "MIT", "quote_ids": ["lic_card", "lic_text"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE of an open text-to-video model trained on general video", "quote_ids": ["dom_vae"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "the v1.2.0 report names the VAE training data per stage (K400; data collected in v1.1.0), and the v1.1.0 report names those sources (Mixkit, Pixabay, Pexels) with hours; caveat: SD2.1 image-VAE initialisation data not documented here", "quote_ids": ["data_train", "data_table", "data_mixkit", "data_pixabay", "data_pexel"]},
  "eligible": "YES (all four criteria PASS; caveat: SD2.1 image-VAE initialisation; Appendix300 UNKNOWN)"
 },
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"vae/checkpoint.ckpt\",", "source_file": API12},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API12},
  {"id": "w_report_model", "quote": "- Model: Both Diffusion Model and CausalVideoVAE [here](https://huggingface.co/LanguageBind/Open-Sora-Plan-v1.2.0).", "source_file": R12},
  {"id": "lic_card", "quote": "license: mit", "source_file": HF12},
  {"id": "lic_text", "quote": "MIT License", "source_file": LIC},
  {"id": "dom_vae", "quote": "The VAE in version 1.2.0 maintains the overall architecture of the previous version but merges the temporal and spatial downsampling layers.", "source_file": R12},
  {"id": "data_init", "quote": "As with v1.1.0, we initialize from the [SD2.1 VAE](https://huggingface.co/stabilityai/sd-vae-ft-mse) using tail initialization.", "source_file": R12},
  {"id": "data_train", "quote": "We perform the first phase of training on the Kinetic400 video dataset, then use the EMA weights from this phase to initialize the second phase, which is fine-tuned on high-quality data (collected in v1.1.0). All training is conducted on 25-frame 256×256 videos using **one A100 node**.", "source_file": R12},
  {"id": "data_table", "quote": "| 1 | K400 | 200,000 | | 2 | collected in v1.1.0 | 450,000 |", "source_file": R12},
  {"id": "data_v11_hours", "quote": "The v1.1.0 video dataset comprises approximately 3k hours, compared to only 300 hours in v1.0.0.", "source_file": R11},
  {"id": "data_mixkit", "quote": "| [Mixkit](https://mixkit.co/) | 42.0h | 65 | 54,735 |", "source_file": R11},
  {"id": "data_pixabay", "quote": "| [Pixabay](https://pixabay.com/) | 353.3h | 65 | 601,513 |", "source_file": R11},
  {"id": "data_pexel", "quote": "| [Pexel](https://www.pexels.com/) | 2561.9h | 65 | 3,832,666 |", "source_file": R11},
  {"id": "in_res", "quote": "\"resolution\": 256,", "source_file": C12},
  {"id": "in_gen", "quote": "## Gallery 93×1280×720 Text-to-Video Generation.", "source_file": R12},
  {"id": "in_cr", "quote": "| Open-Sora Plan v1.2 | 4x8x8| **31.16** | **0.8694** | 0.0586 |", "source_file": R12},
  {"id": "in_down", "quote": "\"encoder_spatial_downsample\": [ \"Downsample\", \"Spatial2xTime2x3DDownsample\", \"Spatial2xTime2x3DDownsample\", \"\" ],", "source_file": C12},
  {"id": "in_z", "quote": "\"z_channels\": 4", "source_file": C12},
  {"id": "in_class", "quote": "\"_class_name\": \"CausalVAEModel\",", "source_file": C12},
  {"id": "p_odvae", "quote": "| 4 | OD-VAE（Our VAE in v1.2.0） | 94M + 144M | 30.311| 0.043|", "source_file": R13}
 ]
}
save_record(recA)

# ---------------------------------------------------------------- 19b WF-VAE-L-16Chn
DATA_B = [WP, WRM, R13]
recB = {
 "id": "19b_wf_vae_l_16chn",
 "name": "WF-VAE-L 16-channel (PKU-YuanGroup WF-VAE; HF chestnutlzj/WF-VAE-L-16Chn, WFVAEModel); the 8-channel WF-VAE-S ships as the Open-Sora-Plan v1.3.0 VAE",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "chestnutlzj/WF-VAE-L-16Chn, diffusion_pytorch_model.safetensors + config.json (released 2024-11-25 per README; HF repo created 2024-11-24); paper arXiv:2411.17459v3 (CVPR 2025). Not separately recorded: Open-Sora-Plan v1.3.0 vae/merged.ckpt = 8-channel WF-VAE-S (latent_dim 8), 'a distilled form of OD-VAE ... its use is not recommended'",
 "paper": {"title": "WF-VAE: Enhancing Video VAE by Wavelet-Driven Energy Flow for Latent Video Diffusion Model", "year": 2024, "arxiv": "2411.17459"},
 "weights_location": {
  "urls": ["https://huggingface.co/chestnutlzj/WF-VAE-L-16Chn"],
  "files_listed": {"diffusion_pytorch_model.safetensors": 1268351816, "config.json": 947},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + APIWF + "; the official GitHub README links to this repo (first author's account); nothing downloaded",
  "quote_ids": ["w_file", "w_gated", "w_readme"]
 },
 "licence": {
  "id": "Apache-2.0 (HF card; GitHub LICENSE)",
  "url": "https://huggingface.co/chestnutlzj/WF-VAE-L-16Chn ; https://github.com/PKU-YuanGroup/WF-VAE/blob/main/LICENSE",
  "commercial": "permitted", "non_commercial_only": False, "restrictions": "none beyond Apache-2.0", "gating": "none",
  "quote_ids": ["lic_card", "lic_text", "lic_badge"]
 },
 "domain": {"value": "wavelet-driven causal video VAE for latent video diffusion models (used by Open-Sora Plan v1.3); trained on Kinetics-400", "quote_ids": ["dom_title", "data_k400"]},
 "architecture": {"type": "causal 3D conv VAE with multi-level Haar wavelet energy-flow pathway; causal cache for lossless chunked inference",
                  "representation": "encoder latents, 16 channels, 4x temporal x 8x8 spatial compression"},
 "pretraining_data": {"summary": "Kinetics-400 for training and validation (paper); stage I 25 frames at 256x256, stage II 49 frames with FPS halved. No other video data named. Evaluation on WebVid-10M / Panda-70M only.",
                      "form": "dataset list (named: Kinetics-400)"},
 "pretraining_data_quote": {"quote_ids": ["data_k400", "data_stages"]},
 "medical_video_in_data": {"answer": "NO", "basis": "closed named dataset (Kinetics-400, human-action classes) with no medical category; term search: hits only in reference titles (biomedical volume processing, U-Net/MICCAI), no data statement",
                           "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_B, MED_TERMS)}},
 "appendix300_possible": {"answer": "NO", "basis_class": "closed_curated_list",
  "basis": "training data = Kinetics-400 only (closed fixed action-class research dataset -> NO under conventions_v2). Caveat: the statement is the paper's; the README does not separately document the released 16-channel checkpoint's data. Timing: released 2024-11, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_k400"]},
 "appendix300_check": {
  "answer": "NO", "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "closed_curated_list", "basis": "Kinetics-400 only",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_B, A300_TERMS)},
  "quote_ids": ["data_k400"]
 },
 "input": {
  "frame_size": {"value": "trained at 256x256 (stage I); README inference example 512x512", "quote_ids": ["data_stages", "in_recon_size"]},
  "frame_rate_or_sampling": {"value": "stage I native frame rate (not stated); stage II 'reduce the FPS by half'; README reconstruction example --fps 30 --sample_rate 1", "quote_ids": ["data_stages", "in_recon_fps", "in_recon_sr"]},
  "clip_length_frames": {"value": "25 frames (stage I), 49 frames (stage II); evaluation on 33 frames; README example 65 frames", "quote_ids": ["data_stages", "in_eval33", "in_recon_frames"]},
  "temporal_compression": {"value": "4x (causal; first frame kept)", "quote_ids": ["in_cr16", "in_causal"]},
  "spatial_compression": {"value": "8x8", "quote_ids": ["in_cr16"]}
 },
 "embedding_dim": {"value": "16 latent channels x (1 + (T-1)/4) x H/8 x W/8; e.g. 33 x 256 x 256 -> 16 x 9 x 32 x 32 = 147,456 values",
                   "derivation": "latent_dim 16 (config); 4x8x8 compression (paper Table 1, 16-channel row); causal first frame", "quote_ids": ["in_latent", "in_cr16", "in_causal"]},
 "params": {"value": "WF-VAE-L: encoder 84M, decoder 232M (paper Table 3); README: 16-channel WF-VAE-L 316M total", "scope": "encoder 84M", "quote_ids": ["p_table3", "w_readme"]},
 "flops_per_input_if_documented": None,
 "flops_note": "paper/README report encode/decode time and memory (33-frame videos, H100) but no FLOPs figure in the saved text",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists diffusion_pytorch_model.safetensors, gated=False; official README links it", "quote_ids": ["w_file", "w_gated", "w_readme"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "Apache-2.0", "quote_ids": ["lic_card", "lic_text"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE for latent video diffusion (generative) models, trained on general video", "quote_ids": ["dom_title", "data_k400"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "paper names the training dataset (Kinetics-400)", "quote_ids": ["data_k400"]},
  "eligible": "YES (all four criteria PASS; Appendix300 NO; caveat: data statement is the paper's, not checkpoint-specific)"
 },
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"diffusion_pytorch_model.safetensors\",", "source_file": APIWF},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": APIWF},
  {"id": "w_readme", "quote": "We have released our **16-channel WF-VAE-L (316M)** model along with the training code. Welcome to download it from [Huggingface](https://huggingface.co/chestnutlzj/WF-VAE-L-16Chn).", "source_file": WRM},
  {"id": "w_v13_s", "quote": "We have released the **8-channel WF-VAE-S (146M)** on Open-Sora Plan v1.3.", "source_file": WRM},
  {"id": "lic_card", "quote": "license: apache-2.0", "source_file": HFWF},
  {"id": "lic_text", "quote": "Apache License Version 2.0, January 2004", "source_file": WLIC},
  {"id": "lic_badge", "quote": "[![License](https://img.shields.io/badge/Code%20License-Apache2.0-yellow)](https://github.com/PKU-YuanGroup/WF-VAE/blob/main/LICENSE)", "source_file": WRM},
  {"id": "dom_title", "quote": "WF-VAE: Enhancing Video VAE by Wavelet-Driven Energy Flow for Latent Video Diffusion Model", "source_file": HFWF},
  {"id": "data_k400", "quote": "Dataset & Evaluation. We utilize the Kinetics-400 dataset [ 16 ] for both training and validation. For testing, we employ the Panda70M [ 7 ] and WebVid-10M [ 2 ] datasets.", "source_file": WP},
  {"id": "data_stages", "quote": "(I) the first stage aligns with [ 6 ] , where we preprocess videos to 25 frames with 256 × 256 256\\times 256 resolution, and a total batch size of 8. (II) we refresh the discriminator, increase the number of frames to 49, and reduce the FPS by half to enhance motion dynamics.", "source_file": WP},
  {"id": "in_eval33", "quote": "All measurements are conducted on 33 frames with 256×256 resolution videos.", "source_file": WP},
  {"id": "in_recon_fps", "quote": "--fps 30", "source_file": WRM},
  {"id": "in_recon_sr", "quote": "--sample_rate 1", "source_file": WRM},
  {"id": "in_recon_frames", "quote": "--num_frames 65", "source_file": WRM},
  {"id": "in_recon_size", "quote": "--height 512", "source_file": WRM},
  {"id": "in_cr16", "quote": "WF-VAE-L (Ours) 256 " + ZW + " ( 4 × 8 × 8 ) 256(4\\times 8\\times 8) 16 35.76", "source_file": WP},
  {"id": "in_causal", "quote": "For the first time chunk, we perform standard causal padding to support joint processing of graphs and videos.", "source_file": R13},
  {"id": "in_latent", "quote": "\"latent_dim\": 16,", "source_file": CWF},
  {"id": "p_table3", "quote": "Model BC Params (M) Kinetics-400 Enc Dec PSNR ↑ \\uparrow LPIPS ↓ \\downarrow WF-VAE-S 128 38 108 28.21 0.0779 WF-VAE-M 160 58 164 28.44 0.0699 WF-VAE-L 192 84 232 28.66 0.0661", "source_file": WP}
 ]
}
save_record(recB)
