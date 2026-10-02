"""OphCLIP (ICCV 2025) - ophthalmic surgical video-language pretraining on OphVL (YouTube)."""
from ._common import A300, C, NOFLOPS, NOT_MENTIONED, Q, elig

REC = {
    "name": "OphCLIP",
    "aliases": [],
    "paper": {
        "title": "OphCLIP: Hierarchical Retrieval-Augmented Learning for Ophthalmic Surgical Video-Language Pretraining",
        "year": 2025, "venue": "ICCV 2025 (pp. 19838-19849)", "arxiv": "2411.15421",
        "quotes": [Q("[OphCLIP](https://arxiv.org/abs/2411.15421) is accepted by ICCV 2025.", "ophclip_github_readme")],
    },
    "version": {
        "value": "no released checkpoint (repo README TODO 'Release code and checkpoints'); paper arXiv 2411.15421v2",
        "basis": "GitHub README",
        "quotes": [Q("- [ ] Release code and checkpoints", "ophclip_github_readme"),
                   Q("(or arXiv:2411.15421v2 [cs.CV] for this version)", "ophclip_arxiv_abs")],
    },
    "weights_location": {
        "url": None,
        "exists": "NO - the project repository github.com/minghu0830/OphCLIP lists checkpoint release as an open TODO ('Expected in mid-November'); no HF model found (search 'ophclip' returned none)",
        "access": "not released",
        "verification": "README (raw) + repository HTML page, 2026-10-02",
        "quotes": [Q("- [ ] Release code and checkpoints", "ophclip_github_readme"), Q("*Expected in mid-November*", "ophclip_github_readme")],
    },
    "licence": {"code": "none (no code released; no licence on repo page)", "weights": "n/a", "url": "https://github.com/minghu0830/OphCLIP",
                "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {
        "value": "ophthalmic (microscope) surgical video with narration (YouTube)",
        "quotes": [Q("featuring 375K carefully processed video-text pairs from 7.5K hours of narrative open-source surgical videos.", "ophclip_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "OphVL: 375K video-text pairs from 7.5K h of narrated open-source (YouTube) ophthalmic surgery videos, plus silent videos for retrieval; candidate videos (~100K) filtered by a ResNet50 ophthalmic-microscope keyframe classifier; ResNet-50 ImageNet init + BioClinicalBERT",
        "datasets": ["OphVL (YouTube ophthalmic surgery videos)", "Init: ImageNet ResNet-50, BioClinicalBERT"],
        "quotes": [Q("During the download process, we prioritize the highest-resolution versions, filtering out videos shorter than 30 seconds or with resolution below 224p, resulting in a collection of approximately 100K videos.", "ophclip_arxiv_pdf"),
                   Q("Videos with over 80% of keyframes classified as ophthalmic microscope images are labeled as valid videos.", "ophclip_arxiv_pdf"),
                   Q("We use the ResNet-50 as the visual encoder from the ImageNet initialization.", "ophclip_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "NO", NOT_MENTIONED, False,
        "Data are web-scraped YouTube videos (individual uploaders/institutions not listed), but the documented scope is restricted by a "
        "classifier to ophthalmic microscope surgery, which excludes laparoscopic appendectomy recordings; residual risk only from "
        "classifier errors.",
        [Q("We then train and apply a ResNet50 image classifier to determine if the keyframes are microscope images of ophthalmic surgeries.", "ophclip_arxiv_pdf")]),
    "input": {
        "frame_size": "224",
        "frame_rate_or_sampling": "8 frames per clip (clip- and video-level pretraining); sampling rate not stated",
        "clip_length_frames": "8",
        "notes": "Table 6 hyper-parameters: image size 224, # of frames 8 for both stages; visual features average-pooled",
        "quotes": [Q("Batch Size Image Size # of Frames Text Length Batch Size Image Size # of Frames # of Retrieved Videos Text Length Learning Rate Scheduler Optimizer Momentum Temperature Weight of Lvv clip Weight of Lvl clip Value 60 120 224 8 77 140 224 8 1 77", "ophclip_arxiv_pdf"),
                   Q("Then we apply the average pooling at the visual features to generate the visual embeddings.", "ophclip_arxiv_pdf")],
    },
    "embedding_dim": {"value": 768, "basis": "shared embedding space",
                      "quotes": [Q("We use 768 as the dimensionality of the embedding space.", "ophclip_arxiv_pdf")]},
    "params": {"value": "not stated (ResNet-50 + BioClinicalBERT)", "quotes": [Q("We apply BioClinicalBert [20] as the textual encoder", "ophclip_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'param' in arXiv PDF"),
    "eligibility": elig(
        C("FAIL", "Checkpoints not released (README TODO)."),
        C("UNKNOWN", "No licence (nothing released)."),
        C("PASS", "Video-language pretraining on ophthalmic surgical video clips."),
        C("PASS", "Pretraining corpus named and described (OphVL from YouTube; collection and filtering pipeline documented)."),
        "Ophthalmic microscope surgery; not laparoscopic."),
}


# --- lead harmonisation (2026-10-02) ---
assert REC["appendix300_check"]["answer"] == "NO"
REC["appendix300_check"]["answer"] = "UNKNOWN"
REC["appendix300_check"]["cannot_exclude_note"] += " " + 'LEAD HARMONISATION 2026-10-02: answer changed NO -> UNKNOWN under the uniform lineage rule (training data of the released weights plus their initialisation / base / frozen-backbone weights; distillation teachers are recorded but do not decide): the data are open-ended web-scraped YouTube videos (uploaders/institutions not listed); the ophthalmic-only scope makes inclusion implausible but the documentation does not allow exclusion.'
REC["appendix300_check"]["quotes"].append(Q('3.1. Collecting Clip and Text Pairs from YouTube', 'ophclip_arxiv_pdf'))
REC.setdefault("changes_vs_previous", []).append('Appendix300 NO -> UNKNOWN (lead harmonisation of the lineage rule across all entries): the data are open-ended web-scraped YouTube videos (uploaders/institutions not listed); the ophthalmic-only scope makes inclusion implausible but the documentation does not allow exclusion.')
