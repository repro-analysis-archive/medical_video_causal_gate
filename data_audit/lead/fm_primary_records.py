"""PRIMARY foundation-model candidate records (DECISION_003 §2).  One dict per candidate,
appended incrementally.  Quotes are verified by fm_primary_build.py against the saved copies in
/media/user/LaCie/medvideo_gate/fm_candidates/primary/<file>.txt.

Appendix300 coding (DS203): YES = documented in pretraining data; NO = the documented list is
complete (all sources named) and excludes Appendix300 / the five Dresden-area centres'
appendectomy recordings; UNKNOWN = private/in-house/undisclosed or unnamed (e.g. web-crawled
YouTube) sources leave it undecidable.
"""


def Q(quote, file):
    return {"quote": quote, "file": file}


RECORDS = []

# ---------------------------------------------------------------------------------------------
RECORDS.append({
    "name": "Endo-FM",
    "paper": {
        "title": "Foundation Model for Endoscopy Video Analysis via Large-scale Self-supervised Pre-train",
        "year": 2023, "venue": "MICCAI 2023 (LNCS, pp. 101-111)", "arxiv": "2306.16741",
        "quotes": [Q("Foundation Model for Endoscopy Video Analysis via Large-scale Self-supervised Pre-train", "endofm_arxiv_abs")],
    },
    "weights": {
        "url": "https://drive.google.com/file/d/1H7B91Ewm4QkZRsnUk1Bn0IQch5P8C7Xl/view?usp=sharing",
        "exists": "YES - public Google Drive file page resolves without login and names the file endo_fm.pth (file not downloaded)",
        "request_or_registration_required": False,
        "quotes": [
            Q("You can directly download our pre-trained Endo-FM via this [link](https://drive.google.com/file/d/1H7B91Ewm4QkZRsnUk1Bn0IQch5P8C7Xl/view?usp=sharing)", "endofm_github_readme"),
            Q("endo_fm.pth - Google", "endofm_weights_gdrive_view"),
        ],
    },
    "licence": {
        "code": "Apache-2.0", "weights": "not separately stated; the README places 'This project' under Apache-2.0",
        "url": "https://github.com/med-air/Endo-FM/blob/main/LICENSE",
        "code_and_weights_differ": "no separate weights licence stated",
        "quotes": [
            Q("This project is under the Apache License 2.0 license.", "endofm_github_readme"),
            Q("Apache License Version 2.0, January 2004", "endofm_github_license"),
        ],
    },
    "architecture": {
        "description": "Video transformer based on ViT-B/16 (TimeSformer-style divided space-time attention; SVT/DINO-style self-distillation); initialised from the SVT Kinetics-400 ViT-B checkpoint",
        "params": "not stated in paper or README (ViT-B/16 video transformer; ~121M for a TimeSformer-B is an outside estimate, unverified)",
        "input": "video clips; pretraining global views 224x224 with 8-16 frames, local views 96x96 with 2-16 frames; clips 30 fps, ~5 s; downstream classification 8 frames at 224x224",
        "quotes": [
            Q("we develop a video transformer, based on ViT B/16 [8]", "endofm_arxiv_pdf"),
            Q("where Tg ∈ [8, 16] and Tl ∈ [2, 4, 8, 16]. The spatial sizes of global and local views are 224×224 and 96×96, respectively.", "endofm_arxiv_pdf"),
            Q("We process the original videos into 30fps short clips with a duration of 5s on average.", "endofm_arxiv_pdf"),
            Q("sample 8 frames with spatial size 224 × 224 for every video as the input", "endofm_arxiv_pdf"),
            Q("wget -P checkpoints/ https://github.com/kahnchana/svt/releases/download/v1.0/kinetics400_vitb_ssl.pth", "endofm_github_readme"),
        ],
    },
    "pretraining_data": {
        "summary": "6 public endoscopy video datasets (Colonoscopic, SUN & SUN-SEG, LDPolypVideo, Hyper-Kvasir, Kvasir-Capsule, CholecTriplet) + 1 private colonoscopy/gastroscopy set from Baoshan Branch of Renji Hospital, Shanghai; 32,896 clips / 5.02M frames; initialisation from SVT Kinetics-400 (general YouTube action video)",
        "datasets": ["Colonoscopic (CNRS)", "SUN & SUN-SEG", "LDPolypVideo", "Hyper-Kvasir", "Kvasir-Capsule",
                      "CholecTriplet (cholecystectomy, laparoscope)", "Private: Baoshan Branch of Renji Hospital, Shanghai (colonoscope 16,494 clips; gastroscope 7,653 clips)",
                      "Initialisation only: SVT self-supervised ViT-B on Kinetics-400"],
        "documented_list_complete": True,
        "youtube_derived": "Only via the Kinetics-400 initialisation checkpoint (Kinetics clips are taken from YouTube); the endoscopy pretraining data are not YouTube-derived",
        "notes": "Abstract says '9 publicly available datasets' but README and Table 1 list 6 public pretraining datasets (the 9 count appears to include the 3 downstream sets).",
        "quotes": [
            Q("We utilize 6 public and 1 private datasets for pre-training and 3 datasets as the downstream tasks.", "endofm_github_readme"),
            Q("#### Pre-training Data (6 public + 1 private)", "endofm_github_readme"),
            Q("Colonoscopic [19] SUN [20] & SUN-SEG [13] LDPolypVideo [18] Hyper-Kvasir [5] Kvasir-Capsule [31] CholecTriplet [24]", "endofm_arxiv_pdf"),
            Q("Baoshan Branch 16494 of Renji Hospital 7653 2491952 colonoscope 1170753 gastroscope polyp, erosion, etc.", "endofm_arxiv_pdf"),
            Q("We collect all possible public endoscope video datasets and a new one from Baoshan Branch of Renji Hospital for pre-training.", "endofm_arxiv_pdf"),
            Q("combining 9 publicly available datasets and a privately collected dataset from Baoshan Branch of Renji Hospital in Shanghai, China.", "endofm_arxiv_pdf"),
            Q("taken from a different YouTube video", "kinetics_arxiv_abs"),
        ],
    },
    "appendix300_in_pretraining": {
        "answer": "NO",
        "reason": "All pretraining sources are named; the only surgical (laparoscopic) set is CholecTriplet (cholecystectomy) and the only private set is colonoscopy/gastroscopy from Renji Hospital, Shanghai. No appendectomy data and no Dresden-area centre appear. Kinetics-400 initialisation is general human-action video.",
        "quotes": [
            Q("We utilize 6 public and 1 private datasets for pre-training and 3 datasets as the downstream tasks.", "endofm_github_readme"),
            Q("covering 3 endoscopy protocols and 10+ types of diseases", "endofm_arxiv_pdf"),
        ],
    },
    "eligibility": {
        "open_weights": "PASS", "licence_research_use": "PASS", "domain_primary": "PASS",
        "documented_pretraining_data": "PASS", "eligible": "PASS",
        "notes": "Domain: endoscopy video (mostly GI flexible endoscopy; one laparoscopic cholecystectomy set). Weights licence inferred from project-wide Apache-2.0 statement.",
    },
})

