"""Step 2 of CC_TASK_post_download_preprotocol: DS203 centre institutions x pretraining-data institutions of every
eligible FM candidate (052590c) and of the Decision-005 Cosmos reference. Facts only; no model is chosen.
Inputs: DS203 descriptor copies on LaCie; candidate quotes from out/fm_candidates_{primary,secondary}.json;
dataset recording-site quotes from out/dataset_provenance.json; Cosmos reference from out/cosmos_reference_entry.json.
Every quote is re-verified here as a whitespace-normalised substring of its saved copy.
Cell rule (lineage rule of the survey: training data of the released weights + initialisation / base weights;
distillation teachers recorded only):
  SAME DEPT / SAME HOSP  a named source was recorded at that centre's department / hospital (other department)
  UNK-web    a web-scale source (YouTube, web lecture platforms, stock / social / Internet video) or a base model whose
             training data are not documented
  UNK-site   all sources named, but >=1 human clinical dataset has no recording site in the obtainable sources
  NO         every source has a named recording site (or is non-clinical, or a fixed general benchmark such as
             ImageNet / Kinetics / SSv2 / UCF-101), and none is a DS203 institution
C1, C3, C4, C5 are four public hospitals whose centre-number mapping is not stated; a source from any of the four
would therefore be marked in all four columns. No source from any of them was found."""
import hashlib, json, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..")); OUT = os.path.join(H, "out")
norm = lambda s: re.sub(r"\s+", " ", s).strip()
_cache = {}
def txt(p):
    if p not in _cache: _cache[p] = norm(open(p, errors="replace").read())
    return _cache[p]
def resolve(p, arm=None):
    for c in (p, os.path.join(REPO, p), os.path.join(H, p), os.path.join(H, "fm_sources", arm or "", p + ".txt")):
        if c and os.path.isfile(c): return c
    return None
def Q(quote, path):
    return dict(quote=quote, copy=os.path.relpath(path, REPO) if path.startswith(REPO) else path, verified=norm(quote) in txt(path))

# ---- 2.1 DS203 centres -------------------------------------------------------------------------------------------
DESC = "/media/user/LaCie/medvideo_gate/DS213/appendix300_scidata_PMC13263317.txt"
PDF = "/media/user/LaCie/medvideo_gate/DS203/s41597-026-07593-6.pdf.raw.txt"
README = "/media/user/LaCie/medvideo_gate/DS203/archive/readme_Appendix300.md"
centre_quotes = [
    Q("The participating centers comprise four public hospitals (Asklepios-ASB Krankenhaus Radeberg, Diakonissenkrankenhaus Dresden, Krankenhaus St. Joseph Stift Dresden, St. Elisabethen-Krankenhaus Ravensburg) and one academic surgical department (Department of Pediatric Surgery, University Hospital Carl Gustav Carus Dresden).", DESC),
    Q("Table 1 Recording infrastructure and technical details of the dataset for all contributing centers. Center Characteristics Center 1 Center 2 Center 3 Center 4 Center 5 Clinical Institution public academic public public public Patient Demographics adult pediatric adult pediatric and adult adult", DESC),
    Q("video data from 325 laparoscopic appendectomies and 5 non-appendectomy laparoscopic surgeries were gathered at five German surgical centers.", DESC),
    Q("Department of General, Visceral and Thoracic Surgery, St. Elisabethen-Klinikum Ravensburg, Ravensburg, Germany", DESC),
    Q("**Multicenter Data:** Data from five distinct surgical centers.", README),
]
PUBLIC4 = "one of: Asklepios-ASB Krankenhaus Radeberg; Diakonissenkrankenhaus Dresden; Krankenhaus St. Joseph Stift Dresden; St. Elisabethen-Krankenhaus Ravensburg (centre-number mapping not stated)"
CENTRES = {
 "C1": dict(institution=PUBLIC4, table1="public; adult; 51 recordings; Arthrex Synergy UHD4 / SynergyID; 30 fps"),
 "C2": dict(institution="Department of Pediatric Surgery, University Hospital Carl Gustav Carus Dresden", hospital="Carus Dresden", department="Pediatric Surgery",
            basis="the only 'academic' centre in Table 1 and the only academic surgical department named in the text; Table 1 demographics 'pediatric'",
            table1="academic; pediatric; 49 recordings; STORZ IMAGE1 S; 25 fps"),
 "C3": dict(institution=PUBLIC4, table1="public; adult; 42 recordings; STORZ IMAGE1 S; 25 fps"),
 "C4": dict(institution=PUBLIC4, table1="public; pediatric and adult; 71 recordings; STORZ IMAGE1 S / B. Braun AESCULAP EinsteinVision; 50 fps"),
 "C5": dict(institution=PUBLIC4, table1="public; adult; 118 recordings; Richard Wolf ENDOCAM 4K; 50 fps"),
}
for c in ("C1", "C3", "C4", "C5"): CENTRES[c].update(hospital=None, department=None, basis="Table 1 'public'; the text lists four public hospitals without numbering them")
pdf_check = {q["quote"][:60]: (norm(q["quote"]) in txt(PDF)) for q in centre_quotes[:2]}

