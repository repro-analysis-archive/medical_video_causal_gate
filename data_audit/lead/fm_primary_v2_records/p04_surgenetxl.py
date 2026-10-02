"""SurgeNetXL + SurgeNetXL-pretrained DINO ViTs (old entry 4; legacy fields kept, new fields added)."""
import copy

from fm_primary_records import RECORDS as _OLD
from ._common import A300, C, NOFLOPS, Q, elig

REC = copy.deepcopy(_OLD[3])
assert REC["name"].startswith("SurgeNetXL")
REC["legacy_eligibility_first_pass"] = REC.pop("eligibility")
REC["extra_sources"] = [s for s in REC.get("extra_sources", []) if s != "surgenetyt_hf_dataset_readme"]

_YT = "| | YouTube [ours](https://huggingface.co/datasets/TimJaspersTue/SurgeNetYoutube) | 23 identified procedures | 3,253 | 2,074,234 | Yes |"

REC["version"] = {
    "value": "SurgeNetXL_checkpoint_epoch0050_teacher.pth (CAFormer-S18 DINO teacher, epoch 50; also epoch0005/0025 and full SurgeNetXL_checkpoint0050.pth) in HF TimJaspersTue/SurgeNetModels (repo sha cc21f4a1..., lastModified 2026-03-04); "
             "SurgeNetDINO: DINOv1_ViT{s16,b16}_size224 / DINOv2_ViT{s14,b14,l14}_size336 / DINOv3_ViT{s16,b16,l16}_size336 _SurgeNetXL.pth in HF rlpddejong/SurgeNetXL_DINOv1-v3 (sha 9b2c75b7..., lastModified 2025-11-28)",
    "basis": "HF API listings (file names, repo sha, lastModified); README model tables.",
    "quotes": [Q('"rfilename":"SurgeNetXL_checkpoint_epoch0050_teacher.pth"', "surgenet_hf_api_blobs"),
               Q('"sha":"cc21f4a158f3a17260d8304e9d2b24b580a6ea35","lastModified":"2026-03-04T10:19:50.000Z"', "surgenet_hf_api_blobs"),
               Q('"sha":"9b2c75b7d469850b750a715b90cb91d6319f7e30","lastModified":"2025-11-28T12:56:23.000Z"', "surgenetdino_hf_api_blobs"),
               Q('"rfilename":"DINOv3_ViTl16_size336_SurgeNetXL.pth"', "surgenetdino_hf_api_blobs")],
}
REC["weights_location"] = {
    "url": "https://huggingface.co/TimJaspersTue/SurgeNetModels ; https://huggingface.co/rlpddejong/SurgeNetXL_DINOv1-v3",
    "exists": "YES - HF API lists SurgeNetXL_checkpoint_epoch0050_teacher.pth (93,022,798 B) and the 8 DINO ViT .pth files; both repos gated=false (not downloaded)",
    "access": "public, not gated",
    "verification": "HF API model listings with ?blobs=true, 2026-10-02",
    "quotes": [Q('"rfilename":"SurgeNetXL_checkpoint_epoch0050_teacher.pth","blobId":"621550d8b69a4a9605721d5875c510047c7dd07f","size":93022798', "surgenet_hf_api_blobs"),
               Q('"gated":false', "surgenet_hf_api_blobs"),
               Q('"rfilename":"DINOv2_ViTb14_size336_SurgeNetXL.pth","blobId":"f894e7a078bcf9caa62eeb49546cda978e9162a3","size":343942415', "surgenetdino_hf_api_blobs"),
               Q('"gated":false', "surgenetdino_hf_api_blobs")],
}
REC["domain"] = {
    "value": "frames (1 fps) of laparoscopic and robot-assisted surgery videos (public, private and YouTube)",
    "quotes": [Q("we extract 680 hours of surgical video footage from YouTube, sampled at 1 frame per second (fps).", "surgenetxl_arxiv_pdf"),
               Q("The dataset consists of frames sampled from videos at 1 fps, with black borders removed to standardize the dataset.", "surgenetxl_arxiv_pdf")],
}
REC["pretraining_data_quote"] = {
    "summary": REC["pretraining_data"]["summary"],
    "datasets": REC["pretraining_data"]["datasets"],
    "quotes": REC["pretraining_data"]["quotes"][:7] + [
        Q(_YT, "surgenet_github_readme"),
        Q("| **SurgeNetXL** | All of the above | All of the above | \\>4598 | 4,711,024 | Partly |", "surgenet_github_readme"),
        Q("Following the pipeline described in Schmidgall et al. (2024), we extract 680 hours of surgical video footage from YouTube, sampled at 1 frame per second (fps).", "surgenetxl_arxiv_pdf"),
        Q("We initiate pretraining from ImageNet-initialized weights as recommended by Ramesh et al. (2023)", "surgenetxl_arxiv_pdf")],
}
REC["appendix300_check"] = A300(
    "UNKNOWN", _YT, True,
    "The YouTube portion (3,253 videos, 2,074,234 frames; derived with the GSViT/Schmidgall pipeline) contains an explicit appendectomy subset "
    "(appendectomy/yt_appendectomy_Batch0-6.zip) whose recording hospitals are undocumented -> cannot be excluded. Separately, DSAD (in the "
    "data) is from University Hospital Carl Gustav Carus Dresden (an Appendix300 centre) but is robot-assisted rectal surgery, not appendectomy. "
    "Private sets RAMIE-UMCU (Utrecht esophagectomy) and RARP-AvL (prostatectomy) are identified and are not appendectomy. The GSViT "
    "appendectomy URL list (98 URLs; see GSViT entry) showed no Dresden-area channel, but the SurgeNet YouTube file list itself is gated "
    "and its URL list was not inspected.",
    [Q('"rfilename":"appendectomy/yt_appendectomy_Batch0.zip"', "surgenetyt_hf_dataset_api"),
     Q('"gated":"auto"', "surgenetyt_hf_dataset_api"),
     Q("| **Others** | DSAD ([Carstens et al., 2023](https://www.nature.com/articles/s41597-022-01719-2)) | RA Rectal Resection/Extirpation | 32 | 14,623 | Yes |", "surgenet_github_readme"),
     Q("video data from a total of 32 robot-assisted anterior rectal resections or rectal extirpations performed at the University Hospital Carl Gustav Carus Dresden was gathered", "dsad_scidata")])
