"""DS203 D8 (Decision 002; DS203_D8_SPEC.md §2-3): site x appendix-visible state, frames weighted so each trajectory
sums to 1, Cramer's V on the counted trajectories (centres 2-5, 279 cases). Descriptive: strict 227 single-file cases
and all 330."""
import json, os, re, collections
import numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "out")
probe = json.load(open(os.path.join(OUT, "DS203_container_probe.json")))
meta = pd.read_csv("/media/user/LaCie/medvideo_gate/DS203/overall_merged.csv")
files = collections.defaultdict(dict)                         # (center, op) -> {version: (filename, frames, fps, dur)}
for name, r in probe.items():
    m = re.search(r"Center(\d)_(\d+)(?:_v(\d+))?\.mp4$", name); c, op, v = int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)
    files[(c, op)][v] = (os.path.basename(name), r["frames"], r["fps"], r["video_duration_s"])
def secs(ts):
    h, mi, s = ts.split(":"); return int(h) * 3600 + int(mi) * 60 + float(s)
rows, flags = [], []
for x in meta.itertuples():
    key = (int(x.Center), int(x.OP)); fv = files.get(key)
    if not fv: flags.append(dict(case=key, issue="no probed file")); continue
    vers = sorted(fv); target = [v for v in vers if fv[v][0] == x.Video]
    if len(target) != 1: flags.append(dict(case=key, issue=f"Video column {x.Video} not among {[fv[v][0] for v in vers]}")); continue
    tv = target[0]; fn, nfr, fps, dur = fv[tv]; t = secs(x.Timestamp)
    if t > dur: flags.append(dict(case=key, issue=f"timestamp {t:.1f}s > duration {dur:.1f}s of {fn}")); continue
    before = sum(fv[v][1] for v in vers if v < tv) + round(t * fps); total = sum(fv[v][1] for v in vers)
    rows.append(dict(center=key[0], op=key[1], n_files=len(vers), frames_total=total, frames_before=before, frac_before=before / total,
                     timestamp_s=t, duration_s=sum(fv[v][3] for v in vers), fps_set=sorted({round(fv[v][2], 3) for v in vers})))
D = pd.DataFrame(rows); D.to_csv(os.path.join(OUT, "DS203_d8_cases.csv"), index=False)
def cramers_v(d):
    W = d.groupby("center").agg(before=("frac_before", "sum"), n=("frac_before", "size")); W["after"] = W["n"] - W["before"]
    P = W[["before", "after"]].to_numpy(); P = P / P.sum(); E = P.sum(1, keepdims=True) @ P.sum(0, keepdims=True)
    phi2 = float(((P - E) ** 2 / E).sum()); r, c = P.shape
    return dict(V=float(np.sqrt(phi2 / (min(r, c) - 1))), trajectories=int(len(d)), table_weighted={int(k): dict(before=round(float(v.before), 3), after=round(float(v.after), 3), n=int(v.n)) for k, v in W.iterrows()})
prim = D[D.center.isin([2, 3, 4, 5])]
res = dict(primary_counted_centres2to5=cramers_v(prim), descriptive_strict_single_file=cramers_v(prim[prim.n_files == 1]), descriptive_all330=cramers_v(D),
           D8_pass_primary=None, flags=flags, files_probed=len(probe), cases_with_files=len(files),
           fps_distribution=collections.Counter(round(r["fps"], 2) for r in probe.values()).most_common(8), total_frames_primary=int(prim.frames_total.sum()),
           frac_before_by_center={int(c): dict(mean=round(float(g.frac_before.mean()), 3), median=round(float(g.frac_before.median()), 3)) for c, g in D.groupby("center")})
res["D8_pass_primary"] = res["primary_counted_centres2to5"]["V"] <= 0.5
json.dump(res, open(os.path.join(OUT, "DS203_d8_result.json"), "w"), indent=1); print(json.dumps(res, indent=1, default=str))
