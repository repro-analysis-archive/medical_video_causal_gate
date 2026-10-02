"""Cosmos-H-Dreams (real-time causal distilled action-conditioned surgical world model)."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "Cosmos-H-Dreams (real-time self-forcing distilled action-conditioned surgical world model; dVRK tabletop suturing checkpoint)",
    "aliases": ["NVIDIA Cosmos-H-Dreams", "FlashDreams (inference library)"],
    "group": "surgical video world / generative model",
    "paper": {
        "title": "NVIDIA Cosmos-H-Dreams: Real-Time Generative Physics Simulation for Surgical Robotics",
        "year": 2026, "venue": "arXiv preprint (v1 25 Aug 2026, v2 27 Aug 2026)", "arxiv": "2608.24199",
        "quotes": [Q("Title: NVIDIA Cosmos-H-Dreams: Real-Time Generative Physics Simulation for Surgical Robotics", "cosmoshdreams_arxiv_abs"),
                   Q("[Submitted on 25 Aug 2026 ( v1 ), last revised 27 Aug 2026 (this version, v2)]", "cosmoshdreams_arxiv_abs")],
    },
    "version": {
        "value": "v1.0 real-time self-forcing distilled student (dVRK tabletop suturing); checkpoint checkpoints/model_ema_bf16_jhutabletop_288x512_h73.pt; HF sha 2314ef820863b93f74ab8852de93b1e6f491d75c; released 2026-07-23",
        "basis": "model card 'Model Version(s)' and 'Release Date'; HF API listing",
        "quotes": [Q("**v1.0 Real-time self-forcing distilled student (dVRK tabletop suturing).**", "cosmoshdreams_hf_readme"),
                   Q("- **Huggingface:** 07/23/2026 via https://huggingface.co/nvidia/Cosmos-H-Dreams", "cosmoshdreams_hf_readme"),
                   Q('"sha":"2314ef820863b93f74ab8852de93b1e6f491d75c"', "cosmoshdreams_hf_api")],
    },
    "weights_location": {
        "url": "https://huggingface.co/nvidia/Cosmos-H-Dreams/blob/main/checkpoints/model_ema_bf16_jhutabletop_288x512_h73.pt",
        "exists": "YES - HF API lists checkpoints/model_ema_bf16_jhutabletop_288x512_h73.pt (4,258,611,590 B) + cr1_empty_string_text_embeddings.pt; gated=false (nothing downloaded)",
        "access": "public, not gated",
        "verification": "HF API listing ?blobs=true, 2026-10-02",
        "quotes": [Q('"rfilename":"checkpoints/model_ema_bf16_jhutabletop_288x512_h73.pt","blobId":"7db70c30ff9c1f82202a26bb0ad0477cccc46a50","size":4258611590', "cosmoshdreams_hf_api"),
                   Q('"gated":false', "cosmoshdreams_hf_api")],
    },
    "licence": {
        "code": "runtime library on GitHub isaac-for-healthcare/Cosmos-H-Dreams (code licence not checked)",
        "weights": "NVIDIA Open Model License Agreement",
        "url": "https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/ ; https://huggingface.co/nvidia/Cosmos-H-Dreams/blob/main/LICENSE",
        "code_and_weights_differ": "unknown (code licence not checked)",
        "quotes": [Q("Use of this model is governed by the [NVIDIA Open Model License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).", "cosmoshdreams_hf_readme"),
                   Q("NVIDIA hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, revocable (as stated in Section 2.1) license to publicly perform, publicly display, reproduce, use, create derivative works of, make, have made, sell, offer for sale, distribute (through multiple tiers of distribution) and import the Model.", "cosmoshdreams_hf_license"),
                   Q("This model is ready for commercial or non-commercial use.", "cosmoshdreams_hf_readme")],
    },
    "domain": {
        "value": "surgical robotics video: teacher warm-started from Cosmos-H-Surgical-Simulator (Open-H incl. clinical procedures), released student post-trained on dVRK tabletop (phantom) suturing; base Cosmos-Predict2.5-2B (general domain)",
        "quotes": [Q("Cosmos-H-Dreams is a real-time, action-conditioned generative surgical world model", "cosmoshdreams_hf_readme"),
                   Q("The released checkpoint specializes the model to da Vinci Research Kit (dVRK) tabletop suturing.", "cosmoshdreams_hf_readme")],
    },
    "pretraining_data_quote": {
        "summary": "Pre-training (via the Simulator warm start): Open-H Embodiment (~26,500 demonstrations, 32 datasets, 9 embodiments, 10+ institutions). Post-training: dVRK tabletop suturing dataset from Cosmos-Surg-dVRK (JHU SutureBot suturing/knot tying + failure/OOD episodes, ~1M frames at 10 Hz). Base Cosmos-Predict2.5-2B.",
        "datasets": ["Open-H Embodiment (pre-training via Cosmos-H-Surgical-Simulator)", "dVRK tabletop suturing (JHU SutureBot + failure/OOD episodes; Cosmos-Surg-dVRK)", "Base: Cosmos-Predict2.5-2B"],
        "quotes": [Q("Dataset: Open-H-Embodiment community-generated dataset (pre-training) and the dVRK tabletop suturing dataset (post-training).", "cosmoshdreams_hf_readme"),
                   Q("the dVRK suturing dataset introduced by Cosmos-Surg-dVRK: JHU SutureBot suturing and knot-tying data together with converted failure and out-of-distribution episodes", "cosmoshdreams_hf_readme"),
                   Q("The released model is derived from the public NVIDIA Cosmos-Predict2.5-2B world foundation model for physical AI, and its teacher is warm-started from Cosmos-H-Surgical-Simulator (the Open-H 44D action-conditioned checkpoint).", "cosmoshdreams_hf_readme")],
    },
    "appendix300_check": A300(
        "UNKNOWN",
        "Open-H contributors include 'TUD' (TUNDRA: TUD & NCT Dresden in vivo porcine robot-assistant data); the documented data list does not mention DS203/Appendix300.",
        False,
        "Post-training data are JHU dVRK tabletop suturing (no patient video). Inherits the Simulator's Open-H pre-training (closed list of groups, no appendectomy; CMR Versius clinical recordings from unnamed hospitals) and the general-domain Cosmos-Predict2.5-2B pretraining video (web-scale/proprietary, not enumerated) - the latter cannot be excluded.",
        [Q("Balgrist, CMR, CUHK, GBU (China), HKBU, Hamlyn, ImFusion, JHU, Leeds, MBZUAI (UAE), Moon Surgical, NVIDIA, Northwell, Obuda, PolyU (HK), Qilu Hospital of Shandong University, Rob Surgical, Sanoscience, SDSC, Semaphor, Stanford, TUD, TUM", "openh_hf_dataset_readme")]),
    "input": {
        "frame_size": "288 x 512 (H x W), 16:9; frames auto-resized",
        "frame_rate_or_sampling": "effective 10 Hz for dVRK (30 Hz capture, stride 3)",
        "clip_length_frames": "autoregressive outer blocks of 12 generated frames (each consumes 12 44-D action steps); teacher horizons 13 -> 25 -> 49 -> 73 frames",
        "notes": "Inputs: one context frame + streaming 44-D action vectors; causal student with streaming KV cache, 2-4 denoising steps per latent frame.",
        "quotes": [Q("**Recommended resolution:** The model operates at 288 × 512 (height × width); a 16:9 aspect ratio is recommended.", "cosmoshdreams_hf_readme"),
                   Q("**Control rate:** Effective 10 Hz for dVRK (30 Hz capture, stride 3).", "cosmoshdreams_hf_readme"),
                   Q("The student rolls forward in outer blocks of 12 generated frames, denoising each latent frame in a small number of steps (2–4).", "cosmoshdreams_hf_readme")],
    },
    "embedding_dim": {
        "value": "Wan2.1 video tokenizer latent: 16 channels at 8x spatial / 4x temporal compression; DiT hidden width 2048 (28 blocks, 16 heads)",
        "basis": "model card architecture paragraph (base Cosmos-Predict2.5-2B-Video2World which this model extends)",
        "quotes": [Q("Cosmos-H-Dreams extends Cosmos-Predict2.5-2B-Video2World, a 2B-parameter diffusion transformer for video generation in latent space (Wan2.1 video tokenizer, spatial compression 8×, temporal compression 4×, 16 latent channels; hidden width 2048, 28 blocks, 16 heads", "cosmoshdreams_hf_readme")],
    },
    "params": {"value": "~2B (Cosmos-Predict2.5-2B backbone + two small action MLPs); checkpoint 4.26 GB bf16",
               "quotes": [Q("a 2B-parameter diffusion transformer for video generation in latent space", "cosmoshdreams_hf_readme"),
                          Q("It incorporates two small MLPs that condition the model on kinematic actions", "cosmoshdreams_hf_readme")]},
    "flops_per_input_if_documented": {
        "value": None,
        "statement": "FLOPs not documented; throughput documented: ~160 frames per second interactive generation on one NVIDIA RTX PRO 6000 (vs ~10 fps for standard Simulator inference).",
        "quotes": [Q("from the roughly ten-frames-per-second regime of standard Cosmos-H-Surgical-Simulator inference to interactive operation (~160 frames per second) on a single NVIDIA RTX PRO 6000", "cosmoshdreams_hf_blog")],
    },
    "eligibility": elig(
        C("PASS", "HF API lists the student checkpoint; gated=false."),
        C("PASS", "NVIDIA Open Model License grants use and derivative works (commercial allowed)."),
        C("PASS", "Surgical-robot video world model (Open-H warm start incl. clinical procedures; final post-training on dVRK tabletop suturing phantom video); general-domain Cosmos-Predict2.5-2B initialisation."),
        C("PASS", "Card names Open-H (pre-training) and the JHU SutureBot dVRK tabletop dataset (post-training). Caveat: base Cosmos-Predict2.5 data not enumerated."),
        "Released checkpoint is specialised to tabletop suturing and is action-conditioned; poor fit for laparoscopic appendectomy video representation."),
}
