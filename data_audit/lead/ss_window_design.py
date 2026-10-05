"""SS protocol v0.2 design facts (metadata only: centre, annotated appendix-visible timestamp and duration per case from
out/DS203_d8_cases.csv, the same inputs as the D8 audit of 146f69b). No frame is read, no representation is extracted,
no synthetic action or outcome is drawn.
Compares window-placement rules for the D7 state S_t (S_t = 1 if step t, covering [5t, 5t+5) s, ends at or after the
timestamp): A0 = draft v0.1 (window starts at switch step - floor(K/2)); A1 = fixed procedure-time anchor at the pooled
median timestamp; A1u = seeded uniform eligible-window sampling; A2 = seeded switch-relative offset O_i in {-L..L},
assigned within site from a seeded permutation (site-stratified), on one eligible case set common to all cells.
Writes out/ss_window_design.json and the fixed per-case offsets out/ss_window_offsets.csv."""
import json, math, os
import numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "out")
SEED_OFFSET, L, W_MAX, K_MAX, P_MAX = 20261005, 15, 30, 15, 30
c = pd.read_csv(os.path.join(OUT, "DS203_d8_cases.csv")); c = c[c.center >= 2].reset_index(drop=True)
c["s"] = np.maximum(np.ceil(c.timestamp_s / 5).astype(int) - 1, 0)   # switch step: first step whose end >= timestamp
c["n"] = np.floor(c.duration_s / 5).astype(int)                       # whole 5-s steps
def cramers_v(x, y):
    t = pd.crosstab(x, y).values
    if min(t.shape) < 2: return 0.0
    n = t.sum(); e = np.outer(t.sum(1), t.sum(0)) / n
    return math.sqrt(((t - e) ** 2 / e).sum() / (n * (min(t.shape) - 1)))
res = dict(note=__doc__, n_cases=len(c), cases_by_site=c.groupby("center").size().to_dict())
# A0
res["A0_distinct_S_sequences_per_K"] = {K: len({tuple(int(c.s[i] - K // 2 + j >= c.s[i]) for j in range(K)) for i in range(len(c))}) for K in (1, 2, 5, 15)}
# A1
a_step = int(round(c.timestamp_s.median() / 5)); el = (a_step - W_MAX >= 0) & (c.n >= a_step + K_MAX + P_MAX)
res["A1_fixed_anchor"] = dict(anchor_s=5 * a_step, eligible=int(el.sum()),
    P_S1_by_site_at_start={int(k): round(v, 3) for k, v in c[el].assign(S=(a_step >= c.s[el]).astype(int)).groupby("center").S.mean().items()},
    V_C_S={j: round(cramers_v(c.center[el], (a_step + j >= c.s[el]).astype(int)), 3) for j in (0, 7, 14)})
# A1u
rng = np.random.default_rng(SEED_OFFSET); rows = []
for i in range(len(c)):
    lo, hi = W_MAX, c.n[i] - K_MAX - P_MAX
    if hi >= lo: w = int(rng.integers(lo, hi + 1)); rows.append((c.center[i], int(w >= c.s[i]), int(w < c.s[i] <= w + K_MAX - 1)))
u = pd.DataFrame(rows, columns=["C", "S0", "switch_in_K15"])
res["A1u_uniform_sampling"] = dict(eligible=len(u), P_S1_by_site={int(k): round(v, 3) for k, v in u.groupby("C").S0.mean().items()},
                                   V_C_S0=round(cramers_v(u.C, u.S0), 3), share_K15_windows_containing_switch=round(u.switch_in_K15.mean(), 3))
# A2: eligibility per (L, W)
res["A2_eligible_by_L_W"] = {f"L{Lx}_W{W}": dict(n=int(((c.s - Lx - W >= 0) & (c.s + Lx + K_MAX + P_MAX <= c.n)).sum()),
    by_site={int(k): int(v) for k, v in c[(c.s - Lx - W >= 0) & (c.s + Lx + K_MAX + P_MAX <= c.n)].groupby("center").size().items()})
    for Lx in (10, 15) for W in (0, 5, 30)}
res["early_switch_cases_T_lt_75s_by_site"] = {int(k): int(v) for k, v in c[c.timestamp_s < 75].groupby("center").size().items()}
# A2 final design: L = 15, common eligible set for W_MAX, site-stratified seeded offsets
e = c[(c.s - L - W_MAX >= 0) & (c.s + L + K_MAX + P_MAX <= c.n)].copy()
rng = np.random.default_rng(SEED_OFFSET); O = pd.Series(0, index=e.index)
for C_, g in e.groupby("center"):
    perm = rng.permutation(np.arange(-L, L + 1)); O.loc[g.index] = rng.permutation(np.resize(perm, len(g)))
e["O"] = O; e["window_start_step"] = e.s + e.O
vs = {j: round(cramers_v(e.center, ((e.O + j) >= 0).astype(int)), 4) for j in range(-W_MAX, K_MAX + P_MAX)}
res["A2_final"] = dict(L=L, seed=SEED_OFFSET, eligible=len(e), by_site={int(k): int(v) for k, v in e.groupby("center").size().items()},
    single_file=int((e.n_files == 1).sum()), single_file_by_site={int(k): int(v) for k, v in e[e.n_files == 1].groupby("center").size().items()},
    P_S1_by_rel_step={j: round(((e.O + j) >= 0).mean(), 3) for j in (-30, -5, 0, 1, 4, 14, 15, 44)},
    V_C_S_by_rel_step_max=max(vs.values()), V_C_S_rel0=vs[0], eta2_C_S_rel0=round(vs[0] ** 2, 5), V_C_S_by_rel_step=vs,
    offset_mean_sd_by_site={int(k): [round(m, 2), round(s, 2)] for k, (m, s) in e.groupby("center").O.agg(["mean", "std"]).iterrows()},
    window_start_elapsed_s_median_by_site={int(k): float(v) for k, v in (5 * e.window_start_step).groupby(e.center).median().items()})
e[["center", "op", "n_files", "s", "n", "O", "window_start_step"]].to_csv(os.path.join(OUT, "ss_window_offsets.csv"), index=False)
json.dump(res, open(os.path.join(OUT, "ss_window_design.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "note"}, indent=1)[:3500])
