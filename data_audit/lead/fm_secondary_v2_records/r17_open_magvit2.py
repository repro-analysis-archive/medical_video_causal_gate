import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

API = "openmagvit2_TencentARC__Open-MAGVIT2-Tokenizer-262144-Video_hfapi.json"
C = "openmagvit2_video_hf_README.md"; R = "openmagvit2_seedvoken_github_README.md"; D = "openmagvit2_seedvoken_docs_Open-MAGVIT2.md"
LIC = "openmagvit2_seedvoken_LICENSE.txt"; P = "openmagvit2_arxiv_2409.04410_fulltext.txt"
CFG = "openmagvit2_seedvoken_npu_ucf101_lfqgan_128_L.yaml.txt"; LD = "openmagvit2_seedvoken_data_ucf101.py.txt"
U = "ucf101_arxiv_1212.0402.txt"
DATA_FILES = [R, D, P, C]

rec = {
 "id": "17_open_magvit2_video",
 "name": "Open-MAGVIT2 video tokenizer (TencentARC SEED-Voken; open re-implementation of the MAGVIT-v2 LFQ tokenizer; Open-MAGVIT2-V-UCF)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "TencentARC/Open-MAGVIT2-Tokenizer-262144-Video, video_128_262144.ckpt (Open-MAGVIT2 V1.2 release 2025-02-09, 'Open-MAGVIT2-V-UCF'); HF repo sha 3d904130dac29dab1df5b79cd490f530e75d5c4c; paper arXiv 2409.04410v3 (2025-02-09). The other Open-MAGVIT2 / IBQ releases are image tokenizers (not video) and are not part of this entry.",
 "paper": {"title": "Open-MAGVIT2: An Open-Source Project Toward Democratizing Auto-regressive Visual Generation", "year": 2024, "arxiv": "2409.04410", "versions": "v3 2025-02-09 (HTML rendering saved; adds the video tokenizer)"},
 "weights_location": {
  "urls": ["https://huggingface.co/TencentARC/Open-MAGVIT2-Tokenizer-262144-Video"],
  "files_listed": {"video_128_262144.ckpt": 2964564510},
  "gated": False, "private": False,
  "verified_how": "HF API model listing (metadata only) saved as " + API + "; linked from the official SEED-Voken docs; nothing downloaded",
  "quote_ids": ["w_file", "w_gated", "w_doc_link", "w_news"]
 },
 "licence": {
  "id": "Apache-2.0 (HF card licence: apache-2.0; SEED-Voken repository LICENSE)",
  "url": "https://huggingface.co/TencentARC/Open-MAGVIT2-Tokenizer-262144-Video ; https://github.com/TencentARC/SEED-Voken/blob/main/LICENSE",
  "commercial": "permitted", "non_commercial_only": False,
  "restrictions": "none beyond Apache-2.0 (UCF-101 / ImageNet dataset terms not audited)",
  "gating": "none",
  "quote_ids": ["lic_card", "lic_text"]
 },
 "domain": {
  "value": "video tokenizer (causal 3D-conv VQGAN-style autoencoder with lookup-free quantization, 2^18 codebook) for auto-regressive video generation; trained on general video (UCF-101 human actions), inflated from an ImageNet image tokenizer",
  "quote_ids": ["dom_official", "dom_features", "dom_setup"]
 },
 "architecture": {
  "type": "MAGVIT-v2-style causal 3D convolutional encoder/decoder (ch 128, ch_mult [1,2,2,4], 4 res blocks), LFQ quantizer with 18-bit codes (n_embed 262144), 3D PatchGAN discriminator; inflated from the 128x128 ImageNet image tokenizer",
  "representation": "encoder output: 18-dim (binary LFQ) code per token on a 5 x 16 x 16 grid for a 17-frame 128x128 clip (token index in 2^18 vocabulary)"
 },
 "pretraining_data": {
  "summary": "Video tokenizer trained on UCF-101 (17-frame 128x128 clips), initialised by inflating the image tokenizer trained on 128x128 ImageNet(-1k).",
  "form": "dataset list (named)"
 },
 "pretraining_data_quote": {"quote_ids": ["data_paper", "data_inflate", "data_readme", "data_table", "data_cfg_init", "ucf_def"]},
 "medical_video_in_data": {
  "answer": "NO",
  "basis": "closed list of named datasets (UCF-101 video, ImageNet images) none of which is medical; the UCF-101 class list (saved paper) has no medical/surgical class.",
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES + [U], MED_TERMS)}
 },
 "appendix300_possible": {
  "answer": "NO",
  "basis_class": "closed_curated_list",
  "basis": "video data = UCF-101 (101 fixed human-action classes, YouTube-sourced, manually curated), image initialisation = ImageNet-1k; closed curated list whose content scope excludes surgical recordings (conventions_v2 clarification). Timing: released 2025-02-09, before the OPARA issue 2026-04-29.",
  "quote_ids": ["data_paper", "ucf_def"]
 },
 "appendix300_check": {
  "answer": "NO",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "closed_curated_list",
  "basis": "UCF-101 + ImageNet-1k only.",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES + [U], A300_TERMS)},
  "quote_ids": ["data_paper", "data_inflate", "ucf_def"]
 },
 "input": {
  "frame_size": {"value": "128x128 (training and evaluation)", "quote_ids": ["data_paper", "in_cfg_size"]},
  "frame_rate_or_sampling": {"value": "17 consecutive frames at the native frame rate (no fps resampling when fps is unset; sample_every_n_frames 1); UCF-101 clips are 25 fps", "quote_ids": ["in_cfg_seq", "in_loader_fps", "in_loader_rand", "ucf_fps"]},
  "clip_length_frames": {"value": "17 frames", "quote_ids": ["data_paper", "in_cfg_seq"]},
  "temporal_compression": {"value": "4x (causal; 17 frames -> 5 latent frames)", "quote_ids": ["data_table", "w_doc_link", "dom_features"]},
  "spatial_compression": {"value": "8x8 (128x128 -> 16x16)", "quote_ids": ["data_table", "w_doc_link"]}
 },
 "embedding_dim": {
  "value": "18-dim LFQ code per token x 5 x 16 x 16 tokens = 23,040 binary values per 17-frame 128x128 clip (1,280 token indices into a 262,144 vocabulary)",
  "derivation": "embed_dim 18 / z_channels 18, n_embed 262144 (config); token grid 5 x 16 x 16 (docs table)",
  "quote_ids": ["emb_cfg", "w_doc_link"]
 },
 "params": {
  "value": "not documented for the video tokenizer (the paper's parameter counts are for the AR transformers 343M-1.5B); checkpoint file 2.96 GB (contents, e.g. EMA/discriminator, not documented)",
  "scope": "not documented",
  "quote_ids": ["arch_cfg"]
 },
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs/MACs statement in the saved paper, docs, README or card (searched FLOP)",
 "eligibility": {
  "C1_open_weights": {"status": "PASS", "basis": "HF API lists video_128_262144.ckpt, gated=False; linked from the official docs", "quote_ids": ["w_file", "w_gated", "w_doc_link"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "Apache-2.0", "quote_ids": ["lic_card", "lic_text"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video tokenizer (pixel-reconstruction VQ autoencoder) for auto-regressive video generation, trained on general (UCF-101 action) video", "quote_ids": ["dom_features", "dom_setup"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "paper and README name the video training dataset (UCF-101) and the ImageNet image-tokenizer initialisation", "quote_ids": ["data_paper", "data_inflate", "data_readme"]},
  "eligible": "YES (all four criteria PASS; caveats: small training set (UCF-101, 13k clips) at 128x128; params not documented; this is a re-implementation, not Google's MAGVIT-v2)"
 },
 "quotes": [
  {"id": "w_file", "quote": "\"rfilename\": \"video_128_262144.ckpt\",", "source_file": API},
  {"id": "w_gated", "quote": "\"gated\": false,", "source_file": API},
  {"id": "w_doc_link", "quote": "|Open-MAGVIT2 | 2D | 5 $\\times$ 16 $\\times$ 16 | 8 | 128 $\\times$ 128 |262144 | 16 | [Video_128_262144](https://huggingface.co/TencentARC/Open-MAGVIT2-Tokenizer-262144-Video/blob/main/video_128_262144.ckpt) |", "source_file": D},
  {"id": "w_news", "quote": "* **[2025.02.09]** We release Open-MAGVIT2 Video tokenizers, which achieves SOTA performance compared to OmniTokenizer, LARP and SweetTokenizer.", "source_file": R},
  {"id": "lic_card", "quote": "license: apache-2.0", "source_file": C},
  {"id": "lic_text", "quote": "Apache License Version 2.0, January 2004", "source_file": LIC},
  {"id": "dom_official", "quote": "This is the official repository for Open-MAGVIT2, an open-source project re-implementing Google's MAGVIT-v2 tokenizer and democratizing autoregressive visual generation with a super large vocabulary (i.e., 2^18).", "source_file": D},
  {"id": "dom_features", "quote": "(3) video tokenizer (2^18 codebook size with 4 $\\times$ 8 $\\times 8$ downsampling rate).", "source_file": D},
  {"id": "dom_setup", "quote": "Video Tokenizer Setup. We extend the image version of tokenizer following ( Yu et al., 2024a ) where the temporally casual 3D convolution serves as the main design.", "source_file": P},
  {"id": "data_paper", "quote": "Following ( Yu et al., 2024a ) , we train our video tokenizer on UCF-101 ( Soomro, 2012 ) . We use 17-frame video clips with a spatial resolution of 128 × \\times 128 for both training and evaluation.", "source_file": P},
  {"id": "data_inflate", "quote": "Simultaneously, we inflate the image tokenizer trained at 128 × \\times 128 imagenet for video modeling.", "source_file": P},
  {"id": "data_readme", "quote": "We use UCF-101 as our Video Dataset", "source_file": R},
  {"id": "data_table", "quote": "Open-MAGVIT2-V-UCF UCF-101 262144 128 × 128 128\\times 128 4 8 × 8 8\\times 8", "source_file": P},
  {"id": "data_cfg_init", "quote": "image_pretrain_path: ../upload_ckpts/Open-MAGVIT2/in1k_128_L/imagenet_128_L.ckpt", "source_file": CFG},
  {"id": "ucf_def", "quote": "It consists of 101 action classes, over 13k clips and 27 hours of video data. The database consists of realistic user-uploaded videos containing camera motion and cluttered background.", "source_file": U},
  {"id": "ucf_fps", "quote": "All clips have fixed frame rate and resolution of 25 FPS and 320 × 240 respectively.", "source_file": U},
  {"id": "in_cfg_size", "quote": "data_folder: ../../data/UCF-101 size: 128 mode: train", "source_file": CFG},
  {"id": "in_cfg_seq", "quote": "sequence_length: 17 sample_every_n_frames: 1", "source_file": CFG},
  {"id": "in_loader_fps", "quote": "fps = self.fps if self.fps is not None else -1,", "source_file": LD},
  {"id": "in_loader_rand", "quote": "frame_indices = np.array(range(rand_start, rand_start + num_frm)).astype(int)", "source_file": LD},
  {"id": "emb_cfg", "quote": "n_embed: 262144 embed_dim: 18", "source_file": CFG},
  {"id": "arch_cfg", "quote": "double_z: False z_channels: 18 resolution: 128 in_channels: 3 out_ch: 3 ch: 128 ch_mult: [1,2,2,4] # num_down = len(ch_mult)-1 num_res_blocks: 4", "source_file": CFG}
 ]
}
save_record(rec)
