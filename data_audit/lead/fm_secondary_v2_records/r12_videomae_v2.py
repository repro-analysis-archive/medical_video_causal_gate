import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

A_B = "videomaev2_OpenGVLab__VideoMAEv2-Base_hfapi.json"; A_G = "videomaev2_OpenGVLab__VideoMAEv2-giant_hfapi.json"
A_L = "videomaev2_OpenGVLab__VideoMAEv2-Large_hfapi.json"; A_H = "videomaev2_OpenGVLab__VideoMAEv2-Huge_hfapi.json"
A_2 = "videomaev2_OpenGVLab__VideoMAE2_hfapi.json"
CB = "videomaev2_VideoMAEv2-Base_README.md"; CG = "videomaev2_VideoMAEv2-giant_README.md"; C2R = "videomaev2_VideoMAE2_README.md"
CFB = "videomaev2_VideoMAEv2-Base_config.json"; CFG = "videomaev2_VideoMAEv2-giant_config.json"
CFL = "videomaev2_VideoMAEv2-Large_config.json"; CFH = "videomaev2_VideoMAEv2-Huge_config.json"
GR = "videomaev2_github_README.md"; MZ = "videomaev2_github_MODEL_ZOO.md"; LIC = "videomaev2_github_LICENSE.txt"
DS = "videomaev2_github_DATASET.md"; P = "videomaev2_arxiv_2303.16727v2.txt"; P1 = "videomae_arxiv_2203.12602v3.txt"
DATA_FILES = [CB, CG, P, DS, MZ]

