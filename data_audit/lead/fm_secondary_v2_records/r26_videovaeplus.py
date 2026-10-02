import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

RM = "videovaeplus_github_README.md"; LIC = "videovaeplus_github_LICENSE.txt"; P = "videovaeplus_arxiv_2412.17805_fulltext.txt"
G4 = "videovaeplus_sota-4z_gdrive_view.txt"; G16 = "videovaeplus_sota-16z_gdrive_view.txt"
G4T = "videovaeplus_sota-4z-text_gdrive_view.txt"; G16T = "videovaeplus_sota-16z-text_gdrive_view.txt"
DATA_FILES = [P, RM]

rec = {
 "id": "26_videovae_plus",
 "name": "VideoVAE+ (HKUST VideoVerses/VideoVAEPlus; sota-4z, sota-16z, and text-guided variants)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "GitHub VideoVerses/VideoVAEPlus README 'Pretrained Models': sota-4z (sota-4-4z.ckpt), sota-4z-text (sota-4-4z-text-new.ckpt), sota-16z (sota-4-16z.ckpt), sota-16z-text (sota-4-16z-text.ckpt) on Google Drive; paper arXiv:2412.17805v1",
 "paper": {"title": "Large Motion Video Autoencoding with Cross-modal Video VAE", "year": 2024, "arxiv": "2412.17805"},
 "weights_location": {
  "urls": ["https://drive.google.com/file/d/1WEKBdRFjEUxwcBgX_thckXklD8s6dDTj/view", "https://drive.google.com/file/d/13v2Pq6dG1jo7RNImxNOXr9-WizgMiJ7M/view",
           "https://drive.google.com/file/d/1QfqrKIWu5zG10U-xRgeF8Dhp__njC8OH/view", "https://drive.google.com/file/d/1iYCAtmdaOX0V41p0vbt_6g8kRS1EK56p/view"],
  "files_listed": {"sota-4-4z.ckpt": None, "sota-4-16z.ckpt": None, "sota-4-4z-text-new.ckpt": None, "sota-4-16z-text.ckpt": None},
  "gated": False, "private": False,
  "verified_how": "the four public Google Drive view pages linked from the official README resolve without login (HTTP 200) and name the files; sizes not shown; nothing downloaded",
  "quote_ids": ["w_readme16", "w_view4", "w_view16", "w_view4t", "w_view16t"]
 },
 "licence": {
  "id": "CC BY-NC-ND 4.0 (repository LICENSE; README 'Please follow [CC-BY-NC-ND]')",
  "url": "https://github.com/VideoVerses/VideoVAEPlus/blob/main/LICENSE",
  "commercial": "not permitted", "non_commercial_only": True,
  "restrictions": "NonCommercial; NoDerivatives (sharing of adapted material not licensed); attribution",
  "gating": "none", "quote_ids": ["lic_readme", "lic_text"]
 },
 "domain": {"value": "video VAE (temporal-aware spatial compression + lightweight temporal autoencoder, optional text guidance) for latent video generation; trained on general text-video data", "quote_ids": ["dom_readme", "data_sets"]},
 "architecture": {"type": "sequential spatiotemporal KL video VAE initialised from SD-1.4 (4-ch) / SD-3.5 (16-ch) image VAEs, with cross-modal (text) attention option",
                  "representation": "innermost latent Z2, 4 or 16 channels, T/4 x H/8 x W/8"},
 "pretraining_data": {"summary": "Panda2M and MMTrailer (public) + a private text-video dataset with over 6M pairs; joint image-video training uses frames from Panda2M and the private set. Initialised from SD-1.4 / SD-3.5 VAEs.",
                      "form": "partly named (Panda2M, MMTrailer) + unnamed private dataset"},
 "pretraining_data_quote": {"quote_ids": ["data_sets", "data_joint", "data_init"]},
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "private dataset undisclosed; Panda2M/MMTrailer are open-web (YouTube-derived) sets; automated term search below",
                           "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "undisclosed",
  "basis": "a private 6M-pair text-video dataset is part of the training data (undisclosed), and Panda2M / MMTrailer are YouTube-derived open-ended sets. Timing: 2024-12, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_sets"]},
 "appendix300_check": {
  "answer": "UNKNOWN", "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "undisclosed", "basis": "private dataset + open-web sets",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_sets"]
 },
 "input": {
  "frame_size": {"value": "evaluation 256x256 (WebVid) and 640x864 (Inter4K); README inference example 720x1280 (training resolution not stated)", "quote_ids": ["in_test", "in_res"]},
  "frame_rate_or_sampling": {"value": "not documented in the saved sources", "quote_ids": []},
  "clip_length_frames": {"value": "evaluation 16-frame clips; inference chunk_size 8 (must be divisible by 4); training clip length not stated", "quote_ids": ["in_test", "in_chunk", "in_chunk_note"]},
  "temporal_compression": {"value": "4x", "quote_ids": ["in_latent", "in_cr4"]},
  "spatial_compression": {"value": "8x8", "quote_ids": ["in_latent", "in_cr4"]}
 },
 "embedding_dim": {"value": "C x T/4 x H/8 x W/8 with C = 4 (sota-4z) or 16 (sota-16z); e.g. 16 x 256 x 256 -> 16 x 4 x 32 x 32 = 65,536 values (16z)",
                   "derivation": "innermost latent dimensions T/4 x H/8 x W/8; channel counts from the README model table", "quote_ids": ["in_latent", "w_readme16", "in_cr4", "in_cr16"]},
 "params": {"value": "not documented in the saved paper/README", "scope": "n/a", "quote_ids": []},
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs statement (searched FLOP)",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "official README links public Google Drive files; view pages resolve without login and name the .ckpt files (same evidence standard as Google-Drive weights in the primary survey)", "quote_ids": ["w_readme16", "w_view16"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "CC BY-NC-ND 4.0 permits non-commercial use (restriction recorded: NC, ND)", "quote_ids": ["lic_readme", "lic_text"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE for latent video generation trained on general video", "quote_ids": ["dom_readme"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": "two public datasets are named, but part of the video training data is 'a private text-video dataset with over 6M pairs' with no named source, so the video pretraining sources are not fully listed (judged FAIL; borderline, see convention question in the fork report)", "quote_ids": ["data_sets"]},
  "eligible": "NO (fails C4: unnamed private dataset in the video training data; borderline)"
 },
 "quotes": [
  {"id": "w_readme16", "quote": "| sota-16z | 16 | [Download](https://drive.google.com/file/d/13v2Pq6dG1jo7RNImxNOXr9-WizgMiJ7M/view?usp=sharing) |", "source_file": RM},
  {"id": "w_view4", "quote": "sota-4-4z.ckpt - Google ドライブ", "source_file": G4},
  {"id": "w_view16", "quote": "sota-4-16z.ckpt - Google ドライブ", "source_file": G16},
  {"id": "w_view4t", "quote": "sota-4-4z-text-new.ckpt", "source_file": G4T},
  {"id": "w_view16t", "quote": "sota-4-16z-text.ckpt", "source_file": G16T},
  {"id": "lic_readme", "quote": "Please follow [CC-BY-NC-ND](./LICENSE).", "source_file": RM},
  {"id": "lic_text", "quote": "Attribution-NonCommercial-NoDerivatives 4.0 International", "source_file": LIC},
  {"id": "dom_readme", "quote": "A state-of-the-art **Video Variational Autoencoder (VAE)** designed for high-fidelity video reconstruction.", "source_file": RM},
  {"id": "data_sets", "quote": "We conduct experiments on three datasets: the public Panda2M [ 10 ] and MMTrailer [ 11 ] datasets, and a private text-video dataset with over 6M pairs.", "source_file": P},
  {"id": "data_joint", "quote": "For each training step, we sample 16 videos from Panda2M and our private text-video dataset, concatenating their frames into a single image batch.", "source_file": P},
  {"id": "data_init", "quote": "We initialize our 4-channel and 16-channel latent Video VAEs from SD-1.4 [ 25 ] and SD-3.5 [ 1 ] , respectively.", "source_file": P},
  {"id": "in_test", "quote": "The WebVid test set contains 1,000 256x256, 16-frame videos from the WebVid dataset [ 2 ] . The Inter4K test set consists of 500 640x864, 16-frame videos from the Inter4K dataset [ 26 ] .", "source_file": P},
  {"id": "in_res", "quote": "--resolution 720 1280", "source_file": RM},
  {"id": "in_chunk", "quote": "--chunk_size 8", "source_file": RM},
  {"id": "in_chunk_note", "quote": "Ensure the `chunk_size` is divisible by 4.", "source_file": RM},
  {"id": "in_latent", "quote": "we only regularize the innermost latent 𝐙 𝟐 \\mathbf{Z_{2}} , with dimensions T 4 × H 8 × W 8 \\frac{T}{4}\\times\\frac{H}{8}\\times\\frac{W}{8}", "source_file": P},
  {"id": "in_cr4", "quote": "Video VAE (Ours) 4x8x8 4 30.3140", "source_file": P},
  {"id": "in_cr16", "quote": "4x8x8 16 31.2545", "source_file": P}
 ]
}
save_record(rec)
