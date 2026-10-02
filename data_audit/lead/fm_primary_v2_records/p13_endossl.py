"""EndoSSL (Hirsch et al., MICCAI 2023; Verily) (new entry, fork A)."""
from ._common import A300, C, Q, elig

REC = {
    "name": "EndoSSL (MSN ViT-S/B/L pretrained on private laparoscopy / colonoscopy video frames)",
    "aliases": ["EndoSSL", "Self-Supervised Learning for Endoscopic Video Analysis (Hirsch et al.)"],
    "paper": {
        "title": "Self-Supervised Learning for Endoscopic Video Analysis",
        "year": 2023, "venue": "MICCAI 2023 (arXiv 2308.12394)", "arxiv": "2308.12394",
        "quotes": [Q("Code and models for MICCAI23 paper: \"Self-Supervised Learning for Endoscopy Video Analysis\".", "endossl_github_readme"),
                   Q("Title: Self-Supervised Learning for Endoscopic Video Analysis", "endossl_arxiv_abs")],
    },
    "version": {
        "value": "6 released checkpoints (Google Drive folders, dated 2023/07/16): vits/vitb/vitl_lapro_private (Private Laparoscopy) and ViT-S/B/L Private Colonoscopy; each folder holds jax_checkpoint + saved_model_inference (TensorFlow SavedModel). No GitHub releases.",
        "basis": "README model table; Drive folder pages (titles and listing; nothing downloaded)",
        "quotes": [Q("| ViT-L | Private Laparoscopy | Cholec80 F1: 84.0 | [Link](https://drive.google.com/drive/folders/11TdNyl4HGvpoi6Ro0zZ28L1qxY4IAJPb?usp=drive_link) |", "endossl_github_readme"),
                   Q("jax_checkpoint 2023/07/16 —   Download saved_model_inference 2023/07/16", "endossl_weights_lap_vitl_folder"),
                   Q("default='/root/vits_lapro_private/saved_model_inference',", "endossl_github_inference")],
    },
    "weights_location": {
        "url": "https://drive.google.com/drive/folders/11TdNyl4HGvpoi6Ro0zZ28L1qxY4IAJPb (ViT-L laparoscopy); ViT-B lap https://drive.google.com/drive/folders/1zcLKhE7H50GIDeb53chLrE5SUBtBooAR ; others in README",
        "exists": "YES - public Drive folder pages resolve (HTTP 200) titled vitl_lapro_private / vitb_lapro_private and list jax_checkpoint + saved_model_inference (not downloaded). A PyTorch conversion of the teacher used by SurgVISTA is also on Google Drive.",
        "access": "public link, no login or request",
        "verification": "GET of Drive folder pages (HTML title/listing only), 2026-10-02",
        "quotes": [Q('"html_title": "vitl_lapro_private - Google', "endossl_weights_lap_vitl_gdrive"),
                   Q('"html_title": "vitb_lapro_private - Google', "endossl_weights_lap_vitb_gdrive"),
                   Q("We release a series of models pre-trained with our method over a large corpus of endoscopic videos:", "endossl_github_readme")],
    },
    "licence": {
        "code": "BSD-3-Clause (Copyright (c) 2023, Verily Life Sciences)",
        "weights": "README: 'Our work is licensed under BSD 3-Clause license' (covers the released models; no separate weights licence)",
        "url": "https://github.com/RoyHirsch/endossl/blob/main/LICENSE",
        "code_and_weights_differ": "no separate weights licence stated",
        "quotes": [Q("Our work is licensed under BSD 3-Clause license, as found in the [LICENSE](LICENSE) file.", "endossl_github_readme"),
                   Q("BSD 3-Clause License Copyright (c) 2023, Verily Life Sciences", "endossl_github_license")],
    },
    "domain": {
        "value": "laparoscopic surgery video frames (1 fps) and colonoscopy polyp crops from colonoscopy videos; image (frame-level) MSN encoders",
        "quotes": [Q("Each video recording was sampled at a rate of 1 frame per second (FPS), resulting in an extensive dataset containing 23.3 million images.", "endossl_arxiv_pdf"),
                   Q("For each frame, we cropped the bounding boxes to generate individual images of the polyps.", "endossl_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "Private Laparoscopy: 7,877 adult laparoscopic videos from eight (unnamed) medical centres in Israel, 23.3M frames at 1 fps (cholecystectomy 35%, appendectomy 20%, herniorrhaphy 12%, colectomy 6%, bariatric 5%, other 21%). Private Colonoscopy: 13,979 videos from six centres (2019-2022) -> 2.2M polyp crops. Ablations also report ImageNet-1k initialisation.",
        "datasets": ["Private Laparoscopy (8 medical centres in Israel, unnamed)", "Private Colonoscopy (6 medical centres, unnamed)"],
        "quotes": [Q("The dataset consists of 7,877 videos recorded at eight different medical centers in Israel. The dataset predominantly consists of the following procedures: cholecystectomy (35%), appendectomy (20%), herniorrhaphy (12%), colectomy (6%), and bariatric surgery (5%).", "endossl_arxiv_pdf"),
                   Q("We have curated a dataset comprising 13,979 colonoscopy videos of patients aged 18 years or older. These videos were recorded during standard colonoscopy procedures performed at six different medical centers between the years 2019 and 2022.", "endossl_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "NO",
        "The dataset consists of 7,877 videos recorded at eight different medical centers in Israel.", True,
        "Private in-house data (centres unnamed) that include ~20% appendectomies, but the paper states all laparoscopy videos were recorded at "
        "medical centres in Israel, which excludes the German Appendix300 centres; the colonoscopy set is not surgical. The answer rests on this "
        "geographic statement (no named centre list, data not inspectable). No YouTube data.",
        [Q("cholecystectomy (35%), appendectomy (20%)", "endossl_arxiv_pdf")]),
    "input": {
        "frame_size": "224x224 (inference script default resize)",
        "frame_rate_or_sampling": "laparoscopy videos sampled at 1 fps for pretraining",
        "clip_length_frames": "1 (single-image ViT encoder)",
        "notes": "TensorFlow SavedModel / JAX checkpoints; inference returns the hidden representation (output index 1)",
        "quotes": [Q("def get_image(image_path, size=224):", "endossl_github_inference"),
                   Q("Each video recording was sampled at a rate of 1 frame per second (FPS)", "endossl_arxiv_pdf"),
                   Q("return self.backbone(x)[1]", "endossl_github_inference")],
    },
    "embedding_dim": {"value": "384 / 768 / 1024 for ViT-S / ViT-B / ViT-L (standard ViT widths; not stated in paper or README)",
                      "basis": "architecture names only",
                      "quotes": [Q("As our image encoders we train Vision Transformer (ViT [16]) of different sizes, abbreviated as ViT-S/B/L", "endossl_arxiv_pdf")]},
    "params": {"value": "not stated (standard ViT-S/B/L ~22M / 86M / 304M, outside figures, unverified)",
               "quotes": [Q("As our image encoders we train Vision Transformer (ViT [16]) of different sizes, abbreviated as ViT-S/B/L", "endossl_arxiv_pdf")]},
    "flops_per_input_if_documented": {"value": None, "statement": "not documented in the saved sources (searched 'FLOP' in arXiv PDF and README)", "quotes": []},
    "eligibility": elig(
        C("PASS", "Six public Google Drive folders (README table); the ViT-L/ViT-B laparoscopy folders resolve and list jax_checkpoint and saved_model_inference (not downloaded)."),
        C("PASS", "BSD-3-Clause (Verily Life Sciences) for 'our work' incl. released models."),
        C("PASS", "MSN self-supervised pretraining on frames sampled at 1 fps from laparoscopic surgery videos (and colonoscopy-video polyp crops)."),
        C("PASS", "Paper describes the private pretraining datasets (counts, procedure mix, number and country of centres, years); centres are not named."),
        "Documented-data PASS is borderline: private data are described in detail but centres are unnamed. TensorFlow/JAX formats."),
}
