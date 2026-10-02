"""Literature gate: write lit/RECORDS.csv, every screened record (native search + citation chasing), with the screening
decision and, for FULLTEXT records, the lead analyst's grades (FULLTEXT_NOTES.md S1-S3)."""
import csv, json, os
H = os.path.dirname(os.path.abspath(__file__))
SCREENER = "screening subagent (general-purpose; rubric lit/screening/RUBRIC.md)"
# Lead grades, transcribed from FULLTEXT_NOTES.md (S1 native, S2 Targeted-BEHRT, S3 citation chasing): L1, L2, L3, L4, note
NATIVE = {
 "N0105": ("RELATED","NONE","RELATED","NONE","S1 abstract"), "N0217": ("RELATED","RELATED","NONE","NONE","S1 full-text scan"),
 "N0235": ("RELATED","RELATED","NONE","RELATED","S1 full-text scan"), "N0305": ("RELATED","NONE","NONE","NONE","S1 abstract"),
 "N0309": ("RELATED","NONE","NONE","NONE","S1 abstract"), "N0311": ("NONE","RELATED","NONE","RELATED","S1 abstract"),
 "N0337": ("RELATED","NONE","NONE","NONE","S1 abstract (survey)"), "N0367": ("NONE","NONE","RELATED","NONE","S1 abstract"),
 "N0378": ("NONE","NONE","RELATED","NONE","S1 full-text scan"), "N0386": ("NONE","NONE","RELATED","NONE","S1 full-text scan"),
 "N0445": ("NONE","NONE","NONE","NONE","S1 proceedings volume"), "N0570": ("NONE","RELATED","NONE","RELATED","S1 abstract"),
 "N0587": ("RELATED","NONE","NONE","RELATED","S1 abstract"), "N0596": ("RELATED","NONE","NONE","RELATED","S1 abstract"),
 "N0639": ("RELATED","NONE","NONE","NONE","S1 review"), "N0642": ("RELATED","NONE","NONE","NONE","S1 review"),
 "N0712": ("PARTIAL","NONE","RELATED","RELATED","S2 full text (Targeted-BEHRT)")}
W = {  # work -> grades
 "K1": ("PARTIAL","RELATED","NONE","NONE","K1 full text"), "K2": ("PARTIAL","RELATED","NONE","NONE","K2 full text"),
 "K3": ("PARTIAL","RELATED","NONE","RELATED","K3 full text"), "K4": ("DIRECT (non-medical video)","RELATED","RELATED","RELATED","K4 full text"),
 "veitch20": ("PARTIAL","RELATED","RELATED","NONE","S3.1 full text"), "pryzant21": ("PARTIAL","NONE","RELATED","NONE","S3.1 full text"),
 "gui23": ("PARTIAL","RELATED","RELATED","NONE","S3.1 full text"), "ahrens21": ("PARTIAL","NONE","RELATED","NONE","S3.1 full text"),
 "roberts20": ("PARTIAL","RELATED","RELATED","NONE","S3.1 full text (closest L2 mechanism statement)"),
 "daoud22": ("RELATED","RELATED","NONE","NONE","S3.1 full text"), "mozer20": ("RELATED","NONE","NONE","NONE","S3.1 full text"),
 "mozer24": ("RELATED","NONE","NONE","NONE","S3.1 full text"), "klaassen24": ("PARTIAL","NONE","RELATED","NONE","S3.1 full text"),
 "jerzak23a": ("RELATED","RELATED","RELATED","NONE","S3.1 full text"), "jerzak23b": ("RELATED","NONE","RELATED","NONE","S3.1 full text"),
 "lin24": ("PARTIAL","RELATED","RELATED","NONE","S3.1 full text"), "feldman26": ("PARTIAL","RELATED","RELATED","NONE","S3.1 full text"),
 "guo25": ("PARTIAL","RELATED","RELATED","RELATED","S3.1 full text"), "rao23hyp": ("PARTIAL","NONE","NONE","NONE","S3.1 full text (PMC9944753)"),
 "rao23heart": ("PARTIAL","NONE","NONE","NONE","S3.1 full text (PMC10423512)"), "rao23ehj": ("PARTIAL","NONE","NONE","NONE","S3.1 full text (PMC10635668)"),
 "egami22": ("RELATED","NONE","NONE","NONE","S3.2 abstract"), "feder22": ("RELATED","NONE","NONE","NONE","S3.2 survey"),
 "keith20": ("RELATED","NONE","NONE","NONE","S3.2 review"), "c0260": ("RELATED","NONE","NONE","NONE","S3.2 review"),
 "c0270": ("RELATED","NONE","NONE","NONE","S3.2 editorial"), "c0280": ("RELATED","NONE","NONE","NONE","S3.2 abstract"),
 "c0284": ("RELATED","NONE","NONE","NONE","S3.2 survey"), "c0290": ("RELATED","NONE","NONE","NONE","S3.2 abstract"),
 "omninet": ("UNRESOLVED","NONE","NONE","NONE","S3.3 full text inaccessible (bot challenge); L1 open")}
