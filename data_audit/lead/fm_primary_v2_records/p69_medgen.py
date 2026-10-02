"""MedGen (MedGen-1.3B / MedGen-14B; Wan2.1 fine-tuned on MedVideoCap-55K) - general medical video, not primary surgical domain."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "MedGen-1.3B / MedGen-14B (general medical video generation; Wan2.1 fine-tuned on YouTube-derived MedVideoCap-55K)",
    "aliases": ["FreedomIntelligence/MedGen-1.3B", "FreedomIntelligence/MedGen-14B"],
    "group": "medical (not surgical-specific) video generative model",
    "paper": {"title": "MedGen: Unlocking Medical Video Generation by Scaling Granularly-annotated Medical Videos", "year": 2025, "venue": "arXiv preprint", "arxiv": "2507.05675",
              "quotes": [Q("# Unlocking Medical Video Generation by Scaling Granularly-annotated Medical Videos", "medgen_github_readme")]},
    "version": {"value": "MedGen-1.3B HF sha 817b500d8f1d037a6117b8df2cbb9740e32d2ae0 (2026-04-07) (models/medigen-1.3b.safetensors); MedGen-14B listed in README (not checked)",
                "basis": "HF API listing", "quotes": [Q('"sha":"817b500d8f1d037a6117b8df2cbb9740e32d2ae0","lastModified":"2026-04-07T08:20:05.000Z"', "medgen13_hf_api")]},
    "weights_location": {"url": "https://huggingface.co/FreedomIntelligence/MedGen-1.3B", "exists": "YES - HF API lists models/medigen-1.3b.safetensors (2,838,077,328 B) + Wan2.1 VAE/T5; gated=false",
                         "access": "public, not gated", "verification": "HF API listing ?blobs=true, 2026-10-02",
                         "quotes": [Q('"rfilename":"models/medigen-1.3b.safetensors"', "medgen13_hf_api"), Q('"gated":false', "medgen13_hf_api")]},
    "licence": {"code": "not checked", "weights": "Apache-2.0 (HF card metadata)", "url": "https://huggingface.co/FreedomIntelligence/MedGen-1.3B", "code_and_weights_differ": "not checked",
                "quotes": [Q("license: apache-2.0", "medgen13_hf_readme")]},
    "domain": {"value": "general medical video (clinical practice, medical science/teaching, imaging, animation) - surgical/endoscopic video is only a subset; NOT primary surgical/endoscopic domain",
               "quotes": [Q("it includes medical education, medical imaging, clinical practice, and more.", "medgen_github_readme")]},
    "pretraining_data_quote": {"summary": "MedVideoCap-55K: >55K clips curated from ~25M public YouTube videos; base Wan2.1-T2V-1.3B.",
                               "datasets": ["MedVideoCap-55K (YouTube-derived)", "Base: Wan-AI/Wan2.1-T2V-1.3B"],
                               "quotes": [Q("We construct MedVideoCap-55K using publicly available videos from YouTube.", "medgen_arxiv_pdf"),
                                          Q("base_model: - Wan-AI/Wan2.1-T2V-1.3B", "medgen13_hf_readme")]},
    "appendix300_check": A300("UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
                              "YouTube-derived medical clips (surgical videos among them) and a general web-scale base model (Wan2.1) - recordings from the Appendix300 centres cannot be excluded.",
                              [Q("We construct MedVideoCap-55K using publicly available videos from YouTube.", "medgen_arxiv_pdf")]),
    "input": {"frame_size": "not extracted (Wan2.1-T2V-1.3B defaults)", "frame_rate_or_sampling": "not extracted", "clip_length_frames": "not extracted", "notes": "text-to-video", "quotes": []},
    "embedding_dim": {"value": "not stated (Wan2.1 VAE latent)", "basis": "", "quotes": [Q('"rfilename":"models/Wan2.1_VAE.safetensors"', "medgen13_hf_api")]},
    "params": {"value": "1.3B / 14B (model names)", "quotes": [Q("[HF (1.3B)](https://huggingface.co/FreedomIntelligence/MedGen-1.3B)、[HF (14B)](https://huggingface.co/FreedomIntelligence/MedGen-14B)", "medgen_github_readme")]},
    "flops_per_input_if_documented": NOFLOPS("not searched"),
    "eligibility": elig(C("PASS", "HF API lists the weights; gated=false."), C("PASS", "HF card: apache-2.0."),
                        C("FAIL", "Primary domain is general medical video (education, imaging, clinical practice), not surgical/endoscopic video."),
                        C("PASS", "Paper names its data source (YouTube, MedVideoCap-55K) and base model."), "Included for completeness; fails the primary-domain criterion."),
}


# --- lead completion (2026-10-02) ---
REC["input"]["frame_size"] = "not stated for the released models (Wan2.1 base defaults not restated); training clips filtered to resolution above 480p"
REC["input"]["frame_rate_or_sampling"] = "not stated for training; the data-curation classifier sampled videos at 1 FPS"
REC["input"]["clip_length_frames"] = "not stated"
REC["input"]["quotes"] = [Q("Finally, we kept only clips with a resolution above 480p, resulting in 111K medical video clips.", "medgen_arxiv_pdf"),
                          Q("Videos were sampled at 1 frame per second (FPS), and each frame xi (the i-th frame) was labeled as either medical or non-medical", "medgen_arxiv_pdf")]
REC.setdefault("changes_vs_previous", []).append("Lead: input fields filled from the paper (were 'not extracted').")
