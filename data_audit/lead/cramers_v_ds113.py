"""LEAD_VERIFICATION_SPEC.md §4 for DS113 (Cataract-101): surgeon x phase, frames weighted so each video sums to 1.
Phase per frame = the phase whose start frame (annotations.csv) is the latest at or before that frame; frames before
the first annotated start have no phase and are dropped (count reported)."""
import json, os
import numpy as np, pandas as pd
Z = "/media/user/LaCie/medvideo_gate/DS113/zip_members"; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
V = pd.read_csv(f"{Z}/videos.csv", sep=";"); A = pd.read_csv(f"{Z}/annotations.csv", sep=";").sort_values(["VideoID", "FrameNo"])
cells, dropped = {}, 0
for v in V.itertuples():
    a = A[A.VideoID == v.VideoID]; starts, ph = a.FrameNo.to_numpy(), a.Phase.to_numpy()
    if len(a) == 0: dropped += v.Frames; continue
    ends = np.append(starts[1:], v.Frames); n_lab = int(np.clip(ends - starts, 0, None).sum()); dropped += v.Frames - n_lab
    for s, e, p in zip(starts, ends, ph):
        cells[(v.Surgeon, p)] = cells.get((v.Surgeon, p), 0.0) + max(e - s, 0) / n_lab
T = pd.Series(cells).unstack(fill_value=0.0); P = T.to_numpy() / T.to_numpy().sum()
E = P.sum(1, keepdims=True) @ P.sum(0, keepdims=True); phi2 = float(((P - E) ** 2 / E).sum())
Vc = float(np.sqrt(phi2 / (min(P.shape) - 1)))
res = dict(dataset="DS113 Cataract-101", factor="Surgeon (levels: %s)" % V.Surgeon.value_counts().sort_index().to_dict(), content="phase (categorical)",
           videos=len(V), frames_total=int(V.Frames.sum()), frames_dropped_unlabelled=int(dropped), table_rows=P.shape[0], table_cols=P.shape[1],
           cramers_v=Vc, d8_rule_pass=Vc <= 0.5, note="DS113 is not SS-eligible (101 < 200 trajectories); V reported per gate §4")
json.dump(res, open(os.path.join(OUT, "DS113_cramers_v.json"), "w"), indent=1); print(json.dumps(res, indent=1))
