import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "hy15_tencent__HunyuanVideo-1.5_hfapi.json"; HF = "hy15_hf_README.md"; C = "hy15_hf_vae_config.json"
LIC = "hy15_hf_LICENSE.txt"; P = "hy15_arxiv_2511.18870_fulltext.txt"
DATA_FILES = [P, HF]

rec = {
 "id": "25_hunyuanvideo15_vae",
 "name": "HunyuanVideo 1.5 3D causal VAE (tencent/HunyuanVideo-1.5 vae/, AutoencoderKLConv3D, 16x spatial / 4x temporal, 32 channels)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "tencent/HunyuanVideo-1.5 vae/diffusion_pytorch_model.safetensors + vae/config.json (HF repo created 2025-11-18; licence release date 2025-11-21); technical report arXiv:2511.18870",
 "paper": {"title": "HunyuanVideo 1.5 Technical Report", "year": 2025, "arxiv": "2511.18870"},
 "weights_location": {
  "urls": ["https://huggingface.co/tencent/HunyuanVideo-1.5/tree/main/vae"],
  "files_listed": {"vae/diffusion_pytorch_model.safetensors": 5042560980, "vae/config.json": 462},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; nothing downloaded",
  "quote_ids": ["w_file", "w_gated"]
 },
 "licence": {
  "id": "Tencent Hunyuan Community License Agreement (HF license: other / tencent-hunyuan-community; HunyuanVideo 1.5 release date 2025-11-21) with Acceptable Use Policy",
  "url": "https://huggingface.co/tencent/HunyuanVideo-1.5/blob/main/LICENSE",
  "commercial": "permitted under the community licence terms (not audited in detail here)", "non_commercial_only": False,
  "restrictions": "TERRITORY: does not apply in the EU, UK and South Korea (same structure as entry 04); AUP bans high-stakes automated decisions in medicine/health",
  "gating": "none (HF gated=False)", "quote_ids": ["lic_card", "lic_territory", "lic_grant", "lic_aup_med"]
 },
 "domain": {"value": "3D causal video VAE of the text/image-to-video diffusion model HunyuanVideo 1.5; trained on general video", "quote_ids": ["dom_vae", "dom_card"]},
 "architecture": {"type": "causal 3D VAE (config class AutoencoderKLConv3D; report: 'causal 3D transformer architecture'), joint image-video encoding",
                  "representation": "encoder latents, 32 channels, (1 + (T-1)/4) x H/16 x W/16"},
 "pretraining_data": {"summary": "Raw videos 'sourced ... from a variety of channels', >10M hours after deduplication; images: 5B curated from >10B. No datasets or providers named; VAE training data not separately stated.",
                      "form": "described only"},
 "pretraining_data_quote": {"quote_ids": ["data_src", "data_img"]},
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "sources undisclosed; automated term search below",
                           "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "undisclosed",
  "basis": "raw videos from 'a variety of channels', not itemised. Timing: 2025-11, before the OPARA issue 2026-04-29.", "quote_ids": ["data_src"]},
 "appendix300_check": {
  "answer": "UNKNOWN", "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "undisclosed", "basis": "undisclosed sources",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_src"]
 },
 "input": {
  "frame_size": {"value": "generation at 480p / 720p (1080p via super-resolution); VAE config sample_size 256", "quote_ids": ["in_stages", "in_ss"]},
  "frame_rate_or_sampling": {"value": "training 16 fps (256p stages) to 24 fps (480p/720p); default output fps 24", "quote_ids": ["in_stages", "in_fps"]},
  "clip_length_frames": {"value": "default 121 frames for generation; config sample_tsize 64", "quote_ids": ["in_len", "in_ts"]},
  "temporal_compression": {"value": "4x", "quote_ids": ["dom_vae", "in_tf"]},
  "spatial_compression": {"value": "16x16", "quote_ids": ["dom_vae", "in_sf"]}
 },
 "embedding_dim": {"value": "32 channels x (1 + (T-1)/4) x H/16 x W/16; e.g. 121 x 720 x 1280 -> 32 x 31 x 45 x 80 = 3,571,200 values",
                   "derivation": "latent_channels 32, ffactor_temporal 4, ffactor_spatial 16; causal first frame (inferred from 'causal')", "quote_ids": ["in_lc", "in_tf", "in_sf", "dom_vae"]},
 "params": {"value": "not documented for the VAE (DiT 8.3B); VAE file 5,042,560,980 bytes (count not inferred: dtype unknown)", "scope": "n/a", "quote_ids": ["dom_card"]},
 "flops_per_input_if_documented": None,
 "flops_note": "no VAE FLOPs in the saved report/card",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists vae/diffusion_pytorch_model.safetensors, gated=False", "quote_ids": ["w_file", "w_gated"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "community licence grants use in the Territory (worldwide excl. EU/UK/South Korea) -- same judgement and flag as entry 04 HunyuanVideo", "quote_ids": ["lic_grant", "lic_territory"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VAE of a video diffusion model trained on general video", "quote_ids": ["dom_vae"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": "video data described only as raw videos from 'a variety of channels'; no datasets or named sources", "quote_ids": ["data_src"]},
  "eligible": "NO (fails C4; licence territory flag)"
 },
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"vae/diffusion_pytorch_model.safetensors\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "lic_card", "quote": "license_name: tencent-hunyuan-community", "source_file": HF},
  {"id": "lic_territory", "quote": "THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA AND IS EXPRESSLY LIMITED TO THE TERRITORY, AS DEFINED BELOW.", "source_file": LIC},
  {"id": "lic_grant", "quote": "We grant You, for the Territory only, a non-exclusive, non-transferable and royalty-free limited license under Tencent’s intellectual property or other rights owned by Us embodied in or utilized by the Materials to use, reproduce, distribute, create derivative works of (including Model Derivatives), and make modifications to the Materials", "source_file": LIC},
  {"id": "lic_aup_med", "quote": "To make high-stakes automated decisions in domains that affect an individual’s safety, rights or wellbeing (e.g., law enforcement, migration, medicine/health, management of critical infrastructure, safety components of products, essential services, credit, employment, housing, education, social scoring, or insurance);", "source_file": LIC},
  {"id": "dom_vae", "quote": "VAE. We introduce a causal 3D transformer architecture designed for joint image-video encoding, which achieves a spatial compression ratio of 16 × \\times and a temporal compression ratio of 4 × \\times , with a latent channel dimension of 32.", "source_file": P},
  {"id": "dom_card", "quote": "We propose an efficient architecture that integrates an 8.3B-parameter Diffusion Transformer (DiT) with a 3D causal VAE, achieving compression ratios of 16× in spatial dimensions and 4× along the temporal axis.", "source_file": HF},
  {"id": "data_src", "quote": "We sourced raw videos from a variety of channels, ensuring comprehensive coverage across diverse content, filming techniques, camera movements, styles, and scenarios. After basic deduplication and the removal of corrupted files, we obtained more than 10 million hours of raw video data.", "source_file": P},
  {"id": "data_img", "quote": "For image data, we adopted the acquisition and processing pipeline outlined in [ 9 ] , curating 5 billion images from a pool of over 10 billion", "source_file": P},
  {"id": "in_stages", "quote": "starting from 256p resolution at 16 fps and progressively advancing to 480p and 720p at 24 fps, with video durations ranging from 2 to 10 seconds.", "source_file": P},
  {"id": "in_fps", "quote": "export_to_video(video, \"output.mp4\", fps=24)", "source_file": HF},
  {"id": "in_len", "quote": "| `--video_length` | int | No | `121` | Number of frames to generate |", "source_file": HF},
  {"id": "in_ss", "quote": "\"sample_size\": 256,", "source_file": C},
  {"id": "in_ts", "quote": "\"sample_tsize\": 64,", "source_file": C},
  {"id": "in_lc", "quote": "\"latent_channels\": 32,", "source_file": C},
  {"id": "in_tf", "quote": "\"ffactor_temporal\": 4,", "source_file": C},
  {"id": "in_sf", "quote": "\"ffactor_spatial\": 16,", "source_file": C}
 ]
}
save_record(rec)
