"""HiEndo: two-stage high-resolution laparoscopy video generation (Comput Assist Surg 2025) - no released weights found."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "HiEndo (two-stage high-resolution GI laparoscopy video generation, Endora-based DiT + super-resolution)",
    "aliases": [],
    "group": "surgical video generative model",
    "paper": {"title": "HiEndo: harnessing large-scale data for generating high-resolution laparoscopy videos under a two-stage framework", "year": 2025,
              "venue": "Computer Assisted Surgery 30(1):2536643 (doi 10.1080/24699322.2025.2536643)", "arxiv": None,
              "quotes": [Q("HiEndo: harnessing large-scale data for generating high-resolution laparoscopy videos under a two-stage framework.", "hiendo_pubmed_efetch")]},
    "version": {"value": "none released", "basis": "PubMed abstract has no code/weights statement; publisher full text returned HTTP 403 to the audit client", "quotes": []},
    "weights_location": {"url": None, "exists": "NO (none found) - no weights link in the abstract; full text not accessible here (tandfonline 403); no HF model found",
                         "access": "not found", "verification": "PubMed efetch + tandfonline (403), 2026-10-02", "quotes": []},
    "licence": {"code": "n/a", "weights": "n/a", "url": None, "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "gastrointestinal laparoscopy video generation",
               "quotes": [Q("we propose an innovative two-stage video generation architecture HiEndo for generating high-resolution gastrointestinal laparoscopy videos with high fidelity.", "hiendo_pubmed_efetch")]},
    "pretraining_data_quote": {"summary": "Self-collected large-scale GI laparoscopy dataset (61,270 clips); source institution not named in the abstract (authors include Renji Hospital, Shanghai).",
                               "datasets": ["Self-collected GI laparoscopy dataset (61,270 clips; unnamed source)", "Initial start: Endora"],
                               "quotes": [Q("We also collect a large-scale gastrointestinal laparoscopy video dataset with 61,270 video clips for training and validation of our proposed method.", "hiendo_pubmed_efetch")]},
    "appendix300_check": A300("UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
                              "Self-collected laparoscopy dataset of unnamed origin (full text not accessible) - cannot be excluded. Moot: no weights.",
                              [Q("We also collect a large-scale gastrointestinal laparoscopy video dataset with 61,270 video clips", "hiendo_pubmed_efetch")]),
    "input": {"frame_size": "not extracted (abstract: low-resolution first stage, super-resolved second stage)", "frame_rate_or_sampling": "not extracted", "clip_length_frames": "not extracted", "notes": "",
              "quotes": [Q("In the first stage, we build a diffusion transformer for generating a low-resolution laparoscopy video upon the basic capability of Endora as an initial start.", "hiendo_pubmed_efetch")]},
    "embedding_dim": {"value": "not stated", "basis": "", "quotes": []},
    "params": {"value": "not stated", "quotes": []},
    "flops_per_input_if_documented": NOFLOPS("abstract only"),
    "eligibility": elig(C("FAIL", "No released weights found."), C("UNKNOWN", "No licence (nothing released)."),
                        C("PASS", "Trained on laparoscopy video."), C("UNKNOWN", "Abstract describes a self-collected dataset without naming its source; full text inaccessible."), "Not usable: no weights."),
}

REC["weights_location"]["quotes"].append(Q("search='HiEndo' status=200 n=1 ids=['sunyanming/hi-en-double_nohint-lora_model']", "hf_model_search_generative"))
