"""ZEN (Samsung Medical Center; arXiv 2602.13633) (new entry, fork A; weights not yet released)."""
from ._common import A300, C, Q, elig

REC = {
    "name": "ZEN (multi-teacher distilled surgical video-frame foundation model; Samsung Medical Center)",
    "aliases": ["ZEN", "MIS-DINOv2 (ViT-L teacher trained in the same work)"],
    "paper": {"title": "A generalizable foundation model for intraoperative understanding across surgical procedures", "year": 2026,
              "venue": "arXiv 2602.13633", "arxiv": "2602.13633",
              "quotes": [Q("Here we introduce ZEN, a generalizable foundation model for intraoperative surgical video understanding trained on more than 4 million frames from over 21 procedures using a self-supervised multi-teacher distillation framework.", "intraopfm_arxiv_pdf")]},
    "version": {"value": "no released checkpoint", "basis": "Code availability statement",
                "quotes": [Q("The code and pretrained weights for ZEN will be made publicly available upon acceptance of this manuscript on GitHub.", "intraopfm_arxiv_pdf")]},
    "weights_location": {"url": None, "exists": "NO - weights 'will be made publicly available upon acceptance' (not yet)", "access": "n/a",
                         "verification": "arXiv PDF code-availability statement, 2026-10-02",
                         "quotes": [Q("The code and pretrained weights for ZEN will be made publicly available upon acceptance of this manuscript on GitHub.", "intraopfm_arxiv_pdf")]},
    "licence": {"code": "not stated", "weights": "not stated", "url": "https://arxiv.org/abs/2602.13633", "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "minimally invasive surgery video frames (1 fps); image encoder (ViT-B student distilled from MIS-DINOv2 ViT-L and PeskaVLP teachers)",
               "quotes": [Q("Video frames were uniformly sampled at 1 frame per second using FFmpeg.", "intraopfm_arxiv_pdf"),
                          Q("ZEN is trained via feature-level distillation from multiple frozen expert teachers, including MIS-DINOv2 (ViTLarge) and PeskaVLP.", "intraopfm_arxiv_pdf")]},
    "pretraining_data_quote": {
        "summary": "4,316,410 frames from 4,780+ videos: 100 in-house hepatectomies (Samsung Medical Center, IRB SMC2024-08-027) + 14 public datasets (hSDB-instrument, HeiChole, Cholec80, Endoscapes, HeiCo, ART-Net, LapGyn4, SurgicalActions160, GLENDA, ESAD, MultiBypass140, SISVSE, SurgToolLoc2022, Surgical YouTube (3,253 videos, incl. appendectomy)).",
        "datasets": ["SMC in-house hepatectomy (100)", "hSDB-instrument", "HeiChole", "Cholec80", "Endoscapes", "HeiCo", "ART-Net", "LapGyn4", "SurgicalActions160", "GLENDA", "ESAD",
                     "MultiBypass140", "SISVSE", "SurgToolLoc2022", "Surgical YouTube (3,253 videos)"],
        "quotes": [Q("The dataset consists of 100 in-house hepatectomy cases and 14 publicly available open-access surgical video datasets", "intraopfm_arxiv_pdf"),
                   Q("Upstream datasets SMC Hepatobiliary hSBD-instrument HeiChole Cholec80 Endoscapes HeiCo Colon & Rectum ART-Net LapGyn4 SurgicalAction160 GLENDA ESAD MultiByPass140 Sisvse SurgToolLoc2022 Surgical YouTube", "intraopfm_arxiv_pdf")]},
    "appendix300_check": A300(
        "UNKNOWN", "Surgical YouTube", True,
        "Pretraining includes the 'Surgical YouTube' set (3,253 videos; the SurgeNet/GenSurgery YouTube collection) whose procedure list includes "
        "appendectomy, with undocumented recording centres; plus 100 in-house SMC (Seoul) hepatectomies. The documented list does not mention "
        "DS203/Appendix300; YouTube content cannot be excluded.",
        [Q("Esophageal Appendix Stomach", "intraopfm_arxiv_pdf")]),
    "input": {"frame_size": "224x224", "frame_rate_or_sampling": "1 fps frame sampling", "clip_length_frames": "1 (frame-level encoder)", "notes": "ViT-B student, ImageNet-initialised SSL baselines",
              "quotes": [Q("(13 transformer blocks, 768-dimensional embeddings) with 12 a 224 × 224 input resolution", "intraopfm_arxiv_pdf"),
                         Q("Video frames were uniformly sampled at 1 frame per second using FFmpeg.", "intraopfm_arxiv_pdf")]},
    "embedding_dim": {"value": 768, "basis": "ViT-Base backbone used for ZEN (student)", "quotes": [Q("ZEN uses a lighter ViT-Base architecture than MIS-DINOv2 (ViT-Large)", "intraopfm_arxiv_pdf")]},
    "params": {"value": "not stated (ViT-B)", "quotes": []},
    "flops_per_input_if_documented": {"value": None, "statement": "not documented (searched 'FLOP')", "quotes": []},
    "eligibility": elig(
        C("FAIL", "Weights not released ('will be made publicly available upon acceptance')."),
        C("UNKNOWN", "No licence stated."),
        C("PASS", "Self-supervised distillation pretraining on 1-fps frames of minimally invasive surgery videos."),
        C("PASS", "Supplementary Table 45 names all upstream datasets and the in-house source (SMC hepatectomy)."),
        "Re-check after publication."),
}