# ---------------------------------------------------------------------------------------------
RECORDS.append({
    "name": "EndoFM-LV",
    "paper": {
        "title": "Improving Foundation Model for Endoscopy Video Analysis via Representation Learning on Long Sequences",
        "year": 2025, "venue": "IEEE Journal of Biomedical and Health Informatics 29(5):3526-3536 (doi 10.1109/JBHI.2025.3532311; closed access)",
        "arxiv": None,
        "quotes": [Q("Improving Foundation Model for Endoscopy Video Analysis via Representation Learning on Long Sequences.", "endofmlv_pubmed_efetch"),
                   Q("IEEE J Biomed Health Inform. 2025 May;29(5):3526-3536.", "endofmlv_pubmed_efetch")],
    },
    "weights": {
        "url": "https://mycuhk-my.sharepoint.com/:u:/g/personal/1155167044_link_cuhk_edu_hk/EauTiGd9hg9Lu_7JED3v1E0BwCZ2ZQTsdBfiFo58ADtrmg?e=AZAsP4",
        "exists": "NO (at check 2026-10-02) - the only pretrained-weights link (CUHK SharePoint) returns HTTP 404 '404 FILE NOT FOUND'; open GitHub issue #5 (2026-07-28) reports the same, no reply; no Hugging Face copy found",
        "request_or_registration_required": None,
        "quotes": [
            Q("You can directly download our pre-trained Endo-FM via this [link](https://mycuhk-my.sharepoint.com/:u:/g/personal/1155167044_link_cuhk_edu_hk/EauTiGd9hg9Lu_7JED3v1E0BwCZ2ZQTsdBfiFo58ADtrmg?e=AZAsP4)", "endofmlv_github_readme"),
            Q('"status": 404', "endofmlv_weights_sharepoint_check"),
            Q("The model download links provided in the repository are not working. When I try to access them, I receive a 404 File Not Found error.", "endofmlv_issue5"),
        ],
    },
    "licence": {
        "code": "Apache-2.0", "weights": "not separately stated (project-wide Apache-2.0)",
        "url": "https://github.com/med-air/EndoFM-LV/blob/main/LICENSE",
        "code_and_weights_differ": "no separate weights licence stated",
        "quotes": [Q("This project is under the Apache License 2.0 license.", "endofmlv_github_readme"),
                   Q("Apache License Version 2.0, January 2004", "endofmlv_github_license")],
    },
    "architecture": {
        "description": "TimeSformer video transformer, teacher-student masked-token self-distillation on minute-level sequences",
        "params": "not stated in accessible sources",
        "input": "long clips; pretraining script sets 32 frames (DATA.NUM_FRAMES 32); spatial size not stated in accessible sources (config file is TimeSformer_divST_8x32_224)",
        "quotes": [Q('--arch "timesformer"', "endofmlv_scripts_train"), Q("DATA.NUM_FRAMES 32", "endofmlv_scripts_train")],
    },
    "pretraining_data": {
        "summary": "6,469 long endoscopy videos (>1 min, 13.2M frames) from '4 public and 1 private' datasets; the datasets are NOT named in README/abstract (full paper closed access); repo figure lists domain 'colonoscopy, gastroscopy'; data-prep script globs private2/, private_new/, private_batch3/ and public/*/ folders",
        "datasets": ["4 unnamed public datasets", "1 unnamed private dataset (folders private2, private_new, private_batch3)"],
        "documented_list_complete": False,
        "youtube_derived": "not stated",
        "notes": "Figure assets/dataset.png (saved as endofmlv_github_assets_dataset.png; image, not text-verifiable) gives 'EndoFM-LV (Ours) | 6469 | 13,224,974 | 68.1 | colonoscopy, gastroscopy'. Full JBHI text not accessible (Semantic Scholar openAccessPdf status CLOSED).",
        "quotes": [
            Q("We utilize 4 public and 1 private datasets for pre-training and 4 datasets as the downstream tasks.", "endofmlv_github_readme"),
            Q("For pre-training, we construct a large-scale long endoscopy video dataset comprising 6,469 long endoscopic video samples, each longer than 1 minute and totaling over 13 million frames.", "endofmlv_pubmed_efetch"),
            Q("videolist = glob.glob(f'{datadir}/private2/*.mp4') videolist.extend(glob.glob(f'{datadir}/public/*/*.mp4')) videolist.extend(glob.glob(f'{datadir}/private_new/*.mp4')) videolist.extend(glob.glob(f'{datadir}/private_batch3/*.mp4'))", "endofmlv_data_gencsv"),
        ],
    },
    "appendix300_in_pretraining": {
        "answer": "UNKNOWN",
        "reason": "Public datasets are unnamed in accessible documentation and one private dataset is undisclosed; cannot be decided (domain stated as colonoscopy/gastroscopy, which makes laparoscopic appendectomy unlikely but is not a complete source list).",
        "quotes": [Q("We utilize 4 public and 1 private datasets for pre-training", "endofmlv_github_readme")],
    },
    "eligibility": {
        "open_weights": "FAIL", "licence_research_use": "PASS", "domain_primary": "PASS",
        "documented_pretraining_data": "UNKNOWN", "eligible": "FAIL",
        "notes": "Fails open weights at check time (link 404). Documented-data criterion UNKNOWN: dataset names may be in the closed-access JBHI paper, not verifiable here.",
    },
    "extra_sources": ["endofmlv_github_api_repo", "endofmlv_ieee_doi", "endofmlv_data_trans_videos_pretrain"],
})

