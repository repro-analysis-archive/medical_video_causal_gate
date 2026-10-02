"""Literature gate: one level of backward and forward citation chasing (SEARCH_IMPLEMENTATION.md §6).
Saved verbatim from the session log: this is the code as run 2026-10-02T03:50Z (inline heredoc), wrapped as a file for
provenance. Backward refs of K1-K4 are parsed from lit/fulltext/*.txt (gitignored; hashes in FULLTEXT_SHA256.txt);
N0712 backward refs and all forward citations come from OpenAlex. A second inline step then numbered the records
C0000-C0297 and wrote screening/citation_batch.json."""
import json, re, urllib.request, time
M="hisashi-nakano@nuhw.ac.jp"
def get(u):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":f"gate-audit/1.0 (mailto:{M})"}),timeout=90))
        except Exception as e: err=e; time.sleep(5*(i+1))
    raise err
recs=[]
for k,f,end in (("K1","2410.00903",r"Supplementary Appendix"),("K2","2507.03897",r"Supplementary Materials"),("K3","2605.07834",r"\n\s*Appendix\s*\n"),("K4","2607.06126",r"\n\s*Appendix\s*\n")):
    t=open(f"fulltext/{f}.txt").read().replace("\f","\n")
    m=re.search(r"\n\s*References\s*\n", t); i=m.end(); j=re.search(end, t[i:]).start()+i
    lines=[l.rstrip() for l in t[i:j].split("\n")]
    entries=[]; cur=""
    for l in lines:
        s=l.strip()
        if not s or re.fullmatch(r"\d+",s): continue
        newent = re.match(r"^[A-ZÀ-Ž][A-Za-zÀ-ž'’\-]+( [A-Z][A-Za-zÀ-ž'’\-]+)?, [A-Z]", s) and not l.startswith("   ") 
        if newent and cur: entries.append(cur); cur=s
        else: cur=(cur+" "+s).strip()
    if cur: entries.append(cur)
    for n,e in enumerate(entries,1): recs.append(dict(seed=k, direction="backward", rank=n, ref=e))
    print(k, len(entries), "| e.g.", entries[0][:90], "||", entries[-1][:90])
w=get(f"https://api.openalex.org/works/W4221163971?mailto={M}"); refs=w.get("referenced_works",[])
for n in range(0,len(refs),50):
    ids="|".join(r.rsplit("/",1)[-1] for r in refs[n:n+50])
    d=get(f"https://api.openalex.org/works?per-page=50&filter=openalex:{ids}&mailto={M}")
    for x in d["results"]:
        inv=x.get("abstract_inverted_index") or {}
        recs.append(dict(seed="N0712", direction="backward", openalex=x["id"].rsplit("/",1)[-1], ref=x["display_name"], year=x.get("publication_year"),
                         abstract=" ".join(t for _,t in sorted((p,t) for t,ps in inv.items() for p in ps))[:1500]))
print("N0712 back", sum(r["seed"]=="N0712" for r in recs))
seeds=["W4403826407","W4415058571","W7160856598","W7167716621","W4221163971","W4294743843"]
cur="*"; nfw=0
while cur:
    d=get(f"https://api.openalex.org/works?per-page=100&cursor={cur}&filter=cites:{'|'.join(seeds)}&mailto={M}")
    for x in d["results"]:
        inv=x.get("abstract_inverted_index") or {}
        rw=set(r.rsplit('/',1)[-1] for r in (x.get("referenced_works") or []))
        recs.append(dict(seed="+".join(s for s in seeds if s in rw) or "?", direction="forward", openalex=x["id"].rsplit("/",1)[-1], ref=x["display_name"],
                         year=x.get("publication_year"), abstract=" ".join(t for _,t in sorted((p,t) for t,ps in inv.items() for p in ps))[:1500])); nfw+=1
    cur=d["meta"].get("next_cursor") if d["results"] else None
print("forward", nfw); json.dump(recs, open("runs/citations/citation_records.json","w"), indent=1); print("total", len(recs))
