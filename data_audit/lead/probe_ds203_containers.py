"""Decision 002 / DS203_D8_SPEC.md §1: container-level duration and frame rate of every DS203 (Appendix300) full-video
file via HTTP range requests on the OPARA split zip. Reads the zip central directory, each entry's local header, MP4
top-level box headers and the moov box only. Never reads mdat; decodes no frame. STOP (exit 3) if an entry is
compressed or moov cannot be reached."""
import json, os, struct, sys, time, urllib.request
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); RAW = "/media/user/LaCie/medvideo_gate/DS203/moov"; os.makedirs(RAW, exist_ok=True)
B = "https://opara.zih.tu-dresden.de/server/api/core/bitstreams/"
PARTS = [("z01", B + "79c7da37-1528-4b4c-a2bc-cd5902e9d7a3/content", 268435456000), ("z02", B + "58fedbb8-217c-4dbc-a5dd-0aa05db33462/content", 268435456000),
         ("z03", B + "45ddcca7-0ee0-46de-bad6-88602192fcce/content", 268435456000), ("z04", B + "a97390ae-438b-41fd-a0d3-44917a505a3b/content", 268435456000),
         ("z05", B + "c444b1d6-f6e9-4974-a479-54075e95c06c/content", 268435456000), ("zip", B + "19c0d57a-389a-4579-b8b3-9ef5f18586e1/content", 18145831801)]
CUM = [0]
for p in PARTS: CUM.append(CUM[-1] + p[2])
NREQ = [0, 0]
def _get(url, a, b):
    for i in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "gate-audit/1.0 (mailto:hisashi-nakano@nuhw.ac.jp)", "Range": f"bytes={a}-{b}"})
            with urllib.request.urlopen(req, timeout=120) as r:
                if r.status != 206: raise IOError(f"status {r.status}")
                d = r.read(); NREQ[0] += 1; NREQ[1] += len(d); return d
        except Exception as e:                                                       # noqa: BLE001
            err = e; time.sleep(2 * 2 ** i)
    raise RuntimeError(f"range {a}-{b}: {err!r}")
def read(gpos, n):
    """Read n bytes at a global offset across split parts."""
    out = b""
    while n > 0:
        k = max(i for i in range(len(PARTS)) if CUM[i] <= gpos); off = gpos - CUM[k]; m = min(n, PARTS[k][2] - off)
        out += _get(PARTS[k][1], off, off + m - 1); gpos += m; n -= m
    return out
def central_directory():
    zp = len(PARTS) - 1; size = PARTS[zp][2]; tail = _get(PARTS[zp][1], size - 65536, size - 1)
    i = tail.rfind(b"PK\x06\x07"); assert i >= 0, "no zip64 locator"
    disk_z64, off_z64, _ = struct.unpack("<IQI", tail[i + 4:i + 20])
    z = read(CUM[disk_z64] + off_z64, 56); assert z[:4] == b"PK\x06\x06"
    (cd_disk,) = struct.unpack("<I", z[20:24]); n_ent, = struct.unpack("<Q", z[32:40]); cd_size, cd_off = struct.unpack("<QQ", z[40:56])
    cd = read(CUM[cd_disk] + cd_off, cd_size); ents, p = [], 0
    while p < len(cd) and cd[p:p + 4] == b"PK\x01\x02":
        (meth,) = struct.unpack("<H", cd[p + 10:p + 12]); csz, usz = struct.unpack("<II", cd[p + 20:p + 28])
        nl, el, cl, disk = struct.unpack("<HHHH", cd[p + 28:p + 36]); (lho,) = struct.unpack("<I", cd[p + 42:p + 46])
        name = cd[p + 46:p + 46 + nl].decode("utf-8", "replace"); ex = cd[p + 46 + nl:p + 46 + nl + el]; q = 0
        while q + 4 <= len(ex):
            hid, hl = struct.unpack("<HH", ex[q:q + 4]); body = ex[q + 4:q + 4 + hl]
            if hid == 1:
                vals, r = [], 0
                for fld in ("usz", "csz", "lho"):
                    v = {"usz": usz, "csz": csz, "lho": lho}[fld]
                    if v == 0xFFFFFFFF: vals.append((fld, struct.unpack("<Q", body[r:r + 8])[0])); r += 8
                for fld, v in vals:
                    if fld == "usz": usz = v
                    elif fld == "csz": csz = v
                    else: lho = v
                if disk == 0xFFFF: disk = struct.unpack("<I", body[r:r + 4])[0]
            q += 4 + hl
        ents.append(dict(name=name, method=meth, csz=csz, usz=usz, disk=disk, lho=lho)); p += 46 + nl + el + cl
    assert len(ents) == n_ent, (len(ents), n_ent)
    return ents
