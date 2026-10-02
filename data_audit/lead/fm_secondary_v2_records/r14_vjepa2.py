import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

AL = "vjepa2_facebook__vjepa2-vitl-fpc64-256_hfapi.json"; AH = "vjepa2_facebook__vjepa2-vith-fpc64-256_hfapi.json"
AG = "vjepa2_facebook__vjepa2-vitg-fpc64-256_hfapi.json"; AG384 = "vjepa2_facebook__vjepa2-vitg-fpc64-384_hfapi.json"
CL = "vjepa2_vjepa2-vitl-fpc64-256_README.md"; CG = "vjepa2_vjepa2-vitg-fpc64-256_README.md"
CFL = "vjepa2_vjepa2-vitl-fpc64-256_config.json"; CFH = "vjepa2_vjepa2-vith-fpc64-256_config.json"
CFG = "vjepa2_vjepa2-vitg-fpc64-256_config.json"; CFG384 = "vjepa2_vjepa2-vitg-fpc64-384_config.json"
GR = "vjepa2_github_README.md"; LIC = "vjepa2_github_LICENSE.txt"; P = "vjepa2_arxiv_2506.09985_fulltext.txt"
BLOG = "vjepa2_meta_blog.txt"; HG = "vjepa2_head_vitg.json"; HT = "howto100m_arxiv_1906.03327v2.txt"
DATA_FILES = [GR, P, BLOG, CG, HT]

