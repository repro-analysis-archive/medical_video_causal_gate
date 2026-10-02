"""VISAGE: Video Synthesis using Action Graphs for Surgery (MICCAI 2024 EARTH workshop) - no released weights found."""
from ._common import A300, C, NOFLOPS, NOT_MENTIONED, Q, elig

REC = {
    "name": "VISAGE (action-graph-conditioned future video generation for laparoscopy; CholecT50)",
    "aliases": [],
    "group": "surgical video generative model",
    "paper": {"title": "VISAGE: Video Synthesis using Action Graphs for Surgery", "year": 2024, "venue": "MICCAI 2024 EARTH workshop", "arxiv": "2410.17751v2",
              "quotes": [Q("arXiv:2410.17751v2 [cs.CV] 30 Oct 2024", "visage_arxiv_pdf")]},
    "version": {"value": "none released", "basis": "no code/weights link on arXiv abs page or in paper", "quotes": []},
    "weights_location": {"url": None, "exists": "NO - no code or weight link found (HF model search 'VISAGE' returns no surgical model)", "access": "not released",
                         "verification": "arXiv abs + PDF + HF search, 2026-10-02", "quotes": []},
    "licence": {"code": "n/a", "weights": "n/a", "url": None, "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "laparoscopic cholecystectomy video generation (video latent diffusion)",
               "quotes": [Q("VISAGE predicts the future frames given only a single initial frame, and the action graph triplets.", "visage_arxiv_pdf")]},
    "pretraining_data_quote": {"summary": "CholecT50.", "datasets": ["CholecT50"],
                               "quotes": [Q("We conduct extensive experiments on the CholecT50 dataset", "visage_arxiv_pdf")]},
    "appendix300_check": A300("NO", NOT_MENTIONED, False, "Single named dataset (CholecT50, cholecystectomy). Initialisation of the VLDM/autoencoder not extracted. Moot: no weights.", []),
    "input": {"frame_size": "not extracted", "frame_rate_or_sampling": "not extracted", "clip_length_frames": "7-frame scenes for the SVD baseline (own model length not extracted)", "notes": "",
              "quotes": [Q("we fix 7 as the frame count of each scene.", "visage_arxiv_pdf")]},
    "embedding_dim": {"value": "not stated", "basis": "", "quotes": []},
    "params": {"value": "not stated", "quotes": []},
    "flops_per_input_if_documented": NOFLOPS("not searched beyond method/experiments"),
    "eligibility": elig(C("FAIL", "No released weights found."), C("UNKNOWN", "No licence (nothing released)."),
                        C("PASS", "Trained on laparoscopic surgery video."), C("PASS", "Paper names CholecT50."), "Not usable: no weights."),
}

REC["weights_location"]["quotes"].append(Q("search='VISAGE' status=200 n=30", "hf_model_search_generative"))
