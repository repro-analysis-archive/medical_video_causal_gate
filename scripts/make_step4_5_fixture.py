"""FIXTURE generator for the step 4-5 runner smoke tests (CC_TASK_SS_step4_5_resume_v1.md §2). Synthetic only.

Everything written here is labelled FIXTURE (directory names, mp4 title / comment tags, a `fixture` column in every
CSV, the zip comment, fixture_manifest.json). No DS203 byte, frame, case or metadata value is used: the case IDs (ops
701+), centres 2-5 membership, switch times, durations and offsets are drawn from seed 99990003; only the per-centre
media formats come from the container facts of 2012acd (data_audit/lead/out/DS203_codec_facts.json, medians).

* 278 fixture cases satisfying the locked design's set sizes (primary 158, single-file 123, W0 204, W5 201) and the
  window layout the locked code needs (primary: window start w in 30..34, analysis region w-30..w+44 inside the video;
  W0 / W5: w..w+14 inside the video). 35 primary and 5 further cases have two files (_v01, _v02).
* Reduced-resolution videos (1080p formats -> 256x144, 2160p -> 512x288) with each centre format's codec (H.264),
  profile (High), level, frame rate, keyframe spacing (frames), B-frames / references and bitrate per pixel. They exist
  for orchestration tests (STOP conditions, commit, interruption / resume, status, manifests); not a throughput
  benchmark.
* One short full-resolution clip (16.5 s) per distinct centre / media format (C2 1080p25, C2 2160p25, C3 2160p25,
  C3 1080p25, C4 1080p50, C5 1080p50), as six of the cases outside every analysis set, to exercise full-resolution
  decode, crop and resize.
* Content: ffmpeg testsrc2 with a per-case hue shift, per-case temporal noise seed and a vignette.
* Archive: DS203 layout Full_Videos/Center<c>/FIXTURE_Center<c>_<op>/Center<c>_<op>[_vNN].mp4, stored (zip -0),
  ZIP64 (-fz), split into five .zNN parts plus .zip: <out>/archive/FIXTURE_Appendix300_Full_Videos.zip.
* Metadata in the formats of data_audit/lead/out/{DS203_d8_cases.csv, ss_window_offsets.csv,
  ss_window_offsets_perW.csv} plus a `fixture` column: <out>/FIXTURE_metadata/.

    python scripts/make_step4_5_fixture.py --out DIR [--jobs 8]
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np
import pandas as pd

SEED = 99990003
LABEL = "FIXTURE"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# format: (centre, full W, H, fps, level, median Mbps, keyframe interval in frames) -- 2012acd medians / majority level
FORMATS = {
    "C2_1080p25": (2, 1920, 1080, 25, "5.0", 16.0, 60),
    "C2_2160p25": (2, 3840, 2160, 25, "5.1", 73.1, 30),
    "C3_2160p25": (3, 3840, 2160, 25, "5.1", 75.05, 36),
    "C3_1080p25": (3, 1920, 1080, 25, "5.0", 7.52, 120),
    "C4_1080p50": (4, 1920, 1080, 50, "5.0", 7.8, 96),
    "C5_1080p50": (5, 1920, 1080, 50, "5.0", 8.46, 214),
}
REDUCED = {1080: (256, 144), 2160: (512, 288)}
# fixture cases per centre and reduced-resolution format (C3 1080p25 appears only as its full-resolution clip)
CENTRE_FORMATS = {2: [("C2_1080p25", 54), ("C2_2160p25", 8)], 3: [("C3_2160p25", 42)], 4: [("C4_1080p50", 71)],
                  5: [("C5_1080p50", 103)]}
FULL_RES_CLIP_STEPS = 3


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(16 << 20), b""):
            h.update(b)
    return h.hexdigest()


def design(rng):
    rows = []
    for c, fmts in CENTRE_FORMATS.items():
        k = 0
        for fmt, n in fmts:
            for _ in range(n):
                k += 1
                rows.append(dict(center=c, op=700 + k, fmt=fmt, full_res=False))
    d = pd.DataFrame(rows)
    assert len(d) == 278
    n_c = d.center.value_counts().sort_index()
    # primary 158, proportional per centre (>= 20 each)
    quota = np.floor(158 * n_c / n_c.sum()).astype(int)
    quota[quota.index[np.argsort(-(158 * n_c / n_c.sum() - quota).to_numpy())[:158 - quota.sum()]]] += 1
    d["primary"] = False
    for c, q in quota.items():
        d.loc[rng.choice(d.index[d.center == c], q, replace=False), "primary"] = True
    rest = rng.permutation(d.index[~d.primary])
    d["W0"] = d.primary.copy()
    d.loc[rest[:46], "W0"] = True
    d["W5"] = d.primary.copy()
    d.loc[rest[:43], "W5"] = True
    others = [i for i in rest[46:]]
    # six full-resolution clips among the cases outside every set, one per distinct centre / media format
    for fmt, (c, *_ ) in FORMATS.items():
        i = next(j for j in others if d.at[j, "center"] == c and not d.at[j, "full_res"])
        d.at[i, "fmt"], d.at[i, "full_res"] = fmt, True
    d["n_files"] = 1
    d.loc[rng.choice(d.index[d.primary], 35, replace=False), "n_files"] = 2
    d.loc[rng.choice(rest[:46], 5, replace=False), "n_files"] = 2
    # window layout
    s, n, O = np.zeros(len(d), int), np.zeros(len(d), int), np.zeros(len(d), int)
    for i in d.index:
        if d.at[i, "primary"]:
            w = int(rng.integers(30, 35)); O[i] = int(rng.integers(-15, 16)); s[i] = w - O[i]
            n[i] = w + 45 + int(rng.integers(0, 3))
        elif d.at[i, "W0"]:
            s[i] = int(rng.integers(16, 31)); O[i] = int(rng.integers(-15, 16))
            n[i] = s[i] + O[i] + 16 + int(rng.integers(0, 3))
        elif d.at[i, "full_res"]:
            s[i], n[i] = 1, FULL_RES_CLIP_STEPS
        else:
            s[i], n[i] = 4, 12
    d["s"], d["n"], d["O"] = s, n, O
    d["duration_s"] = 5.0 * d.n + 1.5
    d["timestamp_s"] = 5.0 * d.s + 2.5
    d["fps"] = [FORMATS[f][3] for f in d.fmt]
    d["hue"] = rng.integers(0, 360, len(d))
    d["noise_seed"] = rng.integers(1, 2**31 - 1, len(d))
    split = rng.uniform(0.3, 0.7, len(d))
    d["d1"] = np.where(d.n_files == 2, np.round(d.duration_s * split * 5) / 5, d.duration_s)
    return d


def encode(job):
    path, w, h, fps, level, mbps, gop, dur, hue, seed = job
    if os.path.exists(path):
        return path
    vf = f"hue=h={hue}:s=1,noise=alls=14:allf=t+u:all_seed={seed},vignette=PI/4"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
           f"testsrc2=size={w}x{h}:rate={fps}:duration={dur}", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
           "-profile:v", "high", "-level:v", level, "-pix_fmt", "yuv420p", "-b:v", f"{mbps:.4f}M",
           "-maxrate", f"{1.5 * mbps:.4f}M", "-bufsize", f"{2 * mbps:.4f}M", "-g", str(gop), "-keyint_min", str(gop),
           "-sc_threshold", "0", "-bf", "3", "-refs", "5", "-threads", "2", "-metadata", f"title={LABEL}",
           "-metadata", f"comment={LABEL} synthetic test video (testsrc2); not DS203", path + ".tmp.mp4"]
    subprocess.run(cmd, check=True)
    os.replace(path + ".tmp.mp4", path)
    return path


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args(argv)
    out = os.path.abspath(a.out)
    root, meta, arch = (os.path.join(out, x) for x in ("FIXTURE_tree", "FIXTURE_metadata", "archive"))
    for x in (root, meta, arch):
        os.makedirs(x, exist_ok=True)
    rng = np.random.default_rng(SEED)
    d = design(rng)
    jobs, files = [], []
    for r in d.itertuples():
        c, W, H, fps, level, mbps, gop = FORMATS[r.fmt]
        w, h = (W, H) if r.full_res else REDUCED[H]
        rate = mbps * (w * h) / (W * H)
        parts = [r.d1] if r.n_files == 1 else [r.d1, round(r.duration_s - r.d1, 1)]
        for k, dur in enumerate(parts):
            name = f"Center{c}_{r.op:03d}" + (f"_v{k + 1:02d}" if r.n_files == 2 else "") + ".mp4"
            p = os.path.join(root, "Full_Videos", f"Center{c}", f"{LABEL}_Center{c}_{r.op:03d}", name)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            jobs.append((p, w, h, fps, level, rate, gop, dur, int(r.hue), int(r.noise_seed)))
            files.append(dict(case=f"C{c}_{r.op:03d}", format=r.fmt, full_resolution=bool(r.full_res), width=w,
                              height=h, fps=fps, level=level, target_mbps=round(rate, 4), gop_frames=gop,
                              duration_s=dur, path=os.path.relpath(p, out)))
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(encode, jobs))
    # metadata in the locked formats (+ fixture column)
    fr = (d.duration_s * d.fps).round().astype(int)
    fb = (d.timestamp_s * d.fps).round().astype(int)
    d8 = pd.DataFrame(dict(center=d.center, op=d.op, n_files=d.n_files, frames_total=fr, frames_before=fb,
                           frac_before=fb / fr, timestamp_s=d.timestamp_s, duration_s=d.duration_s, fps_set=d.fps))
    c1 = pd.DataFrame(dict(center=1, op=[701, 702, 703], n_files=1, frames_total=1500, frames_before=600,
                           frac_before=0.4, timestamp_s=24.0, duration_s=60.0, fps_set=25))
    d8 = pd.concat([c1, d8]).assign(fixture=LABEL)
    d8.to_csv(os.path.join(meta, "DS203_d8_cases.csv"), index=False)
    p = d[d.primary]
    pd.DataFrame(dict(center=p.center, op=p.op, n_files=p.n_files, s=p.s, n=p.n, O=p.O, window_start_step=p.s + p.O,
                      fixture=LABEL)).to_csv(os.path.join(meta, "ss_window_offsets.csv"), index=False)
    perw = []
    for set_name in ("W0", "W5"):
        q = d[d[set_name]]
        perw.append(pd.DataFrame(dict(set=set_name, center=q.center, op=q.op, n_files=q.n_files, s=q.s, n=q.n, O=q.O,
                                      window_start_step=q.s + q.O,
                                      offset_source=np.where(q.primary, "primary", "FIXTURE-draw"), fixture=LABEL)))
    pd.concat(perw).to_csv(os.path.join(meta, "ss_window_offsets_perW.csv"), index=False)
    # archive: stored, ZIP64, split into five .zNN parts + .zip
    total = sum(os.path.getsize(os.path.join(out, f["path"])) for f in files)
    split_mb = max(1, math.ceil(total / 5.5 / 2**20))
    zp = os.path.join(arch, f"{LABEL}_Appendix300_Full_Videos.zip")
    for f in os.listdir(arch):
        os.remove(os.path.join(arch, f))
    subprocess.run(["zip", "-q", "-0", "-fz", "-r", "-s", f"{split_mb}m", "-z", zp, "Full_Videos"], cwd=root,
                   input=f"{LABEL}: synthetic archive for the step 4-5 runner smoke tests; not DS203\n".encode(),
                   check=True)
    parts = sorted(os.listdir(arch))
    # facts of the produced media (ffprobe, one file per format and resolution)
    probe = {}
    for f in files:
        key = f"{f['format']}{'_full' if f['full_resolution'] else '_reduced'}"
        if key in probe:
            continue
        pth = os.path.join(out, f["path"])
        st = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                        "stream=codec_name,profile,level,width,height,r_frame_rate,has_b_frames,refs:"
                                        "format=duration,bit_rate:format_tags=title", "-of", "json", pth],
                                       capture_output=True, text=True, check=True).stdout)
        kf = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=flags",
                             "-of", "csv=p=0", pth], capture_output=True, text=True, check=True).stdout.split()
        probe[key] = dict(file=f["path"], stream=st["streams"][0], format=st["format"],
                          packets=len(kf), keyframes=sum("K" in x for x in kf))
    man = dict(label=LABEL, seed=SEED, generator="scripts/make_step4_5_fixture.py", n_cases=int(len(d)),
               sets=dict(primary=int(d.primary.sum()), single_file=int((d.primary & (d.n_files == 1)).sum()),
                         W0=int(d.W0.sum()), W5=int(d.W5.sum())),
               video_files=[dict(f, sha256=sha256(os.path.join(out, f["path"])),
                                 bytes=os.path.getsize(os.path.join(out, f["path"]))) for f in files],
               metadata={f: sha256(os.path.join(meta, f)) for f in sorted(os.listdir(meta))},
               archive={f: dict(bytes=os.path.getsize(os.path.join(arch, f)), sha256=sha256(os.path.join(arch, f)))
                        for f in parts},
               probe=probe, video_hours=round(float(d.duration_s.sum()) / 3600, 2))
    json.dump(man, open(os.path.join(out, "fixture_manifest.json"), "w"), indent=1, default=str)
    print(json.dumps(dict(cases=len(d), files=len(files), bytes=total, video_hours=man["video_hours"],
                          archive_parts=parts, sets=man["sets"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
