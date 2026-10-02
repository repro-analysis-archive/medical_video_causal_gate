"""PL-Stitch (CVPR 2026, KCL visurg) - self-supervised Plackett-Luce temporal-ranking frame encoder pretrained on LEMON."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "PL-Stitch (pl_lemon.pth; LEMON-pretrained ViT-B/16)",
    "aliases": ["PL-Stitch", "A Stitch in Time"],
    "paper": {
        "title": "A Stitch in Time: Learning Procedural Workflow via Self-Supervised Plackett-Luce Ranking",
        "year": 2026, "venue": "CVPR 2026 (pp. 17000-17010); arXiv 2511.17805v2", "arxiv": "2511.17805",
        "quotes": [Q("# A Stitch in Time: Learning Procedural Workflow via Self-Supervised Plackett-Luce Ranking (CVPR 2026)", "plstitch_github_readme"),
                   Q("(or arXiv:2511.17805v2 [cs.CV] for this version)", "plstitch_arxiv_abs")],
    },
    "version": {
        "value": "pl_lemon.pth (surgical, LEMON-pretrained) in HF visurg/PL-Stitch, repo sha 60afeabe681c7bcd2f3da765cc12ffc29521e695; same repo also has pl_breakfast.pth / pl_gtea.pth (cooking, out of domain)",
        "basis": "README checkpoint table; HF API listing",
        "quotes": [Q("| **LEMON** | [🤗 Download](https://huggingface.co/visurg/PL-Stitch/blob/main/pl_lemon.pth) | `pl_lemon.pth` |", "plstitch_github_readme"),
                   Q('"sha":"60afeabe681c7bcd2f3da765cc12ffc29521e695"', "plstitch_hf_api_blobs")],
    },
    "weights_location": {
        "url": "https://huggingface.co/visurg/PL-Stitch (pl_lemon.pth, 376,857,447 B)",
        "exists": "YES - HF API lists pl_lemon.pth; gated=false (not downloaded)",
        "access": "public, no gating",
        "verification": "HF API ?blobs=true listing, 2026-10-02",
        "quotes": [Q('"rfilename":"pl_lemon.pth","blobId":"8db5e0809aa030f0db002d7f1bc5fb3861bdaaf2","size":376857447', "plstitch_hf_api_blobs"),
                   Q('"gated":false', "plstitch_hf_api_blobs")],
    },
    "licence": {
        "code": "MIT (GitHub LICENSE)", "weights": "MIT (HF model card metadata)",
        "url": "https://huggingface.co/visurg/PL-Stitch ; https://github.com/visurg-ai/PL-Stitch/blob/main/LICENSE",
        "code_and_weights_differ": "no",
        "quotes": [Q('"cardData":{"license":"mit"}', "plstitch_hf_api_blobs"), Q("MIT License", "plstitch_github_license")],
    },
    "domain": {
        "value": "surgical video frames (LEMON YouTube surgical videos) for pl_lemon.pth; frame encoder trained with frame-order ranking on clips",
        "quotes": [Q("Download the pretraining dataset ([LEMON](https://github.com/visurg-ai/LEMON))", "plstitch_github_readme"),
                   Q("we propose PL-Stitch, a self-supervised framework that harnesses the inherent temporal order of video frames as a powerful supervisory signal.", "plstitch_github_readme")],
    },
    "pretraining_data_quote": {
        "summary": "LEMON (YouTube surgical videos; see LemonFM entry) for pl_lemon.pth; initialisation ImageNet-1K iBOT ViT-B/16",
        "datasets": ["LEMON (YouTube surgical video)", "Init: ImageNet-1K iBOT ViT-B/16"],
        "quotes": [Q("Initialization can use ImageNet-1K iBOT ViT-B/16", "plstitch_github_readme"),
                   Q("by pretraining on LEMON [6]", "plstitch_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "Pretraining data = LEMON, a web-scraped YouTube surgical video collection whose uploading institutions are not itemised; "
        "Appendix300 centres' recordings cannot be excluded. ImageNet iBOT initialisation is a closed image benchmark.",
        [Q("Download the pretraining dataset ([LEMON](https://github.com/visurg-ai/LEMON))", "plstitch_github_readme")]),
    "input": {
        "frame_size": "224x224 (README feature-extraction example)",
        "frame_rate_or_sampling": "pretraining: k=8 frames per clip with random start and uniform random step; jigsaw context frames at -2.5..-1.5 s and +1.5..+2.5 s; inference per frame",
        "clip_length_frames": "1 at inference (image in, feature vector out); k=8 frames during pretraining",
        "notes": "frame-by-frame predictions in evaluation",
        "quotes": [Q("img = img.resize((224, 224))", "plstitch_github_readme"),
                   Q("It takes an image as input and produces a feature vector as output", "plstitch_github_readme"),
                   Q("For our temporal ranking objective (Lvid ), we sample k=8 frames from each video of length T .", "plstitch_arxiv_pdf")],
    },
    "embedding_dim": {"value": None, "basis": "not stated numerically (ViT-B/16 [CLS] embedding E in R^(k x D); standard ViT-B width 768 is an outside fact)", "quotes": []},
    "params": {"value": "not stated (ViT-B/16 backbone; checkpoint 377 MB)",
               "quotes": [Q("We adopt ViT-B/16 [11] as our framework’s backbone.", "plstitch_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP' in arXiv PDF and README"),
    "eligibility": elig(
        C("PASS", "pl_lemon.pth publicly listed on HF (gated=false)."),
        C("PASS", "MIT licence on HF card and GitHub."),
        C("PASS", "Self-supervised pretraining on surgical video frames/clips (LEMON)."),
        C("PASS", "Pretraining dataset named (LEMON) and initialisation stated."),
        "Use pl_lemon.pth only (the other two checkpoints are cooking-video models). Backbone of SurgLIME."),
}
