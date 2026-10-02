"""EndoFM-LV (old entry 2; legacy fields kept, new structured fields added)."""
import copy

from fm_primary_records import RECORDS as _OLD
from ._common import A300, C, NOFLOPS, Q, elig

REC = copy.deepcopy(_OLD[1])
assert REC["name"] == "EndoFM-LV"
REC["legacy_eligibility_first_pass"] = REC.pop("eligibility")
REC["extra_sources"] = [s for s in REC.get("extra_sources", []) if s != "endofmlv_ieee_doi"] + ["endofmlv_train_ssl"]

REC["version"] = {
    "value": "single pretrained checkpoint linked in README 'Pre-trained Weights' (CUHK SharePoint, file name not visible); no release/tag; paper JBHI 29(5) 2025",
    "basis": "README section and JBHI citation; the link is dead, so no checkpoint file name could be read.",
    "quotes": [Q("#### Pre-trained Weights You can directly download our pre-trained Endo-FM via this [link](https://mycuhk-my.sharepoint.com/:u:/g/personal/1155167044_link_cuhk_edu_hk/EauTiGd9hg9Lu_7JED3v1E0BwCZ2ZQTsdBfiFo58ADtrmg?e=AZAsP4)", "endofmlv_github_readme"),
               Q("IEEE J Biomed Health Inform. 2025 May;29(5):3526-3536.", "endofmlv_pubmed_efetch")],
}
REC["weights_location"] = {
    "url": "https://mycuhk-my.sharepoint.com/:u:/g/personal/1155167044_link_cuhk_edu_hk/EauTiGd9hg9Lu_7JED3v1E0BwCZ2ZQTsdBfiFo58ADtrmg?e=AZAsP4",
    "exists": "NO - HTTP 404 at re-check 2026-10-02; GitHub issue #5 'Model download links return 404' (opened 2026-07-28) is open with 0 comments; Hugging Face model search for 'EndoFM' returns no repository",
    "access": "dead link",
    "verification": "HEAD/GET linkcheck of the SharePoint link; GitHub issue JSON; HF API search listing",
    "quotes": [Q('"status": 404', "endofmlv_weights_sharepoint_check"),
               Q("The model download links provided in the repository are not working. When I try to access them, I receive a 404 File Not Found error.", "endofmlv_issue5"),
               Q('"comments":0', "endofmlv_issue5"), Q('"state":"open"', "endofmlv_issue5"), Q("[]", "endofmlv_hf_search")],
}
REC["domain"] = {
    "value": "long endoscopy video (minute-level sequences; README figure: colonoscopy, gastroscopy)",
    "quotes": [Q("we propose EndoFM-LV, a foundation model developed under a minute-level pre-training framework upon long endoscopy video sequences.", "endofmlv_pubmed_efetch")],
}
REC["pretraining_data_quote"] = {
    "summary": REC["pretraining_data"]["summary"],
    "datasets": REC["pretraining_data"]["datasets"],
    "quotes": [Q("We utilize 4 public and 1 private datasets for pre-training and 4 datasets as the downstream tasks.", "endofmlv_github_readme"),
               Q("For pre-training, we construct a large-scale long endoscopy video dataset comprising 6,469 long endoscopic video samples, each longer than 1 minute and totaling over 13 million frames.", "endofmlv_pubmed_efetch")],
}
REC["appendix300_check"] = A300(
    "UNKNOWN",
    "the documented data list does not mention DS203/Appendix300 (accessible documentation does not name the 4 public datasets or the private source)",
    False,
    "4 unnamed public datasets + 1 undisclosed private dataset (data-prep script folders private2/, private_new/, private_batch3/); full JBHI text closed access. "
    "The README figure states colonoscopy/gastroscopy (makes laparoscopic appendectomy unlikely) but the private/in-house data cannot be excluded from the documentation.",
    [Q("videolist = glob.glob(f'{datadir}/private2/*.mp4')", "endofmlv_data_gencsv")])
REC["input"] = {
    "frame_size": "224x224 crop (TimeSformer config TimeSformer_divST_8x32_224.yaml: TRAIN_CROP_SIZE 224); pretraining resolution not stated in accessible text",
    "frame_rate_or_sampling": "not stated for EndoFM-LV pretraining (base config SAMPLING_RATE 32 is the Kinetics TimeSformer default, overridden settings not documented)",
    "clip_length_frames": "32 frames per sequence in the released pretraining script (DATA.NUM_FRAMES 32, overriding the config's 8); sequences are > 1 min long",
    "notes": "Config is the Kinetics TimeSformer template used as default --cfg by train_ssl.py; values are those of the code, not of the paper (closed access).",
    "quotes": [Q('default="models/configs/Kinetics/TimeSformer_divST_8x32_224.yaml"', "endofmlv_train_ssl"),
               Q("TRAIN_CROP_SIZE: 224", "endofmlv_config_yaml"),
               Q("SAMPLING_RATE: 32", "endofmlv_config_yaml"),
               Q("DATA.NUM_FRAMES 32", "endofmlv_scripts_train"),
               Q("MODEL_NAME: vit_base_patch16_224", "endofmlv_config_yaml")],
}
REC["embedding_dim"] = {"value": None,
                        "basis": "not stated in accessible sources; the config model name vit_base_patch16_224 implies ViT-B (768) but this is an inference, not a documented value",
                        "quotes": [Q("MODEL_NAME: vit_base_patch16_224", "endofmlv_config_yaml")]}
REC["params"] = {"value": "not stated in accessible sources (ViT-B/16 TimeSformer per config; count not documented)",
                 "quotes": [Q('--arch "timesformer"', "endofmlv_scripts_train")]}
REC["flops_per_input_if_documented"] = NOFLOPS("README, PubMed abstract, scripts/config; JBHI full text not accessible")
REC["eligibility"] = elig(
    C("FAIL", "The only pretrained-weights link returns HTTP 404 (re-checked 2026-10-02); open issue #5 unanswered; no mirror found on Hugging Face."),
    C("PASS", "README: 'This project is under the Apache License 2.0 license.'"),
    C("PASS", "Self-supervised pretraining on long endoscopy videos (6,469 videos > 1 min)."),
    C("UNKNOWN", "Accessible documentation gives only '4 public and 1 private datasets' without names; the closed-access JBHI paper may name them (not verifiable)."),
    "Fails open weights at check time.")
REC["changes_vs_previous"] = [
    "Unchanged findings; weights link re-checked 2026-10-02 (still 404); issue #5 still open with 0 comments; HF search for 'EndoFM' added (no copies).",
    "Input field now quotes the default TimeSformer config (224 crop) used by train_ssl.py in addition to NUM_FRAMES 32.",
    "Extra source endofmlv_ieee_doi dropped (IEEE returned HTTP 202 with an empty body at re-fetch; it was not quoted).",
    "Saved copies moved from /media/user/LaCie/... to fm_sources/primary/ and all quotes re-verified there.",
]