CIT = {"C0000":"ahrens21","C0066":"ahrens21","C0008":"daoud22","C0076":"daoud22","C0012":"egami22","C0080":"egami22","C0163":"egami22",
 "C0014":"feder22","C0019":"gui23","C0085":"gui23","C0125":"gui23","C0169":"gui23","C0022":"K2","C0129":"K2","C0172":"K2","C0297":"K2",
 "C0025":"jerzak23a","C0026":"jerzak23b","C0173":"jerzak23b","C0032":"keith20","C0034":"klaassen24","C0091":"klaassen24",
 "C0039":"lin24","C0135":"lin24","C0042":"mozer24","C0043":"mozer20","C0104":"mozer20","C0187":"mozer20",
 "C0048":"pryzant21","C0108":"pryzant21","C0139":"pryzant21","C0193":"pryzant21","C0051":"roberts20","C0111":"roberts20","C0197":"roberts20",
 "C0059":"veitch20","C0116":"veitch20","C0147":"veitch20","C0087":"K1","C0128":"K1","C0171":"K1","C0105":"K4","C0106":"K3","C0188":"K3",
 "C0123":"feldman26","C0126":"guo25","C0260":"c0260","C0262":"rao23hyp","C0265":"rao23heart","C0270":"c0270","C0276":"rao23ehj",
 "C0280":"c0280","C0284":"c0284","C0288":"omninet","C0290":"c0290"}
COLS = ["arm","uid","database","query","rank","all_hits","seed","direction","doi","pmid","arxiv","openalex","title","year","venue",
        "screening_decision","screening_claims","screening_reason","screener","lead_L1","lead_L2","lead_L3","lead_L4","lead_basis"]
rows = []
dec = {}
for i in range(8): dec.update({d["uid"]: d for d in json.load(open(os.path.join(H, f"screening/native_batch_{i}_decisions.json")))})
for r in json.load(open(os.path.join(H, "runs/native_unique.json"))):
    d = dec[r["uid"]]; g = NATIVE.get(r["uid"], ("",) * 5) if d["decision"] == "FULLTEXT" else ("",) * 5
    rows.append(dict(arm="native", uid=r["uid"], database=r["db"], query=r["query"], rank=r["rank"], all_hits=";".join(r["hits"]),
                     doi=r.get("doi") or "", pmid=r.get("pmid") or "", arxiv=r.get("arxiv") or "", openalex=r.get("openalex") or "",
                     title=r["title"], year=r.get("year") or "", venue=r.get("venue") or "", screening_decision=d["decision"],
                     screening_claims=",".join(d.get("claims", [])), screening_reason=d["reason"], screener=SCREENER,
                     lead_L1=g[0], lead_L2=g[1], lead_L3=g[2], lead_L4=g[3], lead_basis=g[4]))
cdec = {d["uid"]: d for d in json.load(open(os.path.join(H, "screening/citation_batch_decisions.json")))}
for r in json.load(open(os.path.join(H, "runs/citations/citation_records.json"))):
    d = cdec[r["uid"]]; g = W[CIT[r["uid"]]] if d["decision"] == "FULLTEXT" else ("",) * 5
    rows.append(dict(arm="citation", uid=r["uid"], database="OpenAlex (citations)", query=f'{r["direction"]} of {r["seed"]}', rank=r.get("rank", ""),
                     all_hits="", seed=r["seed"], direction=r["direction"], openalex=r.get("openalex") or "", title=r["ref"], year=r.get("year") or "",
                     screening_decision=d["decision"], screening_claims=",".join(d.get("claims", [])), screening_reason=d["reason"], screener=SCREENER,
                     lead_L1=g[0], lead_L2=g[1], lead_L3=g[2], lead_L4=g[3], lead_basis=g[4]))
missing = [k for k, v in cdec.items() if v["decision"] == "FULLTEXT" and k not in CIT]
assert not missing, missing
with open(os.path.join(H, "RECORDS.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); [w.writerow({c: row.get(c, "") for c in COLS}) for row in rows]
print(len(rows), "rows")
