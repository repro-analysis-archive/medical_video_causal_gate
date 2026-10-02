"""SurgeNet / SurgeNetPublic / procedure-specific variants without YouTube data (old entry 5)."""
import copy

from fm_primary_records import RECORDS as _OLD
from ._common import A300, C, NOFLOPS, Q, elig

REC = copy.deepcopy(_OLD[4])
assert REC["name"].startswith("SurgeNet / SurgeNetPublic")
REC["legacy_eligibility_first_pass"] = REC.pop("eligibility")

REC["version"] = {
    "value": "HF TimJaspersTue/SurgeNetModels (sha cc21f4a1..., lastModified 2026-03-04): SurgeNet_checkpoint_epoch0050_teacher.pth, Public_checkpoint_epoch0050_teacher.pth, "
             "CHOLEC_/RAMIE_/RARP_checkpoint_epoch0050_teacher.pth, SurgeNetSmall_..., SurgeNet_ConvNextv2_..._teacher.pth, SurgeNet_PVTv2_..._teacher.pth (+ full checkpoints, data-fraction and Laparo/Robot ablation checkpoints)",
    "basis": "HF API listing file names",
    "quotes": [Q('"rfilename":"SurgeNet_checkpoint_epoch0050_teacher.pth"', "surgenet_hf_api_blobs"),
               Q('"rfilename":"Public_checkpoint_epoch0050_teacher.pth"', "surgenet_hf_api_blobs"),
               Q('"rfilename":"SurgeNet_ConvNextv2_checkpoint_epoch0050_teacher.pth"', "surgenet_hf_api_blobs"),
               Q('"rfilename":"SurgeNet_PVTv2_checkpoint_epoch0050_teacher.pth"', "surgenet_hf_api_blobs")],
}
REC["weights_location"] = {
    "url": "https://huggingface.co/TimJaspersTue/SurgeNetModels",
    "exists": "YES - all listed in the HF API (e.g. SurgeNet_checkpoint_epoch0050_teacher.pth 93,022,798 B), gated=false (not downloaded)",
    "access": "public, not gated",
    "verification": "HF API model listing with ?blobs=true, 2026-10-02",
    "quotes": [Q('"rfilename":"SurgeNet_checkpoint_epoch0050_teacher.pth"', "surgenet_hf_api_blobs"), Q('"gated":false', "surgenet_hf_api_blobs")],
}
REC["domain"] = {
    "value": "frames of laparoscopic and robot-assisted surgery videos (public + 2 identified private sets; no YouTube)",
    "quotes": [Q("| **SurgeNet** | All of the above (excluding YouTube) | All of the above (excluding YouTube) | \\>1345 | 2,636,790 | Partly |", "surgenet_github_readme"),
               Q("The dataset consists of frames sampled from videos at 1 fps, with black borders removed to standardize the dataset.", "surgenetxl_arxiv_pdf")],
}
REC["pretraining_data_quote"] = {
    "summary": REC["pretraining_data"]["summary"],
    "datasets": REC["pretraining_data"]["datasets"],
    "quotes": REC["pretraining_data"]["quotes"],
}
REC["appendix300_check"] = A300(
    "NO", "| **Others** | DSAD ([Carstens et al., 2023](https://www.nature.com/articles/s41597-022-01719-2)) | RA Rectal Resection/Extirpation | 32 | 14,623 | Yes |", True,
    "Closed list of 11 named public datasets + 2 identified private sets (RAMIE-UMCU robot-assisted esophagectomy, Utrecht; RARP-AvL robot-assisted "
    "prostatectomy); no YouTube. No appendectomy data. DSAD is from University Hospital Carl Gustav Carus Dresden (an Appendix300 centre) but is "
    "robot-assisted rectal resection/extirpation - same-institution overlap, not Appendix300 recordings. SurgeNetPublic excludes the private sets.",
    [Q("video data from a total of 32 robot-assisted anterior rectal resections or rectal extirpations performed at the University Hospital Carl Gustav Carus Dresden was gathered", "dsad_scidata"),
     Q("| **SurgeNetPublic** | All public datasets (excluding YouTube & private datasets) | All of the above (excluding YouTube & RA Esophagectomy) | \\>1238 | 1,997,987 | Yes |", "surgenet_github_readme")])
REC["input"] = {
    "frame_size": "pretraining input size 224; downstream 224x399",
    "frame_rate_or_sampling": "single frames sampled from surgical videos (1 fps stated for RAMIE; per-dataset sampling otherwise as released)",
    "clip_length_frames": "1 (frame encoders)",
    "notes": "CAFormer-S18 / ConvNeXtV2-tiny / PVTv2-B2 backbones, DINO",
    "quotes": [Q("Hyperparameter Input size Optimizer Gradient clip LR decay schedule Train epochs Train batch size learning rate Warming-up epochs Weight decay Mixed precision Value 224", "surgenetxl_arxiv_pdf"),
               Q("Input frames are resized to a resolution of 224×399 pixels using bicubic interpolation.", "surgenetxl_arxiv_pdf")],
}
REC["embedding_dim"] = {"value": "512 for CAFormer-S18 (stages 64/128/320/512); ConvNeXtV2-tiny / PVTv2-B2 not stated in saved sources",
                        "basis": "caformer_s18 definition in the SurgeNet repository",
                        "quotes": [Q("depths=[3, 3, 9, 3], dims=[64, 128, 320, 512],", "surgenet_metaformer_py")]}
REC["params"] = {"value": "CAFormer-S18 24.3M (ConvNeXtV2-tiny / PVTv2-B2 counts not stated in the saved sources)",
                 "quotes": [Q("Backbone CaFormerS18 Number of parameters 24.3M", "surgenetxl_arxiv_pdf"),
                            Q("The specific variants of these models are PVTv2-B2, ConvNeXtV2-tiny, and CAFormer-S18.", "surgenetxl_arxiv_pdf")]}
REC["flops_per_input_if_documented"] = NOFLOPS("'FLOP', 'MAC' in SurgeNetXL paper and README")
REC["eligibility"] = elig(
    C("PASS", "HF repo lists the SurgeNet/SurgeNetPublic/procedure checkpoints publicly, gated=false."),
    C("PASS", "Weights CC BY-NC-SA 4.0 (README / LICENSE_MODELS.txt; HF metadata cc-by-nc-4.0): non-commercial research use."),
    C("PASS", "DINO pretraining on frames of surgical videos (ImageNet-1k initialisation)."),
    C("PASS", "All datasets named (public with citations, private by institution and procedure)."),
    "Non-commercial weights licence; SurgeNetPublic uses public data only.")
REC["changes_vs_previous"] = [
    "No factual corrections. Added versions (checkpoint file names), embedding dimension 512 (CAFormer-S18), pretraining input size 224; appendix300 check now quotes the DSAD row (Carus Dresden) explicitly.",
    "Saved copies moved from /media/user/LaCie/... to fm_sources/primary/ and all quotes re-verified there.",
]
