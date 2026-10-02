"""Literature gate: Semantic Scholar and proceedings arms (split-and-merge, lit/SEARCH_IMPLEMENTATION.md §3).
Paced and resumable: every sub-query response is cached under lit/runs/s2/. Usage: python lit/search_s2.py"""
import itertools, json, os, sys, time, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "runs", "s2"); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)
from search_native import Q                                                     # noqa: E402  (identical query blocks)

FIELDS = "paperId,title,abstract,year,venue,publicationVenue,externalIds,publicationDate"
PROBES = {"MICCAI": "arXiv:1505.04597", "IPMI": "arXiv:1703.05921", "MIDL": "arXiv:1804.03999",
          "NeurIPS": "arXiv:1706.03762", "ICML": "arXiv:2002.05709", "CLeaR": "arXiv:2302.08070", "UAI": "arXiv:1803.05407"}
FALLBACK = {"CLeaR": ["Conference on Causal Learning and Reasoning", "CLeaR"]}
LOG = open(os.path.join(OUT, "run.log"), "a")


def log(*a):
    s = time.strftime("%Y-%m-%dT%H:%M:%SZ ", time.gmtime()) + " ".join(str(x) for x in a); print(s, flush=True); LOG.write(s + "\n"); LOG.flush()


def get(url, tries=12):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "gate-audit/1.0"}), timeout=90) as r:
                d = json.load(r); time.sleep(4); return d
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                w = min(30 * 2 ** i, 900); log("HTTP", e.code, "wait", w); time.sleep(w); continue
            log("HTTP", e.code, url); return {"error": e.code}
        except Exception as e:                                                      # noqa: BLE001
            w = min(30 * 2 ** i, 900); log("ERR", repr(e), "wait", w); time.sleep(w)
    log("GAVE UP", url); return None


def cached(name, url):
    p = os.path.join(OUT, name + ".json")
    if os.path.exists(p): return json.load(open(p))
    d = get(url)
    if d is None: return None
    json.dump(dict(url=url, response=d), open(p, "w")); return dict(url=url, response=d)


def venues():
    names = {}
    for v, pid in PROBES.items():
        r = cached(f"probe_{v}", f"https://api.semanticscholar.org/graph/v1/paper/{pid}?fields=venue,publicationVenue")
        pv = ((r or {}).get("response") or {}).get("publicationVenue") or {}
        n = [pv["name"]] + pv.get("alternate_names", []) if pv.get("name") else []
        names[v] = n if n else FALLBACK.get(v, [])
        log("venue", v, "->", names[v][:3])
    json.dump(names, open(os.path.join(OUT, "venues_resolved.json"), "w"), indent=1)
    return names


def subqueries(blocks):
    return [" ".join(c) for c in itertools.product(*blocks)]


def run_arm(arm, venue_filter):
    merged_all = {}
    for qid, blocks in Q.items():
        subs = subqueries(blocks); lists = []
        for i, sq in enumerate(subs):
            u = ("https://api.semanticscholar.org/graph/v1/paper/search?limit=100&publicationDateOrYear=2018-01-01:2026-10-02"
                 f"&fields={FIELDS}&query={urllib.parse.quote(sq)}" + (f"&venue={urllib.parse.quote(venue_filter)}" if venue_filter else ""))
            r = cached(f"{arm}_{qid}_{i:03d}", u)
            data = (((r or {}).get("response") or {}).get("data")) or []
            lists.append(data); log(arm, qid, i, repr(sq), "->", len(data))
        seen, merged, depth = set(), [], max((len(l) for l in lists), default=0)
        for k in range(depth):
            for j, l in enumerate(lists):
                if k < len(l) and l[k]["paperId"] not in seen and len(merged) < 100:
                    seen.add(l[k]["paperId"]); merged.append(dict(l[k], subquery=subs[j], subrank=k + 1, rank=len(merged) + 1))
        merged_all[qid] = dict(n_subqueries=len(subs), n_failed=sum(1 for i in range(len(subs))
                               if not os.path.exists(os.path.join(OUT, f"{arm}_{qid}_{i:03d}.json"))), records=merged)
        log(arm, qid, "merged unique", len(merged))
    json.dump(merged_all, open(os.path.join(OUT, f"{arm}_merged.json"), "w"), indent=1)


def main():
    v = venues()
    vf = ",".join(n for names in v.values() for n in names)
    run_arm("S2", None)
    run_arm("PROC", vf)
    log("DONE")


if __name__ == "__main__":
    main()
