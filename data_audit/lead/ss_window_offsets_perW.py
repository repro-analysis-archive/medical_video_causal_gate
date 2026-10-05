"""Offsets for the per-W sensitivity sets of SS protocol v0.4 (§7.2, §10.3; freeze-repair task A1). Metadata only
(centre, annotated timestamp, duration from out/DS203_d8_cases.csv); no frame, representation or synthetic draw.
The primary file out/ss_window_offsets.csv (dbd5984) covers the 158 cases of the common set (W = 30). The W = 0 set
(204 cases) and the W = 5 set (201 cases) contain cases without an offset there. Rule: the 158 primary offsets are kept
unchanged; the missing cases of EACH per-W set receive offsets by the same procedure and seed as dbd5984 (fresh
numpy default_rng(20261005); sites in ascending order; within each site, a seeded permutation of {-15..15} resized
to the site's number of missing cases and shuffled), applied to each per-W set separately.
Writes out/ss_window_offsets_perW.csv and out/ss_window_offsets_perW.json."""
import json, math, os
import numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "out")
SEED, L, K_MAX, P_MAX = 20261005, 15, 15, 30
c = pd.read_csv(os.path.join(OUT, "DS203_d8_cases.csv")); c = c[c.center >= 2].reset_index(drop=True)
c["s"] = np.maximum(np.ceil(c.timestamp_s / 5).astype(int) - 1, 0); c["n"] = np.floor(c.duration_s / 5).astype(int)
prim = pd.read_csv(os.path.join(OUT, "ss_window_offsets.csv")); prim_o = {(r.center, r.op): r.O for r in prim.itertuples()}
def cramers_v(x, y):
    t = pd.crosstab(x, y).values
    if min(t.shape) < 2: return 0.0
    n = t.sum(); e = np.outer(t.sum(1), t.sum(0)) / n
    return math.sqrt(((t - e) ** 2 / e).sum() / (n * (min(t.shape) - 1)))
rows, summary = [], {}
for W in (0, 5):
    e = c[(c.s - L - W >= 0) & (c.s + L + K_MAX + P_MAX <= c.n)].copy()
    e["O"] = [prim_o.get((r.center, r.op), np.nan) for r in e.itertuples()]
    e["offset_source"] = np.where(e.O.notna(), "dbd5984", "perW_draw")
    miss = e[e.O.isna()]; rng = np.random.default_rng(SEED)
    for C_, g in miss.groupby("center"):
        perm = rng.permutation(np.arange(-L, L + 1)); e.loc[g.index, "O"] = rng.permutation(np.resize(perm, len(g)))
    e["O"] = e.O.astype(int); e["window_start_step"] = e.s + e.O; e["set"] = f"W{W}"
    assert (e.window_start_step - W >= 0).all() and (e.window_start_step + K_MAX + P_MAX <= e.n).all()
    vs = {j: round(cramers_v(e.center, ((e.O + j) >= 0).astype(int)), 4) for j in range(-W, K_MAX + P_MAX)}
    summary[f"W{W}"] = dict(n=len(e), by_site={int(k): int(v) for k, v in e.groupby("center").size().items()},
        new_offsets=int((e.offset_source == "perW_draw").sum()), new_by_site={int(k): int(v) for k, v in e[e.offset_source == "perW_draw"].groupby("center").size().items()},
        max_V_C_S_over_rel_steps=max(vs.values()), rel_step_range=[-W, K_MAX + P_MAX - 1], V_C_S_rel0=vs[0], V_by_rel_step=vs)
    rows.append(e[["set", "center", "op", "n_files", "s", "n", "O", "window_start_step", "offset_source"]])
pd.concat(rows).to_csv(os.path.join(OUT, "ss_window_offsets_perW.csv"), index=False)
json.dump(dict(note=__doc__, seed=SEED, summary=summary), open(os.path.join(OUT, "ss_window_offsets_perW.json"), "w"), indent=1)
for k, v in summary.items(): print(k, {kk: vv for kk, vv in v.items() if kk != "V_by_rel_step"})
