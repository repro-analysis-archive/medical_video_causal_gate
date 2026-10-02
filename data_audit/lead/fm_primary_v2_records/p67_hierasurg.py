"""HieraSurg: Hierarchy-Aware Diffusion Model for Surgical Video Generation (MICCAI 2025) - weights 'TODO'."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "HieraSurg (HieraSurg-S2M + HieraSurg-M2V, CogVideoX-2B based surgical video generation)",
    "aliases": [],
    "group": "surgical video generative model",
    "paper": {"title": "HieraSurg: Hierarchy-Aware Diffusion Model for Surgical Video Generation", "year": 2025, "venue": "MICCAI 2025", "arxiv": "2506.21287v1",
              "quotes": [Q("arXiv:2506.21287v1 [cs.CV] 26 Jun 2025", "hierasurg_arxiv_pdf")]},
    "version": {"value": "none released (README feature list: 'TODO (upload weights)')", "basis": "GitHub repo page README", "quotes": [Q("TODO (upload weights)", "hierasurg_github_page")]},
    "weights_location": {"url": None, "exists": "NO - README marks weight upload as TODO", "access": "not released", "verification": "GitHub repo page, 2026-10-02",
                         "quotes": [Q("TODO (upload weights)", "hierasurg_github_page")]},
    "licence": {"code": "not extracted (README has a 'License' section heading; text not captured)", "weights": "n/a", "url": "https://github.com/diegobiagini/HieraSurg", "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "laparoscopic cholecystectomy video generation (CogVideoX-2B fine-tune)",
               "quotes": [Q("HieraSurg is a pair of video diffusion model based on CogVideoX, enabling the realistic generation of surgical videos.", "hierasurg_github_page")]},
    "pretraining_data_quote": {"summary": "Cholec80 and CholecT50/CholecT45; base CogVideoX-2B (general domain).", "datasets": ["Cholec80", "CholecT50 / CholecT45", "Base: CogVideoX-2B"],
                               "quotes": [Q("All the data used is from Cholec80 and CholecT50", "hierasurg_github_page"),
                                          Q("on the CogVideoX-2B [2] architecture-a latent Diffusion Transformer (DiT) [20]", "hierasurg_arxiv_pdf")]},
    "appendix300_check": A300("UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
                              "Surgical data are Cholec80/CholecT50 (cholecystectomy); base CogVideoX general web-scale pretraining not enumerated. Moot: no weights.", []),
    "input": {"frame_size": "not extracted", "frame_rate_or_sampling": "evaluation script name suggests 8 fps ('evaluate_metrics_8fps')", "clip_length_frames": "not extracted", "notes": "",
              "quotes": [Q("evaluate_metrics_8fps", "hierasurg_github_page")]},
    "embedding_dim": {"value": "not stated", "basis": "", "quotes": []},
    "params": {"value": "~2B (CogVideoX-2B base)", "quotes": [Q("on the CogVideoX-2B [2] architecture", "hierasurg_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("not searched beyond method"),
    "eligibility": elig(C("FAIL", "Weights not uploaded (README TODO)."), C("UNKNOWN", "Licence text not captured."),
                        C("PASS", "Fine-tuned on laparoscopic surgery video."), C("PASS", "Names Cholec80 / CholecT50."), "Not usable: no weights."),
}

REC["weights_location"]["quotes"].append(Q("search='HieraSurg' status=200 n=0 ids=[]", "hf_model_search_generative"))


# --- lead completion (2026-10-02) ---
REC["licence"]["code"] = "Creative Commons 4.0, non-commercial scientific research (README 'License' section; variant not specified)"
REC["licence"]["weights"] = "n/a (weights not uploaded; README TODO)"
REC["licence"]["quotes"] = [Q("This code may be used for non-commercial scientific research purposes as defined by Creative Commons 4.0 .", "hierasurg_github_page")]
REC.setdefault("changes_vs_previous", []).append("Lead: licence text filled from the repository page (README section was 'not captured' by fork C).")