def boxes(buf, a, b):
    p = a
    while p + 8 <= b:
        sz, typ = struct.unpack(">I4s", buf[p:p + 8]); hdr = 8
        if sz == 1: sz = struct.unpack(">Q", buf[p + 8:p + 16])[0]; hdr = 16
        elif sz == 0: sz = b - p
        yield typ.decode("latin1"), p + hdr, p + sz; p += sz
def parse_moov(m):
    res = dict(tracks=[])
    for t, a, b in boxes(m, 8, len(m)):
        if t == "mvhd":
            v = m[a]; ts, du = (struct.unpack(">IQ", m[a + 20:a + 32]) if v == 1 else struct.unpack(">II", m[a + 12:a + 20]))
            res["mvhd_timescale"], res["mvhd_duration"] = ts, du
        if t == "trak":
            tr = {}
            def walk(x, y):
                for t2, a2, b2 in boxes(m, x, y):
                    if t2 in ("mdia", "minf", "stbl"): walk(a2, b2)
                    elif t2 == "hdlr": tr["handler"] = m[a2 + 8:a2 + 12].decode("latin1")
                    elif t2 == "mdhd":
                        v2 = m[a2]; tr["mdhd_timescale"], tr["mdhd_duration"] = (struct.unpack(">IQ", m[a2 + 20:a2 + 32]) if v2 == 1 else struct.unpack(">II", m[a2 + 12:a2 + 20]))
                    elif t2 in ("stsz", "stz2"): tr["sample_count"] = struct.unpack(">I", m[a2 + 8:a2 + 12])[0]
            walk(a, b); res["tracks"].append(tr)
    return res
def probe(e):
    g = CUM[e["disk"]] + e["lho"]; lh = read(g, 30); assert lh[:4] == b"PK\x03\x04", e["name"]
    nl, el = struct.unpack("<HH", lh[26:30]); start = g + 30 + nl + el; end = start + e["csz"]; p = start; top = []
    while p < end:
        h = read(p, 16); sz, typ = struct.unpack(">I4s", h[:8]); typ = typ.decode("latin1")
        if sz == 1: sz = struct.unpack(">Q", h[8:16])[0]
        elif sz == 0: sz = end - p
        top.append((typ, sz))
        if typ == "moov":
            m = read(p, sz); open(os.path.join(RAW, e["name"].replace("/", "__") + ".moov"), "wb").write(m)
            r = parse_moov(m); r["top_boxes"] = top; return r
        p += sz
    raise RuntimeError(f"moov not found: {e['name']} {top}")
def main():
    ents = central_directory()
    vids = [e for e in ents if e["name"].startswith("Full_Videos/") and e["name"].endswith(".mp4")]
    comp = [e["name"] for e in vids if e["method"] != 0]
    print("entries", len(ents), "full-video mp4", len(vids), "compressed", len(comp), flush=True)
    if comp: print("STOP: compressed entries", comp[:5]); sys.exit(3)
    cache = os.path.join(OUT, "DS203_container_probe.json"); res = json.load(open(cache)) if os.path.exists(cache) else {}
    for i, e in enumerate(vids):
        if e["name"] in res: continue
        try: r = probe(e)
        except Exception as ex: print("STOP: probe failed", e["name"], repr(ex)); json.dump(res, open(cache, "w"), indent=1); sys.exit(3)  # noqa: BLE001
        v = [t for t in r["tracks"] if t.get("handler") == "vide"]
        if len(v) != 1 or "sample_count" not in v[0]: print("STOP: no single video track", e["name"], r); json.dump(res, open(cache, "w"), indent=1); sys.exit(3)
        v = v[0]; dur_v = v["mdhd_duration"] / v["mdhd_timescale"]
        res[e["name"]] = dict(csz=e["csz"], mvhd_duration_s=r["mvhd_duration"] / r["mvhd_timescale"], video_duration_s=dur_v, frames=v["sample_count"],
                              fps=v["sample_count"] / dur_v if dur_v > 0 else None, top_boxes=r["top_boxes"][:6])
        if i % 20 == 0: print(i, e["name"], round(dur_v, 1), "s", v["sample_count"], "frames", f"req={NREQ[0]} bytes={NREQ[1]/1e6:.1f}MB", flush=True); json.dump(res, open(cache, "w"), indent=1)
    json.dump(res, open(cache, "w"), indent=1)
    print("done", len(res), "files", f"requests={NREQ[0]} bytes_read={NREQ[1]/1e6:.1f}MB")
if __name__ == "__main__": main()
