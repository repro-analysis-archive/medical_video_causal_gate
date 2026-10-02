import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "larp_hywang66__LARP-L-long-tokenizer_hfapi.json"; HF = "larp_hf_README.md"; C = "larp_hf_config.json"
RM = "larp_github_README.md"; LIC = "larp_github_LICENSE.txt"; SH = "larp_github_train_larp_tokenizer_reproduce.sh.txt"
P = "larp_arxiv_2410.21264_fulltext.txt"
DATA_FILES = [P, RM, SH]

rec = {
 "id": "21_larp_tokenizer",
 "name": "LARP video tokenizer (LARP-L-Long-tokenizer; HF hywang66/LARP-L-long-tokenizer)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "hywang66/LARP-L-long-tokenizer, model.safetensors + config.json (HF repo created 2024-10-23); reproduce script scripts/train_larp_tokenizer_reproduce.sh; paper arXiv:2410.21264v2 (ICLR 2025)",
 "paper": {"title": "LARP: Tokenizing Videos with a Learned Autoregressive Generative Prior", "year": 2024, "arxiv": "2410.21264"},
 "weights_location": {
  "urls": ["https://huggingface.co/hywang66/LARP-L-long-tokenizer"],
  "files_listed": {"model.safetensors": 785007336, "config.json": 1773},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; the official GitHub README links the repo (first author's account); nothing downloaded",
  "quote_ids": ["w_file", "w_gated", "w_readme"]
 },
 "licence": {
  "id": "MIT (GitHub repository LICENSE); the HF card carries no licence tag",
  "url": "https://github.com/hywang66/LARP/blob/main/LICENSE",
  "commercial": "permitted", "non_commercial_only": False, "restrictions": "none beyond MIT",
  "gating": "none", "quote_ids": ["lic_mit", "lic_copy", "lic_hf_links"]
 },
 "domain": {"value": "discrete holistic video tokenizer for autoregressive video generative models (trained jointly with a small AR prior); trained on Kinetics-600 + UCF-101", "quote_ids": ["dom_readme", "data_csv"]},
 "architecture": {"type": "ViT encoder with learned holistic queries (patchify 4x8x8) -> VQ bottleneck (codebook 8192, 16-dim, L2-normalised) -> ViT decoder; AR prior (21.7M) used only in training",
                  "representation": "1024 holistic discrete tokens per 16x128x128 clip (not spatially aligned), each a 16-dim code vector; encoder hidden size 768"},
 "pretraining_data": {"summary": "Released tokenizer trained on k600_train.csv + ucf101_train.csv (Kinetics-600 train + UCF-101 train), 16-frame 128x128 clips (reproduce script; paper section 4.1).",
                      "form": "dataset list (named: Kinetics-600, UCF-101)"},
 "pretraining_data_quote": {"quote_ids": ["data_csv", "data_repro", "data_paper"]},
 "medical_video_in_data": {"answer": "NO", "basis": "closed list of named human-action datasets (Kinetics-600, UCF-101); term search finds no medical/surgical data statement",
                           "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}},
 "appendix300_possible": {"answer": "NO", "basis_class": "closed_curated_list",
  "basis": "Kinetics-600 + UCF-101 only (closed fixed action-class research datasets -> NO under conventions_v2). Timing: released 2024-10, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_csv"]},
 "appendix300_check": {
  "answer": "NO", "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "closed_curated_list", "basis": "Kinetics-600 + UCF-101 training CSVs",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_csv"]
 },
 "input": {
  "frame_size": {"value": "128x128 (training and evaluation)", "quote_ids": ["data_paper", "in_size"]},
  "frame_rate_or_sampling": {"value": "not documented in the saved sources", "quote_ids": []},
  "clip_length_frames": {"value": "16", "quote_ids": ["data_paper", "in_frames"]},
  "temporal_compression": {"value": "patchify stride 4 in time (holistic tokens are not a temporal grid)", "quote_ids": ["in_patch"]},
  "spatial_compression": {"value": "patchify 8x8 (1024 patches per clip, then mapped to 1024 holistic tokens)", "quote_ids": ["in_patch"]}
 },
 "embedding_dim": {"value": "1024 tokens x 16-dim quantised code vectors (codebook 8192) = 16,384 values per 16x128x128 clip; pre-quantisation encoder token width 768",
                   "derivation": "bottleneck_token_num 1024, bottleneck_dim 16, codebook_size 8192, encoder_hidden_size 768 (config.json)", "quote_ids": ["in_ntok", "in_bdim", "in_cb", "in_hid"]},
 "params": {"value": "173M tokenizer (encoder + decoder; encoder-only count not documented)", "scope": "whole tokenizer", "quote_ids": ["w_readme", "p_table"]},
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs statement for the tokenizer in the saved paper/README",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists model.safetensors, gated=False; linked from the official README", "quote_ids": ["w_file", "w_gated", "w_readme"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "MIT licence in the official repository (HF card has no licence field; the card links that repository)", "quote_ids": ["lic_mit", "lic_hf_links"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video tokenizer (reconstruction autoencoder) of an autoregressive video generative model, trained on general video", "quote_ids": ["dom_readme"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "the reproduce script for the released checkpoint and the paper name Kinetics-600 and UCF-101", "quote_ids": ["data_csv", "data_repro", "data_paper"]},
  "eligible": "YES (all four criteria PASS; Appendix300 NO; licence via the GitHub repo, not the HF card)"
 },
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"model.safetensors\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "w_readme", "quote": "| LARP-L-Long-tokenizer | 173M | 20 (recon.) | [link](https://huggingface.co/hywang66/LARP-L-long-tokenizer) |", "source_file": RM},
  {"id": "lic_mit", "quote": "MIT License", "source_file": LIC},
  {"id": "lic_copy", "quote": "Copyright (c) 2024 Hanyu Wang", "source_file": LIC},
  {"id": "lic_hf_links", "quote": "- Github: https://github.com/hywang66/LARP", "source_file": HF},
  {"id": "dom_readme", "quote": "We present LARP, a novel video tokenizer inherently aligned with autoregressive (AR) generative models.", "source_file": RM},
  {"id": "data_repro", "quote": "# It can reproduce the pretrained model hywang66/LARP-L-long-tokenizer released on HuggingFace.", "source_file": SH},
  {"id": "data_csv", "quote": "--csv_file k600_train.csv+ucf101_train.csv", "source_file": SH},
  {"id": "data_paper", "quote": "4.1 Setup Dataset. We conduct video reconstruction and generation experiments using the Kinetics-600 (K600) ( Carreira et al., 2018 ) and UCF-101 ( Soomro, 2012 ) datasets. In all experiments, we use 16-frame video clips with a spatial resolution of 128 × 128 128{\\times}128 for both training and evaluation", "source_file": P},
  {"id": "in_frames", "quote": "--frame_num 16 --input_size 128", "source_file": SH},
  {"id": "in_size", "quote": "\"input_size\": 128,", "source_file": C},
  {"id": "in_patch", "quote": "In all experiments, the patch sizes are set to f T = 4 f_{T}=4 , f H = 8 f_{H}=8 , and f W = 8 f_{W}=8 , respectively. As a result, a 16 × 128 × 128 16{\\times}128{\\times}128 video clip is split into 4 × 16 × 16 = 1024 4{\\times}16{\\times}16=1024 video patches", "source_file": P},
  {"id": "in_ntok", "quote": "\"bottleneck_token_num\": 1024,", "source_file": C},
  {"id": "in_bdim", "quote": "\"bottleneck_dim\": 16,", "source_file": C},
  {"id": "in_cb", "quote": "\"codebook_size\": 8192,", "source_file": C},
  {"id": "in_hid", "quote": "\"encoder_hidden_size\": 768,", "source_file": C},
  {"id": "p_table", "quote": "LARP-L-Long (Ours) 173M 343M 1024 20 6.2 102", "source_file": P}
 ]
}
save_record(rec)