# ---------------------------------------------------------------------------------------------
RECORDS.append({
    "name": "EndoViT",
    "paper": {
        "title": "EndoViT: pretraining vision transformers on a large collection of endoscopic images",
        "year": 2024, "venue": "International Journal of Computer Assisted Radiology and Surgery (IJCARS) 2024; doi 10.1007/s11548-024-03091-5; PMC11178556",
        "arxiv": "2303.17636 (earlier version: 'Whether and When does Endoscopy Domain Pretraining Make Sense?')",
        "quotes": [Q("Official codebase of the paper: [EndoViT: pretraining vision transformers on a large collection of endoscopic images]", "endovit_github_readme"),
                   Q("Earlier arXiv version (without semantic-segmentation) can be found here: [Whether and When does Endoscopy Domain Pretraining Make Sense?](https://arxiv.org/abs/2303.17636)", "endovit_github_readme")],
    },
    "weights": {
        "url": "https://huggingface.co/egeozsoy/EndoViT (also Google Drive per-task variants EndoViT_Seg / EndoViT_ATD / EndoViT_SPR linked in GitHub README)",
        "exists": "YES - HF API lists pytorch_model.bin (1,341,188,699 bytes), gated=false, private=false",
        "request_or_registration_required": False,
        "quotes": [Q('"rfilename":"pytorch_model.bin","blobId":"003e961b635141dd163fd12e15550d18c908d60e","size":1341188699', "endovit_hf_api_blobs"), Q('"gated":false', "endovit_hf_api_blobs"),
                   Q("| CholecSeg8k (Segmentation)                 | [EndoViT_Seg](https://drive.google.com/file/d/1NJ-4ZL40kHA_WZ1NylahaS84FcvnigjF/view?usp=share_link)", "endovit_github_readme")],
    },
    "licence": {
        "code": "none declared (GitHub repo DominikBatic/EndoViT has no LICENSE file; GitHub API license = null)",
        "weights": "Apache-2.0 (Hugging Face model card metadata)",
        "url": "https://huggingface.co/egeozsoy/EndoViT",
        "code_and_weights_differ": "yes - weights repo declares apache-2.0; code repo declares no licence",
        "quotes": [Q("license: apache-2.0", "endovit_hf_readme"), Q('"license":null', "endovit_github_api_repo")],
    },
    "architecture": {
        "description": "ViT-Base/16 image encoder pretrained with MAE (75% masking), initialised from ImageNet MAE weights",
        "params": "ViT-B/16 (embed 768, depth 12, 12 heads) ~86M encoder parameters (standard ViT-B figure; count not stated in the sources)",
        "input": "single frames (images) 224x224; Endo700k frames extracted at 1 FPS",
        "quotes": [
            Q("VisionTransformer(patch_size=16, embed_dim=768, depth=12, num_heads=12, mlp_ratio=4", "endovit_hf_readme"),
            Q("The results are reported both for EndoViT’s pretraining resolution of 224 x 224 (Low Res)", "endovit_pmc_fulltext"),
            Q("For consistency, we always downsample to 1 FPS.", "endovit_pmc_fulltext"),
            Q("Consequently, our pre-training uses ImageNet weights as a starting point.", "endovit_github_readme"),
        ],
    },
    "pretraining_data": {
        "summary": "Endo700k = 9 public MIS datasets (743,724 frames at 1 FPS): HeiCo, Cholec80, PSI-AVA, ESAD, LapGyn4 v1.2, hSDB-instrument, DSAD, GLENDA v1.0, SurgicalActions160; plus ImageNet MAE initialisation",
        "datasets": ["HeiCo (Heidelberg colorectal: proctocolectomy, rectal resection, sigmoid resection)", "Cholec80 (cholecystectomy)", "PSI-AVA (robot-assisted radical prostatectomy)",
                      "ESAD (robot-assisted radical prostatectomy)", "LapGyn4 v1.2 (gynecologic laparoscopy)", "hSDB-instrument (lap. cholecystectomy, robotic gastrectomy)",
                      "DSAD - Dresden Surgical Anatomy Dataset (32 robot-assisted rectal resections, University Hospital Carl Gustav Carus Dresden)",
                      "GLENDA v1.0 (gynecologic laparoscopy)", "SurgicalActions160 (gynecologic laparoscopy)", "Initialisation: ImageNet MAE ViT-B"],
        "documented_list_complete": True,
        "youtube_derived": "no (all named curated datasets)",
        "quotes": [
            Q("we introduce Endo700k, a collection of 9 publicly available endoscopic datasets comprising more than 700,000 unlabelled images.", "endovit_github_readme"),
            Q("Table 1 An overview of the individual datasets that form the Endo700k dataset Dataset Surgery type # Surg. # Unique images ESAD [ 3 ] Robot-assisted radical prostatectomy 4 49,544 LapGyn4 (v1.2) [ 15 ] Gynecologic laparoscopy >500 38,192 Surgical Actions160 [ 23 ] Gynecologic laparoscopy 59 761 GLENDA (v1.0) [ 14 ] Gynecologic laparoscopy >400 1,083 hSDB instrument [ 30 ] Laparoscopic cholecystectomy 24 35,576 Robotic gastrectomy 24 HeiCo [ 18 ] Laparoscopic proctocolectomy 10 347,257 Laparoscopic rectal resection 10 Laparoscopic sigmoid resection 10 PSI-AVA [ 27 ] Robot-assisted radical prostatectomy 8 73,618 DSAD [ 4 ] Robot-assisted rectal resection 32 13,195 Cholec80 [ 26 ] Laparoscopic cholecystectomy 80 184,498", "endovit_pmc_fulltext"),
            Q("Outside the previously mentioned exceptions, we use all of the images from the nine datasets.", "endovit_pmc_fulltext"),
            Q("video data from a total of 32 robot-assisted anterior rectal resections or rectal extirpations performed at the University Hospital Carl Gustav Carus Dresden was gathered", "dsad_scidata"),
        ],
    },
    "appendix300_in_pretraining": {
        "answer": "NO",
        "reason": "Complete list of 9 named public datasets; none contains appendectomy. Note: DSAD comes from University Hospital Carl Gustav Carus Dresden (an Appendix300 centre) but consists of robot-assisted rectal resections/extirpations recorded 2019-2021, not appendectomy recordings.",
        "quotes": [
            Q("Endo700k contains a diverse set of endoscopic procedures, both manual and robot-assisted, with several surgery types such as prostatectomy, cholecystectomy, gastrectomy, proctocolectomy, rectal resection, and sigmoid resection.", "endovit_pmc_fulltext"),
            Q("Between February 2019 and February 2021, video data from a total of 32 robot-assisted anterior rectal resections or rectal extirpations performed at the University Hospital Carl Gustav Carus Dresden", "dsad_scidata"),
        ],
    },
    "eligibility": {
        "open_weights": "PASS", "licence_research_use": "PASS", "domain_primary": "PASS",
        "documented_pretraining_data": "PASS", "eligible": "PASS",
        "notes": "Frame-level (image) encoder trained on frames of surgical videos at 1 FPS. Licence PASS rests on the HF weights card (apache-2.0); the GitHub code has no licence. Same-institution overlap (Carus Dresden, via DSAD rectal surgery) should be disclosed even though it is not Appendix300 data.",
    },
    "extra_sources": ["endovit_hf_api", "endovit_arxiv_abs"],
})

