"""Pre-freeze fact task for SS protocol v0.4 (consolidated task Part 2 item 5; final pre-freeze task items 1, 4, 6):
re-determine the eligibility of every 052590c-eligible candidate under the source hierarchy, the clip-level definition,
the mutually exclusive classes and the TWO-LEVEL OVERLAP RULE. NO ranking is applied and NO model is selected.
* Source levels: 1 original paper (incl. a dataset's own paper); 2 official model card / official repository README or
  file listing; 3 documented pretraining-data list (official configs / training scripts); 4 secondary; 5 internal
  tables (052590c, cb07e93). A required fact holds only if a level-1-3 source affirmatively supports it; otherwise it
  is UNK and the candidate is ineligible. Level-4/5 material is shown for context only.
* Two-level overlap rule, per training source of the released weights and of their initialisation / base weights:
  A (direct DS203 / DS203-centre overlap): YES if DS203, a constituent DS203 dataset or a known same-hospital clinical
    source (DSAD) is documented; NO if a level-1-3 source establishes a closed or sufficiently defined corpus whose
    documented scope excludes DS203 and the known DS203 clinical sources (a clinical set with a named non-DS203
    recording site or non-German geography; a versioned non-surgical benchmark with fixed classes finalized before
    DS203's release on 2026-04-29); UNK if open-ended / web-scale or the clinical/site provenance cannot be bounded.
  B (generic web origin): for a fixed closed benchmark, generic web provenance does not change NO to UNK; it is
    disclosed as a limitation ("incidental web-origin exposure cannot be excluded at the level of every source image").
    [v0.4-final3] BOUNDED GENERIC-WEB BENCHMARK OVERRIDE (replaces the v0.4-final2 release-date override): generic
    web provenance alone does not change NO to UNK only for a named, versioned, fixed benchmark whose level-1-3
    documentation provides a sufficiently bounded content scope (a fixed class / task ontology or equivalent closed
    benchmark definition) that permits the DS203 / clinical-overlap concern to be affirmatively excluded. A fixed
    release remains UNK when it is an open-domain or broadly scraped web corpus whose clinical / content / site
    provenance cannot be bounded. Release date alone is not sufficient for NO. The override never overrides A's
    clinical / site-provenance clause. Every benchmark source below carries its ontology quote and the result of a
    term check of its documented class list for clinical / surgical content.
  C (same-hospital): applies to clinical / endoscopic sources only.
  A candidate is eligible on overlap only if every source is NO under A. The strict reading (every web-derived source
  UNK) is reported as a counterfactual only.
* [v0.4-final3, EndoSSL init check] Initialization must be affirmatively stated in a level-1-3 source (pretrained
  checkpoint named, or training from scratch / random initialization); otherwise the initialization is a UNK source and
  the candidate is ineligible. Each eligible model carries its initialization quotes ("init_stated").
* "Fits 24 GB" here is the PRIOR SCREEN (parameter count / checkpoint size); the final determination is the frozen
  synthetic-input feasibility test run after freeze (protocol §4.1).
Every quote is verified as a whitespace-normalised substring of its saved copy."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..")); OUT = os.path.join(H, "out")
FS = os.path.join(H, "fm_sources")
norm = lambda s: re.sub(r"\s+", " ", s).strip()
_c = {}
def level(path):
    b = os.path.basename(path).lower()
    if "label_map_mmaction2" in b or "wayback" in b: return 4
    if any(k in b for k in ("_cfg_", "config", "scripts", ".sh", ".yaml", "reproduce")): return 3
    if any(k in b for k in ("arxiv", "pmc", "scidata", "_pdf", "fulltext", "ucl_pdf", "_abs")): return 1
    return 2
def Q(quote, rel):
    p = rel if os.path.isabs(rel) else os.path.join(FS, rel)
    if p not in _c: _c[p] = norm(open(p, errors="replace").read())
    return dict(quote=quote, copy=os.path.relpath(p, REPO), level=level(p), verified=norm(quote) in _c[p])
prov = {d["name"]: d for d in json.load(open(os.path.join(OUT, "dataset_provenance.json")))["datasets"]}
def PV(name): return [Q(q["quote"], os.path.join(REPO, q["file"])) for q in prov[name]["quotes"] if q.get("kind", "recording_site") == "recording_site"][:2]
P, S, E = "primary/", "secondary/", "eligibility_v04/"
# ---- training sources: status under the two readings ----------------------------------------------------------
NAMED, GEN, GEO, UNK, YES = "A-NO: named non-DS203 recording site", "A-NO: versioned non-surgical benchmark finalized before 2026-04 (B: generic web origin disclosed)", "A-NO: non-German geography", "A-UNK", "A-YES: known same-hospital clinical source"
DS203_RELEASE = Q("\"dc.date.issued\" : [ { \"value\" : \"2026-04-29\"", "/media/user/LaCie/medvideo_gate/DS203/opara_item.json")
SRC = {
 "cholec80": (NAMED, "University Hospital of Strasbourg", PV("Cholec80")),
 "heichole": (NAMED, "Heidelberg University Hospital; Salem Hospital Heidelberg; GRN-hospital Sinsheim", PV("HeiChole")),
 "hsdb_chole": (NAMED, "Cholec80 subset (Strasbourg)", PV("hSDB-instrument")[:1]),
 "esad": (NAMED, "San Raffaele Hospital, Milan", PV("ESAD (SARAS-ESAD)")),
 "psiava": (NAMED, "Fundacion Santa Fe de Bogota", PV("PSI-AVA")),
 "rarp_avl": (NAMED, "Antoni van Leeuwenhoek Hospital, Amsterdam", PV("RARP-AvL (private)")),
 "ramie": (NAMED, "University Medical Center Utrecht", [Q("another containing robot-assisted minimally invasive esophagectomy (RAMIE) procedures from the University Medical Center Utrecht (UMCU)", P + "surgenetxl_arxiv_pdf.txt")]),
 "dsad": (YES, "University Hospital Carl Gustav Carus Dresden (Dept. of Visceral, Thoracic and Vascular Surgery); C2 = Carus Pediatric Surgery", [Q("video data from a total of 32 robot-assisted anterior rectal resections or rectal extirpations performed at the University Hospital Carl Gustav Carus Dresden was gathered", P + "dsad_scidata.txt")]),
 "endossl_init": (UNK, "EndoSSL released-checkpoint initialization: not stated in any level-1-3 source (paper ablations compare starting from scratch and from an ImageNet-1k SSL checkpoint; supplementary Table 4 lists MSN hyper-parameters only)", [Q("In Tab.2e), we look at the effect of the training length when starting from scratch or from a good SSL pretrained checkpoint on ImageNet-1k.", P + "endossl_arxiv_pdf.txt")]),
 "israel8": (GEO, "eight unnamed centres in Israel", [Q("The dataset consists of 7,877 videos recorded at eight different medical centers in Israel.", P + "endossl_arxiv_pdf.txt")]),
 "imagenet": (GEN, "ImageNet (ILSVRC-2012): fixed ontology of 1000 object synsets; medical terms occur only as object classes (stethoscope, syringe, medicine chest), no clinical scene / procedure class", [Q("The 1000 categories used for the image classification task were selected from the ImageNet (Deng et al., 2009) categories. The 1000 synsets are selected such that there is no overlap between synsets", E + "imagenet_ilsvrc_arxiv_1409.0575_pdf_reading.txt"), Q("n04317175: stethoscope n04376876: syringe", E + "imagenet_ilsvrc2012_browse_synsets_page.txt"), Q("The ImageNet Large Scale Visual Recognition Challenge is a benchmark in object category classification and detection on hundreds of object categories and millions of images.", "eligibility_v04/imagenet_ilsvrc_arxiv_1409.0575_api.txt"), Q("<published>2014-09-01T22:29:38Z</published>", "eligibility_v04/imagenet_ilsvrc_arxiv_1409.0575_api.txt")]),
 "k400": (GEN, "Kinetics-400: fixed list of 400 human action classes (full list in the paper); no clinical / surgical class", [Q("This is the list of classes included in the human action video dataset.", S + "kinetics400_arxiv_1705.06950.txt"), Q("The dataset contains 400 human action classes, with at least 400 video clips for each action. Each clip lasts around 10s and is taken from a different YouTube video.", S + "kinetics_arxiv_1705.06950_abs.txt"), Q("[v1] Fri, 19 May 2017 12:07:01 UTC", S + "kinetics_arxiv_1705.06950_abs.txt")]),
 "k600": (GEN, "Kinetics-600: Kinetics-400 list plus the listed new human action classes; no clinical / surgical class", [Q("This is the list of classes in Kinetics-600 that were not in Kinetics-400, or that have been renamed.", S + "kinetics600_arxiv_1808.01340.txt"), Q("We describe an extension of the DeepMind Kinetics human action dataset from 400 classes, each with at least 400 video clips, to 600 classes, each with at least 600 video clips.", S + "kinetics600_arxiv_1808.01340.txt"), Q("arXiv:1808.01340v1 [cs.CV] 3 Aug 2018", S + "kinetics600_arxiv_1808.01340.txt")]),
 "ucf101": (GEN, "UCF-101: fixed list of 101 human action classes; no clinical / surgical class", [Q("It consists of 101 action classes, over 13k clips and 27 hours of video data. The database consists of realistic user-uploaded videos containing camera motion and cluttered background.", S + "ucf101_arxiv_1212.0402.txt"), Q("arXiv:1212.0402v1 [cs.CV] 3 Dec 2012", S + "ucf101_arxiv_1212.0402.txt")]),
 "k700": (GEN, "Kinetics-700: Kinetics-600 list plus the listed new human action classes; no clinical / surgical class", [Q("This is the list of classes in Kinetics-700 that were not in Kinetics-600, or that have been renamed.", E + "kinetics700_arxiv_1907.06987_pdf_reading.txt"), Q("We describe an extension of the DeepMind Kinetics human action dataset from 600 classes to 700 classes, where for each class there are at least 600 video clips from different YouTube videos.", "eligibility_v04/kinetics700_arxiv_1907.06987_api.txt"), Q("<published>2019-07-15T12:58:21Z</published>", "eligibility_v04/kinetics700_arxiv_1907.06987_api.txt")]),
 "howto100m": (UNK, "HowTo100M: fixed release, but its task ontology includes a Health category (WikiHow), so clinical / medical content cannot be excluded -> content scope not bounded for the DS203 / clinical-overlap concern", [Q("To obtain predominantly visual tasks, we limit them to one of 12 categories (listed in Table 2).", E + "howto100m_arxiv_1906.03327_pdf_reading.txt"), Q("Sports and Fitness 205 Health 172 Education and Communications 239", E + "howto100m_arxiv_1906.03327_pdf_reading.txt"), Q("we introduce HowTo100M: a large-scale dataset of 136 million video clips sourced from 1.22M narrated instructional web videos depicting humans performing and describing over 23k different visual tasks.", "eligibility_v04/howto100m_arxiv_1906.03327_api.txt"), Q("<published>2019-06-07T20:48:19Z</published>", "eligibility_v04/howto100m_arxiv_1906.03327_api.txt")]),
 "heico": (NAMED, "Heidelberg University Hospital, Department of Surgery", PV("HeiCo / ROBUST-MIS")),
 "mbp140": (NAMED, "University Hospital of Strasbourg; Inselspital, Bern University Hospital", PV("MultiBypass140")),
 "ssv2": (GEN, "SSv2: 174 caption templates of object manipulations recorded by crowd workers themselves; no clinical / surgical class", [Q("Crowdworkers are asked to record videos and to complete captiontemplates, by providing appropriate input-text for placeholders.", E + "ssv2_arxiv_1706.04261_pdf_reading.txt"), Q("The database currently contains more than 100,000 videos across 174 classes, which are defined as caption-templates. We also describe the challenges in crowd-sourcing this data at scale.", S + "ssv2_arxiv_1706.04261_abs.txt"), Q("[v1] Tue, 13 Jun 2017 21:26:19 UTC", S + "ssv2_arxiv_1706.04261_abs.txt")]),
}
UNK_REASON = {  # decisive reasons for overlap-ineligible candidates
 "dsad_yes": "direct overlap YES under rule A: DSAD, a known same-hospital clinical source (University Hospital Carl Gustav Carus Dresden; C2 = its Department of Pediatric Surgery); other sources are also UNK",
 "site_not_stated": "a clinical training set has no recording site in any obtainable level-1-3 source (out/dataset_provenance.json status NOT_STATED / NOT_OBTAINABLE)",
 "web": "a training source is an open-ended / unversioned web corpus (stock / social / self-crawled Internet video; not a named versioned benchmark)",
 "clinical_web": "a training source is surgical / clinical video from web platforms whose recording sites cannot be bounded (Rule A clinical/site-provenance clause, which Rule B never overrides)",
 "base_undoc": "a base or initialisation model's training data are not documented",
}
LEVEL4_CONTEXT = "mmaction2 label maps (level 4, context only): no Kinetics-400/600/700 class name contains surg/operat/laparo/endoscop/hospital/medic/doctor/patient/clinic"
# ---- candidates --------------------------------------------------------------------------------------------------
VIT_TAB = Q("Model Layers Hidden size D MLP size Heads Params ViT-Base 12 768 3072 12 86M ViT-Large 24 1024 4096 16 307M", "eligibility_v04/vit_arxiv_2010.11929_pdf.txt")
C = []
def cand(name, survey, cls, cls_q, clip, clip_q, rules=None, unk=None, unk_q=None, note=""):
    C.append(dict(name=name, survey_entry=survey, cls=cls, class_quotes=cls_q, clip_level=clip, clip_quotes=clip_q, rules=rules or {}, unk=unk, unk_quotes=unk_q or [], note=note))
ENC, GENERIC, NEITHER = "primary (medical/endoscopic representation-learning encoder)", "secondary (generic reconstructive / generative video model)", "neither (surgical-domain generative model)"
# primary class, failing on DS203 overlap (UNK)
cand("Endo-FM", "Endo-FM", ENC, [Q("Foundation Model for Endoscopy Video Analysis via Large-scale Self-supervised Pre-train", P + "endofm_arxiv_abs.txt")], True,
     [Q("we develop a video transformer, based on ViT B/16 [8]", P + "endofm_arxiv_pdf.txt")], unk="site_not_stated",
     unk_q=[Q("Colonoscopic [19] SUN [20] & SUN-SEG [13] LDPolypVideo [18] Hyper-Kvasir [5] Kvasir-Capsule [31] CholecTriplet [24]", P + "endofm_arxiv_pdf.txt")], note="LDPolypVideo, Colonoscopic: recording site not obtainable")
cand("EndoViT", "EndoViT", ENC, [Q("For pretraining, we closely follow the approach of MAE [ 9 ] and employ the Masked Image Modeling strategy.", P + "endovit_pmc_fulltext.txt")], False,
     [Q("For consistency, we always downsample to 1 FPS.", P + "endovit_pmc_fulltext.txt")], unk="dsad_yes",
     unk_q=[Q("we introduce Endo700k, a collection of 9 publicly available endoscopic datasets comprising more than 700,000 unlabelled images.", P + "endovit_github_readme.txt"), Q("DSAD [ 4 ] Robot-assisted rectal resection 32 13,195", P + "endovit_pmc_fulltext.txt")], note="DSAD (same hospital as C2) -> A-YES; LapGyn4 / GLENDA / SurgicalActions160 / hSDB gastrectomy also A-UNK (site not stated)")
cand("SurgeNetXL", "SurgeNetXL", ENC, [Q("Scaling up self-supervised learning for improved surgical foundation models", P + "surgenetxl_arxiv_pdf.txt")], False,
     [Q("Input frames are resized to a resolution of 224×399 pixels using bicubic interpolation.", P + "surgenetxl_arxiv_pdf.txt")], unk="dsad_yes",
     unk_q=[Q("we extract 680 hours of surgical video footage from YouTube, sampled at 1 frame per second (fps).", P + "surgenetxl_arxiv_pdf.txt"), Q("| **Others** | DSAD ([Carstens et al., 2023](https://www.nature.com/articles/s41597-022-01719-2)) | RA Rectal Resection/Extirpation | 32 | 14,623 | Yes |", P + "surgenet_github_readme.txt")], note="DSAD -> A-YES; YouTube portion also A-UNK")
cand("SurgeNet / SurgeNetPublic", "SurgeNet /", ENC, [Q("Scaling up self-supervised learning for improved surgical foundation models", P + "surgenetxl_arxiv_pdf.txt")], False, [], unk="dsad_yes",
     unk_q=[Q("| **Others** | DSAD ([Carstens et al., 2023](https://www.nature.com/articles/s41597-022-01719-2)) | RA Rectal Resection/Extirpation | 32 | 14,623 | Yes |", P + "surgenet_github_readme.txt"), Q("| **SurgeNetPublic** | All public datasets (excluding YouTube & private datasets) | All of the above (excluding YouTube & RA Esophagectomy) | \\>1238 | 1,997,987 | Yes |", P + "surgenet_github_readme.txt")], note="DSAD -> A-YES; GLENDA / LapGyn4 / hSDB-Gastric / SurgToolLoc also A-UNK")
cand("SurgVLP / HecVL / PeskaVLP", "SurgVLP", ENC, [Q("We utilize the dual-encoder architecture with ResNet50 [21] as visual encoder and ClinicalBert [22] as textual encoder, respectively.", P + "peskavlp_arxiv_pdf.txt")], False,
     [Q("For a given video clip v, we first sample a fixed number of frames {z0 , ..., zT } and then feed them through F", P + "surgvlp_arxiv_pdf.txt")], unk="clinical_web",
     unk_q=[Q("we query the videos based on keywords from three online platforms, i.e., Websurg (Websurg, 2023), EAES (EAES, 2023), and YouTube (YouTube, 2023).", P + "surgvlp_arxiv_pdf.txt")], note="clip embedding = average of per-frame embeddings: not conditioned on temporal order, so frame-level under the v0.4 definition")
cand("EndoMamba", "EndoMamba", ENC, [Q("we propose a self-supervised hierarchical pre-training diagram to enhance EndoMamba’s representation learning using endoscopic videos", P + "endomamba_arxiv_pdf.txt")], True, [], unk="site_not_stated",
     unk_q=[Q("This includes MIX7 (shared with EndoFM), four curated from public datasets, and one from our porcine bronchoscopy dataset (PB), as detailed in Table 1 and Fig. 2.", P + "endomamba_arxiv_pdf.txt")], note="inherits Endo-FM's LDPolypVideo / Colonoscopic; GLENDA")
cand("LemonFM", "LemonFM", ENC, [Q("*LemonFM* is an image foundation model for surgery, it receives an image as input and produces a feature vector of 1536 features as output.", P + "lemonfm_hf_readme.txt")], False,
     [Q("*LemonFM* is an image foundation model for surgery, it receives an image as input and produces a feature vector of 1536 features as output.", P + "lemonfm_hf_readme.txt")], unk="clinical_web",
     unk_q=[Q("Inspired by works [1, 11, 19, 50, 70], we collected our videos from YouTube.", P + "lemon_arxiv_pdf.txt")])
cand("SurgLIME", "SurgLIME", ENC, [Q("Can LLM-Generated Text Empower Surgical Vision-Language Pre-training?", P + "llmtext_vlp_arxiv_pdf.txt")], None, [], unk="clinical_web",
     unk_q=[Q("LEMON collection comprises 4194 surgical videos sourced from YouTube", P + "llmtext_vlp_arxiv_pdf.txt")])
cand("PL-Stitch", "PL-Stitch", ENC, [Q("Learning Procedural Workflow via Self-Supervised Plackett-Luce Ranking", P + "plstitch_github_readme.txt")], False, [], unk="clinical_web",
     unk_q=[Q("Download the pretraining dataset ([LEMON](https://github.com/visurg-ai/LEMON))", P + "plstitch_github_readme.txt")])
cand("Basel V-JEPA ViT-L (jepa-12h)", "Finetuned V-JEPA", ENC, [Q("We finetuned *V-JEPA ViT-L* on unlabeled endoscopic surgical videos, as described in the paper.", P + "mlcds_hf_readme.txt")], True,
     [Q("Each model takes as input a video clip of 16 frames sampled with a frameskip of 4, corresponding to roughly 3 second clips on average.", P + "vjepa_arxiv_pdf.txt")], rules=dict(
    init_stated=("STATED", [Q("By pretrained V-JEPA, we refer to the weights provided by Bardes et al. [1].", P + "mlcds_arxiv_pdf.txt")]),
    sources=["heico", "cholec80", "mbp140", "k400", "k600", "k700", "ssv2", "howto100m"],
    laparoscopic=("YES", [Q("we use all videos from the Cholec80 [12] dataset (80 laparoscopic videos of cholecystectomy surgery, 51:15 h)", P + "mlcds_arxiv_pdf.txt")]),
    same_hospital=("NO", []),
    fits_24gb=("YES", [Q('"rfilename":"jepa-12h.pth.tar","blobId":"5a6e468d2107d9b8f49a17820a6314ea4c2ac498","size":5143102207', P + "mlcds_hf_api_blobs.txt"), VIT_TAB]),
    compute=("YES", [Q("For all experiments, we use the V-JEPA ViT-L model size.", P + "mlcds_arxiv_pdf.txt"), VIT_TAB]),
    init=[Q("By pretrained V-JEPA, we refer to the weights provided by Bardes et al. [1].", P + "mlcds_arxiv_pdf.txt"),
          Q("Specifically, we combine the videos from HowTo100M (HT) (Miech et al., 2019), Kinetics-400/600/700 (K710) (Kay et al., 2017), and Something-Something-v2 (SSv2) (Goyal et al., 2017)", P + "vjepa_arxiv_pdf.txt"),
          Q("Videos from the following datasets were used for finetuning:", P + "mlcds_hf_readme.txt")]),
    note="v0.4-final3: ineligible - HowTo100M (in the V-JEPA base data VideoMix2M) has an unbounded content scope (Health category); finetuning sets HeiCo / Cholec80 / MultiBypass140 are named non-DS203 sites")
cand("EndoSSL (colonoscopy weights)", "EndoSSL", ENC, [Q("we study the use of a leading SSL framework, namely Masked Siamese Networks (MSNs), for endoscopic video analysis such as colonoscopy and laparoscopy.", P + "endossl_arxiv_pdf.txt")], False, [],
     unk="site_not_stated", unk_q=[Q("These videos were recorded during standard colonoscopy procedures performed at six different medical centers between the years 2019 and 2022.", P + "endossl_arxiv_pdf.txt")], note="also fails the laparoscopic rule (colonoscopy only)")
# primary class, candidates for eligibility (full rule evaluation)
SN_ARCH = [Q("Backbone CaFormerS18 Number of parameters 24.3M", P + "surgenetxl_arxiv_pdf.txt"), Q("We initiate pretraining from ImageNet-initialized weights as recommended by Ramesh et al. (2023)", P + "surgenetxl_arxiv_pdf.txt")]
SN_CLS = [Q("Scaling up self-supervised learning for improved surgical foundation models", P + "surgenetxl_arxiv_pdf.txt")]
SN_CLIP = [Q("Input frames are resized to a resolution of 224×399 pixels using bicubic interpolation.", P + "surgenetxl_arxiv_pdf.txt")]
cand("SurgeNetCholec (CAFormer-S18)", "SurgeNet /", ENC, SN_CLS, False, SN_CLIP, rules=dict(
    init_stated=("STATED", SN_ARCH[1:] + [Q('"ImageNet1k": "https://huggingface.co/sail/dl/resolve/main/caformer/caformer_s18.pth"', P + "surgenet_github_readme.txt")]),
    sources=["cholec80", "heichole", "hsdb_chole", "imagenet"],
    laparoscopic=("YES", [Q("SurgeNetCholec: this subset contains 250,655 frames extracted from laparoscopic cholecystectomy procedures.", P + "surgenetxl_arxiv_pdf.txt")]),
    same_hospital=("NO", []),
    fits_24gb=("YES", [Q('"rfilename":"CHOLEC_checkpoint_epoch0050_teacher.pth","blobId":"01ae6ac519157210df9c21dc8e69a20dbdebeda7","size":93022798', P + "surgenet_hf_api_blobs.txt")] + SN_ARCH[:1]),
    compute=("YES", SN_ARCH[:1]), init=SN_ARCH[1:]))
cand("SurgeNetRARP (CAFormer-S18)", "SurgeNet /", ENC, SN_CLS, False, SN_CLIP, rules=dict(
    init_stated=("STATED", SN_ARCH[1:] + [Q('"ImageNet1k": "https://huggingface.co/sail/dl/resolve/main/caformer/caformer_s18.pth"', P + "surgenet_github_readme.txt")]),
    sources=["esad", "psiava", "rarp_avl", "imagenet"],
    laparoscopic=("YES", [Q("In the images, it can been seen that bounding boxes are centred around the tool as laparoscopic tools represent the subject of action", "datasets/esad__arxiv_pdf.txt"),
                          Q("SurgeNetRARP: this subset comprises 382,416 frames from RARP procedures.", P + "surgenetxl_arxiv_pdf.txt")]),
    same_hospital=("NO", []),
    fits_24gb=("YES", [Q('"rfilename":"RARP_checkpoint_epoch0050_teacher.pth","blobId":"883acd7aa73006b3d55d356e18c871df51e772d0","size":93022798', P + "surgenet_hf_api_blobs.txt")] + SN_ARCH[:1]),
    compute=("YES", SN_ARCH[:1]), init=SN_ARCH[1:]), note="SurgeNetRARP = ESAD + PSI-AVA + RARP-AvL (paper Table 1)")
cand("SurgeNetRAMIE (CAFormer-S18)", "SurgeNet /", ENC, SN_CLS, False, SN_CLIP, rules=dict(
    init_stated=("STATED", SN_ARCH[1:]),
    sources=["ramie", "imagenet"],
    laparoscopic=("UNK", [Q("SurgeNetRAMIE: a total of 377,287 frames are included from RAMIE procedures.", P + "surgenetxl_arxiv_pdf.txt")]),
    same_hospital=("NO", []), fits_24gb=("YES", SN_ARCH[:1]), compute=("YES", SN_ARCH[:1]), init=SN_ARCH[1:]),
    note="no level-1-3 source calls the RAMIE videos laparoscopic ('robot-assisted minimally invasive esophagectomy')")
ESSL_CLS = [Q("we study the use of a leading SSL framework, namely Masked Siamese Networks (MSNs), for endoscopic video analysis such as colonoscopy and laparoscopy.", P + "endossl_arxiv_pdf.txt")]
ESSL_ARCH = Q("As our image encoders we train Vision Transformer (ViT [16]) of different sizes, abbreviated as ViT-S/B/L", P + "endossl_arxiv_pdf.txt")
ESSL_INIT = [Q("In Tab.2e), we look at the effect of the training length when starting from scratch or from a good SSL pretrained checkpoint on ImageNet-1k.", P + "endossl_arxiv_pdf.txt")]
ESSL_T3 = Q("ViT-S ViT-B ViT-L 12 12 24 384 768 1024 1536 3072 4096 6 12 16 23M 86M 307M", P + "endossl_arxiv_pdf.txt")
for sz in ("ViT-B", "ViT-L", "ViT-S"):
    cand(f"EndoSSL laparoscopy {sz}", "EndoSSL", ENC, ESSL_CLS, False, [Q("Each video recording was sampled at a rate of 1 frame per second (FPS)", P + "endossl_arxiv_pdf.txt")], rules=dict(
        sources=["israel8", "endossl_init"],
        laparoscopic=("YES", [Q("The dataset predominantly consists of the following procedures: cholecystectomy (35%), appendectomy (20%), herniorrhaphy (12%), colectomy (6%), and bariatric surgery (5%).", P + "endossl_arxiv_pdf.txt")]),
        same_hospital=("NO", []), fits_24gb=("YES", [ESSL_ARCH, ESSL_T3]), compute=("YES", [ESSL_ARCH, ESSL_T3]), init=ESSL_INIT,
        init_stated=("UNK", [])),
        note="v0.4-final3 init check: initialization of the released checkpoints is not stated in the paper, its supplementary, the README or the released code (inference / downstream only) -> UNK; ineligible. Sizes from supplementary Table 3 (ViT-S 23M, ViT-B 86M, ViT-L 307M)")
RN = Q("This model has 3.8 billion FLOPs.", "eligibility_v04/resnet_arxiv_1512.03385_pdf.txt")
cand("SelfSupSurg (ResNet-50; MoCo v2 / SimCLR / SwAV / DINO)", "SelfSupSurg", ENC, [Q("Self-supervised weights trained on cholec80 dataset using four state-of-the-art SSL methods (MOCO V2, SimCLR, SwAV, and DINO).", P + "selfsupsurg_github_readme.txt")], False,
     [Q("replaced by a linear head that maps the feature vector (2048) to the number of outputs", P + "selfsupsurg_arxiv_pdf.txt")], rules=dict(
    init_stated=("STATED", [Q("Recommended 2 On On Off 256 300 5 Imagenet fully supervised", P + "selfsupsurg_arxiv_pdf.txt")] + [Q('PARAMS_FILE: "./checkpoints/defaults/resnet_50/resnet50-19c8e357.pth"', E + f"selfsupsurg_cfg_h00{k}_yaml.txt") for k in (1, 2, 3, 4)] + [Q("'resnet50': 'https://download.pytorch.org/models/resnet50-19c8e357.pth',", E + "torchvision_v0.8.0_resnet_py.txt"), Q("pretrained (bool): If True, returns a model pre-trained on ImageNet", E + "torchvision_v0.8.0_resnet_py.txt"), Q("We evaluate our method on the ImageNet 2012 classification dataset [36] that consists of 1000 classes.", E + "resnet_arxiv_1512.03385_pdf_reading.txt")]),
    sources=["cholec80", "imagenet"],
    laparoscopic=("YES", [Q("This dataset contains 80 videos of complete laparoscopic cholecystectomy procedures", P + "selfsupsurg_arxiv_pdf.txt")]),
    same_hospital=("NO", []),
    fits_24gb=("YES", [Q("We use ResNet-50 (He et al., 2016) as the base encoder architecture", P + "selfsupsurg_arxiv_pdf.txt"), Q('"content_length": "352288944"', P + "selfsupsurg_weights_dino_check.txt")]),
    compute=("YES", [Q("We use ResNet-50 (He et al., 2016) as the base encoder architecture", P + "selfsupsurg_arxiv_pdf.txt"), RN]),
    init=[Q('PARAMS_FILE: "./checkpoints/defaults/resnet_50/resnet50-19c8e357.pth"', P + "selfsupsurg_cfg_dino.txt")]))
# neither class
for nm, sv, q, f in [("Cosmos-H-Surgical v0.3.1", "Cosmos-H-Surgical v0.3.1", "Cosmos-H-Surgical delivers high-quality video prediction and transfer for surgical scenes, including future-state simulation and control-conditioned generation across modalities.", "cosmoshsurg_github_readme.txt"),
                     ("Cosmos-H-Surgical Predict/Transfer 2.5", "Cosmos-H-Surgical-Predict", "Fine-tuned from Cosmos-Predict2.5-2B, the model takes a first frame image and a text description as input and predicts the next 92 future frames of surgical video.", "cosmoshsurg25_hf_readme.txt"),
                     ("Cosmos-H-Surgical-Simulator", "Cosmos-H-Surgical-Simulator", "Cosmos-H-Surgical-Simulator is a kinematic action-conditioned surgical world foundation model", "cosmoshsurgsim_hf_readme.txt"),
                     ("Cosmos-H-Dreams", "Cosmos-H-Dreams", "Cosmos-H-Dreams is a real-time, action-conditioned generative surgical world model", "cosmoshdreams_hf_readme.txt"),
                     ("MedSora", "MedSora", "MedSora: Optical Flow Representation Alignment Mamba Diffusion Model for Medical Video Generation", "medsora_arxiv_pdf.txt"),
                     ("SG2VID", "SG2VID", "we introduce SG2VID, the first diffusion-based video model that leverages Scene Graphs for both precise video synthesis and fine-grained human control.", "sg2vid_arxiv_pdf.txt"),
                     ("KVLR", "KVLR", "From Articulated Kinematics to Routed Visual Control for Action-Conditioned Surgical Video Generation", "kvlr_arxiv_pdf.txt")]:
    cand(nm, sv, NEITHER, [Q(q, P + f)], None, [])
# secondary class
cand("Open-Sora VAE v1.2", "Open-Sora VAE", GENERIC, [Q("This repository stores the weights of the VAE released by the Open-Sora team.", S + "opensora_OpenSora-VAE-v1.2_README.md")], True, [], unk="web",
     unk_q=[Q("The training data is videos from pixels and pixabay, and the training video size is mainly 17 frames, 256x256 resolution.", S + "opensora_github_v1.2.0_report_03.md")], note="also SDXL image-VAE initialisation (undocumented data)")
cand("VideoMAE V2", "VideoMAE V2", GENERIC, [Q("we propose to mask the decoder as well and devise the dual masking strategy.", S + "videomaev2_arxiv_2303.16727v2.txt")], True, [], unk="web",
     unk_q=[Q("Specifically, our dataset is built by simply selecting videos from the public available datasets of Kinetics [43], Something-Something [31], AVA [32], WebVid2M [5], and our own crawled Instagram dataset.", S + "videomaev2_arxiv_2303.16727v2.txt")])
cand("Open-Sora-Plan v1.2 VAE", "Open-Sora-Plan", GENERIC, [Q("The VAE in version 1.2.0 maintains the overall architecture of the previous version but merges the temporal and spatial downsampling layers.", S + "osplan_github_Report-v1.2.0.md")], True, [], unk="web",
     unk_q=[Q("We perform the first phase of training on the Kinetic400 video dataset, then use the EMA weights from this phase to initialize the second phase, which is fine-tuned on high-quality data (collected in v1.1.0).", S + "osplan_github_Report-v1.2.0.md")], note="v1.1.0 data = Mixkit / Pixabay / Pexels stock video; SD2.1 VAE initialisation")
cand("CV-VAE", "CV-VAE", GENERIC, [Q("A video VAE for latent generative video models, which is compatible with pretrained image and video models, e.g., SD 2.1 and SVD", S + "cvvae_github_README.md")], True, [], unk="base_undoc",
     unk_q=[Q("The architecture of CV-VAE is primarily derived from the VAE in Stable Diffusion [ 28 ] , with several notable differences: (1) Some or all 2D convolutions within the network are transformed into 3D convolutions, while retaining their weights.", S + "cvvae_arxiv_2405.20279_fulltext.txt"), Q("Training Details. We train our CV-VAE model using image datasets including LAION-COCO [ 9 ] and Unsplash [ 23 ] , as well as the video dataset Webvid-10M [ 3 ] .", S + "cvvae_arxiv_2405.20279_fulltext.txt")], note="LAION-COCO / Unsplash / WebVid-10M would fall under the B1 override, but the Stable Diffusion VAE whose weights are retained has no training-data statement in the obtained level-1-3 sources")
cand("Reducio-VAE", "Reducio", GENERIC, [Q("This model is a 3D VAE that encodes video into a compact latent space conditioned on a content frame.", S + "reducio_hf_README.md")], True, [], unk="web",
     unk_q=[Q("Our Reducio -VAE is trained on a 400K video dataset collected from Pexels", S + "reducio_arxiv_2411.13552_fulltext.txt")])
VMAE_T7 = [Q("VideoMAE ViT-B 7 16 180×5×3 87 81.5 95.1", S + "videomae_arxiv_2203.12602v3.txt"), Q("VideoMAE ViT-L 7 16 597×5×3 305 85.2 96.8", S + "videomae_arxiv_2203.12602v3.txt")]
cand("VideoMAE (K400 / SSv2 / UCF101 checkpoints)", "VideoMAE (", GENERIC, [Q("VideoMAE is an extension of [Masked Autoencoders (MAE)](https://arxiv.org/abs/2111.06377) to video.", S + "videomae_videomae-base_README.md")], True,
     [Q('"num_frames": 16,', S + "videomae_videomae-base_config.json")], rules=dict(
    init_stated=("STATED", [Q("effectively and efficiently train a vanilla vision transformer on the video dataset itself without using any pre-trained model", S + "videomae_arxiv_2203.12602v3.txt")]),
    sources=["k400", "ssv2", "ucf101"], same_hospital=("NO", []), fits_24gb=("YES", VMAE_T7), compute=("YES", VMAE_T7),
    init=[Q("VideoMAE achieves impressive results on very small datasets (i.e., around 3k-4k videos) without using any extra data.", S + "videomae_arxiv_2203.12602v3.txt"),
          Q("VideoMAE model pre-trained on Kinetics-400 for 1600 epochs in a self-supervised way.", S + "videomae_videomae-base_README.md"),
          Q("VideoMAE model pre-trained on Something-Something-v2 for 2400 epochs in a self-supervised way.", S + "videomae_videomae-base-ssv2_README.md")]),
    note="each checkpoint is trained on one benchmark; the eligibility holds per checkpoint")
cand("OmniTokenizer (ImageNet + K600)", "OmniTokenizer", GENERIC, [Q("We introduce OmniTokenizer, a joint image-video tokenizer which features the following properties:", S + "omnitok_github_README.md")], True, [], rules=dict(
    init_stated=("STATED", [Q("# Stage1: Image-only training on a fixed resolution", S + "omnitok_github_scripts_recons_train.sh.txt"), Q("--logitslaplace_weight 0.4 --initialize_vit --disloss_check_thres 0.001", S + "omnitok_github_scripts_recons_train.sh.txt"), Q("if initialize: self.apply(self._init_weights)", E + "omnitok_omnitokenizer_py.txt"), Q("trunc_normal_(m.weight, std=.02)", E + "omnitok_omnitokenizer_py.txt"), Q("--pretrained {CKPT_OF_PREVIOUS_STAGE}", S + "omnitok_github_scripts_recons_train.sh.txt")]),
    sources=["imagenet", "k600"], same_hospital=("NO", []),
    fits_24gb=("YES", [Q('"rfilename": "imagenet_k600.ckpt", "blobId": "64aa8ed0997c4f8d25b1d911a57a31c957a26852", "size": 742455697,', S + "omnitok_Daniel0724__OmniTokenizer_hfapi.json")]),
    compute=("YES", [Q("Ours 51 262 1.28", S + "omnitok_arxiv_2406.09399_fulltext.txt")]),
    init=[Q("| VQVAE | ImageNet + K600 | 1.23 | 25.97 | [imagenet_k600.ckpt](https://huggingface.co/Daniel0724/OmniTokenizer/resolve/main/imagenet_k600.ckpt) |", S + "omnitok_github_README.md")]))
cand("WF-VAE-L 16ch", "WF-VAE", GENERIC, [Q("WF-VAE: Enhancing Video VAE by Wavelet-Driven Energy Flow for Latent Video Diffusion Model", S + "osplan_hf_WF-VAE-L-16Chn_README.md")], True, [], rules=dict(
    init_stated=("STATED", [Q("The model config of VAE. If you want to train from scratch use this parameter.", E + "wfvae_TRAIN_AND_VALIDATE_md.txt"), Q("--model_config examples/wfvae-large-16chn.json", E + "wfvae_train_ddp_sh.txt")]),
    sources=["k400"], same_hospital=("NO", []),
    fits_24gb=("YES", [Q("We have released our **16-channel WF-VAE-L (316M)** model along with the training code.", S + "wfvae_github_README.md")]),
    compute=("YES", [Q("We have released our **16-channel WF-VAE-L (316M)** model along with the training code.", S + "wfvae_github_README.md")]),
    init=[Q("Dataset & Evaluation. We utilize the Kinetics-400 dataset [ 16 ] for both training and validation.", S + "wfvae_arxiv_2411.17459_fulltext.txt")]), note="no pretrained initialisation named in the paper")
cand("LARP-L-Long tokenizer", "LARP", GENERIC, [Q("We present LARP, a novel video tokenizer inherently aligned with autoregressive (AR) generative models.", S + "larp_github_README.md")], True, [], rules=dict(
    init_stated=("STATED", [Q("# If you want to initialize the model with a checkpoint, set the path here init_checkpoint: ''", E + "larp_cfg_larp_tokenizer_yaml.txt"), Q("# It can reproduce the pretrained model hywang66/LARP-L-long-tokenizer released on HuggingFace. python3 \\ train.py --cfg cfgs/larp_tokenizer.yaml", S + "larp_github_train_larp_tokenizer_reproduce.sh.txt")]),
    sources=["k600", "ucf101"], same_hospital=("NO", []),
    fits_24gb=("YES", [Q("| LARP-L-Long-tokenizer | 173M | 20 (recon.) |", S + "larp_github_README.md")]),
    compute=("YES", [Q("| LARP-L-Long-tokenizer | 173M | 20 (recon.) |", S + "larp_github_README.md")]),
    init=[Q("--csv_file k600_train.csv+ucf101_train.csv", S + "larp_github_train_larp_tokenizer_reproduce.sh.txt")]), note="no pretrained initialisation named in the paper")
cand("LeanVAE", "LeanVAE", GENERIC, [Q("We present **LeanVAE**, a lightweight Video VAE designed for ultra-efficient video compression and scalable generation in Latent Video Diffusion Models (LVDMs).", S + "leanvae_github_README.md")], True, [], rules=dict(
    init_stated=("STATED", [Q("Unlike previous methods that either inherited the Video VAE from the SD VAE or employed ViT [ 3 ] architectures, we use two key designs to ensure a lightweight network.", S + "leanvae_arxiv_2503.14325_fulltext.txt"), Q("parser.add_argument('--pretrained', type=str, default=None)", E + "leanvae_train_py.txt"), Q("CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python leanvae_train.py", E + "leanvae_train_sh.txt")]),
    sources=["k600"], same_hospital=("NO", []),
    fits_24gb=("YES", [Q("| **LeanVAE-16ch** | 30.15 | 0.0461 | 39.8M | 0.203 |", S + "leanvae_hf_README.md")]),
    compute=("YES", [Q("| **LeanVAE-16ch** | 30.15 | 0.0461 | 39.8M | 0.203 |", S + "leanvae_hf_README.md")]),
    init=[Q("Training Details We train the model using Kinetics-600 dataset [ 7 ] .", S + "leanvae_arxiv_2503.14325_fulltext.txt")]), note="no pretrained initialisation named in the paper")
cand("Open-MAGVIT2 video tokenizer", "Open-MAGVIT2", GENERIC, [Q("This is the official repository for Open-MAGVIT2, an open-source project re-implementing Google's MAGVIT-v2 tokenizer", S + "openmagvit2_seedvoken_docs_Open-MAGVIT2.md")], True, [], rules=dict(
    init_stated=("STATED", [Q("Simultaneously, we inflate the image tokenizer trained at 128 × \\times 128 imagenet for video modeling.", S + "openmagvit2_arxiv_2409.04410_fulltext.txt")]),
    sources=["ucf101", "imagenet"], same_hospital=("NO", []),
    fits_24gb=("YES", [Q('"rfilename": "video_128_262144.ckpt", "blobId": "bd81d824e18c8114c30558cae57481da9d0ab845", "size": 2964564510,', S + "openmagvit2_TencentARC__Open-MAGVIT2-Tokenizer-262144-Video_hfapi.json")]),
    compute=("UNK", []),
    init=[Q("Simultaneously, we inflate the image tokenizer trained at 128 × \\times 128 imagenet for video modeling.", S + "openmagvit2_arxiv_2409.04410_fulltext.txt")]),
    note="no parameter count or FLOPs in any level-1-3 source (the paper's counts are for the AR transformers)")
# ---- evaluation: two-level rule (A decides; B disclosed; C = same-hospital applies to clinical sources) ----------
TIEBREAK_ORDER = ["scientific rank criteria of protocol §4.1.4 (not applied here)",
                  "1. authors' explicitly documented default / recommended checkpoint (level-1 source; not inferred)",
                  "2. lower protocol-relevant compute", "3. lower measured synthetic-input peak memory (§4.1 feasibility test, after freeze)",
                  "4. lexical order of the model / checkpoint identifier"]
def rule_a(sources): return "NO" if all(SRC[s][0] in (NAMED, GEO, GEN) for s in sources) else ("YES" if any(SRC[s][0] == YES for s in sources) else "UNK")
def strict(sources): return "NO" if all(SRC[s][0] in (NAMED, GEO) for s in sources) else "UNK"
rows = []
for c in C:
    r = dict(name=c["name"], cls=c["cls"], clip_level=c["clip_level"], note=c["note"])
    if c["cls"] == NEITHER:
        r.update(eligible=False, eligible_strict_counterfactual=False, failing="class: surgical-domain generative (neither arm)")
    elif c["unk"]:
        r.update(eligible=False, eligible_strict_counterfactual=False, overlap_A="YES" if c["unk"] == "dsad_yes" else "UNK",
                 failing=("" if c["unk"] == "dsad_yes" else "direct overlap UNK under rule A: ") + UNK_REASON[c["unk"]])
    else:
        R = c["rules"]; fails = []
        if c["cls"] == ENC and R["laparoscopic"][0] != "YES": fails.append("laparoscopic video not affirmatively documented")
        if R["fits_24gb"][0] != "YES": fails.append("prior 24-GB screen: size not documented")
        if R["compute"][0] != "YES": fails.append("compute not documented")
        if R.get("init_stated", ("UNK",))[0] != "STATED": fails.append("initialization not stated in any level-1-3 source")
        a = rule_a(R["sources"]); r["overlap_A"] = a
        f = fails + ([] if a == "NO" else [f"direct overlap {a} under rule A"])
        r.update(eligible=not f, failing="; ".join(f) or "-", eligible_strict_counterfactual=(not fails) and strict(R["sources"]) == "NO",
                 web_origin_disclosure_B=[SRC[s][1] for s in R["sources"] if SRC[s][0] == GEN],
                 sources=[dict(source=s, status=SRC[s][0], institution_or_content=SRC[s][1]) for s in R["sources"]],
                 prior_screen_24gb=R["fits_24gb"][0], init_stated=R.get("init_stated", ("UNK", []))[0],
                 init_quotes=[q["quote"] for q in R.get("init_stated", ("UNK", []))[1]])
    rows.append(r)
allq = [DS203_RELEASE] + [q for c in C for q in c["class_quotes"] + c["clip_quotes"] + c["unk_quotes"] + [x for k, v in c["rules"].items() if isinstance(v, tuple) for x in v[1]] + c["rules"].get("init", [])] + [q for v in SRC.values() for q in v[2]]
bad = [q for q in allq if not q["verified"]]; low = [q for q in allq if q["level"] > 3]
# ---- [v0.4-final3] term check of documented ontologies + boundedness of every source of every candidate --------
import re as _re
TERMS = r"surg|laparo|endoscop|hospital|operating room|medic|doctor|patient|clinic|dentist|health|stethoscope|syringe|nurse|injection"
ONTO = {"imagenet": E + "imagenet_ilsvrc2012_browse_synsets_page.txt", "k400": S + "kinetics400_arxiv_1705.06950.txt", "k600": S + "kinetics600_arxiv_1808.01340.txt",
        "k700": E + "kinetics700_arxiv_1907.06987_pdf_reading.txt", "ucf101": S + "ucf101_arxiv_1212.0402.txt", "ssv2": E + "ssv2_arxiv_1706.04261_pdf_reading.txt",
        "howto100m": E + "howto100m_arxiv_1906.03327_pdf_reading.txt"}
term_check = {k_: sorted(set(m.group(0).strip().lower() for m in _re.finditer(r"[a-z\- ]{0,20}(" + TERMS + r")[a-z\- ]{0,20}", open(os.path.join(FS, v_), errors="replace").read(), _re.I)))[:20] for k_, v_ in ONTO.items()}
BOUND_OF = {NAMED: "bounded: named non-DS203 recording site", GEO: "bounded: stated non-German geography", GEN: "bounded: fixed ontology (Rule B override applies)",
            YES: "known same-hospital clinical source (Rule A YES)", UNK: "not bounded (Rule A UNK)"}
SO = json.load(open(os.path.join(OUT, "site_overlap.json")))["rows"]
SO_MAP = {"SURGICAL": None}
SO_CLASS = {"hospital named": "bounded: named recording site (non-DS203 unless DSAD)", "unnamed centres, geography stated": "bounded: stated non-German geography",
            "clinical, recording site not stated": "not bounded: clinical set without stated site (Rule A UNK)",
            "non-clinical (animal / phantom / bench), site not stated": "not bounded: site not stated (Rule A UNK, conservative)",
            "web-scale": "not bounded: open-domain / scraped web or surgical web corpus (Rule A UNK)", "undocumented base / init weights": "not bounded: undocumented base data (Rule A UNK)",
            "fixed general benchmark (non-medical)": "see benchmark entry (bounded ontology unless stated otherwise)"}
SO_NAME = {"Endo-FM": "Endo-FM", "EndoViT": "EndoViT", "SurgeNetXL": "SurgeNetXL", "SurgeNet / SurgeNetPublic": "SurgeNet / SurgeNetPublic",
           "SurgVLP / HecVL / PeskaVLP": "SurgVLP / HecVL / PeskaVLP", "EndoMamba": "EndoMamba", "LemonFM": "LemonFM", "SurgLIME": "SurgLIME",
           "PL-Stitch": "PL-Stitch", "EndoSSL (colonoscopy weights)": "EndoSSL (colonoscopy weights)", "Cosmos-H-Surgical v0.3.1": "Cosmos-H-Surgical v0.3.1",
           "Cosmos-H-Surgical Predict/Transfer 2.5": "Cosmos-H-Surgical Predict/Transfer 2.5", "Cosmos-H-Surgical-Simulator": "Cosmos-H-Surgical-Simulator",
           "Cosmos-H-Dreams": "Cosmos-H-Dreams", "MedSora": "MedSora", "SG2VID": "SG2VID", "KVLR": "KVLR", "Open-Sora VAE v1.2": "Open-Sora VAE v1.2",
           "VideoMAE V2": "VideoMAE V2", "Open-Sora-Plan v1.2 VAE": "Open-Sora-Plan v1.2 VAE", "CV-VAE": "CV-VAE", "Reducio-VAE": "Reducio-VAE"}
def so_row(name):
    lab = SO_NAME.get(name)
    return next((r_ for r_ in SO if r_["candidate"].strip() == lab), None)
per_candidate = {}
for c in C:
    if c["rules"].get("sources"):
        per_candidate[c["name"]] = [dict(source=s_, verdict=BOUND_OF[SRC[s_][0]], what=SRC[s_][1]) for s_ in c["rules"]["sources"]]
    else:
        r_ = so_row(c["name"])
        per_candidate[c["name"]] = [dict(source=x["source"], verdict=("bounded: fixed ontology" if x["key"] in ("imagenet", "kinetics", "ssv2", "ucf101") else ("known same-hospital clinical source (Rule A YES)" if x["key"] == "dsad" else SO_CLASS.get(x["cls"], x["cls"]))), what=x["institution"]) for x in (r_["sources"] if r_ else [])] or [dict(source="(see decisive quote)", verdict=UNK_REASON.get(c["unk"], c["cls"]))]
res = dict(note=__doc__, level4_context=LEVEL4_CONTEXT, ds203_release=DS203_RELEASE, quotes_verified=f"{len(allq) - len(bad)}/{len(allq)}",
           quotes_above_level3=len(low), tie_break_order=TIEBREAK_ORDER,
           eligible_primary=[r["name"] for r in rows if r["cls"] == ENC and r["eligible"]],
           eligible_secondary=[r["name"] for r in rows if r["cls"] == GENERIC and r["eligible"]],
           strict_reading_counterfactual=dict(primary=[r["name"] for r in rows if r["cls"] == ENC and r["eligible_strict_counterfactual"]],
                                              secondary=[r["name"] for r in rows if r["cls"] == GENERIC and r["eligible_strict_counterfactual"]]),
           ontology_term_check=term_check, per_candidate_source_boundedness=per_candidate, rows=rows, candidates=C, sources={k: dict(status=v[0], what=v[1], quotes=v[2]) for k, v in SRC.items()})
json.dump(res, open(os.path.join(OUT, "ss_eligibility_v04.json"), "w"), indent=1, ensure_ascii=False)
print(res["quotes_verified"], "above level 3:", len(low))
print("eligible_primary", res["eligible_primary"]); print("eligible_secondary", res["eligible_secondary"]); print("strict counterfactual", res["strict_reading_counterfactual"])
for q in bad: print("NOT VERIFIED:", q["quote"][:100], q["copy"])
for r in rows: print(f"{r['name'][:44]:44s} | {r['cls'][:9]:9s} | clip={str(r['clip_level']):5s} | A={r.get('overlap_A','-'):3s} | {r['failing']}")
