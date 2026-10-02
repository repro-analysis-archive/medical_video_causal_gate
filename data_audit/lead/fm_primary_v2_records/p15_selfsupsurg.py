"""SelfSupSurg (CAMMA; Ramesh et al., MedIA 2023) (new entry, fork A)."""
from ._common import A300, C, NOT_MENTIONED, Q, elig

REC = {
    "name": "SelfSupSurg (CAMMA: MoCo v2 / SimCLR / SwAV / DINO ResNet-50 pretrained on Cholec80)",
    "aliases": ["SelfSupSurg", "Dissecting self-supervised learning methods for surgical computer vision"],
    "paper": {
        "title": "Dissecting self-supervised learning methods for surgical computer vision",
        "year": 2023, "venue": "Medical Image Analysis 2023 (doi 10.1016/j.media.2023.102844); arXiv 2207.00449v3", "arxiv": "2207.00449",
        "quotes": [Q("This article has been accepted for publication in Medical Image Analysis. DOI: 10.1016/", "selfsupsurg_arxiv_pdf"),
                   Q("[v3] Wed, 31 May 2023 09:08:11 UTC", "selfsupsurg_arxiv_abs")],
    },
    "version": {
        "value": "model_final_checkpoint_{moco_v2,simclr,swav,dino}_surg.torch (VISSL checkpoints; configs series_01 h001-h004)",
        "basis": "README 'Model Weights for the pre-training experiments' table",
        "quotes": [Q("| [DINO](configs/config/hparams/cholec80/pre_training/cholec_to_cholec/series_01/h004.yaml)| [download](https://s3.unistra.fr/camma_public/github/selfsupsurg/models/model_final_checkpoint_dino_surg.torch) |", "selfsupsurg_github_readme"),
                   Q("| [MoCo V2](configs/config/hparams/cholec80/pre_training/cholec_to_cholec/series_01/h001.yaml)| [download](https://s3.unistra.fr/camma_public/github/selfsupsurg/models/model_final_checkpoint_moco_v2_surg.torch) |", "selfsupsurg_github_readme")],
    },
    "weights_location": {
        "url": "https://s3.unistra.fr/camma_public/github/selfsupsurg/models/ (model_final_checkpoint_{moco_v2,simclr,swav,dino}_surg.torch)",
        "exists": "YES - HEAD: MoCo v2 checkpoint 1,426,020,674 B and DINO checkpoint 352,288,944 B, HTTP 200 binary/octet-stream (not downloaded; SimCLR/SwAV links not checked)",
        "access": "public S3 URLs, no login",
        "verification": "HEAD requests, 2026-10-02",
        "quotes": [Q('"content_length": "1426020674"', "selfsupsurg_weights_moco_check"),
                   Q('"content_length": "352288944"', "selfsupsurg_weights_dino_check")],
    },
    "licence": {
        "code": "CC BY-NC-SA 4.0 (code, models and datasets; non-commercial scientific research)",
        "weights": "CC BY-NC-SA 4.0",
        "url": "https://github.com/CAMMA-public/SelfSupSurg#license",
        "code_and_weights_differ": "no",
        "quotes": [Q("This code, models, and datasets are available for non-commercial scientific research purposes as defined in the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).", "selfsupsurg_github_readme")],
    },
    "domain": {
        "value": "laparoscopic cholecystectomy video frames (Cholec80); image (frame-level) ResNet-50 SSL encoders",
        "quotes": [Q("Self-supervised weights trained on cholec80 dataset using four state-of-the-art SSL methods (MOCO V2, SimCLR, SwAV, and DINO).", "selfsupsurg_github_readme"),
                   Q("This dataset contains 80 videos of complete laparoscopic cholecystectomy procedures, recorded at 25 frames per second", "selfsupsurg_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "Cholec80 training pool (40 videos) sampled at 5 fps (recommended setting; config train list 5fps_100_0.pickle); ResNet-50 initialised from ImageNet fully-supervised weights (resnet50-19c8e357.pth).",
        "datasets": ["Cholec80 (40 training videos; laparoscopic cholecystectomy)", "Initialisation: ImageNet supervised ResNet-50"],
        "quotes": [Q("In the hyperparameter study, we perform SSL pretraining on the entire pool of 40 training videos", "selfsupsurg_arxiv_pdf"),
                   Q("DATA_PATHS: [./datasets/cholec80/labels/train/5fps_100_0.pickle]", "selfsupsurg_cfg_dino"),
                   Q("Recommended 2 On On Off 256 300 5 Imagenet fully supervised", "selfsupsurg_arxiv_pdf"),
                   Q('PARAMS_FILE: "./checkpoints/defaults/resnet_50/resnet50-19c8e357.pth"', "selfsupsurg_cfg_dino")],
    },
    "appendix300_check": A300(
        "NO", NOT_MENTIONED, False,
        "Closed list: Cholec80 training videos only (laparoscopic cholecystectomy) + ImageNet initialisation. No appendectomy, no YouTube, no "
        "undisclosed in-house data.",
        [Q("This dataset contains 80 videos of complete laparoscopic cholecystectomy procedures", "selfsupsurg_arxiv_pdf")]),
    "input": {
        "frame_size": "pretraining: resize to 252x448 then 224x224 multi-crops; evaluation resize 224x399",
        "frame_rate_or_sampling": "Cholec80 frames at 5 fps for pretraining (videos recorded at 25 fps)",
        "clip_length_frames": "1 (single-frame CNN encoder)",
        "notes": "VISSL configs (h004 = DINO)",
        "quotes": [Q("- name: Resize size: [252, 448] - name: ImgPilToMultiCrop total_num_crops: 2 size_crops: [224, 224]", "selfsupsurg_cfg_dino"),
                   Q("- name: Resize size: [224, 399]", "selfsupsurg_cfg_dino"),
                   Q("DATA_PATHS: [./datasets/cholec80/labels/train/5fps_100_0.pickle]", "selfsupsurg_cfg_dino")],
    },
    "embedding_dim": {"value": 2048, "basis": "ResNet-50 trunk feature vector",
                      "quotes": [Q("replaced by a linear head that maps the feature vector (2048) to the number of outputs", "selfsupsurg_arxiv_pdf")]},
    "params": {"value": "not stated (ResNet-50 trunk ~25.6M standard figure, unverified)",
               "quotes": [Q("We use ResNet-50 (He et al., 2016) as the base encoder architecture", "selfsupsurg_arxiv_pdf")]},
    "flops_per_input_if_documented": {"value": None, "statement": "not documented in the saved sources (searched 'FLOP' in arXiv PDF and README)", "quotes": []},
    "eligibility": elig(
        C("PASS", "Public S3 checkpoint URLs resolve (HEAD 200, sizes recorded); not downloaded."),
        C("PASS", "CC BY-NC-SA 4.0, non-commercial scientific research."),
        C("PASS", "Self-supervised pretraining on frames (5 fps) of Cholec80 laparoscopic surgery videos."),
        C("PASS", "Cholec80 (40-video training pool) + ImageNet initialisation named."),
        "Small single-procedure corpus; frame-level ResNet-50; predates the 'foundation model' label but is a released surgical-video SSL encoder."),
}
