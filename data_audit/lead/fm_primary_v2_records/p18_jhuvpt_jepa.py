"""JHU-VPT(JEPA) cataract-surgery video FM (MIDL 2025) (new entry, fork A; weights not found)."""
from ._common import A300, C, Q, elig

REC = {
    "name": "JHU-VPT(JEPA) (cataract-surgery video foundation model, JEPA)",
    "aliases": ["JHU-VPT"],
    "paper": {"title": "A Vision Foundation Model for Cataract Surgery Using Joint-Embedding Predictive Architecture", "year": 2025,
              "venue": "MIDL 2025 (OpenReview QbBPeAIdrk; full text not retrievable: OpenReview returned HTTP 403 to the audit client)", "arxiv": None,
              "quotes": [Q("A Vision Foundation Model for Cataract Surgery Using Joint-Embedding Predictive Architecture", "jhuvpt_mlanthology")]},
    "version": {"value": "no public checkpoint name found", "basis": "MIDL anthology page (abstract + links: PDF/OpenReview/Semantic Scholar only) and web search", "quotes": []},
    "weights_location": {"url": None,
                         "exists": "NOT FOUND - the anthology page links only to OpenReview/Semantic Scholar; no code or weights link in the abstract or in web search; full paper inaccessible (OpenReview 403)",
                         "access": "unknown", "verification": "mlanthology.org page fetched; OpenReview PDF fetch returned 403, 2026-10-02",
                         "quotes": [Q("PDF MIDL OpenReview Semantic Scholar", "jhuvpt_mlanthology")]},
    "licence": {"code": "not found", "weights": "not found", "url": "https://mlanthology.org/midl/2025/shah2025midl-vision/", "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "cataract (ophthalmic microscope) surgery video; JEPA latent feature prediction",
               "quotes": [Q("a self-supervised vision foundation model leveraging Joint-Embedding Predictive Architecture (JEPA) to learn spatiotemporal representations via latent feature prediction on a large corpus of unlabeled cataract videos", "jhuvpt_mlanthology")]},
    "pretraining_data_quote": {"summary": "2,591 cataract-surgery videos from multiple (unnamed in the abstract) sites", "datasets": ["2,591 unlabeled cataract videos, multiple sites"],
                               "quotes": [Q("JHU-VPT(JEPA) is pretrained on 2591 videos from multiple sites that capture different surgical technique and style variations.", "jhuvpt_mlanthology")]},
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "Only the abstract is accessible: 2,591 cataract videos from unnamed sites. Content is ophthalmic (cataract), not laparoscopic appendectomy, "
        "which makes Appendix300 recordings implausible, but sites are not named in accessible text.",
        [Q("pretrained on 2591 videos from multiple sites", "jhuvpt_mlanthology")]),
    "input": {"frame_size": "not stated in accessible text", "frame_rate_or_sampling": "not stated in accessible text", "clip_length_frames": "not stated in accessible text",
              "notes": "spatiotemporal (video) JEPA encoder per abstract", "quotes": []},
    "embedding_dim": {"value": None, "basis": "not stated in accessible text", "quotes": []},
    "params": {"value": "not stated in accessible text", "quotes": []},
    "flops_per_input_if_documented": {"value": None, "statement": "not documented in accessible text", "quotes": []},
    "eligibility": elig(
        C("UNKNOWN", "No public weights link found (abstract page, web search); full paper not retrievable to confirm a release statement."),
        C("UNKNOWN", "No licence found."),
        C("PASS", "Self-supervised JEPA pretraining on cataract-surgery video."),
        C("UNKNOWN", "Abstract gives counts ('2591 videos from multiple sites') only; the source list may be in the inaccessible full text."),
        "Ophthalmic microscope video, far from laparoscopic appendectomy."),
}