REC["input"] = {
    "frame_size": "CAFormer-S18 pretraining input size 224 (DINO); downstream fine-tuning frames 224x399; DINO ViTs 224 (v1) or 336 (v2/v3) per file names",
    "frame_rate_or_sampling": "single frames; source videos sampled at 1 fps (YouTube and RAMIE explicitly)",
    "clip_length_frames": "1 (frame encoders; no temporal input)",
    "notes": "Pretraining hyperparameter table (paper appendix) gives Input size 224.",
    "quotes": [Q("Hyperparameter Input size Optimizer Gradient clip LR decay schedule Train epochs Train batch size learning rate Warming-up epochs Weight decay Mixed precision Value 224", "surgenetxl_arxiv_pdf"),
               Q("Input frames are resized to a resolution of 224×399 pixels using bicubic interpolation.", "surgenetxl_arxiv_pdf"),
               Q("sampled at 1 frame per second (fps)", "surgenetxl_arxiv_pdf"),
               Q("DINOv1_ViTs16_size224_SurgeNetXL.pth", "surgenetdino_hf_api_blobs"),
               Q("DINOv2_ViTs14_size336_SurgeNetXL.pth", "surgenetdino_hf_api_blobs")],
}
REC["embedding_dim"] = {
    "value": "512 (CAFormer-S18 final-stage channels; multi-scale stages 64/128/320/512). DINO ViTs: not stated in the sources (standard ViT-S/B/L widths 384/768/1024 - architecture convention, unverified here)",
    "basis": "caformer_s18 definition in the SurgeNet repository (dims of the four stages)",
    "quotes": [Q("def caformer_s18(num_classes=0, pretrained='ImageNet', pretrained_weights=None, **kwargs):", "surgenet_metaformer_py"),
               Q("depths=[3, 3, 9, 3], dims=[64, 128, 320, 512],", "surgenet_metaformer_py")],
}
REC["params"] = {
    "value": "CAFormer-S18 24.3M; SurgeNetDINO segmentation models (encoder + head) ViT-S 23M, ViT-B 90-92M, ViT-L 311-314M",
    "quotes": [Q("Backbone CaFormerS18 Number of parameters 24.3M", "surgenetxl_arxiv_pdf"),
               Q("(parameters of the segmentation models)", "surgenetdino_github_readme"),
               Q("<th>Params (M)</th>", "surgenetdino_github_readme"),
               Q('<td rowspan="2">311</td>', "surgenetdino_github_readme"),
               Q('<td rowspan="2">314</td>', "surgenetdino_github_readme")],
}
REC["flops_per_input_if_documented"] = {
    "value": None,
    "statement": "FLOPs not documented (searched 'FLOP', 'MAC' in paper and READMEs). SurgeNetDINO reports throughput instead: segmentation/phase FPS on one NVIDIA H100 (e.g. ViT-L v2: 123 seg FPS, 35 phase FPS).",
    "quotes": [Q("online inference efficiency on a single NVIDIA H100 GPU", "surgenetdino_github_readme"),
               Q('<td rowspan="2">123</td><td rowspan="2">35</td>', "surgenetdino_github_readme")],
}
REC["eligibility"] = elig(
    C("PASS", "HF repos list the SurgeNetXL and SurgeNetDINO .pth files publicly, gated=false (API metadata only)."),
    C("PASS", "Weights CC BY-NC-SA 4.0 (README / LICENSE_MODELS.txt; HF metadata cc-by-nc-4.0): non-commercial research use permitted."),
    C("PASS", "DINO self-supervised pretraining on 4.7M frames sampled at 1 fps from surgical videos (ImageNet-1k initialisation)."),
    C("PASS", "All public and private datasets named; the YouTube set is named with counts and a published (gated) dataset."),
    "Non-commercial weights licence. Appendix300 contamination UNKNOWN because of the YouTube appendectomy subset.")
REC["changes_vs_previous"] = [
    "No factual corrections. Added: CAFormer-S18 embedding dimension 512 (from metaformer.py), pretraining input size 224 (paper appendix), "
    "repo versions (HF sha/lastModified), YouTube dataset gating flag (gated=auto) and the GSViT-pipeline provenance of the YouTube data.",
    "Extra source surgenetyt_hf_dataset_readme dropped (HTTP 401 at re-fetch: the dataset README is behind the gate; it was not quoted).",
    "Saved copies moved from /media/user/LaCie/... to fm_sources/primary/ and all quotes re-verified there.",
]
