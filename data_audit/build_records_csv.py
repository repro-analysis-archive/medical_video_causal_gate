"""Write data_audit/RECORDS.csv: every screened dataset-search record (SEARCH_IMPLEMENTATION.md §3), with source, query,
rank, ids, title, year, screening category, dataset name, mapped dataset id and screener. Covers the original search
(D0000-D1359, screened in ds_batch_0..2) and the Semantic Scholar arm (D1360-D1609, ds_s2_batch)."""
import csv, json, os
H = os.path.dirname(os.path.abspath(__file__))
SCREENER = "screening subagent (general-purpose; rubric data_audit/screening/RUBRIC.md)"
recs = json.load(open(f"{H}/runs/dataset_records.json"))["records"] + json.load(open(f"{H}/runs/dataset_records_s2.json"))["records"]
dec = {}
for f in ["ds_batch_0", "ds_batch_1", "ds_batch_2", "ds_s2_batch"]:
    for d in json.load(open(f"{H}/screening/{f}_decisions.json")): dec[d["uid"]] = d
uid2ds = {}
for e in json.load(open(f"{H}/DATASETS.json")) + json.load(open(f"{H}/DATASETS_S2.json")):
    for u in e.get("uids", []): uid2ds[u] = e["id"]
cols = ["uid", "source", "query", "rank", "id", "doi", "arxiv", "url", "title", "year", "category", "dataset_name", "mapped_dataset_id", "reason", "screener"]
missing = [r["uid"] for r in recs if r["uid"] not in dec]
assert not missing, missing[:5]
with open(f"{H}/RECORDS.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
    for r in recs:
        d = dec[r["uid"]]
        mapped = uid2ds.get(r["uid"]) or d.get("existing_id") or ""
        w.writerow(dict(uid=r["uid"], source=r["source"], query=r["query"], rank=r["rank"], id=r.get("id"), doi=r.get("doi", ""), arxiv=r.get("arxiv", ""),
                        url=r.get("url", ""), title=r.get("title", ""), year=r.get("year", ""), category=d.get("category"), dataset_name=d.get("dataset_name", ""),
                        mapped_dataset_id=mapped, reason=d.get("reason", ""), screener=SCREENER))
print(len(recs), "rows")
