import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, prev_candidate, term_search, MED_TERMS, A300_TERMS

API8 = "cosmos_nvidia__Cosmos-Tokenize1-CV8x8x8-720p_hfapi.json"
APIDV = "cosmos_nvidia__Cosmos-Tokenize1-DV8x16x16-720p_hfapi.json"
API4 = "cosmos_nvidia__Cosmos-Tokenize1-CV4x8x8-360p_hfapi.json"
C = "cosmos_Cosmos-Tokenize1-CV8x8x8-720p_README.md"
LIC = "license_nvidia_open_model_license.txt"
P = "cosmos_arxiv_2501.03575_fulltext.txt"
K4 = "K4_arxiv_2607.06126v2_fulltext.txt"
DATA_FILES = [P, C]
FMAP = {"K4_arxiv_2607.06126v2_fulltext.html": K4, "license_nvidia_open_model_license.html": LIC,
        "cosmos_arxiv_2501.03575_fulltext.html": P}

v1 = prev_candidate("01_nvidia_cosmos_tokenize1")
v1q = [{"id": q["id"], "quote": q["quote"], "source_file": FMAP.get(q["source_file"], q["source_file"])} for q in v1["quotes"]]

rec = {
 "id": "01_nvidia_cosmos_tokenize1",
 "name": v1["name"],
 "family_note": v1["family_note"],
 "prior_work_K4": v1["prior_work_K4"],
 "version": "nvidia/Cosmos-Tokenize1-CV8x8x8-720p (primary; HF repo sha b6af495317c76f287a4131e9299936b1533f5f9f, created 2025-03-14, last modified 2025-04-23; files encoder.jit / decoder.jit / autoencoder.jit / model.pt); also listed: Cosmos-Tokenize1-DV8x16x16-720p (sha 017d82884b28491c191f9ea9107d1a6dcc20e725), Cosmos-Tokenize1-CV4x8x8-360p (sha d82fab12c9fe1fc579d05f082d94d35c5962bf06). Paper arXiv 2501.03575 (Cosmos-Tokenize1 = the second-generation tokenizer release; Cosmos-0.1-Tokenizer = the first).",
 "paper": v1["paper"],
 "weights_location": {
  "urls": v1["weights"]["urls"],
  "files_listed_CV8x8x8": v1["weights"]["files_listed_CV8x8x8"],
  "files_listed_DV8x16x16": {"encoder.jit": 92292848, "decoder.jit": 132042180, "autoencoder.jit": 223576773, "model.pt": 1912566352},
  "files_listed_CV4x8x8": {"encoder.jit": 91128212, "decoder.jit": 130271330, "autoencoder.jit": 221415661, "model.pt": 1543318925},
  "gated": False, "private": False,
  "verified_how": "HF API model listings (metadata only) saved as " + ", ".join([API8, APIDV, API4]) + "; nothing downloaded",
  "note": v1["weights"]["note"],
  "quote_ids": ["w_enc", "w_gated8", "w_gateddv", "w_gated4"]
 },
 "licence": {
  "id": v1["licence"]["id"], "url": v1["licence"]["url"], "version_note": v1["licence"]["version_note"],
  "commercial": v1["licence"]["commercial"], "non_commercial_only": False,
  "restrictions": v1["licence"]["restrictions"], "gating": v1["licence"]["gating"],
  "quote_ids": ["lic_card", "lic_commercial", "lic_grant", "lic_ethics", "lic_terminate", "lic_version_live"]
 },
 "domain": {
  "value": "video tokenizer (causal wavelet-space autoencoder; continuous AE or discrete FSQ) of the Cosmos-Predict1 generative world foundation models; trained jointly on images and general video (proprietary + open-domain Internet video, 9 content categories)",
  "quote_ids": ["dom_desc", "dom_type", "tok_train", "data_sources"]
 },
 "architecture": {"type": v1["architecture"]["type"], "representation": v1["architecture"]["representation"]},
 "pretraining_data": {"summary": v1["pretraining_data"]["summary"], "form": v1["pretraining_data"]["form"]},
 "pretraining_data_quote": {"quote_ids": ["data_sources", "data_categories", "data_hours", "tok_train", "tok_joint"]},
 "medical_video_in_data": {
  "answer": v1["medical_video_in_data"]["answer"], "basis": v1["medical_video_in_data"]["basis"],
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}
 },
 "appendix300_possible": v1["appendix300_possible"],
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "undisclosed",
  "basis": v1["appendix300_possible"]["basis"],
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_sources"]
 },
 "input": {
  "frame_size": {"value": "min 256 px shorter side, up to 4K; CV8x8x8 variant for 720p and above (trained on 360p/720p frames); up to 8 s of 1080p per pass on an A100-80GB", "quote_ids": ["arch_input", "arch_variant", "in_train_frames", "in_len"]},
  "frame_rate_or_sampling": {"value": "not documented for the tokenizer (consecutive frames are encoded causally; no frame-rate requirement stated); the paper's FPS-aware RoPE concerns the diffusion WFM, not the tokenizer", "quote_ids": ["in_first_frame"]},
  "clip_length_frames": {"value": "121-frame context for CV8x8x8-720p (trained on 121-frame mini-batches); 49 for CV4x8x8-360p and DV8x16x16-720p; causal 1+T frame layout", "quote_ids": ["arch_variant", "in_train_frames", "in_first_frame"]},
  "temporal_compression": {"value": "8x for CV8x8x8 (1 + T/8 latent frames; first frame kept as its own latent frame); 4x for CV4x8x8; 8x for DV8x16x16", "quote_ids": ["arch_variant", "in_first_frame", "in_wavelet"]},
  "spatial_compression": {"value": "8x8 for CV8x8x8 and CV4x8x8; 16x16 for DV8x16x16", "quote_ids": ["arch_variant", "in_wavelet"]}
 },
 "embedding_dim": {
  "value": "CV8x8x8-720p, 121 frames x 720x1280 input: 16 channels x (1+120/8 = 16) x 90 x 160 = 3,686,400 values; generally 16 x (1 + T/8) x H/8 x W/8 for 1+T input frames. DV variants: FSQ indices (6-dim latent, vocabulary 64,000) instead of 16-dim vectors.",
  "derivation": "latent dimension 16 for continuous tokenizers (card + paper); temporal token count 1 + T/s_T (paper Fig. 7); s_T = 8, s_HW = 8 for CV8x8x8",
  "quote_ids": ["arch_output", "in_latent16", "in_first_frame", "arch_variant", "in_vocab"]
 },
 "params": {
  "value": "not documented for Cosmos-Tokenize1-CV8x8x8-720p. The only documented count is 105M for the 4x8x8 continuous video tokenizer (paper Table 9: 'Cosmos-0.1-Tokenizer-CV4x8x8', i.e. the first-generation release; the card's runtime table labels the same row 'Cosmos-Tokenizer-CV'), whole encoder+decoder. Inferred only: autoencoder.jit 212.3 MB, encoder.jit 86.3 MB (dtype not documented).",
  "scope": "whole autoencoder of the 4x8x8 variant (encoder-only count not documented)",
  "quote_ids": ["arch_params", "in_params_paper", "in_runtime_def"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs/MACs statement for the tokenizer (paper FLOPs table 13 concerns the diffusion transformer). Documented proxy: 34.8 ms per video frame for the 4x8x8 continuous tokenizer (encode+decode) at 720x1280 on one A100-80GB; runtime of CV8x8x8 not documented.",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": v1["eligibility"]["C1_open_weights"]["basis"], "quote_ids": ["w_enc", "w_gated8"]},
  "C2_licence_research_use": {"status": "PASS", "basis": v1["eligibility"]["C2_licence_research_use"]["basis"], "quote_ids": ["lic_card", "lic_grant", "lic_ethics"]},
  "C3_domain_secondary": {"status": "PASS", "basis": v1["eligibility"]["C3_domain_secondary"]["basis"], "quote_ids": ["dom_desc", "tok_train"]},
  "C4_documented_pretraining_data": {"status": "FAIL", "basis": v1["eligibility"]["C4_documented_pretraining_data"]["basis"], "quote_ids": ["data_sources", "data_categories"]},
  "eligible": v1["eligibility"]["eligible"]
 },
 "changes_vs_v1": [
  "sources re-fetched into /home fm_sources/secondary (raw sha256 compared with v1 per quote); the NVIDIA licence page raw HTML differs from the v1 copy (site markup) but every v1 licence quote still verifies; live page still shows 'Version Release Date: October 24, 2025'",
  "clarification (architecture.params wording): v1 said '~105M (card/paper runtime table, CV 4x8x8 variant)'. The paper's Table 9 attributes 105M to 'Cosmos-0.1-Tokenizer-CV4x8x8' (first-generation tokenizer, 49 frames), not to a Cosmos-Tokenize1 checkpoint; params of the audited CV8x8x8-720p are not documented. Recorded in the new params field; eligibility unaffected.",
  "added structured fields with new quotes (HF listings of all three repos, latent shape 1+T/s_T, training frame counts, vocabulary)",
  "no change to any eligibility status or Appendix300 answer"
 ],
 "quotes": v1q + [
  {"id": "w_enc", "quote": "\"rfilename\": \"encoder.jit\",", "source_file": API8},
  {"id": "w_gated8", "quote": "\"gated\": false,", "source_file": API8},
  {"id": "w_gateddv", "quote": "\"gated\": false,", "source_file": APIDV},
  {"id": "w_gated4", "quote": "\"gated\": false,", "source_file": API4},
  {"id": "lic_version_live", "quote": "Version Release Date: October 24, 2025", "source_file": LIC},
  {"id": "dom_desc", "quote": "Cosmos Tokenizer can serve as an effective and efficient building block in both diffusion-based and autoregressive models for image and video generation.", "source_file": C},
  {"id": "dom_type", "quote": "Model Type: | Auto-Encoder", "source_file": C},
  {"id": "in_len", "quote": "**Video Length:** Up to 8 seconds for 1080p videos (bounded by A100 80G GPU memory; higher resolutions will have shorter supported durations)", "source_file": C},
  {"id": "in_wavelet", "quote": "The encoder starts with a 2-level [Haar wavelet](https://link.springer.com/book/10.1007/978-3-319-04295-4) transform layer, which down-samples inputs by a factor of 4 in both spatial and temporal dimensions.", "source_file": C},
  {"id": "in_train_frames", "quote": "2. Cosmos-Tokenize1 : Trained using mini-batches sampling a larger number of 360p or 720p video frames (121 frames for CV and 49 frames for DV ).", "source_file": P},
  {"id": "in_first_frame", "quote": "The first temporal token represents the first input frame, enabling joint image ( T = 0 T=0 ) and video ( T > 0 T>0 ) tokenization in a shared latent space.", "source_file": P},
  {"id": "in_latent16", "quote": "The latent dimension for the continuous tokenizers is 16 16 , whereas for the discrete tokenizers, it is 6 6 , which represents the number of the FSQ levels", "source_file": P},
  {"id": "in_vocab", "quote": "This configuration corresponds to a vocabulary size of 64,000 64{,}000 .", "source_file": P},
  {"id": "in_params_paper", "quote": "Cosmos-0.1-Tokenizer-CV4 × \\times 8 × \\times 8 Continuous-Video 720 × 1280 720\\times 1280 49 105M 34.8", "source_file": P},
  {"id": "in_runtime_def", "quote": "Table 9: Runtime performance comparison of tokenizers. Time is reported per image or per video frame.", "source_file": P}
 ]
}
prev_q = {q["id"]: q for q in v1["quotes"]}
save_record(rec, prev_quotes=prev_q)
