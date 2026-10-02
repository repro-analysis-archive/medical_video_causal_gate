"""Cosmos-Surg-dVRK (NVIDIA/JHU, arXiv 2510.16240) - no official weight release found."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "Cosmos-Surg-dVRK (action-conditioned Cosmos-Predict2-2B fine-tune for dVRK policy evaluation)",
    "aliases": [],
    "group": "surgical video world model",
    "paper": {"title": "Cosmos-Surg-dVRK: World Foundation Model-based Automated Online Evaluation of Surgical Robot Policy Learning", "year": 2025, "venue": "arXiv preprint", "arxiv": "2510.16240",
              "quotes": [Q("Cosmos-Surg-dVRK: World Foundation Model-based Automated Online Evaluation of Surgical Robot Policy Learning", "cosmossurgdvrk_arxiv_abs")]},
    "version": {"value": "none released by the authors (only unofficial third-party HF repos named 'cosmos3-nanoh-surgical-dvrk' found)", "basis": "paper text + HF search 'Surg-dVRK'", "quotes": []},
    "weights_location": {"url": None, "exists": "NO (official) - no weight link in the paper; HF search finds only third-party repos (chrisvoncsefalvay/, introvoyz041/cosmos3-nanoh-surgical-dvrk) not attributable to the authors. Its dVRK suturing data are reused by Cosmos-H-Dreams (separate record).",
                         "access": "not released", "verification": "PDF search + HF model search, 2026-10-02", "quotes": []},
    "licence": {"code": "n/a", "weights": "n/a", "url": None, "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "dVRK tabletop suture-pad and ex vivo porcine cholecystectomy video (action-conditioned)",
               "quotes": [Q("For both the tabletop and cholecystectomy datasets, we separately finetune the action-conditional Cosmos WFM model Cosmos-Predict2-2B-Video2World (NVIDIA Cosmos, 2025) with video and kinematic action paired data sampled at 10 Hz", "cosmossurgdvrk_arxiv_pdf")]},
    "pretraining_data_quote": {"summary": "Authors' dVRK tabletop and cholecystectomy (ex vivo) datasets; base Cosmos-Predict2-2B.", "datasets": ["dVRK tabletop suturing (JHU)", "dVRK ex vivo porcine cholecystectomy", "Base: Cosmos-Predict2-2B"],
                               "quotes": [Q("we separately finetune the action-conditional Cosmos WFM model Cosmos-Predict2-2B-Video2World", "cosmossurgdvrk_arxiv_pdf")]},
    "appendix300_check": A300("UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
                              "dVRK lab data (tabletop / ex vivo) contain no patient appendectomy; base Cosmos-Predict2 general pretraining not enumerated. Moot: no weights.", []),
    "input": {"frame_size": "not extracted", "frame_rate_or_sampling": "10 Hz", "clip_length_frames": "not extracted", "notes": "video + kinematic action pairs",
              "quotes": [Q("with video and kinematic action paired data sampled at 10 Hz", "cosmossurgdvrk_arxiv_pdf")]},
    "embedding_dim": {"value": "not stated (Cosmos-Predict2 latent)", "basis": "", "quotes": []},
    "params": {"value": "~2B (Cosmos-Predict2-2B base)", "quotes": [Q("Cosmos-Predict2-2B-Video2World", "cosmossurgdvrk_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("not searched beyond method"),
    "eligibility": elig(C("FAIL", "No official weights released."), C("UNKNOWN", "No licence (nothing released)."),
                        C("PASS", "Fine-tuned on surgical-robot video (tabletop/ex vivo)."), C("UNKNOWN", "Own dVRK datasets described, not separately published as named datasets in the saved text."), "Not usable: no official weights."),
}

REC["weights_location"]["quotes"].append(Q("search='Surg-dVRK' status=200 n=2 ids=['chrisvoncsefalvay/cosmos3-nanoh-surgical-dvrk', 'introvoyz041/cosmos3-nanoh-surgical-dvrk']", "hf_model_search_generative"))
