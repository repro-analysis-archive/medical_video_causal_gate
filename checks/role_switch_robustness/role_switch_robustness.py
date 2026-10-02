"""Role-switch robustness (SPEC.md, commit 04859b2). Closed form (E1-E3) or Gauss-Hermite quadrature (E4).
No random draws. Base = checks/role_switch (spec 0810087, result 47a49ea)."""
import csv, json, os, sys
import numpy as np
from scipy.special import log_ndtr, logsumexp, roots_hermitenorm
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_GRID = os.path.join(HERE, "..", "role_switch", "ROLE_SWITCH_GRID.csv")
BASE_CROSS = os.path.join(HERE, "..", "role_switch", "ROLE_SWITCH_CROSSOVER.csv")
MU, TAU, DELTA, RHO, MU_B = 1.0, 1.0, 1.05, 0.05, 0.0
KS, PS, ALPHAS, GAMMAS = (1, 2, 3, 5, 15), (0, 5, 30), (0.0, 0.5, 1.0), (0.5, 1.0, 2.0)
SETTINGS = [("E1", 0.5), ("E1", 0.9), ("E2", 5), ("E2", 30), ("E3", 0.5), ("E3", 0.9), ("E4", None)]


# ------------------------------------------------------------------ continuous (E1-E3): exact moments
def moments(ext, par, K, P, a, g, b, delta=DELTA):
    """Return m, C over W = (Z, A_1..A_N), cY = Cov(Y, W), EY, cvec, truth Psi(delta), Psi(1)."""
    if ext == "E1":
        N = K + P; t = np.arange(N)
        M = np.tril(par ** (t[:, None] - t[None, :]).clip(min=0)) * (t[:, None] >= t[None, :])
        M1 = M.sum(axis=1)
        mA = MU * M1; CA = (g * g + a * a) * np.outer(M1, M1) + M @ M.T
        CAZ = g * M1; cYA = TAU * CA.sum(axis=1) + b * a * M1; cYZ = TAU * g * M1.sum(); EY = TAU * MU * M1.sum()
        cvec = np.r_[np.full(K, delta), np.ones(P)]
        def psi(c):
            e, s = 0.0, 0.0
            for ck in c:
                e = ck * (MU + par * e); s += e
            return TAU * s
        tr, tr1 = psi(cvec), psi(np.ones(N))
    elif ext == "E2":
        W = int(par); N = W + K + P
        mA = np.full(N, MU); CA = (g * g + a * a) * np.ones((N, N)) + np.eye(N); CAZ = np.full(N, g)
        cYA = TAU * CA[:, W:].sum(axis=1) + b * a; cYZ = TAU * g * (K + P); EY = TAU * MU * (K + P)
        cvec = np.r_[np.ones(W), np.full(K, delta), np.ones(P)]
        tr, tr1 = TAU * MU * (delta * K + P), TAU * MU * (K + P)
    elif ext in ("E3", "BASE"):
        N = K + P; phi = 1.0 if ext == "BASE" else par; t = np.arange(N)
        R = phi ** np.abs(t[:, None] - t[None, :])
        mA = np.full(N, MU); CA = g * g + a * a * R + np.eye(N); CAZ = np.full(N, g)
        cYA = TAU * CA.sum(axis=1) + b * a * R[:, N - 1]; cYZ = TAU * g * N; EY = TAU * MU * N
        cvec = np.r_[np.full(K, delta), np.ones(P)]
        tr, tr1 = TAU * MU * (delta * K + P), TAU * MU * (K + P)
    else:
        raise KeyError(ext)
    n = len(mA)
    m = np.r_[0.0, mA]
    C = np.zeros((n + 1, n + 1)); C[0, 0] = 1.0; C[0, 1:] = C[1:, 0] = CAZ; C[1:, 1:] = CA
    cY = np.r_[cYZ, cYA]
    return m, C, cY, EY, cvec, tr, tr1


