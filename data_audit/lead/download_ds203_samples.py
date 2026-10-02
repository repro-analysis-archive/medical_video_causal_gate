"""Decision 003 §1: download ONE full sample video per centre (2-5) from the OPARA split zip by HTTP range requests
over the stored entry (64 MB chunks, 4 parallel connections); record sha256, size and measured throughput."""
import concurrent.futures as cf, hashlib, json, os, struct, time
import probe_ds203_containers as P
OUTD = "/media/user/LaCie/medvideo_gate/DS203/samples"; os.makedirs(OUTD, exist_ok=True)
H = os.path.dirname(os.path.abspath(__file__)); SEL = json.load(open(os.path.join(H, "out", "DS203_sample_selection.json")))
CH = 64 * 2 ** 20
ents = {e["name"]: e for e in P.central_directory()}
log = {}
for c, s in SEL.items():
    e = ents[s["file"][0]]; assert e["method"] == 0
    g = P.CUM[e["disk"]] + e["lho"]; lh = P.read(g, 30); nl, el = struct.unpack("<HH", lh[26:30]); start = g + 30 + nl + el; n = e["csz"]
    dst = os.path.join(OUTD, os.path.basename(e["name"]))
    with open(dst, "wb") as f: f.truncate(n)
    t0 = time.time()
    def chunk(k):
        a = k * CH; m = min(CH, n - a); d = P.read(start + a, m)
        with open(dst, "r+b") as f: f.seek(a); f.write(d)
        return m
    with cf.ThreadPoolExecutor(4) as ex: got = sum(ex.map(chunk, range((n + CH - 1) // CH)))
    dt = time.time() - t0; assert got == n and os.path.getsize(dst) == n
    h = hashlib.sha256()
    with open(dst, "rb") as f:
        for b in iter(lambda: f.read(2 ** 24), b""): h.update(b)
    log[c] = dict(file=e["name"], local=dst, bytes=n, seconds=round(dt, 1), MBps=round(n / dt / 1e6, 1), sha256=h.hexdigest())
    print(c, log[c], flush=True)
json.dump(log, open(os.path.join(H, "out", "DS203_sample_download.json"), "w"), indent=1)
tot_b = sum(v["bytes"] for v in log.values()); tot_t = sum(v["seconds"] for v in log.values())
print("aggregate MB/s", round(tot_b / tot_t / 1e6, 1), "-> 1.69 TB in", round(1.692471368687e12 / (tot_b / tot_t) / 3600, 1), "h")
