"""Role-switch check: closed form, no random draws. Implements checks/role_switch/SPEC.md (commit 0810087).

Model (SPEC I-1..I-5): Z ~ N(0,1), U ~ N(0,1), eps ~ N(0,1), independent;
A_t = mu + gamma*Z + alpha*U + eps_t (t = 1..K+P); Y = tau*sum_t A_t + beta*U + eps_Y.
Recursive multiplicative MTP: A_t -> delta*A_t^nat for t <= K, natural course for t > K.
Functional (I-8/I-9): sequential g-formula; linear-Gaussian conditionals, so g-law means propagate exactly.
"""
import contextlib, csv, io, json, os, runpy, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MU, TAU, DELTA = 1.0, 1.0, 1.05
KS, PS, ALPHAS, GAMMAS = (1, 2, 3, 5, 15), (0, 5, 30), (0.0, 0.5, 1.0), (0.5, 1.0, 2.0)
TOL = 1e-12


def moments(n, alpha, gamma, beta, mu=MU, tau=TAU):
    """Means / covariances of W = (Z, A_1..A_n) and their covariances with Y (U is marginalised: unobserved)."""
    m = np.r_[0.0, np.full(n, mu)]
    C = np.zeros((n + 1, n + 1)); C[0, 0] = 1.0
    C[0, 1:] = C[1:, 0] = gamma
    C[1:, 1:] = gamma ** 2 + alpha ** 2 + np.eye(n)
    cY = np.r_[tau * n * gamma, tau * C[1:, 1:].sum(axis=0) + beta * alpha]
    return m, C, cY, tau * n * mu


def g_formula(K, P, alpha, gamma, beta, with_Z, delta=DELTA, mu=MU, tau=TAU, return_law=False):
    n = K + P
    m, C, cY, EY = moments(n, alpha, gamma, beta, mu, tau)
    idx = ([0] if with_Z else []) + list(range(1, n + 1))     # observed coordinates of W, in time order
    gm = {0: 0.0}                                               # g-law mean; Z keeps its marginal law
    B = np.zeros((n + 1, n + 1)); const = np.zeros(n + 1); v = np.zeros(n + 1); D = np.ones(n + 1)
    v[0] = 1.0
    for t in range(1, n + 1):
        H = ([0] if with_Z else []) + list(range(1, t))
        c = delta if t <= K else 1.0
        if H:
            b = np.linalg.solve(C[np.ix_(H, H)], C[t, H])
            cond = m[t] + b @ (np.array([gm[i] for i in H]) - m[H])
            v[t] = C[t, t] - C[t, H] @ b
            B[t, H] = c * b; const[t] = c * (m[t] - b @ m[H])
        else:
            cond = m[t]; v[t] = C[t, t]; const[t] = c * m[t]
        gm[t] = c * cond; D[t] = c
    w = np.linalg.solve(C[np.ix_(idx, idx)], cY[idx])
    psi = EY + w @ (np.array([gm[i] for i in idx]) - m[idx])
    if not return_law:
        return psi
    # g-law covariance (linear SEM X = const + B X + D r), used only for the Monte Carlo standard error
    keep = idx
    Bk = B[np.ix_(keep, keep)]; Dk = np.diag(D[keep]); Vk = np.diag(v[keep])
    Ainv = np.linalg.inv(np.eye(len(keep)) - Bk)
    cov = Ainv @ Dk @ Vk @ Dk @ Ainv.T
    sel = np.array([1.0 if i > 0 else 0.0 for i in keep])     # total of the actions
    return psi, float(sel @ cov @ sel)


def truth(K, P, mu=MU, tau=TAU, delta=DELTA):
    return tau * mu * (delta * K + P)


