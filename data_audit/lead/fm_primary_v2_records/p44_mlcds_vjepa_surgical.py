"""Finetuned V-JEPA ViT-L on surgical video (ML-CDS 2025, Digital Surgery Lab Basel; arXiv 2509.06831)."""
from ._common import A300, C, NOFLOPS, NOT_MENTIONED, Q, elig

REC = {
    "name": "Finetuned V-JEPA ViT-L (ML-CDS-2025 / multimods3, Basel; jepa-12h)",
    "aliases": ["ML-CDS-2025", "multimods3", "jepa-12h.pth.tar"],
    "paper": {
        "title": "Leveraging generic foundation models for multimodal surgical data analysis",
        "year": 2025, "venue": "arXiv preprint 2509.06831v1 (MICCAI 2025 ML-CDS workshop repository name)", "arxiv": "2509.06831",
        "quotes": [Q("# Leveraging generic foundation models for multimodal surgical data analysis", "mlcds_hf_readme"),
                   Q("(or arXiv:2509.06831v1 [cs.CV] for this version)", "mlcds_arxiv_abs")],
    },
    "version": {
        "value": "jepa-12h.pth.tar (12 h wall-clock / 7 epochs of continued V-JEPA training); HF repo sha eb803900299171b5a45a4b2caf0b349530e80c9a",
        "basis": "HF API listing; paper training description",
        "quotes": [Q('"sha":"eb803900299171b5a45a4b2caf0b349530e80c9a"', "mlcds_hf_api_blobs"),
                   Q("Due to resource restrictions, training was limited to 12 hours wall-clock time, which amounted to 7 completed epochs of continued training on the finetuning data.", "mlcds_arxiv_pdf")],
    },
    "weights_location": {
        "url": "https://huggingface.co/DigitalSurgeryLab-Basel/ML-CDS-2025 (jepa-12h.pth.tar, 5,143,102,207 B)",
        "exists": "YES - HF API lists jepa-12h.pth.tar; gated=false (not downloaded)",
        "access": "public, no gating",
        "verification": "HF API ?blobs=true listing, 2026-10-02",
        "quotes": [Q('"rfilename":"jepa-12h.pth.tar","blobId":"5a6e468d2107d9b8f49a17820a6314ea4c2ac498","size":5143102207', "mlcds_hf_api_blobs"),
                   Q('"gated":false', "mlcds_hf_api_blobs")],
    },
    "licence": {
        "code": "CC BY-NC 4.0 (GitHub README / LICENSE.txt; inherits V-JEPA code licence)",
        "weights": "CC BY-NC-SA 4.0 (HF model card)",
        "url": "https://huggingface.co/DigitalSurgeryLab-Basel/ML-CDS-2025 ; https://github.com/DigitalSurgeryLab-Basel/ML-CDS-2025",
        "code_and_weights_differ": "yes - code CC BY-NC 4.0, weights CC BY-NC-SA 4.0 (both non-commercial)",
        "quotes": [Q("As we utilized public datasets for finetuning, we distribute our *model weights* under the same license: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).", "mlcds_hf_readme"),
                   Q("we distribute our *code* under the same license: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).", "mlcds_github_readme"),
                   Q("Attribution-NonCommercial 4.0 International", "mlcds_github_license")],
    },
    "domain": {
        "value": "laparoscopic surgical video (continued self-supervised V-JEPA training of Meta's general-video V-JEPA ViT-L on unlabeled endoscopic surgery videos)",
        "quotes": [Q("We finetuned *V-JEPA ViT-L* on unlabeled endoscopic surgical videos, as described in the paper.", "mlcds_hf_readme"),
                   Q("By finetuned V-JEPA, we refer to the weights that we gained by continued self-supervised JEPA training of pretrained V-JEPA on the finetuning data", "mlcds_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "Continued SSL on parts of HeiCo (Heidelberg colorectal), all Cholec80 (80 videos, 51:15 h) and MultiBypass140 (70 Bern + 70 Strasbourg videos); initial weights = Meta V-JEPA v1 ViT-L (VideoMix2M, ~2M everyday-activity videos)",
        "datasets": ["HeiCo (part)", "Cholec80", "MultiBypass140 (Inselspital Bern, University Hospital Strasbourg)", "Init: V-JEPA v1 ViT-L (Bardes et al.)"],
        "quotes": [Q("In addition to parts of the HeiCo data (see above), we use all videos from the Cholec80 [12] dataset (80 laparoscopic videos of cholecystectomy surgery, 51:15 h) and MultiBypass140 [6] dataset (laparoscopic videos of gastric bypass surgery; 70 videos, 87:56 h, from Inselspital Bern; 70 videos, 129:09 h, from University Hospital Strasbourg) for domain-specific finetuning of V-JEPA", "mlcds_arxiv_pdf"),
                   Q("V-JEPA’s published weights have been trained on 2 million videos of primarily human everyday activities without special focus on the medical field.", "mlcds_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "NO", NOT_MENTIONED, False,
        "Closed list of named public surgical datasets (HeiCo, Cholec80, MultiBypass140; centres Heidelberg, Strasbourg, Bern); none is "
        "Appendix300 or a Dresden-area recording. The in-house liver-surgery videos (Basel) are used only for downstream heads, not for the "
        "released encoder finetuning. Base V-JEPA v1 data = VideoMix2M (Kinetics/SSv2/HowTo100M, everyday-activity benchmarks, YouTube-derived but fixed lists).",
        [Q("Videos from the following datasets were used for finetuning:", "mlcds_hf_readme")]),
    "input": {
        "frame_size": "not stated in the paper (follows the V-JEPA ViT-L/16 code base)",
        "frame_rate_or_sampling": "not stated for training; evaluation clips sampled densely at one-second intervals",
        "clip_length_frames": "not stated in the paper (V-JEPA code-base default)",
        "notes": "video clip encoder (ViT with temporal extension); training schedule adopted from the V-JEPA code base",
        "quotes": [Q("For evaluation, we densely sampled clips at one-second intervals from all videos in the test split.", "mlcds_arxiv_pdf"),
                   Q("adopting the training schedule from the V-JEPA code base", "mlcds_arxiv_pdf")],
    },
    "embedding_dim": {"value": None, "basis": "not stated (ViT-L; standard width 1024 is an outside fact)", "quotes": []},
    "params": {"value": "not stated (V-JEPA ViT-L; checkpoint 5.1 GB incl. training state)",
               "quotes": [Q("For all experiments, we use the V-JEPA ViT-L model size.", "mlcds_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP' in arXiv PDF and READMEs"),
    "eligibility": elig(
        C("PASS", "jepa-12h.pth.tar publicly listed on HF (gated=false)."),
        C("PASS", "Weights CC BY-NC-SA 4.0 (non-commercial research use)."),
        C("PASS", "Continued self-supervised V-JEPA training on laparoscopic surgical videos."),
        C("PASS", "Finetuning datasets named with counts; base model and its data named."),
        "Short continued pretraining (7 epochs); V-JEPA v1 ViT-L video encoder."),
}


# --- lead harmonisation (2026-10-02) ---
assert REC["appendix300_check"]["answer"] == "NO"
REC["appendix300_check"]["answer"] = "UNKNOWN"
REC["appendix300_check"]["cannot_exclude_note"] += " " + 'LEAD HARMONISATION 2026-10-02: answer changed NO -> UNKNOWN under the uniform lineage rule (training data of the released weights plus their initialisation / base / frozen-backbone weights; distillation teachers are recorded but do not decide): the V-JEPA initialisation was pretrained on VideoMix2M, which includes HowTo100M (keyword-searched YouTube instructional videos, open-ended web content), so source recordings cannot be excluded by documentation.'
REC["appendix300_check"]["quotes"].append(Q('Specifically, we combine the videos from HowTo100M (HT) (Miech et al., 2019), Kinetics-400/600/700 (K710) (Kay et al., 2017), and Something-Something-v2 (SSv2) (Goyal et al., 2017)', 'vjepa_arxiv_pdf'))
REC.setdefault("changes_vs_previous", []).append('Appendix300 NO -> UNKNOWN (lead harmonisation of the lineage rule across all entries): the V-JEPA initialisation was pretrained on VideoMix2M, which includes HowTo100M (keyword-searched YouTube instructional videos, open-ended web content), so source recordings cannot be excluded by documentation.')
