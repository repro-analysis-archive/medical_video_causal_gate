"""NVIDIA Qwen2.5-VL-7B-Surg-CholecT50 - task fine-tune of Qwen2.5-VL-7B on CholecT50 frames."""
from ._common import A300, C, NOFLOPS, NOT_MENTIONED, Q, elig

REC = {
    "name": "Qwen2.5-VL-7B-Surg-CholecT50 (NVIDIA)",
    "aliases": ["Qwen2.5-VL-7B-Surg"],
    "paper": {"title": "no paper (HF model card only)", "year": 2025, "venue": "Hugging Face model card (nvidia)", "arxiv": None,
              "quotes": [Q("Qwen2.5-VL-7B-Surg-CholecT50 was developed by NVIDIA for research in surgical workflow analyses and fine-grained action recognition.", "nvqwensurg_hf_readme")]},
    "version": {"value": "v1.0 (Finetuned on CholecT50); HF repo sha c1a01db98c72f4fca5ec671405325c4c841dcafd",
                "basis": "model card; HF API listing",
                "quotes": [Q("v1.0 (Finetuned on CholecT50)", "nvqwensurg_hf_readme"), Q('"sha":"c1a01db98c72f4fca5ec671405325c4c841dcafd"', "nvqwensurg_hf_api_blobs")]},
    "weights_location": {"url": "https://huggingface.co/nvidia/Qwen2.5-VL-7B-Surg-CholecT50 (4 safetensors shards)",
                         "exists": "YES - HF API lists model-0000N-of-00004.safetensors; gated=false (not downloaded)",
                         "access": "public, no gating", "verification": "HF API ?blobs=true listing, 2026-10-02",
                         "quotes": [Q('"rfilename":"model-00001-of-00004.safetensors","blobId":"9dc44f5314c928f5b2ffccabd3e4222f6da375e5","size":4968243304', "nvqwensurg_hf_api_blobs"),
                                    Q('"gated":false', "nvqwensurg_hf_api_blobs")]},
    "licence": {"code": "n/a", "weights": "NVIDIA License NSCLv1 (License.docx): non-commercial use = research or evaluation only",
                "url": "https://huggingface.co/nvidia/Qwen2.5-VL-7B-Surg-CholecT50/resolve/main/License.docx", "code_and_weights_differ": "n/a",
                "quotes": [Q("license_name: nsclv1", "nvqwensurg_hf_readme"),
                           Q("3.3 Use Limitation. The Work and any derivative works thereof only may be used or intended for use non-commercially.", "nvqwensurg_license_docx"),
                           Q("As used herein, “non-commercially” means for research or evaluation purposes only.", "nvqwensurg_license_docx")]},
    "domain": {"value": "task-specific supervised fine-tune (surgical action-triplet recognition) of the general VLM Qwen2.5-VL-7B on CholecT50 laparoscopic frames (1 fps)",
               "quotes": [Q("Qwen2.5-VL-7B-Surg-CholecT50 is a multimodal large language model fine-tuned on the CholecT50 dataset of laparoscopic cholecystectomy procedures to recognize and describe surgical actions, instruments, and targets in endoscopic video frames.", "nvqwensurg_hf_readme")]},
    "pretraining_data_quote": {"summary": "Fine-tuning data: CholecT50 (~50 laparoscopic cholecystectomies, ~100K frames at 1 fps); base Qwen2.5-VL-7B (Alibaba; general web-scale data)",
                               "datasets": ["CholecT50", "Base: Qwen2.5-VL-7B"],
                               "quotes": [Q("~50 laparoscopic cholecystectomy procedures; frames extracted at 1 fps (~100K training frames)", "nvqwensurg_hf_readme"),
                                          Q("base_model: Qwen/Qwen2.5-VL-7B", "nvqwensurg_hf_readme")]},
    "appendix300_check": A300(
        "NO", NOT_MENTIONED, False,
        "Surgical data = CholecT50 only (named public cholecystectomy dataset, Strasbourg); not appendectomy. The Qwen2.5-VL-7B base model "
        "was pretrained by Alibaba on undisclosed web-scale image/video/text data, which cannot be itemised (generic, not surgical-specific).",
        [Q("[CholecT50](https://github.com/CAMMA-public/cholect50)", "nvqwensurg_hf_readme")]),
    "input": {"frame_size": "recommended 480p or higher; minimal resizing (e.g. 224x224) if required (Qwen2.5-VL dynamic resolution)",
              "frame_rate_or_sampling": "single frames extracted at 1 fps", "clip_length_frames": "1 (image input)",
              "notes": "text output (no embedding head)",
              "quotes": [Q("Image: Two-Dimensional (2D) laparoscopic image frames (extracted at 1 fps)", "nvqwensurg_hf_readme"),
                         Q("Recommended resolution: 480p or higher. Minimal resizing (e.g., 224×224) if required by the model’s vision encoder.", "nvqwensurg_hf_readme")]},
    "embedding_dim": {"value": None, "basis": "not stated (VLM, text output)", "quotes": []},
    "params": {"value": "~7.0e9", "quotes": [Q("** Number of model parameters: ~7.0×10^9**", "nvqwensurg_hf_readme")]},
    "flops_per_input_if_documented": NOFLOPS("model card"),
    "eligibility": elig(
        C("PASS", "Weights publicly listed on HF (gated=false)."),
        C("PASS", "NSCLv1: non-commercial research/evaluation use permitted."),
        C("FAIL", "Task-specific supervised fine-tune (CholecT50 triplets) of a general VLM; not surgical/endoscopic pretraining."),
        C("PASS", "Fine-tuning dataset named (CholecT50); base model named."),
        "Listed for completeness (released surgical VLM)."),
}


# --- lead harmonisation (2026-10-02) ---
assert REC["appendix300_check"]["answer"] == "NO"
REC["appendix300_check"]["answer"] = "UNKNOWN"
REC["appendix300_check"]["cannot_exclude_note"] += " " + "LEAD HARMONISATION 2026-10-02: answer changed NO -> UNKNOWN under the uniform lineage rule (training data of the released weights plus their initialisation / base / frozen-backbone weights; distillation teachers are recorded but do not decide): the Qwen2.5-VL-7B base model's undisclosed web-scale pretraining data cannot be excluded."
REC["appendix300_check"]["quotes"].append(Q('base_model: Qwen/Qwen2.5-VL-7B base_model_relation: finetune', 'nvqwensurg_hf_readme'))
REC.setdefault("changes_vs_previous", []).append("Appendix300 NO -> UNKNOWN (lead harmonisation of the lineage rule across all entries): the Qwen2.5-VL-7B base model's undisclosed web-scale pretraining data cannot be excluded.")
