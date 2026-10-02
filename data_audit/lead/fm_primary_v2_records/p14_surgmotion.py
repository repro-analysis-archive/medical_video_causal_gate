"""SurgMotion (V-JEPA-based surgical video FM) (new entry, fork A)."""
from ._common import A300, C, Q, elig

REC = {
    "name": "SurgMotion (SurgMotion-L ViT-L / SurgMotion-G ViT-g; V-JEPA-based)",
    "aliases": ["SurgMotion-L", "SurgMotion-G", "UniSurg (earlier title of arXiv 2602.05638, as cited by SurgRec)"],
    "paper": {
        "title": "SurgMotion: A Video-Native Foundation Model for Universal Understanding of Surgical Videos",
        "year": 2026, "venue": "arXiv preprint 2602.05638 (v1 2026-02-05, v2 2026-03-24, later versions)", "arxiv": "2602.05638",
        "quotes": [Q("Official Code for \"SurgMotion: A Video-Native Foundation Model for Universal Understanding of Surgical Videos\"", "surgmotion_github_page"),
                   Q("[v1] Thu, 5 Feb 2026 13:18:33 UTC", "surgmotion_arxiv_abs"),
                   Q("UniSurg: A Video-Native Foundation Model for Universal Understanding of Surgical Videos. arXiv:2602.05638 (2026)", "surgrec_arxiv_pdf")],
    },
    "version": {
        "value": "SurgMotion-vitl.pt (1,215,657,879 B) and SurgMotion-vitg-xformer.pt (4,048,888,855 B) on HF CAIR-HKISI/SurgMotion, repo sha 2d07bd78..., lastModified 2026-07-20",
        "basis": "HF API listing (metadata only) + README variant table",
        "quotes": [Q('"rfilename":"SurgMotion-vitl.pt","blobId":"b4e18c05c6bc4cc8b096980990c4ff688b3e7399","size":1215657879', "surgmotion_hf_api_blobs"),
                   Q('"rfilename":"SurgMotion-vitg-xformer.pt","blobId":"7df6d3e2e34f83ad6c7b6e014c22a949b6e71001","size":4048888855', "surgmotion_hf_api_blobs"),
                   Q('"sha":"2d07bd780881245866e2e694264f910b5c587328","lastModified":"2026-07-20T09:23:49.000Z"', "surgmotion_hf_api_blobs")],
    },
    "weights_location": {
        "url": "https://huggingface.co/CAIR-HKISI/SurgMotion",
        "exists": "YES (listed) - HF API lists both .pt files, but the repo is gated='manual': files need an HF account, a request form (institution, role, country, intended use, project description) and owner approval; README.md itself returns HTTP 401 without login. Not requested.",
        "access": "gated, MANUAL approval request",
        "verification": "HF API /api/models/CAIR-HKISI/SurgMotion?blobs=true (metadata only) + unauthenticated GET of README (401), 2026-10-02",
        "quotes": [Q('"gated":"manual"', "surgmotion_hf_api_blobs"),
                   Q('"extra_gated_button_content":"Agree and request access"', "surgmotion_hf_api_blobs"),
                   Q("Access to model CAIR-HKISI/SurgMotion is restricted. You must have access to it and be authenticated to access it.", "surgmotion_hf_readme")],
    },
    "licence": {
        "code": "Apache-2.0 (GitHub LICENSE)",
        "weights": "Apache-2.0 per HF gating text ('same license as the GitHub repository') and card metadata",
        "url": "https://github.com/CAIR-HKISI/SurgMotion/blob/main/LICENSE",
        "code_and_weights_differ": "no (both Apache-2.0); weights additionally behind a manual access agreement",
        "quotes": [Q("Apache License Version 2.0, January 2004", "surgmotion_github_license"),
                   Q('"extra_gated_description":"Access to SurgMotion is provided under the same license as the GitHub repository: Apache License 2.0.', "surgmotion_hf_api_blobs")],
    },
    "domain": {
        "value": "surgical video, multi-specialty (neurosurgery, open abdominal, ophthalmic, gastric, laparoscopic, colonoscopy, bronchoscopy, etc.); V-JEPA masked latent prediction",
        "quotes": [Q("Built on the Video Joint Embedding Predictive Architecture (V-JEPA), SurgMotion introduces three key technical innovations tailored to surgical videos", "surgmotion_arxiv_pdf"),
                   Q("We pretrain on SurgMotion-15M, a large-scale multi-specialty surgical video collection aggregated from both public datasets and private institutional sources (Table 1).", "surgmotion_arxiv_pdf")],
    },
    "pretraining_data_quote": {
        "summary": "SurgMotion-15M: 3,658 h from 50 sources. Neurosurgery PitVis + 'Web + Institutional' (2,303 videos, 2,860.85 h, mixed public/private); AVOS (open surgery, 10,874 videos); OphNet + CATARACTS; MultiBypass140 + CoPESD; Cholec80 + M2CAI-2016; EndoFM colonoscopy; AutoLaparo; PSI-AVA; PmLR50; JIGSAWS + AIxSuture; institutional bronchoscopy (private, 60 videos); EgoSurgery.",
        "datasets": ["PitVis", "Neurosurgery web + institutional videos (unnamed)", "AVOS", "OphNet", "CATARACTS", "MultiBypass140", "CoPESD", "Cholec80", "M2CAI-2016",
                     "EndoFM colonoscopy", "AutoLaparo", "PSI-AVA", "PmLR50", "JIGSAWS", "AIxSuture", "Institutional bronchoscopy (private)", "EgoSurgery"],
        "quotes": [Q("Neurosurgery Endonasal pituitary; cranial; spine General surgery Public/Private PitVis [11]; Web+ Institutional 2,303 2,860.85 Mixed Abdominal (various) AVOS [30] 10,874 125.16 Public", "surgmotion_arxiv_pdf"),
                   Q("Ophthalmology Cataract / ophthalmic OphNet [29]; CATARACTS [38] 1,969 230.76 Public Gastric surgery Gastric bypass; ESD MultiBypass140 [39]; CoPESD [40] 180 252.10 Public Laparoscopic cholecystectomy Cholecystectomy Cholec80 [10]; M2CAI-2016 [25] 121 77.51 Public Colonoscopy Endoscopy EndoFM [5] 30,000 45.00 Public", "surgmotion_arxiv_pdf"),
                   Q("Bronchoscopy Endoscopy Institutional 60 50.00 Private Breast surgery Egocentric / OR EgoSurgery [12] 21 10.55 Mixed", "surgmotion_arxiv_pdf"),
                   Q("comprising 3,658 hours of video from 50 sources across 13 organs.", "surgmotion_arxiv_pdf")],
    },
    "appendix300_check": A300(
        "UNKNOWN",
        "aggregated from both public datasets and private institutional sources", True,
        "The documented list does not mention DS203/Appendix300 or its centres, but the largest block ('Web + Institutional' neurosurgery/general "
        "surgery, 2,860 h) and the private bronchoscopy set are unnamed, and AVOS ('Abdominal (various)') is a web-sourced open-surgery set; "
        "web/private/in-house content cannot be excluded.",
        [Q("PitVis [11]; Web+ Institutional", "surgmotion_arxiv_pdf")]),
    "input": {
        "frame_size": "224x224 (shorter side resized to 256, random 224 crop)",
        "frame_rate_or_sampling": "all videos processed at 1 fps",
        "clip_length_frames": "Stage 1: 16 frames; Stage 2 (final): 64 frames; downstream encoder processes 64-frame clips (sliding window)",
        "notes": "16x16 patches as tubes across all T frames; tube masking ratio U(0.75, 0.95)",
        "quotes": [Q("each video frame is resized to have a shorter side of 256 pixels and randomly cropped to 224 × 224 during training. All videos are processed at 1 fps.", "surgmotion_arxiv_pdf"),
                   Q("Stage 1 uses T = 16 frames for 200 epochs with a learning rate of 5 × 10−4 , while Stage 2 continues from the Stage 1 checkpoint using T = 64 frames for 80 epochs.", "surgmotion_arxiv_pdf"),
                   Q("**Video Encoder (ViT)** — processes 64-frame surgical video clips into spatiotemporal token sequences", "surgmotion_github_readme")],
    },
    "embedding_dim": {"value": "1024 (ViT-L) / 1408 (ViT-g) - standard V-JEPA 2 widths, not stated in paper/README",
                      "basis": "backbone names only", "quotes": [Q("| ViT-Large | 300M | SurgMotion-15M |", "surgmotion_github_readme")]},
    "params": {"value": "SurgMotion-L 300M; SurgMotion-G 1B",
               "quotes": [Q("| ViT-Large | 300M | SurgMotion-15M |", "surgmotion_github_readme"), Q("| ViT-Giant-xformer | 1B | SurgMotion-15M |", "surgmotion_github_readme")]},
    "flops_per_input_if_documented": {"value": None, "statement": "not documented in the saved sources (searched 'FLOP' in arXiv PDF and README)", "quotes": []},
    "eligibility": elig(
        C("UNKNOWN", "Weights are listed on HF but gated='manual' (request form + owner approval); per convention manual approval = UNKNOWN. No access was requested."),
        C("PASS", "Apache-2.0 for code and (per gating text) weights."),
        C("PASS", "V-JEPA-style self-supervised pretraining on surgical video (SurgMotion-15M)."),
        C("PASS", "Paper Table 1 names the sources per specialty (with an unnamed 'Web + Institutional' block and one private bronchoscopy set)."),
        "Eligible only if manual access is granted. Largest data block is unnamed web/institutional video."),
}
