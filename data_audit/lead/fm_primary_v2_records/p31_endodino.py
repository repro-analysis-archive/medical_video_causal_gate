"""EndoDINO (Virgo Surgical Video Solutions, 2025) - DINOv2 pretraining on GI endoscopy video frames."""
from ._common import A300, C, NOFLOPS, NOT_MENTIONED, Q, elig

REC = {
    "name": "EndoDINO",
    "aliases": ["EndoDINO ViT-B/14, ViT-L/14, ViT-g/14 (Virgo)"],
    "paper": {
        "title": "EndoDINO: A Foundation Model for GI Endoscopy",
        "year": 2025, "venue": "arXiv preprint (Virgo Surgical Video Solutions)", "arxiv": "2501.05488",
        "quotes": [Q("(or arXiv:2501.05488v1 [cs.CV] for this version)", "endodino_arxiv_abs")],
    },
    "version": {
        "value": "no public checkpoint; paper arXiv 2501.05488v1 describes ViT-B/14, ViT-L/14, ViT-g/14 checkpoints selected by downstream evaluation",
        "basis": "Paper reports internal checkpoints; no public release; the model is offered inside Virgo's commercial EndoML platform.",
        "quotes": [Q("We studied three different model sizes (ViT-B, ViT-L, and ViT-g) [17, 18]", "endodino_arxiv_pdf"),
                   Q("Checkpoints were saved every 25,000 iterations for downstream task evaluation.", "endodino_arxiv_pdf")],
    },
    "weights_location": {
        "url": None,
        "exists": "NO public weights - the paper gives no code/weights link; Hugging Face model search 'endodino' returns no model; Virgo exposes EndoDINO through its EndoML platform (commercial product), not as downloadable weights",
        "access": "not released (platform access only)",
        "verification": "paper text searched for 'github', 'hugging', 'release', 'available'; HF API model search listing; Virgo EndoML press item",
        "quotes": [Q("[]", "endodino_hf_search"),
                   Q("The platform leverages Virgo’s AI foundation model, EndoDINO, which has been trained on a vast dataset of over 130,000 full-length gastrointestinal endoscopy videos.", "endodino_endoml_news")],
    },
    "licence": {
        "code": "none published", "weights": "none published (proprietary)", "url": "https://arxiv.org/abs/2501.05488",
        "code_and_weights_differ": "n/a",
        "quotes": [],
        "note": "No licence text found in the paper (searched 'licen') or elsewhere for the model; DINOv2 code licence applies only to Meta's code.",
    },
    "domain": {
        "value": "GI endoscopy video frames (upper and lower GI endoscopy, United States)",
        "quotes": [Q("we present EndoDINO, a foundation model for GI endoscopy tasks that achieves strong generalizability by pre-training on a well-curated image dataset sampled from the largest known GI endoscopy video dataset in the literature.", "endodino_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "Frames from 130,037 de-identified GI endoscopy videos captured on the VirgoCloud platform (US; upper and lower GI); 30->5 fps downsampling, deduplication to 112M index frames, hierarchical k-means balanced sampling to 100K-10M images",
        "datasets": ["VirgoCloud GI endoscopy videos (130,037 videos, ~3.5B frames; proprietary, Virgo Surgical Video Solutions, US)"],
        "quotes": [Q("We assembled our dataset by first retrieving still frames from a pool of 130,037 de-identified endoscopy videos, totaling over 3.5 billion still frames. All videos were captured using the VirgoCloud platform from Virgo Surgical Video Solutions, Inc.", "endodino_arxiv_pdf"),
                   Q("GI endoscopy in the United States. This set is inclusive of videos from a wide range of procedures, indications, and endoscopy equipment.", "endodino_arxiv_pdf"),
                   Q("Duplicate and near-duplicate frames were removed to create an index set of 112 million frames.", "endodino_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "NO", NOT_MENTIONED, False,
        "Proprietary data (VirgoCloud), not itemised per centre, but documented as GI (upper/lower) endoscopy videos from the United States; "
        "laparoscopic appendectomy recordings from the German Appendix300 centres are outside the documented scope. No YouTube data. "
        "Residual caveat: the exact institutions are not listed.",
        [Q("Videos were randomly selected to create a set that is approximately representative of upper and lower", "endodino_arxiv_pdf")]),
    "input": {
        "frame_size": "not stated (DINOv2 ViT-*/14; 'Input image resolution ... equivalent' to the comparator, value not given)",
        "frame_rate_or_sampling": "source video 30 fps downsampled to 5 fps, then deduplicated and cluster-balanced sampling of single frames",
        "clip_length_frames": "1 (image model on still frames)",
        "notes": "frozen-encoder use with linear / boosted-linear heads on patch/class tokens",
        "quotes": [Q("From the initial set of 3.5 billion frames, we initially downsampled from 30 frames per second to 5 frames per second.", "endodino_arxiv_pdf"),
                   Q("Input image resolution, data split ratios (80/10/10), training data augmentations, and relevant hyper-parameter values are equivalent between our models and the best", "endodino_arxiv_pdf")],
    },
    "embedding_dim": {"value": None, "basis": "not stated in the paper (searched 'dimension', '768', '1024', '1536'); standard DINOv2 ViT-B/L/g widths would be 768/1024/1536 (outside fact, unverified for EndoDINO)", "quotes": []},
    "params": {"value": "86M (ViT-B), 307M (ViT-L), 1B (ViT-g)",
               "quotes": [Q("we pre-trained ViT models with 1B, 307M, and 86M parameters using datasets ranging from 100K to 10M curated images.", "endodino_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP' in arXiv PDF"),
    "eligibility": elig(
        C("FAIL", "No public weights: no download link in the paper, no HF model; EndoDINO is offered only via Virgo's EndoML platform."),
        C("UNKNOWN", "No licence text found for the model."),
        C("PASS", "DINOv2 pretraining on frames sampled from GI endoscopy videos."),
        C("PASS", "Paper names the source (130,037 VirgoCloud GI endoscopy videos, US) with counts and curation; institutions not itemised."),
        "Not usable: proprietary weights."),
}
