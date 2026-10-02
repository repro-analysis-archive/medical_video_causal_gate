import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "allegro_rhymes-ai__Allegro_hfapi.json"; CARD = "allegro_Allegro_README.md"; VC = "allegro_Allegro_vae_config.json"
GH = "allegro_github_README.md"; LIC = "allegro_github_LICENSE.txt"; P = "allegro_arxiv_2410.15458_fulltext.txt"
DATA_FILES = [P, CARD, GH]

rec = {
 "id": "09_allegro_vae",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "name": "Allegro VideoVAE (Rhymes AI, rhymes-ai/Allegro vae/; AutoencoderKLAllegro, 4x8x8, 4 channels)",
 "version": "rhymes-ai/Allegro vae/diffusion_pytorch_model.safetensors (HF repo sha c1b9207bb5cb79e2aa08f3d139c17d26c0de55b6, created 2024-10-16); paper arXiv 2410.15458v1",
 "paper": {"title": "Allegro: Open the Black Box of Commercial-Level Video Generation Model", "year": 2024, "arxiv": "2410.15458", "version_read": "arXiv HTML v1 (2024-10-20)"},
 "weights_location": {
  "urls": ["https://huggingface.co/rhymes-ai/Allegro/tree/main/vae"],
  "files_listed": {"vae/diffusion_pytorch_model.safetensors": 699904972, "vae/config.json": 803},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; nothing downloaded",
  "quote_ids": ["w_file", "w_gated", "w_card"]
 },
 "licence": {
  "id": "Apache-2.0",
  "url": "https://huggingface.co/rhymes-ai/Allegro ; https://github.com/rhymes-ai/Allegro/blob/main/LICENSE.txt",
  "commercial": "permitted", "non_commercial_only": False,
  "restrictions": "none beyond Apache-2.0 (spatial layers initialised from the Playground v2.5 image VAE, whose upstream licence is not audited here)",
  "gating": "none",
  "quote_ids": ["lic_card", "lic_paper", "lic_text"]
 },
 "domain": {
  "value": "video VAE of the Allegro text-to-video diffusion model (Playground v2.5 image VAE + added temporal 3D-CNN layers); trained on 54.7K videos and 3.73M images from the authors' filtered general text-video dataset",
  "quote_ids": ["dom_card", "arch_playground", "data_vae"]
 },
 "architecture": {
  "type": "image VAE (Playground v2.5) inflated with 1D/3D temporal CNN layers; non-causal strided temporal downsampling (stride 2, twice); KL latent",
  "representation": "encoder latents: 4 channels per latent voxel (4 frames x 8 x 8 pixels)"
 },
 "pretraining_data": {
  "summary": "Allegro dataset: 106M images + 48M videos built from 'a large pool of raw images and videos' by a filtering pipeline (>= 360p, >= 2 s, >= 23 FPS, scene split, aesthetics, artifacts, captioning); VAE trained on 54.7K videos and 3.73M images (shortest side > 720 px) from this filtered dataset. Sources of the raw pool are not named; WebVid, Panda-70M, HD-VILA, HD-VG and OpenVid-1M are named only as existing public datasets that 'have provided solid foundation for data sourcing' in the field, not as the Allegro training sources.",
  "form": "described only (pipeline and counts; no source list)"
 },
 "pretraining_data_quote": {"quote_ids": ["data_total", "data_vae", "data_pool", "data_public_context", "data_fps30"]},
 "medical_video_in_data": {
  "answer": "NOT MENTIONED",
  "basis": "Automated search of the saved paper text, HF card and GitHub README for medical|surgical|surgery|endoscop|laparoscop|clinical|health|hospital: no hits.",
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}
 },
 "appendix300_possible": {
  "answer": "UNKNOWN", "basis_class": "undisclosed",
  "basis": "raw pool sources undisclosed. Timing: released 2024-10-16/20, before the OPARA issue 2026-04-29; prior circulation of the source recordings not documented.",
  "quote_ids": ["data_pool"]
 },
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "undisclosed",
  "basis": "no source list for the 48M videos / 54.7K VAE videos exists (only a filtering pipeline and counts), so the Appendix300 source recordings cannot be excluded.",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_pool", "data_vae"]
 },
 "input": {
  "frame_size": {"value": "VAE trained at 256x256 crops (stage 1: 16-frame videos + images; stage 2: 24-frame videos); inference tiled with 256 or 320 px tiles; model generates 720x1280", "quote_ids": ["in_stage1", "in_stage2", "in_tile", "in_card_res"]},
  "frame_rate_or_sampling": {"value": "VAE training: frames sampled with a random interval from {1, 3, 5, 10}; data clips re-encoded at 30 FPS; DiT trained/generates at 15 FPS", "quote_ids": ["in_interval", "data_fps30", "in_15fps"]},
  "clip_length_frames": {"value": "VAE training 16 frames (stage 1) and 24 frames (stage 2); encoder tile 24 frames; generation 88 frames", "quote_ids": ["in_stage1", "in_stage2", "in_tile", "in_card_frames"]},
  "temporal_compression": {"value": "4x (non-causal strided conv; T' = T/4)", "quote_ids": ["arch_latent_paper", "arch_tcomp"]},
  "spatial_compression": {"value": "8x8", "quote_ids": ["arch_latent_paper"]}
 },
 "embedding_dim": {
  "value": "4 latent channels x 22 x 90 x 160 = 1,267,200 values for an 88-frame 720x1280 clip; generally 4 x T/4 x H/8 x W/8 (per 24-frame encoder tile: 4 x 6 x p/8 x p/8)",
  "derivation": "C_l = 4, S_T x S_H x S_W = 4 x 8 x 8, latent shape T/S_T x C_l x H/S_H x W/S_W; reference input = the model's 88 frames at 720x1280",
  "quote_ids": ["arch_latent_paper", "arch_cfg_latent", "in_card_frames", "in_card_res"]
 },
 "params": {
  "value": "174.96M (~175M) for the whole VideoVAE (encoder + decoder); encoder-only count not documented",
  "scope": "whole autoencoder (encoder + decoder)",
  "quote_ids": ["arch_params", "arch_params_card"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs/MACs statement in the saved paper text, card or config (FLOP|MAC hits are only commercial-system names)",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists vae/diffusion_pytorch_model.safetensors, gated=False", "quote_ids": ["w_file", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "Apache-2.0, 'free for both academic and commercial use'", "quote_ids": ["lic_card", "lic_paper", "lic_text"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE of a general text-to-video diffusion model, trained on general video", "quote_ids": ["dom_card", "data_vae"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": "the training videos are described by pipeline and counts only ('a large pool of raw images and videos'); the named public datasets appear only as background on the field, not as Allegro's sources -> no datasets or named sources listed (borderline wording, recorded)", "quote_ids": ["data_pool", "data_total", "data_public_context"]},
  "eligible": "NO (fails C4)"
 },
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"vae/diffusion_pytorch_model.safetensors\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "w_card", "quote": "**Open Source**: Full [model weights](https://huggingface.co/rhymes-ai/Allegro) and [code](https://github.com/rhymes-ai/Allegro) available to the community, Apache 2.0!", "source_file": CARD},
  {"id": "lic_card", "quote": "license: apache-2.0", "source_file": CARD},
  {"id": "lic_paper", "quote": "We release Allegro under the Apache 2.0 license, free for both academic and commercial use.", "source_file": P},
  {"id": "lic_text", "quote": "Apache License Version 2.0, January 2004", "source_file": LIC},
  {"id": "dom_card", "quote": "**Versatile Content Creation**: Capable of generating a wide range of content, from close-ups of humans and animals to diverse dynamic scenes.", "source_file": CARD},
  {"id": "arch_playground", "quote": "We first adopt the architecture and weights of the image VAE from Playground v2.5 ( Li et al., 2024a ) to model spatial information.", "source_file": P},
  {"id": "arch_params", "quote": "After incorporating these temporal layers, the parameter count of our VideoVAE has reached 174.96M.", "source_file": P},
  {"id": "arch_params_card", "quote": "**Small and Efficient**: Features a 175M parameter VideoVAE and a 2.8B parameter VideoDiT model.", "source_file": CARD},
  {"id": "arch_latent_paper", "quote": "We continue to use the latent channel C l = 4 C_{l}=4 from image VAE without any expansion and have compression stride S T × S H × S W = 4 × 8 × 8 S_{T}\\times S_{H}\\times S_{W}=4\\times 8\\times 8 in temporal, height and width dimension respectively.", "source_file": P},
  {"id": "arch_cfg_latent", "quote": "\"latent_channels\": 4,", "source_file": VC},
  {"id": "arch_tcomp", "quote": "\"temporal_compression_ratio\": 4,", "source_file": VC},
  {"id": "arch_class", "quote": "\"_class_name\": \"AutoencoderKLAllegro\",", "source_file": VC},
  {"id": "in_stage1", "quote": "utilizing a batch composition of one 16-frame video and four images, all with a spatial resolution of 256 × 256 256\\times 256 .", "source_file": P},
  {"id": "in_stage2", "quote": "fine-tune the temporal layers using 24-frame 256 × 256 256\\times 256 resolution videos", "source_file": P},
  {"id": "in_tile", "quote": "In practice, we employ a tile size of 24 × p × p 24\\times p\\times p (time, height, width) in Encoder", "source_file": P},
  {"id": "in_interval", "quote": "For temporal data augmentation in videos, we randomly choose a sampling interval from the set [1, 3, 5, 10] to sample frames evenly across video clips.", "source_file": P},
  {"id": "in_15fps", "quote": "All videos across the three sub-stages are sampled at 15 FPS, enabling the model to generate 6-second videos at 720 × 1280 720\\times 1280 resolution.", "source_file": P},
  {"id": "in_card_res", "quote": "**High-Quality Output**: Generate detailed 6-second videos at 15 FPS with 720x1280 resolution", "source_file": CARD},
  {"id": "in_card_frames", "quote": "Context length is 79.2K, equivalent to 88 frames.", "source_file": CARD},
  {"id": "data_total", "quote": "With this pipeline, we build our dataset containing 106M images and 48M videos, with highly associated text captions.", "source_file": P},
  {"id": "data_vae", "quote": "We ultimately select 54.7K videos and 3.73M images from our filtered dataset to train VideoVAE.", "source_file": P},
  {"id": "data_pool", "quote": "Figure 2: Allegro data filtering pipeline. A large pool of raw images and videos is fed into this pipeline to get a training set of high visual quality with associated text captions.", "source_file": P},
  {"id": "data_public_context", "quote": "Existing publicly available datasets, such as WebVid ( Bain et al., 2021 ) , Panda-70M ( Chen et al., 2024b ) , HD-VILA ( Xue et al., 2022 ) , HD-VG ( Wang et al., 2023 ) and OpenVid-1M ( Nan et al., 2024 ) , have provided solid foundation for data sourcing and acquisition, offering diverse and extensive video data.", "source_file": P},
  {"id": "data_fps30", "quote": "To facilitate the usability of the data, all video clips are uniformly re-encoded using H.264, and the frame rate is fixed at 30 FPS.", "source_file": P}
 ]
}
save_record(rec)
