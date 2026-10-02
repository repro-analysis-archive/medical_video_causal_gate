"""SurgLIME (CVPRW 2026, KCL visurg) - LoRA VLP on LLM-narrated LEMON clips over the PL-Stitch encoder."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "SurgLIME (LIME dataset; 'Can LLM-Generated Text Empower Surgical Vision-Language Pre-training?')",
    "aliases": ["SurgLIME", "surglime.pth"],
    "paper": {
        "title": "Can LLM-Generated Text Empower Surgical Vision-Language Pre-training?",
        "year": 2026, "venue": "CVPR 2026 Workshops (oral); arXiv 2604.18134v2", "arxiv": "2604.18134",
        "quotes": [Q("# Can LLM-Generated Text Empower Surgical Vision-Language Pre-training? (CVPRW 2026 Oral)", "surglime_github_readme"),
                   Q("arXiv:2604.18134v2 [cs.CV] 3 May 2026", "llmtext_vlp_arxiv_pdf")],
    },
    "version": {
        "value": "surglime.pth (HF visurg/SurgLIME, repo sha 085e7a8962926354e6a999a694421708ec20cfed, lastModified 2026-08-04); requires the PL-Stitch backbone checkpoint (visurg/PL-Stitch) as frozen base",
        "basis": "HF API listing; README preparation step",
        "quotes": [Q('"sha":"085e7a8962926354e6a999a694421708ec20cfed"', "surglime_hf_api_blobs"),
                   Q("2. Download the [PL-Stitch](https://github.com/visurg-ai/PL-Stitch) vision foundation model.", "surglime_github_readme")],
    },
    "weights_location": {
        "url": "https://huggingface.co/visurg/SurgLIME (surglime.pth, 793,673,798 B)",
        "exists": "YES - HF API lists surglime.pth; gated=false (not downloaded)",
        "access": "public, no gating (the LIME dataset itself is gated='auto')",
        "verification": "HF API ?blobs=true listing, 2026-10-02",
        "quotes": [Q('"rfilename":"surglime.pth","blobId":"2d465f4a99908af4ee1f0642ca41c3a38b3058fd","size":793673798', "surglime_hf_api_blobs"),
                   Q('"gated":false', "surglime_hf_api_blobs")],
    },
    "licence": {
        "code": "not declared in the GitHub repo (no LICENSE file; README has no licence section)",
        "weights": "Apache-2.0 (HF model card metadata); LIME dataset CC BY-NC 4.0",
        "url": "https://huggingface.co/visurg/SurgLIME",
        "code_and_weights_differ": "yes - weights apache-2.0, code undeclared",
        "quotes": [Q("license: apache-2.0", "surglime_hf_readme"), Q('"license:cc-by-nc-4.0"', "lime_hf_dataset_api"),
                   Q("404: Not Found", "surglime_github_license")],
    },
    "domain": {
        "value": "surgical (laparoscopic/endoscopic) YouTube video clips from LEMON with LLM-generated narratives",
        "quotes": [Q("we introduce LIME, a large-scale multi-modal dataset derived from open-access surgical videos using human-free, Large Language Model (LLM)-generated narratives.", "llmtext_vlp_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "LIME: 54k clips from the LEMON collection (4,194 YouTube surgical videos), Gemini-generated captions; vision backbone PL-Stitch (ViT-B, self-supervised on LEMON) frozen + LoRA; PubMedBERT text encoder frozen + LoRA",
        "datasets": ["LIME (derived from LEMON YouTube videos)", "Backbone: PL-Stitch (LEMON-pretrained)", "Text: PubMedBERT"],
        "quotes": [Q("LEMON collection comprises 4194 surgical videos sourced from YouTube", "llmtext_vlp_arxiv_pdf"),
                   Q("we developed a multi-stage automated pipeline to transform these raw videos into a collection of 54k surgical clips with dense semantic annotations.", "llmtext_vlp_arxiv_pdf"),
                   Q("We utilize PL-Stitch [5], a surgical vision foundation model (ViT-Base) robustly pre-trained on the large-scale surgical dataset LEMON [6], as our visual foundation.", "llmtext_vlp_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "All visual training data (LIME and the PL-Stitch backbone) derive from LEMON, a YouTube scrape of surgical videos whose uploading "
        "institutions are not itemised; Appendix300 centres' recordings cannot be excluded (see the LemonFM entry for LEMON's procedure list).",
        [Q("LEMON collection comprises 4194 surgical videos sourced from YouTube", "llmtext_vlp_arxiv_pdf")]),
    "input": {
        "frame_size": "not stated for the encoder input (raw videos standardised to 832x480 during dataset construction); ViT-B/16 backbone",
        "frame_rate_or_sampling": "not stated; frame-level embeddings of a temporal window aggregated by attention pooling",
        "clip_length_frames": "8 (T = 8 temporal window)",
        "notes": "the spatial encoder processes the T frames independently",
        "quotes": [Q("a temporal window of T = 8 frames is processed via the learnable attention-based pooling layer.", "llmtext_vlp_arxiv_pdf"),
                   Q("we performed a shortest-side resize followed by a center crop to achieve a fixed resolution of 832 × 480 pixels.", "llmtext_vlp_arxiv_pdf"),
                   Q("the spatial encoder processes the T frames independently to extract frame-level global embeddings", "llmtext_vlp_arxiv_pdf")],
    },
    "embedding_dim": {"value": None, "basis": "not stated numerically (shared space z in R^D; searched 'dimension', '768', '512')", "quotes": []},
    "params": {"value": "not stated (ViT-B/16 PL-Stitch + PubMedBERT + LoRA; checkpoint 794 MB)", "quotes": []},
    "flops_per_input_if_documented": NOFLOPS("'FLOP' in arXiv PDF and README"),
    "eligibility": elig(
        C("PASS", "surglime.pth publicly listed on HF (gated=false)."),
        C("PASS", "HF model card: apache-2.0."),
        C("PASS", "Video-language pretraining (LoRA) on surgical video clips; backbone self-supervised on surgical video frames (LEMON)."),
        C("PASS", "Sources named: LEMON YouTube collection (4,194 videos) -> LIME 54k clips."),
        "Depends on the PL-Stitch checkpoint (visurg/PL-Stitch) as frozen base; PL-Stitch itself not assessed here."),
}
