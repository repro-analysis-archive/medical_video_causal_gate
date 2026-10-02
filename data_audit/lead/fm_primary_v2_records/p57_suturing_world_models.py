"""Towards Suturing World Models (Suturing-LTX-T2V / Suturing-LTX-I2V LoRA on LTX-Video)."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "Suturing World Models (Suturing-LTX-T2V / Suturing-LTX-I2V: LoRA fine-tunes of LTX-Video on laparoscopic suturing exercise video)",
    "aliases": ["Towards Suturing World Models", "mehmetkeremturkcan/Suturing-LTX-I2V", "mehmetkeremturkcan/Suturing-LTX-T2V"],
    "group": "surgical video generative model",
    "paper": {"title": "Towards Suturing World Models: Learning Predictive Models for Robotic Surgical Tasks", "year": 2025, "venue": "arXiv preprint (Columbia University / Northwell Health)", "arxiv": "2503.12531",
              "quotes": [Q("Towards Suturing World Models: Learning Predictive Models for Robotic Surgical Tasks", "suturingwm_arxiv_pdf")]},
    "version": {
        "value": "HF Suturing-LTX-I2V sha 8c8a187fc1f67edb907d4d2898c1c30113734e46 and Suturing-LTX-T2V sha ca1f05187c7a3af405823f0a22a73649226abb26 (both 2025-03-11); LoRA on LTX-Video 0.9.1 (diffusers); HunyuanVideo variants described in the paper are not in the HF collection",
        "basis": "HF API listings + collection + card usage example",
        "quotes": [Q('"sha":"8c8a187fc1f67edb907d4d2898c1c30113734e46","lastModified":"2025-03-11T17:04:37.000Z"', "suturingltx_i2v_hf_api"),
                   Q('"sha":"ca1f05187c7a3af405823f0a22a73649226abb26","lastModified":"2025-03-11T17:04:26.000Z"', "suturingltx_t2v_hf_api"),
                   Q('"a-r-r-o-w/LTX-Video-0.9.1-diffusers"', "suturingltx_i2v_hf_readme"),
                   Q('"id":"mehmetkeremturkcan/Suturing-LTX-T2V"', "suturingwm_hf_collection")],
    },
    "weights_location": {
        "url": "https://huggingface.co/mehmetkeremturkcan/Suturing-LTX-I2V ; https://huggingface.co/mehmetkeremturkcan/Suturing-LTX-T2V (pytorch_lora_weights.safetensors; requires base LTX-Video weights)",
        "exists": "YES - HF API lists pytorch_lora_weights.safetensors (I2V 781,528,232 B; T2V 939,583,904 B); gated=false (nothing downloaded). Linked from the authors' project page collection.",
        "access": "public, not gated (LoRA adapter only; base LTX-Video 0.9.1 needed)",
        "verification": "HF API listings ?blobs=true + collection API, 2026-10-02",
        "quotes": [Q('"rfilename":"pytorch_lora_weights.safetensors","blobId":"ec44aec49296f3da6bf35c0e559e4236aba427d7","size":781528232', "suturingltx_i2v_hf_api"),
                   Q('"rfilename":"pytorch_lora_weights.safetensors","blobId":"2f61f724d1e1a2b06c8fa594c19aa6ffed138ce9","size":939583904', "suturingltx_t2v_hf_api"),
                   Q('"gated":false', "suturingltx_i2v_hf_api")],
    },
    "licence": {
        "code": "not stated", "weights": "not stated on either HF card (no license metadata); base LTX-Video has its own licence (not checked here)",
        "url": "https://huggingface.co/mehmetkeremturkcan/Suturing-LTX-I2V",
        "code_and_weights_differ": "no licence stated",
        "quotes": [Q("base_model: - Lightricks/LTX-Video library_name: diffusers", "suturingltx_i2v_hf_readme")],
    },
    "domain": {
        "value": "laparoscopic / robotic suturing exercise (simulation) video; LoRA fine-tune of general-domain LTX-Video",
        "quotes": [Q("This repository hosts the fine-tuned LTX-Video image-to-video (i2v) diffusion model specialized for generating realistic robotic surgical suturing videos", "suturingltx_i2v_hf_readme"),
                   Q("- **Data Source**: Annotated laparoscopic surgery exercise videos (∼2,000 clips)", "suturingltx_i2v_hf_readme")],
    },
    "pretraining_data_quote": {
        "summary": "~2,000 annotated clips 'extracted from simulation videos' (laparoscopic surgery exercise videos); source/institution of the recordings not named. Base LTX-Video (general domain).",
        "datasets": ["~2K annotated suturing clips from simulation / exercise videos (unnamed source)", "Base: Lightricks LTX-Video"],
        "quotes": [Q("Annotating a dataset of ∼ 2K clips extracted from simulation videos", "suturingwm_arxiv_pdf"),
                   Q("- **Data Source**: Annotated laparoscopic surgery exercise videos (∼2,000 clips)", "suturingltx_i2v_hf_readme")],
    },
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "The fine-tuning clips are suturing exercise/simulation videos (not patient appendectomy) but their source is not named; the base LTX-Video was pretrained on general web-scale video not enumerated here - cannot be excluded.",
        [Q("Annotating a dataset of ∼ 2K clips extracted from simulation videos", "suturingwm_arxiv_pdf")]),
    "input": {
        "frame_size": "768x512 (adjustable)",
        "frame_rate_or_sampling": "not stated",
        "clip_length_frames": "49 frames per generated video (adjustable)",
        "notes": "I2V: one input image + text prompt (prefix 'suturingmodel, '); T2V: text only.",
        "quotes": [Q("- **Resolution**: 768×512 pixels (Adjustable)", "suturingltx_i2v_hf_readme"), Q("- **Frame Length**: 49 frames per generated video (Adjustable)", "suturingltx_i2v_hf_readme")],
    },
    "embedding_dim": {"value": "not stated in saved sources (base LTX-Video latent space; not documented on the cards)", "basis": "searched cards and paper for latent/channel/dimension", "quotes": []},
    "params": {"value": "base LTX-Video ~2B (paper); LoRA adapter files 0.78-0.94 GB",
               "quotes": [Q("specifically LTXVideo (2B parameters) and HunyuanVideo (13B parameters)", "suturingwm_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'latency' in paper and cards"),
    "eligibility": elig(
        C("PASS", "HF API lists LoRA weight files; gated=false (base LTX-Video required)."),
        C("UNKNOWN", "No licence stated on the HF cards or project page; base LTX-Video licence terms would also apply."),
        C("PASS", "LoRA-fine-tuned on laparoscopic suturing exercise/simulation video (surgical task video, not patient surgery)."),
        C("FAIL", "Training data described only as ~2K clips 'extracted from simulation videos' / 'laparoscopic surgery exercise videos' - no named dataset or source."),
        "Narrow suturing-only generative LoRA."),
}
