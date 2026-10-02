"""CrossScope: dual-scope (Mother-Child ERCP) surgical world model - weights not announced."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "CrossScope (role-asymmetric dual-scope world model for Mother-Child ERCP video prediction)",
    "aliases": [],
    "group": "endoscopic video world model",
    "paper": {"title": "CrossScope: A Role-Asymmetric World Model for Joint Dual-Scope Surgical Video Prediction", "year": 2026, "venue": "arXiv preprint (4 Aug 2026)", "arxiv": "2608.03211v1",
              "quotes": [Q("Title: CrossScope: A Role-Asymmetric World Model for Joint Dual-Scope Surgical Video Prediction", "crossscope_arxiv_abs")]},
    "version": {"value": "none released", "basis": "paper release statement covers phantom data, annotations, splits and evaluation code - not model weights",
                "quotes": [Q("The phantom videos, annotations, data splits, and evaluation code will be released, while real-world data will remain available only through controlled access", "crossscope_arxiv_pdf")]},
    "weights_location": {"url": None, "exists": "NO - no weights announced or linked (release statement lists data/annotations/evaluation code only)", "access": "not released",
                         "verification": "arXiv abs + PDF, 2026-10-02",
                         "quotes": [Q("The phantom videos, annotations, data splits, and evaluation code will be released", "crossscope_arxiv_pdf")]},
    "licence": {"code": "n/a", "weights": "n/a", "url": None, "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "flexible endoscopy (ERCP, Mother-Child dual scope) video prediction; phantom + real-world episodes",
               "quotes": [Q("we establish a paired dual-scope benchmark comprising synchronized phantom and real-world ERCP episodes", "crossscope_arxiv_pdf")]},
    "pretraining_data_quote": {"summary": "Own paired dual-scope ERCP benchmark (phantom + real-world, institution not extracted); DiT experts compared against Wan2.2 / Cosmos-H-Surgical baselines (base model not extracted).",
                               "datasets": ["Dual-scope ERCP phantom episodes", "Real-world ERCP episodes (controlled access)"],
                               "quotes": [Q("we establish a paired dual-scope benchmark comprising synchronized phantom and real-world ERCP episodes", "crossscope_arxiv_pdf")]},
    "appendix300_check": A300("UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
                              "ERCP flexible-endoscopy data (not laparoscopic appendectomy) from the authors' collection; base video model not extracted. Moot: no weights.", []),
    "input": {"frame_size": "not extracted", "frame_rate_or_sampling": "not extracted", "clip_length_frames": "9-frame clip per view (anchor + 8 predicted)", "notes": "two synchronized streams",
              "quotes": [Q("we predict eight frames after their observed anchors.", "crossscope_arxiv_pdf")]},
    "embedding_dim": {"value": "not stated", "basis": "", "quotes": []},
    "params": {"value": "not stated", "quotes": []},
    "flops_per_input_if_documented": NOFLOPS("not searched beyond abstract/method"),
    "eligibility": elig(C("FAIL", "No weights released or announced."), C("UNKNOWN", "No licence (nothing released)."),
                        C("PASS", "Trained on endoscopic (ERCP) video."), C("UNKNOWN", "Own dataset described (phantom + real ERCP); source institution not extracted."), "Not usable: no weights."),
}

REC["weights_location"]["quotes"].append(Q("search='CrossScope' status=200 n=0 ids=[]", "hf_model_search_generative"))
