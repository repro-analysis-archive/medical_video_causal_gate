"""GSViT (old entry 6; legacy fields kept, new structured fields added)."""
import copy

from fm_primary_records import RECORDS as _OLD
from ._common import A300, C, NOFLOPS, Q, elig

REC = copy.deepcopy(_OLD[5])
assert REC["name"].startswith("GSViT")
REC["legacy_eligibility_first_pass"] = REC.pop("eligibility")
# correction of the first-pass input note (see changes_vs_previous)
REC["architecture"]["input"] = ("single frames (next-frame prediction, 1 frame input -> frame 1 s later); resolution not stated in the paper; "
                                "the pretraining script's placeholder batch is 3x224x224 and the decoder reshape 384*4*4 is consistent with it")
REC["architecture"]["quotes"].append(Q("images = torch.rand(1, 3, 224, 224).repeat(in_size*num_devices, 1, 1, 1)", "gsvit_pretrain_model"))

REC["version"] = {
    "value": "GSViT.pkl (Documents/GSViT_Models on Johns Hopkins OneDrive); no GitHub releases; paper arXiv 2403.05949v3; procedure-specific fine-tunes announced 'ASAP' (not released in the checked folder link)",
    "basis": "README download sentence and the resolved OneDrive viewer URL naming GSViT.pkl",
    "quotes": [Q("GSViT_Models%2FGSViT.pkl", "gsvit_weights_sharepoint_check"),
               Q("Procedure-specific fine-tuned models to be released in the same folder ASAP.", "gsvit_github_readme"),
               Q("[v3] Fri, 12 Apr 2024 22:30:54 UTC", "gsvit_arxiv_abs")],
}
REC["weights_location"] = {
    "url": "https://livejohnshopkins-my.sharepoint.com/:u:/g/personal/sschmi46_jh_edu/ERwRJGVUHRtKqvnSabuyKPgBfM8Hhe_Ks0EPTXg97nZ1Qw?e=hh02un",
    "exists": "YES - the share link resolves (HTTP 200, no login redirect) to the OneDrive viewer for Documents/GSViT_Models/GSViT.pkl (not downloaded)",
    "access": "public anonymous share link",
    "verification": "HEAD/GET linkcheck (HTML title only), 2026-10-02",
    "quotes": [Q('"status": 200', "gsvit_weights_sharepoint_check"), Q("GSViT_Models%2FGSViT.pkl", "gsvit_weights_sharepoint_check"),
               Q("Please download the GSViT model from here: https://livejohnshopkins-my.sharepoint.com/:u:/g/personal/sschmi46_jh_edu/ERwRJGVUHRtKqvnSabuyKPgBfM8Hhe_Ks0EPTXg97nZ1Qw?e=hh02un", "gsvit_github_readme")],
}
REC["licence"]["quotes"] = REC["licence"]["quotes"] + [Q('"status": 404', "gsvit_license_404_check")]
REC["domain"] = {
    "value": "laparoscopic and robotic general-surgery video from YouTube (frame-to-next-frame prediction)",
    "quotes": [Q("we open-source the largest dataset of general surgery videos to-date, consisting of 680 hours of surgical videos, including data from robotic and laparoscopic techniques across 28 procedures", "gsvit_arxiv_pdf")],
}
REC["pretraining_data_quote"] = {
    "summary": REC["pretraining_data"]["summary"],
    "datasets": REC["pretraining_data"]["datasets"],
    "quotes": [Q("we open-source the largest dataset of general surgery videos to-date, consisting of 680 hours of surgical videos, including data from robotic and laparoscopic techniques across 28 procedures", "gsvit_arxiv_pdf"),
               Q("For the data collection process, a selection of videos was curated from specific playlists of surgical demonstrations on YouTube using surgery related keywords.", "gsvit_arxiv_pdf"),
               Q("https://youtu.be/x8sUeH5M5Q0", "gsvit_videos_appendectomy"),
               Q("self.evit = EfficientViT_M5(pretrained='efficientvit_m5')", "gsvit_load_gsvit")],
}
REC["appendix300_check"] = A300(
    "UNKNOWN",
    "For the data collection process, a selection of videos was curated from specific playlists of surgical demonstrations on YouTube using surgery related keywords.",
    True,
    "Entirely YouTube-derived (GenSurgery, 680 h, 28 procedures) with an explicit appendectomy URL list (98 URLs). oEmbed metadata of those 98 "
    "(titles/channels only, re-checked 2026-10-02): channels Dr. Daniel A. Popowich (40), IgorTFerreira (29), Dr Tayyab Riaz Ch (24), ashwin "
    "thangavelu (3), Colorectal Disease Journal (1), Dr. R. K. Mishra (1); no title/channel mentions Dresden, Radeberg, Ravensburg, Asklepios, "
    "Elisabethen, Diakonissen, Friedrichstadt, Joseph, Carus or Germany. The unsorted.txt list and the hospital of origin of each upload "
    "(re-uploads) are undocumented, so Appendix300 source recordings cannot be excluded.",
    [Q('"author_name": "Dr. Daniel A. Popowich @ Minimally Invasive Surgeon"', "gsvit_appendectomy_oembed"),
     Q('"n_urls": 98', "gsvit_appendectomy_oembed"),
     Q("https://youtu.be/4CoA4bUl7G0", "gsvit_videos_appendectomy")])
