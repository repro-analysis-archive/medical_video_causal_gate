import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

GR = "vjepa_github_README.md"; LIC = "vjepa_github_LICENSE.txt"; P = "vjepa_arxiv_2404.08471_fulltext.txt"
BLOG = "vjepa_meta_blog.txt"; VT = "vjepa_github_vision_transformer.py.txt"; CFG = "vjepa_github_pretrain_vitl16.yaml.txt"
HL = "vjepa_head_vitl16.json"; HH = "vjepa_head_vith16.json"; HH384 = "vjepa_head_vith16-384.json"
HT = "howto100m_arxiv_1906.03327v2.txt"; KABS = "kinetics_arxiv_1705.06950_abs.txt"; SABS = "ssv2_arxiv_1706.04261_abs.txt"
DATA_FILES = [GR, P, BLOG, HT, KABS, SABS]

rec = {
 "id": "13_vjepa",
 "name": "V-JEPA (Meta FAIR; video joint-embedding predictive architecture; ViT-L/16, ViT-H/16, ViT-H/16-384 pretrained on VideoMix2M)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "facebookresearch/jepa release (2024-02): pretrained checkpoints vitl16.pth.tar (ViT-L/16, 224), vith16.pth.tar (ViT-H/16, 224), vith16-384.pth.tar (ViT-H/16, 384) on dl.fbaipublicfiles.com; no official HF repo found for V-JEPA (v1) (HF search author=facebook 'jepa' lists only 3d-jepa and jepa-wms)",
 "paper": {"title": "Revisiting Feature Prediction for Learning Visual Representations from Video", "year": 2024, "arxiv": "2404.08471 (HTML, v1 rendering)", "venue": "TMLR 2024"},
 "weights_location": {
  "urls": ["https://dl.fbaipublicfiles.com/jepa/vitl16/vitl16.pth.tar", "https://dl.fbaipublicfiles.com/jepa/vith16/vith16.pth.tar",
           "https://dl.fbaipublicfiles.com/jepa/vith16-384/vith16-384.pth.tar"],
  "files_listed": {"vitl16.pth.tar": 5143105394, "vith16.pth.tar": 10393043714, "vith16-384.pth.tar": 10428847322},
  "gated": False, "private": False,
  "verified_how": "official GitHub README model-zoo links + HTTP HEAD (status 200, Content-Length; no body transferred) saved as " + ", ".join([HL, HH, HH384]),
  "quote_ids": ["w_readme_l", "w_head_l", "w_head_h", "w_head_h384"]
 },
 "licence": {
  "id": "CC-BY-NC-4.0 (repository LICENSE: Attribution-NonCommercial 4.0 International)",
  "url": "https://github.com/facebookresearch/jepa/blob/main/LICENSE",
  "commercial": "not permitted", "non_commercial_only": True,
  "restrictions": "non-commercial use only; attribution",
  "gating": "none", "quote_ids": ["lic_readme", "lic_text"]
 },
 "domain": {
  "value": "self-supervised video encoder trained by FEATURE PREDICTION in latent space (x-encoder + predictor regress EMA target-encoder features of masked spatio-temporal regions with an L1 loss); no pixel decoder; described by its authors as non-generative. Trained on general video (VideoMix2M).",
  "authors_wording_generative_vs_not": [
   "Meta blog: 'V-JEPA is a non-generative model that learns by predicting missing or masked parts of a video in an abstract representation space.'",
   "Meta blog: 'Unlike generative approaches that try to fill in every missing pixel, V-JEPA has the flexibility to discard unpredictable information'",
   "GitHub README: 'As opposed to generative methods that have a pixel decoder, V-JEPA has a predictor that makes predictions in latent space.'",
   "GitHub README / paper: pretraining 'does not utilize ... pixel-level reconstruction'; paper abstract: 'trained solely using a feature prediction objective, without the use of pretrained image encoders, text, negative examples, reconstruction, or other sources of supervision.'",
   "Note: the README also reports a separately trained conditional diffusion model used only to visualise the frozen predictor's feature-space predictions as pixels; the V-JEPA encoder/predictor themselves stay frozen and are not generative."
  ],
  "quote_ids": ["dom_blog_nongen", "dom_blog_unlike", "dom_readme_pixdec", "dom_readme_noreco", "dom_abs", "dom_diffusion", "dom_l1"]
 },
 "architecture": {
  "type": "ViT x-encoder on 2x16x16 tubelets + narrow ViT predictor (12 blocks, 384-dim); EMA y-encoder supplies targets; multi-block masking",
  "representation": "frozen encoder output tokens (1024-dim ViT-L, 1280-dim ViT-H), pooled downstream by a learned attentive probe"
 },
 "pretraining_data": {
  "summary": "VideoMix2M (~2M videos) = HowTo100M (1.22M narrated instructional YouTube videos, WikiHow task categories incl. 'Health') + Kinetics-400/600/700 (K710) + Something-Something-v2, minus validation overlap. Named public datasets.",
  "form": "dataset list (named; HowTo100M is an open-ended YouTube-search-derived set)"
 },
 "pretraining_data_quote": {"quote_ids": ["data_mix", "data_readme", "data_cfg_ht", "ht_youtube", "ht_health", "data_kin_abs", "data_ssv2_abs"]},
 "medical_video_in_data": {
  "answer": "YES (indirect, health-category instructional video via HowTo100M; no surgical/endoscopic content documented)",
  "basis": "VideoMix2M includes HowTo100M, whose paper lists a WikiHow 'Health' category (172 tasks, 1.7M clips; subcategories include 'Conditions and Treatments', 'Injury and Accidents', 'Medication and Equipment', 'Medical Information'). The V-JEPA paper/README/blog themselves contain no medical/surgical term (term search below).",
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)},
  "quote_ids": ["ht_health", "ht_medinfo"]
 },
 "appendix300_possible": {
  "answer": "UNKNOWN", "basis_class": "named_open_web_sources",
  "basis": "HowTo100M is a named but open-ended YouTube-search-derived set (1.22M videos, incl. health/medical-information instructional videos), so the documentation does not allow the Appendix300 source recordings to be excluded. Timing: release 2024-02, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_mix", "ht_youtube", "ht_health"]
 },
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "named_open_web_sources",
  "basis": "HowTo100M component is open-ended YouTube content; see appendix300_possible",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_mix", "ht_youtube"]
 },
 "input": {
  "frame_size": {"value": "224x224 (ViT-L/16, ViT-H/16); 384x384 (ViT-H/16-384)", "quote_ids": ["in_res", "in_cfg_crop"]},
  "frame_rate_or_sampling": {"value": "16 frames with temporal stride 4 (64 raw frames, ~2 s at 30 fps)", "quote_ids": ["in_stride", "in_cfg_sr"]},
  "clip_length_frames": {"value": "16 frames", "quote_ids": ["in_stride", "in_cfg_nf"]},
  "temporal_compression": {"value": "tubelet 2 frames (16 -> 8 token slices)", "quote_ids": ["in_patch", "in_cfg_tub"]},
  "spatial_compression": {"value": "16x16 patches (224 -> 14x14; 384 -> 24x24)", "quote_ids": ["in_patch", "in_cfg_ps"]}
 },
 "embedding_dim": {
  "value": "ViT-L/16: 1024 x (8 x 14 x 14) = 1024 x 1568 tokens per 16-frame 224 clip; ViT-H/16: 1280 x 1568; ViT-H/16-384: 1280 x (8 x 24 x 24) = 1280 x 4608. No fixed pooled vector: the authors pool with a learned attentive probe (pooled dim = embed dim).",
  "derivation": "embed_dim from src/models/vision_transformer.py (vit_large 1024, vit_huge 1280); token grid from 16 frames / tubelet 2 and 224/16 or 384/16",
  "quote_ids": ["in_vitl", "in_vith", "in_patch", "dom_probe"]
 },
 "params": {
  "value": "paper Table 6 'Params.': ViT-L/16 200M (as printed), ViT-H/16 630M, ViT-H/16-384 630M (encoder); note a 24-layer 1024-dim ViT-L has ~300M parameters by the standard 12*d^2*depth count (inferred), so the printed 200M looks inconsistent; checkpoint .pth.tar sizes (5.1 / 10.4 GB) include target encoder, predictor and optimizer state (inferred)",
  "scope": "encoder",
  "quote_ids": ["par_hdr", "par_row"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs/MACs per input stated in the saved paper, README or blog (searched FLOP)",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "official README links public checkpoints on dl.fbaipublicfiles.com; HEAD 200 with Content-Length, no login or form", "quote_ids": ["w_readme_l", "w_head_l"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "CC-BY-NC-4.0 permits non-commercial research", "quote_ids": ["lic_text"]},
  "C3_domain_secondary": {"status": "FAIL", "basis": "latent-space feature predictor without a pixel decoder, described by its authors as 'a non-generative model' (blog) and 'as opposed to generative methods that have a pixel decoder' (README) -> FAIL under the v1 convention (V-JEPA family)", "quote_ids": ["dom_blog_nongen", "dom_readme_pixdec", "dom_readme_noreco"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "paper names VideoMix2M components (HowTo100M, K400/600/700, SSv2)", "quote_ids": ["data_mix"]},
  "eligible": "NO (fails C3: non-generative feature-prediction model per the authors' own wording)"
 },
 "quotes": [
  {"id": "w_readme_l", "quote": "<td><a href=\"https://dl.fbaipublicfiles.com/jepa/vitl16/vitl16.pth.tar\">checkpoint</a></td>", "source_file": GR},
  {"id": "w_head_l", "quote": "\"Content-Length\": \"5143105394\",", "source_file": HL},
  {"id": "w_head_h", "quote": "\"Content-Length\": \"10393043714\",", "source_file": HH},
  {"id": "w_head_h384", "quote": "\"Content-Length\": \"10428847322\",", "source_file": HH384},
  {"id": "lic_readme", "quote": "See the [LICENSE](./LICENSE) file for details about the license under which this code is made available.", "source_file": GR},
  {"id": "lic_text", "quote": "Attribution-NonCommercial 4.0 International", "source_file": LIC},
  {"id": "dom_blog_nongen", "quote": "V-JEPA is a non-generative model that learns by predicting missing or masked parts of a video in an abstract representation space.", "source_file": BLOG},
  {"id": "dom_blog_unlike", "quote": "Unlike generative approaches that try to fill in every missing pixel, V-JEPA has the flexibility to discard unpredictable information, which leads to improved training and sample efficiency by a factor between 1.5x and 6x.", "source_file": BLOG},
  {"id": "dom_readme_pixdec", "quote": "As opposed to generative methods that have a pixel decoder, V-JEPA has a predictor that makes predictions in latent space.", "source_file": GR},
  {"id": "dom_readme_noreco", "quote": "V-JEPA pretraining is based solely on an unsupervised feature prediction objective, and does not utilize pretrained image encoders, text, negative examples, human annotations, or pixel-level reconstruction.", "source_file": GR},
  {"id": "dom_abs", "quote": "a collection of vision models trained solely using a feature prediction objective, without the use of pretrained image encoders, text, negative examples, reconstruction, or other sources of supervision.", "source_file": P},
  {"id": "dom_diffusion", "quote": "We train a conditional diffusion model to decode the V-JEPA feature-space predictions to interpretable pixels; the pretrained V-JEPA encoder and predictor networks are kept frozen in this process.", "source_file": GR},
  {"id": "dom_l1", "quote": "The outputs of the predictor are then regressed to the prediction targets using an L 1 L_{1} loss.", "source_file": P},
  {"id": "dom_probe", "quote": "e.g., using a frozen backbone and only a light-weight task-specific attentive probe.", "source_file": GR},
  {"id": "data_mix", "quote": "We combine several public datasets to construct an unsupervised video pretraining dataset, which we refer to as VideoMix2M. Specifically, we combine the videos from HowTo100M (HT) ( Miech et al., 2019 ) , Kinetics-400/600/700 (K710) ( Kay et al., 2017 ) , and Something-Something-v2 (SSv2) ( Goyal et al., 2017 ) , and remove any overlap with the validation sets of Kinetics-400/600/700 and Something-Something-v2, resulting in approximately 2 million videos.", "source_file": P},
  {"id": "data_readme", "quote": "V-JEPA models are trained by passively watching video pixels from the VideoMix2M dataset", "source_file": GR},
  {"id": "data_cfg_ht", "quote": "- /your_path_to_howto100m_csv_file_index.csv", "source_file": CFG},
  {"id": "ht_youtube", "quote": "HowTo100M features 1.22 million videos from YouTube, with activities from domains such as cooking, hand crafting, personal care, gardening, etc.", "source_file": HT},
  {"id": "ht_health", "quote": "Health 172 1.7M Emotional Health 63 853k Conditions and Treatments 35 271k Injury and Accidents 22 147k Medication and Equipment 20 138k", "source_file": HT},
  {"id": "ht_medinfo", "quote": "Medical Information 3 31k", "source_file": HT},
  {"id": "data_kin_abs", "quote": "The dataset contains 400 human action classes, with at least 400 video clips for each action. Each clip lasts around 10s and is taken from a different YouTube video.", "source_file": KABS},
  {"id": "data_ssv2_abs", "quote": "We also describe the challenges in crowd-sourcing this data at scale.", "source_file": SABS},
  {"id": "in_res", "quote": "The ViT-L/16 and ViT-H/16 process the video at a spatial resolution of 224, while the ViT-H/16 384 uses an input resolution of 384", "source_file": P},
  {"id": "in_stride", "quote": "during pretraining, we always randomly sample a clip of 16 frames from each input video with a temporal stride of 4 between sampled frames. An input video clip therefore covers 64 frames in total, or roughly 2 seconds of a given video running at 30 frames per second.", "source_file": P},
  {"id": "in_patch", "quote": "V-JEPA flattens the video clip into a sequence of non-overlapping spatio-temporal patches of size 16 × 16 × 2 16\\times 16\\times 2", "source_file": P},
  {"id": "in_cfg_nf", "quote": "num_frames: 16", "source_file": CFG},
  {"id": "in_cfg_tub", "quote": "tubelet_size: 2", "source_file": CFG},
  {"id": "in_cfg_sr", "quote": "sampling_rate: 4", "source_file": CFG},
  {"id": "in_cfg_crop", "quote": "crop_size: 224", "source_file": CFG},
  {"id": "in_cfg_ps", "quote": "patch_size: 16", "source_file": CFG},
  {"id": "in_vitl", "quote": "def vit_large(patch_size=16, **kwargs): model = VisionTransformer( patch_size=patch_size, embed_dim=1024, depth=24,", "source_file": VT},
  {"id": "in_vith", "quote": "def vit_huge(patch_size=16, **kwargs): model = VisionTransformer( patch_size=patch_size, embed_dim=1280, depth=32,", "source_file": VT},
  {"id": "par_hdr", "quote": "Method Arch. Params. Data", "source_file": P},
  {"id": "par_row", "quote": "V-JEPA ViT-L/16 200M VideoMix2M 80.8 69.5 25.6 74.8 60.3 67.8 ViT-H/16 630M 82.0 71.4 25.8 75.9 61.7 67.9 ViT-H/16 384 630M", "source_file": P}
 ]
}
save_record(rec)
