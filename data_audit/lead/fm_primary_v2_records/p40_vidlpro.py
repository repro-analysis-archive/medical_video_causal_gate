"""VidLPRO (arXiv 2409.04732) - video-language pretraining on GenSurg+ (GenSurgery YouTube clips)."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "VidLPRO",
    "aliases": ["GenSurg+"],
    "paper": {
        "title": "VidLPRO: A Video-Language Pre-training Framework for Robotic and Laparoscopic Surgery",
        "year": 2024, "venue": "arXiv preprint (2409.04732v2)", "arxiv": "2409.04732",
        "quotes": [Q("(or arXiv:2409.04732v2 [cs.CV] for this version)", "vidlpro_arxiv_abs")],
    },
    "version": {"value": "no released checkpoint found", "basis": "paper contains no code/weights link (searched 'http', 'github', 'code'); HF search 'vidlpro' empty",
                "quotes": []},
    "weights_location": {"url": None, "exists": "NO - no public checkpoint located", "access": "not released",
                         "verification": "paper text; HF API model search", "quotes": []},
    "licence": {"code": "n/a", "weights": "n/a", "url": "https://arxiv.org/abs/2409.04732", "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "robotic and laparoscopic surgical video clips with GPT-4 captions of Whisper transcripts (GenSurg+ from GenSurgery/YouTube)",
               "quotes": [Q("GenSurg+ builds upon the GenSurgery dataset [35], which was originally introduced as the largest publicly available dataset of general surgery videos.", "vidlpro_arxiv_pdf")]},
    "pretraining_data_quote": {
        "summary": "GenSurg+: 17k clip-caption pairs, 1.3k videos, 213 h, derived from GenSurgery (GSViT YouTube collection); BEiT ViT-B/16 + BERT-base initialisation",
        "datasets": ["GenSurg+ (from GenSurgery YouTube videos)", "Init: BEiT, BERT-base"],
        "quotes": [Q("GenSurg+ SVL-Pretrain [33] Publicly Available # Videos # Clip-Caption Pairs Total Duration 3.3 ✓ 1.3k 17k 213 hours", "vidlpro_arxiv_pdf"),
                   Q("The video and text encoders were initialized with BEiT [63] and BERTbase [64] weights, respectively.", "vidlpro_arxiv_pdf")]},
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "Built from GenSurgery (YouTube general-surgery videos incl. an appendectomy list; see GSViT entry); uploading institutions are not "
        "documented, so Appendix300 centres' recordings cannot be excluded.",
        [Q("GenSurg+ builds upon the GenSurgery dataset [35]", "vidlpro_arxiv_pdf")]),
    "input": {"frame_size": "not stated in the saved text (ViT-B/16)", "frame_rate_or_sampling": "4 frames sampled per 45-second clip",
              "clip_length_frames": "4", "notes": "TimeSformer-style divided space-time attention",
              "quotes": [Q("For each 45-second clip, we sampled 4 frames to capture temporal information while maintaining computational efficiency.", "vidlpro_arxiv_pdf"),
                         Q("We employ a standard Vision Transformer, specifically ViT-B/16 [61], as our video encoder.", "vidlpro_arxiv_pdf")]},
    "embedding_dim": {"value": None, "basis": "not stated", "quotes": []},
    "params": {"value": "not stated (ViT-B/16 + BERT-base + fusion module)", "quotes": []},
    "flops_per_input_if_documented": NOFLOPS("'FLOP' in arXiv PDF"),
    "eligibility": elig(
        C("FAIL", "No released weights located."), C("UNKNOWN", "No licence (nothing released)."),
        C("PASS", "Video-language pretraining on surgical video clips."),
        C("PASS", "Pretraining data named (GenSurg+ derived from GenSurgery, counts)."), ""),
}
