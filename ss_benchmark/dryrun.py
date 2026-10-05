"""PLACEHOLDER dry run of the representation-level checks and the family aggregation (§14 step 2: "a dry run on fully
synthetic placeholder features (no DS203 frames)").

Runs, on the PLACEHOLDER 278-case set and its 158-case primary set: fold-wise PCA / LEACE (placeholder.build), E1
(278 and 158), E2 primary (158, analysis region) and secondary (278, all steps), E3-site (linear and MLP probes, both
sets), E3-state-retention, the FM conditions; and a small causal run (two family cells, six arms, three replicates,
linear learners) followed by the §12.3 aggregation code. All seeds derive from 99990001. Output: one JSON file.

    python -m ss_benchmark.dryrun --out FILE [--n-boot B]
"""
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

from . import arms as arms_mod
from . import checks, dgp, grid, placeholder, sdr, seeds
from .constants import ANALYSIS_REGION, PLACEHOLDER_LABEL


def _roots():
    return (int(seeds.placeholder_seq("dryrun", "probe").generate_state(1)[0]),
            int(seeds.placeholder_seq("dryrun", "bootstrap").generate_state(1)[0]))


def run(n_boot=2000):
    rep_set, designs, reps, reports, full = placeholder.build()
    roots = _roots()
    sites = rep_set.centre.to_numpy()
    folds = rep_set.fold.to_numpy()
    n_steps = rep_set.n.to_numpy()
    s = rep_set.s.to_numpy()
    w = (rep_set.s + rep_set.O).to_numpy()
    prim = np.flatnonzero(rep_set.primary.to_numpy())
    all_idx = np.arange(len(rep_set))
    lo, hi = ANALYSIS_REGION

    def all_steps(i):
        return np.arange(n_steps[i])

    def region(i):
        return np.arange(w[i] + lo, w[i] + hi + 1)

    R, RC = full["P"]["R"], full["P"]["R-C"]
    out = dict(label=PLACEHOLDER_LABEL, reduction_reports={k: v for k, v in reports.items()})
    e1_278 = checks.e1(R, all_idx, sites, folds, all_steps, "PH:278:FM-P", roots)
    e1_158 = checks.e1(R, prim, sites, folds, region, "PH:158:FM-P", roots)
    rows158 = pd.DataFrame([(i, t, t, int(t >= s[i])) for i in prim for t in region(i)],
                           columns=["case", "step", "time", "S"])
    rows278 = pd.DataFrame([(i, t, t, int(t >= s[i])) for i in all_idx for t in all_steps(i)],
                           columns=["case", "step", "time", "S"])
    e2_pre = checks.e2_auc(rows158, R, folds, sites, "PH:158:FM-P", roots=roots, n_boot=n_boot)
    e2_post = checks.e2_auc(rows158, RC, folds, sites, "PH:158:FM-P-C", roots=roots, n_boot=n_boot)
    e2_sec = checks.e2_auc(rows278, R, folds, sites, "PH:278:FM-P", roots=roots, n_boot=n_boot)
    e3_278 = checks.e3_site(RC, all_idx, sites, folds, all_steps, "PH:278:FM-P-C", roots)
    e3_158 = checks.e3_site(RC, prim, sites, folds, region, "PH:158:FM-P-C", roots)
    e3_state = checks.e3_state_retention(e2_pre, e2_post)
    out.update(E1_278=e1_278, E1_158=e1_158, E2_primary=e2_pre, E2_primary_after_removal=e2_post,
               E2_secondary_278=e2_sec, E3_site_278=e3_278, E3_site_158=e3_158, E3_state_retention=e3_state,
               fm_conditions=checks.fm_conditions(e1_278, e1_158, e3_278, e3_158, e3_state))

    # small causal run + aggregation (exercise path only)
    D = designs["primary"]
    root = int(seeds.placeholder_seq("dryrun", "replicates").generate_state(1)[0])
    cells = [grid.find_cell(1, 0, 0, 0.5, 1.0), grid.find_cell(2, 5, 0, 0.5, 1.0)]
    arm_list = ("NV", "SITE", "FM-P", "FM-P-C", "ORACLE-C", "ORACLE")
    res = {}
    for c in cells:
        for r in range(3):
            seq = seeds.replicate_seq(c.index, r, root)
            d = dgp.draw(D, c, seq)
            A, Y = dgp.simulate(D, c, d)
            tr = dgp.truth(D, c, d)
            for arm in arm_list:
                X = arms_mod.arm_covariates(arm, D, c, d, reps["primary"])
                e = sdr.sdr_mtp(A, Y, X, c.W, c.K, D.folds, seeds.child(seq, "learners"), "linear")
                res.setdefault((c.index, arm), []).append((e["est"], tr))
    fam = {}
    for f, cells_f in (("P1b-SITE", [cells[1]]), ("P2-SITE", [cells[0]])):
        w_arm, wo_arm = grid.FAMILIES[f][:2]
        per = {c.index: ([x[0] for x in res[(c.index, w_arm)]], [x[0] for x in res[(c.index, wo_arm)]],
                         [x[1] for x in res[(c.index, w_arm)]]) for c in cells_f}
        fam[f] = grid.family_verdict(f, per, n_boot=n_boot, conditions={"G-SITE": True})
    out["causal_dryrun"] = {f"{k[0]}:{k[1]}": v for k, v in sorted(res.items())}
    out["family_dryrun"] = fam
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-boot", type=int, default=2000)
    a = ap.parse_args(argv)
    res = run(a.n_boot)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
