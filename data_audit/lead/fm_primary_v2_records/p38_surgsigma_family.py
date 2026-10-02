"""SurgSigma (SurgΣ) model family: SurgVLM, Surg-R1, BSA (Cosmos-H-Surgical is a separate entry)."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "SurgΣ family: SurgVLM / Surg-R1 / BSA (surgical VLMs and action model trained on SurgΣ-DB)",
    "aliases": ["SurgSigma", "SurgVLM-7B/32B/72B", "SurgVLM-9B-Instruct", "SurgVLM-9B-Reasoning", "Surg-R1", "BSA"],
    "paper": {
        "title": "SurgΣ: A Spectrum of Large-Scale Multimodal Data and Foundation Models for Surgical Intelligence (arXiv 2603.16822); SurgVLM (arXiv 2506.02555); Surg-R1 (arXiv 2603.12430); BSA: Generalized Recognition of Basic Surgical Actions (arXiv 2603.12787)",
        "year": "2025-2026", "venue": "arXiv preprints", "arxiv": "2603.16822; 2506.02555; 2603.12430; 2603.12787",
        "quotes": [Q("Building upon SurgΣ-DB, a family of surgical foundation models (i.e., BSA [87], SurgVLM [95], Surg-R1 [33], and Cosmos-H-Surgical [31]) are developed", "surgsigma_arxiv_pdf"),
                   Q("arXiv:2603.12787v1 [cs.CV] 13 Mar 2026", "bsa_arxiv_pdf")],
    },
    "version": {
        "value": "no official public checkpoints: SurgVLM README lists SurgVLM-9B-Instruct / SurgVLM-9B-Reasoning (Qwen3.5-9B) without download links (HF org SurgSigma has datasets only); Surg-R1 'will be released upon publication' (project page 404); BSA no code/weights link",
        "basis": "GitHub README of jinlab-imvr/SurgVLM; Surg-R1 code-availability statement; BSA paper text (no 'github'/'hugging' link)",
        "quotes": [Q("| **SurgVLM-9B-Instruct** | Qwen3.5-9B | An instruction-tuned model for general surgical vision-language understanding |", "surgvlm_github_readme"),
                   Q("The source code and model weights will be released upon publication at the project page:", "surgr1_arxiv_pdf"),
                   Q("There isn't a GitHub Pages site here.", "surgr1_project_page")],
    },
    "weights_location": {
        "url": None,
        "exists": "NO official weights found (2026-10-02). An HF repo SurgR1/qwen2.5-7B-round35-model-merged (Qwen2.5-VL safetensors, no model card, not linked from the paper or project page) exists; its provenance is unverified and it is not treated as the official release",
        "access": "not released (official)",
        "verification": "SurgVLM README; SurgVLM project page links (no model repo); Surg-R1 project page (HTTP 404); HF API listing of the unofficial repo (metadata only)",
        "quotes": [Q("Additional resources and updates will be released through the project page and repository.", "surgvlm_github_readme"),
                   Q('"architectures":["Qwen2_5_VLForConditionalGeneration"]', "surgr1_hf_api_blobs")],
    },
    "licence": {"code": "not stated in the SurgVLM README; Surg-R1/BSA nothing released", "weights": "n/a (not released)",
                "url": "https://github.com/jinlab-imvr/SurgVLM", "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {
        "value": "surgical image/video instruction tuning of general VLMs (Qwen2.5-VL / Qwen3.5) on surgical frames and clips; BSA = action recognition on surgical video clips",
        "quotes": [Q("we propose SurgVLM, which is built upon Qwen2.5-VL, and undergoes instruction tuning to 10+ surgical tasks.", "surgvlm_arxiv_pdf"),
                   Q("We use Qwen2.5-VL-7B as the base model and construct DBase (SurgDB-3M) from multiple public surgical benchmarks", "surgr1_arxiv_pdf"),
                   Q("we present a BSA dataset comprising 10 basic actions across 6 surgical specialties with over 11,000 video clips", "bsa_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "SurgVLM-DB: 1.81M frames / 7.79M conversations from 23 public datasets (arXiv v1); SurgΣ-DB (umbrella) consolidates open-source datasets, in-house clinical collections and web-collected surgical videos; Surg-R1: SurgDB-3M (2,755,141 frames, 23 public datasets) + Surg-R1-Data CoT from 7 public datasets",
        "datasets": ["23 public surgical datasets (SurgVLM-DB / SurgDB-3M)", "SurgΣ-DB in-house clinical collections (not itemised)", "SurgΣ-DB web-collected surgical videos (not itemised)"],
        "quotes": [Q("SurgVLM-DB, comprising over 1.81 million frames with 7.79 million conversations, spanning more than 16 surgical types and 18 anatomical structures. We unify and reorganize 23 public datasets", "surgvlm_arxiv_pdf"),
                   Q("SurgΣ-DB consolidates heterogeneous surgical data sources (including open-source datasets, curated in-house clinical collections and web-source data) into a unified schema", "surgsigma_arxiv_pdf"),
                   Q("For pre-training, we constructed SurgDB-3M, aggregating 2,755,141 image frames across 23 public datasets", "surgr1_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "SurgVLM (arXiv v1) and Surg-R1 pretraining name public datasets only, but the SurgΣ-DB umbrella used for the family includes "
        "web-collected surgical videos and in-house clinical collections that are not itemised, so Appendix300 recordings cannot be "
        "excluded for the released-later models.",
        [Q("SurgΣ-DB combines open-source resources with web-collected surgical videos", "surgsigma_arxiv_pdf")]),
    "input": {
        "frame_size": "not stated in the saved sources (Qwen2.5-VL dynamic-resolution vision encoder)",
        "frame_rate_or_sampling": "image frames and video clips; sampling not stated",
        "clip_length_frames": "not stated",
        "notes": "VLMs (image/video + text in, text out); not a fixed-size embedding encoder",
        "quotes": [],
    },
    "embedding_dim": {"value": None, "basis": "not stated (VLM; hidden size of Qwen2.5-VL-7B not quoted here)", "quotes": []},
    "params": {"value": "SurgVLM-7B / 32B / 72B (arXiv); SurgVLM-9B (Qwen3.5-9B, README); Surg-R1 7B (Qwen2.5-VL-7B)",
               "quotes": [Q("SurgVLM-72B SurgVLM-72B OV SurgVLM-32B OV", "surgvlm_arxiv_pdf"),
                          Q("Includes two specialized models built on **Qwen3.5-9B**", "surgvlm_github_readme")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP' in the SurgVLM / Surg-R1 / BSA PDFs"),
    "eligibility": elig(
        C("FAIL", "No official released weights for SurgVLM, Surg-R1 or BSA."),
        C("UNKNOWN", "No licence statement for models."),
        C("PASS", "Surgical-domain post-training (multi-task instruction tuning / action recognition) on surgical frames and video clips; generic VLM initialisation."),
        C("UNKNOWN", "Public datasets are named, but SurgΣ-DB in-house and web-collected portions are not itemised."),
        "Large VLMs; not frame/clip embedding encoders by design."),
}
