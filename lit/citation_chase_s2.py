"""Literature gate §6 stopping rule: one level of backward and forward citation for every new DIRECT/PARTIAL hit from the
Semantic Scholar / proceedings arms (S0414, S0209, S0446, S0460). OpenAlex holds no reference lists for these works,
so backward references are parsed from the PDFs (as for K1-K4, citation_chase.py); forward citations use the OpenAlex
cites: filter. Output: runs/citations/citation_records_s2.json (uids C0298...)."""
import json, os, re, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); M = "hisashi-nakano@nuhw.ac.jp"
SEEDS = {"S0414": ("2502.06343", ["W7197018894", "W4407358740"]), "S0209": ("2310.06100", ["W4387560725"]),
         "S0446": ("2402.07419", ["W4415796791", "W4391801085"]), "S0460": ("2507.02843", ["W7196962552"])}
def get(u):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": f"gate-audit/1.0 (mailto:{M})"}), timeout=90))
        except Exception as e: err = e; time.sleep(5 * (i + 1))                     # noqa: BLE001
    raise err
def refs(arx):
    """Parse the reference list. Numbered styles split on [n]; author-year styles split after an entry-final year
    ('..., 2021.'). S0460's two-column PDF keeps [n] with its text only in -layout extraction."""
    fn = f"{H}/fulltext/{arx}.layout.txt" if os.path.exists(f"{H}/fulltext/{arx}.layout.txt") else f"{H}/fulltext/{arx}.txt"
    t = open(fn).read().replace("\f", "\n")
    m = list(re.finditer(r"\n\s*(References|REFERENCES|R EFERENCES|Bibliography)\s*\n", t)); i = m[0].end()
    end = re.search(r"\n\s*(A\s+)?(Appendix|A PPENDIX|APPENDIX|Supplementary|NeurIPS Paper Checklist)\b", t[i:]); j = i + end.start() if end else len(t)
    block = t[i:j]
    if re.search(r"^\s*\[\d+\]\s+\S", block, re.M):                                  # numbered style
        parts = re.split(r"\n\s*\[(\d+)\]\s*", "\n" + block)[1:]
        ents = [re.sub(r"\s+", " ", parts[k + 1]).strip() for k in range(0, len(parts), 2)]
    else:                                                                               # author-year style
        ents, cur = [], ""
        for l in block.split("\n"):
            s = l.strip()
            if not s or re.fullmatch(r"\d+", s): continue
            cur = (cur + " " + s).strip()
            if re.search(r"(19|20)\d\d[a-z]?\.\s*$", s) or re.search(r"https?://\S+\s*$", s) and re.search(r"(19|20)\d\d", cur):
                ents.append(cur); cur = ""
        if cur: ents.append(cur)
    return [e for e in ents if len(e) > 25]
recs = []
for s, (arx, wids) in SEEDS.items():
    R = refs(arx)
    for n, e in enumerate(R, 1): recs.append(dict(seed=s, direction="backward", rank=n, ref=e))
    nf = 0; seen = set()
    d = get(f"https://api.openalex.org/works?per-page=100&filter=cites:{'|'.join(wids)}&mailto={M}")
    for x in d["results"]:
        if x["id"] in seen: continue
        seen.add(x["id"]); inv = x.get("abstract_inverted_index") or {}
        recs.append(dict(seed=s, direction="forward", openalex=x["id"].rsplit("/", 1)[-1], ref=x["display_name"], year=x.get("publication_year"),
                         abstract=" ".join(t for _, t in sorted((p, t) for t, ps in inv.items() for p in ps))[:1500])); nf += 1
    print(s, "backward", len(R), "forward", nf, "| e.g.", R[0][:80] if R else "", "||", R[-1][:80] if R else "")
    time.sleep(1)
n0 = len(json.load(open(f"{H}/runs/citations/citation_records.json")))
for i, r in enumerate(recs): r["uid"] = f"C{n0 + i:04d}"
json.dump(recs, open(f"{H}/runs/citations/citation_records_s2.json", "w"), indent=1); print("total", len(recs), recs[0]["uid"], "-", recs[-1]["uid"])
