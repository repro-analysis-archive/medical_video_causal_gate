"""GastroNet-5M pretrained models (TU/e + Amsterdam UMC; MedIA 2024 and Gastroenterology 2025/2026)."""
from ._common import A300, C, NOFLOPS, NOT_MENTIONED, Q, elig

REC = {
    "name": "GastroNet-5M pretrained models (DINOv2 ViT-B; DINO/MoCov2/SimCLRv2 ResNet50 & ViT-S)",
    "aliases": ["GastroNetDinov2", "GastroNet-5M_Pretrained_Weights"],
    "paper": {
        "title": "GastroNet-5M: A Multicenter Dataset for Developing Foundation Models in Gastrointestinal Endoscopy (Gastroenterology 2026;170(1):174-187); Foundation models in gastrointestinal endoscopic AI: Impact of architecture, pre-training approach and data efficiency (MedIA 2024;98:103298)",
        "year": "2024-2026", "venue": "Gastroenterology / Medical Image Analysis (both closed access per Europe PMC)", "arxiv": None,
        "quotes": [Q("GastroNet-5M: A Multicenter Dataset for Developing Foundation Models in Gastrointestinal Endoscopy.", "gastronet_pubmed_efetch"),
                   Q("Foundation models in gastrointestinal endoscopic AI: Impact of architecture, pre-training approach and data efficiency.", "gastronet_pubmed_efetch"),
                   Q('"isOpenAccess":"N"', "gastronet_pmc_search")],
    },
    "version": {
        "value": "DINOv2 ViT-B checkpoint 'dinov2.pth' (HF card BONS-AI-TUE-AMC/GastroNetDinov2, card sha b003452f9f51c825bfae4ebe3ed01fa2e538bf37); MedIA-2024 ResNet50/ViT-S weights formerly on HF tgwboers/GastroNet-5M_Pretrained_Weights (repo now README-only, sha 6a8554d1e517344887bd10017cfd936b85f4d481)",
        "basis": "HF API listings (metadata only) and model cards",
        "quotes": [Q("Download the file (e.g., `dinov2.pth`) and place it locally or on your device.", "gastronetdinov2_hf_readme"),
                   Q('"sha":"b003452f9f51c825bfae4ebe3ed01fa2e538bf37"', "gastronetdinov2_hf_api_blobs"),
                   Q('"sha":"6a8554d1e517344887bd10017cfd936b85f4d481"', "gastronet_hf_api_blobs")],
    },
    "weights_location": {
        "url": "https://cortex.thetavision.nl/dataset-provider/listing/2/ (linked from https://huggingface.co/BONS-AI-TUE-AMC/GastroNetDinov2 and https://huggingface.co/tgwboers/GastroNet-5M_Pretrained_Weights)",
        "exists": "UNKNOWN - both HF repos list only .gitattributes and README.md (no weight files); weights are said to be hosted on the Theta Vision Cortex data-provider platform, whose listing page is a JavaScript app (HTTP 200, no readable content without executing it); whether download needs an account/agreement could not be verified without creating an account",
        "access": "external platform (terms not verifiable without account); earlier HF revision of the tgwboers repo carried a cc-by-nc-nd-4.0 card",
        "verification": "HF API ?blobs=true listings; GET of the Cortex listing page (586-byte JS shell)",
        "quotes": [Q('"siblings":[{"rfilename":".gitattributes","blobId":"a6344aac8c09253b3b630fb776ae94478aa0275b","size":1519},{"rfilename":"README.md","blobId":"38e6e0c9df1ec487bcee3eda8a5f4b7cdb33d02a","size":2765}]', "gastronetdinov2_hf_api_blobs"),
                   Q("The pretrained model weights are hosted externally and can be downloaded here:", "gastronetdinov2_hf_readme"),
                   Q("📢 **Update:** Model weights are now available via [Theta Vision Cortex](https://cortex.thetavision.nl/dataset-provider/listing/2/).", "gastronet_hf_readme"),
                   Q('"status": 200', "gastronet_cortex_check")],
    },
    "licence": {
        "code": "n/a (usage snippet in card only)",
        "weights": "CC BY-NC 4.0 (BONS-AI-TUE-AMC/GastroNetDinov2 card); the earlier tgwboers card declared CC BY-NC-ND 4.0",
        "url": "https://huggingface.co/BONS-AI-TUE-AMC/GastroNetDinov2",
        "code_and_weights_differ": "n/a",
        "quotes": [Q("license: cc-by-nc-4.0", "gastronetdinov2_hf_readme"), Q("license: cc-by-nc-nd-4.0", "gastronet_hf_readme_old")],
    },
    "domain": {
        "value": "GI endoscopy still images ('general endoscopic images captured' during ~500k procedures); not documented as video frames in the accessible text",
        "quotes": [Q("GastroNet-5M consists of anonymized general endoscopic images captured in 8 Dutch hospitals between 2012 and 2020.", "gastronet_pubmed_efetch")],
    },
    "pretraining_data_quote": {
        "summary": "GastroNet-5M: 4,820,653 (Gastroenterology) / 5,014,174 (MedIA) anonymised GI endoscopic images of ~500,000 procedures from 8 Dutch hospitals, 2012-2020; DINOv2 (ViT-B) and DINO/MoCov2/SimCLRv2 (ResNet50, ViT-S) self-supervised pretraining",
        "datasets": ["GastroNet-5M (8 Dutch hospitals, BONS-AI consortium)"],
        "quotes": [Q("In this study, we present GastroNet-5M, a dataset comprising 4,820,653 endoscopic images of ∼500,000 procedures.", "gastronet_pubmed_efetch"),
                   Q("GastroNet-5M consists of anonymized general endoscopic images captured in 8 Dutch hospitals between 2012 and 2020.", "gastronet_pubmed_efetch"),
                   Q("we present a dataset comprising of 5,014,174 gastrointestinal endoscopic images from eight different medical centers (GastroNet-5M), and exploit self-supervised learning with SimCLRv2, MoCov2 and DINO", "gastronet_pubmed_efetch"),
                   Q("The model was pretrained on the **GastroNet‑5M** dataset using dinov2.", "gastronetdinov2_hf_readme")],
    },
    "appendix300_check": A300(
        "NO", NOT_MENTIONED, False,
        "In-house multicentre data, hospitals not itemised in the accessible abstract, but documented as GI endoscopy images from 8 Dutch "
        "hospitals (2012-2020); German laparoscopic appendectomy recordings are outside the documented scope. No YouTube/web data mentioned. "
        "Initialisation (if any) not documented in the accessible text.",
        [Q("anonymized general endoscopic images captured in 8 Dutch hospitals between 2012 and 2020", "gastronet_pubmed_efetch")]),
    "input": {
        "frame_size": "336x336 for the DINOv2 ViT-B/14 checkpoint (card usage code); MedIA-2024 models: not stated in accessible text",
        "frame_rate_or_sampling": "single still images; no temporal sampling",
        "clip_length_frames": "1 (image model)",
        "notes": "the card loads the checkpoint into timm vit_base_patch14_dinov2 with num_classes=0 (teacher weights)",
        "quotes": [Q('model = timm.create_model("timm/vit_base_patch14_dinov2.lvd142m", pretrained=False, num_classes=0, img_size=336, )', "gastronetdinov2_hf_readme")],
    },
    "embedding_dim": {"value": None, "basis": "not stated in the card or accessible abstracts (ViT-Base architecture named; standard width 768 is an outside fact)",
                      "quotes": [Q("This repository contains a Vision Transformer (ViT-Base) model", "gastronetdinov2_hf_readme")]},
    "params": {"value": "not stated (ViT-Base; ResNet50 / ViT-S in MedIA 2024)",
               "quotes": [Q("On the ResNet50 and Vision-Transformer-small architectures", "gastronet_pubmed_efetch")]},
    "flops_per_input_if_documented": NOFLOPS("model cards and PubMed abstracts (full texts closed access)"),
    "eligibility": elig(
        C("UNKNOWN", "Weights removed from HF; now on the external Theta Vision Cortex platform whose access conditions cannot be verified without an account."),
        C("PASS", "CC BY-NC 4.0 (non-commercial) on the GastroNetDinov2 card."),
        C("UNKNOWN", "GI endoscopy images, but described as captured endoscopic images, not as frames sampled from video."),
        C("PASS", "Pretraining dataset named (GastroNet-5M; 8 Dutch hospitals, counts, years)."),
        "Image (still) FM; full texts not accessible here."),
}
