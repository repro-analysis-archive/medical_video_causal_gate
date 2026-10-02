"""OmniRAS (V-JEPA-2.1 continued pretraining on robot-assisted surgery video) (new entry, fork A)."""
from ._common import A300, C, Q, elig

REC = {
    "name": "OmniRAS (V-JEPA-2.1 ViT-g 1B / ViT-G 2B, surgical continued pretraining)",
    "aliases": ["OmniRAS 1B", "OmniRAS 2B"],
    "paper": {
        "title": "OmniRAS: Standardizing Foundation Model Training and Evaluation in Robot-Assisted Surgery",
        "year": 2026, "venue": "arXiv 2608.31048 (under review at IEEE T-RO)", "arxiv": "2608.31048",
        "quotes": [Q("Under review at IEEE Transactions on Robotics (T-RO)", "omniras_arxiv_abs"),
                   Q("We present OmniRAS, a family of 1B- and 2B-parameter V-JEPA-2.1 encoders for robot-assisted surgery", "omniras_arxiv_pdf")],
    },
    "version": {
        "value": "OmniRAS 1B (ViT-g) and OmniRAS 2B (ViT-G) checkpoints; production runs of 9.22M / 18.43M / 36.86M samples; no public file names (request-only)",
        "basis": "paper + project page; checkpoints not listed publicly",
        "quotes": [Q("| OmniRAS checkpoints (1B, 2B) | [Request access][access-form] |", "omniras_github_readme"),
                   Q("including three production runs of 9.22 M, 18.43 M, and 36.86 M samples", "omniras_arxiv_pdf")],
    },
    "weights_location": {
        "url": "https://docs.google.com/forms/d/e/1FAIpQLSfXCTF9ISdQ3a_I87wYowRh-0QNLWzCC3ZqQ7wpqbnlgZMN0A/viewform (access request form; no public file URL)",
        "exists": "UNKNOWN - checkpoints are offered only via a Google Form (email, affiliation, intended use); no file listing is public. Not requested.",
        "access": "request form (manual)",
        "verification": "project page, GitHub README and the form page fetched (HTML only), 2026-10-02",
        "quotes": [Q("To request access to the checkpoints or datasets, complete the [Google Form][access-form].", "omniras_github_readme"),
                   Q("OmniRAS - access form", "omniras_request_form"),
                   Q("Checkpoints request access", "omniras_project_page")],
    },
    "licence": {
        "code": "repository contents (project page, manuscript, figures, docs) CC BY 4.0; training/eval code 'will be released under a separate software license'",
        "weights": "not yet licensed: 'Model checkpoints, which will be released under their own terms.'",
        "url": "https://github.com/Borgioli/omniras/blob/main/LICENSE",
        "code_and_weights_differ": "yes - CC BY 4.0 excludes checkpoints, code and datasets",
        "quotes": [Q("Creative Commons Attribution 4.0 International (CC BY 4.0)", "omniras_github_license"),
                   Q("* Model checkpoints, which will be released under their own terms.", "omniras_github_license")],
    },
    "domain": {
        "value": "surgical video, 51% da Vinci robotic + laparoscopic/mixed; V-JEPA-2.1 continued pretraining from Meta general-video weights, with Kinetics-400 rehearsal",
        "quotes": [Q("Billion-scale V-JEPA-2.1 encoders are continued-pretrained at up to 256 nodes on a 19-source, approximately 2,650-hour surgical-video catalog that is 51% da Vinci robotic video by hours", "omniras_arxiv_pdf"),
                   Q("initialized from the publicly released general-video weights and continued on a domain- 6 focused surgical corpus.", "omniras_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "19 sources (~2,650 h): private robotic collection (427 h), SurgToolLoc/SurgVU, GraSP, SurgeNet robotic + laparoscopic subsets, Cholec80, HeiChole, MultiBypass140, GynSurg, LapGyn6, LEMON/Surg-3M (YouTube-scraped), JIGSAWS, SurgVisDom, CRCD, EndoVis/MICCAI instrument sets; non-surgical anchors Kinetics-400 and Open-H-Embodiment.",
        "datasets": ["private robotic collection (427 h)", "SurgToolLoc/SurgVU", "GraSP", "SurgeNet robotic subset", "Cholec80", "HeiChole", "MultiBypass140", "GynSurg", "LapGyn6",
                     "SurgeNet laparoscopic subset", "LEMON/Surg-3M (YouTube-scraped)", "JIGSAWS", "SurgVisDom", "CRCD", "EndoVis/MICCAI instrument sets", "Kinetics-400", "Open-H-Embodiment"],
        "quotes": [Q("The robotic sources are our private contribution (427h), SurgToolLoc/SurgVU, GraSP (robotic radical prostatectomy), and a scrubbed SurgeNet robotic subset.", "omniras_arxiv_pdf"),
                   Q("The laparoscopic and mixed-modality sources are Cholec80, HeiChole, MultiBypass140 (gastric bypass), the gynecologic sets GynSurg and LapGyn6, a laparoscopic SurgeNet subset, the multi-procedure LEMON/Surg-3M collection, and a bundle of smaller established benchmarks (JIGSAWS, SurgVisDom, CRCD, and several EndoVis/MICCAI instrument sets).", "omniras_arxiv_pdf"),
                   Q("the catalog adds two non-surgical anchors: Kinetics-400", "omniras_arxiv_pdf"),
                   Q("lemon · YouTube-scraped", "omniras_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "UNKNOWN", "lemon · YouTube-scraped", True,
        "The documented list does not mention DS203/Appendix300 or its centres, but it includes LEMON (YouTube-scraped, contains appendectomy "
        "videos of undocumented origin), SurgeNet subsets (whose XL version includes YouTube), a 427 h private robotic collection and an unnamed "
        "'bundle' of smaller benchmarks; these cannot be excluded.",
        [Q("the multi-procedure LEMON/Surg-3M collection", "omniras_arxiv_pdf")]),
    "input": {
        "frame_size": "not stated precisely ('cropped at high resolution')",
        "frame_rate_or_sampling": "4 fps",
        "clip_length_frames": "16 frames (~4 s window)",
        "notes": "V-JEPA-2.1 patch 16",
        "quotes": [Q("Pretraining clips are sixteen frames sampled at four frames per second, a temporal window of approximately four seconds, cropped at high resolution", "omniras_arxiv_pdf")],
    },
    "embedding_dim": {"value": "1408 (OmniRAS 1B, ViT-g) / 1664 (OmniRAS 2B, ViT-G)", "basis": "encoder roster table token width D",
                      "quotes": [Q("OmniRAS 1B Meta ViT-g 1B 1408 83.0 M (8.3%) OmniRAS 2B Meta ViT-G 2B 1664", "omniras_arxiv_pdf")]},
    "params": {"value": "~1B (ViT-g, 40 blocks) and ~2B (ViT-G, 48 blocks), including predictor",
               "quotes": [Q("with widths 1,408 and 1,664 and depths 40 and 48, respectively. Including the predictor, these configurations contain approximately 1B and 2", "omniras_arxiv_pdf")]},
    "flops_per_input_if_documented": {"value": None, "statement": "not documented in the saved sources (searched 'FLOP' in arXiv PDF)", "quotes": []},
    "eligibility": elig(
        C("UNKNOWN", "Checkpoints only via an access-request Google Form; no public file listing (manual request = UNKNOWN)."),
        C("UNKNOWN", "Checkpoint licence not yet defined ('will be released under their own terms'); repo CC BY 4.0 explicitly excludes checkpoints."),
        C("PASS", "Self-supervised V-JEPA-2.1 continued pretraining on a ~2,650 h surgical video corpus (with Kinetics-400 rehearsal)."),
        C("PASS", "Paper section 'Pretraining data' names the sources (one private robotic collection)."),
        "Very new (2026-08-31); re-check for a public release."),
}
