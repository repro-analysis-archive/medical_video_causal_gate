"""SurgVLP / HecVL / PeskaVLP (old entry 7; legacy fields kept, new structured fields added)."""
import copy

from fm_primary_records import RECORDS as _OLD
from ._common import A300, C, NOFLOPS, Q, elig

REC = copy.deepcopy(_OLD[6])
assert REC["name"].startswith("SurgVLP")
REC["legacy_eligibility_first_pass"] = REC.pop("eligibility")
# first-pass weights quotes contained per-request download tokens that change on every request -> replaced
REC["weights"]["quotes"] = [Q("- SurgVLP [1]: https://seafile.unistra.fr/f/93757ace1bfc47248e1e/?dl=1", "surgvlp_github_readme"),
                            Q('"content_length": "495063240"', "surgvlp_weights_check"),
                            Q('"content_length": "495069659"', "hecvl_weights_check"),
                            Q('"content_length": "495071118"', "peskavlp_weights_check")]
# first-pass truncated quote "In total, we collect 1, 326 le" -> full sentence
REC["pretraining_data"]["quotes"] = [q for q in REC["pretraining_data"]["quotes"] if q["quote"] != "In total, we collect 1, 326 le"] + [
    Q("In total, we collect 1, 326 lectures for the pre-training set.", "surgvlp_arxiv_pdf")]

_APP = "They cover the five main categories, “Hepatobiliary and pancreatic surgery”, “General and digestive surgery”, “Bariatric surgery”, “Hernia surgery” and “Colorectal, transanal and proctological surgery”."

REC["version"] = {
    "value": "SurgVLP.zip, HecVL.zip, PeskaVLP.zip (seafile.unistra.fr; ~495 MB each); loaded via the surgvlp package with tests/config_{surgvlp,hecvl,peskavlp}.py; README recommends PeskaVLP; no versioned release",
    "basis": "README weight links and Content-Disposition file names from HEAD requests",
    "quotes": [Q("We recommend using the best version, PeskaVLP, for your study.", "surgvlp_github_readme"),
               Q("filename*=\\\"utf-8' 'SurgVLP.zip\\\"", "surgvlp_weights_check"),
               Q("filename*=\\\"utf-8' 'HecVL.zip\\\"", "hecvl_weights_check"),
               Q("filename*=\\\"utf-8' 'PeskaVLP.zip\\\"", "peskavlp_weights_check")],
}
REC["weights_location"] = {
    "url": "https://seafile.unistra.fr/f/93757ace1bfc47248e1e/?dl=1 (SurgVLP); https://seafile.unistra.fr/f/3b9b9207068a4b03bc2a/?dl=1 (HecVL); https://seafile.unistra.fr/f/65a2b1bf113e428280d0/?dl=1 (PeskaVLP)",
    "exists": "YES - HEAD requests resolve (HTTP 200, application/zip) to SurgVLP.zip 495,063,240 B, HecVL.zip 495,069,659 B, PeskaVLP.zip 495,071,118 B (not downloaded)",
    "access": "public link, no login",
    "verification": "HEAD linkcheck (headers only), 2026-10-02",
    "quotes": [Q('"status": 200', "surgvlp_weights_check"), Q('"content_type": "application/zip"', "surgvlp_weights_check"),
               Q('"content_length": "495063240"', "surgvlp_weights_check"),
               Q('"content_length": "495069659"', "hecvl_weights_check"),
               Q('"content_length": "495071118"', "peskavlp_weights_check")],
}
REC["domain"] = {
    "value": "surgical video lectures (laparoscopic/robotic surgery video with narration) - video-language pretraining",
    "quotes": [Q("we query the videos based on keywords from three online platforms, i.e., Websurg (Websurg, 2023), EAES (EAES, 2023), and YouTube (YouTube, 2023).", "surgvlp_arxiv_pdf"),
               Q("Pretraining dataset: we use the surgical lecture videos from the Surgical Video Lecture dataset (SVL) for the pretraining, which was proposed by the SurgVLP [22].", "hecvl_arxiv_pdf")],
}
REC["pretraining_data_quote"] = {
    "summary": REC["pretraining_data"]["summary"],
    "datasets": REC["pretraining_data"]["datasets"],
    "quotes": REC["pretraining_data"]["quotes"],
}
REC["appendix300_check"] = A300(
    "UNKNOWN", _APP, True,
    "Pretraining videos are keyword-crawled lectures (WebSurg 1,124 via 'intervention'/'laparoscopic'; EAES + YouTube 202); no per-video list or "
    "originating hospitals are published, and the 'General and digestive surgery' category can contain laparoscopic appendectomy lectures. "
    "Whether any recording from an Appendix300 centre is among them cannot be decided (web-platform data).",
    [Q(_APP, "surgvlp_arxiv_pdf"),
     Q("For EAES and YouTube, we manually collect 202 surgical video lectures using manually designed keywords.", "surgvlp_arxiv_pdf")])
