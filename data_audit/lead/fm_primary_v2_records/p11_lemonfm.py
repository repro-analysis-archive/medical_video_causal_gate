"""LemonFM / LEMON (formerly Surg-3M / SurgFM) (new entry, fork A)."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "LemonFM (LEMON; earlier arXiv title Surg-3M / SurgFM)",
    "aliases": ["LemonFM", "SurgFM (arXiv v1 'Surg-3M: A Dataset and Foundation Model for Perception in Surgical Settings')"],
    "paper": {
        "title": "LEMON: A Large Endoscopic MONocular Dataset and Foundation Model for Perception in Surgical Settings",
        "year": 2026, "venue": "CVPR 2026 (arXiv 2503.19740 v1 2025-03-25 ... v4 2026-03-20)", "arxiv": "2503.19740",
        "quotes": [Q("This is the official Hugging Face repository for the paper [LEMON: A Large Endoscopic MONocular Dataset and Foundation Model for Perception in Surgical Settings](https://arxiv.org/abs/2503.19740).", "lemonfm_hf_readme"),
                   Q("Title: Surg-3M: A Dataset and Foundation Model for Perception in Surgical Settings", "lemon_arxiv_abs_v1"),
                   Q("[v4] Fri, 20 Mar 2026 18:48:22 UTC", "lemon_arxiv_abs")],
    },
    "version": {
        "value": "lemonfm.pth (HF visurg/LemonFM, repo sha 4c58064eabf69b0ab148d30933549bf8a1c5bdcc, lastModified 2025-08-12; full checkpoint with student+teacher backbone and heads; feature extractor = teacher backbone)",
        "basis": "HF API listing (metadata only) + GitHub README description of the checkpoint",
        "quotes": [Q('"sha":"4c58064eabf69b0ab148d30933549bf8a1c5bdcc","lastModified":"2025-08-12T14:42:05.000Z"', "lemonfm_hf_api_blobs"),
                   Q("You can download the LemonFM full checkpoint which contains backbone and projection head weights for both student and teacher networks", "lemon_github_readme"),
                   Q("state_dict = state_dict['teacher']", "lemonfm_hf_model_loader")],
    },
    "weights_location": {
        "url": "https://huggingface.co/visurg/LemonFM (file lemonfm.pth)",
        "exists": "YES - HF API lists lemonfm.pth, 1,767,792,186 bytes (LFS sha256 6b0550f6...), gated=false, private=false (not downloaded)",
        "access": "public, not gated",
        "verification": "HF API /api/models/visurg/LemonFM?blobs=true (metadata only), 2026-10-02",
        "quotes": [Q('"rfilename":"lemonfm.pth","blobId":"664ec70680e974843667f32393815375aba80c95","size":1767792186', "lemonfm_hf_api_blobs"),
                   Q('"gated":false', "lemonfm_hf_api_blobs")],
    },
    "licence": {
        "code": "no LICENSE file / licence statement for the code found in the GitHub repo (README licence section covers dataset metadata and annotations: CC BY 4.0)",
        "weights": "Apache-2.0 (HF model card metadata)",
        "url": "https://huggingface.co/visurg/LemonFM",
        "code_and_weights_differ": "yes - weights apache-2.0; dataset metadata/annotations CC BY 4.0 (GitHub) / HF dataset repo cc-by-nc-4.0 with manual gating; raw-video copyright stays with YouTube creators",
        "quotes": [Q("license: apache-2.0", "lemonfm_hf_readme"),
                   Q("We publicly release the dataset metadata, the list of original YouTube video IDs, and our corresponding annotations under the [Creative Commons Attribution 4.0 International (CC BY 4.0) license](https://creativecommons.org/licenses/by/4.0/). The copyright of the raw videos remains with their original creators.", "lemon_github_readme"),
                   Q('"gated":"manual"', "lemon_hf_dataset_api")],
    },
    "domain": {
        "value": "surgical video frames (laparoscopic and robotic minimally invasive surgery, 35 procedure types, YouTube); image (frame-level) encoder",
        "quotes": [Q("*LemonFM* is an image foundation model for surgery, it receives an image as input and produces a feature vector of 1536 features as output.", "lemonfm_hf_readme"),
                   Q("we extract frames from the 4194 videos in LEMON at 1 fps for our foundation model pretraining.", "lemon_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "LEMON: 4,194 curated YouTube surgical videos (938 h), 35 procedure types (robotic and non-robotic laparoscopy), frames at 1 fps; video IDs + procedure labels published in labels.json (252 entries labelled appendectomy).",
        "datasets": ["LEMON (YouTube; video-ID list labels.json, 4,194 entries, 35 procedure labels incl. appendectomy)"],
        "quotes": [Q("Inspired by works [1, 11, 19, 50, 70], we collected our videos from YouTube. For each of the 35 procedures, we searched for videos of their robotic and non-robotic variants using the strings “robotic <procedure type>” and “laparoscopic <procedure type>”, respectively.", "lemon_arxiv_pdf"),
                   Q("the final LEMON dataset consisted of 4194 surgical videos across 35 distinct procedure types, with 94% in 1280 × 720 resolution", "lemon_arxiv_pdf"),
                   Q("[*LEMON*](https://huggingface.co/datasets/visurg/LEMON) is a dataset of over 4K surgical high-resolution videos totaling 938 hours from 35 diverse surgical procedure types.", "lemon_github_readme"),
                   Q('"procedureName": [ "appendectomy" ], "robotic": false, "title": "Laparoscopic Appendectomy", "youtubeId": "IG-uQUSyGC8"', "lemon_github_labels")],
    },
    "appendix300_check": A300(
        "UNKNOWN",
        "Inspired by works [1, 11, 19, 50, 70], we collected our videos from YouTube.", True,
        "Pretraining data are web-collected YouTube videos, including 252 labels.json entries labelled appendectomy whose recording hospitals are not "
        "documented. YouTube oEmbed metadata check of those 252 IDs (titles/channels only; no video downloaded; 2 IDs return 404): no title or "
        "channel matches Dresden, Radeberg, Ravensburg, Asklepios, Elisabethen, Diakonissen, Friedrichstadt, Joseph-Stift, Carus, German/Deutsch, "
        "Klinik/Krankenhaus. Re-uploads or unlabelled origin cannot be excluded, so UNKNOWN. No private/in-house data. Appendix300 (OPARA, "
        "2026-04-29) post-dates the LEMON video collection.",
        [Q('"procedureName": [ "appendectomy" ], "robotic": false, "title": "Laparoscopic Appendectomy", "youtubeId": "IG-uQUSyGC8"', "lemon_github_labels"),
         Q('"keyword_hits": []', "lemon_appendectomy_oembed")]),
    "input": {
        "frame_size": "224x224 (downstream resize stated in paper and HF example; source videos mostly 1280x720)",
        "frame_rate_or_sampling": "frames extracted at 1 fps for pretraining",
        "clip_length_frames": "1 (single-image encoder); the augmented distillation also samples neighbouring frames t±1, t±2 as views",
        "notes": "LemonFM-Vid is a separate video-classification head over per-frame embeddings",
        "quotes": [Q("The images were resized to 224 × 224 for all downstream tasks.", "lemon_arxiv_pdf"),
                   Q("img = img.resize((224, 224))", "lemonfm_hf_readme"),
                   Q("we extract frames from the 4194 videos in LEMON at 1 fps for our foundation model pretraining.", "lemon_arxiv_pdf"),
                   Q("Previous and next frames Input frame 2 Temporal t-1 t+1 t-2 t+2 sampling", "lemon_arxiv_pdf")],
    },
    "embedding_dim": {"value": 1536, "basis": "model card; ConvNeXt-L final feature width",
                      "quotes": [Q("produces a feature vector of 1536 features as output.", "lemonfm_hf_readme")]},
    "params": {
        "value": "not stated in paper/card/README; backbone is torchvision convnext_large (ConvNeXt-L, ~198M parameters is the standard outside figure, unverified here); checkpoint file 1.77 GB holds student+teacher+heads",
        "quotes": [Q("employs ConvNeXt-L [45] for both the teacher and student networks.", "lemon_arxiv_pdf"),
                   Q("net = torchvision.models.convnext_large()", "lemonfm_hf_model_loader")],
    },
    "flops_per_input_if_documented": {
        "value": None,
        "statement": "no FLOP count in paper/card (searched 'FLOP', 'GFLOP'); latency reported instead: 10 ms/frame with a TCN head",
        "quotes": [Q("allows for real-time performance (≤ 40ms/frame [12, 61]) at 10ms/frame", "lemon_arxiv_pdf")],
    },
    "eligibility": elig(
        C("PASS", "HF repo visurg/LemonFM lists lemonfm.pth (1.77 GB), gated=false (API metadata only)."),
        C("PASS", "HF model card licence apache-2.0 (weights). Code repo declares no licence; YouTube source-video copyright stays with creators."),
        C("PASS", "Self-supervised (augmented knowledge distillation) pretraining on frames sampled at 1 fps from surgical videos."),
        C("PASS", "Pretraining source documented: named platform (YouTube) with the full per-video ID list and procedure labels (labels.json)."),
        "Same work as Surg-3M/SurgFM (arXiv v1/v2 title). Appendix300 UNKNOWN because of 252 YouTube appendectomy videos of undocumented origin."),
}
