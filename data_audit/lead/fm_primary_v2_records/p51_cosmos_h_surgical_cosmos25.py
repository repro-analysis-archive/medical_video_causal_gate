"""Cosmos-H-Surgical-Predict / -Transfer (Cosmos 2.5 based, 2B; HF branch cosmos-2.5, tags v0.2.0/v0.3.0)."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "Cosmos-H-Surgical-Predict / Cosmos-H-Surgical-Transfer (Cosmos-Predict2.5-2B / Cosmos-Transfer2.5-2B post-trained; HF branch cosmos-2.5)",
    "aliases": ["SurgWorld world model (arXiv 2512.23162)", "nvidia/cosmos-h-surgical-predict"],
    "group": "surgical video world / generative model",
    "paper": {
        "title": "Cosmos-H-Surgical: Learning Surgical Robot Policies from Videos via World Modeling (SurgWorld)",
        "year": "2025-2026", "venue": "arXiv preprint", "arxiv": "2512.23162v4",
        "quotes": [Q("A powerful world model (Cosmos-H-Surgical) is built using Cosmos2.5 [1] and SATA, which is able to generate high quality, generalizable videos for surgical robots.", "surgworld_arxiv_pdf"),
                   Q("arXiv:2512.23162v4 [cs.RO] 11 Mar 2026", "surgworld_arxiv_pdf")],
    },
    "version": {
        "value": "HF branch cosmos-2.5 (sha 92d2558c3329c91fa77002f6604987ba8a6ce29a; tags v0.2.0 / v0.3.0); model versions 0.1 (legacy predict/, transfer/{depth,edge,seg,vis}) and 0.2 (openmdw-1.1/ edition of the same checkpoints)",
        "basis": "HF refs API + cosmos-2.5 README 'Model Version(s)'",
        "quotes": [Q('{"name":"cosmos-2.5","ref":"refs/heads/cosmos-2.5","targetCommit":"92d2558c3329c91fa77002f6604987ba8a6ce29a"}', "cosmoshsurg_hf_refs"),
                   Q('{"name":"v0.2.0","ref":"refs/tags/v0.2.0"', "cosmoshsurg_hf_refs"),
                   Q("0.1 - Initial release version for surgical robotics synthetic data generation", "cosmoshsurg25_hf_readme"),
                   Q("0.2 - OpenMDW-1.1 checkpoint edition for Predict and Transfer", "cosmoshsurg25_hf_readme")],
    },
    "weights_location": {
        "url": "https://huggingface.co/nvidia/Cosmos-H-Surgical/tree/cosmos-2.5 (predict/cosmos-h-surgical-predict_model_ema_bf16.pt 4,118,575,006 B; transfer/{depth,edge,seg,vis}/..._model_ema_bf16.pt 4,716,357,097 B each; same files under openmdw-1.1/)",
        "exists": "YES - HF tree API for branch cosmos-2.5 lists the .pt checkpoints; repo gated=false (nothing downloaded)",
        "access": "public, not gated",
        "verification": "HF tree API (recursive) on branch cosmos-2.5 + repo-level API gated flag, 2026-10-02",
        "quotes": [Q('"path":"predict/cosmos-h-surgical-predict_model_ema_bf16.pt"', "cosmoshsurg25_hf_tree"),
                   Q('"path":"openmdw-1.1/predict/cosmos-h-surgical-predict_model_ema_bf16.pt"', "cosmoshsurg25_hf_tree"),
                   Q('"size":4118575006', "cosmoshsurg25_hf_tree"),
                   Q('"gated":false', "cosmoshsurg_hf_api")],
    },
    "licence": {
        "code": "OpenMDW-1.1 (cosmos-2.5 branch of the GitHub repo; not re-checked separately)",
        "weights": "Legacy predict/ + transfer/ checkpoints: NVIDIA-OneWay-Noncommercial-License ('noncommercially' = research or evaluation purposes only). openmdw-1.1/ edition: OpenMDW-1.1 (commercial and non-commercial).",
        "url": "https://huggingface.co/nvidia/Cosmos-H-Surgical/blob/cosmos-2.5/LICENSE.weights ; https://developer.download.nvidia.com/licenses/NVIDIA-OneWay-Noncommercial-License-22Mar2022.pdf",
        "code_and_weights_differ": "legacy weights non-commercial; OpenMDW edition permissive",
        "quotes": [Q("Checkpoint artifacts under predict/ and transfer/ are licensed under the NVIDIA-OneWay-Noncommercial-License, except for artifacts explicitly identified as OpenMDW-1.1 in release-manifest.json.", "cosmoshsurg25_hf_license_weights"),
                   Q("Only checkpoint artifacts under openmdw-1.1/ that are explicitly identified with license_id \"OpenMDW-1.1\" in release-manifest.json are licensed under the OpenMDW License Agreement, version 1.1.", "cosmoshsurg25_hf_license_weights"),
                   Q("As used herein, “noncommercially” means for research or evaluation purposes only.", "nvidia_oneway_nc_license"),
                   Q("permission is hereby granted, free of charge, to deal in the Model Materials without restriction", "cosmoshsurg25_hf_license_openmdw")],
    },
    "domain": {
        "value": "surgical video generation (first-frame + text -> 92 future frames; control video -> photorealistic surgical video); post-trained from general-domain Cosmos-Predict2.5-2B / Cosmos-Transfer2.5-2B on surgical endoscopic video",
        "quotes": [Q("Fine-tuned from Cosmos-Predict2.5-2B, the model takes a first frame image and a text description as input and predicts the next 92 future frames of surgical video.", "cosmoshsurg25_hf_readme"),
                   Q("we adopt Cosmos-Predict2.5 [1], a large-scale video world model pretrained on diverse robotic and embodied datasets, as our base model and adapt it to the surgical domain.", "surgworld_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "Legacy checkpoints: public surgical video datasets Cholec80, CholecT50, HeiChole (cholecystectomy), GraSP, SAR-RARP50 (RARP), AutoLaparo (hysterectomy), MultiBypass140 (gastric bypass), SurgicalActions160 (gynecologic laparoscopy), SutureBot (ex-vivo phantom); the paper's SATA corpus (2,447 clips) additionally names HeiCo and 'credentialed YouTube surgical channels' (ref [32], Schmidgall et al.). OpenMDW edition: GraSP + synthetic surgical data. Base: Cosmos-Predict2.5-2B / Cosmos-Transfer2.5-2B (general domain).",
        "datasets": ["Cholec80", "CholecT50", "HeiChole", "GraSP", "SAR-RARP50", "AutoLaparo", "MultiBypass140", "SurgicalActions160", "SutureBot (ex vivo)",
                     "per paper (SATA): HeiCo, YouTube surgical channels (68 knotting clips)", "OpenMDW edition: GraSP + synthetic surgical data",
                     "Base: Cosmos-Predict2.5-2B / Cosmos-Transfer2.5-2B"],
        "quotes": [Q("The collection covers thousands of surgical videos and hundreds of thousands of annotated frames across multiple procedure types — laparoscopic cholecystectomy (Cholec80, CholecT50, HeiChole), robot-assisted radical prostatectomy (GraSP, SAR-RARP50), laparoscopic hysterectomy (AutoLaparo), laparoscopic Roux-en-Y gastric bypass (MultiBypass140), gynecologic laparoscopy (SurgicalActions160), and robotic suturing (SutureBot).", "cosmoshsurg25_hf_readme"),
                   Q("The commercial-friendly OpenMDW-1.1 checkpoints under `openmdw-1.1/` were trained using the GraSP dataset and synthetic surgical data.", "cosmoshsurg25_hf_readme"),
                   Q("SATA is curated by aggregating and re-annotating videos from credentialed YouTube surgical channels [32] and publicly available datasets, including GraSP [33], SAR-RARP50 [34], Multiypass140 [35], SurgicalActions160 [36], AutoLaparo [37], and HeiCo [38].", "surgworld_arxiv_pdf"),
                   Q("Dataset AutoLaparo [37] GraSP [33] HeiCo [38] Multiypass140 [35] SAR-RARP50 [34] SurgicalActions160 [36] YouTube [32] Knotting 47 37 16 1 118 7 68", "surgworld_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "The named surgical datasets contain no appendectomy and no Appendix300 centre (HeiChole/HeiCo are Heidelberg-area, not Dresden). Cannot be excluded: "
        "(i) the paper's SATA corpus includes clips from 'credentialed YouTube surgical channels' (ref [32]) whose origin is not documented; "
        "(ii) the general-domain base models Cosmos-Predict2.5-2B / Cosmos-Transfer2.5-2B were pretrained on web-scale / proprietary video not enumerated. "
        "The model card and paper data lists also differ (card omits YouTube/HeiCo).",
        [Q("videos from credentialed YouTube surgical channels [32]", "surgworld_arxiv_pdf")]),
    "input": {
        "frame_size": "Predict 720P: first-frame image 1280x704, output 1280x704; Transfer: control video 1280x720",
        "frame_rate_or_sampling": "16 FPS",
        "clip_length_frames": "Predict: 1 conditioning frame -> 92 generated frames (~5.8 s); Transfer: control videos in multiples of 93 frames work best",
        "notes": "Text prompt < 300 words; Predict requires a first frame (no text-only generation).",
        "quotes": [Q("For the 720P model, the input image should be 1280x704.", "cosmoshsurg25_hf_readme"),
                   Q("92 frames at 1280x704, 16 FPS (~5.8 seconds of video)", "cosmoshsurg25_hf_readme"),
                   Q("a length which is multiples of 93 frames (e.g., 93, 186, or 279 frames) performs the best.", "cosmoshsurg25_hf_readme"),
                   Q("The control input video should have a spatial resolution of 1280x720 for the 720P model.", "cosmoshsurg25_hf_readme")],
    },
    "embedding_dim": {
        "value": "Base Cosmos-Predict2.5-2B latent space: Wan2.1 video tokenizer, 16 latent channels at 8x spatial / 4x temporal compression; DiT hidden width 2048 (28 blocks, 16 heads)",
        "basis": "architecture of the base model Cosmos-Predict2.5-2B-Video2World as stated in NVIDIA's Cosmos-H-Dreams model card (the Cosmos-H-Surgical cosmos-2.5 card does not state it); Transfer2.5-2B assumed to share the tokenizer (not verified)",
        "quotes": [Q("Cosmos-Predict2.5-2B-Video2World, a 2B-parameter diffusion transformer for video generation in latent space (Wan2.1 video tokenizer, spatial compression 8×, temporal compression 4×, 16 latent channels; hidden width 2048, 28 blocks, 16 heads", "cosmoshdreams_hf_readme")],
    },
    "params": {"value": "2B (Predict; Transfer also 2B base)",
               "quotes": [Q("**Number of model parameters:** 2B", "cosmoshsurg25_hf_readme")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'GFLOP', 'latency' in the cosmos-2.5 model card and arXiv 2512.23162v4"),
    "eligibility": elig(
        C("PASS", "HF branch cosmos-2.5 lists predict/ and transfer/ .pt checkpoints (and openmdw-1.1/ copies); repo gated=false."),
        C("PASS", "Legacy weights: NVIDIA OneWay Noncommercial = 'research or evaluation purposes only' (research permitted); openmdw-1.1 edition: OpenMDW-1.1 (no use restriction)."),
        C("PASS", "LoRA/post-training of Cosmos-Predict2.5-2B / Transfer2.5-2B on surgical endoscopic video (general-domain initialisation recorded)."),
        C("PASS", "Model card and paper name the surgical datasets (card list; paper SATA source table incl. YouTube channels). Caveat: base Cosmos 2.5 pretraining data not enumerated."),
        "Two weight editions with different licences; the legacy edition is non-commercial."),
}