rec = {
 "id": "12_videomae_v2",
 "name": "VideoMAE V2 (OpenGVLab; dual-masking video masked autoencoder, ViT-B/L/H/g pre-trained on UnlabeledHybrid)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "Primary: HF OpenGVLab/VideoMAEv2-giant (ViT-g/14, 1,011M params, UnlabeledHybrid 1200 epochs, encoder only, feature extraction; repo sha d27568eb41ccb2d41bb191fc2e3fe5aad74942d4, 2025-01-14). Same series: OpenGVLab/VideoMAEv2-Base (800 ep), -Large (800 ep), -Huge (1200 ep), and the full pretrain checkpoint mae-g/vit_g_hybrid_pt_1200e.pth in OpenGVLab/VideoMAE2. NOT in scope of this entry: the K710 fine-tuned ViT-g checkpoints and the distilled ViT-S/ViT-B (vit_*_k710_dl_from_giant.pth: supervised distillation from the K710-fine-tuned teacher, not masked-autoencoder pretraining).",
 "paper": {"title": "VideoMAE V2: Scaling Video Masked Autoencoders with Dual Masking", "year": 2023, "venue": "CVPR 2023", "arxiv": "2303.16727 (v2 used)",
           "note": "the HF VideoMAEv2-* cards link the paper title to arXiv 2203.12602 (VideoMAE v1) -- a card mislink; the BibTeX in the same cards gives eprint 2303.16727"},
 "weights_location": {
  "urls": ["https://huggingface.co/OpenGVLab/VideoMAEv2-giant", "https://huggingface.co/OpenGVLab/VideoMAEv2-Huge",
           "https://huggingface.co/OpenGVLab/VideoMAEv2-Large", "https://huggingface.co/OpenGVLab/VideoMAEv2-Base",
           "https://huggingface.co/OpenGVLab/VideoMAE2 (mae-g/vit_g_hybrid_pt_1200e.pth)"],
  "files_listed": {"VideoMAEv2-giant model.safetensors": 4105286120, "VideoMAEv2-Huge model.safetensors": 2526470968,
                   "VideoMAEv2-Large model.safetensors": 1215474840, "VideoMAEv2-Base model.safetensors": 344924592,
                   "VideoMAE2 mae-g/vit_g_hybrid_pt_1200e.pth": 4105433973},
  "gated": False, "private": False,
  "verified_how": "HF API model listings (metadata only) saved as " + ", ".join([A_G, A_H, A_L, A_B, A_2]) + "; nothing downloaded",
  "note": "The GitHub MODEL_ZOO directs users to a Google 'VideoMAE V2 Download Request Form' for the ViT-g weights; the same official organisation (OpenGVLab) also lists the pretrain weights publicly and ungated on HF, which is what C1 is judged on.",
  "quote_ids": ["w_file_g", "w_gated_g", "w_file_b", "w_file_pt", "w_gated_2", "w_form"]
 },
 "licence": {
  "id": "CC-BY-NC-4.0 (HF VideoMAEv2-* cards); GitHub repo LICENSE = MIT; HF OpenGVLab/VideoMAE2 card = apache-2.0 (inconsistent tags; the most restrictive, CC-BY-NC-4.0, is assumed for the VideoMAEv2-* weights)",
  "url": "https://huggingface.co/OpenGVLab/VideoMAEv2-giant ; https://github.com/OpenGVLab/VideoMAEv2/blob/master/LICENSE ; https://huggingface.co/OpenGVLab/VideoMAE2",
  "commercial": "not permitted under CC-BY-NC-4.0 (the MIT/Apache tags would permit it; unresolved inconsistency)",
  "non_commercial_only": True,
  "restrictions": "non-commercial (assumed); attribution",
  "gating": "none at HF level (GitHub route uses a request form)",
  "quote_ids": ["lic_card_b", "lic_card_g", "lic_mit", "lic_vm2"]
 },
 "domain": {
  "value": "masked video autoencoder (VideoMAE with dual masking: encoder tube masking 90% + decoder running-cell masking; MSE reconstruction of masked pixel cubes), self-supervised on a 1.35M-clip general-video mix (UnlabeledHybrid)",
  "quote_ids": ["dom_dual", "dom_mse", "dom_card_feat", "data_card_g"]
 },
 "architecture": {
  "type": "vanilla ViT (joint space-time attention) on 2x14x14 (ViT-g) or 2x16x16 (B/L/H) cube tokens; 4-block 512-dim decoder used only in pretraining (HF VideoMAEv2-* repos are encoder-only)",
  "representation": "encoder output tokens (1408-dim for ViT-g; 1280 H, 1024 L, 768 B) or a pooled vector of the same dimension"
 },
 "pretraining_data": {
  "summary": "UnlabeledHybrid, ~1.35M clips: K710 (658k, YouTube; union of K400/600/700), SSv2 (169k, shot from scripts), AVA (21k, movies), WebVid2M subset (250k, 'scraped from the internet'), self-collected Instagram (250k, 'uncurated videos crawled from Instagram'). Named sources; the Instagram part is a non-public self-crawl.",
  "form": "dataset/source list (named, includes open-ended web/Instagram sources)"
 },
 "pretraining_data_quote": {"quote_ids": ["data_select", "data_t8", "data_k710", "data_ssv2", "data_ava", "data_webvid", "data_ig", "data_total", "data_webvid_app", "data_ig_uncur", "data_card_g"]},
 "medical_video_in_data": {
  "answer": "NOT MENTIONED",
  "basis": "Term search of the cards, paper and GitHub data docs found no medical/surgical term; WebVid2M and the self-crawled Instagram clips are open-ended web content whose categories are not documented.",
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}
 },
 "appendix300_possible": {
  "answer": "UNKNOWN", "basis_class": "named_open_web_sources",
  "basis": "Besides closed benchmarks (Kinetics, SSv2, AVA), UnlabeledHybrid contains WebVid2M (internet stock footage) and 250k 'uncurated videos crawled from Instagram': named but open-ended sources, so the documentation does not allow the Appendix300 source recordings to be excluded. Timing: paper 2023-03, HF weights 2024-08 / 2025-01, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_webvid_app", "data_ig_uncur", "data_ig"]
 },
 "appendix300_check": {
  "answer": "UNKNOWN",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "named_open_web_sources",
  "basis": "open-ended WebVid2M and self-crawled Instagram components; see appendix300_possible",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_webvid_app", "data_ig_uncur"]
 },
 "input": {
  "frame_size": {"value": "224x224 (all models; config img_size 224)", "quote_ids": ["in_img_g", "in_res_zoo", "in_t7_data"]},
  "frame_rate_or_sampling": {"value": "16 frames with sampling interval 2 for SSv2 videos and 4 for the other UnlabeledHybrid sources (source fps not fixed)", "quote_ids": ["in_interval"]},
  "clip_length_frames": {"value": "16 frames", "quote_ids": ["in_nf_g", "in_t7_data"]},
  "temporal_compression": {"value": "tubelet 2 frames (16 -> 8 token slices)", "quote_ids": ["in_tub_b", "in_t7_cube"]},
  "spatial_compression": {"value": "14x14 patches for ViT-g (224 -> 16x16 = 256 tokens per slice); 16x16 patches for ViT-B/L/H (224 -> 14x14 = 196)", "quote_ids": ["in_patch_g", "in_patch_b", "in_t7_cube"]}
 },
 "embedding_dim": {
  "value": "ViT-g: 1408 x (8 x 16 x 16) = 1408 x 2048 tokens per 16-frame 224x224 clip; pooled 1408. ViT-H 1280 x 1568; ViT-L 1024 x 1568; ViT-B 768 x 1568 (pooled = embed_dim; VideoMAEv2-Base config use_mean_pooling true)",
  "derivation": "embed_dim from HF configs; Table 7 cube output 1408 x 8 x 256 for ViT-g",
  "quote_ids": ["in_emb_g", "in_emb_b", "in_t7_cube", "in_meanpool_b"]
 },
 "params": {
  "value": "ViT-g 1,011M (paper); ViT-B/L/H backbones = VideoMAE v1 architectures (87M / 305M / 633M per VideoMAE paper Table 7, incl. task head); HF VideoMAEv2-giant model.safetensors 4.105 GB fp32 ~ 1.03B (inferred, consistent)",
  "scope": "encoder (ViT-g backbone)",
  "quote_ids": ["par_g", "par_v1_hdr", "par_v1_b", "par_v1_h"]
 },
 "flops_per_input_if_documented": {
  "value": "ViT-g: 38.16 TFLOPs for 5x3 views of 16x224x224 on K400 = ~2.54 TFLOPs per view (division inferred; the table's 'TFLOPs' column is the multi-view total: VideoMAE ViT-H 17.88 = 1192 GFLOPs x 15). ViT-H: 17.88 TFLOPs / 15 views = 1.19 TFLOPs per view.",
  "quote_ids": ["fl_hdr", "fl_g", "fl_h", "fl_v1"]
 },
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "official OpenGVLab HF repos list model.safetensors / vit_g_hybrid_pt_1200e.pth with gated=False (the GitHub request-form route is an alternative, not the only route)", "quote_ids": ["w_file_g", "w_gated_g", "w_file_pt", "w_form"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "CC-BY-NC-4.0 (most restrictive tag) permits non-commercial research; MIT / Apache tags also present", "quote_ids": ["lic_card_g", "lic_mit"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "masked video autoencoder with a pixel-cube MSE reconstruction objective on general video -> PASS under the v1 convention", "quote_ids": ["dom_dual", "dom_mse"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "paper Table 8 lists the components and sources of UnlabeledHybrid (K710, SSv2, AVA, WebVid2M, self-collected Instagram); caveat: the Instagram subset is a non-public self-crawl named only by provider", "quote_ids": ["data_select", "data_t8", "data_ig"]},
  "eligible": "YES (all four criteria PASS; licence tags inconsistent, CC-BY-NC assumed; Appendix300 UNKNOWN)"
 },
 "quotes": [
  {"id": "w_file_g", "quote": "\"rfilename\": \"model.safetensors\",", "source_file": A_G},
  {"id": "w_gated_g", "quote": "\"gated\": false,", "source_file": A_G},
  {"id": "w_file_b", "quote": "\"rfilename\": \"model.safetensors\",", "source_file": A_B},
  {"id": "w_file_pt", "quote": "\"rfilename\": \"mae-g/vit_g_hybrid_pt_1200e.pth\",", "source_file": A_2},
  {"id": "w_gated_2", "quote": "\"gated\": false,", "source_file": A_2},
  {"id": "w_form", "quote": "Please fill out [VideoMAE V2 Download Request Form](https://docs.google.com/forms/d/e/1FAIpQLSd1SjKMtD8piL9uxGEUwicerxd46bs12QojQt92rzalnoI3JA/viewform?usp=sf_link), **you will see the download link** for the VideoMAE V2 model weights after submission.", "source_file": MZ},
  {"id": "lic_card_b", "quote": "license: cc-by-nc-4.0", "source_file": CB},
  {"id": "lic_card_g", "quote": "license: cc-by-nc-4.0", "source_file": CG},
  {"id": "lic_mit", "quote": "MIT License Copyright (c) 2023 OpenGVLab", "source_file": LIC},
  {"id": "lic_vm2", "quote": "license: apache-2.0", "source_file": C2R},
  {"id": "dom_dual", "quote": "we propose to mask the decoder as well and devise the dual masking strategy.", "source_file": P},
  {"id": "dom_mse", "quote": "VideoMAE v2 does not reconstruct the full video clip, while only calculates MSE loss on tokens that are invisible to the encoder.", "source_file": P},
  {"id": "dom_card_feat", "quote": "You can use the raw model for video feature extraction.", "source_file": CG},
  {"id": "data_card_g", "quote": "VideoMAEv2-giant model pre-trained for 1200 epochs in a self-supervised way on UnlabeldHybrid-1M dataset.", "source_file": CG},
  {"id": "data_select", "quote": "Specifically, our dataset is built by simply selecting videos from the public available datasets of Kinetics [43], Something-Something [31], AVA [32], WebVid2M [5], and our own crawled Instagram dataset.", "source_file": P},
  {"id": "data_t8", "quote": "Table 8. Components of UnlabeledHybrid.", "source_file": P},
  {"id": "data_k710", "quote": "K710 658k YouTube", "source_file": P},
  {"id": "data_ssv2", "quote": "SSV2 169k Shot from Scripts", "source_file": P},
  {"id": "data_ava", "quote": "AVA 21k Movie", "source_file": P},
  {"id": "data_webvid", "quote": "WebVid2M 250k Internet", "source_file": P},
  {"id": "data_ig", "quote": "self-collected 250k Instagram", "source_file": P},
  {"id": "data_total", "quote": "UnlabeledHybrid 1.348M Multi-Source", "source_file": P},
  {"id": "data_webvid_app", "quote": "WebVid2M. Videos in WebVid2M are scraped from the internet.", "source_file": P},
  {"id": "data_ig_uncur", "quote": "We collect videos from the public datasets of Kinetics, Something-Something, AVA, WebVid, and uncurated videos crawled from Instagram.", "source_file": P},
  {"id": "in_img_g", "quote": "\"img_size\": 224,", "source_file": CFG},
  {"id": "in_nf_g", "quote": "\"num_frames\": 16,", "source_file": CFG},
  {"id": "in_patch_g", "quote": "\"patch_size\": 14,", "source_file": CFG},
  {"id": "in_patch_b", "quote": "\"patch_size\": 16,", "source_file": CFB},
  {"id": "in_tub_b", "quote": "\"tubelet_size\": 2,", "source_file": CFB},
  {"id": "in_emb_g", "quote": "\"embed_dim\": 1408,", "source_file": CFG},
  {"id": "in_emb_b", "quote": "\"embed_dim\": 768,", "source_file": CFB},
  {"id": "in_meanpool_b", "quote": "\"use_mean_pooling\": true,", "source_file": CFB},
  {"id": "in_res_zoo", "quote": "all the input resolution is $224^2$.", "source_file": MZ},
  {"id": "in_interval", "quote": "We set **different sampling intervals** for the videos from different sources in unlabeledhybrid: 2 for SSv2 and 4 for the other datasets.", "source_file": MZ},
  {"id": "in_t7_data", "quote": "UnlabeldHybrid 3 × 16 × 224 × 224", "source_file": P},
  {"id": "in_t7_cube", "quote": "1408 × 8 × 256", "source_file": P},
  {"id": "par_g", "quote": "It has 1,011M parameters.", "source_file": P},
  {"id": "par_v1_hdr", "quote": "Method Backbone Extra data Ex. labels Frames GFLOPs Param Top-1 Top-5", "source_file": P1},
  {"id": "par_v1_b", "quote": "VideoMAE ViT-B 7 16 180×5×3 87 81.5 95.1", "source_file": P1},
  {"id": "par_v1_h", "quote": "VideoMAE ViT-H 7 16 1192×5×3 633 86.6 97.1", "source_file": P1},
  {"id": "fl_hdr", "quote": "Method Top 1 Top 5 Views TFLOPs", "source_file": P},
  {"id": "fl_g", "quote": "VideoMAE V2-g 88.5 98.1 5×3 38.16", "source_file": P},
  {"id": "fl_h", "quote": "VideoMAE V2-H 88.6 97.9 5×3 17.88", "source_file": P},
  {"id": "fl_v1", "quote": "VideoMAE [90] 86.6 97.1 5×3 17.88", "source_file": P}
 ]
}
save_record(rec)
