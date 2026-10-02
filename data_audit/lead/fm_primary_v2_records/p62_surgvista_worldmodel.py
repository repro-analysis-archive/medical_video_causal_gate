"""SurgVista (world model, arXiv 2606.19889) - NOT the SurgVISTA encoder; no released weights found."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "SurgVista world model (long-horizon action-conditioned surgical world modeling; Wan2.1-1.3B based) - distinct from the SurgVISTA video encoder",
    "aliases": ["SurgWorld-Bench"],
    "group": "surgical video world model",
    "paper": {"title": "SurgVista: Long-Horizon Surgical World Modeling with Plausible Instrument-Tissue Dynamics", "year": 2026, "venue": "arXiv preprint (18 Jun 2026)", "arxiv": "2606.19889v1",
              "quotes": [Q("Title: SurgVista: Long-Horizon Surgical World Modeling with Plausible Instrument-Tissue Dynamics", "surgvistawm_arxiv_abs")]},
    "version": {"value": "none released (no code/weights link in the arXiv abstract page or paper)", "basis": "abs page links + PDF search for github/huggingface/release",
                "quotes": [Q("arXiv:2606.19889v1 [cs.CV] 18 Jun 2026", "surgvistawm_arxiv_pdf")]},
    "weights_location": {"url": None, "exists": "NO - no code or weight link found (arXiv abs page external links, PDF text); HF model search 'SurgVista' returns only syangcw/SurgVISTA (the unrelated encoder)",
                         "access": "not released", "verification": "arXiv abs + PDF + HF search, 2026-10-02", "quotes": []},
    "licence": {"code": "n/a", "weights": "n/a", "url": None, "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "surgical video world model fine-tuned from general-domain Wan2.1-1.3B on GraSP, SurgToolLoc22, CholecTrack20",
               "quotes": [Q("SurgVista builds on Wan2.1-1.3B and is trained for 100K iterations at 512×320 resolution with a clip length of 81 frames.", "surgvistawm_arxiv_pdf")]},
    "pretraining_data_quote": {"summary": "SurgWorld-Bench from GraSP (prostatectomy), SurgToolLoc22 (porcine), CholecTrack20 (cholecystectomy); base Wan2.1-1.3B.",
                               "datasets": ["GraSP", "SurgToolLoc22", "CholecTrack20", "Base: Wan2.1-1.3B"],
                               "quotes": [Q("SurgWorld-Bench draws from three public datasets covering three surgical procedure types (Fig. 4a): GraSP [2] for radical prostatectomy, SurgToolLoc22 [40] for porcine laparoscopic procedures, and CholecTrack20 [26] for laparoscopic cholecystectomy", "surgvistawm_arxiv_pdf")]},
    "appendix300_check": A300("UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
                              "Surgical data are three named public datasets (no appendectomy); base Wan2.1 general web-scale pretraining not enumerated. Moot: no weights.", []),
    "input": {"frame_size": "512x320", "frame_rate_or_sampling": "not extracted", "clip_length_frames": "81", "notes": "",
              "quotes": [Q("trained for 100K iterations at 512×320 resolution with a clip length of 81 frames.", "surgvistawm_arxiv_pdf")]},
    "embedding_dim": {"value": "not stated (Wan2.1 VAE latent)", "basis": "", "quotes": []},
    "params": {"value": "~1.3B (Wan2.1-1.3B base)", "quotes": [Q("SurgVista builds on Wan2.1-1.3B", "surgvistawm_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP' in paper"),
    "eligibility": elig(C("FAIL", "No released weights found."), C("UNKNOWN", "No licence (nothing released)."),
                        C("PASS", "Fine-tuned on surgical video."), C("PASS", "Paper names GraSP, SurgToolLoc22, CholecTrack20."), "Not usable: no weights."),
}

REC["weights_location"]["quotes"].append(Q("search='SurgVista' status=200 n=1 ids=['syangcw/SurgVISTA']", "hf_model_search_generative"))