# ---------------------------------------------------------------------------------------------
_SURGENET_LIC = {
    "code": "MIT (GitHub TimJaspers0801/SurgeNet LICENSE.txt; SurgeNetDINO repo also MIT)",
    "weights": "CC BY-NC-SA 4.0 per GitHub README/LICENSE_MODELS.txt; the Hugging Face repos' metadata say cc-by-nc-4.0 (inconsistent; both non-commercial, research use permitted)",
    "url": "https://github.com/TimJaspers0801/SurgeNet/blob/main/LICENSE_MODELS.txt",
    "code_and_weights_differ": "yes - code MIT, weights non-commercial (CC BY-NC-SA 4.0 / CC BY-NC 4.0)",
    "quotes": [
        Q("- Code: MIT — see LICENSE (permissive; commercial use permitted).", "surgenet_github_readme"),
        Q("- Pretrained model weights: CC-BY-NC-SA — non-commercial share-alike. The weights and any derivative models that include these weights are NOT cleared for commercial use.", "surgenet_github_readme"),
        Q("Attribution-NonCommercial-ShareAlike 4.0 International", "surgenet_github_license_models"),
        Q('"cardData":{"license":"cc-by-nc-4.0"}', "surgenet_hf_api_blobs"),
        Q("MIT License", "surgenet_github_license"),
    ],
}
_SURGENET_TABLE_Q = [
    Q("| **SurgeNetCholec** | Cholec80 ([Twinnanda et al., 2017b](https://arxiv.org/abs/1602.03012)) | Laparoscopic Cholecystectomy | 76 | 179,164 | Yes |", "surgenet_github_readme"),
    Q("| | HeiChole ([Maier-Hein et al., 2021](https://www.synapse.org/Synapse:syn25101790/wiki/608802)) | Laparoscopic Cholecystectomy | 30 | 53,427 | Yes |", "surgenet_github_readme"),
    Q("| **SurgeNetRAMIE** | RAMIE-UMCU | RA Esophagectomy | 28 | 377,287 | No |", "surgenet_github_readme"),
    Q("| | RARP-AvL | RA Prostatectomy | 8 | 261,516 | No |", "surgenet_github_readme"),
    Q("| **Others** | DSAD ([Carstens et al., 2023](https://www.nature.com/articles/s41597-022-01719-2)) | RA Rectal Resection/Extirpation | 32 | 14,623 | Yes |", "surgenet_github_readme"),
    Q("| | MultiBypass140 ([Lavanchy et al., 2024](https://github.com/CAMMA-public/MultiBypass140)) | Laparoscopic Gastric Bypass Surgery | 140 | 749,419 | Yes |", "surgenet_github_readme"),
    Q("| | SurgToolLoc2022 ([Zia et al., 2023](https://arxiv.org/abs/2305.07152)) | 11 different RA porcine procedures | N/A | 741,516 | Yes |", "surgenet_github_readme"),
]
_SURGENET_DATASETS = ["Cholec80", "HeiChole", "hSDB-Chole", "RAMIE-UMCU (private; UMC Utrecht robot-assisted esophagectomy)", "ESAD",
                      "PSI-AVA", "RARP-AvL (private; robot-assisted prostatectomy)", "DSAD (Carus Dresden robot-assisted rectal resection/extirpation)",
                      "GLENDA", "LapGyn4", "MultiBypass140", "hSDB-Gastric", "SurgToolLoc2022 (porcine)"]

