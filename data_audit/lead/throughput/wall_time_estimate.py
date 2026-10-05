"""Step 3.5: per-model x per-grid-rate wall time for ALL DS203 full videos (403 files, from out/DS203_codec_facts.json),
combining three separately measured or estimated components, each a lower-bound style rate model:
  I/O    bytes read from LaCie / sustained O_DIRECT read rate (lacie_read_throughput.json). seq and skip read every
         byte; hybrid reads the fraction of frames it decodes (single-stream NVDEC count) plus 12 ms per seek.
  decode per centre format: hours / aggregate decode speed (x realtime) measured on the matching synthetic video
         (throughput_decode.json + throughput_decode_addendum.json), best of {CPU 5x4 threads, NVDEC 4 sessions,
         both together} x {seq, hybrid, skip}; dense-clip models (documented setting) need seq.
  model  GPU-h on the RTX 4500 Ada from the 052590c FLOPs/input at 30% of dense BF16 peak, with inputs per video-hour
         = 3600 R / frames_per_input on a fixed grid of R frames/s (clip models: non-overlapping clips of consecutive
         grid frames); the 'doc' column uses the 052590c documented sampling instead (rescaled from 145.6 h to all files).
Wall time if the three stages are pipelined = max(component); the bottleneck is the arg max. Serial sum also given.
Resizing / colour conversion of sampled frames and host<->GPU copies of model inputs are not included."""
import json, os, statistics
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "..", "out")
J = lambda f: json.load(open(os.path.join(OUT, f)))
codec, dec, io, fm, ref = J("DS203_codec_facts.json"), J("throughput_decode.json"), J("lacie_read_throughput.json"), J("fm_compute_estimate.json"), J("cosmos_reference_entry.json")
add = J("throughput_decode_addendum.json")
RATES = (0.5, 1, 2, 4); IO_BPS = io["sustained"]["MBps"] * 1e6; SEEK_S = 0.012
SYN = {"C1": "C1_1080p30", ("C2", 1080): "C2_1080p25", ("C2", 2160): "C2_2160p25", ("C3", 2160): "C3_2160p25", ("C3", 1080): "C2_1080p25", "C4": "C4_1080p50", "C5": "C5_1080p50"}
fmt = {}  # synthetic format -> (hours, bytes)
for name, v in codec["per_file"].items():
    c = f"C{v['center']}"; key = SYN.get(c) or SYN[(c, v["height"])]
    h, b = fmt.get(key, (0.0, 0)); fmt[key] = (h + (v["duration_s"] or 0) / 3600, b + v["stored_bytes"])
HOURS = sum(h for h, _ in fmt.values()); BYTES = sum(b for _, b in fmt.values())
single = {(r["file"], r["device"], r["mode"], r["rate"]): r for r in dec["single"] + add["single"]}
single.update({(r["file"], r["device"], r["mode"], r["rate"]): dict(r, remeasured=True) for r in add["remeasured_rows"]})  # rows that overlapped the skip check
agg = {(r["file"], r["device"], r["mode"], r["rate"]): r for r in dec["aggregate"] + add["aggregate"]}
DEVS = ("cpu", "nvdec", "cpu+nvdec"); MODES = ("seq", "hybrid", "skip")
def speed(f, dev, mode, rate):  # aggregate x realtime
    if mode == "seq":  # seq aggregate measured at R=1; R changes only the selected-frame copies -> scale by single-stream ratio
        d1 = "nvdec" if dev == "cpu+nvdec" else dev
        return agg[(f, dev, "seq", 1)]["x_realtime_aggregate"] * single[(f, d1, "seq", rate)]["x_realtime"] / single[(f, d1, "seq", 1)]["x_realtime"]
    k = (f, dev, mode, rate)
    return agg[k]["x_realtime_aggregate"] if k in agg else None
def paths(rate, modes=MODES):  # every measured (decode hours, device, strategy) for all formats at this grid rate
    out = []
    for dev in DEVS:
        for mode in modes:
            sp = [speed(f, dev, mode, rate) for f in fmt]
            if None not in sp: out.append((sum(h * 3600 / v for (h, _), v in zip(fmt.values(), sp)) / 3600, dev, mode))
    return out
def io_h(mode, rate):
    if mode in ("seq", "skip"): return BYTES / IO_BPS / 3600
    t = 0.0
    for f, (h, b) in fmt.items():
        s = single[(f, "nvdec", "hybrid", rate)]; frames = s["video_s"] * codec_fps(f)  # NVDEC: 1 decode thread, so no frame-thread overshoot in the count
        t += b * min(1.0, s["decoded"] / frames) / IO_BPS + s["seeks"] * (h * 3600 / s["video_s"]) * SEEK_S
    return t / 3600
