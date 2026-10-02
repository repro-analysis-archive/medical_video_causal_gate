"""MedSora: Optical Flow Representation Alignment Mamba Diffusion Model for Medical Video Generation."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "MedSora (Mamba video diffusion model + frequency-compensation video VAE; per-dataset endoscopy checkpoints)",
    "aliases": ["Medical Simulation Video Generator", "MedSora-B"],
    "group": "endoscopy video generative model",
    "paper": {"title": "MedSora: Optical Flow Representation Alignment Mamba Diffusion Model for Medical Video Generation", "year": 2024, "venue": "arXiv preprint", "arxiv": "2411.01647",
              "quotes": [Q("# MedSora: Optical Flow Representation Alignment Mamba Diffusion Model for Medical Video Generation", "medsora_github_readme")]},
    "version": {
        "value": "HF ZhenbinWang/MedSora sha e129d1200296f5d54228077f0b7d5b33cc07fdcf (2024-12-03): MedSora_B_{CholecTriplet,Colonoscopic,KvasirCapsule}.pt + VAE_{...}.pt; no tags",
        "basis": "HF API listing",
        "quotes": [Q('"sha":"e129d1200296f5d54228077f0b7d5b33cc07fdcf","lastModified":"2024-12-03T13:09:59.000Z"', "medsora_hf_api")],
    },
    "weights_location": {
        "url": "https://huggingface.co/ZhenbinWang/MedSora (MedSora_B_Colonoscopic.pt etc.)",
        "exists": "YES - HF API lists MedSora_B_CholecTriplet.pt / _Colonoscopic.pt / _KvasirCapsule.pt (1,383,831,433 B each) and VAE_*.pt; gated=false. Uploader ZhenbinWang = first author Zhenbin Wang, who also hosts the processed datasets the official GitHub README points to (official-ness inferred, not stated).",
        "access": "public, not gated",
        "verification": "HF API listing ?blobs=true, 2026-10-02",
        "quotes": [Q('"rfilename":"MedSora_B_Colonoscopic.pt","blobId":"be5bdaf6a74f47f0f98a1bd4f3e15b754642010e","size":1383831433', "medsora_hf_api"),
                   Q('"rfilename":"VAE_Colonoscopic.pt"', "medsora_hf_api"), Q('"gated":false', "medsora_hf_api"),
                   Q("**Cholec Triplet**:  You can directly use the [processed data](https://huggingface.co/datasets/ZhenbinWang/CholecTriplet_processed)", "medsora_github_readme")],
    },
    "licence": {
        "code": "none found in GitHub repo (raw LICENSE 404)",
        "weights": "Apache-2.0 (HF model card metadata)",
        "url": "https://huggingface.co/ZhenbinWang/MedSora",
        "code_and_weights_differ": "weights apache-2.0; code no licence file",
        "quotes": [Q("license: apache-2.0", "medsora_hf_readme"), Q('"cardData":{"license":"apache-2.0"}', "medsora_hf_api"), Q("404: Not Found", "medsora_github_license")],
    },
    "domain": {
        "value": "endoscopy video generation (colonoscopy, capsule endoscopy, laparoscopic cholecystectomy); one model + VAE per dataset",
        "quotes": [Q("Run [`train_vae.py`](train_vae.py) with the resolution of 128x128 with `1` GPUs on the Colonoscopic dataset", "medsora_github_readme"),
                   Q("The CholecTriplet dataset is an endoscopic video dataset that extends the CholecT40 dataset (Nwoye et al., 2020) for laparoscopic cholecystectomy surgery", "medsora_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "Colonoscopic (Mesejo et al. 2016; 210 colonoscopy videos), CholecTriplet, Kvasir-Capsule; priors: RAFT optical-flow models (Chairs/Things/Sintel/KITTI checkpoints listed) and DINO; video VAE 'built on the 3D causal VAE' (base VAE weights/data not named).",
        "datasets": ["Colonoscopic", "CholecTriplet", "Kvasir-Capsule", "Priors: RAFT, DINO", "Base 3D causal VAE (unnamed source)"],
        "quotes": [Q("Colonoscopic (Mesejo et al., 2016). The Colonoscopic dataset comprises 210 colonoscopy videos", "medsora_arxiv_pdf"),
                   Q("we start by using a pre-trained optical flow prediction model RAFT (Teed & Deng, 2020) to track pixel motion across video frames, and employ a self-supervised visual model DINO", "medsora_arxiv_pdf"),
                   Q("built on the 3D causal VAE", "medsora_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "UNKNOWN", "the documented data list does not mention DS203/Appendix300", False,
        "Diffusion models are trained on three named public endoscopy datasets (no appendectomy, no Appendix300 centre). Not excludable: the video VAE is 'built on the 3D causal VAE' (figure shows frozen parameters) whose pretraining data are not named; DINO/RAFT priors are ImageNet/synthetic+driving.",
        [Q("built on the 3D causal VAE", "medsora_arxiv_pdf")]),
    "input": {
        "frame_size": "128x128",
        "frame_rate_or_sampling": "not stated (source Colonoscopic videos are 30 fps)",
        "clip_length_frames": "16 frames (+8 images for joint training)",
        "notes": "latent z-shape 6x16x16x16 per 16x128x128x3 clip",
        "quotes": [Q("we configured the training video to consist of 16 frames, each with a resolution of 128 × 128 pixels.", "medsora_arxiv_pdf"),
                   Q("LDM 16 × 128 × 128 × 3 8 × 128 × 128 × 3 6 × 16 × 16 × 16 512 12 2 2", "medsora_arxiv_pdf")],
    },
    "embedding_dim": {
        "value": "VAE latent z-shape 6x16x16x16 per 16-frame 128x128 clip; diffusion embedding dimension 512 (MedSora-B, depth 12)",
        "basis": "paper architecture table (S/B/L columns: z-shape, embedding dimension, depth)",
        "quotes": [Q("Architecture video resolution images resolution z-shape Embedding dimension Depth Patch size Strip size LDM 16 × 128 × 128 × 3 8 × 128 × 128 × 3 6 × 16 × 16 × 16 512 6 2 2", "medsora_arxiv_pdf")],
    },
    "params": {"value": "MedSora-B 86.47M trainable (S 43.76M, L 171.89M); released checkpoints are MedSora-B",
               "quotes": [Q("Total training parameters 43.76 M 86.47 M 171.89 M", "medsora_arxiv_pdf")]},
    "flops_per_input_if_documented": {
        "value": None,
        "statement": "Single-forward FLOPs are plotted (Figure 6) but no numeric value is given in the text; not documented numerically.",
        "quotes": [Q("Figure 6 summarizes the floating-point operations (FLOPs), parameter size, and memory consumption involved in training the video Mamba diffusion model", "medsora_arxiv_pdf")],
    },
    "eligibility": elig(
        C("PASS", "HF API lists MedSora-B and VAE checkpoints per dataset; gated=false (author-hosted repo)."),
        C("PASS", "HF model card declares apache-2.0 (no licence file in the GitHub code repo)."),
        C("PASS", "Video diffusion + video VAE trained on endoscopy video datasets."),
        C("PASS", "Paper names the three training datasets (base 3D causal VAE data unnamed)."),
        "Per-dataset 128x128 generative models; official status of the HF repo inferred from author identity."),
}