REC["input"] = {
    "frame_size": "not stated in the paper; pretraining script placeholder input 3x224x224 (decoder from a 384x4x4 encoder map back to an image)",
    "frame_rate_or_sampling": "frame pairs 1 s apart: 1 input frame -> prediction of the frame 1 s later",
    "clip_length_frames": "1 input frame (single-frame encoder; next-frame target)",
    "notes": "BGR channel flip in the official loader (process_inputs)",
    "quotes": [Q("performing next-frame reconstruction for pre-training with a 1 frame input and a 1 second prediction (1 frame).", "gsvit_arxiv_pdf"),
               Q("images = torch.rand(1, 3, 224, 224).repeat(in_size*num_devices, 1, 1, 1)", "gsvit_pretrain_model"),
               Q("x = process_inputs(x) # flip color channels", "gsvit_load_gsvit")],
}
REC["embedding_dim"] = {"value": "384 channels x 4 x 4 spatial (6,144 flattened) EfficientViT-M5 output map, as consumed by the decoder",
                        "basis": "decoder input layer in pretrain_model.py; not stated in the paper",
                        "quotes": [Q("self.fc = nn.Linear(384*4*4, 7 * 7 * 1024)", "gsvit_pretrain_model")]}
REC["params"] = {"value": "12.4M (foundation-model encoder, per paper; SurgeNetXL paper lists 12.1M for GSViT EfficientViT-M5)",
                 "quotes": [Q("an additional 12.4M non-tuneable parameters for the foundation model", "gsvit_arxiv_pdf"),
                            Q("C4 GSViT EfficientViT-M5 12.1M", "surgenetxl_arxiv_pdf")]}
REC["flops_per_input_if_documented"] = NOFLOPS("'FLOP', 'GFLOP' in paper PDF and repository files")
REC["eligibility"] = elig(
    C("PASS", "Official OneDrive share link resolves anonymously to GSViT.pkl (viewer page; not downloaded)."),
    C("UNKNOWN", "No licence for code or weights: no LICENSE file (raw LICENSE 404), GitHub licence field null, no statement in README/paper beyond 'open-source'."),
    C("PASS", "Self-supervised next-frame prediction on 680 h of laparoscopic/robotic surgery video."),
    C("PASS", "Pretraining source documented as YouTube with per-procedure URL lists published in the repository."),
    "Eligibility UNKNOWN solely because research-use permission is not established by any licence text.")
REC["changes_vs_previous"] = [
    "architecture.input CORRECTED: the first pass inferred '256x256 for EfficientViT-M5 - inference, unverified'; the pretraining script's placeholder input is 3x224x224 (now quoted); the paper states no resolution.",
    "Added licence evidence: raw LICENSE returns 404 (gsvit_license_404_check). oEmbed check of the 98 appendectomy URLs re-run 2026-10-02 with identical channel counts.",
    "Saved copies moved from /media/user/LaCie/... to fm_sources/primary/ and all quotes re-verified there.",
]
