import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_record, term_search, MED_TERMS, A300_TERMS

RM = "videogpt_github_README.md"; LIC = "videogpt_github_LICENSE.txt"; DL = "videogpt_github_download.py.txt"
VQ = "videogpt_github_vqvae.py.txt"; DATA = "videogpt_github_data.py.txt"; P = "videogpt_arxiv_2104.10157.txt"
V = {k: f"videogpt_gdrive_{k}_view.txt" for k in ["bair_stride4x2x2", "ucf101_stride4x4x4", "kinetics_stride4x4x4", "kinetics_stride2x4x4"]}
H = {k: f"videogpt_gdrive_{k}_uc_head.json" for k in V}
DATA_FILES = [P, RM, DL]
NOTFOUND = "リクエストされたファイルは存在しません。"

rec = {
 "id": "18_videogpt_vqvae",
 "name": "VideoGPT VQ-VAE (wilson1yan/VideoGPT; checkpoints bair_stride4x2x2, ucf101_stride4x4x4, kinetics_stride4x4x4, kinetics_stride2x4x4)",
 "status_in_survey": "added in revision 2 (2026-10-02)",
 "version": "VQ-VAE checkpoints listed in videogpt/download.py on GitHub master (bair_stride4x2x2, ucf101_stride4x4x4, kinetics_stride4x4x4, kinetics_stride2x4x4); paper arXiv:2104.10157v2 (2021-09-14)",
 "paper": {"title": "VideoGPT: Video Generation using VQ-VAE and Transformers", "year": 2021, "arxiv": "2104.10157"},
 "weights_location": {
  "urls": [f"https://drive.google.com/file/d/{i}/view" for i in ["1iIAYJ2Qqrx5Q94s5eIXQYJgAydzvT_8L", "1uuB_8WzHP_bbBmfuaIV7PK_Itl3DyHY5", "1DOvOZnFAIQmux6hG7pN_HkyJZy3lXbCB", "1jvtjjtrtE4cy6pl7DK_zWFEPY3RZt2pB"]],
  "files_listed": {},
  "gated": None, "private": None,
  "verified_how": "Official links = Google Drive file ids hard-coded in videogpt/download.py (downloaded via gdown). The public Drive view page of each id was saved (HTTP 404, 'the requested file does not exist') and a HEAD request to the drive.google.com/uc download endpoint returned 404 for all four ids (2026-10-02). No HF repo by the authors was found. Nothing downloaded.",
  "status": "NOT AVAILABLE: all four official checkpoint links return HTTP 404 on 2026-10-02",
  "quote_ids": ["w_bair", "w_ucf", "w_kin444", "w_kin244", "w_gdown", "w_404_bair", "w_404_ucf", "w_404_kin444", "w_404_kin244", "w_head_bair", "w_head_ucf", "w_head_kin444", "w_head_kin244"]
 },
 "licence": {
  "id": "MIT (GitHub repository LICENSE; no separate weights licence stated)",
  "url": "https://github.com/wilson1yan/VideoGPT/blob/master/LICENSE",
  "commercial": "permitted", "non_commercial_only": False, "restrictions": "none beyond MIT",
  "gating": "n/a (weights not reachable)", "quote_ids": ["lic_mit", "lic_copy"]
 },
 "domain": {
  "value": "VQ-VAE video tokenizer (3D conv + axial attention) of the likelihood-based video generative model VideoGPT; trained on general research video datasets (BAIR robot pushing, UCF-101, Kinetics)",
  "quote_ids": ["dom_readme", "w_ucf", "w_kin444"]
 },
 "architecture": {
  "type": "VQ-VAE: 3D convolutional encoder/decoder with axial self-attention residual blocks, single codebook",
  "representation": "discrete latent code grid (T/st x H/sh x W/sw), each code an embedding vector (default embedding_dim 256, default n_codes 2048 in code; paper BAIR: 256-dim, 1024 codes)"
 },
 "pretraining_data": {
  "summary": "Per checkpoint (download.py comments + checkpoint names): BAIR robot pushing, 16 frames of 64x64; UCF-101, 16 frames of 128x128; Kinetics (version not stated anywhere in the saved sources), 16 frames of 128x128. The paper names BAIR, UCF-101, TGIF, Moving MNIST, ViZDoom/RoboNet for its experiments; Kinetics is not mentioned in the paper.",
  "form": "dataset list (named, per checkpoint; Kinetics version unspecified)"
 },
 "pretraining_data_quote": {"quote_ids": ["w_bair", "w_ucf", "w_kin444", "w_kin244", "data_ucf", "data_bair"]},
 "medical_video_in_data": {
  "answer": "NO",
  "basis": "the checkpoint data are a closed list of named research datasets (BAIR robot pushing, UCF-101, Kinetics human-action classes), none medical; term search of paper/README/download.py: hits only for the ViZDoom 'Health Gathering' game environment (not medical data)",
  "term_search": {"pattern": MED_TERMS, "hits": term_search(DATA_FILES, MED_TERMS)}
 },
 "appendix300_possible": {
  "answer": "NO", "basis_class": "closed_curated_list",
  "basis": "BAIR robot pushing, UCF-101 and Kinetics are closed curated research datasets with fixed robot-pushing / human-action content scope (conventions_v2 clarification: Kinetics/UCF-101 -> NO). Caveat: the Kinetics version of the kinetics_* checkpoints is not stated. Timing: 2021, before the OPARA issue 2026-04-29.",
  "quote_ids": ["w_bair", "w_ucf", "w_kin444"]
 },
 "appendix300_check": {
  "answer": "NO",
  "quote_or_statement": "the documented data list does not mention DS203/Appendix300",
  "basis_class": "closed_curated_list",
  "basis": "closed list of named curated datasets (BAIR, UCF-101, Kinetics) whose content scope excludes surgical recordings; Kinetics version unspecified",
  "term_search": {"pattern": A300_TERMS, "hits": term_search(DATA_FILES, A300_TERMS)},
  "quote_ids": ["w_bair", "w_ucf", "w_kin444"]
 },
 "input": {
  "frame_size": {"value": "64x64 (bair_stride4x2x2); 128x128 (ucf101 / kinetics checkpoints); preprocessing scales the shorter side to the resolution and center-crops", "quote_ids": ["w_bair", "w_ucf", "data_ucf"]},
  "frame_rate_or_sampling": {"value": "consecutive frames at the source frame rate (torchvision VideoClips with no frame_rate argument; preprocess takes the first sequence_length frames of a clip); no fps stated", "quote_ids": ["in_crop", "in_clips"]},
  "clip_length_frames": {"value": "16", "quote_ids": ["w_ucf", "in_seq"]},
  "temporal_compression": {"value": "4x (bair_stride4x2x2, ucf101_stride4x4x4, kinetics_stride4x4x4) or 2x (kinetics_stride2x4x4), per checkpoint name = T H W stride; note the paper states 2x for its BAIR model while the released BAIR checkpoint is named stride4x2x2", "quote_ids": ["in_down", "w_bair", "data_bair"]},
  "spatial_compression": {"value": "4x4 (ucf101 / kinetics checkpoints); 2x2 (bair_stride4x2x2)", "quote_ids": ["in_down", "w_ucf"]}
 },
 "embedding_dim": {
  "value": "kinetics_stride4x4x4 / ucf101_stride4x4x4 at 16x128x128: 4 x 32 x 32 = 4,096 discrete codes, each mapped to a codebook vector (default 256-dim) -> 4,096 x 256; kinetics_stride2x4x4: 8 x 32 x 32 codes; bair_stride4x2x2 at 16x64x64: 4 x 32 x 32 codes",
  "derivation": "grid = (16/st) x (H/sh) x (W/sw) from the checkpoint stride names; code vector dim = argparse default --embedding_dim 256 (the released checkpoints' hyper-parameters are not documented outside the checkpoint files, which were not opened)",
  "quote_ids": ["in_embdim", "in_ncodes", "w_kin444", "data_bair"]
 },
 "params": {"value": "not documented (no parameter count for the VQ-VAEs in the saved paper, README or code)", "scope": "n/a", "quote_ids": []},
 "flops_per_input_if_documented": None,
 "flops_note": "no FLOPs/MACs statement in the saved paper, README or code (searched FLOP)",
 "eligibility": {
  "C1_open_weights": {"status": "FAIL", "basis": "the only official weight links (Google Drive ids in download.py) return HTTP 404 (view page and download endpoint) on 2026-10-02; no other official host found -> weights not publicly downloadable now", "quote_ids": ["w_gdown", "w_404_ucf", "w_head_ucf"]},
  "C2_licence_research_use": {"status": "PASS", "basis": "MIT licence on the repository", "quote_ids": ["lic_mit"]},
  "C3_domain_secondary": {"status": "PASS", "basis": "video VQ-VAE tokenizer of a video generative model trained on general (non-surgical) video", "quote_ids": ["dom_readme"]},
  "C4_documented_pretraining_data": {"status": "PASS", "basis": "per-checkpoint datasets are named (BAIR, UCF-101, Kinetics) in the official download code and the paper; caveat: the Kinetics version is unspecified", "quote_ids": ["w_bair", "w_ucf", "w_kin444", "data_ucf"]},
  "eligible": "NO (fails C1: official checkpoint links are dead)"
 },
 "quotes": [
  {"id": "w_bair", "quote": "'bair_stride4x2x2': '1iIAYJ2Qqrx5Q94s5eIXQYJgAydzvT_8L', # trained on 16 frames of 64 x 64 images", "source_file": DL},
  {"id": "w_ucf", "quote": "'ucf101_stride4x4x4': '1uuB_8WzHP_bbBmfuaIV7PK_Itl3DyHY5', # trained on 16 frames of 128 x 128 images", "source_file": DL},
  {"id": "w_kin444", "quote": "'kinetics_stride4x4x4': '1DOvOZnFAIQmux6hG7pN_HkyJZy3lXbCB', # trained on 16 frames of 128 x 128 images", "source_file": DL},
  {"id": "w_kin244", "quote": "'kinetics_stride2x4x4': '1jvtjjtrtE4cy6pl7DK_zWFEPY3RZt2pB' # trained on 16 frames of 128 x 128 images", "source_file": DL},
  {"id": "w_gdown", "quote": "gdown.download(id=id, output=destination, quiet=False)", "source_file": DL},
  {"id": "w_404_bair", "quote": NOTFOUND, "source_file": V["bair_stride4x2x2"]},
  {"id": "w_404_ucf", "quote": NOTFOUND, "source_file": V["ucf101_stride4x4x4"]},
  {"id": "w_404_kin444", "quote": NOTFOUND, "source_file": V["kinetics_stride4x4x4"]},
  {"id": "w_404_kin244", "quote": NOTFOUND, "source_file": V["kinetics_stride2x4x4"]},
  {"id": "w_head_bair", "quote": "\"http_status\": 404,", "source_file": H["bair_stride4x2x2"]},
  {"id": "w_head_ucf", "quote": "\"http_status\": 404,", "source_file": H["ucf101_stride4x4x4"]},
  {"id": "w_head_kin444", "quote": "\"http_status\": 404,", "source_file": H["kinetics_stride4x4x4"]},
  {"id": "w_head_kin244", "quote": "\"http_status\": 404,", "source_file": H["kinetics_stride2x4x4"]},
  {"id": "lic_mit", "quote": "MIT License", "source_file": LIC},
  {"id": "lic_copy", "quote": "Copyright (c) 2021 Wilson Yan", "source_file": LIC},
  {"id": "dom_readme", "quote": "VideoGPT uses VQ-VAE that learns downsampled discrete latent representations of a raw video by employing 3D convolutions and axial self-attention.", "source_file": RM},
  {"id": "data_ucf", "quote": "UCF-101 (Soomro et al., 2012) is an action classification dataset with 13,320 videos from 101 different classes. We train unconditional VideoGPT models on 16 frame 64 × 64 and 128 × 128 videos, where the original videos have their shorter side scaled to 128 pixels, and then center cropped.", "source_file": P},
  {"id": "data_bair", "quote": "For BAIR, VQ-VAE downsamples the inputs by a factor of 2x over each of height, width and time dimensions. The embedding in the latent space is a 256-dimensional vector, which is discretized through a codebook with 1024 codes.", "source_file": P},
  {"id": "in_crop", "quote": "# temporal crop if sequence_length is not None: assert sequence_length <= t video = video[:sequence_length]", "source_file": DATA},
  {"id": "in_clips", "quote": "clips = VideoClips(files, sequence_length, num_workers=32)", "source_file": DATA},
  {"id": "in_seq", "quote": "* `--sequence_length 16`: temporal resolution, or video clip length", "source_file": RM},
  {"id": "in_down", "quote": "* `--downsample 4 4 4`: T H W downsampling stride of the encoder", "source_file": RM},
  {"id": "in_embdim", "quote": "parser.add_argument('--embedding_dim', type=int, default=256)", "source_file": VQ},
  {"id": "in_ncodes", "quote": "parser.add_argument('--n_codes', type=int, default=2048)", "source_file": VQ}
 ]
}
save_record(rec)