def g_formula(m, C, cY, EY, cvec, with_Z):
    N = len(cvec); gm = np.zeros(N + 1); gm[0] = m[0]
    for t in range(1, N + 1):
        H = ([0] if with_Z else []) + list(range(1, t))
        cond = m[t] + (np.linalg.solve(C[np.ix_(H, H)], C[t, H]) @ (gm[H] - m[H]) if H else 0.0)
        gm[t] = cvec[t - 1] * cond
    O = ([0] if with_Z else []) + list(range(1, N + 1))
    w = np.linalg.solve(C[np.ix_(O, O)], cY[O])
    return EY + w @ (gm[O] - m[O])


def cont_cell(ext, par, K, P, a, g, delta=DELTA):
    m, C, cY, EY, cvec, tr, tr1 = moments(ext, par, K, P, a, g, a, delta)
    return g_formula(m, C, cY, EY, cvec, False) - tr, g_formula(m, C, cY, EY, cvec, True) - tr, tr, tr1


# ------------------------------------------------------------------ binary (E4): exchangeable DP + quadrature
NMAX = max(KS) + max(PS)


def gh(n):
    x, w = roots_hermitenorm(n); return x, w / w.sum()


def moment_tables(logp, log1p, logw, u):
    """logM[n, s] = log E[p^s (1-p)^(n-s)], and EU[s] = E[U | S = s, n] for every n (signed, stable)."""
    L = np.full((NMAX + 2, NMAX + 2), -np.inf); EU = np.full((NMAX + 1, NMAX + 1), np.nan)
    for n in range(NMAX + 2):
        s = np.arange(n + 1)
        lt = logw[None, :] + s[:, None] * logp[None, :] + (n - s)[:, None] * log1p[None, :]
        L[n, : n + 1] = logsumexp(lt, axis=1)
        if n <= NMAX:
            mx = lt.max(axis=1, keepdims=True); e = np.exp(lt - mx)
            EU[n, : n + 1] = (e * u[None, :]).sum(axis=1) / e.sum(axis=1)
    return L, EU


def dp_psi(L, EU, K, P, rho, b):
    N = K + P; Pg = np.zeros(N + 1); Pg[0] = 1.0
    for t in range(1, N + 1):
        s = np.arange(t)                                     # counts among t-1 past actions
        pi = np.exp(L[t, 1: t + 1] - L[t - 1, :t])            # P(A_t = 1 | s ones among t-1)
        q = pi + (1 - pi) * rho if t <= K else pi
        new = np.zeros(N + 1); new[1: t + 1] += Pg[:t] * q; new[:t] += Pg[:t] * (1 - q); Pg = new
    s = np.arange(N + 1)
    return float((Pg * (TAU * s + b * EU[N, : N + 1])).sum())


def binary_cells(a, g, nodes, rho=RHO):
    """bias_H, bias_HZ for every (K, P) at (alpha = beta = a, gamma = g)."""
    x, w = gh(nodes); b = a
    zz, uu = np.meshgrid(x, x, indexing="ij"); ww = np.outer(w, w)
    lin = MU_B + g * zz + a * uu
    LH, EUH = moment_tables(log_ndtr(lin).ravel(), log_ndtr(-lin).ravel(), np.log(ww).ravel(), uu.ravel())
    tabs = []
    for i, z in enumerate(x):
        lz = MU_B + g * z + a * x
        tabs.append(moment_tables(log_ndtr(lz), log_ndtr(-lz), np.log(w), x))
    pbar = norm.cdf(MU_B / np.sqrt(1 + g * g + a * a)); out = {}
    for K in KS:
        for P in PS:
            tr = TAU * ((K + P) * pbar + K * rho * (1 - pbar)); tr1 = TAU * (K + P) * pbar
            psiH = dp_psi(LH, EUH, K, P, rho, b)
            psiZ = float(sum(w[i] * dp_psi(Lz, EUz, K, P, rho, b) for i, (Lz, EUz) in enumerate(tabs)))
            out[(K, P)] = (psiH - tr, psiZ - tr, tr, tr1)
    return out


