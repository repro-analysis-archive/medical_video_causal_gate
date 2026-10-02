"""DS203 pre-protocol facts (no new download): per-site distributions of total duration, appendix-visible timestamp
and post-timestamp duration (from the probe of 146f69b), frame rates, and resolutions / aspect ratios parsed from the
moov boxes already saved on LaCie (tkhd width/height; avc1/hvc1 sample-entry width/height)."""
import glob, json, os, re, struct, collections
import numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "out")
def boxes(m, a, b):
    p = a
    while p + 8 <= b:
        sz, t = struct.unpack(">I4s", m[p:p + 8]); h = 8
        if sz == 1: sz = struct.unpack(">Q", m[p + 8:p + 16])[0]; h = 16
        elif sz == 0: sz = b - p
        yield t.decode("latin1"), p + h, p + sz; p += sz
def video_info(m):
    info = {}
    def walk(a, b, in_vide=False):
        for t, x, y in boxes(m, a, b):
            if t == "trak":
                tr = {}; walk_trak(x, y, tr)
                if tr.get("handler") == "vide": info.update(tr)
    def walk_trak(a, b, tr):
        for t, x, y in boxes(m, a, b):
            if t == "tkhd":
                v = m[x]; o = x + (88 if v == 1 else 76); w, h = struct.unpack(">II", m[o:o + 8]); tr["tkhd_w"], tr["tkhd_h"] = w / 65536, h / 65536
            elif t in ("mdia", "minf", "stbl"): walk_trak(x, y, tr)
            elif t == "hdlr": tr["handler"] = m[x + 8:x + 12].decode("latin1")
            elif t == "stsd":
                e = x + 8; sz, fmt = struct.unpack(">I4s", m[e:e + 8]); tr["codec"] = fmt.decode("latin1")
                tr["enc_w"], tr["enc_h"] = struct.unpack(">HH", m[e + 32:e + 36])
                sub = m[e + 86:e + sz]                      # child boxes of the visual sample entry (pasp etc.)
                i = sub.find(b"pasp")
                if i >= 4: tr["pasp"] = struct.unpack(">II", sub[i + 4:i + 12])
    walk(8, len(m)); return info
P = json.load(open(os.path.join(OUT, "DS203_container_probe.json")))
vi = {}
for f in glob.glob("/media/user/LaCie/medvideo_gate/DS203/moov/*.moov"):
    name = os.path.basename(f)[:-5].replace("__", "/"); vi[name] = video_info(open(f, "rb").read())
C = pd.read_csv(os.path.join(OUT, "DS203_d8_cases.csv"))
C["post_s"] = C.duration_s - C.timestamp_s
q = lambda s: dict(n=int(s.size), min=round(float(s.min()) / 60, 1), q25=round(float(s.quantile(.25)) / 60, 1), median=round(float(s.median()) / 60, 1),
                   q75=round(float(s.quantile(.75)) / 60, 1), max=round(float(s.max()) / 60, 1))
res = {"minutes_by_site": {int(c): dict(total_duration=q(g.duration_s), appendix_visible_timestamp=q(g.timestamp_s), post_timestamp=q(g.post_s))
                           for c, g in C.groupby("center")}}
rows = []
for name, r in P.items():
    c = int(re.search(r"Center(\d)", name).group(1)); v = vi.get(name, {})
    rows.append(dict(center=c, fps=round(r["fps"], 2), codec=v.get("codec"), w=v.get("enc_w"), h=v.get("enc_h"), tkw=v.get("tkhd_w"), tkh=v.get("tkhd_h"), pasp=str(v.get("pasp"))))
F = pd.DataFrame(rows); F["res"] = F.w.astype(str) + "x" + F.h.astype(str); F["aspect"] = (F.tkw / F.tkh).round(3)
res["files_by_site"] = {int(c): dict(files=int(len(g)), fps=dict(collections.Counter(g.fps).most_common(4)), resolution=dict(collections.Counter(g.res).most_common(4)),
                        display_aspect=dict(collections.Counter(g.aspect).most_common(3)), codec=dict(collections.Counter(g.codec)), pasp=dict(collections.Counter(g.pasp).most_common(2)))
                        for c, g in F.groupby("center")}
json.dump(res, open(os.path.join(OUT, "DS203_preprotocol_facts.json"), "w"), indent=1); print(json.dumps(res, indent=1))
