"""DS203 per-centre codec facts from the moov boxes already saved on LaCie (146f69b / 67d8fcf); no mdat byte is read and
no frame is decoded. Per file: sample-entry codec, avcC profile/level, SPS chroma format / bit depth / frame_mbs_only /
max_num_ref_frames, ctts presence (B-frame reordering), stss keyframe interval, stts constant-frame-rate check, encoder
tags in udta, and bitrate = stored size / duration from the container probe."""
import collections, glob, json, os, re, struct
import numpy as np

H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "out"); MOOV = "/media/user/LaCie/medvideo_gate/DS203/moov"


def boxes(m, a, b):  # copied from ds203_preprotocol_facts.py (not imported: that script runs and writes on import)
    p = a
    while p + 8 <= b:
        sz, t = struct.unpack(">I4s", m[p:p + 8]); h = 8
        if sz == 1: sz = struct.unpack(">Q", m[p + 8:p + 16])[0]; h = 16
        elif sz == 0: sz = b - p
        yield t.decode("latin1"), p + h, p + sz; p += sz


class Bits:
    def __init__(s, b): s.b, s.p = b, 0
    def u(s, n):
        v = 0
        for _ in range(n): v = (v << 1) | ((s.b[s.p >> 3] >> (7 - (s.p & 7))) & 1); s.p += 1
        return v
    def ue(s):
        z = 0
        while s.u(1) == 0: z += 1
        return (1 << z) - 1 + s.u(z)
    def se(s):
        k = s.ue(); return (k + 1) // 2 if k & 1 else -(k // 2)


def sps_fields(nal):
    rbsp = re.sub(b"\x00\x00\x03", b"\x00\x00", nal[1:]); r = Bits(rbsp)
    d = dict(profile_idc=r.u(8), constraint_flags=r.u(8), level_idc=r.u(8)); r.ue()
    d["chroma_format_idc"], d["bit_depth_luma"] = 1, 8
    if d["profile_idc"] in (100, 110, 122, 244, 44, 83, 86, 118, 128, 138, 139, 134, 135):
        d["chroma_format_idc"] = r.ue()
        if d["chroma_format_idc"] == 3: r.u(1)
        d["bit_depth_luma"] = r.ue() + 8; r.ue(); r.u(1)
        if r.u(1): d["note"] = "seq_scaling_matrix present: later fields not parsed"; return d
    r.ue(); poc = r.ue()
    if poc == 0: r.ue()
    elif poc == 1:
        r.u(1); r.se(); r.se(); [r.se() for _ in range(r.ue())]
    d["max_num_ref_frames"] = r.ue(); r.u(1); r.ue(); r.ue(); d["frame_mbs_only"] = r.u(1)
    return d


def trak_facts(m, a, b, f):
    for t, x, y in boxes(m, a, b):
        if t in ("mdia", "minf", "stbl"): trak_facts(m, x, y, f)
        elif t == "hdlr": f["handler"] = m[x + 8:x + 12].decode("latin1")
        elif t == "mdhd": v = m[x]; f["timescale"] = struct.unpack(">I", m[x + (20 if v == 1 else 12):][:4])[0]
        elif t == "stsd":
            e = x + 8; sz, fmt = struct.unpack(">I4s", m[e:e + 8]); f["codec"] = fmt.decode("latin1")
            f["width"], f["height"] = struct.unpack(">HH", m[e + 32:e + 36])
            f["compressorname"] = m[e + 51:e + 51 + m[e + 50]].decode("latin1", "replace")
            sub = m[e + 86:e + sz]; i = sub.find(b"avcC")
            if i >= 4:
                c = sub[i + 4:]; f["avcC_profile"], f["avcC_level"] = c[1], c[3]
                n_sps = c[5] & 31; L = struct.unpack(">H", c[6:8])[0]
                if n_sps: f.update({"sps_" + k: v for k, v in sps_fields(c[8:8 + L]).items()})
            j = sub.find(b"btrt")
            if j >= 4: f["btrt_max_bps"], f["btrt_avg_bps"] = struct.unpack(">II", sub[j + 8:j + 16])
        elif t == "stss":
            n = struct.unpack(">I", m[x + 4:x + 8])[0]; f["stss"] = np.frombuffer(m[x + 8:x + 8 + 4 * n], ">u4").astype(np.int64)
        elif t == "stsz": f["n_samples"] = struct.unpack(">I", m[x + 8:x + 12])[0]
        elif t == "ctts": f["has_ctts"] = True
        elif t == "stts":
            n = struct.unpack(">I", m[x + 4:x + 8])[0]; e = np.frombuffer(m[x + 8:x + 8 + 8 * n], ">u4").reshape(-1, 2)
            f["stts_distinct_deltas"] = sorted({int(v) for v in e[:, 1]})[:5]; f["stts_main_delta"] = int(e[np.argmax(e[:, 0]), 1])


