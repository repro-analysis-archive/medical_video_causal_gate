"""Lead verification (LEAD_VERIFICATION_SPEC.md §2): download the 2,509 DS024 episode parquet files (no mp4) at Open-H
revision e29dda7c to LaCie, and record sha256 + size against the tree listing."""
import concurrent.futures as cf, hashlib, json, os, time, urllib.request
REV = "e29dda7cabf2a2626634c7822db27695553ae523"; ROOT = "/media/user/LaCie/medvideo_gate/DS024"
OUT = os.path.join(ROOT, "parquet"); os.makedirs(OUT, exist_ok=True)
tree = json.load(open(os.path.join(ROOT, "tree.json")))
pq = [f for f in tree if f.get("path", "").endswith(".parquet")]
assert len(pq) == 2509 and not any(f["path"].endswith(".mp4") for f in pq)
def get(f):
    rel = f["path"].split("Surgical/jhu/lcsr/smarts/")[1]; dst = os.path.join(OUT, rel)
    if os.path.exists(dst) and os.path.getsize(dst) == f["size"]: return rel, "cached"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    url = f"https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Open-H-Embodiment/resolve/{REV}/{f['path']}"
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "gate-audit/1.0"}), timeout=120) as r: b = r.read()
            if len(b) != f["size"]: raise IOError(f"size {len(b)} != {f['size']}")
            open(dst, "wb").write(b); return rel, "ok"
        except Exception as e:                                                       # noqa: BLE001
            err = e; time.sleep(3 * (i + 1))
    return rel, f"FAILED {err!r}"
with cf.ThreadPoolExecutor(8) as ex: res = list(ex.map(get, pq))
bad = [r for r in res if r[1].startswith("FAILED")]
man = {rel: hashlib.sha256(open(os.path.join(OUT, rel), "rb").read()).hexdigest() for rel, s in res if not s.startswith("FAILED")}
json.dump(dict(revision=REV, n=len(man), failed=bad, sha256=man), open(os.path.join(ROOT, "parquet_manifest.json"), "w"), indent=1)
print(len(man), "ok;", len(bad), "failed")
