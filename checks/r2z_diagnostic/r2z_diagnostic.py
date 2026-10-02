"""R2_Z recoverability diagnostic (SPEC.md, commit a45298d). Reads committed biases only (47a49ea, 6165ece).
Closed form (linear Gaussian) or Gauss-Hermite quadrature (E4 secondary). No random draws."""
import csv, json, os, sys
from math import comb
import numpy as np
from scipy.special import log_ndtr, logsumexp, roots_hermitenorm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "role_switch_robustness"))
import role_switch_robustness as RR                                          # noqa: E402  (moments only)

BASE_GRID = os.path.join(HERE, "..", "role_switch", "ROLE_SWITCH_GRID.csv")
ROB_GRID = os.path.join(HERE, "..", "role_switch_robustness", "ROBUSTNESS_GRID.csv")
SEVEN = ["E1_0.5", "E1_0.9", "E2_5", "E2_30", "E3_0.5", "E3_0.9", "E4_binary"]


def parse(setting):
    if setting == "BASE": return "BASE", None
    if setting == "E4_binary": return "E4", None
    e, p = setting.split("_"); return e, (int(p) if e == "E2" else float(p))


def r2_gauss(ext, par, K, P, a, g, n_hist):
    """1 - Var(Z | first n_hist actions)/Var(Z) under the observational law (Var(Z) = 1)."""
    if n_hist == 0: return 0.0
    m, C, *_ = RR.moments(ext, par, K, P, a, g, a)
    H = list(range(1, n_hist + 1))
    return float(C[0, H] @ np.linalg.solve(C[np.ix_(H, H)], C[H, 0]))


def r2_binary(a, g, n_hist, nodes):
    """1 - E_H[Var(Z | H)] for n_hist i.i.d.-given-(Z,U) probit actions (count is sufficient)."""
    if n_hist == 0: return 0.0
    x, w = roots_hermitenorm(nodes); w = w / w.sum()
    zz, uu = np.meshgrid(x, x, indexing="ij"); lw = np.log(np.outer(w, w)).ravel(); z = zz.ravel()
    lin = (RR.MU_B + g * zz + a * uu).ravel(); lp, lq = log_ndtr(lin), log_ndtr(-lin)
    ev = 0.0
    for s in range(n_hist + 1):
        lt = lw + s * lp + (n_hist - s) * lq; lm = logsumexp(lt); e = np.exp(lt - lm)
        ps = comb(n_hist, s) * np.exp(lm); ez = (e * z).sum(); ez2 = (e * z * z).sum()
        ev += ps * (ez2 - ez * ez)
    return 1.0 - ev


def best_rule(r2, helps):
    vals = sorted(set(np.round(r2, 12)))
    best = None
    for c in [-np.inf] + vals:
        for kind in ("help_if_R2_gt_c", "help_if_R2_le_c"):
            pred = (np.round(r2, 12) > c) if kind == "help_if_R2_gt_c" else (np.round(r2, 12) <= c)
            mis = int((pred != helps).sum())
            if best is None or mis < best["misclassified"]:
                best = dict(c=(None if c == -np.inf else float(c)), rule=kind, misclassified=mis, n=int(len(helps)))
    return best


def fit(cells):
    out, tot = {}, 0
    for a in (0.0, 0.5, 1.0):
        sub = [c for c in cells if c["alpha"] == a]
        for key in ("R2_first", "R2_last"):
            pass
        out[str(a)] = {k: best_rule(np.array([c[k] for c in sub]), np.array([c["help"] for c in sub]))
                       for k in ("R2_first", "R2_last")}
    for k in ("R2_first", "R2_last"):
        out[f"total_{k}"] = sum(out[str(a)][k]["misclassified"] for a in (0.0, 0.5, 1.0))
    out["n_cells"] = len(cells)
    return out


def main():
    rows = [dict(setting="BASE", **r) for r in csv.DictReader(open(BASE_GRID))] + list(csv.DictReader(open(ROB_GRID)))
    cells, conv = [], 0.0
    for r in rows:
        ext, par = parse(r["setting"])
        K, P, a, g = int(r["K"]), int(r["P"]), float(r["alpha"]), float(r["gamma"])
        bH, bZ = float(r["bias_H"]), float(r["bias_HZ"])
        tol = 1e-8 if ext == "E4" else 1e-12
        W = par if ext == "E2" else 0
        if ext == "E4":
            r1 = 0.0
            r2l = r2_binary(a, g, K - 1, 200)
            conv = max(conv, abs(r2l - r2_binary(a, g, K - 1, 400)))
        else:
            r1 = r2_gauss(ext, par, K, P, a, g, W)
            r2l = r2_gauss(ext, par, K, P, a, g, W + K - 1)
        diff = abs(bZ) - abs(bH)
        cells.append(dict(setting=r["setting"], K=K, P=P, alpha=a, gamma=g, R2_first=r1, R2_last=r2l,
                          abs_diff=diff, tie=abs(diff) <= tol, help=bool(abs(bZ) < abs(bH) - tol)))
    # closed-form spot check of the E2 primary formula
    e2chk = max(abs(c["R2_first"] - (c["gamma"] ** 2 * int(c["setting"].split("_")[1]) /
                                     (1 + int(c["setting"].split("_")[1]) * (c["gamma"] ** 2 + c["alpha"] ** 2))))
                for c in cells if c["setting"].startswith("E2"))
    seven = [c for c in cells if c["setting"] in SEVEN]; base = [c for c in cells if c["setting"] == "BASE"]
    res = dict(seven=fit(seven), base=fit(base), eight=fit(cells))
    thr = int(np.floor(0.10 * len(seven)))
    res["stop_rule"] = dict(threshold_cells=thr, primary_total=res["seven"]["total_R2_first"],
                            outcome=("CANDIDATE DIAGNOSTIC" if res["seven"]["total_R2_first"] <= thr else "THEORY TRACK STOPS"),
                            secondary_total_non_binding=res["seven"]["total_R2_last"])
    res["checks"] = dict(E2_primary_formula_max_abs_err=e2chk, E4_secondary_quadrature_200_vs_400=conv,
                         R2_first_nonzero_settings=sorted({c["setting"] for c in cells if c["R2_first"] > 0}),
                         n_no_help_seven=int(sum(not c["help"] for c in seven)),
                         n_ties_seven=int(sum(c["tie"] for c in seven)))
    # cross-tabs: help rate by alpha x (R2_first == 0 / > 0), and by (K, P), seven settings
    xt = {}
    for a in (0.0, 0.5, 1.0):
        for z in ("R2=0", "R2>0"):
            sub = [c for c in seven if c["alpha"] == a and ((c["R2_first"] == 0) == (z == "R2=0"))]
            xt[f"alpha={a} {z}"] = f"{sum(c['help'] for c in sub)}/{len(sub)}"
    for K in RR.KS:
        for P in RR.PS:
            sub = [c for c in seven if c["K"] == K and c["P"] == P]
            xt[f"K={K} P={P}"] = f"{sum(c['help'] for c in sub)}/{len(sub)}"
    res["help_crosstab_seven"] = xt
    cols = ["setting", "K", "P", "alpha", "gamma", "R2_first", "R2_last", "abs_diff", "tie", "help"]
    with open(os.path.join(HERE, "R2Z_CELLS.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, cols, lineterminator="\n"); wr.writeheader()
        wr.writerows([{k: (f"{c[k]:.10g}" if isinstance(c[k], float) else c[k]) for k in cols} for c in cells])
    json.dump(res, open(os.path.join(HERE, "R2Z_RULES.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