RECORDS.append({
    "name": "SurgeNetXL (CAFormer-S18; plus SurgeNetXL-pretrained DINOv1/v2/v3 ViT-S/B/L from SurgeNetDINO)",
    "paper": {
        "title": "Scaling up self-supervised learning for improved surgical foundation models",
        "year": 2026, "venue": "Medical Image Analysis 108:103873 (2026; arXiv Jan 2025); DINO variants: 'Towards Effective Surgical Representation Learning with DINO Models', MIDL 2026 (OpenReview 6FoIDPKzRV)",
        "arxiv": "2501.09436",
        "quotes": [Q("title = {Scaling up self-supervised learning for improved surgical foundation models}, journal = {Medical Image Analysis}, volume = {108}, pages = {103873}, year = {2026},", "surgenet_github_readme"),
                   Q("**(Accepted for Medical Imaging with Deep Learning (MIDL) 2026)**", "surgenetdino_github_readme")],
    },
    "weights": {
        "url": "https://huggingface.co/TimJaspersTue/SurgeNetModels (SurgeNetXL_checkpoint_epoch0050_teacher.pth); https://huggingface.co/rlpddejong/SurgeNetXL_DINOv1-v3",
        "exists": "YES - HF API lists SurgeNetXL_checkpoint_epoch0050_teacher.pth (93,022,798 B) and DINOv1/v2/v3 ViT .pth files; both repos gated=false",
        "request_or_registration_required": False,
        "quotes": [Q('"rfilename":"SurgeNetXL_checkpoint_epoch0050_teacher.pth","blobId":"621550d8b69a4a9605721d5875c510047c7dd07f","size":93022798', "surgenet_hf_api_blobs"),
                   Q('"gated":false', "surgenet_hf_api_blobs"),
                   Q('"rfilename":"DINOv2_ViTb14_size336_SurgeNetXL.pth","blobId":"f894e7a078bcf9caa62eeb49546cda978e9162a3","size":343942415', "surgenetdino_hf_api_blobs"),
                   Q('"gated":false', "surgenetdino_hf_api_blobs")],
    },
    "licence": dict(_SURGENET_LIC, quotes=_SURGENET_LIC["quotes"] + [Q('"cardData":{"license":"cc-by-nc-4.0"}', "surgenetdino_hf_api_blobs")]),
    "architecture": {
        "description": "Frame encoder. Main model CAFormer-S18 (MetaFormer) pretrained with DINO from ImageNet-1k initialisation; ConvNeXtV2-tiny / PVTv2-B2 variants trained on SurgeNet (no YouTube); SurgeNetDINO: DINOv1 ViT-S/16, ViT-B/16 (224), DINOv2 ViT-S/B/L-14 (336), DINOv3 ViT-S/B/L-16 (336) pretrained on SurgeNetXL",
        "params": "CAFormer-S18 24.3M; SurgeNetDINO segmentation models ViT-S 23M, ViT-B 90-92M, ViT-L 311-314M (segmentation-model parameters as reported)",
        "input": "single frames; downstream frames resized to 224x399; DINO ViTs at 224 (v1) or 336 (v2/v3)",
        "quotes": [Q("Backbone CaFormerS18 Number of parameters 24.3M", "surgenetxl_arxiv_pdf"),
                   Q("We initiate pretraining from ImageNet-initialized weights as recommended by Ramesh et al. (2023)", "surgenetxl_arxiv_pdf"),
                   Q("Input frames are resized to a resolution of 224×399 pixels using bicubic interpolation.", "surgenetxl_arxiv_pdf"),
                   Q("| **DINOv2** | ViT-b | [Download](https://huggingface.co/rlpddejong/SurgeNetXL_DINOv1-v3/resolve/main/DINOv2_ViTb14_size336_SurgeNetXL.pth?download=true) |", "surgenetdino_github_readme")],
    },
    "pretraining_data": {
        "summary": "SurgeNetXL = 4,711,024 frames: 11 public datasets + 2 private (RAMIE-UMCU esophagectomy, RARP-AvL prostatectomy) + Surgical YouTube dataset (3,253 YouTube videos, 2,074,234 frames, 23 procedures incl. an 'appendectomy' subset); ImageNet-1k initialisation",
        "datasets": _SURGENET_DATASETS + ["Surgical YouTube dataset (3,253 videos, 23 procedures; obtained with GSViT/Schmidgall et al. code, curated)"],
        "documented_list_complete": False,
        "youtube_derived": "YES - 2,074,234 of 4,711,024 frames from 3,253 YouTube videos; the released dataset contains an appendectomy folder (7 zip batches); individual video sources/uploaders not enumerated in the documentation (URL list provided via SharePoint text file, not inspected)",
        "quotes": _SURGENET_TABLE_Q + [
            Q("| | YouTube [ours](https://huggingface.co/datasets/TimJaspersTue/SurgeNetYoutube) | 23 identified procedures | 3,253 | 2,074,234 | Yes |", "surgenet_github_readme"),
            Q("| **SurgeNetXL** | All of the above | All of the above | \\>4598 | 4,711,024 | Partly |", "surgenet_github_readme"),
            Q("This curated dataset contains 2,074,234 frames sampled from 23 distinct surgical procedures and is available upon request at [huggingface datasets](https://huggingface.co/datasets/TimJaspersTue/SurgeNetYoutube).", "surgenet_github_readme"),
            Q("The original dataset was created by Schmidgall et al. (2024) and manually curated in our work.", "surgenet_github_readme"),
            Q('"rfilename":"appendectomy/yt_appendectomy_Batch0.zip"', "surgenetyt_hf_dataset_api"),
        ],
    },
    "appendix300_in_pretraining": {
        "answer": "UNKNOWN",
        "reason": "Pretraining includes 3,253 web-crawled YouTube surgical videos with an explicit appendectomy subset whose recording centres are not documented; whether any Dresden-area appendectomy recording is among them cannot be decided. All non-YouTube sources are named and none is Appendix300 (DSAD is Carus Dresden rectal surgery).",
        "quotes": [Q('"rfilename":"appendectomy/yt_appendectomy_Batch0.zip"', "surgenetyt_hf_dataset_api"),
                   Q("| | YouTube [ours](https://huggingface.co/datasets/TimJaspersTue/SurgeNetYoutube) | 23 identified procedures | 3,253 | 2,074,234 | Yes |", "surgenet_github_readme")],
    },
    "eligibility": {
        "open_weights": "PASS", "licence_research_use": "PASS (non-commercial)", "domain_primary": "PASS",
        "documented_pretraining_data": "PASS", "eligible": "PASS",
        "notes": "Eligible under the rule (all four criteria hold); Appendix300 contamination is UNKNOWN because of the YouTube appendectomy subset. Non-commercial weights licence.",
    },
    "extra_sources": ["surgenet_github_api_repo", "surgenet_hf_readme", "surgenetxl_arxiv_abs", "surgenetdino_hf_readme", "surgenetyt_hf_dataset_readme"],
})