rec = {
 "id": "14_vjepa2",
 "name": "V-JEPA 2 (Meta FAIR; ViT-L/16, ViT-H/16, ViT-g/16, ViT-g/16-384 video encoders pretrained on VideoMix22M)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "HF facebook/vjepa2-vitg-fpc64-256 (primary; ViT-g/16, 64 frames per clip, 256 px; sha 875c192b7b704b87d1e1d99345769632dd5f739a), facebook/vjepa2-vitg-fpc64-384, facebook/vjepa2-vith-fpc64-256, facebook/vjepa2-vitl-fpc64-256 (all pretrained encoders, 2025); also dl.fbaipublicfiles.com/vjepa2/{vitl,vith,vitg,vitg-384}.pt. Out of scope: the -ssv2 / -diving48 fine-tuned classifier repos, V-JEPA 2-AC (action-conditioned predictor post-trained on Droid robot video) and V-JEPA 2.1 (listed separately in the README).",
 "paper": {"title": "V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning", "year": 2025, "arxiv": "2506.09985 (HTML)"},
 "weights_location": {
  "urls": ["https://huggingface.co/facebook/vjepa2-vitg-fpc64-256", "https://huggingface.co/facebook/vjepa2-vitg-fpc64-384",
           "https://huggingface.co/facebook/vjepa2-vith-fpc64-256", "https://huggingface.co/facebook/vjepa2-vitl-fpc64-256",
           "https://dl.fbaipublicfiles.com/vjepa2/vitg.pt"],
  "files_listed": {"vjepa2-vitg-fpc64-256 model.safetensors": 4138311608, "vjepa2-vitg-fpc64-384 model.safetensors": 4138311608,
                   "vjepa2-vith-fpc64-256 model.safetensors": 2615800136, "vjepa2-vitl-fpc64-256 model.safetensors": 1303947864,
                   "dl.fbaipublicfiles vitg.pt (HEAD Content-Length)": 16464208210},
  "gated": False, "private": False,
  "verified_how": "HF API model listings (metadata only) " + ", ".join([AG, AG384, AH, AL]) + " and HTTP HEAD of vitg.pt (" + HG + "); nothing downloaded",
  "quote_ids": ["w_file_g", "w_gated_g", "w_file_l", "w_readme_g", "w_head_g"]
 },
 "licence": {
  "id": "MIT (GitHub LICENSE; HF card tag for vitl/vith) / Apache-2.0 (HF card tag for vitg-256 and vitg-384)",
  "url": "https://github.com/facebookresearch/vjepa2/blob/main/LICENSE ; https://huggingface.co/facebook/vjepa2-vitg-fpc64-256",
  "commercial": "permitted (MIT / Apache-2.0)", "non_commercial_only": False,
  "restrictions": "none beyond MIT / Apache-2.0 notices (card tags differ between repos)",
  "gating": "none", "quote_ids": ["lic_mit", "lic_readme", "lic_card_g", "lic_card_l"]
 },
 "domain": {
  "value": "self-supervised video encoder trained by mask-denoising FEATURE PREDICTION in a learned representation space (predictor regresses EMA-encoder targets with an L1 loss; no pixel decoder), at scale on general internet video; the authors contrast it with video-generation approaches and call it a 'world model'.",
  "authors_wording_generative_vs_not": [
   "Paper: 'in contrast to approaches based on video generation, the JEPA approach focuses on learning representations for predictable aspects of a scene ... while ignoring unpredictable details that generative objectives emphasize, since they make pixel-level predictions'",
   "Paper: 'we use a mask-denoising feature prediction objective ..., where the model predicts masked segments of a video in a learned representation space.'",
   "Paper: 'The outputs of the predictor are then regressed to the prediction targets using an L1 loss.'",
   "Meta blog: 'V-JEPA 2 is a world model that achieves state-of-the-art performance on visual understanding and prediction in the physical world.' (no use of the word 'generative'; the paper explicitly sets JEPA apart from generative/pixel-level objectives)"
  ],
  "quote_ids": ["dom_contrast", "dom_featpred", "dom_l1", "dom_blog_wm", "dom_card_use"]
 },
 "architecture": {
  "type": "ViT encoder on 2x16x16 tubelets + 12-layer 384-dim predictor (pretraining); EMA target encoder",
  "representation": "frozen encoder output tokens (1408-dim ViT-g, 1280 ViT-H, 1024 ViT-L), pooled downstream by an attentive probe; HF get_vision_features returns the token sequence"
 },
 "pretraining_data": {
  "summary": "VideoMix22M (22M samples): SSv2 168K, Kinetics-400/600/700 733K, HowTo100M 1.1M, YT-Temporal-1B 19M (retrieval-curated general YouTube), plus ImageNet 1M images (duplicated into 16-frame clips). All named public sources.",
  "form": "dataset list (named; HowTo100M and YT-Temporal-1B are open-ended YouTube-derived sets)"
 },
 "pretraining_data_quote": {"quote_ids": ["data_t1", "data_rows", "data_sources", "ht_youtube", "ht_health"]},
 "medical_video_in_data": {
  "answer": "YES (indirect, health-category instructional video via HowTo100M; no surgical/endoscopic content documented)",
  "basis": "VideoMix22M includes HowTo100M (weight 0.318), whose paper lists a WikiHow 'Health' category (172 tasks, 1.7M clips, incl. 'Conditions and Treatments', 'Medication and Equipment', 'Medical Information'). The V-JEPA 2 paper/README/blog contain no medical/surgical term in a data context (term search below); YT-Temporal-1B content is undocumented general YouTube.",
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)},
  "quote_ids": ["ht_health"]
 },
 "appendix300_possible": {
  "answer": "UNKNOWN", "basis_class": "named_open_web_sources",
  "basis": "YT-Temporal-1B ('general YouTube videos', 19M, curated only against cartoon/clipart-style noise) and HowTo100M are named but open-ended YouTube-derived sources, so the documentation does not allow the Appendix300 source recordings to be excluded. Timing: release 2025-06, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_sources", "data_t1"]
 },
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "named_open_web_sources",
  "basis": "open-ended YT-Temporal-1B and HowTo100M components; see appendix300_possible",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_sources"]
 },
 "input": {
  "frame_size": {"value": "256x256 (fpc64-256 repos); 384x384 (vitg-fpc64-384); primary pretraining at 256, cooldown crops 256/384/512", "quote_ids": ["in_crop_g", "in_crop_384", "in_hparams"]},
  "frame_rate_or_sampling": {"value": "4 fps in both pretraining phases (primary 16 frames = 4 s; cooldown 64 frames = 16 s)", "quote_ids": ["in_hparams", "in_64_16s"]},
  "clip_length_frames": {"value": "64 frames for the released fpc64 checkpoints (config frames_per_clip 64); primary pretraining used 16", "quote_ids": ["in_fpc", "in_card_64", "in_hparams"]},
  "temporal_compression": {"value": "tubelet 2 frames (64 -> 32 token slices)", "quote_ids": ["in_tub"]},
  "spatial_compression": {"value": "16x16 patches (256 -> 16x16 = 256 tokens per slice; 384 -> 24x24)", "quote_ids": ["in_patch"]}
 },
 "embedding_dim": {
  "value": "ViT-g/16 @64x256: 1408 x (32 x 16 x 16) = 1408 x 8192 tokens; ViT-g/16-384: 1408 x (32 x 24 x 24) = 1408 x 18432; ViT-H: 1280 x 8192; ViT-L: 1024 x 8192. Pooled dim = hidden size when an attentive / mean pool is applied (no fixed pooled output).",
  "derivation": "hidden_size from HF configs; grid from frames_per_clip 64 / tubelet 2 and crop / patch 16",
  "quote_ids": ["in_hid_g", "in_hid_h", "in_hid_l", "in_fpc", "in_tub", "in_patch"]
 },
 "params": {
  "value": "ViT-L/16 300M, ViT-H/16 600M, ViT-g/16 1B, ViT-g/16-384 1B (encoder; README '#Parameters')",
  "scope": "encoder",
  "quote_ids": ["par_hdr", "par_l", "par_h", "par_g"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs/MACs per input stated in the saved paper, README, card or blog (searched FLOP)",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists model.safetensors for the four encoder repos, gated=False; README also links public dl.fbaipublicfiles checkpoints (HEAD 200)", "quote_ids": ["w_file_g", "w_gated_g", "w_head_g"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "MIT (repo) / Apache-2.0 (vitg card tags)", "quote_ids": ["lic_mit", "lic_card_g"]},
  "C3_domain_secondary": {"status": "FAIL", "basis": "latent-space feature predictor without a pixel decoder; the authors set the JEPA approach apart from 'approaches based on video generation' and 'generative objectives' that 'make pixel-level predictions' -> FAIL under the v1 convention (V-JEPA family)", "quote_ids": ["dom_contrast", "dom_featpred"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "paper Table 1 lists every VideoMix22M source with sample counts and hours", "quote_ids": ["data_t1", "data_rows"]},
  "eligible": "NO (fails C3: feature-prediction model explicitly contrasted with generative objectives by its authors)"
 },
 "quotes": [
  {"id": "w_file_g", "quote": "\"rfilename\": \"model.safetensors\",", "source_file": AG},
  {"id": "w_gated_g", "quote": "\"gated\": false,", "source_file": AG},
  {"id": "w_file_l", "quote": "\"rfilename\": \"model.safetensors\",", "source_file": AL},
  {"id": "w_readme_g", "quote": "<td><a href=\"https://dl.fbaipublicfiles.com/vjepa2/vitg.pt\">checkpoint</a></td>", "source_file": GR},
  {"id": "w_head_g", "quote": "\"Content-Length\": \"16464208210\",", "source_file": HG},
  {"id": "lic_mit", "quote": "MIT License Copyright (c) Meta Platforms, Inc. and affiliates.", "source_file": LIC},
  {"id": "lic_readme", "quote": "The majority of V-JEPA 2 is licensed under MIT, however portions of the project are available under separate license terms:", "source_file": GR},
  {"id": "lic_card_g", "quote": "license: apache-2.0", "source_file": CG},
  {"id": "lic_card_l", "quote": "license: mit", "source_file": CL},
  {"id": "dom_contrast", "quote": "in contrast to approaches based on video generation, the JEPA approach focuses on learning representations for predictable aspects of a scene (e.g., the trajectory of an object in motion) while ignoring unpredictable details that generative objectives emphasize, since they make pixel-level predictions", "source_file": P},
  {"id": "dom_featpred", "quote": "we use a mask-denoising feature prediction objective ( Assran et al., 2023 ; Bardes et al., 2024 ) , where the model predicts masked segments of a video in a learned representation space.", "source_file": P},
  {"id": "dom_l1", "quote": "The outputs of the predictor are then regressed to the prediction targets using an L1 loss.", "source_file": P},
  {"id": "dom_blog_wm", "quote": "Meta Video Joint Embedding Predictive Architecture 2 (V-JEPA 2) is a world model that achieves state-of-the-art performance on visual understanding and prediction in the physical world.", "source_file": BLOG},
  {"id": "dom_card_use", "quote": "V-JEPA 2 is intended to represent any video (and image) to perform video classification, retrieval, or as a video encoder for VLMs.", "source_file": CG},
  {"id": "data_t1", "quote": "Table 1: VideoMix22M (VM22M) Pretraining Dataset. To build our observation pretraining dataset, we combined four different video sources and one image dataset.", "source_file": P},
  {"id": "data_rows", "quote": "SSv2 ( Goyal et al., 2017 ) 168K EgoVideo 168 No 0.056 Kinetics ( Carreira et al., 2019 ) 733K ExoVideo 614 No 0.188 Howto100M ( Miech et al., 2019 ) 1.1M ExoVideo 134K No 0.318 YT-Temporal-1B ( Zellers et al., 2022 ) 19M ExoVideo 1.6M Yes 0.188 ImageNet ( Deng et al., 2009 ) 1M Images n/a No 0.250", "source_file": P},
  {"id": "data_sources", "quote": "YouTube tutorial videos from HowTo100M ( Miech et al., 2019 ) , and general YouTube videos from YT-Temporal-1B ( Zellers et al., 2022 ) , which we refer to as YT1B.", "source_file": P},
  {"id": "ht_youtube", "quote": "HowTo100M features 1.22 million videos from YouTube, with activities from domains such as cooking, hand crafting, personal care, gardening, etc.", "source_file": HT},
  {"id": "ht_health", "quote": "Health 172 1.7M Emotional Health 63 853k Conditions and Treatments 35 271k Injury and Accidents 22 147k Medication and Equipment 20 138k", "source_file": HT},
  {"id": "in_crop_g", "quote": "\"crop_size\": 256,", "source_file": CFG},
  {"id": "in_crop_384", "quote": "\"crop_size\": 384,", "source_file": CFG384},
  {"id": "in_fpc", "quote": "\"frames_per_clip\": 64,", "source_file": CFG},
  {"id": "in_card_64", "quote": "To load a video, sample the number of frames according to the model. For this model, we use 64.", "source_file": CG},
  {"id": "in_tub", "quote": "\"tubelet_size\": 2,", "source_file": CFG},
  {"id": "in_patch", "quote": "\"patch_size\": 16,", "source_file": CFG},
  {"id": "in_hid_g", "quote": "\"hidden_size\": 1408,", "source_file": CFG},
  {"id": "in_hid_h", "quote": "\"hidden_size\": 1280,", "source_file": CFH},
  {"id": "in_hid_l", "quote": "\"hidden_size\": 1024,", "source_file": CFL},
  {"id": "in_hparams", "quote": "Parameter Primary Phase Cooldown Phase Number of frames 16 64 Frames per Second 4.0 4.0 Crop Size 256 [256, 384, 512]", "source_file": P},
  {"id": "in_64_16s", "quote": "we explore training with longer clips of up to 64 frames (16 seconds) at higher spatial resolutions.", "source_file": P},
  {"id": "par_hdr", "quote": "<th colspan=\"1\">#Parameters</th>", "source_file": GR},
  {"id": "par_l", "quote": "<td>ViT-L/16</td> <td>300M</td> <td>256</td> <td><a href=\"https://dl.fbaipublicfiles.com/vjepa2/vitl.pt\">checkpoint</a></td>", "source_file": GR},
  {"id": "par_h", "quote": "<td>ViT-H/16</td> <td>600M</td> <td>256</td>", "source_file": GR},
  {"id": "par_g", "quote": "<td>ViT-g/16</td> <td>1B</td> <td>256</td> <td><a href=\"https://dl.fbaipublicfiles.com/vjepa2/vitg.pt\">checkpoint</a></td>", "source_file": GR}
 ]
}
save_record(rec)
