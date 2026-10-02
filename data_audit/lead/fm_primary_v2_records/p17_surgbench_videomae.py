"""SurgBench continual-pretrained VideoMAE (new entry, fork A; no public weights)."""
from ._common import A300, C, Q, elig

REC = {
    "name": "SurgBench VideoMAE (continual pretraining of VideoMAE-B/L on SurgBench-P)",
    "aliases": ["SurgBench-P VideoMAE CPT"],
    "paper": {
        "title": "SurgBench: A Unified Large-Scale Benchmark for Surgical Video Analysis",
        "year": 2025, "venue": "arXiv 2506.07603v2 (2025-06-16)", "arxiv": "2506.07603",
        "quotes": [Q("Title: SurgBench: A Unified Large-Scale Benchmark for Surgical Video Analysis", "surgbench_arxiv_abs"),
                   Q("[v2] Mon, 16 Jun 2025 03:31:25 UTC", "surgbench_arxiv_abs")],
    },
    "version": {"value": "no released checkpoint (VideoMAE-Standard ViT-B and VideoMAE-Large ViT-L CPT models described only in the paper)",
                "basis": "paper: dataset and code only 'available upon request'; no weights URL found",
                "quotes": [Q("Our dataset and code are available upon request.", "surgbench_arxiv_pdf")]},
    "weights_location": {"url": None, "exists": "NO - no weights URL in paper/abstract page; dataset and code only upon request; no repository or HF listing found in search",
                         "access": "n/a (request for dataset/code only)", "verification": "arXiv abs + PDF text searched for github/huggingface/release, 2026-10-02",
                         "quotes": [Q("Our dataset and code are available upon request.", "surgbench_arxiv_pdf")]},
    "licence": {"code": "none stated for code/models (paper Appendix A lists the licences of the aggregated source datasets only)", "weights": "none stated",
                "url": "https://arxiv.org/abs/2506.07603", "code_and_weights_differ": "n/a",
                "quotes": [Q("A Dataset License SurgBench aggregates several publicly available surgical video datasets, with their respective licenses meticulously reviewed", "surgbench_arxiv_pdf")]},
    "domain": {"value": "surgical video (laparoscopic, endoscopic, robotic, open); VideoMAE masked reconstruction, continued from Kinetics-400 VideoMAE",
               "quotes": [Q("We initiated our continual pre-training (CPT) by leveraging VideoMAE models (Tong et al., 2022) pre-trained on the general-domain Kinetics-400 dataset.", "surgbench_arxiv_pdf")]},
    "pretraining_data_quote": {
        "summary": "SurgBench-P: 16 sources (15 public incl. AVOS, AIxSuture, Cholec80, CholecT45, Colonoscopic, Endo-FM, SimSurgSkill 2021, JIGSAWS, CholecT50, AutoLaparo, EndoVis 2019, Hyper-Kvasir, Colonoscopic-web, Kvasir-Capsule, LDPolypVideo + 1 private dataset), 53M frames, 22 procedures incl. appendectomy; refined to 39,807 clips for CPT.",
        "datasets": ["AVOS", "AIxSuture", "Cholec80", "CholecT45", "Colonoscopic", "Endo-FM", "SimSurgSkill 2021", "JIGSAWS", "CholecT50", "AutoLaparo", "EndoVis 2019", "Hyper-Kvasir",
                     "Colonoscopic-web", "Kvasir-Capsule", "LDPolypVideo", "Private Data (right hemicolectomy)"],
        "quotes": [Q("The pre-training subset SurgBench-P comprises 53 million frames from 16 distinct sources (Figure 1)", "surgbench_arxiv_pdf"),
                   Q("included 15 public datasets and 1 additional private dataset", "surgbench_arxiv_pdf"),
                   Q("General Surgery Appendectomy S1, S6", "surgbench_arxiv_pdf")]},
    "appendix300_check": A300(
        "UNKNOWN", "General Surgery Appendectomy S1, S6", True,
        "Appendectomy footage comes from S1 (AVOS, web-sourced open-surgery videos) and S6; one private dataset is included. The documented list "
        "does not mention DS203/Appendix300 or its centres, but web-sourced and private content cannot be excluded.",
        [Q("included 15 public datasets and 1 additional private dataset", "surgbench_arxiv_pdf")]),
    "input": {"frame_size": "224x224", "frame_rate_or_sampling": "temporal sampling rate 4", "clip_length_frames": "16",
              "notes": "masking ratio 0.9",
              "quotes": [Q("a refined set of 39,807 video clips (resized to 224×224 resolution)", "surgbench_arxiv_pdf"),
                         Q("CPT parameters for both variants included an input of 16 frames per clip with a temporal sampling rate of 4.", "surgbench_arxiv_pdf")]},
    "embedding_dim": {"value": "768 (ViT-B) / 1024 (ViT-L) - standard widths, not stated", "basis": "architecture names",
                      "quotes": [Q("VideoMAE-Standard, which incorporates a ViT-Base encoder and a 4-layer Transformer decoder, and VideoMAE-Large, featuring a ViT-Large encoder", "surgbench_arxiv_pdf")]},
    "params": {"value": "not stated", "quotes": []},
    "flops_per_input_if_documented": {"value": None, "statement": "not documented (searched 'FLOP' in arXiv PDF)", "quotes": []},
    "eligibility": elig(
        C("FAIL", "No public checkpoint; paper offers dataset and code only upon request."),
        C("UNKNOWN", "No licence stated for code or models."),
        C("PASS", "Continued VideoMAE pretraining on surgical video (SurgBench-P)."),
        C("PASS", "Paper Table 2 names the 15 public sources and one private dataset."),
        "Listed for completeness (VideoMAE on surgical video)."),
}
