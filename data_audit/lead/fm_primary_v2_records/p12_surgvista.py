"""SurgVISTA (new entry, fork A).  Not to be confused with 'SurgVista' world model (arXiv 2606.19889)."""
from ._common import A300, C, Q, elig

REC = {
    "name": "SurgVISTA (Surgical Video-level Spatial-Temporal Architecture)",
    "aliases": ["SurgVISTA"],
    "paper": {
        "title": "Large-scale self-supervised video foundation model for intelligent surgery",
        "year": 2026, "venue": "npj Digital Medicine 2026 (doi 10.1038/s41746-026-02403-0; correction 16 June 2026); arXiv 2506.02692v1", "arxiv": "2506.02692",
        "quotes": [Q("Official Code for \"Large-scale Self-supervised Video Foundation Model for Intelligent Surgery\"", "surgvista_github_page"),
                   Q("[v1] Tue, 3 Jun 2025 09:42:54 UTC", "surgvista_arxiv_abs")],
    },
    "version": {
        "value": "no pretrained SurgVISTA checkpoint released at check date (HF syangcw/SurgVISTA sha e9a8a71e..., lastModified 2025-06-03, contains only README.md + .gitattributes; README 'Parameters: Will be released soon!')",
        "basis": "HF API listing + GitHub README",
        "quotes": [Q('"siblings":[{"rfilename":".gitattributes","blobId":"a6344aac8c09253b3b630fb776ae94478aa0275b","size":1519},{"rfilename":"README.md","blobId":"1f48c32e9df46945f0ac7142bfda001a1beb4747","size":33}]', "surgvista_hf_api_blobs"),
                   Q("## 💾 Parameters Will be released soon! Check out [our Hugging Face page](https://huggingface.co/syangcw/SurgVISTA) for updates.", "surgvista_github_readme")],
    },
    "weights_location": {
        "url": "https://huggingface.co/syangcw/SurgVISTA (announced location; empty)",
        "exists": "NO - the HF repo lists no weight file (only README.md, .gitattributes; usedStorage 0). The only released checkpoint in the README is the converted EndoSSL image TEACHER (Google Drive), not SurgVISTA.",
        "access": "n/a",
        "verification": "HF API /api/models/syangcw/SurgVISTA?blobs=true (metadata only), 2026-10-02",
        "quotes": [Q('"usedStorage":0', "surgvista_hf_api_blobs"),
                   Q("We also release our own converted PyTorch `.pth` checkpoint, available at [this link](https://drive.google.com/file/d/1bazW3W5Cglzfeeh_pdJALLktfxpateJ6/view?usp=sharing).", "surgvista_github_readme")],
    },
    "licence": {
        "code": "CC BY-NC-ND 4.0 (README 'License and Terms of Use': model and code)",
        "weights": "CC BY-NC-ND 4.0 per README; HF repo metadata cc-by-nc-4.0 (no weights there)",
        "url": "https://github.com/isyangshu/SurgVISTA#license-and-terms-of-tuse",
        "code_and_weights_differ": "README covers model and code jointly; HF card says cc-by-nc-4.0",
        "quotes": [Q("This model and associated code are released under the [CC-BY-NC-ND 4.0]((https://creativecommons.org/licenses/by-nc-nd/4.0/deed.en)) license and may only be used for non-commercial, academic research purposes with proper attribution.", "surgvista_github_readme"),
                   Q("license: cc-by-nc-4.0", "surgvista_hf_readme")],
    },
    "domain": {
        "value": "surgical video (laparoscopic/robotic/endoscopic pituitary etc.); video-level masked reconstruction (VideoMAE-style) + image-level distillation from the EndoSSL surgical image teacher",
        "quotes": [Q("we constructed a large-scale surgical video dataset comprising 3,650 videos and approximately 3.55 million frames, spanning more than 20 surgical procedures and over 10 anatomical structures.", "surgvista_arxiv_pdf"),
                   Q("Please refer to [this link](https://github.com/RoyHirsch/endossl) for the teacher model checkpoint used in our pre-training pipeline.", "surgvista_github_readme")],
    },
    "pretraining_data_quote": {
        "summary": "SurgPub (8 public datasets: Cholec80, M2CAI16-Workflow, HeiChole, PitVis, PSI-AVA, AutoLaparo, BernBypass70, StrasBypass70; 274 videos, 1.20M frames) + SurgWeb (3,376 web videos via the GenSurgery/GSViT YouTube pipeline + manual additions; 2.35M frames; includes 98 appendectomy videos); random init; EndoSSL image teacher (private laparoscopy data).",
        "datasets": ["Cholec80", "M2CAI16-Workflow", "HeiChole", "PitVis", "PSI-AVA", "AutoLaparo", "BernBypass70", "StrasBypass70",
                     "SurgWeb (online platforms; GenSurgery pipeline; manually added videos)", "Teacher only: EndoSSL (MSN ViT-L on 23.3M private laparoscopic frames)"],
        "quotes": [Q("SurgPub is constructed from eight publicly available surgical video datasets21–27 , encompassing 274 videos with a total of 1.20 million frames. Complementing SurgPub, SurgWeb comprises 3,376 surgical recordings sourced from online platforms, totaling 2.35 million frames", "surgvista_arxiv_pdf"),
                   Q("Cholec8021 MI2CAI16-Workflow21, 22 HeiChole23 PitVis24 PSI-AVA25 AutoLaparo26 BernBypass7027 StrasBypass7027 SurgWeb", "surgvista_arxiv_pdf"),
                   Q("SurgWeb is a web-sourced dataset constructed using the data collection pipeline proposed in the study19 . After manually removing noisy videos, the dataset consists of 3,376 videos with 2,349,618 frames", "surgvista_arxiv_pdf"),
                   Q("For videos collected from online sources, you can directly follow the [GenSurgery](https://github.com/SamuelSchmidgall/GSViT) pipeline for downloading.", "surgvista_github_readme"),
                   Q("- Adding additional relevant surgical videos manually", "surgvista_github_readme")],
    },
    "appendix300_check": A300(
        "UNKNOWN",
        "Appendix Appendectomy 98", True,
        "SurgWeb (web videos collected with the GenSurgery YouTube pipeline plus manually added videos, list not published; 'will be released' on HF) "
        "contains 98 appendectomy videos of undocumented origin, so Appendix300 source recordings cannot be excluded. SurgPub datasets are named "
        "(HeiChole is Heidelberg-area, none is Appendix300). Teacher EndoSSL was trained on undisclosed private laparoscopy data.",
        [Q("Appendix Appendectomy 98", "surgvista_arxiv_pdf"),
         Q("The complete video dataset will be released via [Hugging Face Datasets](https://huggingface.co/datasets/syangcw/SurgVISTADATA) after final cleaning and validation.", "surgvista_github_readme")]),
    "input": {
        "frame_size": "224x224",
        "frame_rate_or_sampling": "videos first sampled at 1 fps; clip = 16 frames at a fixed interval of 4 (i.e. spanning ~64 s)",
        "clip_length_frames": "16 (cube embedding 2x16x16 -> 8 temporal tokens)",
        "notes": "masking ratio 0.85",
        "quotes": [Q("For each frame, we adopted an input resolution of 224 × 224 pixels", "surgvista_npj_article"),
                   Q("For each video, we first sampled frames at 1 frame per second (fps), and subsequently constructed input video clips by uniformly sampling 16 frames at a fixed interval of 4", "surgvista_arxiv_pdf"),
                   Q("we employ a joint space-time cube embedding strategy29 with a cube size of 2 × 16 × 16", "surgvista_arxiv_pdf")],
    },
    "embedding_dim": {"value": 768, "basis": "ViT-B encoder width (standard ViT-B; the paper states ViT-B but not the width explicitly)",
                      "quotes": [Q("The encoder adopted the ViT-B architecture with fixed spatiotemporal positional embeddings and omitted the use of a class token.", "surgvista_arxiv_pdf")]},
    "params": {"value": "87.4M encoder (100.8M total with decoders)",
               "quotes": [Q("The total number of parameters was 100.8 M, with the encoder accounting for 87.4 M.", "surgvista_arxiv_pdf")]},
    "flops_per_input_if_documented": {"value": None, "statement": "not documented in the saved sources (searched 'FLOP' in arXiv PDF and npj article)", "quotes": []},
    "eligibility": elig(
        C("FAIL", "No SurgVISTA checkpoint is published: HF repo syangcw/SurgVISTA holds only README/.gitattributes; README says parameters 'Will be released soon!'."),
        C("PASS", "README: model and code under CC BY-NC-ND 4.0 for non-commercial academic research."),
        C("PASS", "Self-supervised video-level pretraining on surgical videos (SurgPub + SurgWeb)."),
        C("PASS", "Paper names the 8 public datasets and describes SurgWeb as web-sourced via the GenSurgery pipeline with per-procedure counts."),
        "Re-check later: weights announced for HF. The EndoSSL teacher checkpoint (converted .pth) is the only released file."),
}