codec_fps = lambda f: J("synthetic_videos.json")["videos"][f]["target"]["fps"]
FPI = {"Endo-FM": 16, "EndoMamba": 16, "Basel V-JEPA": 16, "Cosmos-H-Surgical v0.3.1": 93, "Cosmos-H-Surgical Predict": 93, "Cosmos-H-Surgical-Simulator": 13,
       "Cosmos-H-Dreams": 12, "MedSora": 16, "SG2VID": 16, "KVLR": 17, "Open-Sora VAE": 17, "VideoMAE": 16, "OmniTokenizer": 17, "Open-Sora-Plan": 25,
       "WF-VAE": 33, "CV-VAE": 17, "LARP": 16, "LeanVAE": 17, "Reducio": 16}
fpi = lambda name: next((v for k, v in FPI.items() if name.startswith(k)), 1)
THR = fm["gpus"]["RTX 4500 Ada (24 GB)"]["sustained_flops"]
models = [(r["model"], r["arm"], r["flops_per_input"], r["inputs_per_video_hour"], fpi(r["model"])) for r in fm["rows"]]
cv = ref["compute"]["value"]["rtx4500ada_gpu_h_per_video_h"]
rows = []
for name, arm, F, iph, f in models + [("Cosmos tokenizer CV8x8x8 (Decision 005 reference)", "reference", None, 720, 121)]:
    r = dict(model=name, arm=arm, frames_per_input=f, cells={})
    for col in RATES + ("doc",):
        if name.startswith("Cosmos tokenizer"):
            if col == "doc": gl, gh = cv["runtime_scaled_encode_only"] * HOURS, cv["flops_calibrated_whole_AE_105M"] * HOURS
            else: k = 3600 * col / 87120; gl, gh = cv["runtime_scaled_encode_only"] * k * HOURS, cv["flops_calibrated_whole_AE_105M"] * k * HOURS
            model_h, model_note = gh, f"{gl:.1f}-{gh:.1f} (high end used)"
        elif F is None: model_h, model_note = None, "not estimable (params / FLOPs not documented)"
        else:
            n_in = (iph if col == "doc" else 3600 * col / f) * HOURS; model_h = F * n_in / THR / 3600; model_note = ""
        if col == "doc":  # frames consumed per second under the documented sampling decides the decode regime
            consumed = (iph or 3600) * f / 3600
            if consumed > max(RATES): eff, P_ = 1, paths(1, ("seq",)); dn = f"dense, {consumed:.1f} frames/s consumed: seq"
            else: eff = min(r_ for r_ in RATES if r_ >= consumed); P_ = paths(eff); dn = f"{consumed:.2f} frames/s -> grid {eff}"
        else: eff, P_, dn = col, paths(col), ""
        mh = model_h if model_h is not None else 0.0  # choose the decode path that minimises the pipelined wall time
        d = min(P_, key=lambda p: (max(io_h(p[2], eff), p[0], mh), io_h(p[2], eff) + p[0]))
        io_t = io_h(d[2], eff)
        comp = {"I/O": io_t, "decode": d[0], "model": mh}
        srt = sorted(comp, key=comp.get, reverse=True); bott = srt[0]
        if comp[srt[1]] >= 0.9 * comp[srt[0]]: bott = f"{srt[0]} ~ {srt[1]}"  # within 10 %: co-limiting
        r["cells"][str(col)] = dict(io_h=round(io_t, 2), decode_h=round(d[0], 2), decode_path=f"{d[1]} {d[2]}" + (f" ({dn})" if dn else ""),
                                    model_gpu_h=None if model_h is None else round(model_h, 2), model_note=model_note,
                                    wall_pipelined_h=round(max(comp.values()), 2), wall_serial_h=round(sum(comp.values()), 2),
                                    bottleneck=bott if model_h is not None else f"{bott} (model n/e)")
    rows.append(r)
res = dict(note=__doc__, video_hours_all_files=round(HOURS, 2), bytes_all_files=BYTES, io_MBps_sustained=io["sustained"]["MBps"],
           formats={k: dict(hours=round(h, 2), TB=round(b / 1e12, 3)) for k, (h, b) in fmt.items()},
           decode_only={str(R): {f"{dev} {m}": round(sum(h * 3600 / speed(f, dev, m, R) for f, (h, _) in fmt.items()) / 3600, 2)
                                 for dev in DEVS for m in MODES if all(speed(f, dev, m, R) for f in fmt)} for R in RATES},
           io_only={str(R): dict(seq_or_skip=round(io_h("seq", R), 2), hybrid=round(io_h("hybrid", R), 2)) for R in RATES}, rows=rows)
json.dump(res, open(os.path.join(OUT, "ds203_wall_time_estimate.json"), "w"), indent=1)
md = ["| model | arm | 0.5 fps | 1 fps | 2 fps | 4 fps | documented sampling |", "|---|---|---|---|---|---|---|"]
for r in rows:
    md.append(f"| {r['model']} | {r['arm']} | " + " | ".join(f"{c['wall_pipelined_h']:.1f} h ({c['bottleneck']})" for c in r["cells"].values()) + " |")
open(os.path.join(OUT, "ds203_wall_time_table.md"), "w").write("\n".join(md) + "\n")
print(json.dumps({k: res[k] for k in ("video_hours_all_files", "formats", "decode_only", "io_only")}, indent=1)); print("\n".join(md))
