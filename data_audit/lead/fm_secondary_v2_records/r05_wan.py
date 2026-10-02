import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, prev_candidate, term_search, MED_TERMS, A300_TERMS

API21 = "wan_Wan-AI__Wan2.1-T2V-1.3B_hfapi.json"; API22 = "wan_Wan-AI__Wan2.2-TI2V-5B_hfapi.json"
R21 = "wan_Wan2.1-T2V-1.3B_README.md"; L21 = "wan_Wan2.1-T2V-1.3B_LICENSE.txt"; R22 = "wan_Wan2.2-TI2V-5B_README.md"
L22 = "wan_github_Wan2.2_main_LICENSE.txt"; P = "wan_arxiv_2503.20314_fulltext.txt"
V21 = "wan_github_Wan2.1_main_vae.py.txt"; V22 = "wan_github_Wan2.2_main_vae2_2.py.txt"
C21 = "wan_github_Wan2.1_main_wan_t2v_1_3B.py.txt"; S21 = "wan_github_Wan2.1_main_shared_config.py.txt"
G21 = "wan_github_Wan2.1_main_generate.py.txt"; C22 = "wan_github_Wan2.2_main_wan_ti2v_5B.py.txt"
DATA_FILES = [P, R21, R22]

v1 = prev_candidate("05_wan_vae")
rec = {
 "id": "05_wan_vae",
 "name": v1["name"],
 "version": "Wan2.1_VAE.pth in Wan-AI/Wan2.1-T2V-1.3B (HF repo sha 37ec512624d61f7aa208f7ea8140a131f93afc9a, created 2025-02-25) and Wan2.2_VAE.pth in Wan-AI/Wan2.2-TI2V-5B (HF repo sha 921dbaf3f1674a56f47e83fb80a34bac8a8f203e, created 2025-07-18); loader code: Wan-Video/Wan2.1 wan/modules/vae.py (WanVAE) and Wan-Video/Wan2.2 wan/modules/vae2_2.py (Wan2_2_VAE), main branch 2026-10-02",
 "paper": v1["paper"],
 "weights_location": {
  "urls": ["https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B (Wan2.1_VAE.pth)", "https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B (Wan2.2_VAE.pth)"],
  "files_listed": {"Wan2.1_VAE.pth": 507609880, "Wan2.2_VAE.pth": 2818839170},
  "gated": False, "private": False,
  "verified_how": "HF API model listings (metadata only) saved as " + API21 + " and " + API22 + "; nothing downloaded",
  "quote_ids": ["w_file21", "w_gated21", "w_file22", "w_gated22"]
 },
 "licence": {
  "id": v1["licence"]["id"],
  "url": v1["licence"]["url"] + " ; https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B (card) ; https://github.com/Wan-Video/Wan2.2/blob/main/LICENSE.txt",
  "commercial": v1["licence"]["commercial"], "non_commercial_only": v1["licence"]["non_commercial_only"],
  "restrictions": v1["licence"]["restrictions"], "gating": v1["licence"]["gating"],
  "quote_ids": ["lic_card21", "lic_text", "lic_card22", "lic_text22"]
 },
 "domain": {
  "value": "3D causal video VAEs of the Wan2.1 / Wan2.2 text/image-to-video diffusion models; Wan2.1-VAE inflated from a 2D image VAE and trained on videos from a general-domain curated pool (internal copyrighted + publicly accessible sources)",
  "quote_ids": ["arch_448", "arch_train", "data_src"]
 },
 "architecture": {"type": v1["architecture"]["type"], "representation": v1["architecture"]["representation"]},
 "pretraining_data": {"summary": v1["pretraining_data"]["summary"], "form": v1["pretraining_data"]["form"]},
 "pretraining_data_quote": {"quote_ids": ["data_src", "data_billions", "arch_train", "vae_ft", "data_22"]},
 "medical_video_in_data": {
  "answer": v1["medical_video_in_data"]["answer"],
  "basis": v1["medical_video_in_data"]["basis"],
  "quote_ids": ["lim_medicine"],
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}
 },
 "appendix300_possible": v1["appendix300_possible"],
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "undisclosed",
  "basis": "pretraining data 'sourced from both internal copyrighted sources and publicly accessible data', not itemised; the documentation does not allow the Appendix300 source recordings to be excluded. Timing: Wan2.1 2025-02/03, Wan2.2 2025-07, both before the OPARA issue 2026-04-29.",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_src"]
 },
 "input": {
  "frame_size": {"value": "Wan2.1-VAE: trained first at 128x128 (5-frame), then fine-tuned on high-quality videos of different resolutions; card: encodes/decodes 1080P video of any length; Wan2.1-T2V-1.3B recommended 480P (832x480). Wan2.2-VAE: used at 720P (1280x704) in TI2V-5B", "quote_ids": ["arch_train", "vae_ft", "in_1080p", "arch_res21", "in_size21", "in_size22"]},
  "frame_rate_or_sampling": {"value": "VAE fps not documented; Wan2.1 DiT stage-1 video clips at 16 fps and default sample_fps = 16; Wan2.2 TI2V-5B: 720P at 24 fps (sample_fps = 24)", "quote_ids": ["in_fps_train21", "in_fps21", "in_fps22_card", "in_fps22"]},
  "clip_length_frames": {"value": "causal 1+T frames, encoded chunk-wise (at most 4 frames per chunk), any length; default generation 81 frames (Wan2.1) / 121 frames (Wan2.2 TI2V-5B)", "quote_ids": ["in_shape21", "in_chunk", "in_frames21", "in_frames22"]},
  "temporal_compression": {"value": "4x (1 + T/4 latent frames) for both", "quote_ids": ["arch_448", "in_shape21", "in_stride21", "in_stride22"]},
  "spatial_compression": {"value": "8x8 (Wan2.1-VAE); 16x16 (Wan2.2-VAE: 2x2 patchify + 8x8)", "quote_ids": ["arch_448", "arch_22", "in_stride21", "in_stride22", "in_patchify22"]}
 },
 "embedding_dim": {
  "value": "Wan2.1-VAE: 16 x 21 x 60 x 104 = 2,096,640 values for an 81-frame 480x832 clip (16 x (1+T/4) x H/8 x W/8). Wan2.2-VAE: 48 x 31 x 44 x 80 = 5,237,760 values for a 121-frame 704x1280 clip (48 x (1+T/4) x H/16 x W/16)",
  "derivation": "Wan2.1 latent channels 16 (paper; WanVAE z_dim=16); Wan2.2 latent channels 48 (Wan2_2_VAE z_dim=48, official code); strides from the official configs",
  "quote_ids": ["arch_latent16", "in_shape21", "in_zdim21", "in_zdim22", "in_stride21", "in_stride22"]
 },
 "params": {
  "value": "Wan2.1-VAE: 127M (whole VAE, paper); encoder-only not documented. Wan2.2-VAE: not documented (inferred, not documentation: Wan2.2_VAE.pth 2,818,839,170 bytes)",
  "scope": "whole autoencoder (Wan2.1); not documented (Wan2.2)",
  "quote_ids": ["arch_127m", "w_file22"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs/MACs statement in the saved paper, cards or code (searched FLOP|TFLOP)",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": v1["eligibility"]["C1_open_weights"]["basis"], "quote_ids": ["w_file21", "w_gated21", "w_file22", "w_gated22"]},
  "C2_licence_research_use": {"status": "PASS", "basis": v1["eligibility"]["C2_licence_research_use"]["basis"], "quote_ids": ["lic_card21", "lic_card22"]},
  "C3_domain_secondary": {"status": "PASS", "basis": v1["eligibility"]["C3_domain_secondary"]["basis"], "quote_ids": ["arch_448", "arch_22"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": v1["eligibility"]["C4_documented_pretraining_data"]["basis"], "quote_ids": ["data_src", "data_billions"]},
  "eligible": v1["eligibility"]["eligible"]
 },
 "changes_vs_v1": [
  "sources re-fetched into /home fm_sources/secondary (raw sha256 compared with v1 per quote)",
  "v1 architecture.representation said the Wan2.2-VAE latent dim was 'not quoted from saved sources'; revision 2 documents it from the official Wan2.2 code: z_dim=48 (Wan2_2_VAE), with 2x2 patchify before the 8x8 encoder (16x16 total)",
  "the HF repo Wan-AI/Wan2.2-TI2V-5B has no LICENSE file (raw LICENSE.txt returned 404); its licence is quoted from the card ('license: apache-2.0' and 'licensed under the Apache 2.0 License') and the GitHub Wan2.2 LICENSE.txt",
  "added structured fields (version, weights_location, domain, pretraining_data_quote, appendix300_check, input, embedding_dim, params, flops)",
  "no change to any eligibility status or Appendix300 answer"
 ],
 "quotes": [
  {"id": "w_file21", "quote": "\"rfilename\": \"Wan2.1_VAE.pth\",", "source_file": API21},
  {"id": "w_gated21", "quote": "\"gated\": false,", "source_file": API21},
  {"id": "w_file22", "quote": "\"rfilename\": \"Wan2.2_VAE.pth\",", "source_file": API22},
  {"id": "w_gated22", "quote": "\"gated\": false,", "source_file": API22},
  {"id": "lic_card21", "quote": "The models in this repository are licensed under the Apache 2.0 License.", "source_file": R21},
  {"id": "lic_text", "quote": "Apache License", "source_file": L21},
  {"id": "lic_card22", "quote": "The models in this repository are licensed under the Apache 2.0 License.", "source_file": R22},
  {"id": "lic_text22", "quote": "Apache License Version 2.0, January 2004", "source_file": L22},
  {"id": "arch_448", "quote": "Wan -VAE can compress the spatio-temporal dimension of a video by 4 × 8 × 8 4\\times 8\\times 8 times.", "source_file": P},
  {"id": "arch_127m", "quote": "Wan -VAE achieves a compact model size of only 127M parameters.", "source_file": P},
  {"id": "arch_latent16", "quote": "adopt the same compression rate and latent feature dimension as our approach, i.e., a compression rate of 4 × 8 × 8 4\\times 8\\times 8 with a latent dimension of 16.", "source_file": P},
  {"id": "arch_22", "quote": "It is supported by a high-compression Wan2.2-VAE, which achieves a $T\\times H\\times W$ compression ratio of $4\\times16\\times16$, increasing the overall compression rate to 64 while maintaining high-quality video reconstruction.", "source_file": R22},
  {"id": "arch_train", "quote": "First, we construct a 2D image VAE with the same structure and train it on image data. Then, we inflate the well-trained 2D image VAE into a 3D causal Wan -VAE to provide an initial spatial compression prior, which drastically improves the training speed compared to training a video VAE from scratch. At this stage, Wan -VAE is trained on the low-resolution (128 × \\times 128) and small frame number (5-frame) videos to accelerate convergence speed.", "source_file": P},
  {"id": "vae_ft", "quote": "Finally, we fine-tune the model on high-quality videos with different resolutions and frame numbers, integrating the GAN loss ( Esser et al., 2021 ) from a 3D discriminator.", "source_file": P},
  {"id": "arch_res21", "quote": "For optimal performance, we recommend using 480P resolution", "source_file": R21},
  {"id": "in_1080p", "quote": "encoding and decoding 1080P videos of any length while preserving temporal information", "source_file": R21},
  {"id": "in_size21", "quote": "python generate.py --task t2v-1.3B --size 832*480 --ckpt_dir ./Wan2.1-T2V-1.3B", "source_file": R21},
  {"id": "in_size22", "quote": "python generate.py --task ti2v-5B --size 1280*704 --ckpt_dir ./Wan2.2-TI2V-5B", "source_file": R22},
  {"id": "in_fps_train21", "quote": "5-second video clips ( 192 ​ p ​ x 192\\penalty\\ px resolution, 16 16 fps)", "source_file": P},
  {"id": "in_fps21", "quote": "wan_shared_cfg.sample_fps = 16", "source_file": S21},
  {"id": "in_fps22_card", "quote": "This model supports both text-to-video and image-to-video generation at 720P resolution with 24fps", "source_file": R22},
  {"id": "in_fps22", "quote": "ti2v_5B.sample_fps = 24", "source_file": C22},
  {"id": "in_frames21", "quote": "args.frame_num = 1 if \"t2i\" in args.task else 81", "source_file": G21},
  {"id": "in_frames22", "quote": "ti2v_5B.frame_num = 121", "source_file": C22},
  {"id": "in_shape21", "quote": "Wan -VAE compresses its spatio-temporal dimensions to [ 1 + T / 4 , H / 8 , W / 8 ] [1+T/4,H/8,W/8] while expanding the number of channels C C to 16.", "source_file": P},
  {"id": "in_chunk", "quote": "the number of frames in each processing chunk is limited to at most 4, effectively preventing memory overflow.", "source_file": P},
  {"id": "in_stride21", "quote": "t2v_1_3B.vae_stride = (4, 8, 8)", "source_file": C21},
  {"id": "in_stride22", "quote": "ti2v_5B.vae_stride = (4, 16, 16)", "source_file": C22},
  {"id": "in_zdim21", "quote": "class WanVAE: def __init__(self, z_dim=16,", "source_file": V21},
  {"id": "in_zdim22", "quote": "class Wan2_2_VAE: def __init__( self, z_dim=48, c_dim=160,", "source_file": V22},
  {"id": "in_patchify22", "quote": "x = patchify(x, patch_size=2)", "source_file": V22},
  {"id": "data_src", "quote": "3.1 Pre-training Data We curated and deduplicated a candidate dataset sourced from both internal copyrighted sources and publicly accessible data.", "source_file": P},
  {"id": "data_billions", "quote": "Following these principles, we curated a dataset comprising billions of videos and images.", "source_file": P},
  {"id": "data_22", "quote": "Compared to Wan2.1, Wan2.2 is trained on a significantly larger data, with +65.6% more images and +83.2% more videos.", "source_file": R22},
  {"id": "lim_medicine", "quote": "As a foundational video model, we are committed to enhancing Wan ’s general capabilities, yet performance in specific localized scenarios, such as education and medicine, may be insufficient.", "source_file": P}
 ]
}
prev_q = {q["id"]: q for q in v1["quotes"]}
save_record(rec, prev_quotes=prev_q)
