import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_lib import save_record
R = "opensora_github_v1.2.0_report_03.md"; D = "opensora_github_v1.2.0_datasets.md"; P1 = "opensora_arxiv_2412.20404_fulltext.html"
P2 = "opensora_arxiv_2503.09642_fulltext.html"; CV = "opensora_OpenSora-VAE-v1.2_config.json"; CR = "opensora_OpenSora-VAE-v1.2_README.md"
LIC = "opensora_github_main_LICENSE"; C2 = "opensora_Open-Sora-v2-Video-DC-AE_README.md"
recA = {
 "id": "06a_opensora_vae_v1_2",
 "name": "Open-Sora VAE v1.2 (hpcai-tech/OpenSora-VAE-v1.2; SDXL 2D VAE + MAGVIT-v2-style causal temporal VAE)",
 "paper": {"title": "Open-Sora: Democratizing Efficient Video Production for All", "year": 2024, "arxiv": "2412.20404",
           "also": "Open-Sora 1.2 technical report, GitHub docs/report_03.md at tag v1.2.0"},
 "weights": {"urls": ["https://huggingface.co/hpcai-tech/OpenSora-VAE-v1.2"], "hf_api_evidence": ["opensora_OpenSora-VAE-v1.2_hfapi_blobs.json"],
             "files_listed": {"model.safetensors": 1573430548}, "gated": False, "private": False,
             "note": "config pulls the 2D VAE from PixArt-alpha/pixart_sigma_sdxlvae_T5_diffusers (SDXL VAE). Not downloaded."},
 "licence": {"id": "Apache-2.0", "url": "https://huggingface.co/hpcai-tech/OpenSora-VAE-v1.2 ; https://github.com/hpcaitech/Open-Sora/blob/main/LICENSE",
             "commercial": "permitted", "non_commercial_only": False, "restrictions": "none beyond Apache-2.0 (SDXL VAE component carries its own upstream licence, not audited here)",
             "gating": "none", "quote_ids": ["lic_card", "lic_text"]},
 "architecture": {
   "type": "stacked video compression network: 2D VAE (SDXL, 83M) spatial 8x8 then causal 3D VAE (MAGVIT-v2 structure, 300M) temporal 4x",
   "params": "384M total",
   "representation": "4-channel latents after 8x8 spatial + 4x temporal compression (scale/shift per channel in config)",
   "input_resolution": "trained mainly at 256x256; Open-Sora 1.2 generates 144p-720p",
   "frames_per_clip": "17-frame micro-clips (micro_frame_size 17); stage 3 mixed lengths up to 34 frames",
   "temporal_compression": "4x", "spatial_compression": "8x8",
   "quote_ids": ["arch_384", "arch_4x", "arch_micro", "arch_sdxl"]
 },
 "pretraining_data": {
   "summary": "3D VAE trained on videos from Pexels and Pixabay (17-frame, 256x256 clips); 2D VAE initialised from SDXL VAE (image data, not documented here). Open-Sora 1.2 diffusion model data are a named list (Webvid-10M, Panda-70M, HD-VG-130M, MiraData, Vript, Inter4K, Pexels, Pixabay, Mixkit; images: Midjourney sets, Unsplash-lite, LAION-Aesthetics subset).",
   "form": "dataset/source list (named)",
   "quote_ids": ["data_vae", "data_vae_paper", "data_open", "data_list_intro"]
 },
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "Search of saved report_03.md, datasets.md and paper HTML for medic|surg|endoscop|laparoscop|clinic|hospital|health: no hits. Sources are free-licence stock-footage sites."},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "named_open_web_sources", "basis": "VAE video data = Pexels + Pixabay stock-footage sites: named, but item-level content is open-ended, so the documentation does not exclude the source recordings. Context: VAE released 2024-06-17, before the OPARA issue 2026-04-29; nothing documented suggests surgical content.", "quote_ids": ["data_vae"]},
 "eligibility": {
   "C1_open_weights": {"status": "PASS", "basis": "HF API lists model.safetensors, gated=False"},
   "C2_licence_research_use": {"status": "PASS", "basis": "Apache-2.0"},
   "C3_domain_secondary": {"status": "PASS", "basis": "video VAE of an open text-to-video model trained on general (stock) video"},
   "C4_documented_pretraining_data": {"status": "PASS", "basis": "technical report and paper name the VAE training sources (Pexels, Pixabay) and the full Open-Sora 1.2 dataset list; caveat: the initialising SDXL 2D VAE's image data are not documented in these sources"},
   "eligible": "YES (all four criteria PASS; caveat on the SDXL image-VAE initialisation)"
 },
 "quotes": [
  {"id": "lic_card", "quote": "license: apache-2.0", "source_file": CR},
  {"id": "lic_text", "quote": "Apache License Version 2.0, January 2004", "source_file": LIC},
  {"id": "arch_384", "quote": "For the 3D VAE, we adopt the structure of VAE in [Magvit-v2](https://magvit.cs.cmu.edu/v2/), which contains 300M parameters. Along with 83M 2D VAE, the total parameters of the video compression network is 384M.", "source_file": R},
  {"id": "arch_4x", "quote": "we propose a simple video compression network, which first compress the video in the spatial dimension by 8x8 times, then compress the video in the temporal dimension by 4x times.", "source_file": R},
  {"id": "arch_micro", "quote": "\"micro_frame_size\": 17,", "source_file": CV},
  {"id": "arch_sdxl", "quote": "We initialize the 2D VAE with [SDXL's VAE](https://huggingface.co/stabilityai/sdxl-vae), which is better than our previously used one.", "source_file": R},
  {"id": "data_vae", "quote": "The training data is videos from pixels and pixabay, and the training video size is mainly 17 frames, 256x256 resolution.", "source_file": R},
  {"id": "data_vae_paper", "quote": "The 3D VAE was trained for 1.2M steps with a local batch size of 1, using videos from Pexels and Pixabay. The training data primarily consisted of 17-frame clips at a resolution of 256×256.", "source_file": P1},
  {"id": "data_open", "quote": "2.1 Data Source The dataset used is all open-sourced to make the model training fully reproducible.", "source_file": P1},
  {"id": "data_list_intro", "quote": "For Open-Sora 1.2, we conduct mixed training with both images and videos. The main datasets we use are listed below.", "source_file": D}
 ]
}
save_record(recA)
recB = {
 "id": "06b_opensora_v2_video_dc_ae",
 "name": "Open-Sora 2.0 Video DC-AE (hpcai-tech/Open-Sora-v2-Video-DC-AE, F32T4C128_AE.safetensors); note Open-Sora-v2 main repo ships hunyuan_vae.safetensors (= HunyuanVideo VAE, see 04)",
 "paper": {"title": "Open-Sora 2.0: Training a Commercial-Level Video Generation Model in $200k", "year": 2025, "arxiv": "2503.09642"},
 "weights": {"urls": ["https://huggingface.co/hpcai-tech/Open-Sora-v2-Video-DC-AE"], "hf_api_evidence": ["opensora_Open-Sora-v2-Video-DC-AE_hfapi_blobs.json", "opensora_Open-Sora-v2_hfapi_blobs.json"],
             "files_listed": {"F32T4C128_AE.safetensors": 918970214}, "gated": False, "private": False, "note": "Not downloaded."},
 "licence": {"id": "Apache-2.0 (HF card)", "url": "https://huggingface.co/hpcai-tech/Open-Sora-v2-Video-DC-AE", "commercial": "permitted", "non_commercial_only": False,
             "restrictions": "none beyond Apache-2.0", "gating": "none", "quote_ids": ["lic_card2"]},
 "architecture": {"type": "deep-compression video autoencoder (no KL), trained from scratch", "params": "not stated in saved sources (file 919 MB)",
   "representation": "latents at 4x32x32 compression; 128 or 256 channels trained (released file name F32T4C128 suggests 128 channels -- inferred from the file name only)", "input_resolution": "trained on 256px 1:1 clips; generation up to 768px",
   "frames_per_clip": "32-frame training clips", "temporal_compression": "4x", "spatial_compression": "32x32", "quote_ids": ["arch_dcae", "arch_train"]},
 "pretraining_data": {"summary": "AE training data described only as 32-frame 256px 1:1 videos; the paper's data section describes a filtering pyramid and statistics but does not name sources.",
   "form": "described only", "quote_ids": ["arch_train", "data_pyramid"]},
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "Search of saved paper HTML and card for medic|surg|endoscop|laparoscop|clinic|hospital|health: no hits."},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "undisclosed", "basis": "sources not named. Context: released 2025-03, before the OPARA issue 2026-04-29.", "quote_ids": ["data_pyramid"]},
 "eligibility": {
   "C1_open_weights": {"status": "PASS", "basis": "HF API lists F32T4C128_AE.safetensors, gated=False"},
   "C2_licence_research_use": {"status": "PASS", "basis": "Apache-2.0"},
   "C3_domain_secondary": {"status": "PASS", "basis": "video autoencoder of a text/image-to-video model"},
   "C4_documented_pretraining_data": {"status": "FAIL", "basis": "no datasets or named sources for the Open-Sora 2.0 / DC-AE training video"},
   "eligible": "NO (fails C4)"
 },
 "quotes": [
  {"id": "lic_card2", "quote": "license: apache-2.0", "source_file": C2},
  {"id": "arch_dcae", "quote": "our Video DC-AE with a 4 × 32 × 32 4\\times 32\\times 32 compression ratio and a patch size of 1 × 1 × 1 1\\times 1\\times 1 enables training on 32-frame, 256px videos with a latent shape of 8 × 8 × 8 8\\times 8\\times 8 .", "source_file": P2},
  {"id": "arch_train", "quote": "We train each AE model on 8 GPUs with a local batch size of 1. Our training data consists of 32 frames of 256px videos at an aspect ratio of 1:1.", "source_file": P2},
  {"id": "data_pyramid", "quote": "2 Data Our goal for data is to build a hierarchical data pyramid, catering to the requirement of the progressive training process.", "source_file": P2}
 ]
}
save_record(recB)
