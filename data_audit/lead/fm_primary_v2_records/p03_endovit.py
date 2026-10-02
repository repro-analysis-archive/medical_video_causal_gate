"""EndoViT (old entry 3; legacy fields kept, new structured fields added)."""
import copy

from fm_primary_records import RECORDS as _OLD
from ._common import A300, C, NOFLOPS, Q, elig

REC = copy.deepcopy(_OLD[2])
assert REC["name"] == "EndoViT"
REC["legacy_eligibility_first_pass"] = REC.pop("eligibility")

_DSAD = "video data from a total of 32 robot-assisted anterior rectal resections or rectal extirpations performed at the University Hospital Carl Gustav Carus Dresden was gathered"

REC["version"] = {
    "value": "HF egeozsoy/EndoViT pytorch_model.bin (repo sha 984187302377a398b77b37c11183eafe2a30546a, lastModified 2024-04-11); GitHub Google-Drive variants EndoViT_Seg / EndoViT ATD / EndoViT_SPR (each excludes one downstream test set); no GitHub releases/tags",
    "basis": "HF API listing (sha, lastModified, siblings) and README checkpoint table.",
    "quotes": [Q('"sha":"984187302377a398b77b37c11183eafe2a30546a","lastModified":"2024-04-11T07:56:33.000Z"', "endovit_hf_api_blobs"),
               Q("To prevent data leakage for our evaluation, we excluded the test set for backbone training of our segmentation, action triplet recognition, and surgical phase recognition tasks, respectively.", "endovit_github_readme"),
               Q("There aren’t any releases here", "endovit_github_tags")],
}
REC["weights_location"] = {
    "url": "https://huggingface.co/egeozsoy/EndoViT (pytorch_model.bin); Drive variants via https://github.com/DominikBatic/EndoViT#pre-trained-endovit-checkpoints",
    "exists": "YES - HF API lists pytorch_model.bin (1,341,188,699 B, LFS sha256 ec41888f...), private=false, gated=false (not downloaded)",
    "access": "public, not gated",
    "verification": "HF API model listing with ?blobs=true, 2026-10-02",
    "quotes": [Q('"rfilename":"pytorch_model.bin","blobId":"003e961b635141dd163fd12e15550d18c908d60e","size":1341188699', "endovit_hf_api_blobs"),
               Q('"private":false', "endovit_hf_api_blobs"), Q('"gated":false', "endovit_hf_api_blobs")],
}
REC["domain"] = {
    "value": "frames (1 FPS) of minimally invasive surgery videos (laparoscopic and robot-assisted)",
    "quotes": [Q("Endo700k contains a diverse set of endoscopic procedures, both manual and robot-assisted, with several surgery types such as prostatectomy, cholecystectomy, gastrectomy, proctocolectomy, rectal resection, and sigmoid resection.", "endovit_pmc_fulltext"),
               Q("For consistency, we always downsample to 1 FPS.", "endovit_pmc_fulltext")],
}
REC["pretraining_data_quote"] = {
    "summary": REC["pretraining_data"]["summary"],
    "datasets": REC["pretraining_data"]["datasets"],
    "quotes": [Q("we introduce Endo700k, a collection of 9 publicly available endoscopic datasets comprising more than 700,000 unlabelled images.", "endovit_github_readme"),
               REC["pretraining_data"]["quotes"][1],
               Q("Outside the previously mentioned exceptions, we use all of the images from the nine datasets.", "endovit_pmc_fulltext"),
               Q("Consequently, our pre-training uses ImageNet weights as a starting point.", "endovit_github_readme")],
}
REC["appendix300_check"] = A300(
    "NO", _DSAD, True,
    "Closed list of 9 named public datasets (+ ImageNet MAE initialisation); none contains appendectomy recordings. One dataset, DSAD, comes from "
    "University Hospital Carl Gustav Carus Dresden (an Appendix300 centre) but consists of 32 robot-assisted rectal resections/extirpations "
    "(Feb 2019-Feb 2021), not appendectomies - same-institution overlap, not Appendix300 data. No YouTube, private or in-house data.",
    [Q(_DSAD, "dsad_scidata"),
     Q("Between February 2019 and February 2021, video data from a total of 32 robot-assisted anterior rectal resections or rectal extirpations performed at the University Hospital Carl Gustav Carus Dresden", "dsad_scidata")])
REC["input"] = {
    "frame_size": "224x224 (pretraining resolution); fine-tuning also at 256x448 ('High Res')",
    "frame_rate_or_sampling": "single images; Endo700k frames extracted at 1 FPS from the source videos",
    "clip_length_frames": "1 (image encoder; no temporal input)",
    "notes": "MAE ViT-B/16; HF feature-extraction example resizes images to input_size=224 with Endo700k mean/std",
    "quotes": [Q("The results are reported both for EndoViT’s pretraining resolution of 224 x 224 (Low Res) and the resolution used in [ 24 ] of 256 x 448 (High Res).", "endovit_pmc_fulltext"),
               Q("Endo700k images were extracted at 1 FPS.", "endovit_github_readme"),
               Q("def process_single_image(image_path, input_size=224, dataset_mean=[0.3464, 0.2280, 0.2228], dataset_std=[0.2520, 0.2128, 0.2093]):", "endovit_hf_readme")],
}
REC["embedding_dim"] = {"value": 768, "basis": "ViT-B token dimension in the official HF loading code",
                        "quotes": [Q("VisionTransformer(patch_size=16, embed_dim=768, depth=12, num_heads=12, mlp_ratio=4", "endovit_hf_readme")]}
REC["params"] = {"value": "85.8M (ViT-Base; third-party figure from the SurgeNetXL paper Table 3 - not stated by the EndoViT authors). Note: the HF checkpoint file is 1.34 GB, larger than fp32 encoder-only ViT-B weights; its content (e.g. MAE decoder/optimizer state) was not inspected.",
                 "quotes": [Q("C5 EndoViT ViT-Base 85.8M", "surgenetxl_arxiv_pdf")]}
REC["flops_per_input_if_documented"] = NOFLOPS("'FLOP' in PMC full text, GitHub README, HF card")
REC["eligibility"] = elig(
    C("PASS", "HF repo egeozsoy/EndoViT lists pytorch_model.bin publicly, gated=false (API metadata only)."),
    C("PASS", "HF model card metadata 'license: apache-2.0' (GitHub code repo declares no licence)."),
    C("PASS", "MAE pretraining on Endo700k, frames sampled at 1 FPS from 9 public minimally invasive surgery video datasets."),
    C("PASS", "All 9 pretraining datasets named with procedure types and frame counts (Table 1)."),
    "Frame-level (image) encoder. Same-institution overlap with Appendix300 (Carus Dresden, via DSAD rectal surgery) to be disclosed.")
REC["changes_vs_previous"] = [
    "params: first pass gave '~86M (standard ViT-B figure; count not stated in the sources)'; now quoted as 85.8M from SurgeNetXL Table 3 (third-party) and the 1.34 GB checkpoint-size caveat added.",
    "Saved copies moved from /media/user/LaCie/... to fm_sources/primary/ and all quotes re-verified there.",
]
