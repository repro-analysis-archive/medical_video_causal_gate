"""Data audit: dataset search across the non-Semantic-Scholar sources (data_audit/SEARCH_IMPLEMENTATION.md).
Raw responses -> data_audit/runs/; normalized records -> data_audit/runs/dataset_records.json."""
import html, json, os, re, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(HERE, "runs"); os.makedirs(RUNS, exist_ok=True)
MAIL = "hisashi-nakano@nuhw.ac.jp"; UA = {"User-Agent": f"gate-audit/1.0 (mailto:{MAIL})"}
QUERIES = ["colonoscopy video dataset", "full-procedure colonoscopy", "endoscopy video dataset multi-center",
           "surgical video dataset", "surgical kinematics video dataset"]


def fetch(url, data=None, headers=None, raw=False):
    for i in range(5):
        try:
            req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
            with urllib.request.urlopen(req, timeout=120) as r:
                b = r.read(); return b.decode("utf-8", "replace") if raw else json.loads(b)
        except Exception as e:                                                      # noqa: BLE001
            err = e; time.sleep(5 * (i + 1))
    raise RuntimeError(f"{url}: {err}")


def save(name, obj):
    with open(os.path.join(RUNS, name), "w") as f:
        f.write(obj if isinstance(obj, str) else json.dumps(obj))


def openalex(q, k):
    d = fetch(f"https://api.openalex.org/works?per-page=50&search={urllib.parse.quote(q)}&mailto={MAIL}"); save(f"openalex_q{k}.json", d)
    out = []
    for r, w in enumerate(d["results"], 1):
        inv = w.get("abstract_inverted_index") or {}
        ab = " ".join(t for _, t in sorted((p, t) for t, ps in inv.items() for p in ps))
        out.append(dict(source="OpenAlex", query=q, rank=r, id=w["id"], title=w.get("display_name") or "", text=ab[:1500],
                        year=w.get("publication_year"), url=w.get("doi") or w["id"]))
    return out


def hf(q, k):
    d = fetch(f"https://huggingface.co/api/datasets?search={urllib.parse.quote(q)}&limit=50&full=true"); save(f"hf_q{k}.json", d)
    return [dict(source="HuggingFace", query=q, rank=r, id=x["id"], title=x["id"], text=(x.get("description") or "")[:1500],
                 year=(x.get("createdAt") or "")[:4], url="https://huggingface.co/datasets/" + x["id"]) for r, x in enumerate(d, 1)]


def synapse(q, k):
    body = json.dumps({"queryTerm": q.split(), "start": 0, "size": 50}).encode()
    d = fetch("https://repo-prod.prod.sagebase.org/repo/v1/search", data=body, headers={"Content-Type": "application/json"}); save(f"synapse_q{k}.json", d)
    return [dict(source="Synapse", query=q, rank=r, id=h.get("id"), title=h.get("name") or "", text=(h.get("description") or "")[:1500],
                 year="", url="https://www.synapse.org/#!Synapse:" + str(h.get("id"))) for r, h in enumerate(d.get("hits", []), 1)]


def physionet(q, k):
    t = ""
    for page in range(1, 6):
        tp = fetch(f"https://physionet.org/content/?q={urllib.parse.quote(q)}&page={page}", raw=True)
        save(f"physionet_q{k}_p{page}.html", tp); t += tp
    links = []; seen = set()
    for m in re.finditer(r'<a href="(/content/[^"/]+/[^"]*)"[^>]*>(.*?)</a>', t, re.S):
        href, txt = m.group(1), html.unescape(re.sub("<[^>]+>", "", m.group(2))).strip()
        slug = href.split("/")[2]
        if slug in seen or not txt: continue
        seen.add(slug); links.append((href, txt))
    return [dict(source="PhysioNet", query=q, rank=r, id=h, title=x, text="", year="", url="https://physionet.org" + h)
            for r, (h, x) in enumerate(links[:50], 1)]


def zenodo(q, k):
    hits = []
    for page in (1, 2):
        d = fetch(f"https://zenodo.org/api/records?q={urllib.parse.quote(q)}&size=25&page={page}&sort=bestmatch")
        save(f"zenodo_q{k}_p{page}.json", d); hits += d["hits"]["hits"]
    out = []
    for r, h in enumerate(hits[:50], 1):
        md = h.get("metadata", {})
        out.append(dict(source="Zenodo", query=q, rank=r, id=str(h.get("id")), title=md.get("title") or "",
                        text=re.sub("<[^>]+>", " ", md.get("description") or "")[:1500], year=(md.get("publication_date") or "")[:4],
                        url=h.get("links", {}).get("self_html") or f"https://zenodo.org/records/{h.get('id')}",
                        rtype=(md.get("resource_type") or {}).get("type")))
    return out


