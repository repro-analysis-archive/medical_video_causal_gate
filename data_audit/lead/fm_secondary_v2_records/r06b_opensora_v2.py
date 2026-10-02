import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, prev_candidate, term_search, MED_TERMS, A300_TERMS

API = "opensora_hpcai-tech__Open-Sora-v2-Video-DC-AE_hfapi.json"; API2 = "opensora_hpcai-tech__Open-Sora-v2_hfapi.json"
C2 = "opensora_Open-Sora-v2-Video-DC-AE_README.md"; P2 = "opensora_arxiv_2503.09642_fulltext.txt"
LIC = "opensora_github_main_LICENSE.txt"; AE = "opensora_github_main_docs_ae.md"; TR = "opensora_github_main_docs_train.md"
HC = "opensora_github_main_docs_hcae.md"; TRC = "opensora_github_main_configs_vae_train_video_dc_ae.py.txt"
HCI = "opensora_github_main_configs_diffusion_inference_high_compression.py.txt"; DC = "opensora_github_main_dc_ae_models_dc_ae.py.txt"
DATA_FILES = [P2, C2, AE, TR]

v1 = prev_candidate("06b_opensora_v2_video_dc_ae")
arch = dict(v1["architecture"])
rec = {
 "id": "06b_opensora_v2_video_dc_ae",
 "name": v1["name"],
 "version": "hpcai-tech/Open-Sora-v2-Video-DC-AE, F32T4C128_AE.safetensors (HF repo sha 36059624245459163efecfdb89eb08e01ee32fbf, created 2025-03-10); model_name 'dc-ae-f32t4c128' in the official Open-Sora main code (the same repo also holds Open_Sora_v2_Video_DC_AE.safetensors = the DiT adapted to this AE, not the AE)",
 "paper": v1["paper"],
 "weights_location": {
  "urls": ["https://huggingface.co/hpcai-tech/Open-Sora-v2-Video-DC-AE"],
  "files_listed": {"F32T4C128_AE.safetensors": 918970214, "Open_Sora_v2_Video_DC_AE.safetensors (DiT, not the AE)": 23784062736},
  "gated": False, "private": False,
  "verified_how": "HF API model listings (metadata only) saved as " + API + " and " + API2 + "; nothing downloaded",
  "quote_ids": ["w_file", "w_gated", "w_cfg_ckpt"]
 },
 "licence": {
  "id": v1["licence"]["id"], "url": v1["licence"]["url"] + " ; https://github.com/hpcaitech/Open-Sora/blob/main/LICENSE",
  "commercial": v1["licence"]["commercial"], "non_commercial_only": v1["licence"]["non_commercial_only"],
  "restrictions": v1["licence"]["restrictions"], "gating": v1["licence"]["gating"],
  "quote_ids": ["lic_card2", "lic_text"]
 },
 "domain": {
  "value": "deep-compression video autoencoder (no KL) of the Open-Sora 2.0 text/image-to-video model (used for its high-compression variant), trained from scratch on general video",
  "quote_ids": ["dom_ae", "dom_scratch", "arch_dcae"]
 },
 "architecture": {"type": arch["type"],
                  "representation": "latents at 4x32x32 compression with 128 channels (released dc-ae-f32t4c128; a 256-channel variant was trained but not released in this repo)"},
 "pretraining_data": {"summary": v1["pretraining_data"]["summary"] + " The official AE training config defaults to datasets/pexels_45k_necessary.csv, which the training guide presents only as an example dataset; neither the paper nor the card states the released AE's training sources.",
                      "form": v1["pretraining_data"]["form"]},
 "pretraining_data_quote": {"quote_ids": ["arch_train", "data_pyramid", "data_fps_filter", "data_ae_docs", "data_example", "data_cfg"]},
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
  "basis": "the paper describes only a filtering pyramid and statistics of 'the collected video data'; no sources named. Even if the AE was trained on the Pexels-45k example set referenced by the training config, that is an open-ended stock-footage source (would be named_open_web_sources -> still UNKNOWN). Timing: released 2025-03, before the OPARA issue 2026-04-29.",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_pyramid", "data_example"]
 },
 "input": {
  "frame_size": {"value": "trained on 256px 1:1 clips (spatial tile 256 at inference); Open-Sora 2.0 generates 256px and 768px", "quote_ids": ["arch_train", "in_tile_doc", "in_gen"]},
  "frame_rate_or_sampling": {"value": "AE training config fps_max=24; training data filtered to 16 <= fps < 30; generation at 24 FPS", "quote_ids": ["in_fps_cfg", "data_fps_filter", "data_fps_out", "in_gen"]},
  "clip_length_frames": {"value": "32-frame training clips (temporal tile 32 at inference; multiples of 4 work, multiples of 32 recommended); generation up to 128 frames", "quote_ids": ["arch_train", "in_tile_doc", "in_mult", "in_gen"]},
  "temporal_compression": {"value": "4x (non-causal)", "quote_ids": ["arch_dcae", "in_cfg_tc", "in_table"]},
  "spatial_compression": {"value": "32x32", "quote_ids": ["arch_dcae", "in_cfg_sc"]}
 },
 "embedding_dim": {
  "value": "128 latent channels x 8 x 8 x 8 = 65,536 values per 32-frame 256x256 clip (128 x T/4 x H/32 x W/32)",
  "derivation": "latent_channels=128 (official dc-ae-f32t4c128 config; paper: 128-channel variant used in the generation model); latent shape 8x8x8 for 32-frame 256px (paper)",
  "quote_ids": ["in_cfg_lc", "in_128", "arch_dcae", "w_cfg_ckpt"]
 },
 "params": {
  "value": "not documented in the saved paper, card, docs or code; (inferred, not documentation: F32T4C128_AE.safetensors 918,970,214 bytes)",
  "scope": "not documented",
  "quote_ids": ["w_file"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "the paper's only FLOPs statement is training MFU ('maximum FLOPs utilization (MFU) of 38.19%'); no AE FLOPs per input documented",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": v1["eligibility"]["C1_open_weights"]["basis"], "quote_ids": ["w_file", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": v1["eligibility"]["C2_licence_research_use"]["basis"], "quote_ids": ["lic_card2"]},
  "C3_domain_secondary": {"status": "PASS", "basis": v1["eligibility"]["C3_domain_secondary"]["basis"], "quote_ids": ["dom_ae", "arch_dcae"]},
  "C4_documented_pretraining_data": {"status": "FAIL",
   "basis": v1["eligibility"]["C4_documented_pretraining_data"]["basis"] + "; borderline caveat: the official AE training config's default data_path is the Pexels-45k set, but the training guide calls it 'an example' and neither the model card nor the paper lists the AE training data, so under the frozen wording ('a model card or paper lists ...') C4 stays FAIL",
   "quote_ids": ["data_pyramid", "data_example", "data_cfg"]},
  "eligible": v1["eligibility"]["eligible"] + " -- borderline (see C4 caveat)"
 },
 "changes_vs_v1": [
  "sources re-fetched into /home fm_sources/secondary (raw sha256 compared with v1 per quote)",
  "CORRECTION architecture.representation: v1 '128 or 256 channels trained (released file name F32T4C128 suggests 128 channels -- inferred from the file name only)' -> '128 channels', now documented by the official code (dc_ae_f32: latent_channels=128 for 'dc-ae-f32t4c128'), by the official high-compression inference config (loads F32T4C128_AE.safetensors as dc-ae-f32t4c128, DiT in_channels=128) and by the paper ('we opt for the 128-channel variant')",
  "NEW caveat on C4 (status unchanged FAIL): official AE training config data_path = datasets/pexels_45k_necessary.csv, presented in docs/train.md as an example dataset; recorded as borderline, not a pass, because neither card nor paper lists the AE training data",
  "added structured fields (version, weights_location, domain, pretraining_data_quote, appendix300_check, input, embedding_dim, params, flops)",
  "no change to any eligibility status or Appendix300 answer"
 ],
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"F32T4C128_AE.safetensors\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "w_cfg_ckpt", "quote": "model_name=\"dc-ae-f32t4c128\", from_pretrained=\"./ckpts/F32T4C128_AE.safetensors\",", "source_file": HCI},
  {"id": "lic_card2", "quote": "license: apache-2.0", "source_file": C2},
  {"id": "lic_text", "quote": "Apache License Version 2.0, January 2004", "source_file": LIC},
  {"id": "dom_ae", "quote": "We propose a video autoencoder architecture based on [DC-AE](https://github.com/mit-han-lab/efficientvit), the __Video DC-AE__, which compression the video by 4x in the temporal dimension and 32x32 in the spatial dimension.", "source_file": AE},
  {"id": "dom_scratch", "quote": "We train our __Video DC-AE__ from scratch on 8xGPUs for 3 weeks.", "source_file": AE},
  {"id": "arch_dcae", "quote": "our Video DC-AE with a 4 × 32 × 32 4\\times 32\\times 32 compression ratio and a patch size of 1 × 1 × 1 1\\times 1\\times 1 enables training on 32-frame, 256px videos with a latent shape of 8 × 8 × 8 8\\times 8\\times 8 .", "source_file": P2},
  {"id": "arch_train", "quote": "We train each AE model on 8 GPUs with a local batch size of 1. Our training data consists of 32 frames of 256px videos at an aspect ratio of 1:1.", "source_file": P2},
  {"id": "in_table", "quote": "Video DC-AE 4 × 32 × 32 4\\times 32\\times 32 96 128 × \\times 0.051 30.538 0.863", "source_file": P2},
  {"id": "in_128", "quote": "we opt for the 128-channel variant in the video generation model to enable faster adaptation due to its reduced channel size", "source_file": P2},
  {"id": "in_cfg_lc", "quote": "\"latent_channels=128\"", "source_file": DC},
  {"id": "in_cfg_tc", "quote": "\"time_compression_ratio=4 \"", "source_file": DC},
  {"id": "in_cfg_sc", "quote": "\"spatial_compression_ratio=32 \"", "source_file": DC},
  {"id": "in_tile_doc", "quote": "Since our Video DC-AE is trained on 256px videos of 32 frames only, `spatial_tile_size` should be set to 256 and `temporal_tile_size` should be set to 32.", "source_file": AE},
  {"id": "in_mult", "quote": "although multiples of 4 works, we generally recommend to use frame numbers of multiples of 32", "source_file": AE},
  {"id": "in_gen", "quote": "Our model supports both T2V and I2V generation at 256×256px and 768×768px resolutions (hereafter referred to as 256px and 768px), generating videos up to 128 frames long. At 24 FPS, this corresponds to a 5-second duration.", "source_file": P2},
  {"id": "in_fps_cfg", "quote": "fps_max=24,", "source_file": TRC},
  {"id": "data_pyramid", "quote": "2 Data Our goal for data is to build a hierarchical data pyramid, catering to the requirement of the progressive training process.", "source_file": P2},
  {"id": "data_fps_filter", "quote": "we filter out videos with a duration of less than 2 seconds, a bit per pixel (bpp) below 0.02, a frame rate (fps) under 16, and an aspect ratio outside the range [1/3, 3]", "source_file": P2},
  {"id": "data_fps_out", "quote": "frame rate (fps) below 30, longer dimension not exceeding 1080 pixels, and H.264 codec.", "source_file": P2},
  {"id": "data_ae_docs", "quote": "Follow this [guide](./train.md#prepare-dataset) to prepare the __DATASET__ for training and inference. You may use our provided dataset or custom ones.", "source_file": AE},
  {"id": "data_example", "quote": "To better illustrate the process, we will use a 45k [pexels dataset](https://huggingface.co/datasets/hpcai-tech/open-sora-pexels-45k) as an example. This dataset contains clipped, score filtered high-quality videos from [Pexels](https://www.pexels.com/).", "source_file": TR},
  {"id": "data_cfg", "quote": "data_path=\"datasets/pexels_45k_necessary.csv\",", "source_file": TRC}
 ]
}
prev_q = {q["id"]: q for q in v1["quotes"]}
save_record(rec, prev_quotes=prev_q)
