"""Literature gate: PubMed, arXiv, OpenAlex searches (native boolean). Implements lit/SEARCH_IMPLEMENTATION.md.
Writes raw responses to lit/runs/ and a normalized record list to lit/runs/native_records.json."""
import json, os, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(HERE, "runs"); os.makedirs(RUNS, exist_ok=True)
MAIL = "hisashi-nakano@nuhw.ac.jp"
Q = {
    "Q1": [["medical video", "surgical video", "endoscopy", "colonoscopy", "ultrasound video", "fluoroscopy"],
           ["causal", "treatment effect", "confounding", "propensity", "counterfactual"],
           ["representation", "embedding", "foundation model", "generative"]],
    "Q2": [["image embedding", "foundation model", "deep features"], ["site", "scanner", "batch", "acquisition"],
           ["confounding", "causal", "propensity"]],
    "Q3": [["semi-synthetic", "benchmark"], ["causal"], ["medical image", "medical video"]],
    "Q4": [["domain-invariant", "site-invariant", "harmonization", "debiasing", "adversarial"],
           ["causal", "treatment effect", "propensity", "confounding"], ["longitudinal", "sequential", "time-varying"]],
}


def term(t, style):
    if style == "arxiv": return f'all:"{t}"' if (" " in t or "-" in t) else f"all:{t}"
    return f'"{t}"' if (" " in t or "-" in t) else t


def boolean(blocks, style):
    return " AND ".join("(" + " OR ".join(term(t, style) for t in b) + ")" for b in blocks)


def get(url, binary=False, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"gate-audit/1.0 (mailto:{MAIL})"})
            with urllib.request.urlopen(req, timeout=120) as r:
                b = r.read(); return b if binary else b.decode("utf-8")
        except Exception as e:                                          # noqa: BLE001
            time.sleep(5 * (i + 1)); err = e
    raise RuntimeError(f"failed {url}: {err}")


def pubmed(qid, blocks):
    q = boolean(blocks, "pubmed")
    u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&sort=relevance&retmax=100"
         f"&datetype=pdat&mindate=2018/01/01&maxdate=2026/10/02&term={urllib.parse.quote(q)}&email={MAIL}")
    s = json.loads(get(u)); ids = s["esearchresult"]["idlist"]
    open(os.path.join(RUNS, f"pubmed_{qid}_esearch.json"), "w").write(json.dumps(s, indent=1))
    recs = []
    if ids:
        x = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id={','.join(ids)}&email={MAIL}")
        open(os.path.join(RUNS, f"pubmed_{qid}_efetch.xml"), "w").write(x)
        root = ET.fromstring(x); by = {}
        for art in root.findall(".//PubmedArticle"):
            pmid = art.findtext(".//PMID"); a = art.find(".//Article")
            title = "".join(a.find("ArticleTitle").itertext()) if a is not None and a.find("ArticleTitle") is not None else ""
            abst = " ".join("".join(t.itertext()) for t in art.findall(".//Abstract/AbstractText"))
            doi = next((e.text for e in art.findall(".//ArticleId") if e.get("IdType") == "doi"), None)
            year = art.findtext(".//PubDate/Year") or art.findtext(".//PubDate/MedlineDate") or ""
            venue = art.findtext(".//Journal/Title") or ""
            by[pmid] = dict(title=title, abstract=abst, doi=doi, year=year[:4], venue=venue, pmid=pmid)
        for rank, pmid in enumerate(ids, 1):
            r = by.get(pmid, dict(pmid=pmid, title="", abstract="")); recs.append(dict(db="PubMed", query=qid, rank=rank, **r))
    return q, int(s["esearchresult"]["count"]), recs


def arxiv(qid, blocks):
    q = (boolean(blocks, "arxiv") + " AND (cat:cs.CV OR cat:cs.LG OR cat:stat.ME OR cat:stat.ML)"
         " AND submittedDate:[201801010000 TO 202610022359]")
    u = ("https://export.arxiv.org/api/query?sortBy=relevance&sortOrder=descending&start=0&max_results=100&search_query="
         + urllib.parse.quote(q))
    x = get(u); open(os.path.join(RUNS, f"arxiv_{qid}.xml"), "w").write(x)
    ns = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/"}
    root = ET.fromstring(x); total = int(root.findtext("o:totalResults", default="0", namespaces=ns)); recs = []
    for rank, e in enumerate(root.findall("a:entry", ns), 1):
        aid = e.findtext("a:id", namespaces=ns).rsplit("/abs/", 1)[-1]
        recs.append(dict(db="arXiv", query=qid, rank=rank, arxiv=re.sub(r"v\d+$", "", aid),
                         title=" ".join(e.findtext("a:title", namespaces=ns).split()),
                         abstract=" ".join(e.findtext("a:summary", namespaces=ns).split()),
                         year=e.findtext("a:published", namespaces=ns)[:4], venue="arXiv",
                         doi=e.findtext("{http://arxiv.org/schemas/atom}doi")))
    time.sleep(3.5)
    return q, total, recs


def openalex(qid, blocks):
    q = boolean(blocks, "openalex")
    u = ("https://api.openalex.org/works?per-page=100&page=1&filter=from_publication_date:2018-01-01,to_publication_date:2026-10-02"
         f"&search={urllib.parse.quote(q)}&mailto={MAIL}")
    d = json.loads(get(u)); open(os.path.join(RUNS, f"openalex_{qid}.json"), "w").write(json.dumps(d))
    recs = []
    for rank, w in enumerate(d["results"], 1):
        inv = w.get("abstract_inverted_index") or {}
        pos = sorted((p, t) for t, ps in inv.items() for p in ps); abst = " ".join(t for _, t in pos)
        ids = w.get("ids", {}); loc = (w.get("primary_location") or {}).get("source") or {}
        recs.append(dict(db="OpenAlex", query=qid, rank=rank, openalex=w["id"].rsplit("/", 1)[-1],
                         doi=(w.get("doi") or "").replace("https://doi.org/", "") or None, pmid=(ids.get("pmid") or "").rsplit("/", 1)[-1] or None,
                         title=w.get("display_name") or "", abstract=abst, year=str(w.get("publication_year") or ""),
                         venue=loc.get("display_name") or ""))
    return q, d["meta"]["count"], recs


def main():
    out, meta = [], []
    for qid, blocks in Q.items():
        for name, fn in (("PubMed", pubmed), ("arXiv", arxiv), ("OpenAlex", openalex)):
            q, total, recs = fn(qid, blocks)
            meta.append(dict(db=name, query=qid, query_string=q, total_hits=total, retrieved=len(recs),
                             utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
            out += recs; print(name, qid, "hits", total, "retrieved", len(recs), flush=True)
    json.dump(dict(meta=meta, records=out), open(os.path.join(RUNS, "native_records.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
