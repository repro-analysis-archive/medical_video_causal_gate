"""SurGen: Text-Guided Diffusion Model for Surgical Video Generation (CogVideoX-2B on Cholec80) - no released weights found."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "SurGen (text-guided surgical video diffusion; CogVideoX-2B adapted to Cholec80)",
    "aliases": [],
    "group": "surgical video generative model",
    "paper": {"title": "SurGen: Text-Guided Diffusion Model for Surgical Video Generation", "year": 2024, "venue": "arXiv preprint (v3 24 Sep 2024)", "arxiv": "2408.14028v3",
              "quotes": [Q("arXiv:2408.14028v3 [cs.CV] 24 Sep 2024", "surgen_arxiv_pdf")]},
    "version": {"value": "none released", "basis": "no code/weights link on arXiv abs page or in paper (only a placeholder 'github.com/yourlink' inside a reference)", "quotes": []},
    "weights_location": {"url": None, "exists": "NO - no code or weight link found; HF model search 'SurGen' returns no SurGen video model", "access": "not released",
                         "verification": "arXiv abs + PDF + HF search, 2026-10-02", "quotes": []},
    "licence": {"code": "n/a", "weights": "n/a", "url": None, "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "laparoscopic cholecystectomy video generation (fine-tuned CogVideoX)",
               "quotes": [Q("SurGen leverages a video diffusion architecture based on CogVideoX [19] to generate videos of surgical procedures with a higher resolution (720 x 480 pixels, width x height) and longer duration (49 frames)", "surgen_arxiv_pdf")]},
    "pretraining_data_quote": {"summary": "Cholec80 (first 40 videos for training; 200,000 frame sequences); base CogVideoX (general domain).",
                               "datasets": ["Cholec80", "Base: CogVideoX"],
                               "quotes": [Q("The data used for model training and evaluation is sourced from Cholec80 [27], a dataset of 80 laparoscopic cholecystectomy procedures performed by 13 surgeons.", "surgen_arxiv_pdf")]},
    "appendix300_check": A300("UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
                              "Surgical data = Cholec80 only; base CogVideoX general web-scale pretraining not enumerated. Moot: no weights.", []),
    "input": {"frame_size": "720x480 (W x H)", "frame_rate_or_sampling": "not extracted", "clip_length_frames": "49", "notes": "",
              "quotes": [Q("(720 x 480 pixels, width x height) and longer duration (49 frames)", "surgen_arxiv_pdf")]},
    "embedding_dim": {"value": "not stated in saved text (CogVideoX 3D VAE)", "basis": "", "quotes": []},
    "params": {"value": "2B", "quotes": [Q("a 2 billion parameter text-guided diffusion model adapted to laparoscopic cholecystectomy procedures.", "surgen_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP' in paper"),
    "eligibility": elig(C("FAIL", "No released weights found."), C("UNKNOWN", "No licence (nothing released)."),
                        C("PASS", "Fine-tuned on laparoscopic surgery video."), C("PASS", "Paper names Cholec80."), "Not usable: no weights."),
}

REC["weights_location"]["quotes"].append(Q("search='SurGen' status=200 n=6", "hf_model_search_generative"))