RECORDS.append({
    "name": "SurgeNet / SurgeNetPublic / procedure-specific SurgeNet variants (no YouTube data)",
    "paper": {
        "title": "Exploring the Effect of Dataset Diversity in Self-Supervised Learning for Surgical Computer Vision (SurgeNet); variants reported in 'Scaling up self-supervised learning for improved surgical foundation models'",
        "year": 2024, "venue": "MICCAI 2024 DEMI workshop (LNCS, doi 10.1007/978-3-031-73748-0_5); Medical Image Analysis 2026",
        "arxiv": "2407.17904 (SurgeNet; not fetched) / 2501.09436",
        "quotes": [Q("title={Exploring the Effect of Dataset Diversity in Self-supervised Learning for Surgical Computer Vision},", "surgenet_github_readme")],
    },
    "weights": {
        "url": "https://huggingface.co/TimJaspersTue/SurgeNetModels (SurgeNet_checkpoint_epoch0050_teacher.pth, Public_checkpoint_epoch0050_teacher.pth, CHOLEC_/RAMIE_/RARP_ ..., SurgeNet_ConvNextv2_..., SurgeNet_PVTv2_...)",
        "exists": "YES - listed in HF API, gated=false",
        "request_or_registration_required": False,
        "quotes": [Q('"rfilename":"SurgeNet_checkpoint_epoch0050_teacher.pth"', "surgenet_hf_api_blobs"),
                   Q('"rfilename":"Public_checkpoint_epoch0050_teacher.pth"', "surgenet_hf_api_blobs"),
                   Q('"gated":false', "surgenet_hf_api_blobs")],
    },
    "licence": _SURGENET_LIC,
    "architecture": {
        "description": "Frame encoders CAFormer-S18 (also ConvNeXtV2-tiny, PVTv2-B2) pretrained with DINO from ImageNet-1k initialisation",
        "params": "CAFormer-S18 24.3M (ConvNeXtV2-tiny / PVTv2-B2 counts not stated in sources)",
        "input": "single frames (downstream 224x399)",
        "quotes": [Q("The specific variants of these models are PVTv2-B2, ConvNeXtV2-tiny, and CAFormer-S18.", "surgenetxl_arxiv_pdf"),
                   Q("Backbone CaFormerS18 Number of parameters 24.3M", "surgenetxl_arxiv_pdf")],
    },
    "pretraining_data": {
        "summary": "SurgeNet = all SurgeNetXL datasets excluding YouTube (2,636,790 frames: 11 public + 2 named private); SurgeNetPublic = public only (1,997,987 frames); SurgeNetCholec/RAMIE/RARP = procedure subsets; ImageNet-1k initialisation",
        "datasets": _SURGENET_DATASETS,
        "documented_list_complete": True,
        "youtube_derived": "no",
        "notes": "README table labels ESAD as 'RA Esophagectomy' (ESAD is prostatectomy; apparent typo). Private sets are identified by institution and procedure.",
        "quotes": _SURGENET_TABLE_Q + [
            Q("| **SurgeNetPublic** | All public datasets (excluding YouTube & private datasets) | All of the above (excluding YouTube & RA Esophagectomy) | \\>1238 | 1,997,987 | Yes |", "surgenet_github_readme"),
            Q("| **SurgeNet** | All of the above (excluding YouTube) | All of the above (excluding YouTube) | \\>1345 | 2,636,790 | Partly |", "surgenet_github_readme"),
        ],
    },
    "appendix300_in_pretraining": {
        "answer": "NO",
        "reason": "All sources named (11 public + RAMIE-UMCU esophagectomy + RARP-AvL prostatectomy); no appendectomy data and no Appendix300 centre recordings. DSAD is from Carus Dresden but is robot-assisted rectal surgery.",
        "quotes": [Q("| **SurgeNet** | All of the above (excluding YouTube) | All of the above (excluding YouTube) | \\>1345 | 2,636,790 | Partly |", "surgenet_github_readme")],
    },
    "eligibility": {
        "open_weights": "PASS", "licence_research_use": "PASS (non-commercial)", "domain_primary": "PASS",
        "documented_pretraining_data": "PASS", "eligible": "PASS",
        "notes": "Non-commercial weights licence. SurgeNetPublic contains public data only.",
    },
})

