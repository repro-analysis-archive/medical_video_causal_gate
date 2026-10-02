"""Deduplicate the Semantic Scholar and proceedings records (SEARCH_IMPLEMENTATION.md §5: DOI, then arXiv id, then PMID,
then normalized title) against each other and against the already-screened native and citation records; write
runs/s2_unique.json (uids S0000...) and screening batches screening/s2_batch_<k>.json for records not yet screened."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
norm = lambda t: re.sub(r"[^a-z0-9]", "", (t or "").lower())
def keys(doi=None, arxiv=None, pmid=None, title=None):
    k = []
    if doi: k.append("doi:" + doi.lower().replace("https://doi.org/", ""))
    if arxiv: k.append("arxiv:" + str(arxiv).split("v")[0])
    if pmid: k.append("pmid:" + str(pmid))
    if title and len(norm(title)) > 20: k.append("t:" + norm(title))
    return k
seen = {}
for r in json.load(open(f"{H}/runs/native_unique.json")):
    for k in keys(r.get("doi"), r.get("arxiv"), r.get("pmid"), r.get("title")): seen.setdefault(k, r["uid"])
for r in json.load(open(f"{H}/runs/citations/citation_records.json")):
    for k in keys(None, None, None, r.get("ref") if r.get("openalex") else None): seen.setdefault(k, r["uid"])
uniq, by_key, n_hits = [], {}, 0
for arm in ("S2", "PROC"):
    M = json.load(open(f"{H}/runs/s2/{arm}_merged.json"))
    for qid, blk in M.items():
        for x in blk["records"]:
            n_hits += 1; ext = x.get("externalIds") or {}
            ks = keys(ext.get("DOI"), ext.get("ArXiv"), ext.get("PubMed"), x.get("title"))
            hit = f"{arm}:{qid}:{x['rank']}"
            prev = next((by_key[k] for k in ks if k in by_key), None)
            if prev is not None: prev["hits"].append(hit); continue
            dup = next((seen[k] for k in ks if k in seen), None)
            rec = dict(uid=None, paperId=x["paperId"], db=arm, query=qid, rank=x["rank"], subquery=x.get("subquery"), title=x.get("title") or "",
                       abstract=x.get("abstract") or "", year=x.get("year"), venue=x.get("venue") or "", doi=ext.get("DOI"), arxiv=ext.get("ArXiv"),
                       pmid=ext.get("PubMed"), hits=[hit], duplicate_of=dup)
            for k in ks: by_key[k] = rec
            uniq.append(rec)
for i, r in enumerate(uniq): r["uid"] = f"S{i:04d}"
json.dump(uniq, open(f"{H}/runs/s2_unique.json", "w"), indent=1)
new = [r for r in uniq if not r["duplicate_of"]]
B = 90
for b in range(0, len(new), B):
    json.dump([dict(uid=r["uid"], title=r["title"], abstract=r["abstract"], venue=r["venue"], year=r["year"]) for r in new[b:b + B]],
              open(f"{H}/screening/s2_batch_{b // B}.json", "w"), indent=1)
print(dict(hits=n_hits, unique=len(uniq), already_screened=len(uniq) - len(new), to_screen=len(new), batches=(len(new) + B - 1) // B))
