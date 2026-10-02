"""SurgWM: Surgical Vision World Model (Genie-style, latent actions) - no released weights."""
from ._common import A300, C, NOFLOPS, NOT_MENTIONED, Q, elig

REC = {
    "name": "SurgWM (Surgical Vision World Model; Genie-style video tokenizer + latent action model + dynamics model)",
    "aliases": ["Surgical Vision World Model", "bhattarailab/Surgical-Vision-World-Model"],
    "group": "surgical video world model",
    "paper": {"title": "Surgical Vision World Model", "year": 2025, "venue": "arXiv preprint (v2 26 Sep 2025)", "arxiv": "2503.02904",
              "quotes": [Q("arXiv:2503.02904v2 [eess.IV] 26 Sep 2025", "surgwm_arxiv_pdf")]},
    "version": {"value": "none released (GitHub README: 'Codes coming soon!')", "basis": "GitHub README at check time",
                "quotes": [Q("## Codes coming soon!", "surgwm_github_readme")]},
    "weights_location": {"url": None, "exists": "NO - the official repository contains only a 'Codes coming soon!' README; no weights or code; HF model search 'SurgWM' returns nothing",
                         "access": "not released", "verification": "raw README + GitHub repo page, 2026-10-02",
                         "quotes": [Q("## Codes coming soon!", "surgwm_github_readme")]},
    "licence": {"code": "none (no code released)", "weights": "none", "url": "https://github.com/bhattarailab/Surgical-Vision-World-Model",
                "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "robot-assisted (porcine) surgical video world model trained on SurgToolLoc2022",
               "quotes": [Q("the architecture design is verified with extensive experiments on the unlabeled SurgToolLoc2022 dataset.", "surgwm_arxiv_pdf")]},
    "pretraining_data_quote": {"summary": "SurgToolLoc2022 (24,695 30-s clips at 60 fps, 1280x720, from one endoscope channel).",
                               "datasets": ["SurgToolLoc2022"],
                               "quotes": [Q("The dataset consists of 30seconds long 24,695 video clips, captured at 60 fps at a resolution of 1280 x 720, from one channel of the endoscope.", "surgwm_arxiv_pdf")]},
    "appendix300_check": A300("NO", NOT_MENTIONED, False,
                              "Single named dataset (SurgToolLoc2022, porcine robotic training procedures); no YouTube or in-house data stated. Moot: no weights released.",
                              [Q("extensive experiments on the unlabeled SurgToolLoc2022 dataset", "surgwm_arxiv_pdf")]),
    "input": {"frame_size": "center crop 900x600 (latent action model trained at 60x40)", "frame_rate_or_sampling": "1 fps", "clip_length_frames": "16",
              "notes": "", "quotes": [Q("All models are trained on 16 frame clips sampled at 1 fps from the videos. A center crop of 900 x 600 pixels is applied", "surgwm_arxiv_pdf"),
                                      Q("we train the latent action model on a lower resolution of 60 x 40 pixels.", "surgwm_arxiv_pdf")]},
    "embedding_dim": {"value": "not stated in saved sources (VQ-VAE discrete tokens)", "basis": "", "quotes": [Q("It is trained using the standard VQ-VAE objective [20].", "surgwm_arxiv_pdf")]},
    "params": {"value": "not stated", "quotes": []},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'parameter' in paper"),
    "eligibility": elig(C("FAIL", "No weights (or code) released: 'Codes coming soon!'."), C("UNKNOWN", "No licence (nothing released)."),
                        C("PASS", "Trained on surgical (porcine robotic) endoscopic video."), C("PASS", "Paper names SurgToolLoc2022."),
                        "Not usable: no weights."),
}

REC["weights_location"]["quotes"].append(Q("search='SurgWM' status=200 n=0 ids=[]", "hf_model_search_generative"))
