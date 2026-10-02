import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API_B = "videomae_MCG-NJU__videomae-base_hfapi.json"; API_L = "videomae_MCG-NJU__videomae-large_hfapi.json"
API_S = "videomae_MCG-NJU__videomae-base-ssv2_hfapi.json"; API_BS = "videomae_MCG-NJU__videomae-base-short_hfapi.json"
CB = "videomae_videomae-base_README.md"; CL = "videomae_videomae-large_README.md"; CS = "videomae_videomae-base-ssv2_README.md"
CBS = "videomae_videomae-base-short_README.md"
CFB = "videomae_videomae-base_config.json"; CFL = "videomae_videomae-large_config.json"
GR = "videomae_github_README.md"; MZ = "videomae_github_MODEL_ZOO.md"; LIC = "videomae_github_LICENSE.txt"
PT = "videomae_github_PRETRAIN.md"; DS = "videomae_github_DATASET.md"; P = "videomae_arxiv_2203.12602v3.txt"
K400 = "kinetics400_label_map_mmaction2.txt"; KABS = "kinetics_arxiv_1705.06950_abs.txt"; SABS = "ssv2_arxiv_1706.04261_abs.txt"
DATA_FILES = [CB, CL, CS, CBS, P, DS, MZ, KABS, SABS, K400]

