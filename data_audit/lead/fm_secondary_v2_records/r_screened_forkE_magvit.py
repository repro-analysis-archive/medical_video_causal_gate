import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_screened, copy_path

V1R = "magvit_v1_github_README.md"; ISS = "magvit_v1_github_issue16_api.json"; REL = "magvit_v1_github_releases_api.json"
V2P = "magvit_v2_project_page.txt"; V2A = "magvit_v2_arxiv_abs.txt"; OM2 = "openmagvit2_video_hf_README.md"
SRCH = "hf_api_model_search_magvit.json"

items = [
 {
  "name": "MAGVIT (v1): Masked Generative Video Transformer (Yu et al., CVPR 2023; google-research/magvit)",
  "screened_utc_date": "2026-10-02",
  "reason_not_added": "C1: no official weights. The official repository (google-research/magvit) lists 3D-VQ tokenizer models by dataset (BAIR, UCF-101, Kinetics-600, SSv2) but gives no download links; its README points to issue #16, in which the MAGVIT team (posted by roadjiang, repository contributor) states that the weight release was not approved by the company. The GitHub releases API for the repository returns an empty list. Code only (JAX) -> would require training from scratch, which is outside this survey.",
  "would_otherwise_be": "video tokenizer (3D-VQ) trained on closed curated datasets (UCF-101 / K600 / SSv2 / BAIR) -- would have been a C4 PASS / Appendix300 NO candidate had weights existed",
  "evidence_files": [copy_path(V1R), copy_path(ISS), copy_path(REL)],
  "statement": "GitHub releases API (saved copy magvit_v1_github_releases_api.json) returned [] (no releases).",
  "quotes": [
   {"id": "magvit1_note", "quote": "As for the model pretrained weight release, please see this [note](https://github.com/google-research/magvit/issues/16).", "source_file": V1R},
   {"id": "magvit1_table", "quote": "3D-VQ|B|16 frames x 128x128|4x16x16|1024| Kinetics-600", "source_file": V1R},
   {"id": "magvit1_issue_title", "quote": "\"title\": \"Update: Model Weight Release Not Approved\",", "source_file": ISS},
   {"id": "magvit1_issue_body", "quote": "Regrettably, we must inform you that the release of our model weights was not approved by our company.", "source_file": ISS},
   {"id": "magvit1_issue_code", "quote": "This will enable everyone to train the model using the provided code.", "source_file": ISS}
  ]
 },
 {
  "name": "MAGVIT-v2 (Yu et al., 'Language Model Beats Diffusion: Tokenizer is Key to Visual Generation', ICLR 2024, arXiv 2310.05737)",
  "screened_utc_date": "2026-10-02",
  "reason_not_added": "C1: no official weights (and no official code). The official project page magvit.cs.cmu.edu/v2 links only the paper; the google-research/magvit repository covers MAGVIT v1 only and its weights were not approved for release (see the MAGVIT v1 item). HF model search for 'magvit' (saved) lists only third-party repos: unofficial re-implementations (TencentARC Open-MAGVIT2 -> separate entry 17_open_magvit2; showlab/magvitv2, nielsr/magvit-v2, snu-aidas/magvitv2 = Show-o image tokenizer pushes; maverickrzw/magvit* = undocumented personal checkpoints, no model card). Third-party authors (Open-MAGVIT2) state that the original tokenizer is not accessible.",
  "evidence_files": [copy_path(V2P), copy_path(V2A), copy_path(OM2), copy_path(SRCH)],
  "statement": "The saved project-page rendering contains no code or weight link (only 'Research Paper' and VideoPoet links); no official Google/CMU repository for MAGVIT-v2 exists in the HF search listing.",
  "quotes": [
   {"id": "magvit2_def", "quote": "In this paper, we introduce MAGVIT-v2, a video tokenizer designed to generate concise and expressive tokens for both videos and images using a common token vocabulary.", "source_file": V2P},
   {"id": "magvit2_videopoet", "quote": "MAGVIT-v2 tokenizer is the core technique that enables VideoPoet: A large language model for zero-shot video generation .", "source_file": V2P},
   {"id": "magvit2_noaccess", "quote": "However, we have no access to this strong tokenizer so far.", "source_file": OM2},
   {"id": "magvit2_search_om2", "quote": "\"id\": \"TencentARC/Open-MAGVIT2-Tokenizer-262144-Video\",", "source_file": SRCH}
  ]
 }
]
save_screened(items, "forkE")
