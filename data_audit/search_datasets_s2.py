"""Data audit, Semantic Scholar arm of the dataset search (gate §3; data_audit/SEARCH_IMPLEMENTATION.md §2 and §5).
The five fixed queries, relevance search, first 50 per query, no other filter. Uses the keyed, paced client
lit/s2_client.py. Raw responses -> data_audit/runs/s2_q{k}.json; records -> data_audit/runs/dataset_records_s2.json."""
import json, os, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(HERE, "runs")
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "lit"))
import s2_client                                                                    # noqa: E402
from search_datasets import QUERIES                                                 # noqa: E402  (the five frozen queries)
FIELDS = "paperId,title,abstract,year,venue,externalIds,url"
def main():
    recs, meta, n0 = [], [], len(json.load(open(os.path.join(RUNS, "dataset_records.json")))["records"])
    for k, q in enumerate(QUERIES):
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(q)}&limit=50&fields={FIELDS}"
        d = s2_client.get(url); json.dump(dict(url=url, response=d), open(os.path.join(RUNS, f"s2_q{k}.json"), "w"))
        data = (d or {}).get("data") or []
        for r, x in enumerate(data, 1):
            ext = x.get("externalIds") or {}
            recs.append(dict(source="SemanticScholar", query=q, rank=r, id=x.get("paperId"), title=x.get("title") or "",
                             text=(x.get("abstract") or "")[:1500], year=x.get("year"), url=x.get("url") or "", doi=ext.get("DOI"), arxiv=ext.get("ArXiv")))
        meta.append(dict(source="semanticscholar", query=q, n=len(data), total=(d or {}).get("total"), status="ok" if "data" in (d or {}) else f"error {d}"))
        print("s2", k, len(data), flush=True)
    for i, r in enumerate(recs): r["uid"] = f"D{n0 + i:04d}"
    json.dump(dict(meta=meta, records=recs), open(os.path.join(RUNS, "dataset_records_s2.json"), "w"), indent=1)
    print("records", len(recs), "uids", recs[0]["uid"] if recs else None, "-", recs[-1]["uid"] if recs else None)
if __name__ == "__main__":
    try: main()
    except s2_client.S2Stop as e: print("STOPPED (backoff schedule exhausted):", e); sys.exit(2)
