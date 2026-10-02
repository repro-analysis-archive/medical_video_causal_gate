"""KVLR: From Articulated Kinematics to Routed Visual Control for Action-Conditioned Surgical Video Generation (NeurIPS 2026)."""
from ._common import A300, C, Q, elig

REC = {
    "name": "KVLR / KVLR-fast (kinematics-to-visual action-conditioned surgical video generation; fine-tuned on KASA from SAR-RARP50)",
    "aliases": ["KVLR", "KVLR-fast", "KASA benchmark"],
    "group": "surgical video world / generative model",
    "paper": {"title": "From Articulated Kinematics to Routed Visual Control for Action-Conditioned Surgical Video Generation", "year": 2026, "venue": "NeurIPS 2026", "arxiv": "2605.08712",
              "quotes": [Q("KVLR [NeurIPS 2026] From Articulated Kinematics to Routed Visual Control for Action-Conditioned Surgical Video Generation", "kvlr_github_page")]},
    "version": {
        "value": "Google Drive folder 'KVAR_CHECKPOINT' (kvlr/merged_model.safetensors, kvlr_fast/merged_model.safetensors, stage1_i2v, stage2_i2v per README layout); GitHub repo with 2 commits, no tags",
        "basis": "README checkpoint layout + Drive folder title",
        "quotes": [Q("kvlr/merged_model.safetensors kvlr_fast/merged_model.safetensors", "kvlr_github_readme_master"),
                   Q('"html_title": "KVAR_CHECKPOINT - Google', "kvlr_weights_gdrive_check")],
    },
    "weights_location": {
        "url": "https://drive.google.com/drive/folders/1KRLFxWvjmfTTtImigWUMKXWAU6mhX1o5?usp=sharing",
        "exists": "YES (folder level) - the public Google Drive folder resolves (HTTP 200, title 'KVAR_CHECKPOINT'); individual files not enumerated (folder listing is JS-rendered); nothing downloaded",
        "access": "public link",
        "verification": "GET of Drive folder page (HTML title only), 2026-10-02",
        "quotes": [Q("- Checkpoints: https://drive.google.com/drive/folders/1KRLFxWvjmfTTtImigWUMKXWAU6mhX1o5?usp=sharing", "kvlr_github_readme_master"),
                   Q('"status": 200', "kvlr_weights_gdrive_check")],
    },
    "licence": {
        "code": "Apache-2.0 (repo LICENSE)", "weights": "not separately stated (repository-level Apache-2.0)",
        "url": "https://github.com/Arlo0o/KVLR/blob/master/LICENSE",
        "code_and_weights_differ": "no separate weights licence stated",
        "quotes": [Q("Apache License Version 2.0, January 2004", "kvlr_github_license_master"), Q("README Apache-2.0 license", "kvlr_github_page")],
    },
    "domain": {
        "value": "robotic surgical video generation conditioned on instrument kinematics; fine-tuned on real robot-assisted radical prostatectomy video (SAR-RARP50) from a pretrained general-domain DiT video generator",
        "quotes": [Q("We curate KASA from the SAR-RARP dataset [68], collecting 1,047 surgical scenes with 105,175 frames.", "kvlr_arxiv_pdf"),
                   Q("This preserves 5 the pretrained generative prior at initialization while allowing the model to progressively learn action conditioning.", "kvlr_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "Fine-tuning: KASA (1,047 scenes, 105,175 frames curated from SAR-RARP50; needle grasping / puncture / knotting). Base generator: pretrained DiT video generator not named in the saved sources (README base components: hunyuan_vae.safetensors, google/t5-v1_1-xxl, openai/clip-vit-large-patch14 - an Open-Sora-2.0-style stack, inference only); its pretraining data are not documented here.",
        "datasets": ["KASA (from SAR-RARP50)", "Base video generator (unnamed; general domain)"],
        "quotes": [Q("We curate KASA from the SAR-RARP dataset [68], collecting 1,047 surgical scenes with 105,175 frames.", "kvlr_arxiv_pdf"),
                   Q("hunyuan_vae.safetensors google/t5-v1_1-xxl/ openai/clip-vit-large-patch14/", "kvlr_github_readme_master")],
    },
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "Surgical fine-tuning data are SAR-RARP50 prostatectomy only (no appendectomy). The pretrained base video generator is not named and its (general web-scale) pretraining data are not documented - cannot be excluded.",
        [Q("We curate KASA from the SAR-RARP dataset [68]", "kvlr_arxiv_pdf")]),
    "input": {
        "frame_size": "evaluated at 288x512 and 576x1024; data preparation at '768px'",
        "frame_rate_or_sampling": "KASA videos downsampled to 30 FPS",
        "clip_length_frames": "17-frame clips in the efficiency evaluation; KASA sequences 55-235 frames",
        "notes": "image-to-video with kinematic action conditioning (KVA-Field)",
        "quotes": [Q("Videos are downsampled to 30 FPS, and each sequence contains 55-235 frames.", "kvlr_arxiv_pdf"),
                   Q("Tab. 3 reports latency and FLOPs on H20 GPUs with 17-frame clips.", "kvlr_arxiv_pdf"),
                   Q("--resolution 768px \\", "kvlr_github_readme_master")],
    },
    "embedding_dim": {"value": "not stated (HunyuanVideo VAE latent per README layout; channel count not given in saved sources)", "basis": "searched paper/README for latent channels", "quotes": []},
    "params": {"value": "~12.06B total (ablation table: 11.00B base -> 12.06B with KVA-Field + routing)",
               "quotes": [Q("Total Params CD ↓ TI ↑ FID ↓ PSNR ↑ Latency (s) ↓ 11.00B 12.06B 12.06B 12.05B 12.06B", "kvlr_arxiv_pdf")]},
    "flops_per_input_if_documented": {
        "value": "per 17-frame clip (Tab. 3, H20 GPU; pdftotext column order, read as latency/FLOPs per resolution): KVLR 288x512 = 4.64 s / 6.94 PF; 576x1024 = 23.39 s / 24.77 PF; KVLR-fast 288x512 = 0.37 s / 0.55 PF; 576x1024 = 1.88 s / 1.98 PF (row/column assignment reconstructed from flattened PDF text - verify against the PDF table)",
        "statement": "documented in Table 3",
        "quotes": [Q("KVLR (Ours) KVLR-fast (Ours) 4.64 0.37 6.94 0.55 23.39 1.88 24.77 1.98", "kvlr_arxiv_pdf"),
                   Q("Method 288×512 576×1024 Latency (s)↓ FLOPs↓ (PF/clip) Latency (s)↓ FLOPs↓ (PF/clip)", "kvlr_arxiv_pdf")],
    },
    "eligibility": elig(
        C("PASS", "Official public Google Drive checkpoint folder resolves (folder-level check; file list not enumerated)."),
        C("PASS", "Repository LICENSE is Apache-2.0 (no separate weights licence)."),
        C("PASS", "Fine-tuned on real robotic surgery video (KASA from SAR-RARP50) from a general-domain video generator."),
        C("PASS", "Paper names KASA / SAR-RARP50 as training data. Caveat: base generator and its pretraining data not named."),
        "Action-conditioned (needs instrument kinematics); ~12B parameters."),
}