# ---------------------------------------------------------------------------------------------
RECORDS.append({
    "name": "GSViT (General Surgery Vision Transformer)",
    "paper": {
        "title": "General surgery vision transformer: A video pre-trained foundation model for general surgery",
        "year": 2024, "venue": "arXiv preprint", "arxiv": "2403.05949",
        "quotes": [Q('Code repository for paper: "General surgery vision transformer: A video pre-trained foundation model for general surgery"', "gsvit_github_readme")],
    },
    "weights": {
        "url": "https://livejohnshopkins-my.sharepoint.com/:u:/g/personal/sschmi46_jh_edu/ERwRJGVUHRtKqvnSabuyKPgBfM8Hhe_Ks0EPTXg97nZ1Qw?e=hh02un",
        "exists": "YES - the Johns Hopkins OneDrive share link resolves (HTTP 200, no login redirect) to the viewer for Documents/GSViT_Models/GSViT.pkl (file not downloaded)",
        "request_or_registration_required": False,
        "quotes": [Q("Please download the GSViT model from here: https://livejohnshopkins-my.sharepoint.com/:u:/g/personal/sschmi46_jh_edu/ERwRJGVUHRtKqvnSabuyKPgBfM8Hhe_Ks0EPTXg97nZ1Qw?e=hh02un", "gsvit_github_readme"),
                   Q("GSViT_Models%2FGSViT.pkl", "gsvit_weights_sharepoint_check"),
                   Q("We open-source the code and weights for GSViT as well as finetuned versions for 10 different procedures.", "gsvit_arxiv_pdf")],
    },
    "licence": {
        "code": "none declared (no LICENSE file; GitHub API license = null; README has no licence statement)",
        "weights": "none declared",
        "url": "https://github.com/SamuelSchmidgall/GSViT",
        "code_and_weights_differ": "no licence for either",
        "quotes": [Q('"license":null', "gsvit_github_api_repo")],
    },
    "architecture": {
        "description": "EfficientViT-M5 encoder (ImageNet-initialised, 'efficientvit_m5') + asymmetric convolutional decoder, pretrained by next-frame prediction on surgical video",
        "params": "12.4M (foundation-model encoder; 26.1M incl. 13.7M classifier head in the Cholec80 experiment); SurgeNetXL paper lists GSViT EfficientViT-M5 12.1M",
        "input": "single frames (next-frame prediction from the current frame); input resolution not stated (decoder reshape 384*4*4 implies 256x256 for EfficientViT-M5 - inference, unverified)",
        "quotes": [Q("The total number of parameters is 26.1M, with 13.7M tuneable parameters and an additional 12.4M non-tuneable parameters for the foundation model", "gsvit_arxiv_pdf"),
                   Q("self.evit = EfficientViT_M5(pretrained='efficientvit_m5')", "gsvit_load_gsvit"),
                   Q("opted for the next-frame reconstruct as demonstrated in [Gao+22].", "gsvit_arxiv_pdf"),
                   Q("x = self.fc(x.reshape(self.in_size, 384*4*4))", "gsvit_pretrain_model")],
    },
    "pretraining_data": {
        "summary": "GenSurgery: 680 h of public YouTube laparoscopic/robotic general-surgery videos, 28 procedures; per-procedure YouTube URL lists in repo videos_to_download/ (incl. appendectomy.txt, 98 URLs) + unsorted.txt",
        "datasets": ["GenSurgery (YouTube; URL lists per procedure incl. appendectomy, cholecystectomy, colectomy, hernia, ... and unsorted)", "Initialisation: ImageNet EfficientViT-M5"],
        "documented_list_complete": "URL lists published (sources enumerated as YouTube URLs), but the recording institution of each video is not documented",
        "youtube_derived": "YES - entirely",
        "notes": "oEmbed metadata check (titles/channels only, no video downloaded) of the 98 appendectomy URLs: all resolve; channels = Dr. Daniel A. Popowich (40), IgorTFerreira (29), Dr Tayyab Riaz Ch (24), ashwin thangavelu (3), Colorectal Disease Journal (1), Dr. R. K. Mishra (1); no title/channel mentions Dresden, Radeberg, Ravensburg, Asklepios, Elisabethen, Diakonissen, Friedrichstadt, St. Joseph-Stift, Carus or Germany. unsorted.txt (~68 kB of URLs) was not checked.",
        "quotes": [Q("we open-source the largest dataset of general surgery videos to-date, consisting of 680 hours of surgical videos, including data from robotic and laparoscopic techniques across 28 procedures", "gsvit_arxiv_pdf"),
                   Q("For the data collection process, a selection of videos was curated from specific playlists of surgical demonstrations on YouTube using surgery related keywords.", "gsvit_arxiv_pdf"),
                   Q("We avoid issues with confidentiality by curating our dataset from public sources", "gsvit_arxiv_pdf"),
                   Q("https://youtu.be/x8sUeH5M5Q0", "gsvit_videos_appendectomy"),
                   Q('"author_name": "Dr. Daniel A. Popowich @ Minimally Invasive Surgeon"', "gsvit_appendectomy_oembed")],
    },
    "appendix300_in_pretraining": {
        "answer": "UNKNOWN",
        "reason": "Pretraining data are YouTube videos including an explicit appendectomy list; video origin (hospital) is not documented. The appendectomy-list channels checked show no Dresden-area link, but the unsorted list and origin of re-uploaded recordings cannot be excluded.",
        "quotes": [Q("a selection of videos was curated from specific playlists of surgical demonstrations on YouTube", "gsvit_arxiv_pdf"),
                   Q("https://youtu.be/4CoA4bUl7G0", "gsvit_videos_appendectomy")],
    },
    "eligibility": {
        "open_weights": "PASS", "licence_research_use": "UNKNOWN", "domain_primary": "PASS",
        "documented_pretraining_data": "PASS", "eligible": "UNKNOWN",
        "notes": "No licence is declared for code or weights (default copyright; 'open-source' wording only) -> research-use permission not established. Pretrained on YouTube video with no licence clearance stated.",
    },
    "extra_sources": ["gsvit_arxiv_abs", "gsvit_download_videos"],
})