# ---- 2.2 pretraining sources ---------------------------------------------------------------------------------------
P = json.load(open(os.path.join(OUT, "dataset_provenance.json")))
prov = {d["name"]: d for d in P["datasets"]}
def pv(name):  # recording-site quotes from the provenance agent's saved copies
    d = prov[name]; return [Q(q["quote"], os.path.join(REPO, q["file"])) for q in d["quotes"]]
PRI = os.path.join(H, "fm_sources", "primary")
HOSP, SITE_NS, NONCLIN, WEB, BASE, GEN, GEO = "hospital named", "clinical, recording site not stated", "non-clinical (animal / phantom / bench), site not stated", "web-scale", "undocumented base / init weights", "fixed general benchmark (non-medical)", "unnamed centres, geography stated"
D = {  # key: (label, class, institution(s), quotes, ds203_match)
 "cholec80": ("Cholec80", HOSP, "University Hospital of Strasbourg", pv("Cholec80"), None),
 "cholect50": ("CholecTriplet / CholecT50", SITE_NS, "45 videos = Cholec80 (Strasbourg); 5 in-house (Cholec120) videos, site not restated", pv("CholecT50 / CholecT45 / CholecTriplet"), None),
 "heichole": ("HeiChole", HOSP, "Heidelberg University Hospital; Salem Hospital Heidelberg; GRN-hospital Sinsheim", pv("HeiChole"), None),
 "heico": ("HeiCo / ROBUST-MIS", HOSP, "Heidelberg University Hospital, Department of Surgery", pv("HeiCo / ROBUST-MIS"), None),
 "psiava": ("PSI-AVA", HOSP, "Fundacion Santa Fe de Bogota", pv("PSI-AVA"), None),
 "grasp": ("GraSP", HOSP, "Fundacion Santa Fe de Bogota", pv("GraSP"), None),
 "esad": ("ESAD", HOSP, "San Raffaele Hospital, Milan", pv("ESAD (SARAS-ESAD)"), None),
 "dsad": ("DSAD (Dresden Surgical Anatomy Dataset)", HOSP, "University Hospital Carl Gustav Carus Dresden; Department of Visceral, Thoracic and Vascular Surgery (rectal surgery; department per author affiliation)",
          [Q("video data from a total of 32 robot-assisted anterior rectal resections or rectal extirpations performed at the University Hospital Carl Gustav Carus Dresden was gathered", os.path.join(PRI, "dsad_scidata.txt")),
           Q("Department of Visceral, Thoracic and Vascular Surgery, University Hospital and Faculty of Medicine Carl Gustav Carus, Technische Universität Dresden, Dresden, Germany Matthias Carstens", os.path.join(PRI, "dsad_scidata.txt"))],
          dict(hospital="Carus Dresden", department="Visceral, Thoracic and Vascular Surgery")),
 "ramie": ("RAMIE-UMCU (private)", HOSP, "University Medical Center Utrecht", [Q("another containing robot-assisted minimally invasive esophagectomy (RAMIE) procedures from the University Medical Center Utrecht (UMCU)", os.path.join(PRI, "surgenetxl_arxiv_pdf.txt"))], None),
 "rarp_avl": ("RARP-AvL (private)", HOSP, "Antoni van Leeuwenhoek Hospital, Amsterdam", pv("RARP-AvL (private)"), None),
 "mbp140": ("MultiBypass140", HOSP, "University Hospital of Strasbourg; Inselspital, Bern University Hospital", pv("MultiBypass140"), None),
 "sarrarp50": ("SAR-RARP50 (KVLR: KASA subset)", HOSP, "University College Hospital at Westmoreland Street, London", pv("SAR-RARP50"), None),
 "autolaparo": ("AutoLaparo", HOSP, "Prince of Wales Hospital, Hong Kong", pv("AutoLaparo"), None),
 "sun": ("SUN / SUN-SEG", HOSP, "Showa University Northern Yokohama Hospital (SUN-SEG also names Nagoya University)", pv("SUN database / SUN-SEG"), None),
 "hyperkvasir": ("Hyper-Kvasir", HOSP, "Baerum Hospital, Vestre Viken Hospital Trust, Norway", pv("Hyper-Kvasir"), None),
 "kvasircap": ("Kvasir-Capsule", HOSP, "Baerum Hospital, Vestre Viken Hospital Trust, Norway", pv("Kvasir-Capsule"), None),
 "endomapper": ("EndoMapper", HOSP, "Hospital Clinico Universitario Lozano Blesa, Zaragoza", pv("EndoMapper"), None),
 "cataract1k": ("Cataract-1K", HOSP, "Klinikum Klagenfurt", pv("Cataract-1K"), None),
 "cataracts": ("CATARACTS", HOSP, "Brest University Hospital", pv("CATARACTS"), None),
 "renji": ("Endo-FM private set", HOSP, "Baoshan Branch of Renji Hospital, Shanghai", [Q("combining 9 publicly available datasets and a privately collected dataset from Baoshan Branch of Renji Hospital in Shanghai, China.", os.path.join(PRI, "endofm_arxiv_pdf.txt"))], None),
 "hsdb_chole": ("hSDB-instrument / hSDB-Chole (cholecystectomy part)", HOSP, "subset of Cholec80 (Strasbourg)", pv("hSDB-instrument"), None),
 "endossl_lap": ("EndoSSL Private Laparoscopy", GEO, "eight unnamed medical centres in Israel", [Q("The dataset consists of 7,877 videos recorded at eight different medical centers in Israel.", os.path.join(PRI, "endossl_arxiv_pdf.txt"))], None),
 "lapgyn4": ("LapGyn4", SITE_NS, "not stated (dataset page: originator Prof. J. Keckstein; Zenodo affiliation Ulm University)", pv("LapGyn4"), None),
 "glenda": ("GLENDA v1.0", SITE_NS, "not stated (author affiliations Klagenfurt / LMU Munich / Ulm; originator J. Keckstein)", pv("GLENDA v1.0"), None),
 "sa160": ("SurgicalActions160", SITE_NS, "not stated (originator Prof. J. Keckstein)", pv("SurgicalActions160"), None),
 "hsdb_gastric": ("hSDB-instrument / hSDB-Gastric (gastrectomy part)", SITE_NS, "not stated (authors: hutom; Yonsei University College of Medicine, Seoul)", pv("hSDB-instrument"), None),
 "colonoscopic": ("Colonoscopic (Mesejo et al. 2016)", SITE_NS, "not obtainable (archived dataset page lists only affiliations: CHU Estaing Clermont-Ferrand; Clinique de la Sauvegarde Lyon)", pv("Colonoscopic (Mesejo et al.)"), None),
 "ldpolyp": ("LDPolypVideo", SITE_NS, "not obtainable (paper behind bot challenge; README names no hospital)", pv("LDPolypVideo"), None),
 "endossl_colon": ("EndoSSL Private Colonoscopy", SITE_NS, "six unnamed medical centres, location not stated", [Q("These videos were recorded during standard colonoscopy procedures performed at six different medical centers between the years 2019 and 2022.", os.path.join(PRI, "endossl_arxiv_pdf.txt"))], None),
 "cmr": ("Open-H CMR Versius clinical procedures", SITE_NS, "unnamed hospitals (institution listed: CMR Surgical)", [Q("~26,500+ surgical task demonstrations (plus CMR Versius clinical procedures) spanning 32 datasets, 9 robot embodiments, and 10+ institutions", os.path.join(PRI, "cosmoshsurgsim_hf_readme.txt")),
          Q("| CMR Versius | cholecystectomy, hysterectomy, inguinal hernia, prostatectomy | ~17M | 50% |", os.path.join(PRI, "cosmoshsurgsim_github_readme.txt"))], None),
 "surgtoolloc": ("SurgToolLoc2022", NONCLIN, "porcine da Vinci training exercises; location not stated", pv("SurgToolLoc 2022"), None),
 "suturebot": ("SutureBot / dVRK tabletop suturing", NONCLIN, "suture-pad phantom on dVRK; location not stated (authors JHU / NVIDIA / Stanford / Toronto)", pv("SutureBot"), None),
 "endomamba_pb": ("EndoMamba porcine bronchoscopy", NONCLIN, "authors' porcine dataset; location not stated", pv("EndoMamba porcine bronchoscopy (PB)"), None),
 "openh_labs": ("Open-H non-CMR groups", NONCLIN, "JHU, JHU LSCR ARCADE, UC Berkeley, Stanford, UCSD, Hamlyn Centre, University of Turin, USTC, Moon Surgical (bench / ex vivo / animal)",
                [Q("| `hamlyn_30hz` | Hamlyn Centre dVRK | **20D** | Hamlyn Centre |", os.path.join(PRI, "cosmoshsurgsim_github_readme.txt")),
                 Q("| `turin_mitic_ex_vivo` | Turin MITIC | **18D** (no grippers) | University of Turin |", os.path.join(PRI, "cosmoshsurgsim_github_readme.txt"))], None),
 "synthetic": ("Cosmos-H synthetic cholecystectomy videos", BASE, "generated by the Cosmos-H-Surgical transfer pipeline; control/source inputs not described", [], None),
 "yt_surgenet": ("Surgical YouTube dataset (SurgeNetXL)", WEB, "YouTube; uploading institutions not itemised", [], None),
 "svl": ("SVL lectures (WebSurg, EAES, YouTube)", WEB, "web lecture platforms; originating hospitals not itemised", [], None),
 "lemon": ("LEMON (YouTube)", WEB, "YouTube; uploading institutions not itemised; oEmbed check of the 252 appendectomy entries found no DS203 institution keyword", [], None),
 "sata_yt": ("SATA 'credentialed YouTube surgical channels'", WEB, "YouTube", [], None),
 "videomix2m": ("V-JEPA base: VideoMix2M (HowTo100M + Kinetics + SSv2)", WEB, "HowTo100M = keyword-searched YouTube instructional video", [], None),
 "webvid": ("WebVid", WEB, "scraped from the Internet", [], None), "instagram": ("self-crawled Instagram", WEB, "Instagram", [], None),
 "stock": ("Pexels / Pixabay / Mixkit stock video", WEB, "stock-video websites", [], None), "laion": ("LAION-COCO / Unsplash images", WEB, "web images", [], None),
 "cosmos_web": ("Cosmos tokenizer data: proprietary + open-domain Internet video (~20M h raw)", WEB, "undisclosed", [], None),
 "cosmos3": ("base Cosmos3-Nano", BASE, "general-domain pretraining video not enumerated", [], None),
 "cosmos25": ("base Cosmos-Predict2.5-2B / Cosmos-Transfer2.5-2B", BASE, "general-domain pretraining video not enumerated", [], None),
 "medsora_vae": ("MedSora base '3D causal VAE'", BASE, "pretraining data not named", [], None),
 "kvlr_base": ("KVLR base video generator", BASE, "not named; data not documented", [], None),
 "sd_vae": ("SD / SDXL / SD2.1 image-VAE initialisation", BASE, "image data not documented in the candidate sources", [], None),
 "imagenet": ("ImageNet (initialisation)", GEN, "fixed image benchmark", [], None), "kinetics": ("Kinetics-400/600/700", GEN, "fixed YouTube human-action benchmark", [], None),
 "ssv2": ("Something-Something v2", GEN, "crowd-sourced action clips", [], None), "ucf101": ("UCF-101", GEN, "fixed action benchmark", [], None), "ava": ("AVA", GEN, "movies", [], None),
}
SURGENET = ["cholec80", "heichole", "hsdb_chole", "ramie", "esad", "psiava", "rarp_avl", "dsad", "glenda", "lapgyn4", "mbp140", "hsdb_gastric", "surgtoolloc", "imagenet"]
ENDOFM = ["colonoscopic", "sun", "ldpolyp", "hyperkvasir", "kvasircap", "cholect50", "renji"]
SIM = ["cmr", "openh_labs", "cosmos25"]
CAND = [  # (row label, survey name prefix or None, arm, dataset keys, note)
 ("Endo-FM", "Endo-FM", "primary", ENDOFM + ["kinetics"], ""),
 ("EndoViT", "EndoViT", "primary", ["heico", "cholec80", "psiava", "esad", "lapgyn4", "hsdb_chole", "hsdb_gastric", "dsad", "glenda", "sa160", "imagenet"], ""),
 ("SurgeNetXL", "SurgeNetXL", "primary", SURGENET + ["yt_surgenet"], ""),
 ("SurgeNet / SurgeNetPublic", "SurgeNet /", "primary", SURGENET, "SurgeNetPublic = public sets only (DSAD included)"),
 ("  SurgeNetCholec variant", "SurgeNet /", "primary", ["cholec80", "heichole", "hsdb_chole", "imagenet"], "procedure subset of the SurgeNet row"),
 ("  SurgeNetRAMIE variant", "SurgeNet /", "primary", ["ramie", "imagenet"], "procedure subset"),
 ("  SurgeNetRARP variant", "SurgeNet /", "primary", ["rarp_avl", "imagenet"], "procedure subset"),
 ("SurgVLP / HecVL / PeskaVLP", "SurgVLP", "primary", ["svl", "imagenet"], ""),
 ("EndoMamba", "EndoMamba", "primary", ENDOFM + ["glenda", "hsdb_chole", "hsdb_gastric", "endomapper", "heico", "endomamba_pb"], "VideoMamba-S teacher = distillation target only"),
 ("LemonFM", "LemonFM", "primary", ["lemon"], ""),
 ("EndoSSL (laparoscopy weights)", "EndoSSL", "primary", ["endossl_lap"], "NO rests on the geographic statement (Israel)"),
 ("EndoSSL (colonoscopy weights)", "EndoSSL", "primary", ["endossl_colon"], ""),
 ("SelfSupSurg", "SelfSupSurg", "primary", ["cholec80", "imagenet"], ""),
 ("SurgLIME", "SurgLIME", "primary", ["lemon"], ""),
 ("PL-Stitch", "PL-Stitch", "primary", ["lemon", "imagenet"], ""),
 ("Basel V-JEPA ViT-L", "Finetuned V-JEPA", "primary", ["heico", "cholec80", "mbp140", "videomix2m"], ""),
 ("Cosmos-H-Surgical v0.3.1", "Cosmos-H-Surgical v0.3.1", "primary", ["grasp", "synthetic", "cosmos3"], ""),
 ("Cosmos-H-Surgical Predict/Transfer 2.5", "Cosmos-H-Surgical-Predict", "primary", ["cholec80", "cholect50", "heichole", "grasp", "sarrarp50", "autolaparo", "mbp140", "sa160", "suturebot", "heico", "sata_yt", "cosmos25"], ""),
 ("Cosmos-H-Surgical-Simulator", "Cosmos-H-Surgical-Simulator", "primary", SIM, "Open-H also holds TUD/NCT Dresden porcine (TUNDRA) data; not in the documented training mixture"),
 ("Cosmos-H-Dreams", "Cosmos-H-Dreams", "primary", ["suturebot"] + SIM, "inherits the Simulator; TUNDRA not documented"),
 ("MedSora", "MedSora", "primary", ["colonoscopic", "cholect50", "kvasircap", "medsora_vae"], ""),
 ("SG2VID", "SG2VID", "primary", ["cataract1k", "cataracts", "cholec80"], "initialisation of U-Net/VQGAN not stated"),
 ("KVLR", "KVLR", "primary", ["sarrarp50", "kvlr_base"], ""),
 ("Open-Sora VAE v1.2", "Open-Sora VAE", "secondary", ["stock", "sd_vae"], ""),
 ("VideoMAE", "VideoMAE (", "secondary", ["kinetics", "ssv2", "ucf101"], ""),
 ("VideoMAE V2", "VideoMAE V2", "secondary", ["kinetics", "ssv2", "ava", "webvid", "instagram"], ""),
 ("OmniTokenizer", "OmniTokenizer", "secondary", ["imagenet", "kinetics"], ""),
 ("Open-MAGVIT2 video", "Open-MAGVIT2", "secondary", ["ucf101", "imagenet"], ""),
 ("Open-Sora-Plan v1.2 VAE", "Open-Sora-Plan", "secondary", ["kinetics", "stock", "sd_vae"], ""),
 ("WF-VAE-L", "WF-VAE", "secondary", ["kinetics"], ""),
 ("CV-VAE", "CV-VAE", "secondary", ["laion", "webvid", "sd_vae"], ""),
 ("LARP", "LARP", "secondary", ["kinetics", "ucf101"], ""),
 ("LeanVAE", "LeanVAE", "secondary", ["kinetics"], ""),
 ("Reducio-VAE", "Reducio", "secondary", ["stock", "sd_vae"], ""),
 ("Cosmos tokenizer CV8x8x8 (Decision 005 reference)", None, "reference", ["cosmos_web"], ""),
]
surveys = {a: json.load(open(os.path.join(OUT, f"fm_candidates_{a}.json")))["candidates"] for a in ("primary", "secondary")}
def cand_quotes(prefix, arm):
    if arm == "reference":
        e = json.load(open(os.path.join(OUT, "cosmos_reference_entry.json")))
        return [Q(q["quote"], os.path.join(H, q["copy"])) for q in e["training_data"]["quotes"]]
    if prefix is None: return []
    x = [c for c in surveys[arm] if c["name"].startswith(prefix)][0]; out = []
    for q in (x.get("pretraining_data_quote") or {}).get("quotes", []):
        p = resolve(q.get("saved_copy") or q.get("copy_path") or "", arm) or resolve(q.get("file") or "", arm)
        if p: out.append(Q(q["quote"], p))
    return out
