"""SG2VID: Scene Graphs Enable Fine-Grained Control for Video Synthesis (MICCAI 2025)."""
from ._common import A300, C, NOFLOPS, Q, elig

REC = {
    "name": "SG2VID (scene-graph-conditioned surgical video diffusion; per-dataset checkpoints for Cataract-1K, CATARACTS, Cholec80)",
    "aliases": ["SsharvienKumar/SG2VID", "SG2VID-XIMG"],
    "group": "surgical video generative model",
    "paper": {"title": "SG2VID: Scene Graphs Enable Fine-Grained Control for Video Synthesis", "year": 2025, "venue": "MICCAI 2025 (oral)", "arxiv": "2506.03082",
              "quotes": [Q("# SG2VID: Scene Graphs Enable Fine-Grained Control for Video Synthesis (MICCAI 2025 - ORAL)", "sg2vid_hf_readme")]},
    "version": {
        "value": "HF SsharvienKumar/SG2VID sha 869a3efbad4f505818a2094bbbfb831deff0697f (2025-08-28); checkpoints/<dataset>/{vqgan_image, vqgan_segmentation, vae_vid_diffusion, graphencoder_*, video_diffusion_img_graph, video_diffusion_ximg_graph}",
        "basis": "HF API listing",
        "quotes": [Q('"sha":"869a3efbad4f505818a2094bbbfb831deff0697f"', "sg2vid_hf_api"),
                   Q('"rfilename":"checkpoints/Cholec-80/vae_vid_diffusion/vae/config.json"', "sg2vid_hf_api")],
    },
    "weights_location": {
        "url": "https://huggingface.co/SsharvienKumar/SG2VID/tree/main/checkpoints",
        "exists": "YES - HF API lists per-dataset VQGAN/VAE/graph-encoder/video-diffusion checkpoints (e.g. checkpoints/Cataract-1K/video_diffusion_img_graph/checkpoint/unet/diffusion_pytorch_model.safetensors, 4,964,732,628 B); gated=false; linked from the official GitHub README",
        "access": "public, not gated",
        "verification": "HF API listing ?blobs=true, 2026-10-02",
        "quotes": [Q('"rfilename":"checkpoints/Cataract-1K/video_diffusion_img_graph/checkpoint/unet/diffusion_pytorch_model.safetensors"', "sg2vid_hf_api"),
                   Q('"gated":false', "sg2vid_hf_api"),
                   Q("- `Checkpoints`: [VAEs, Graph Encoders, Video Diffusion Models](https://huggingface.co/SsharvienKumar/SG2VID/tree/main/checkpoints)", "sg2vid_github_readme")],
    },
    "licence": {
        "code": "CC-BY-4.0 (GitHub repo licence: LICENSE.txt)", "weights": "CC-BY-4.0 (HF card metadata)",
        "url": "https://huggingface.co/SsharvienKumar/SG2VID ; https://github.com/MECLabTUDA/SG2VID",
        "code_and_weights_differ": "no",
        "quotes": [Q("license: cc-by-4.0", "sg2vid_hf_readme"), Q("Readme CC-BY-4.0 license", "sg2vid_github_page")],
    },
    "domain": {
        "value": "surgical video generation (cataract surgery microscope video; laparoscopic cholecystectomy)",
        "quotes": [Q("We train and validate our model on three publicly available surgical video datasets featuring real-world cataract and cholecystectomy surgeries: Cataract1k [7], CATARACTS [1], and Cholec80 [29].", "sg2vid_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "Cataract-1K (1,000 videos), CATARACTS (50), Cholec80 (80), one model set per dataset; VQGAN/VAE trained per dataset (README training commands); pretrained RAFT, MiDaS and SASVi used only to build scene graphs/segmentations.",
        "datasets": ["Cataract-1K", "CATARACTS", "Cholec80", "Auxiliary (graph construction only): RAFT, MiDaS, SASVi"],
        "quotes": [Q("These datasets vary significantly in size, containing 1000, 50, and 80 videos, respectively", "sg2vid_arxiv_pdf"),
                   Q("python sg2vid/taming/main.py --base configs/vae/config_image_autoencoder_vqgan_<dataset_name>.yaml", "sg2vid_github_readme"),
                   Q("we leverage pre-trained RAFT [28] and MiDaS [22] models averaged over each component’s region.", "sg2vid_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "NO", "the documented data list does not mention DS203/Appendix300", False,
        "Closed list of three named public datasets (Cataract-1K, CATARACTS, Cholec80 - cataract surgery and cholecystectomy); autoencoders trained per dataset. No YouTube or in-house data. Caveat: the paper does not state whether the U-Net/VQGAN were initialised from general-domain weights; the auxiliary RAFT/MiDaS/SASVi models are used only for scene-graph extraction.",
        [Q("Cataract1k [7], CATARACTS [1], and Cholec80 [29]", "sg2vid_arxiv_pdf")]),
    "input": {
        "frame_size": "128x128",
        "frame_rate_or_sampling": "videos downsampled to 4 fps",
        "clip_length_frames": "16 frames (75% overlap between sequences)",
        "notes": "first-frame + scene-graph conditioning",
        "quotes": [Q("videos are downsampled to 4 fps, and video sequences of 16 frames are extracted with a 75% overlap between neighbouring sequences. The frames are downsampled to a resolution of 128×128.", "sg2vid_arxiv_pdf")],
    },
    "embedding_dim": {"value": "not stated (latent of the per-dataset VAE/VQGAN; dimensions not given in paper text)", "basis": "searched paper for latent/channel", "quotes": []},
    "params": {"value": "not stated (video-diffusion U-Net safetensors 4,964,732,628 B per dataset)", "quotes": [Q('"size":4964732628', "sg2vid_hf_api")]},
    "flops_per_input_if_documented": NOFLOPS("'FLOP', 'latency' in paper"),
    "eligibility": elig(
        C("PASS", "HF API lists all checkpoints; gated=false; linked from the official repo README."),
        C("PASS", "CC-BY-4.0 (code repo and HF weights)."),
        C("PASS", "Video diffusion trained on surgical video (cataract, cholecystectomy)."),
        C("PASS", "Paper names the three training datasets."),
        "Per-dataset conditional generator at 128x128, 4 fps."),
}
