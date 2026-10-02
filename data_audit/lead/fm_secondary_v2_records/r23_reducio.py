import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "reducio_microsoft__Reducio-VAE_hfapi.json"; HF = "reducio_hf_README.md"; C = "reducio_hf_config.json"
P = "reducio_arxiv_2411.13552_fulltext.txt"
DATA_FILES = [P, HF]

rec = {
 "id": "23_reducio_vae",
 "name": "Reducio-VAE (microsoft/Reducio-VAE; content-frame-conditioned 3D VAE of Reducio-DiT)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "microsoft/Reducio-VAE reducio-ft4-fs32-attn23.ckpt (4x temporal, 32x32 spatial) and reducio-ft2-fs32-attn23.ckpt (2x temporal) (HF repo created 2024-11-08); paper arXiv:2411.13552",
 "paper": {"title": "REDUCIO! Generating 1K Video within 16 Seconds using Extremely Compressed Motion Latents", "year": 2024, "arxiv": "2411.13552"},
 "weights_location": {
  "urls": ["https://huggingface.co/microsoft/Reducio-VAE"],
  "files_listed": {"reducio-ft4-fs32-attn23.ckpt": 1748598662, "reducio-ft2-fs32-attn23.ckpt": 1729733518, "config.json": 1024},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; nothing downloaded",
  "quote_ids": ["w_ft4", "w_ft2", "w_gated"]
 },
 "licence": {"id": "MIT (HF card)", "url": "https://huggingface.co/microsoft/Reducio-VAE", "commercial": "permitted", "non_commercial_only": False,
             "restrictions": "none beyond MIT (SD-VAE initialisation upstream licence not audited)", "gating": "none", "quote_ids": ["lic_card"]},
 "domain": {"value": "3D VAE of the text-image-to-video diffusion model Reducio-DiT; encodes a video into an extremely compressed motion latent conditioned on a content frame; trained on Pexels stock video", "quote_ids": ["dom_card", "dom_dit", "data_pexels"]},
 "architecture": {"type": "3D-conv VAE (initialised from SD-VAE weights) + 2D content-frame encoder; decoder fuses middle-frame content features by cross-attention",
                  "representation": "motion latent z, 16 channels, T/4 x H/32 x W/32 (ft4) or T/2 x H/32 x W/32 (ft2); reconstruction additionally needs the content (middle) frame"},
 "pretraining_data": {"summary": "400K videos collected from Pexels, 256x256 at 16 FPS (paper 4.1); initialised from SD-VAE weights. (Reducio-DiT additionally uses an internal 5M-video set; the VAE statement names Pexels only.)",
                      "form": "named source (Pexels)"},
 "pretraining_data_quote": {"quote_ids": ["data_pexels", "data_init"]},
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "Pexels stock footage is open-ended; term search of the paper/card finds no medical/surgical data statement",
                           "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "named_open_web_sources",
  "basis": "VAE data = videos collected from Pexels (named, open-ended stock-footage site), so the documentation does not allow the Appendix300 source recordings to be excluded. Timing: 2024-11, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_pexels"]},
 "appendix300_check": {
  "answer": "UNKNOWN", "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "named_open_web_sources", "basis": "400K Pexels videos",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_pexels"]
 },
 "input": {
  "frame_size": {"value": "256x256 training; larger inputs encoded with overlapping spatial tiles", "quote_ids": ["data_pexels", "in_res", "in_tile"]},
  "frame_rate_or_sampling": {"value": "16 FPS (training)", "quote_ids": ["data_pexels"]},
  "clip_length_frames": {"value": "16 (config temp_res 16; z-shape stated for 256^2 videos)", "quote_ids": ["in_temp", "in_zshape"]},
  "temporal_compression": {"value": "4x (ft4 checkpoint) or 2x (ft2 checkpoint)", "quote_ids": ["in_card_factor", "in_zshape", "w_ft4", "w_ft2"]},
  "spatial_compression": {"value": "32x32", "quote_ids": ["in_card_factor", "in_card_row"]}
 },
 "embedding_dim": {"value": "16 channels x T/4 x H/32 x W/32: 16 x 256 x 256 clip -> 4 x 8 x 8 x 16 = 4,096 values (ft4) or 8 x 8 x 8 x 16 = 8,192 (ft2)",
                   "derivation": "paper Table 9 z-shape on 256^2 videos; z_channels / embed_dim 16 in config", "quote_ids": ["in_zshape", "in_z", "in_card_row"]},
 "params": {"value": "437M for the whole Reducio-VAE with attention fusion (paper Table 6); encoder-only not documented", "scope": "whole autoencoder incl. content-frame branch", "quote_ids": ["p_437"]},
 "flops_per_input_if_documented": None,
 "flops_note": "no VAE FLOPs per input in the saved paper/card",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists both .ckpt files, gated=False", "quote_ids": ["w_ft4", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "MIT", "quote_ids": ["lic_card"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE of a video diffusion model trained on general stock video; caveat: decoding needs a content frame, the encoder latent is motion-only", "quote_ids": ["dom_card", "dom_dit"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "paper names the VAE training source (400K videos collected from Pexels)", "quote_ids": ["data_pexels"]},
  "eligible": "YES (all four criteria PASS; Appendix300 UNKNOWN; caveat: content-frame-conditioned motion latent)"
 },
 "quotes": [
  {"id": "w_ft4", "quote": "\"rfilename\": \"reducio-ft4-fs32-attn23.ckpt\",", "source_file": API},
  {"id": "w_ft2", "quote": "\"rfilename\": \"reducio-ft2-fs32-attn23.ckpt\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "lic_card", "quote": "license: mit", "source_file": HF},
  {"id": "dom_card", "quote": "This model is a 3D VAE that encodes video into a compact latent space conditioned on a content frame.", "source_file": HF},
  {"id": "dom_dit", "quote": "It is part of the [Reducio-DiT](https://arxiv.org/abs/2411.13552), which is a video generation method.", "source_file": HF},
  {"id": "data_pexels", "quote": "Our Reducio -VAE is trained on a 400K video dataset collected from Pexels * * * https://www.pexels.com/ . Pexels contains a large number of free and high-quality stock videos, where each video is accompanied by a short text description. We train Reducio -VAE from scratch on 256 × 256 256\\times 256 videos with 16 FPS.", "source_file": P},
  {"id": "data_init", "quote": "While initializing the 2D encoder and the 3D VAE with SD-VAE pre-trained weights accelerates convergence, we find that freezing the 2D encoder leads to worse performance than training the full parameters.", "source_file": P},
  {"id": "in_card_factor", "quote": r"It compresses a video by a factor of \\(\frac{T}{4}\times\frac{H}{32}\times\frac{W}{32}\\), enabling 4096x downsampling.", "source_file": HF},
  {"id": "in_card_row", "quote": r"|Reducio-VAE|4\*32\*32|16|35.88|0.94|0.05|17.88|65.17|", "source_file": HF},
  {"id": "in_zshape", "quote": "Table 9: Hyperparameters for Reducio -VAE Reducio -VAE z z -shape † † † on 256 2 256^{2} videos 4 × 8 × 8 × 16 4\\times 8\\times 8\\times 16 8 × 8 × 8 × 16 8\\times 8\\times 8\\times 16", "source_file": P},
  {"id": "in_tile", "quote": "During inference, We split videos with a resolution over 256 × 256 256\\times 256 into overlapping spatial tiles", "source_file": P},
  {"id": "in_res", "quote": "\"resolution\": 256,", "source_file": C},
  {"id": "in_temp", "quote": "\"temp_res\": 16,", "source_file": C},
  {"id": "in_z", "quote": "\"embed_dim\": 16,", "source_file": C},
  {"id": "in_content", "quote": "Generally, we choose the middle frame V T / 2 V_{T/2} as the content guidance", "source_file": P},
  {"id": "p_437", "quote": "attention 35.88 0.94 437M", "source_file": P}
 ]
}
save_record(rec)