def cell(keys, centre):
    c = CENTRES[centre]; parts = []
    for k in keys:
        m = D[k][4]
        if m and c["hospital"] == m["hospital"]: parts.append(("SAME DEPT" if c["department"] == m["department"] else "SAME HOSP") + f" ({D[k][0].split(' ')[0]})")
    cls = {D[k][1] for k in keys}
    if WEB in cls or BASE in cls: parts.append("UNK-web")
    elif SITE_NS in cls: parts.append("UNK-site")
    return " + ".join(parts) if parts else "NO"
rows = []
for label, prefix, arm, keys, note in CAND:
    rows.append(dict(candidate=label, arm=arm, note=note, cells={c: cell(keys, c) for c in CENTRES},
        sources=[dict(key=k, source=D[k][0], cls=D[k][1], institution=D[k][2], quotes=D[k][3]) for k in keys],
        candidate_quotes=cand_quotes(prefix, arm),
        web_or_undocumented=[D[k][0] for k in keys if D[k][1] in (WEB, BASE)], site_not_stated=[D[k][0] for k in keys if D[k][1] == SITE_NS]))
allq = centre_quotes + [q for d in D.values() for q in d[3]] + [q for r in rows for q in r["candidate_quotes"]]
res = dict(note=__doc__, ds203_centres=CENTRES, centre_quotes=centre_quotes, pdf_text_check=pdf_check,
           descriptor_sha256={p: hashlib.sha256(open(p, "rb").read()).hexdigest() for p in (DESC, PDF, README)},
           rows=rows, quotes_verified=f"{sum(q['verified'] for q in allq)}/{len(allq)}",
           keyword_search=dict(dataset_copies=P.get("ds203_institution_keyword_hits", {}).get("summary"), note="fm_sources/{primary,secondary,reference}: Radeberg / Ravensburg / Diakonissen / Joseph-Stift / Elisabethen / Asklepios occur only in the survey's own keyword list inside lemon_appendectomy_oembed.txt (keyword_hits: [])"))