# ------------------------------------------------------------------ analysis helpers
def crossover(rows, tol):
    res = []
    for P in PS:
        for a in ALPHAS:
            for g in GAMMAS:
                cell = sorted([r for r in rows if r["P"] == P and r["alpha"] == a and r["gamma"] == g], key=lambda r: r["K"])
                helps = [abs(r["bias_H"]) - abs(r["bias_HZ"]) > tol for r in cell]
                ks = [r["K"] for r, h in zip(cell, helps) if h]
                S = (not helps[0] and all(helps[1:])) if P == 0 else all(helps)
                res.append(dict(P=P, alpha=a, gamma=g, K_star=ks[0] if ks else "none",
                                pattern="".join("R" if h else "." for h in helps), S_holds=S))
    return res


def main():
    rows, checks = [], {}
    # sanity 2: reductions to the base grid
    base = {(int(r["K"]), int(r["P"]), float(r["alpha"]), float(r["gamma"])): (float(r["bias_H"]), float(r["bias_HZ"]))
            for r in csv.DictReader(open(BASE_GRID))}
    red = {}
    for ext, par in (("E1", 0.0), ("E2", 0), ("E3", 1.0)):
        red[ext] = max(max(abs(cont_cell(ext, par, K, P, a, g)[0] - base[(K, P, a, g)][0]),
                           abs(cont_cell(ext, par, K, P, a, g)[1] - base[(K, P, a, g)][1]))
                       for K in KS for P in PS for a in ALPHAS for g in GAMMAS)
    checks["s2_reduction_to_base_max_abs_diff"] = red
    # sanity 1 (continuous): delta = 1
    d1 = {}
    for ext, par in SETTINGS[:6]:
        d1[f"{ext}_{par}"] = max(max(abs(v) for v in cont_cell(ext, par, K, P, a, g, delta=1.0)[:2])
                                 for K in KS for P in PS for a in ALPHAS for g in GAMMAS)
    # continuous grids
    for ext, par in SETTINGS[:6]:
        for K in KS:
            for P in PS:
                for a in ALPHAS:
                    for g in GAMMAS:
                        bH, bZ, tr, tr1 = cont_cell(ext, par, K, P, a, g)
                        rows.append(dict(setting=f"{ext}_{par}", K=K, P=P, alpha=a, gamma=g, truth=tr, psi1=tr1,
                                         contrast=tr - tr1, bias_H=bH, bias_HZ=bZ))
    # binary E4
    e4, e4_400, e4_rho0, kmax = {}, {}, {}, 0.0
    for a in ALPHAS:
        for g in GAMMAS:
            e4[(a, g)] = binary_cells(a, g, 200)
            e4_400[(a, g)] = binary_cells(a, g, 400)
            e4_rho0[(a, g)] = binary_cells(a, g, 200, rho=0.0)
    conv = max(abs(e4[k][kp][i] - e4_400[k][kp][i]) for k in e4 for kp in e4[k] for i in (0, 1))
    d1["E4_rho0"] = max(abs(e4_rho0[k][kp][i]) for k in e4 for kp in e4[k] for i in (0, 1))
    checks["s1_natural_value_zero_bias"] = d1
    checks["s3_E4_quadrature_200_vs_400_max_abs_diff"] = conv
    xs, ws = gh(400); cf = []
    for a in ALPHAS:
        for g in GAMMAS:
            fH = a * a * RHO * 0.7978845608028654 / np.sqrt(1 + g * g + a * a)
            sz = np.sqrt(1 + a * a); c = g * xs / sz
            fZ = a * RHO * (a / sz) * float((ws * np.exp(norm.logpdf(c) - log_ndtr(c))).sum())
            bH, bZ = e4[(a, g)][(1, 0)][:2]
            cf.append(dict(alpha=a, gamma=g, formula_H=fH, dp_H=bH, formula_HZ=fZ, dp_HZ=bZ,
                           abs_err=max(abs(fH - bH), abs(fZ - bZ))))
    checks["s4_E4_K1_P0_independent_closed_form"] = cf
    for (a, g), d in e4.items():
        for (K, P), (bH, bZ, tr, tr1) in d.items():
            rows.append(dict(setting="E4_binary", K=K, P=P, alpha=a, gamma=g, truth=tr, psi1=tr1,
                             contrast=tr - tr1, bias_H=bH, bias_HZ=bZ))
    for r in rows:
        r["rel_H"] = r["bias_H"] / r["contrast"]; r["rel_HZ"] = r["bias_HZ"] / r["contrast"]
    ok = (all(v < 1e-9 for v in red.values()) and all(v < (1e-8 if k.startswith("E4") else 1e-10) for k, v in d1.items())
          and conv < 1e-8 and all(c["abs_err"] < 1e-8 for c in cf))
    checks["all_sanity_checks_pass"] = bool(ok)

    # crossover + statement S
    base_cross = {(int(r["P"]), float(r["alpha"]), float(r["gamma"])): r for r in csv.DictReader(open(BASE_CROSS))}
    base_rows = [dict(K=K, P=P, alpha=a, gamma=g, bias_H=v[0], bias_HZ=v[1]) for (K, P, a, g), v in base.items()]
    base_S = {(c["P"], c["alpha"], c["gamma"]): c["S_holds"] for c in crossover(base_rows, 1e-12)}
    cross, summary = [], {}
    for ext, par in SETTINGS:
        name = f"{ext}_{par}" if ext != "E4" else "E4_binary"
        cr = crossover([r for r in rows if r["setting"] == name], 1e-8 if ext == "E4" else 1e-12)
        for c in cr:
            c["setting"] = name; c["S_holds_base"] = base_S[(c["P"], c["alpha"], c["gamma"])]
            c["K_star_base"] = base_cross[(c["P"], c["alpha"], c["gamma"])]["K_star"]
        cross += cr
        newly = [(c["P"], c["alpha"], c["gamma"], c["pattern"]) for c in cr if c["S_holds_base"] and not c["S_holds"]]
        gained = [(c["P"], c["alpha"], c["gamma"], c["pattern"]) for c in cr if c["S_holds"] and not c["S_holds_base"]]
        summary[name] = dict(S_rows=f"{sum(c['S_holds'] for c in cr)}/27", base_S_rows=f"{sum(base_S.values())}/27",
                             verdict="PRESERVES" if not newly else "BREAKS", newly_failing=newly, gained=gained)
    checks["S_summary"] = summary

    cols = ["setting", "K", "P", "alpha", "gamma", "truth", "psi1", "contrast", "bias_H", "bias_HZ", "rel_H", "rel_HZ"]
    with open(os.path.join(HERE, "ROBUSTNESS_GRID.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, cols, lineterminator="\n"); wr.writeheader()
        wr.writerows([{k: (f"{r[k]:.10g}" if isinstance(r[k], float) else r[k]) for k in cols} for r in rows])
    with open(os.path.join(HERE, "ROBUSTNESS_CROSSOVER.csv"), "w", newline="") as f:
        cc = ["setting", "P", "alpha", "gamma", "K_star", "K_star_base", "pattern", "S_holds", "S_holds_base"]
        wr = csv.DictWriter(f, cc, lineterminator="\n"); wr.writeheader(); wr.writerows([{k: c[k] for k in cc} for c in cross])
    json.dump(checks, open(os.path.join(HERE, "ROBUSTNESS_CHECKS.json"), "w"), indent=1, default=float)
    print(json.dumps({k: v for k, v in checks.items() if k != "s4_E4_K1_P0_independent_closed_form"}, indent=1, default=float))
    print("s4 max err:", max(c["abs_err"] for c in cf))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
