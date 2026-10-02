import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_lib import save_record
C1 = "wan_Wan2.1-T2V-1.3B_README.md"; C2 = "wan_Wan2.2-TI2V-5B_README.md"; P = "wan_arxiv_2503.20314_fulltext.html"; L = "wan_Wan2.1-T2V-1.3B_LICENSE.txt"
rec = {
 "id": "05_wan_vae",
 "name": "Wan-VAE (Wan2.1_VAE.pth, 4x8x8) and Wan2.2-VAE (Wan2.2_VAE.pth, 4x16x16)",
 "paper": {"title": "Wan: Open and Advanced Large-Scale Video Generative Models", "year": 2025, "arxiv": "2503.20314",
           "note": "Wan2.2-VAE is documented only in the Wan2.2 model card (no separate paper found in this audit)"},
 "weights": {
   "urls": ["https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B (Wan2.1_VAE.pth)", "https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B (Wan2.2_VAE.pth)"],
   "hf_api_evidence": ["wan_Wan2.1-T2V-1.3B_hfapi_blobs.json", "wan_Wan2.2-TI2V-5B_hfapi_blobs.json"],
   "files_listed": {"Wan2.1_VAE.pth": 507609880, "Wan2.2_VAE.pth": 2818839170},
   "gated": False, "private": False, "note": "Not downloaded."
 },
 "licence": {
   "id": "Apache-2.0", "url": "https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B/blob/main/LICENSE.txt",
   "commercial": "permitted", "non_commercial_only": False,
   "restrictions": "card adds a usage statement (no sharing unlawful/harmful/misinformation content); no gating",
   "gating": "none", "quote_ids": ["lic_card21", "lic_text"]
 },
 "architecture": {
   "type": "3D causal VAE (inflated from a 2D image VAE), feature-cache chunked causal encoding of arbitrary-length video",
   "params": "Wan2.1-VAE 127M (paper); Wan2.2-VAE not stated (file 2.82 GB)",
   "representation": "VAE encoder latents: Wan2.1 latent dim 16 at 4x8x8 compression; Wan2.2-VAE 4x16x16 (latent dim not quoted from saved sources)",
   "input_resolution": "Wan2.1: 480P (832x480) recommended for 1.3B, VAE encodes up to 1080P; Wan2.2-TI2V-5B: 720P (1280x704)",
   "frames_per_clip": "arbitrary length (causal chunks, 1 + 4k frames); generation ~5 s",
   "temporal_compression": "4x", "spatial_compression": "8x8 (Wan2.1) / 16x16 (Wan2.2)",
   "quote_ids": ["arch_448", "arch_127m", "arch_22", "arch_latent16", "arch_train", "arch_res21"]
 },
 "pretraining_data": {
   "summary": "Candidate dataset 'sourced from both internal copyrighted sources and publicly accessible data', billions of images and videos, curated by a four-step cleaning pipeline; VAE: 2D image VAE on image data, then 128x128 5-frame videos, then high-quality videos. Wan2.2: +65.6% images, +83.2% videos vs Wan2.1. No datasets named.",
   "form": "described only",
   "quote_ids": ["data_src", "data_billions", "arch_train", "data_22"]
 },
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "Search of saved paper HTML for medic|surg|endoscop|laparoscop|clinic|hospital|health: hits only 'healthy nodes', a reference title, and the limitations sentence that performance 'in specific localized scenarios, such as education and medicine, may be insufficient' (no data statement).", "quote_ids": ["lim_medicine"]},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "undisclosed", "basis": "internal copyrighted + publicly accessible sources not itemised. Context: Wan2.1 2025-02/03, Wan2.2 2025-07, both before the OPARA issue 2026-04-29.", "quote_ids": ["data_src"]},
 "eligibility": {
   "C1_open_weights": {"status": "PASS", "basis": "HF API lists Wan2.1_VAE.pth / Wan2.2_VAE.pth, gated=False"},
   "C2_licence_research_use": {"status": "PASS", "basis": "Apache-2.0"},
   "C3_domain_secondary": {"status": "PASS", "basis": "video VAE of a text/image-to-video diffusion model on general video"},
   "C4_documented_pretraining_data": {"status": "FAIL", "basis": "sources described only as 'internal copyrighted sources and publicly accessible data'"},
   "eligible": "NO (fails C4)"
 },
 "quotes": [
  {"id": "lic_card21", "quote": "The models in this repository are licensed under the Apache 2.0 License.", "source_file": C1},
  {"id": "lic_text", "quote": "Apache License", "source_file": L},
  {"id": "arch_448", "quote": "Wan -VAE can compress the spatio-temporal dimension of a video by 4 × 8 × 8 4\\times 8\\times 8 times.", "source_file": P},
  {"id": "arch_127m", "quote": "Wan -VAE achieves a compact model size of only 127M parameters.", "source_file": P},
  {"id": "arch_latent16", "quote": "adopt the same compression rate and latent feature dimension as our approach, i.e., a compression rate of 4 × 8 × 8 4\\times 8\\times 8 with a latent dimension of 16.", "source_file": P},
  {"id": "arch_22", "quote": "It is supported by a high-compression Wan2.2-VAE, which achieves a $T\\times H\\times W$ compression ratio of $4\\times16\\times16$, increasing the overall compression rate to 64 while maintaining high-quality video reconstruction.", "source_file": C2},
  {"id": "arch_train", "quote": "First, we construct a 2D image VAE with the same structure and train it on image data. Then, we inflate the well-trained 2D image VAE into a 3D causal Wan -VAE to provide an initial spatial compression prior, which drastically improves the training speed compared to training a video VAE from scratch. At this stage, Wan -VAE is trained on the low-resolution (128 × \\times 128) and small frame number (5-frame) videos to accelerate convergence speed.", "source_file": P},
  {"id": "arch_res21", "quote": "For optimal performance, we recommend using 480P resolution.", "source_file": C1},
  {"id": "data_src", "quote": "3.1 Pre-training Data We curated and deduplicated a candidate dataset sourced from both internal copyrighted sources and publicly accessible data.", "source_file": P},
  {"id": "data_billions", "quote": "Following these principles, we curated a dataset comprising billions of videos and images.", "source_file": P},
  {"id": "data_22", "quote": "Compared to Wan2.1, Wan2.2 is trained on a significantly larger data, with +65.6% more images and +83.2% more videos.", "source_file": C2},
  {"id": "lim_medicine", "quote": "As a foundational video model, we are committed to enhancing Wan ’s general capabilities, yet performance in specific localized scenarios, such as education and medicine, may be insufficient.", "source_file": P}
 ]
}
save_record(rec)
