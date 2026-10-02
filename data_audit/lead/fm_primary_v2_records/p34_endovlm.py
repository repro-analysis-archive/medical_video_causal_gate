"""EndoVLM (arXiv 2608.04472, DAMO Academy et al.) - endoscopy image-set / report vision-language pretraining."""
from ._common import A300, C, NOFLOPS, NOT_MENTIONED, Q, elig

REC = {
    "name": "EndoVLM (Anatomy-Guided Sparsity and Progressive Alignment)",
    "aliases": ["EndoVLM (Scatteredrain/EndoVLM)"],
    "paper": {
        "title": "EndoVLM: An Endoscopy Vision-Language Pre-training Model via Anatomy-Guided Sparsity and Progressive Alignment",
        "year": 2026, "venue": "arXiv preprint (2608.04472v1, 5 Aug 2026)", "arxiv": "2608.04472",
        "quotes": [Q("# EndoVLM: An Endoscopy Vision-Language Pre-training Model via Anatomy-Guided Sparsity and Progressive Alignment", "endovlm_github_readme"),
                   Q("arXiv:2608.04472v1 [cs.CV] 5 Aug 2026", "endovlm_arxiv_pdf")],
    },
    "version": {
        "value": "no released checkpoint (README: weights 'will be made publicly available upon acceptance'); code repo Scatteredrain/EndoVLM, no releases",
        "basis": "README and repository page",
        "quotes": [Q("weights will be made publicly available upon acceptance", "endovlm_github_readme")],
    },
    "weights_location": {
        "url": None,
        "exists": "NO - not yet released by the authors. Note: an unrelated-looking same-named HF repo TiramisuQiao/EndoVLM is a Qwen3-VL image-text-to-text fine-tune with gated='manual' access (not linked from the paper; not assessed as this model)",
        "access": "not released",
        "verification": "GitHub README (raw) + repository HTML; HF API listing of TiramisuQiao/EndoVLM (metadata only)",
        "quotes": [Q("you can initialize the model and load our pre-trained weights (weights will be made publicly available upon acceptance).", "endovlm_github_readme"),
                   Q('"gated":"manual"', "endovlm_hf_api_blobs"),
                   Q('"architectures":["Qwen3VLForConditionalGeneration"]', "endovlm_hf_api_blobs")],
    },
    "licence": {
        "code": "none declared on the repository page", "weights": "n/a (not released)", "url": "https://github.com/Scatteredrain/EndoVLM",
        "code_and_weights_differ": "n/a", "quotes": [],
        "note": "Repository page and README searched for 'licen': no licence statement.",
    },
    "domain": {
        "value": "GI endoscopy examination image packages (unordered still-image sets) paired with clinical reports; not video",
        "quotes": [Q("**EndoVLM** is the first vision-language foundation model pre-trained on a massive dataset of 348K unordered endoscopic image sets paired with comprehensive gastrointestinal clinical reports.", "endovlm_github_readme")],
    },
    "pretraining_data_quote": {
        "summary": "Private: >400K endoscopic examinations retrospectively collected from two (unnamed) medical centres, filtered to 348K image-set/report pairs; not releasable",
        "datasets": ["private two-centre GI endoscopy examinations (348K after filtering)"],
        "quotes": [Q("We retrospectively collected over 400K endoscopic examinations from two medical centers1 , each consisting of a clinical report and its corresponding image package.", "endovlm_arxiv_pdf"),
                   Q("Due to patient privacy and ethical guidelines, the 348K pre-training dataset cannot be released at this stage.", "endovlm_github_readme")],
    },
    "appendix300_check": A300(
        "NO", NOT_MENTIONED, False,
        "Private two-centre data (centres not named; IRB of the lead centre, affiliations in China) documented as GI endoscopy examinations "
        "with reports (gastroscopy/colonoscopy image packages); laparoscopic appendectomy video is outside the documented scope. Generic "
        "initialisations (ViT-B/16, PubMedBERT) not itemised.",
        [Q("each consisting of a clinical report and its corresponding image package", "endovlm_arxiv_pdf")]),
    "input": {
        "frame_size": "224x224",
        "frame_rate_or_sampling": "unordered image sets per examination; anatomy-guided sparse pooling selects frames (no temporal sampling)",
        "clip_length_frames": "variable-size image set per examination (not a fixed clip)",
        "notes": "SC-MAE masks 75% of patches on the selected subset",
        "quotes": [Q("All input images are resized to 224 × 224 for pre-training.", "endovlm_arxiv_pdf"),
                   Q("It masks 75% of patches in", "endovlm_arxiv_pdf")],
    },
    "embedding_dim": {"value": None, "basis": "not stated (ViT-B/16 vision encoder; searched 'dimension')", "quotes": []},
    "params": {"value": "not stated (ViT-B/16 + PubMedBERT)",
               "quotes": [Q("The vision encoder and language encoder are instantiated as ViT-B/16 (Dosovitskiy et al., 2020) and PubMedBERT (Gu et al., 2021), respectively.", "endovlm_arxiv_pdf")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'parameters' in arXiv PDF"),
    "eligibility": elig(
        C("FAIL", "Weights not released ('will be made publicly available upon acceptance')."),
        C("UNKNOWN", "No licence statement."),
        C("UNKNOWN", "Endoscopy domain, but training data are examination still-image sets, not documented as video frames."),
        C("FAIL", "Pretraining data described only as private data from 'two medical centers' (not named)."),
        ""),
}