def file_facts(m):
    vid, tags = {}, []
    for t, x, y in boxes(m, 8, len(m)):
        if t == "trak":
            f = {}; trak_facts(m, x, y, f)
            if f.get("handler") == "vide": vid = f
        elif t == "udta":
            u = m[x:y]
            for key in (b"\xa9too", b"\xa9enc"):
                i = u.find(key)
                if i >= 0 and u[i + 8:i + 12] == b"data":
                    L = struct.unpack(">I", u[i + 4:i + 8])[0]; tags.append(u[i + 20:i + 4 + L].decode("latin1", "replace"))
    vid["udta_encoder_tags"] = sorted(set(tags)); return vid


def summarise(v, fps):
    s = v.pop("stss", None); n = v.get("n_samples")
    if s is None: v["keyframes"] = "no stss box: every sample is a sync sample (intra-only)"
    else:
        g = np.diff(s)
        v.update(n_keyframes=int(len(s)), gop_frames_median=float(np.median(g)) if len(g) else None, gop_frames_min=int(g.min()) if len(g) else None,
                 gop_frames_max=int(g.max()) if len(g) else None, gop_seconds_median=round(float(np.median(g)) / fps, 3) if len(g) else None)
    v["cfr"] = len(v.get("stts_distinct_deltas", [0, 0])) == 1
    return v


if __name__ == "__main__":
    P = json.load(open(os.path.join(OUT, "DS203_container_probe.json")))
    per_file = {}
    for fpath in sorted(glob.glob(os.path.join(MOOV, "*.moov"))):
        name = os.path.basename(fpath)[:-5].replace("__", "/"); r = P[name]
        v = summarise(file_facts(open(fpath, "rb").read()), r["fps"])
        v["mbps"] = round(r["csz"] * 8 / r["video_duration_s"] / 1e6, 2) if r.get("video_duration_s") else None
        v.update(center=int(re.search(r"Center(\d)", name).group(1)), fps=round(r["fps"], 3), duration_s=r.get("video_duration_s"), stored_bytes=r["csz"])
        per_file[name] = v
    by = collections.defaultdict(list)
    for k, v in per_file.items(): by[v["center"]].append(v)
    C = lambda xs: dict(collections.Counter(xs).most_common(6))
    q = lambda xs: dict(min=round(float(np.min(xs)), 2), median=round(float(np.median(xs)), 2), max=round(float(np.max(xs)), 2)) if len(xs) else None
    centre = {}
    for c, L in sorted(by.items()):
        res_ = collections.defaultdict(list)
        for v in L: res_[f"{v['width']}x{v['height']}@{v['fps']:g}"].append(v)
        centre[c] = dict(files=len(L), codec=C(v.get("codec") for v in L),
            formats={k: dict(files=len(g), hours=round(sum(v["duration_s"] or 0 for v in g) / 3600, 2), mbps=q([v["mbps"] for v in g if v["mbps"]]),
                             gop_frames_median=float(np.median([v["gop_frames_median"] for v in g if v.get("gop_frames_median")]))) for k, g in sorted(res_.items(), key=lambda kv: -len(kv[1]))},
            profile_level=C(f"profile_idc {v.get('avcC_profile')} level_idc {v.get('avcC_level')}" for v in L),
            chroma_bitdepth=C(f"chroma_format_idc {v.get('sps_chroma_format_idc')} / {v.get('sps_bit_depth_luma')}-bit" for v in L),
            frame_mbs_only=C(v.get("sps_frame_mbs_only") for v in L), max_num_ref_frames=C(v.get("sps_max_num_ref_frames") for v in L),
            b_frames_ctts=C(bool(v.get("has_ctts")) for v in L), cfr=C(v["cfr"] for v in L), fps=C(v["fps"] for v in L),
            gop_frames_median=C(v.get("gop_frames_median") for v in L), gop_seconds=q([v["gop_seconds_median"] for v in L if v.get("gop_seconds_median")]),
            gop_frames_range=[min(v.get("gop_frames_min") or 0 for v in L), max(v.get("gop_frames_max") or 0 for v in L)],
            compressorname=C(v.get("compressorname") for v in L), udta_encoder_tags=C(t for v in L for t in v["udta_encoder_tags"]),
            mbps=q([v["mbps"] for v in L if v["mbps"]]), hours=round(sum(v["duration_s"] or 0 for v in L) / 3600, 2), tb=round(sum(v["stored_bytes"] for v in L) / 1e12, 3))
    json.dump(dict(note=__doc__, by_centre=centre, per_file=per_file), open(os.path.join(OUT, "DS203_codec_facts.json"), "w"), indent=1, default=str)
    print(json.dumps(centre, indent=1, default=str))
