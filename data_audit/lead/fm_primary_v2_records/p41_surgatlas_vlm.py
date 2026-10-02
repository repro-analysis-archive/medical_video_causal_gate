"""SurgAtlas-VLM (arXiv 2606.25905) - Qwen3-VL-8B aligned on the SurgAtlas YouTube video-language dataset."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "SurgAtlas-VLM",
    "aliases": ["SurgAtlas"],
    "paper": {
        "title": "SurgAtlas: A Large-Scale Surgical Video-Language Dataset with 2,391 Hours of Open and Minimally Invasive Surgery",
        "year": 2026, "venue": "arXiv preprint (2606.25905v2)", "arxiv": "2606.25905",
        "quotes": [Q("(or arXiv:2606.25905v2 [cs.CV] for this version)", "surgatlas_arxiv_abs")],
    },
    "version": {"value": "no released model checkpoint found; only the dataset filbel/SurgAtlas is public (HF dataset, CC BY 4.0)",
                "basis": "paper states dataset availability only; HF models by author 'filbel' list only an unrelated InternVL3-2B",
                "quotes": [Q("Dataset publicly available at filbel/SurgAtlas.", "surgatlas_arxiv_pdf"), Q('"license:cc-by-4.0"', "surgatlas_hf_dataset_api")]},
    "weights_location": {"url": None, "exists": "NO - SurgAtlas-VLM weights not released (only the dataset)", "access": "not released",
                         "verification": "paper text; HF API author listing", "quotes": []},
    "licence": {"code": "n/a", "weights": "n/a (dataset CC BY 4.0)", "url": "https://huggingface.co/datasets/filbel/SurgAtlas", "code_and_weights_differ": "n/a",
                "quotes": [Q('"license:cc-by-4.0"', "surgatlas_hf_dataset_api")]},
    "domain": {"value": "open and minimally invasive surgical YouTube videos; captioning pretraining + instruction tuning of Qwen3-VL-8B",
               "quotes": [Q("we propose SurgAtlasVLM, built on Qwen3-VL-8B [5].", "surgatlas_arxiv_pdf")]},
    "pretraining_data_quote": {
        "summary": "SurgAtlas: 15,291 YouTube videos (2,391 h), 18 specialties, >5,000 procedure types (6,182 open surgery)",
        "datasets": ["SurgAtlas (YouTube)", "Init: Qwen3-VL-8B"],
        "quotes": [Q("SurgAtlas contains 𝑁 = 15,291 surgical videos and 𝜏 (D) = 2,391 hours of operative footage, sourced entirely from publicly available YouTube content.", "surgatlas_arxiv_pdf")]},
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "Entirely YouTube-sourced (CPT-code-driven search queries); uploading institutions not itemised, so Appendix300 centres' recordings cannot be excluded.",
        [Q("sourced entirely from publicly available YouTube content", "surgatlas_arxiv_pdf")]),
    "input": {"frame_size": "not stated", "frame_rate_or_sampling": "not stated for SurgAtlas-VLM", "clip_length_frames": "not stated",
              "notes": "VLM (video + text in, text out)", "quotes": []},
    "embedding_dim": {"value": None, "basis": "not stated", "quotes": []},
    "params": {"value": "8B (Qwen3-VL-8B base)", "quotes": [Q("SurgAtlas-VLM (8B) outperforms SureonVLM (also 8B)", "surgatlas_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP' in arXiv PDF"),
    "eligibility": elig(
        C("FAIL", "Model weights not released (dataset only)."), C("UNKNOWN", "No model licence."),
        C("PASS", "Surgical-video captioning pretraining + instruction tuning (domain post-training)."),
        C("PASS", "Data source named (SurgAtlas, YouTube, counts)."), ""),
}