REC["input"] = {
    "frame_size": "frames resized to 360x640 then centre-cropped to 224x224",
    "frame_rate_or_sampling": "frames sampled uniformly within each clip (clip boundaries from ASR sentence timestamps; variable clip length)",
    "clip_length_frames": "SurgVLP: T = 4 frames per clip; HecVL: 4 / 8 / 32 frames (clip / phase / video level); PeskaVLP: 4 / 16 / 64 frames",
    "notes": "per-frame ResNet-50 embeddings average-pooled over time into one clip vector",
    "quotes": [Q("transforms.Resize((360, 640)), transforms.CenterCrop(224),", "surgvlp_config_peskavlp"),
               Q("We uniformly sample T = 4 frames for each video clip.", "surgvlp_arxiv_pdf"),
               Q("We sample 4, 8, and 32 frames for each clip-level, phase-level, and video-level", "hecvl_arxiv_pdf"),
               Q("We sample 4/16/64 frames for videos of clip/phase-/video-level.", "peskavlp_arxiv_pdf")],
}
REC["embedding_dim"] = {"value": 768, "basis": "joint video/text embedding dimension d (visual ResNet-50 projected to 768)",
                        "quotes": [Q("Finally, we obtain a d = 768 dimensional vector for each video clip.", "surgvlp_arxiv_pdf"),
                                   Q("num_classes=768,", "surgvlp_config_peskavlp")]}
REC["params"] = {"value": "not stated as a total; text encoder BioClinicalBERT 110M (stated); visual ResNet-50 count not stated (standard ~25M, outside figure); each weight zip ~495 MB",
                 "quotes": [Q("containing 12 encoders with 12 bidirectional self-attention heads totaling 110 million parameters.", "surgvlp_arxiv_pdf")]}
REC["flops_per_input_if_documented"] = NOFLOPS("'FLOP' in SurgVLP, HecVL and PeskaVLP PDFs and README")
REC["eligibility"] = elig(
    C("PASS", "Official seafile.unistra.fr links resolve to the three weight zips without login (HEAD only)."),
    C("PASS", "README: code and models 'available for non-commercial scientific research purposes' under CC BY-NC-SA 4.0."),
    C("PASS", "Contrastive video-language pretraining on surgical video lectures (frames of laparoscopic/robotic surgery videos)."),
    C("PASS", "Sources named (WebSurg, EAES, YouTube) with counts and query keywords; no per-video list."),
    "Documented at platform level, not per video. Visual encoder is frame-level ResNet-50 (temporal average pooling).")
REC["changes_vs_previous"] = [
    "weights quotes CORRECTED: the first pass quoted per-request seafile download URLs (token in path) that change on every request and cannot be re-verified; replaced by the stable Content-Length values.",
    "pretraining_data quote CORRECTED: truncated quote 'In total, we collect 1, 326 le' replaced by the full sentence.",
    "Added SurgVLP T=4 frames per clip and d=768, HecVL 4/8/32 and PeskaVLP 4/16/64 frame counts, BioClinicalBERT 110M.",
    "Saved copies moved from /media/user/LaCie/... to fm_sources/primary/ and all quotes re-verified there.",
]
