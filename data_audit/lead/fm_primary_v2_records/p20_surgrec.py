"""SurgRec (SurgRec-MAE / SurgRec-JEPA; arXiv 2603.29966) (new entry, fork A; weights not yet released)."""
from ._common import A300, C, Q, elig

REC = {
    "name": "SurgRec (SurgRec-MAE / SurgRec-JEPA video pretraining recipe)",
    "aliases": ["SurgRec-MAE", "SurgRec-JEPA"],
    "paper": {"title": "Scaling Video Pretraining for Surgical Foundation Models", "year": 2026, "venue": "arXiv 2603.29966v2 (2026-04-02)", "arxiv": "2603.29966",
              "quotes": [Q("Title: Scaling Video Pretraining for Surgical Foundation Models", "surgrec_arxiv_abs"),
                         Q("We propose SurgRec, a scalable and reproducible pretraining recipe for surgical video understanding, instantiated with two variants: SurgRec-MAE and SurgRecJEPA.", "surgrec_arxiv_pdf")]},
    "version": {"value": "no released checkpoint", "basis": "paper abstract promises future release",
                "quotes": [Q("All code, models, and data will be publicly released.", "surgrec_arxiv_pdf")]},
    "weights_location": {"url": None, "exists": "NO - 'will be publicly released'; no repository/HF link in the paper", "access": "n/a",
                         "verification": "arXiv abs + PDF text searched for github/huggingface, 2026-10-02",
                         "quotes": [Q("All code, models, and data will be publicly released.", "surgrec_arxiv_pdf")]},
    "licence": {"code": "not stated", "weights": "not stated", "url": "https://arxiv.org/abs/2603.29966", "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "surgical video (endoscopy, laparoscopy, cataract, robotic); masked video reconstruction (MAE) and latent prediction (JEPA)",
               "quotes": [Q("We curate a large multi-source corpus of 10,535 videos and 214.5M frames spanning endoscopy, laparoscopy, cataract, and robotic surgery.", "surgrec_arxiv_pdf")]},
    "pretraining_data_quote": {
        "summary": "10,535 videos / 214.5M frames: 2,790 videos from 32 public datasets + 7,745 videos 'curated from publicly available platforms' (web-crawled open-access educational videos) + private data.",
        "datasets": ["32 public datasets (e.g. AIxSuture, AutoLaparo, Cholec80/T45, KUMC, Kvasir-Capsule, LDPolypVideo, PitVis, PolypDiag, PolypsSet, CATARACTS-1k, Cataract101/21, GraSP, JIGSAWS, PSI-AVA, SAR-RARP50, AVOS)",
                     "web-crawled open-access educational surgical videos (7,745)", "private data (unnamed)"],
        "quotes": [Q("We source data from three streams: (i) public clinical datasets, (ii) web-crawled surgical videos, and (iii) private data to improve coverage of procedure types.", "surgrec_arxiv_pdf"),
                   Q("This total consists of 2,790 videos (39.9M frames) from 32 public datasets and 7,745 videos (174.6M frames) curated from publicly available platforms.", "surgrec_arxiv_pdf")]},
    "appendix300_check": A300(
        "UNKNOWN", "(ii) web-crawled surgical videos, and (iii) private data", True,
        "The documented list does not mention DS203/Appendix300 or its centres, but 7,745 web-crawled videos (>50 procedure keywords, list not "
        "published) and unnamed private data cannot be excluded.",
        [Q("The open-access educational stream contributes a long-tail taxonomy of more than 50 procedure keywords.", "surgrec_arxiv_pdf")]),
    "input": {"frame_size": "224x224 random crops after resizing the shortest side to 320", "frame_rate_or_sampling": "not stated in the saved text",
              "clip_length_frames": "not stated in the saved text", "notes": "",
              "quotes": [Q("all frames are resized so that the shortest side is 320 pixels, followed by random 224×224 spatial crops.", "surgrec_arxiv_pdf")]},
    "embedding_dim": {"value": None, "basis": "backbone width not stated in the saved text", "quotes": []},
    "params": {"value": "not stated in the saved text", "quotes": []},
    "flops_per_input_if_documented": {"value": None, "statement": "not documented (searched 'FLOP')", "quotes": []},
    "eligibility": elig(
        C("FAIL", "No released weights ('will be publicly released')."),
        C("UNKNOWN", "No licence stated."),
        C("PASS", "MAE / JEPA video pretraining on surgical video."),
        C("PASS", "Public datasets named; web and private streams described generically (partial)."),
        "Re-check later."),
}