def main():
    rows = []
    for P in PS:
        for a in ALPHAS:
            for g in GAMMAS:
                for K in KS:
                    t = truth(K, P)
                    bH = g_formula(K, P, a, g, a, False) - t
                    bZ = g_formula(K, P, a, g, a, True) - t
                    rows.append(dict(K=K, P=P, alpha=a, beta=a, gamma=g, truth=t, bias_H=bH, bias_HZ=bZ,
                                     diff=bZ - bH, diff_abs=abs(bZ) - abs(bH)))
    cross = []
    for P in PS:
        for a in ALPHAS:
            for g in GAMMAS:
                cell = [r for r in rows if r["P"] == P and r["alpha"] == a and r["gamma"] == g]
                red = [abs(r["bias_H"]) - abs(r["bias_HZ"]) > TOL for r in cell]
                ks = [r["K"] for r, x in zip(cell, red) if x]
                kstar = ks[0] if ks else "none"
                mono = (all(red[KS.index(kstar):]) if ks else None)
                cross.append(dict(P=P, alpha=a, beta=a, gamma=g, K_star=kstar,
                                  reduction_at_all_larger_K=mono,
                                  pattern="".join("R" if x else "." for x in red)))

    # ---- sanity checks (SPEC I-13) ----
    chk = {}
    d1 = max(abs(g_formula(K, P, a, g, a, z, delta=1.0) - truth(K, P, delta=1.0))
             for K in KS for P in PS for a in ALPHAS for g in GAMMAS for z in (False, True))
    chk["a_delta1_max_abs_bias"] = d1
    with contextlib.redirect_stdout(io.StringIO()):
        prior = runpy.run_path(os.path.join(HERE, "prior", "persistent_iv_exact.py"))
    pe = prior["gform_mean"]
    comp = []
    for K, P in ((1, 0), (2, 0), (15, 0), (1, 30), (15, 30)):
        for z in (False, True):
            new = g_formula(K, P, 0.0, 1.0, 0.0, z) - truth(K, P)
            old = pe(K, P, z) - (1.05 * K + P)
            comp.append(dict(K=K, P=P, with_Z=z, new=new, prior_exact=old, abs_diff=abs(new - old)))
    chk["b_prior_exact_reproduction"] = comp
    cf = []
    for a in ALPHAS:
        for g in GAMMAS:
            fH = a * a * (DELTA - 1) * MU / (g * g + a * a + 1); fZ = a * a * (DELTA - 1) * MU / (a * a + 1)
            cH = g_formula(1, 0, a, g, a, False) - truth(1, 0); cZ = g_formula(1, 0, a, g, a, True) - truth(1, 0)
            cf.append(dict(alpha=a, gamma=g, formula_H=fH, computed_H=cH, formula_HZ=fZ, computed_HZ=cZ,
                           abs_err=max(abs(fH - cH), abs(fZ - cZ))))
    chk["c_K1_P0_closed_forms"] = cf
    ok = (d1 < 1e-10 and all(c["abs_diff"] < 1e-10 for c in comp) and all(c["abs_err"] < 1e-12 for c in cf))
    chk["all_sanity_checks_pass"] = bool(ok)

    # ---- cross-check against the single-seed MC available here (SPEC I-14) ----
    mc = {(1, False): 0.0013, (2, False): 0.0267, (15, False): 1.2635,
          (1, True): -0.0003, (2, True): 0.0007, (15, True): 0.0145}
    N = 2_000_000; xc = []
    for (K, z), val in mc.items():
        psi, var = g_formula(K, 0, 0.0, 1.0, 0.0, z, return_law=True)
        b = psi - truth(K, 0); se = (var / N) ** 0.5
        xc.append(dict(K=K, P=0, alpha=0.0, gamma=1.0, with_Z=z, mc_printed=val, closed_form=b,
                       mc_se=se, z=(val - b) / se))
    chk["cross_check_vs_prior_mc_alpha0"] = xc
    chk["requested_cells_closed_form_alpha1_gamma1_P0"] = [
        dict(K=K, truth=truth(K, 0), bias_H=g_formula(K, 0, 1.0, 1.0, 1.0, False) - truth(K, 0),
             bias_HZ=g_formula(K, 0, 1.0, 1.0, 1.0, True) - truth(K, 0)) for K in (1, 5, 15)]
    chk["note"] = ("The MC named in the task (alpha=beta=1, K=1,5,15) is not available in this session; "
                   "cross-check is against prior/persistent_iv.py (alpha=0), per SPEC I-14.")

    with open(os.path.join(HERE, "ROLE_SWITCH_GRID.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, list(rows[0]), lineterminator="\n"); wr.writeheader()
        wr.writerows([{k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in r.items()} for r in rows])
    with open(os.path.join(HERE, "ROLE_SWITCH_CROSSOVER.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, list(cross[0]), lineterminator="\n"); wr.writeheader(); wr.writerows(cross)
    json.dump(chk, open(os.path.join(HERE, "ROLE_SWITCH_CHECKS.json"), "w"), indent=1)
    print("sanity:", chk["all_sanity_checks_pass"], "delta1:", d1)
    for c in xc: print("xcheck", c)
    for r in chk["requested_cells_closed_form_alpha1_gamma1_P0"]: print("requested", r)
    for c in cross: print(c)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