rec = {
 "id": "11_videomae",
 "name": "VideoMAE (MCG-NJU; masked video autoencoder, ViT + pixel-reconstruction decoder; pretrain-only checkpoints)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "Primary: HF MCG-NJU/videomae-base (ViT-B/16, Kinetics-400, 1600 epochs, pre-trained only; repo sha dc740ceda42fce44faed2ea03c6d447db72f6af9). Also pretrain-only on HF: MCG-NJU/videomae-large (ViT-L, K400, 1600 ep), MCG-NJU/videomae-base-short (ViT-B, K400, 800 ep), MCG-NJU/videomae-base-ssv2 (ViT-B, SSv2, 2400 ep). ViT-S/ViT-H and UCF101 pretrain checkpoints are linked from the GitHub MODEL_ZOO on Google Drive (not verified file-by-file).",
 "paper": {"title": "VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training", "year": 2022,
           "venue": "NeurIPS 2022", "arxiv": "2203.12602 (v3 used)"},
 "weights_location": {
  "urls": ["https://huggingface.co/MCG-NJU/videomae-base", "https://huggingface.co/MCG-NJU/videomae-large",
           "https://huggingface.co/MCG-NJU/videomae-base-short", "https://huggingface.co/MCG-NJU/videomae-base-ssv2",
           "https://github.com/MCG-NJU/VideoMAE/blob/main/MODEL_ZOO.md (Google Drive links)"],
  "files_listed": {"videomae-base model.safetensors": 376873760, "videomae-large model.safetensors": 1372055288,
                   "videomae-base-short model.safetensors": 376873760, "videomae-base-ssv2 model.safetensors": 376873760},
  "gated": False, "private": False,
  "verified_how": "HF API model listings (metadata only) saved as " + ", ".join([API_B, API_L, API_BS, API_S]) + "; nothing downloaded",
  "quote_ids": ["w_file_b", "w_gated_b", "w_file_l", "w_gated_l", "w_file_s", "w_gated_s", "w_zoo"]
 },
 "licence": {
  "id": "CC-BY-NC-4.0 (HF card licence tag; GitHub repo LICENSE = Attribution-NonCommercial 4.0 International)",
  "url": "https://huggingface.co/MCG-NJU/videomae-base ; https://github.com/MCG-NJU/VideoMAE/blob/main/LICENSE",
  "commercial": "not permitted (NonCommercial)", "non_commercial_only": True,
  "restrictions": "non-commercial use only; attribution required; portions of the code under Apache-2.0 / MIT",
  "gating": "none", "quote_ids": ["lic_card", "lic_readme", "lic_text"]
 },
 "domain": {
  "value": "masked video autoencoder (ViT encoder + shallow decoder predicting normalized pixels of masked space-time cubes; MSE in pixel space), self-supervised on general human-action video (Kinetics-400 / Something-Something V2)",
  "quote_ids": ["dom_card", "dom_mse", "dom_fig1", "data_card_b"]
 },
 "architecture": {
  "type": "vanilla ViT (joint space-time attention) encoder on 2x16x16 cube tokens, tube masking 90%; 4-layer (ViT-B) / 12-layer (ViT-L) decoder for pixel reconstruction (pretraining only)",
  "representation": "encoder output tokens (768-dim per cube for ViT-B, 1024 for ViT-L) or their mean / [CLS]-style pooled vector; decoder not needed for features"
 },
 "pretraining_data": {
  "summary": "Each released checkpoint is pre-trained on ONE named public benchmark, without labels: Kinetics-400 (~240k 10-s YouTube clips, 400 human-action classes) for videomae-base/-large/-base-short; Something-Something V2 (~169k crowd-sourced clips, 174 motion-centric classes) for videomae-base-ssv2; UCF101 for one Google-Drive checkpoint. No extra data ('no external data').",
  "form": "dataset list (named, closed)"
 },
 "pretraining_data_quote": {"quote_ids": ["data_card_b", "data_card_l", "data_card_s", "data_t7", "data_k400_ssv2", "data_kin_abs", "data_ssv2_abs"]},
 "medical_video_in_data": {
  "answer": "NO",
  "basis": "Closed list of named non-medical datasets (Kinetics-400 human-action classes; SSv2 crowd-sourced everyday-object actions). Term search of the cards, paper, DATASET.md, dataset abstracts and the Kinetics-400 class list (mmaction2 label_map_k400.txt, 400 classes) found no medical/surgical term; the nearest classes are 'bandaging' (first aid), 'massaging ...', 'getting a tattoo', 'brushing teeth' (searched separately; none is surgical/endoscopic).",
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)},
  "class_list_search": {"pattern": "surg|medic|operat|endoscop|laparo|hospital|doctor|dentist|clinic|nurs|patient|health|appendi",
                        "hits": term_search([K400], r"surg|medic|operat|endoscop|laparo|hospital|doctor|dentist|clinic|nurs|patient|health|appendi")},
  "quote_ids": ["k400_bandaging"]
 },
 "appendix300_possible": {
  "answer": "NO", "basis_class": "closed_curated_list",
  "basis": "Pretraining video = Kinetics-400 or Something-Something V2 (or UCF101), closed named curated research benchmarks with fixed human-action / crowd-sourced class scopes that exclude surgical recordings (v1 convention example 'fixed action-class or crowd-sourced benchmarks'; conventions_v2 clarification: Kinetics treated as closed although its clips come from YouTube). Timing: paper 2022-03, HF weights 2022-07/08, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_k400_ssv2", "data_kin_abs", "data_ssv2_abs", "data_t7"]
 },
 "appendix300_check": {
  "answer": "NO",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "closed_curated_list",
  "basis": "closed list (K400 / SSv2 / UCF101 action benchmarks) whose documented class scope excludes surgical recordings; Kinetics-400 class list term-searched (no surgical/medical class).",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["data_k400_ssv2", "data_kin_abs", "data_ssv2_abs"]
 },
 "input": {
  "frame_size": {"value": "224x224 (config image_size 224; input 3x16x224x224)", "quote_ids": ["in_img", "in_t8"]},
  "frame_rate_or_sampling": {"value": "16 frames sampled with temporal stride tau = 4 on Kinetics-400 and tau = 2 on SSv2 (source-video fps not fixed)", "quote_ids": ["in_stride", "in_sr4"]},
  "clip_length_frames": {"value": "16 frames (config num_frames 16)", "quote_ids": ["in_nf"]},
  "temporal_compression": {"value": "tubelet 2 frames (16 frames -> 8 token slices)", "quote_ids": ["in_tub", "in_cube"]},
  "spatial_compression": {"value": "16x16 patches (224x224 -> 14x14 = 196 tokens per slice)", "quote_ids": ["in_patch", "in_cube"]}
 },
 "embedding_dim": {
  "value": "ViT-B: 768 x (8 x 14 x 14) = 768 x 1568 tokens per 16-frame 224x224 clip; pooled clip vector 768. ViT-L: 1024 x 1568; pooled 1024.",
  "derivation": "hidden_size 768 (ViT-B) / 1024 (ViT-L); Table 8 cube output 768x8x196; pooled dim = hidden size (card: last hidden state of the [CLS]-position token / mean pooling)",
  "quote_ids": ["in_hid_b", "in_hid_l", "in_t8", "in_cube", "dom_cls"]
 },
 "params": {
  "value": "ViT-B 87M, ViT-L 305M, ViT-H 633M, ViT-S 22M (paper Table 7 'Param', backbone as fine-tuned, i.e. encoder + classification head); encoder-only count of the pretrain checkpoint (with decoder) not separately documented; HF videomae-base model.safetensors 376.9 MB fp32 ~ 94M incl. decoder (inferred)",
  "scope": "encoder (+ task head) as reported in the transfer tables",
  "quote_ids": ["fl_hdr", "fl_b", "fl_l", "fl_h"]
 },
 "flops_per_input_if_documented": {
  "value": "ViT-B 180 GFLOPs, ViT-L 597, ViT-H 1192, ViT-S 57 per view of 16 frames at 224x224 (Table 7; 'x5x3' = 5 clips x 3 crops at test time)",
  "quote_ids": ["fl_hdr", "fl_b", "fl_l", "fl_h", "fl_cap"]
 },
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists model.safetensors for videomae-base / -large / -base-ssv2, gated=False", "quote_ids": ["w_file_b", "w_gated_b"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "CC-BY-NC-4.0: non-commercial research permitted (restriction recorded)", "quote_ids": ["lic_card", "lic_text"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "masked video autoencoder with a pixel-reconstruction objective trained on general (non-surgical) video -> PASS under the v1 convention", "quote_ids": ["dom_card", "dom_mse"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "card and paper name the single pretraining dataset of each checkpoint (Kinetics-400 / Something-Something V2)", "quote_ids": ["data_card_b", "data_card_s", "data_t7"]},
  "eligible": "YES (all four criteria PASS; non-commercial licence; Appendix300 NO)"
 },
 "quotes": [
  {"id": "w_file_b", "quote": "\"rfilename\": \"model.safetensors\",", "source_file": API_B},
  {"id": "w_gated_b", "quote": "\"gated\": false,", "source_file": API_B},
  {"id": "w_file_l", "quote": "\"rfilename\": \"model.safetensors\",", "source_file": API_L},
  {"id": "w_gated_l", "quote": "\"gated\": false,", "source_file": API_L},
  {"id": "w_file_s", "quote": "\"rfilename\": \"model.safetensors\",", "source_file": API_S},
  {"id": "w_gated_s", "quote": "\"gated\": false,", "source_file": API_S},
  {"id": "w_zoo", "quote": "# VideoMAE Model Zoo", "source_file": MZ},
  {"id": "lic_card", "quote": "license: \"cc-by-nc-4.0\"", "source_file": CB},
  {"id": "lic_readme", "quote": "The majority of this project is released under the CC-BY-NC 4.0 license as found in the [LICENSE](https://github.com/MCG-NJU/VideoMAE/blob/main/LICENSE) file.", "source_file": GR},
  {"id": "lic_text", "quote": "Attribution-NonCommercial 4.0 International", "source_file": LIC},
  {"id": "dom_card", "quote": "VideoMAE is an extension of [Masked Autoencoders (MAE)](https://arxiv.org/abs/2111.06377) to video. The architecture of the model is very similar to that of a standard Vision Transformer (ViT), with a decoder on top for predicting pixel values for masked patches.", "source_file": CB},
  {"id": "dom_cls", "quote": "One typically places a linear layer on top of the [CLS] token, as the last hidden state of this token can be seen as a representation of an entire video.", "source_file": CB},
  {"id": "dom_mse", "quote": "The loss function is mean squared error (MSE) loss between the normalized masked tokens and reconstructed ones in the pixel space", "source_file": P},
  {"id": "dom_fig1", "quote": "Figure 1: VideoMAE performs the task of masking random cubes and reconstructing the missing ones with an asymmetric encoder-decoder architecture.", "source_file": P},
  {"id": "data_card_b", "quote": "VideoMAE model pre-trained on Kinetics-400 for 1600 epochs in a self-supervised way.", "source_file": CB},
  {"id": "data_card_l", "quote": "VideoMAE model pre-trained on Kinetics-400 for 1600 epochs in a self-supervised way.", "source_file": CL},
  {"id": "data_card_s", "quote": "VideoMAE model pre-trained on Something-Something-v2 for 2400 epochs in a self-supervised way.", "source_file": CS},
  {"id": "data_t7", "quote": "Here models are self-supervised pre-trained with a masking ratio of 90% for 1600 epochs on Kinetics-400.", "source_file": P},
  {"id": "data_k400_ssv2", "quote": "The Kinetics-400 contains around 240k training videos and 20k validation videos of 10s from 400 classes. The Something-Something V2 is another large-scale video dataset, having around 169k videos for training and 20k videos for validation. In contrast to Kinetics-400, this dataset contains 174 motion-centric action classes.", "source_file": P},
  {"id": "data_kin_abs", "quote": "The dataset contains 400 human action classes, with at least 400 video clips for each action. Each clip lasts around 10s and is taken from a different YouTube video.", "source_file": KABS},
  {"id": "data_ssv2_abs", "quote": "The database currently contains more than 100,000 videos across 174 classes, which are defined as caption-templates. We also describe the challenges in crowd-sourcing this data at scale.", "source_file": SABS},
  {"id": "k400_bandaging", "quote": "bandaging", "source_file": K400},
  {"id": "in_img", "quote": "\"image_size\": 224,", "source_file": CFB},
  {"id": "in_nf", "quote": "\"num_frames\": 16,", "source_file": CFB},
  {"id": "in_tub", "quote": "\"tubelet_size\": 2,", "source_file": CFB},
  {"id": "in_patch", "quote": "\"patch_size\": 16,", "source_file": CFB},
  {"id": "in_hid_b", "quote": "\"hidden_size\": 768,", "source_file": CFB},
  {"id": "in_hid_l", "quote": "\"hidden_size\": 1024,", "source_file": CFL},
  {"id": "in_stride", "quote": "In experiments, the stride τ is set to 4 and 2 on Kinetics and Something-Something, respectively.", "source_file": P},
  {"id": "in_sr4", "quote": "--sampling_rate 4", "source_file": PT},
  {"id": "in_cube", "quote": "Cube embedding. We adopt the joint space-time cube embedding [3, 22, 39] in our VideoMAE, where we treat each cube of size 2 × 16 × 16 as one token", "source_file": P},
  {"id": "in_t8", "quote": "2×16×16, 768 cube 768×8×196", "source_file": P},
  {"id": "fl_hdr", "quote": "Method Backbone Extra data Ex. labels Frames GFLOPs Param Top-1 Top-5", "source_file": P},
  {"id": "fl_b", "quote": "VideoMAE ViT-B 7 16 180×5×3 87 81.5 95.1", "source_file": P},
  {"id": "fl_l", "quote": "VideoMAE ViT-L 7 16 597×5×3 305 85.2 96.8", "source_file": P},
  {"id": "fl_h", "quote": "VideoMAE ViT-H 7 16 1192×5×3 633 86.6 97.1", "source_file": P},
  {"id": "fl_cap", "quote": "Table 7: Comparison with the state-of-the-art methods on Kinetics-400.", "source_file": P}
 ]
}
save_record(rec)
