"""EndoMamba (new entry, fork A)."""
from ._common import A300, C, NOFLOPS, NOT_MENTIONED, Q, elig

REC = {
    "name": "EndoMamba",
    "aliases": ["EndoMamba-S (endomamba_small)"],
    "paper": {
        "title": "EndoMamba: An Efficient Foundation Model for Endoscopic Videos via Hierarchical Pre-training",
        "year": 2025, "venue": "MICCAI 2025 (provisionally accepted per README; arXiv 2502.19090v2)", "arxiv": "2502.19090",
        "quotes": [Q("This repository provides the code for the paper **EndoMamba: An Efficient Foundation Model for Endoscopic Videos via Hierarchical Pre-training**, which has been provisionally accepted by **MICCAI 2025**.", "endomamba_github_readme"),
                   Q("[v2] Thu, 15 May 2025 05:59:22 UTC", "endomamba_arxiv_abs")],
    },
    "version": {
        "value": "endomamba_small_b48_seqlen16_withteacher_MIX12 / checkpoint-499.pth (the single pretrained checkpoint; CSTCloud share Wdh1rxF2QRk); no GitHub releases",
        "basis": "CSTCloud share metadata API (shareGetInfo / shareDirList; metadata only) names the shared folder and file; README links one pretrained-weights share.",
        "quotes": [Q('"name":"endomamba_small_b48_seqlen16_withteacher_MIX12"', "endomamba_weights_cstcloud_shareinfo"),
                   Q('"name":"checkpoint-499.pth"', "endomamba_weights_cstcloud_dirlist")],
    },
    "weights_location": {
        "url": "https://pan.cstcloud.cn/s/Wdh1rxF2QRk",
        "exists": "YES - share resolves (HTTP 200); share metadata API returns stat OK, downloadable=1, expires 2066-06 (epoch ms 2066090709000); folder lists checkpoint-499.pth, 318,035,606 bytes (not downloaded)",
        "access": "public share link, no login or request",
        "verification": "HEAD/GET of the share page + CSTCloud /s/api/shareGetInfo and /s/api/shareDirList JSON (metadata only), 2026-10-02",
        "quotes": [Q("[download pretrained weights](https://pan.cstcloud.cn/s/Wdh1rxF2QRk", "endomamba_github_readme"),
                   Q('"downloadable":1', "endomamba_weights_cstcloud_shareinfo"),
                   Q('"name":"checkpoint-499.pth","parent":1553532620639158,"right":8796094071872,"root":false,"rootFid":1553532620636160,"rs_mtime":1747274496309,"s_ctime":1747274496309,"s_mtime":1747274496309,"size":318035606', "endomamba_weights_cstcloud_dirlist"),
                   Q('"status": 200', "endomamba_weights_cstcloud_check")],
    },
    "licence": {
        "code": "Apache-2.0 (LICENSE.txt in repo)",
        "weights": "not separately stated; repo licence Apache-2.0 (GitHub sidebar 'Apache-2.0 license')",
        "url": "https://github.com/TianCuteQY/EndoMamba/blob/main/LICENSE.txt",
        "code_and_weights_differ": "no separate weights licence stated",
        "quotes": [Q("Apache License Version 2.0, January 2004", "endomamba_github_license"),
                   Q("Readme Apache-2.0 license", "endomamba_github_page")],
    },
    "domain": {
        "value": "endoscopic video (GI colonoscopy/gastroscopy/capsule, laparoscopic surgery sets, porcine bronchoscopy); masked video reconstruction + feature alignment to a general-domain VideoMamba teacher",
        "quotes": [Q("EndoMamba is pretrained on MIX12, a combination of 12 endoscopic datasets.", "endomamba_arxiv_pdf"),
                   Q("we propose to align EndoMamba’s features with VideoMamba, a general-domain video model pretrained on large-scale video data as teacher model.", "endomamba_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "MIX12 = 74,828 clips / 11,303,853 frames: MIX7 shared with Endo-FM (Colonoscopic, SUN & SUN-SEG, LDPolypVideo, Hyper-Kvasir, Kvasir-Capsule, CholecTriplet, Endo-FM private Renji set 'EFM') + GLENDA v1.0, hSDB-instrument, EndoMapper, ROBUST-MIS + own porcine bronchoscopy (PB). Teacher: general-domain VideoMamba-S.",
        "datasets": ["Colonoscopic", "SUN & SUN-SEG", "LDPolypVideo", "Hyper-Kvasir", "Kvasir-Capsule", "CholecTriplet", "EndoFM (Endo-FM pretraining set incl. Renji Hospital private data)",
                     "GLENDA v1.0", "hSDB-instrument", "EndoMapper", "ROBUST-MIS", "PB: authors' porcine bronchoscopy dataset", "Teacher only: VideoMamba-S (general-domain video)"],
        "quotes": [Q("Our full pre-training dataset MIX12 consists of 74,828 video clips, comprising a total of 11,303,853 frames.", "endomamba_arxiv_pdf"),
                   Q("This includes MIX7 (shared with EndoFM), four curated from public datasets, and one from our porcine bronchoscopy dataset (PB), as detailed in Table 1 and Fig. 2.", "endomamba_arxiv_pdf"),
                   Q("MIX7 Source CS [16] S&S [17,9] LP [15] Additional to MIX12 HK [3] KC [25] CT [18] EFM [32] G [10] hS [34] EM [1] R [23] PB", "endomamba_arxiv_pdf"),
                   Q("- [EndoFM](https://github.com/med-air/Endo-FM) - [GLENDA v1.0](https://ftp.itec.aau.at/datasets/GLENDA/v1_0/index.html) - [hSDB-instrument](https://hsdb-instrument.github.io/) - [EndoMapper](https://www.synapse.org/Synapse:syn26707219/wiki/615178) - [ROBUST-MIS](https://www.synapse.org/Synapse:syn18779624)", "endomamba_github_readme")],
    },
    "appendix300_check": A300(
        "NO", NOT_MENTIONED, False,
        "Closed list of 11 named public endoscopy datasets + Endo-FM's set (Renji Hospital Shanghai colonoscopy/gastroscopy) + the authors' own porcine "
        "bronchoscopy data (animal). The laparoscopic sets are CholecTriplet (cholecystectomy), hSDB-instrument, GLENDA (gynaecology) and "
        "ROBUST-MIS (colorectal); none is Appendix300 or an appendectomy recording of its centres. No YouTube or undisclosed in-house human surgical "
        "data. The general-domain VideoMamba-S teacher's own pretraining video is not restated in the paper (feature-alignment target only).",
        [Q("one from our porcine bronchoscopy dataset (PB)", "endomamba_arxiv_pdf")]),
    "input": {
        "frame_size": "224x224",
        "frame_rate_or_sampling": "pretraining default sampling_rate 4 (every 4th frame) per training script; native fps of the sources not normalised in the paper",
        "clip_length_frames": "16 frames in pretraining (tubelet 2); downstream phase recognition/localisation 32-frame clips; recurrent per-frame inference supported",
        "notes": "masked reconstruction with mask_ratio 0.75 default",
        "quotes": [Q("Frames in each video clips are resized to spatial size of 224×224 and frame number of 16 as pre-training input.", "endomamba_arxiv_pdf"),
                   Q("parser.add_argument('--sampling_rate', type=int, default=4)", "endomamba_code_pretrain_script"),
                   Q("parser.add_argument('--tubelet_size', default=2, type=int,", "endomamba_code_pretrain_script"),
                   Q("we sample 32-frame input clips of spatial size 224×224 for fine-tuning", "endomamba_arxiv_pdf"),
                   Q("For real-time applications, EndoMamba processes each frame of a live video stream individually, passing the past states as memory", "endomamba_arxiv_pdf")],
    },
    "embedding_dim": {
        "value": 384,
        "basis": "embed_dim of endomamba_small in the model code; the released checkpoint folder is 'endomamba_small_...' (paper itself does not state the width)",
        "quotes": [Q("def endomamba_small(pretrained=False, **kwargs):", "endomamba_code_model"),
                   Q("model = EndoMamba( embed_dim=384, depth=24,", "endomamba_code_model")],
    },
    "params": {
        "value": "24.46M (paper Table 5, column order EndoFM / VideoMAEv2 / VideoMamba / Ours -> 121.26M / 22.26M / 25.42M / 24.46M)",
        "quotes": [Q("Method Backbone Param Num. Inference Complexity T=32 FPS↑ T=64 T=128 EndoFM [32] VideoMAEv2 [30] VideoMamba [11] Ours video ViT video ViT VideoMamba EndoMamba 121.26M 22.26M 25.42M 24.46M", "endomamba_arxiv_pdf")],
    },
    "flops_per_input_if_documented": {
        "value": None,
        "statement": "no FLOP count reported in paper/README; only asymptotic inference complexity O(P m^2) and throughput 46.7 FPS at T=32 on an A800 (model code contains an fvcore FLOP-count snippet for endomamba_middle, not a reported number)",
        "quotes": [Q("boosting inference speed from 9.2 frames per second (FPS) to 46.7 FPS with a memory length of 32 frames", "endomamba_arxiv_pdf")],
    },
    "eligibility": elig(
        C("PASS", "README links a public CSTCloud share; share API reports downloadable=1 and lists checkpoint-499.pth (318 MB); no login/request (metadata only, not downloaded)."),
        C("PASS", "Repository is Apache-2.0 (LICENSE.txt); no separate weights licence."),
        C("PASS", "Self-supervised masked video pretraining on 12 endoscopic video datasets (MIX12)."),
        C("PASS", "Paper Table 1 and README name every pretraining dataset (incl. own porcine bronchoscopy set)."),
        "Weights licence inferred from the repository licence. Checkpoint file name is a training checkpoint (epoch 499) that may include optimizer state."),
}


# --- lead harmonisation (2026-10-02) ---
REC["appendix300_check"]["cannot_exclude_note"] += (
    " LEAD NOTE: the VideoMamba-S teacher is a distillation target only (does not decide the answer under the lineage rule); "
    "in the repository's videomamba.py the pretrained path registered for VideoMamba-S is an ImageNet-1k checkpoint "
    "(videomamba_s16_in1k_res224.pth), while the paper calls the teacher 'pretrained on large-scale video data' without naming it.")
REC["appendix300_check"]["quotes"].append(Q('"videomamba_s16_in1k": os.path.join(MODEL_PATH, "videomamba_s16_in1k_res224.pth")', "endomamba_code_videomamba"))
REC.setdefault("changes_vs_previous", []).append("Lead note on the distillation teacher added (answer unchanged: NO).")
