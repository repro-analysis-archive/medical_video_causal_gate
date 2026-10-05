"""G-SITE quantity for the per-W sensitivity sets (SS protocol v0.4 §5.4, §10.3; v0.4-final3 item 4): eta^2 of S at
the window start (window-relative step 0, S = 1{O_i >= 0}) on centre C, one-way, from the fixed offsets only
(out/ss_window_offsets.csv for the primary set; out/ss_window_offsets_perW.csv for W = 0 / W = 5). Metadata only."""
import json, os
import numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "out")
def eta2(c, y):
    y = np.asarray(y, float); m = y.mean(); tot = ((y - m) ** 2).sum()
    return float(sum(len(g) * (g.mean() - m) ** 2 for _, g in pd.Series(y).groupby(np.asarray(c)))) / tot if tot else 0.0
sets = {"primary_W30": pd.read_csv(os.path.join(OUT, "ss_window_offsets.csv"))}
pw = pd.read_csv(os.path.join(OUT, "ss_window_offsets_perW.csv"))
for w in ("W0", "W5"): sets[w] = pw[pw.set == w]
res = {k: dict(n=len(d), eta2_S_rel0_on_C=round(eta2(d.center, (d.O >= 0).astype(int)), 5), P_S1_rel0=round(float((d.O >= 0).mean()), 3),
               gate_le_0_01=bool(eta2(d.center, (d.O >= 0).astype(int)) <= 0.01)) for k, d in sets.items()}
json.dump(dict(note=__doc__, results=res), open(os.path.join(OUT, "ss_gsite_perW.json"), "w"), indent=1); print(res)
