"""NVIDIA Cosmos-Tokenizer-Surg = Telesurgery Neural Tokenizer v1.0 (frame autoencoder distilled from Wan2.1)."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "Cosmos-Tokenizer-Surg (Telesurgery Neural Tokenizer; frame autoencoder distilled from Wan2.1, trained on in-house laparoscopic video)",
    "aliases": ["nvidia/Cosmos-Tokenizer-Surg", "Telesurgery Neural Tokenizer v1.0"],
    "group": "surgical video tokenizer / autoencoder (generative-model component)",
    "paper": {"title": "no paper; NVIDIA model card", "year": "2025-2026", "venue": "Hugging Face model card (created 2025-12-10, lastModified 2026-03-18)", "arxiv": None,
              "quotes": [Q("# Telesurgery Neural Tokenizer v1.0 Overview", "cosmostoksurg_hf_readme")]},
    "version": {
        "value": "card title v1.0; 'Model Version(s): v0.1'; HF sha 97757e20556e8905dd3ddb0734d7c987bf4cc9e8; ONNX encoders/decoders per resolution (540p/720p/1080p *_cs_discrete8_wan_patch2.onnx) + best_model.pth",
        "basis": "model card + HF API listing (the card states both v1.0 in its title and v0.1 under Model Version(s))",
        "quotes": [Q("## Model Version(s): v0.1", "cosmostoksurg_hf_readme"),
                   Q('"sha":"97757e20556e8905dd3ddb0734d7c987bf4cc9e8","lastModified":"2026-03-18T08:22:10.000Z"', "cosmostoksurg_hf_api")],
    },
    "weights_location": {
        "url": "https://huggingface.co/nvidia/Cosmos-Tokenizer-Surg (e.g. 720p/encoder_720p_cs_discrete8_wan_patch2.onnx, best_model.pth)",
        "exists": "YES - HF API lists encoder/decoder/quantizer ONNX files for 540p/720p/1080p and best_model.pth (50,493,554 B); gated=false (nothing downloaded)",
        "access": "public, not gated",
        "verification": "HF API listing ?blobs=true, 2026-10-02",
        "quotes": [Q('"rfilename":"720p/encoder_720p_cs_discrete8_wan_patch2.onnx","blobId":"b1cb140cc9c0822f7df671b998dea129c8bdb1d0","size":23172295', "cosmostoksurg_hf_api"),
                   Q('"rfilename":"best_model.pth","blobId":"b51c7df4c9442e4ed48b26d6d1d5e8e0451c12e5","size":50493554', "cosmostoksurg_hf_api"),
                   Q('"gated":false', "cosmostoksurg_hf_api")],
    },
    "licence": {
        "code": "sample scripts in the HF repo; covered by the same NVIDIA Open Model License statement (no separate code licence found)",
        "weights": "NVIDIA Open Model License",
        "url": "https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/",
        "code_and_weights_differ": "no separate code licence stated",
        "quotes": [Q("Governing Terms: Use of this model system is governed by the [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).", "cosmostoksurg_hf_readme"),
                   Q("Models are commercially usable.", "nvidia_open_model_license"),
                   Q("_This model is available for commercial use._", "cosmostoksurg_hf_readme")],
    },
    "domain": {
        "value": "laparoscopic surgery video frames (in-house); per-frame neural codec/tokenizer for telesurgery streaming, distilled from the general-domain Wan2.1 VAE",
        "quotes": [Q("Telesurgery Neural Tokenizer processes surgical scenario inputs by tokenizing frames using a distilled frame autoencoder, optimized for low-latency applications like telesurgery video streaming.", "cosmostoksurg_hf_readme"),
                   Q("**This model was distilled from Wan2.1.**", "cosmostoksurg_hf_readme")],
    },
    "pretraining_data_quote": {
        "summary": "In-house surgical data (laparoscopic surgeries): 5,765 five-minute video items for training (1,224 test, 1,220 evaluation); no institution, procedure list or source named. Teacher: Wan2.1 (general-domain VAE).",
        "datasets": ["NVIDIA in-house laparoscopic surgery videos (unnamed source)", "Distillation teacher: Wan2.1 VAE"],
        "quotes": [Q("**Link:** In-house surgical data (laparoscopic surgeries)", "cosmostoksurg_hf_readme"),
                   Q("Training set consists of 5765 (5-minute) video items for laparoscopic surgeries. **Modality**: Video (Image sequences). **Content Nature**: In-house surgical data.", "cosmostoksurg_hf_readme")],
    },
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "Training data are 'In-house surgical data (laparoscopic surgeries)' with no institution, procedure or recording-period information; whether laparoscopic appendectomy recordings from the Appendix300 centres are among them cannot be excluded. Distillation teacher Wan2.1 was trained on general web-scale video (not enumerated).",
        [Q("Training set consists of 5765 (5-minute) video items for laparoscopic surgeries.", "cosmostoksurg_hf_readme")]),
    "input": {
        "frame_size": "single RGB frames at 536x960, 720x1280 or 1080x1920 (range [-1, 1])",
        "frame_rate_or_sampling": "frame-wise (2D convolutions; no temporal compression)",
        "clip_length_frames": "1 (per-frame tokenizer)",
        "notes": "ONNX/TensorRT runtime; one encoder per resolution.",
        "quotes": [Q("**Other Properties Related to Input:** Image Resolution: 536x960, 720x1280 or 1080x1920; Image Range: [-1, 1]", "cosmostoksurg_hf_readme"),
                   Q("based on Wan2.1 with 2D Convolutions", "cosmostoksurg_hf_readme")],
    },
    "embedding_dim": {
        "value": "2 x (H/8) x (W/8) per frame (2 latent channels at 8x spatial downsampling; discrete-8 quantizer per file names)",
        "basis": "model card output description",
        "quotes": [Q("**Other Properties Related to Output:** Embeddings format: 2x(H/8)x(W/8) (With `H` and `W` being Height and Width of the original image).", "cosmostoksurg_hf_readme")],
    },
    "params": {"value": "12.6M", "quotes": [Q("**Number of model parameters:** 12.6M", "cosmostoksurg_hf_readme")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'latency', 'ms' in the model card"),
    "eligibility": elig(
        C("PASS", "HF API lists ONNX encoder/decoder files and best_model.pth; gated=false."),
        C("PASS", "NVIDIA Open Model License (commercial use allowed; research covered)."),
        C("PASS", "Trained on frames of in-house laparoscopic surgery videos (frame autoencoder distilled from Wan2.1)."),
        C("FAIL", "Pretraining data described only generically as 'In-house surgical data (laparoscopic surgeries)' - no named dataset, institution or source."),
        "Frame-level codec (2-channel 1/8 latent), not a semantic encoder; fails documented-data criterion."),
}
