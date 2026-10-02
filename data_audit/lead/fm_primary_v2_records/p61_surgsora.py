"""SurgSora: Object-Aware Diffusion Model for Controllable Surgical Video Generation (MICCAI 2025) - training code only."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "SurgSora (motion-controllable surgical video generation on frozen Stable Video Diffusion; trained on CoPESD)",
    "aliases": ["DavisMeee/SurgSora"],
    "group": "surgical video generative model",
    "paper": {"title": "SurgSora: Object-Aware Diffusion Model for Controllable Surgical Video Generation", "year": 2025, "venue": "MICCAI 2025", "arxiv": "2412.14018v3",
              "quotes": [Q("arXiv:2412.14018v3 [cs.CV] 22 Jun 2025", "surgsora_arxiv_pdf")]},
    "version": {"value": "GitHub training code (Oct 2025); no SurgSora checkpoint release", "basis": "README Update list",
                "quotes": [Q("· Oct/2025: 📢📢📢 Training Code Released!", "surgsora_github_readme")]},
    "weights_location": {"url": None,
                         "exists": "NO - README lists a local layout with controlnet/diffusion_pytorch_model.safetensors but gives download links only for third-party components (Depth-Anything-V2, CMP); no link to trained SurgSora weights",
                         "access": "not released", "verification": "GitHub README + project page links, 2026-10-02",
                         "quotes": [Q("1. Download the pretrained checkpoint of [DAV2](https://huggingface.co/depth-anything/Depth-Anything-V2-Base/resolve/main/depth_anything_v2_vitb.pth) from huggingface", "surgsora_github_readme"),
                                    Q("|-- controlnet |   |-- config.json |   `-- diffusion_pytorch_model.safetensors", "surgsora_github_readme")]},
    "licence": {"code": "not found (no licence on README/repo page checked)", "weights": "n/a", "url": "https://github.com/DavisMeee/SurgSora", "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "endoscopic submucosal dissection (ESD) video, in vivo porcine (CoPESD); ControlNet-style conditioning of a frozen general-domain SVD",
               "quotes": [Q("This fusion serves as the guidance conditions for a frozen Stable Video Diffusion model to generate realistic surgical video sequences.", "surgsora_arxiv_pdf")]},
    "pretraining_data_quote": {"summary": "CoPESD (20 ESD videos, in vivo porcine, 30 Hz); base Stable Video Diffusion frozen.",
                               "datasets": ["CoPESD", "Base: Stable Video Diffusion (frozen)"],
                               "quotes": [Q("We utilize the publicly available CoPESD dataset [21], which was collected from 20 videos using both conventional endoscopic submucosal dissection (ESD) and the DREAMS system [3], performed on in-vivo porcine models.", "surgsora_arxiv_pdf")]},
    "appendix300_check": A300("UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
                              "Surgical training data are porcine ESD (CoPESD) only; the frozen base Stable Video Diffusion was trained on general web video not enumerated. Moot: no weights.",
                              [Q("performed on in-vivo porcine models", "surgsora_arxiv_pdf")]),
    "input": {"frame_size": "CoPESD source 1920x1080 cropped to 1300x1024; generation resolution not extracted", "frame_rate_or_sampling": "source 30 Hz", "clip_length_frames": "not extracted",
              "notes": "single input frame + user trajectories", "quotes": [Q("The videos were recorded at a frame rate of 30 Hz with an original resolution of 1920 × 1080, which was cropped to 1300 × 1024.", "surgsora_arxiv_pdf")]},
    "embedding_dim": {"value": "not stated (SVD latent space)", "basis": "", "quotes": []},
    "params": {"value": "not stated", "quotes": []},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'parameter' in paper"),
    "eligibility": elig(C("FAIL", "No trained SurgSora weights linked (training code only)."), C("UNKNOWN", "No licence found."),
                        C("PASS", "Conditioning modules trained on surgical endoscopic (porcine ESD) video."), C("PASS", "Paper names CoPESD."), "Not usable: no weights."),
}

REC["weights_location"]["quotes"].append(Q("search='SurgSora' status=200 n=0 ids=[]", "hf_model_search_generative"))
