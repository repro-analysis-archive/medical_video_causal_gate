"""Endora: Video Generation Models as Endoscopy Simulators (MICCAI 2024)."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "Endora (endoscopy video generation; latent video diffusion transformer with DINO prior)",
    "aliases": ["EnDoraIMG-XL/2"],
    "group": "endoscopy video generative model",
    "paper": {"title": "Endora: Video Generation Models as Endoscopy Simulators", "year": 2024, "venue": "MICCAI 2024", "arxiv": "2403.11050",
              "quotes": [Q("# *Endora*: Video Generation Models as Endoscopy Simulators (MICCAI 2024)", "endora_github_readme")]},
    "version": {
        "value": "per-dataset checkpoints (Colonoscopic, Kvasir-Capsule, CholecT45) from the README links; model config EnDoraIMG-XL/2; no release tags",
        "basis": "README sampling scripts (col/kva/cho) + configs/col/col_train.yaml",
        "quotes": [Q("model: EnDoraIMG-XL/2", "endora_config_col"),
                   Q("bash sample/col.sh bash sample/kva.sh bash sample/cho.sh", "endora_github_readme")],
    },
    "weights_location": {
        "url": "https://stuxmueducn-my.sharepoint.com/:f:/g/personal/chenxinli_stu_xmu_edu_cn/EnlDBG3dzwlPnSjqYdpp4l8BfettnJoeX1XVSX_BIVNyHQ?e=W6kXM9 ; https://1drv.ms/f/c/4ba61f71217230ec/EuwwciFxH6YggEtgIwAAAAABvyM2h6CSA-7549Xqkh4lNQ?e=nbOeeL",
        "exists": "NO (at check 2026-10-02) - both README weight links (SharePoint folder and OneDrive folder) return a SharePoint error page 'Sorry, you cannot access this document. Please contact the person who shared it with you.' No Hugging Face copy found (HF model search 'Endora').",
        "access": "share links not accessible",
        "verification": "GET of both share pages (HTML text only), 2026-10-02; same method resolved GSViT's OneDrive link",
        "quotes": [Q("1. Download the pre-trained weights from [here](https://stuxmueducn-my.sharepoint.com/:f:/g/personal/chenxinli_stu_xmu_edu_cn/EnlDBG3dzwlPnSjqYdpp4l8BfettnJoeX1XVSX_BIVNyHQ?e=W6kXM9)", "endora_github_readme"),
                   Q("|Endora (Ours)| 460.7 | 13.41 | 3.90| [Link](https://1drv.ms/f/c/4ba61f71217230ec/EuwwciFxH6YggEtgIwAAAAABvyM2h6CSA-7549Xqkh4lNQ?e=nbOeeL)|", "endora_github_readme"),
                   Q("Sorry, you cannot access this document. Please contact the person who shared it with you.", "endora_weights_sharepoint_page"),
                   Q("Sorry, you cannot access this document. Please contact the person who shared it with you.", "endora_weights_onedrive_page")],
    },
    "licence": {
        "code": "none found (no LICENSE file: raw LICENSE returns 404; README has no licence statement)",
        "weights": "none stated",
        "url": "https://github.com/CUHK-AIM-Group/Endora",
        "code_and_weights_differ": "no licence for either",
        "quotes": [Q("404: Not Found", "endora_github_license")],
    },
    "domain": {
        "value": "endoscopy video generation (colonoscopy, capsule endoscopy, laparoscopic cholecystectomy); trained separately per dataset",
        "quotes": [Q("We conduct comprehensive experiments on three public endoscopy video datasets: Colonoscopic [40], Kvasir-Capsule [7], CholecTriplet [43].", "endora_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "Colonoscopic, Kvasir-Capsule, CholecTriplet (CholecT45) - one model per dataset; DINO ViT-B/8 (ImageNet self-supervised) as feature prior; a 'pretrained variational autoencoder' whose training data are not named.",
        "datasets": ["Colonoscopic", "Kvasir-Capsule", "CholecTriplet / CholecT45", "Prior: DINO ViT-B/8", "Frozen pretrained VAE (source not named)"],
        "quotes": [Q("We conduct comprehensive experiments on three public endoscopy video datasets: Colonoscopic [40], Kvasir-Capsule [7], CholecTriplet [43].", "endora_arxiv_pdf"),
                   Q("in our implementation we use ViT-B/8 during training Endora.", "endora_github_readme"),
                   Q("the training process involves using a pretrained variational autoencoder [64,28] to encode video inputs into a latent space.", "endora_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "The diffusion model is trained on three named public endoscopy datasets (colonoscopy, capsule endoscopy, cholecystectomy) - none is Appendix300. Not excludable only for the frozen 'pretrained variational autoencoder', whose source and training data are not named; DINO prior is ImageNet.",
        [Q("the training process involves using a pretrained variational autoencoder [64,28] to encode video inputs into a latent space.", "endora_arxiv_pdf")]),
    "input": {
        "frame_size": "128x128",
        "frame_rate_or_sampling": "frames sampled at a fixed interval (config frame_interval: 3)",
        "clip_length_frames": "16 frames (+8 images for joint image training)",
        "notes": "Unconditional generation per dataset.",
        "quotes": [Q("we extract 16-frame video clips from these datasets using a specific sampling interval, with each frame resized to 128×128 resolution for training.", "endora_arxiv_pdf"),
                   Q("num_frames: 16 image_size: 128", "endora_config_col"), Q("frame_interval: 3", "endora_config_col")],
    },
    "embedding_dim": {
        "value": "not stated (latent clip V in R^(F x H x W x C) from the unnamed VAE; transformer width of the XL/2 config not stated in saved sources)",
        "basis": "paper method section",
        "quotes": [Q("given a video clip in the latent space, denoted as V ∈ RF ×H×W ×C", "endora_arxiv_pdf")],
    },
    "params": {"value": "not stated in paper/README (config EnDoraIMG-XL/2; MedSora paper compares against 'Endora (base size)' but gives values only in a figure)", "quotes": [Q("model: EnDoraIMG-XL/2", "endora_config_col")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'GFLOP' in paper PDF and README"),
    "eligibility": elig(
        C("FAIL", "Both official weight links return 'Sorry, you cannot access this document.'; no other official copy found."),
        C("UNKNOWN", "No LICENSE file (404) and no licence statement in README."),
        C("PASS", "Video diffusion model trained on endoscopy video datasets."),
        C("PASS", "Paper names the three training datasets (VAE source unnamed)."),
        "Per-dataset generative models at 128x128; not usable (weights inaccessible)."),
}

REC["weights_location"]["quotes"].append(Q("search='Endora' status=200 n=1 ids=['EndorAI/MD-1']", "hf_model_search_generative"))
