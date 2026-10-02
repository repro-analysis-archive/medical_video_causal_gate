"""Endo-CLIP (MICCAI 2025) - colonoscopy image-report CLIP pretraining."""
from ._common import A300, C, NOFLOPS, NOT_MENTIONED, Q, elig

REC = {
    "name": "Endo-CLIP",
    "aliases": ["EndoCLIP"],
    "paper": {
        "title": "Endo-CLIP: Progressive Self-Supervised Pre-training on Raw Colonoscopy Records",
        "year": 2025, "venue": "MICCAI 2025 (early accept)", "arxiv": "2505.09435",
        "quotes": [Q("Endo-CLIP: Progressive Self-Supervised Pre-training on Raw Colonoscopy Records", "endoclip_arxiv_pdf"),
                   Q("Early accepted to MICCAI 2025", "endoclip_arxiv_abs")],
    },
    "version": {
        "value": "no released checkpoint; paper arXiv 2505.09435v1",
        "basis": "The code/weights repository named in the paper is empty; no Hugging Face model found (search 'endoclip', 'endo-clip' returned []).",
        "quotes": [Q("(or arXiv:2505.09435v1 [cs.CV] for this version)", "endoclip_arxiv_abs"),
                   Q("This repository is empty.", "endoclip_github_page")],
    },
    "weights_location": {
        "url": None,
        "exists": "NO - the announced repository https://github.com/chrlott/EndoCLIP is empty (checked 2026-10-02); Hugging Face model search for 'endoclip' / 'endo-clip' returns no model",
        "access": "not released",
        "verification": "GitHub repository HTML page; HF API model search listing",
        "quotes": [Q("Code will be made publicly available on https://github.com/chrlott/ EndoCLIP.", "endoclip_arxiv_pdf"),
                   Q("This repository is empty.", "endoclip_github_page"),
                   Q("[]", "endoclip_hf_search")],
    },
    "licence": {
        "code": "none (empty repository)", "weights": "none (not released)", "url": "https://github.com/chrlott/EndoCLIP",
        "code_and_weights_differ": "n/a",
        "quotes": [Q("This repository is empty.", "endoclip_github_page")],
    },
    "domain": {
        "value": "colonoscopy still images (screenshots from electronic colonoscopy records) paired with free-text reports; not documented as video frames",
        "quotes": [Q("The vast, daily-accumulating archives of electronic colonoscopy records – comprising numerous screenshots and free-text reports – represent a largely untapped resource for such pre-training.", "endoclip_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "13k colorectal examination cases, 874k endoscopic images with diagnostic reports; the source institution is not named (author affiliations include Zhongshan Hospital, Fudan University); CLIP initialisation",
        "datasets": ["unnamed in-house colonoscopy-record collection (13k cases, 874k images + reports)", "Initialisation: OpenAI CLIP ViT-B/32 + text Transformer"],
        "quotes": [Q("Pre-training Dataset: Our dataset comprises 13k colorectal examination cases with 874k endoscopic images and corresponding diagnostic reports.", "endoclip_arxiv_pdf"),
                   Q("both initialized with pre-trained CLIP weights", "endoclip_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "NO", NOT_MENTIONED, False,
        "The pretraining data are an unnamed in-house collection, but its documented content is colorectal examination (colonoscopy) "
        "screenshots with diagnostic reports, which excludes laparoscopic appendectomy recordings; the CLIP initialisation is web image-text "
        "data (not video). Exact institution not stated, so a Dresden-area origin is not documented either way, but the modality differs.",
        [Q("Our dataset comprises 13k colorectal examination cases with 874k endoscopic images and corresponding diagnostic reports.", "endoclip_arxiv_pdf")]),
    "input": {
        "frame_size": "not stated (ViT-B/32 CLIP image encoder; CLIP default is 224x224 - not confirmed in the paper)",
        "frame_rate_or_sampling": "single still images (record screenshots); no temporal sampling",
        "clip_length_frames": "1 (image model)",
        "notes": "patient-level aggregation of multiple images in stage 3 (averaged embeddings)",
        "quotes": [Q("The vision encoder adopts the ViT-B/32 version of the Vision Transformer [10]", "endoclip_arxiv_pdf"),
                   Q("we aggregate polyp-level features by averaging the updated image and text embeddings", "endoclip_arxiv_pdf")],
    },
    "embedding_dim": {"value": None, "basis": "not stated in the paper (searched 'dimension', '512', '768'); embeddings V, T in R^(N x d) with d unspecified",
                      "quotes": [Q("We gather all vi and ti for a batch of N patients into matrices V, T ∈ RN ×d .", "endoclip_arxiv_pdf")]},
    "params": {"value": "not stated (ViT-B/32 vision encoder + base Transformer text encoder)",
               "quotes": [Q("while the text encoder utilizes a base Transformer architecture, both initialized with pre-trained CLIP weights", "endoclip_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'param' in arXiv PDF"),
    "eligibility": elig(
        C("FAIL", "No released weights: the announced GitHub repository is empty and no HF model exists."),
        C("UNKNOWN", "No licence text (nothing released)."),
        C("UNKNOWN", "Endoscopic (colonoscopy) domain, but training images are record screenshots, not documented as video frames."),
        C("FAIL", "Pretraining data described only generically ('Our dataset ... 13k colorectal examination cases'); source not named."),
        "Not usable: weights unreleased."),
}


# --- lead harmonisation (2026-10-02) ---
assert REC["appendix300_check"]["answer"] == "NO"
REC["appendix300_check"]["answer"] = "UNKNOWN"
REC["appendix300_check"]["cannot_exclude_note"] += " " + 'LEAD HARMONISATION 2026-10-02: answer changed NO -> UNKNOWN under the uniform lineage rule (training data of the released weights plus their initialisation / base / frozen-backbone weights; distillation teachers are recorded but do not decide): the CLIP initialisation (web-scale image-text pairs, not itemised) cannot be excluded.'
REC["appendix300_check"]["quotes"].append(Q('both initialized with pre-trained CLIP weights', 'endoclip_arxiv_pdf'))
REC.setdefault("changes_vs_previous", []).append('Appendix300 NO -> UNKNOWN (lead harmonisation of the lineage rule across all entries): the CLIP initialisation (web-scale image-text pairs, not itemised) cannot be excluded.')
