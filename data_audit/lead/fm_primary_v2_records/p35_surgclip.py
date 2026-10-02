"""SurgCLIP-beta (SurgLaVi, MedIA 2026; Intuitive Surgical) - CLIP-style surgical video-text model."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "SurgCLIP-β (SurgLaVi)",
    "aliases": ["SurgCLIP", "SurgCLIP-B", "surgclip_beta.pth"],
    "paper": {
        "title": "SurgLaVi: Large-Scale Hierarchical Dataset for Surgical Vision-Language Representation Learning",
        "year": 2026, "venue": "Medical Image Analysis 2026, 103982 (arXiv 2509.10555)", "arxiv": "2509.10555",
        "quotes": [Q("### Large-Scale Hierarchical Dataset for Surgical Vision-Language Representation Learning [MedIA 2026]", "surglavi_github2_readme")],
    },
    "version": {
        "value": "SurgCLIP-β checkpoint surgclip_beta.pth (HF aleperez24/SurgCLIP, repo sha b7a205316c50517dcf84ee50d05b90a3253982b8; loaded as 'SurgCLIP-B' by pip package surgclip 0.1.0). The full SurgCLIP (trained with the partly private SurgLaVi) is not released.",
        "basis": "HF API listing; README; pyproject",
        "quotes": [Q('"rfilename":"surgclip_beta.pth","blobId":"78603a90c27b446f078800e52909387baaa614b2","size":922408512', "surgclip_hf_api_blobs"),
                   Q('"sha":"b7a205316c50517dcf84ee50d05b90a3253982b8"', "surgclip_hf_api_blobs"),
                   Q("**SurgCLIP-β** is the open-source version trained on SurgLaVi-β.", "surglavi_github2_readme"),
                   Q('version = "0.1.0"', "surgclip_pyproject")],
    },
    "weights_location": {
        "url": "https://huggingface.co/aleperez24/SurgCLIP (surgclip_beta.pth, 922,408,512 B)",
        "exists": "YES - HF API lists surgclip_beta.pth; gated=false, private=false (not downloaded)",
        "access": "public, no gating",
        "verification": "HF API ?blobs=true listing (metadata only), 2026-10-02",
        "quotes": [Q('"gated":false', "surgclip_hf_api_blobs"), Q('"private":false', "surgclip_hf_api_blobs"),
                   Q("[![Hugging Face Model](https://img.shields.io/badge/%F0%9F%A4%97%20Model-SurgCLIP-blue)](https://huggingface.co/aleperez24/SurgCLIP)", "surglavi_github2_readme")],
    },
    "licence": {
        "code": "MIT (pip package surgclip, pyproject.toml / PyPI metadata)",
        "weights": "not stated: the HF weights repo has no model card or licence tag; the GitHub README licence section covers the dataset (CC BY-NC-SA 4.0)",
        "url": "https://github.com/aperezr20/SurgLaVi#license ; https://pypi.org/project/surgclip",
        "code_and_weights_differ": "weights licence undeclared",
        "quotes": [Q('license = {text = "MIT"}', "surgclip_pyproject"),
                   Q("This dataset is released under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).", "surglavi_github2_readme"),
                   Q("Entry not found", "surgclip_hf_readme")],
    },
    "domain": {
        "value": "surgical video (laparoscopic / robotic / open, YouTube educational operative recordings) with narration-derived captions",
        "quotes": [Q("These videos originate from surgeons and institutions that publicly share operative recordings for educational purposes.", "surglavi_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "SurgLaVi-β: 2,464 videos / 465 h / 112,757 clip-caption pairs from the YouTube scrapes of LEMON (3,110 videos) and GenSurgery/GSViT (4,172 videos), 6,812 unique source videos (3,148 narrated); video IDs in the released SQL database. Full SurgLaVi adds 2,945 videos from an institutional surgical training archive (not used for β). ViT-B/16 ImageNet init + BERT-base",
        "datasets": ["LEMON YouTube scrape (3,110 videos)", "GenSurgery (GSViT) YouTube scrape (4,172 videos)", "Init: ImageNet ViT-B/16, BERT-base"],
        "quotes": [Q("To construct SurgLaVi-β, we leveraged prior large-scale web scrapes of surgical YouTube videos provided by LEMON [17] and GenSurgery [18], incorporating 3,110 and 4,172 videos, respectively, for a total of 6,812 unique videos.", "surglavi_arxiv_pdf"),
                   Q("SurgLaVi-β represents the open-source subset of SurgLaVi, containing 2,464 videos with 465 hours of surgical footage, sampled at 15 to 30 fps (mean: 28.75 fps), and 112,757 clip–caption pairs following the same hierarchical structure.", "surglavi_arxiv_pdf"),
                   Q("we additionally include 2,945 videos sourced from a surgical training archive that is part of an institutionally approved educational repository", "surglavi_arxiv_pdf"),
                   Q("We adopt a CLIP-style dual-encoder with a ViT-B/16 vision backbone (ImageNet-initialized) and a BERT-base text encoder.", "surglavi_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "SurgLaVi-β is built entirely from web-scraped YouTube surgical videos (LEMON and GenSurgery scrapes, which include appendectomy "
        "videos; GenSurgery's appendectomy URL list was checked by oEmbed in the GSViT entry with no Dresden-area channel). Recording "
        "institutions of individual YouTube videos are not documented, so Appendix300 centres' recordings cannot be excluded.",
        [Q("These videos originate from surgeons and institutions that publicly share operative recordings for educational purposes.", "surglavi_arxiv_pdf")]),
    "input": {
        "frame_size": "224x224",
        "frame_rate_or_sampling": "fixed 16 frames per clip with level-dependent stride (dynamic temporal sampling); package VideoPreprocessor default sample_rate=1 around an anchor frame",
        "clip_length_frames": "16 (single-frame input also supported)",
        "notes": "TimeSformer divided space-time attention over ViT-B/16",
        "quotes": [Q("video = proc(frames).to(device) # (1, 16, 3, 224, 224)", "surgclip_model_md"),
                   Q("A TimeSformer block encodes temporal dynamics over 16 frames.", "surglavi_arxiv_pdf"),
                   Q("While the number of frames per clip remains fixed, the sampling stride varies with the clip’s duration.", "surglavi_arxiv_pdf"),
                   Q('proc = VideoPreprocessor(num_frames=16 , sample_rate=1, mode="centered")', "surgclip_model_md")],
    },
    "embedding_dim": {"value": "768 (pooled vision/text features); 256 (shared multimodal projection)", "basis": "paper appendix and MODEL.md",
                      "quotes": [Q("Outputs (768-d each) are projected into a shared 256-d multimodal space.", "surglavi_arxiv_pdf"),
                                 Q("_, pooled_vision = model.encode_vision(video) # (B, 768)", "surgclip_model_md")]},
    "params": {"value": "not stated (ViT-B/16 TimeSformer + BERT-base; checkpoint file 922 MB)", "quotes": []},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'GFLOP' in arXiv PDF, README, MODEL.md"),
    "eligibility": elig(
        C("PASS", "surgclip_beta.pth publicly listed on HF (gated=false)."),
        C("UNKNOWN", "No licence for the weights (HF repo has no card/licence; MIT covers the pip package code; CC BY-NC-SA 4.0 covers the dataset)."),
        C("PASS", "Video-text contrastive pretraining on surgical video clips (SurgLaVi-β)."),
        C("PASS", "Sources named (LEMON + GenSurgery YouTube scrapes, counts; video IDs in released database)."),
        "Eligibility hinges on the weights licence; research use is plausible (MIT package that loads the weights) but not stated for the checkpoint."),
}
