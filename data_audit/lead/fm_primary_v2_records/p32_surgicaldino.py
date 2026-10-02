"""Surgical-DINO (IPCAI 2024 / IJCARS 2024) - LoRA adaptation of DINOv2 for endoscopic depth estimation."""
from ._common import A300, C, NOFLOPS, NOT_MENTIONED, Q, elig

REC = {
    "name": "Surgical-DINO",
    "aliases": ["SurgicalDINO"],
    "paper": {
        "title": "Surgical-DINO: adapter learning of foundation models for depth estimation in endoscopic surgery",
        "year": 2024, "venue": "IPCAI 2024 / IJCARS 19:1013-1020 (doi 10.1007/s11548-024-03083-5; PMC11178563)", "arxiv": "2401.06013",
        "quotes": [Q("Surgical-DINO: adapter learning of foundation models for depth estimation in endoscopic surgery", "surgicaldino_pmc"),
                   Q("# [IPCAI'2024] Surgical-DINO: Adapter Learning of Foundation Models for Depth Estimation in Endoscopic Surgery", "surgicaldino_github_readme")],
    },
    "version": {
        "value": "no trained checkpoint released; GitHub BeileiCui/SurgicalDINO provides model code surgicaldino.py only (no releases)",
        "basis": "README states only the model definition and losses are provided.",
        "quotes": [Q("we only provide the __Surgical-DINO model__ and __corresponding losses__ in ```./surgicaldino.py```", "surgicaldino_github_readme")],
    },
    "weights_location": {
        "url": None,
        "exists": "NO - no trained Surgical-DINO weights are published (README provides code and losses only; repository page lists no releases); HF search 'surgical-dino' / 'surgicaldino' returned no model",
        "access": "not released",
        "verification": "README (raw) and repository HTML page, 2026-10-02",
        "quotes": [Q("We are focusing on self-supervised learning now so we only provide the __Surgical-DINO model__ and __corresponding losses__", "surgicaldino_github_readme")],
    },
    "licence": {
        "code": "none declared (no LICENSE file: raw LICENSE returns 404; README has no licence statement)",
        "weights": "n/a (not released)", "url": "https://github.com/BeileiCui/SurgicalDINO",
        "code_and_weights_differ": "n/a",
        "quotes": [Q("404: Not Found", "surgicaldino_github_license")],
        "note": "The paper itself is CC BY 4.0 (article licence, not a software/model licence).",
    },
    "domain": {
        "value": "task-specific LoRA + depth-decoder fine-tune of natural-image DINOv2 ViT-B on surgical stereo-endoscopy frames (SCARED); not surgical pretraining",
        "quotes": [Q("During training, we freeze the DINO image encoder, which shows excellent visual representation capacity, and only optimize the LoRA layers and depth decoder to integrate features from the surgical scene.", "surgicaldino_pmc"),
                   Q("Our model is extensively validated on a MICCAI challenge dataset of SCARED, which is collected from da Vinci Xi endoscope surgery.", "surgicaldino_pmc")],
    },
    "pretraining_data_quote": {
        "summary": "Backbone: Meta DINOv2 ViT-B (LVD-142M natural images, frozen). Adaptation data: SCARED (15,351 training frames); Hamlyn used for validation",
        "datasets": ["SCARED (EndoVis 2019 sub-challenge; da Vinci Xi)", "Hamlyn (evaluation, 21 videos)", "Initialisation/frozen backbone: DINOv2 ViT-B"],
        "quotes": [Q("We followed the split scheme in [ 16 ] where the SCARED dataset is split into 15,351, 1705 and 551 frames for the training, validation and test sets, respectively.", "surgicaldino_pmc"),
                   Q("We utilized the pre-trained ViT-Base model from DINOv2 as our image encoder", "surgicaldino_pmc")],
    },
    "appendix300_check": A300(
        "NO", NOT_MENTIONED, False,
        "Adaptation data are SCARED (da Vinci Xi) and Hamlyn (evaluation), both named public datasets unrelated to appendectomy or the "
        "Appendix300 centres. The frozen DINOv2 backbone was trained by Meta on LVD-142M (curated retrieval from web-crawled still images): a "
        "web-scale generic image corpus that cannot be itemised, recorded here as not strictly excludable but outside the surgical-video scope.",
        [Q("SCARED, which is collected from da Vinci Xi endoscope surgery", "surgicaldino_pmc")]),
    "input": {
        "frame_size": "224x224",
        "frame_rate_or_sampling": "single frames (monocular depth); no temporal sampling",
        "clip_length_frames": "1",
        "notes": "frame-level dense prediction; intermediate token maps upsampled x4 and concatenated for the decoder",
        "quotes": [Q("224 × 224 pixels to fit the patch size of DINOv2", "surgicaldino_pmc")],
    },
    "embedding_dim": {"value": "784 as printed (DINOv2 ViT-Base width is 768; the printed value appears to be a typo)",
                      "basis": "paper wording",
                      "quotes": [Q("We utilized the pre-trained ViT-Base model from DINOv2 as our image encoder with 12 Transformer blocks and a feature dimension of 784.", "surgicaldino_pmc")]},
    "params": {"value": "not stated (DINOv2 ViT-B backbone + LoRA layers + depth decoder)", "quotes": []},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'param' in PMC full text"),
    "eligibility": elig(
        C("FAIL", "No trained weights released (code-only repository)."),
        C("UNKNOWN", "No licence declared for code; no weights."),
        C("FAIL", "Not surgical pretraining: frozen natural-image DINOv2 with a task-specific LoRA/depth-decoder fine-tune on SCARED."),
        C("PASS", "Training/evaluation datasets named (SCARED, Hamlyn) and the backbone (DINOv2 ViT-B)."),
        "Included because the task named 'Surgical-DINO-style surgical DINO pretraining'; it is an adapter, not a pretrained FM."),
}


# --- lead harmonisation (2026-10-02) ---
assert REC["appendix300_check"]["answer"] == "NO"
REC["appendix300_check"]["answer"] = "UNKNOWN"
REC["appendix300_check"]["cannot_exclude_note"] += " " + "LEAD HARMONISATION 2026-10-02: answer changed NO -> UNKNOWN under the uniform lineage rule (training data of the released weights plus their initialisation / base / frozen-backbone weights; distillation teachers are recorded but do not decide): the frozen DINOv2 backbone's LVD-142M web-retrieved image corpus cannot be itemised."
REC["appendix300_check"]["quotes"].append(Q('Another trainable decode head is used on top of the frozen model to estimate the final depth', 'surgicaldino_pmc'))
REC.setdefault("changes_vs_previous", []).append("Appendix300 NO -> UNKNOWN (lead harmonisation of the lineage rule across all entries): the frozen DINOv2 backbone's LVD-142M web-retrieved image corpus cannot be itemised.")