json.dump(res, open(os.path.join(OUT, "site_overlap.json"), "w"), indent=1)
md = ["| candidate | arm | C1 | C2 | C3 | C4 | C5 | web-scale / undocumented sources | clinical sources without stated site |", "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    md.append(f"| {r['candidate']} | {r['arm']} | " + " | ".join(r["cells"][c] for c in CENTRES) + f" | {'; '.join(r['web_or_undocumented']) or '-'} | {'; '.join(r['site_not_stated']) or '-'} |")
open(os.path.join(OUT, "site_overlap_table.md"), "w").write("\n".join(md) + "\n")
print(res["quotes_verified"], pdf_check); print("\n".join(md))
[print("NOT VERIFIED:", q["quote"][:90], q["copy"]) for q in allq if not q["verified"]]
SHORT = {HOSP: "", SITE_NS: " [site not stated]", NONCLIN: " [non-clinical]", WEB: " [web-scale]", BASE: " [undocumented base]", GEN: " [general benchmark]", GEO: " [geography only]"}
src_md = []
for r in rows:
    items = "; ".join(f"{s['source']} ({s['institution']}){SHORT[s['cls']]}" for s in r["sources"])
    src_md.append(f"* **{r['candidate'].strip()}** ({len(r['candidate_quotes'])} candidate quotes): {items}" + (f". *{r['note']}*" if r["note"] else ""))
open(os.path.join(OUT, "site_overlap_sources.md"), "w").write("\n".join(src_md) + "\n")
