"""Lead verification for DS024 (LEAD_VERIFICATION_SPEC.md §3-§4, committed 4a6f2b1 before any parquet was read):
D3 contiguity per case, recount of >=200 / D4 / D1 on contiguous cases, then D8 Cramer's V (operator x 8 PSM variables)."""
import glob, json, os, collections
import numpy as np, pandas as pd
ROOT = "/media/user/LaCie/medvideo_gate/DS024"; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); os.makedirs(OUT, exist_ok=True)
CONTENT = [f"observation.cartesian_state.psm{a}.pose.position.{c}" for a in (1, 2) for c in "xyz"] + [f"observation.state.psm{a}.gripper" for a in (1, 2)]
GATE_GAP, DECR = 1.0, 0.001
eps = []
for f in sorted(glob.glob(f"{ROOT}/SurgSync-*/P*/meta/episodes.jsonl")):
    leaf = f.split(ROOT + "/")[1].split("/meta")[0]
    for l in open(f):
        e = json.loads(l); eps.append(dict(leaf=leaf, case=e["case_id"], ep=e["episode_index"], user=str(e["user_id"]), length=e["length"], chunk=e["episode_chunk"]))
E = pd.DataFrame(eps)
def pq_path(r):
    hits = glob.glob(f"{ROOT}/parquet/{r.leaf}/data/*/episode_{r.ep:06d}.parquet"); assert len(hits) == 1, (r.leaf, r.ep, hits); return hits[0]
rows, frames = [], []
for (leaf, case), g in E.groupby(["leaf", "case"], sort=False):
    g = g.sort_values("ep"); parts = []
    for r in g.itertuples():
        d = pd.read_parquet(pq_path(r), columns=["observation.meta.ros_time_sec", "observation.meta.ros_time_nsec"] + CONTENT)
        for c in d.columns:                                    # LeRobot stores shape-[1] features as length-1 arrays
            if d[c].dtype == object: d[c] = [float(v[0]) if v is not None and len(v) == 1 else np.nan for v in d[c]]
        assert len(d) == r.length, (leaf, r.ep, len(d), r.length)
        d["t"] = d["observation.meta.ros_time_sec"].astype("float64") + 1e-9 * d["observation.meta.ros_time_nsec"].astype("float64"); d["ep"] = r.ep
        parts.append(d)
    D = pd.concat(parts, ignore_index=True); dt = np.diff(D["t"].to_numpy())
    bnd = np.cumsum([len(p) for p in parts])[:-1] - 1      # index in dt of each episode-boundary step
    rows.append(dict(leaf=leaf, case=case, user=g.user.iloc[0], n_eps=len(g), n_frames=len(D), t_missing=int(D["t"].isna().sum()),
                     dur_s=float(D["t"].iloc[-1] - D["t"].iloc[0]), max_gap=float(dt.max()) if len(dt) else 0.0,
                     max_boundary_gap=float(dt[bnd].max()) if len(bnd) else 0.0, min_step=float(dt.min()) if len(dt) else 0.0,
                     median_dt=float(np.median(dt)) if len(dt) else 0.0,
                     n_gap_gt_0p5=int((dt > 0.5).sum()), n_gap_gt_1=int((dt > 1).sum()), n_gap_gt_2=int((dt > 2).sum()), n_gap_gt_5=int((dt > 5).sum())))
    D["leaf"], D["case"], D["user"] = leaf, case, g.user.iloc[0]; frames.append(D[["leaf", "case", "user"] + CONTENT])
C = pd.DataFrame(rows)
C["contiguous"] = (C.max_gap <= GATE_GAP) & (C.min_step >= -DECR) & (C.t_missing == 0)
C["online"] = C.leaf.str.contains("multitask")
C.to_csv(os.path.join(OUT, "DS024_case_contiguity.csv"), index=False)
res = dict(n_cases=len(C), n_contiguous=int(C.contiguous.sum()),
           contiguous_by_recorder={"online (multitask)": int(C[C.online].contiguous.sum()), "offline (stitch-coldcut)": int(C[~C.online].contiguous.sum())},
           cases_by_recorder={"online": int(C.online.sum()), "offline": int((~C.online).sum())},
           descriptive_contiguous_at={str(g): int(((C.max_gap <= g) & (C.min_step >= -DECR)).sum()) for g in (0.5, 1.0, 2.0, 5.0)},
           max_gap_quantiles_online=C[C.online].max_gap.quantile([0, .25, .5, .75, .9, 1]).round(3).to_dict(),
           max_gap_quantiles_offline=C[~C.online].max_gap.quantile([0, .25, .5, .75, .9, 1]).round(3).to_dict(),
           max_boundary_gap_quantiles=C.max_boundary_gap.quantile([0, .5, .9, 1]).round(3).to_dict(),
           median_dt_online=float(C[C.online].median_dt.median()), median_dt_offline=float(C[~C.online].median_dt.median()),
           t_missing_total=int(C.t_missing.sum()), cases_with_decrease=int((C.min_step < -DECR).sum()))
keep = C[C.contiguous]
lv = keep.user.value_counts(); res["operator_levels_contiguous"] = lv.to_dict(); res["qualifying_levels_contiguous"] = int((lv >= 20).sum())
res["ge200_contiguous"] = bool(len(keep) >= 200)
# D8: computed on the trajectories that count (contiguous cases), all recorded operator levels; descriptive restricted version
F = pd.concat(frames, ignore_index=True)
F = F.merge(keep[["leaf", "case"]], on=["leaf", "case"])
def cramers_v(df, var, levels=None):
    d = df[["leaf", "case", "user", var]].dropna(); dropped = len(df) - len(d)
    if levels is not None: d = d[d.user.isin(levels)]
    d = d.assign(w=1.0 / d.groupby(["leaf", "case"])[var].transform("size"))
    # pooled weighted quartiles
    o = np.argsort(d[var].to_numpy(), kind="mergesort"); x = d[var].to_numpy()[o]; cw = np.cumsum(d.w.to_numpy()[o]) / d.w.sum()
    q = [x[np.searchsorted(cw, p)] for p in (0.25, 0.5, 0.75)]
    b = np.searchsorted(np.array(q), d[var].to_numpy(), side="right")
    P = pd.crosstab(d.user, b, values=d.w, aggfunc="sum").fillna(0.0).to_numpy(); P = P / P.sum()
    pi, pj = P.sum(1, keepdims=True), P.sum(0, keepdims=True); E_ = pi @ pj
    phi2 = float(((P - E_) ** 2 / E_).sum()); r, c = P.shape
    return dict(V=float(np.sqrt(phi2 / (min(r, c) - 1))), rows=r, cols=c, quartile_cuts=[float(v) for v in q], frames_dropped_missing=int(dropped),
                trajectories=int(d.groupby(['leaf', 'case']).ngroups))
qual = lv[lv >= 20].index.tolist()
res["D8"] = {v: dict(all_levels=cramers_v(F, v), qualifying_levels_only_descriptive=cramers_v(F, v, qual)) for v in CONTENT}
res["D8_pass"] = bool(any(res["D8"][v]["all_levels"]["V"] <= 0.5 for v in CONTENT))
res["D7_density"] = float(F[CONTENT].notna().all(axis=1).mean())
json.dump(res, open(os.path.join(OUT, "DS024_verification.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "D8"}, indent=1))
print({v: round(res["D8"][v]["all_levels"]["V"], 4) for v in CONTENT})
print({v: round(res["D8"][v]["qualifying_levels_only_descriptive"]["V"], 4) for v in CONTENT})
