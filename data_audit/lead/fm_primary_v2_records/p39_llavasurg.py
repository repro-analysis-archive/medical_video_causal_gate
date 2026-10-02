"""LLaVA-Surg (arXiv 2408.07981) - surgical video conversational assistant (Surg-QA)."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "LLaVA-Surg",
    "aliases": ["Surg-QA"],
    "paper": {
        "title": "LLaVA-Surg: Towards Multimodal Surgical Assistant via Structured Surgical Video Learning",
        "year": 2024, "venue": "arXiv preprint (2408.07981v1)", "arxiv": "2408.07981",
        "quotes": [Q("(or arXiv:2408.07981v1 [cs.CV] for this version)", "llavasurg_arxiv_abs")],
    },
    "version": {"value": "no released checkpoint found (paper promises release; no repository/HF model located)",
                "basis": "paper text; HF model search 'llava-surg'/'llavasurg' returned none; web search found no code repository",
                "quotes": [Q("We will release our code, model, and the instruction-tuning dataset.", "llavasurg_arxiv_pdf")]},
    "weights_location": {"url": None, "exists": "NO - no public checkpoint located (HF search empty; no GitHub link in paper)",
                         "access": "not released", "verification": "HF API model search; paper links (only websurg.com video URLs)", "quotes": []},
    "licence": {"code": "n/a", "weights": "n/a (not released)", "url": "https://arxiv.org/abs/2408.07981", "code_and_weights_differ": "n/a",
                "quotes": [Q("We open-source the surgical instruction-tuning dataset Surg-QA following CC BY NC 4.0 license.", "llavasurg_arxiv_pdf")],
                "note": "CC BY-NC 4.0 is stated for the Surg-QA dataset only."},
    "domain": {"value": "surgical lecture video QA instruction tuning of a general video-LLM; visual encoder is generic CLIP ViT-L/14 (only projector + language model updated)",
               "quotes": [Q("We use CLIP ViT-L/14 as the image encoder and use LLaVA-Med’s language backbone as the initial weight of LLaVA-Surg.", "llavasurg_arxiv_pdf"),
                          Q("by fine-tuning a general-domain vision-language model on SurgQA", "llavasurg_arxiv_pdf")]},
    "pretraining_data_quote": {
        "summary": "Surg-QA: 102K video QA pairs from 44K clips of 2,151 WebSurg surgical lecture videos (per-pair WebSurg URLs provided)",
        "datasets": ["WebSurg lecture videos (2,151)", "Init: CLIP ViT-L/14, LLaVA-Med"],
        "quotes": [Q("We collected 2,151 surgical lecture videos from WebSurg2 [25].", "llavasurg_arxiv_pdf"),
                   Q("featuring over 102K surgical video question-answer pairs derived from more than 44K surgical video clips across 2,201 surgical procedures", "llavasurg_arxiv_pdf")]},
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "WebSurg lectures (IRCAD platform; contributing institutions not itemised in the paper) cover general/digestive surgery incl. "
        "appendectomy-relevant categories; recordings from the Appendix300 centres cannot be excluded.",
        [Q("these videos cover upper and lower gastrointestinal, hepatobiliary, urologic, gynecologic, general hernia, pediatric, endocrine, solid organ, and thoracic surgeries.", "llavasurg_arxiv_pdf")]),
    "input": {"frame_size": "not stated (CLIP ViT-L/14)", "frame_rate_or_sampling": "N frames sampled uniformly per video",
              "clip_length_frames": "N (value not stated in the quoted passage)", "notes": "frame features temporally fused (Video-ChatGPT style)",
              "quotes": [Q("Given a video, the model first samples N frames uniformly", "llavasurg_arxiv_pdf")]},
    "embedding_dim": {"value": None, "basis": "not stated (D = CLIP hidden dimension)", "quotes": []},
    "params": {"value": "not stated (LLaVA-Med 7B-class language backbone + CLIP ViT-L/14)", "quotes": []},
    "flops_per_input_if_documented": NOFLOPS("'FLOP' in arXiv PDF"),
    "eligibility": elig(
        C("FAIL", "No released weights located."),
        C("UNKNOWN", "No model licence (dataset CC BY-NC 4.0 only)."),
        C("FAIL", "Visual encoder is the generic frozen CLIP ViT-L/14; surgical data only tune the projector and language model."),
        C("PASS", "Data source named (2,151 WebSurg lecture videos, per-pair URLs)."),
        ""),
}
