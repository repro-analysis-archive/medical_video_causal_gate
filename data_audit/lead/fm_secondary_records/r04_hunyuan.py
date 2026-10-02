import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_lib import save_record
C = "hunyuan_README.md"; L = "hunyuan_LICENSE"; V = "hunyuan_hunyuan-video-t2v-720p_vae_config.json"; P = "hunyuan_arxiv_2412.03603_fulltext.html"
rec = {
 "id": "04_hunyuanvideo_vae",
 "name": "HunyuanVideo Causal 3D VAE (AutoencoderKLCausal3D; tencent/HunyuanVideo hunyuan-video-t2v-720p/vae)",
 "paper": {"title": "HunyuanVideo: A Systematic Framework For Large Video Generative Models", "year": 2024, "arxiv": "2412.03603"},
 "weights": {
   "urls": ["https://huggingface.co/tencent/HunyuanVideo/tree/main/hunyuan-video-t2v-720p/vae"],
   "hf_api_evidence": ["hunyuan_HunyuanVideo_hfapi_blobs.json"],
   "files_listed": {"hunyuan-video-t2v-720p/vae/pytorch_model.pt": 986000558},
   "gated": False, "private": False, "note": "Not downloaded."
 },
 "licence": {
   "id": "Tencent Hunyuan Community License Agreement (HF license: other / tencent-hunyuan-community), with Acceptable Use Policy (Exhibit A, last modified 2024-11-05)",
   "url": "https://huggingface.co/tencent/HunyuanVideo/blob/main/LICENSE",
   "commercial": "permitted below 100M monthly active users", "non_commercial_only": False,
   "restrictions": "TERRITORY: licence does not apply in the EU, UK and South Korea, and use/display of works or outputs outside the Territory is unlicensed (relevant if any EU-based collaborator, e.g. German data holders, would run it); AUP bans high-stakes automated decisions in medicine/health and unlicensed medical practice",
   "gating": "none (HF gated=False)",
   "quote_ids": ["lic_territory", "lic_grant", "lic_outside", "lic_aup_med"]
 },
 "architecture": {
   "type": "Causal 3D VAE (CausalConv3D), trained from scratch on video:image 4:1",
   "params": "not stated in saved sources; VAE pytorch_model.pt 986 MB (~246M params if fp32, inferred)",
   "representation": "VAE encoder latents, 16 channels, (T/4+1) x H/8 x W/8",
   "input_resolution": "720x1280 (also 544x960) for generation",
   "frames_per_clip": "129 frames (generation default)",
   "temporal_compression": "4x", "spatial_compression": "8x8",
   "quote_ids": ["arch_card", "arch_vae_class", "arch_tcomp", "arch_res", "arch_scratch"]
 },
 "pretraining_data": {
   "summary": "Internal raw data pool spanning people, animals, plants, landscapes, vehicles, objects, buildings, animation; GDPR-governed acquisition; no datasets or providers named.",
   "form": "described only",
   "quote_ids": ["data_pool", "data_gdpr"]
 },
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "Search of saved paper HTML for medic|surg|endoscop|laparoscop|clinic|hospital|health: only 'healthy nodes' (training infrastructure). Listed domains contain no medical domain."},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "undisclosed", "basis": "data pool sources undisclosed. Context: paper v1 2024-12-03, weights 2024-12, before the OPARA issue 2026-04-29.", "quote_ids": ["data_pool"]},
 "eligibility": {
   "C1_open_weights": {"status": "PASS", "basis": "HF API lists vae/pytorch_model.pt, gated=False"},
   "C2_licence_research_use": {"status": "PASS", "basis": "community licence grants use in the Territory (worldwide excl. EU/UK/South Korea); research in Japan is inside the Territory -- flag: not usable by EU/UK-based parties"},
   "C3_domain_secondary": {"status": "PASS", "basis": "3D video VAE of a text-to-video diffusion model on general video"},
   "C4_documented_pretraining_data": {"status": "FAIL", "basis": "only domain categories of an internal data pool; no datasets or named sources"},
   "eligible": "NO (fails C4; licence territory flag)"
 },
 "quotes": [
  {"id": "lic_territory", "quote": "THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA AND IS EXPRESSLY LIMITED TO THE TERRITORY, AS DEFINED BELOW.", "source_file": L},
  {"id": "lic_grant", "quote": "We grant You, for the Territory only, a non-exclusive, non-transferable and royalty-free limited license under Tencent’s intellectual property or other rights owned by Us embodied in or utilized by the Materials to use, reproduce, distribute, create derivative works of (including Model Derivatives), and make modifications to the Materials, only in accordance with the terms of this Agreement and the Acceptable Use Policy", "source_file": L},
  {"id": "lic_outside", "quote": "You must not use, reproduce, modify, distribute, or display the Tencent Hunyuan Works, Output or results of the Tencent Hunyuan Works outside the Territory.", "source_file": L},
  {"id": "lic_aup_med", "quote": "To make high-stakes automated decisions in domains that affect an individual’s safety, rights or wellbeing (e.g., law enforcement, migration, medicine/health, management of critical infrastructure, safety components of products, essential services, credit, employment, housing, education, social scoring, or insurance);", "source_file": L},
  {"id": "arch_card", "quote": "HunyuanVideo trains a 3D VAE with CausalConv3D to compress pixel-space videos and images into a compact latent space. We set the compression ratios of video length, space, and channel to 4, 8, and 16 respectively.", "source_file": C},
  {"id": "arch_vae_class", "quote": "\"_class_name\": \"AutoencoderKLCausal3D\",", "source_file": V},
  {"id": "arch_tcomp", "quote": "\"time_compression_ratio\": 4,", "source_file": V},
  {"id": "arch_res", "quote": "* **Minimum**: The minimum GPU memory required is 60GB for 720px1280px129f and 45G for 544px960px129f.", "source_file": C},
  {"id": "arch_scratch", "quote": "we do not rely on a pre-trained image VAE for parameter initialization; instead, we train our model from scratch. To balance the reconstruction quality of videos and images, we mix video and image data at a ratio of 4 : 1", "source_file": P},
  {"id": "data_pool", "quote": "Our raw data pool initially comprised videos spanning a wide range of domains including people, animals, plants, landscapes, vehicles, objects, buildings, and animation.", "source_file": P},
  {"id": "data_gdpr", "quote": "Our data acquisition process is rigorously governed by the principles outlined in the General Data Protection Regulation (GDPR) [ 39 ] framework.", "source_file": P}
 ]
}
save_record(rec)