def figshare(q, k):
    d = fetch("https://api.figshare.com/v2/articles/search", data=json.dumps({"search_for": q, "page_size": 50}).encode(),
              headers={"Content-Type": "application/json"}); save(f"figshare_q{k}.json", d)
    return [dict(source="Figshare", query=q, rank=r, id=str(x.get("id")), title=x.get("title") or "", text="",
                 year=(x.get("published_date") or "")[:4], url=x.get("url_public_html") or "", rtype=x.get("defined_type_name"))
            for r, x in enumerate(d, 1)]


def grand_challenge():
    out, url, page = [], "https://grand-challenge.org/api/v1/challenges/?limit=100", 0
    while url:
        d = fetch(url); save(f"gc_page{page}.json", d); page += 1
        for c in d["results"]:
            out.append(dict(source="Grand-Challenge", query="(complete listing)", rank=len(out) + 1, id=c.get("slug"),
                            title=c.get("title") or c.get("slug"), text=re.sub("<[^>]+>", " ", c.get("description") or "")[:1500],
                            year=(c.get("start_date") or "")[:4], url=c.get("url")))
        url = d.get("next")
    return out


def endovis():
    t = fetch("https://endovis.grand-challenge.org/", raw=True); save("endovis_home.html", t)
    links = sorted(set(re.findall(r'href="(https?://[a-z0-9\-]+\.grand-challenge\.org/?[^"]*)"', t)))
    sub = sorted(set(re.findall(r'href="(/[^"#?]+/)"', t)))
    pages = {}
    for p in sub:
        if any(s in p for s in ("/media/", "/static/", "/accounts/", "/documentation/")): continue
        try:
            pages[p] = fetch("https://endovis.grand-challenge.org" + p, raw=True); time.sleep(0.5)
        except Exception:                                                           # noqa: BLE001
            pages[p] = ""
    save("endovis_subpages.json", pages)
    for p, h in pages.items():
        links += re.findall(r'href="(https?://[a-z0-9\-]+\.grand-challenge\.org/?[^"]*)"', h)
    links = sorted(set(l.rstrip("/") for l in links if "endovis.grand-challenge.org" not in l and "//grand-challenge.org" not in l))
    return [dict(source="EndoVis", query="(EndoVis pages)", rank=r, id=l, title=l.split("//")[1].split(".")[0], text="", year="", url=l)
            for r, l in enumerate(links, 1)], sorted(pages)


def rerun_paginated():
    """Re-run only Zenodo and PhysioNet with pagination (SEARCH_IMPLEMENTATION.md §4) and merge."""
    p = os.path.join(RUNS, "dataset_records.json"); d = json.load(open(p))
    d["records"] = [r for r in d["records"] if r["source"] not in ("Zenodo", "PhysioNet")]
    d["meta"] = [m for m in d["meta"] if m["source"] not in ("zenodo", "physionet")] + [m for m in d["meta"] if m["source"] in ("zenodo", "physionet") and False]
    for k, q in enumerate(QUERIES):
        for fn in (physionet, zenodo):
            r = fn(q, k); d["records"] += r; d["meta"].append(dict(source=fn.__name__, query=q, n=len(r), status="ok (paginated)"))
            print(fn.__name__, k, len(r), flush=True); time.sleep(1)
    json.dump(d, open(p, "w"), indent=1)


def main():
    recs, meta = [], []
    for k, q in enumerate(QUERIES):
        for fn in (openalex, hf, synapse, physionet, zenodo, figshare):
            try:
                r = fn(q, k); status = "ok"
            except Exception as e:                                                  # noqa: BLE001
                r = []; status = f"FAILED {e!r}"[:200]
            recs += r; meta.append(dict(source=fn.__name__, query=q, n=len(r), status=status)); print(fn.__name__, k, len(r), status, flush=True)
            time.sleep(1)
    gc = grand_challenge(); recs += gc; meta.append(dict(source="grand_challenge", query="(complete)", n=len(gc), status="ok"))
    ev, pages = endovis(); recs += ev; meta.append(dict(source="endovis", query="(pages)", n=len(ev), status="ok", pages=pages))
    print("grand-challenge", len(gc), "endovis links", len(ev))
    json.dump(dict(meta=meta, records=recs), open(os.path.join(RUNS, "dataset_records.json"), "w"), indent=1)


if __name__ == "__main__":
    import sys
    rerun_paginated() if "--paginated" in sys.argv else main()
