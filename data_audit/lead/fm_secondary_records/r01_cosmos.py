import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_lib import save_record
C = "cosmos_Cosmos-Tokenize1-CV8x8x8-720p_README.md"
P = "cosmos_arxiv_2501.03575_fulltext.html"
L = "license_nvidia_open_model_license.html"
rec = {
 "id": "01_nvidia_cosmos_tokenize1",
 "name": "NVIDIA Cosmos-Tokenize1 (Cosmos Tokenizer; CV8x8x8-720p primary variant; DV8x16x16-720p, CV4x8x8-360p also listed)",
 "family_note": "Tokenizer of the Cosmos-Predict1 world foundation models. Cosmos-Predict1-7B-Text2World and Cosmos-Predict2-2B-Video2World (the generative models) are separate HF repos, both gated='auto' (click-through) -> not opened; the representation of interest is the tokenizer.",
 "prior_work_K4": {
   "ref": "Nakamura, Breuer, Crespin, Dietrich, Imai (2026) 'Causal Inference with Video Features as Treatments', arXiv:2607.06126 (v2 2026-09-15)",
   "used": "NVIDIA Cosmos tokenizer (variant not named in the text searched); internal representations used as video summaries",
   "quote_ids": ["k4_use"]
 },
 "paper": {"title": "Cosmos World Foundation Model Platform for Physical AI", "year": 2025, "arxiv": "2501.03575",
           "versions": "v1 2025-01-07, v3 2025-07-09"},
 "weights": {
   "urls": ["https://huggingface.co/nvidia/Cosmos-Tokenize1-CV8x8x8-720p",
            "https://huggingface.co/nvidia/Cosmos-Tokenize1-DV8x16x16-720p",
            "https://huggingface.co/nvidia/Cosmos-Tokenize1-CV4x8x8-360p"],
   "hf_api_evidence": ["cosmos_Cosmos-Tokenize1-CV8x8x8-720p_hfapi_blobs.json", "cosmos_Cosmos-Tokenize1-DV8x16x16-720p_hfapi_blobs.json", "cosmos_Cosmos-Tokenize1-CV4x8x8-360p_hfapi_blobs.json"],
   "files_listed_CV8x8x8": {"encoder.jit": 86272108, "decoder.jit": 126022330, "autoencoder.jit": 212300573, "model.pt": 1479537453},
   "gated": False, "private": False,
   "note": "HF API: gated=False for all three tokenizer repos (the card carries extra_gated_prompt text but gating is off). Not downloaded."
 },
 "licence": {
   "id": "NVIDIA Open Model License Agreement (HF license: other / nvidia-open-model-license)",
   "url": "https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/",
   "version_note": "card embeds the 'Version Release Date: January 6, 2025' text; the live licence page saved 2026-10-02 shows 'Version Release Date: October 24, 2025' (NVIDIA may update the agreement).",
   "commercial": "commercial use permitted", "non_commercial_only": False,
   "restrictions": "must be consistent with NVIDIA Trustworthy AI terms; rights terminate if guardrails/technical limitations are circumvented; 'Built on NVIDIA Cosmos' attribution when distributing or training on outputs (card text)",
   "gating": "none (HF gated=False)",
   "quote_ids": ["lic_card", "lic_commercial", "lic_grant", "lic_ethics", "lic_terminate"]
 },
 "architecture": {
   "type": "causal temporal conv + causal temporal attention autoencoder with 2-level Haar wavelet front end; vanilla AE (continuous) or FSQ (discrete)",
   "params": "~105M (card/paper runtime table, CV 4x8x8 variant); CV8x8x8 not stated -- autoencoder.jit 212.3 MB (~106M params if bf16, inference only)",
   "representation": "encoder output latent tokens: continuous 16-dim vectors per latent voxel (CV) or FSQ indices, vocabulary 64,000 (DV)",
   "input_resolution": "min 256 px shorter side, up to 4K; CV8x8x8 tuned for 720p and above",
   "frames_per_clip": "121-frame context (CV8x8x8-720p); 49 (CV4x8x8-360p, DV8x16x16-720p); causal, so 1+8k frames",
   "temporal_compression": "8x (CV8x8x8, DV8x16x16); 4x (CV4x8x8)",
   "spatial_compression": "8x8 (CV8x8x8, CV4x8x8); 16x16 (DV8x16x16)",
   "quote_ids": ["arch_variant", "arch_input", "arch_output", "arch_params"]
 },
 "pretraining_data": {
   "summary": "Tokenizers trained jointly on images and videos; the paper's training dataset = proprietary video datasets + publicly available open-domain Internet videos, ~20M h raw video, 9 content categories (driving, hand/object manipulation, human motion, navigation, first-person, nature, camera motion, synthetic, others 7%). No dataset names for training (TokenBench/DAVIS named only for evaluation).",
   "form": "described only (sources characterised generically; no training-dataset list)",
   "quote_ids": ["data_sources", "data_categories", "data_hours", "tok_train", "tok_joint"]
 },
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "Search of saved paper full text and card for medical|surgical|surgery|endoscop|laparoscop|clinical|hospital|health: no hit in a data context (only 'healthy range' of gradient norms). Content categories listed contain no medical category; 'Others (7%)' is unspecified."},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "undisclosed", "basis": "Undisclosed proprietary + open-domain Internet video. Context: paper v1 2025-01-07 / weights 2025-03 precede the OPARA issue date 2026-04-29, so the OPARA release itself cannot be in it, but the source recordings' prior circulation is not documented.", "quote_ids": ["data_sources"]},
 "eligibility": {
   "C1_open_weights": {"status": "PASS", "basis": "HF API lists encoder.jit/decoder.jit/model.pt, gated=False"},
   "C2_licence_research_use": {"status": "PASS", "basis": "NVIDIA Open Model License grants use incl. commercial; ethics/guardrail conditions"},
   "C3_domain_secondary": {"status": "PASS", "basis": "video tokenizer (autoencoder) of a generative world model trained on general video"},
   "C4_documented_pretraining_data": {"status": "FAIL", "basis": "paper describes sources only generically ('proprietary video datasets and publicly available open-domain Internet videos') with category percentages; no training datasets or named sources listed"},
   "eligible": "NO (fails C4 under the frozen wording; borderline: sources are characterised but not listed)"
 },
 "quotes": [
  {"id": "k4_use", "quote": "we first regenerate the video content using the NVIDIA Cosmos tokenizer ( Agarwal et al., 2025 ) and extract their internal representations.", "source_file": "K4_arxiv_2607.06126v2_fulltext.html"},
  {"id": "lic_card", "quote": "This model is released under the  [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license).", "source_file": C},
  {"id": "lic_commercial", "quote": "* Models are commercially usable.", "source_file": C},
  {"id": "lic_grant", "quote": "NVIDIA hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, revocable (as stated in Section 2.1) license to publicly perform, publicly display, reproduce, use, create derivative works of, make, have made, sell, offer for sale, distribute (through multiple tiers of distribution) and import the Model.", "source_file": L},
  {"id": "lic_ethics", "quote": "Use of the Models under the Agreement must be consistent with NVIDIA’s Trustworthy AI terms", "source_file": L},
  {"id": "lic_terminate", "quote": "If you bypass, disable, reduce the efficacy of, or circumvent any technical limitation, safety guardrail or", "source_file": C},
  {"id": "arch_variant", "quote": "[Cosmos-Tokenize1-CV8x8x8-720p](https://huggingface.co/nvidia/Cosmos-Tokenize1-CV8x8x8-720p) (8x temporal compression, 8x8 spatial compression, 720p and above, 121 frames context)", "source_file": C},
  {"id": "arch_input", "quote": "**Resolution:** Minimum: 256px (shorter side). Maximum: Up to 4K", "source_file": C},
  {"id": "arch_output", "quote": "Continuous-valued feature vectors with a dimensionality of 16", "source_file": C},
  {"id": "arch_params", "quote": "| Cosmos-Tokenizer-CV      | 720x1280   | 4×8×8            | 105M       | **34.8**  |", "source_file": C},
  {"id": "data_sources", "quote": "3.1 Dataset We use both proprietary video datasets and publicly available open-domain Internet videos to train our models.", "source_file": P},
  {"id": "data_categories", "quote": "1. Driving (11%), 2. Hand motion and object manipulation (16%), 3. Human motion and activity (10%), 4. Spatial awareness and navigation (16%), 5. First person point-of-view (8%), 6. Nature dynamics (20%), 7. Dynamic camera movements (8%), 8. Synthetically rendered (4%), and 9. Others (7%).", "source_file": P},
  {"id": "data_hours", "quote": "In total, we accumulate about 20M hours of raw videos with resolutions from 720p to 4k.", "source_file": P},
  {"id": "tok_train", "quote": "We train our tokenizers directly on high-resolution images and long-duration videos without limiting the categories or aspect ratios.", "source_file": P},
  {"id": "tok_joint", "quote": "4.2 Training Strategy We employ a joint training strategy by alternating mini-batches of images and videos at a preset frequency.", "source_file": P}
 ]
}
save_record(rec)
