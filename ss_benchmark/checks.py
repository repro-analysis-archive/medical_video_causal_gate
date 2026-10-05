"""Pre-causal checks (§5): E1, E2, E3-site / E3-state-retention, the fixed MLP probe, and G-SITE (§5.4).

Shared settings (§5): folds of §2 (restricted to the set); fold-v probes are trained on the set's training-fold cases
and predict its held-out fold, both transformed by the fold-v PCA / LEACE maps (reduce.py). Site probes are per step;
a case's prediction is the mean predicted probability over its steps (argmax); balanced accuracy over cases. CIs:
case bootstrap stratified by site, 2,000 resamples, seed 20261008 (named child stream per check; N10 for the bounds).
Learners: linear site probe = multinomial L2 logistic, penalty by inner 5-fold group CV over {1e-4..1e2} (N9); E2 =
binary L2 logistic, same grid; MLP probe = 256-unit one-hidden-layer MLP (§5.3, N1-N2). Inner-CV splits and MLP
initialisation use streams of SeedSequence(20261006) child "probe" (check, set, arm, fold).
E2 base: natural cubic spline of elapsed time (step index; spline span is invariant to the affine map to seconds), 4 df:
boundary knots at the training-fold min / max and interior knots at the training-fold 25 / 50 / 75 % quantiles
(truncated-power basis of Hastie et al., ESL eq. 5.4-5.5, without the constant).
"""
import numpy as np
import pandas as pd

from . import seeds
from .constants import (E1_BA, E1_LOWER, E2_DELTA_AUC, E3_RETENTION, E3_UPPER, GSITE_MAX_ETA2, MLP_PROBE, N_BOOTSTRAP,
                        PENALTY_GRID_E2, SEED_BOOTSTRAP, SEED_FOLDS)
from .learners import MLP, fit_logistic_cv, fit_multinomial_cv


# ---------------------------------------------------------------------------------------------------------------------
# metrics and bootstrap
# ---------------------------------------------------------------------------------------------------------------------
def balanced_accuracy(y, pred, weights=None, classes=None):
    y, pred = np.asarray(y), np.asarray(pred)
    w = np.ones(len(y)) if weights is None else np.asarray(weights, float)
    classes = np.unique(y) if classes is None else classes
    rec = [np.sum(w * ((y == k) & (pred == k))) / np.sum(w * (y == k)) for k in classes if np.sum(w * (y == k)) > 0]
    return float(np.mean(rec))


def weighted_auc(y, s, w=None):
    y = np.asarray(y, float); s = np.asarray(s, float)
    w = np.ones(len(y)) if w is None else np.asarray(w, float)
    order = np.argsort(s, kind="mergesort")
    s, y, w = s[order], y[order], w[order]
    _, start = np.unique(s, return_index=True)
    wp = np.add.reduceat(w * y, start)
    wn = np.add.reduceat(w * (1 - y), start)
    below = np.cumsum(wn) - wn
    return float(np.sum(wp * (below + 0.5 * wn)) / (wp.sum() * wn.sum()))


def bootstrap_case_weights(case_sites, n_boot, rng):
    """(n_boot, n_cases) multiplicity matrix of a case bootstrap stratified by site."""
    case_sites = np.asarray(case_sites)
    Wt = np.zeros((n_boot, len(case_sites)))
    for site in np.unique(case_sites):
        idx = np.flatnonzero(case_sites == site)
        draws = rng.integers(0, len(idx), size=(n_boot, len(idx)))
        for b in range(n_boot):
            Wt[b] += np.bincount(idx[draws[b]], minlength=len(case_sites))
    return Wt


def boot_rng(name, root=SEED_BOOTSTRAP):
    return seeds.rng(np.random.SeedSequence(root), name)


def probe_rng(*names, root=SEED_FOLDS):
    return seeds.rng(np.random.SeedSequence(root), "probe", *names)


# ---------------------------------------------------------------------------------------------------------------------
# site probes (E1, E3-site)
# ---------------------------------------------------------------------------------------------------------------------
def site_probe_case_predictions(rep_by_fold, case_idx, case_sites, case_folds, steps_of, kind, tag, root=SEED_FOLDS):
    """Out-of-fold case-level site predictions.

    rep_by_fold[v][i]: (n_steps_i, d) features of case i under the fold-v maps; case_idx: cases of the set;
    steps_of(i): row indices of case i's steps used by the set (e.g. the analysis region); kind: 'linear' | 'mlp'.
    """
    case_idx = np.asarray(case_idx)
    sites = np.asarray(case_sites)[case_idx]
    classes = np.unique(np.asarray(case_sites))
    folds = np.asarray(case_folds)[case_idx]
    pred = np.empty(len(case_idx), dtype=classes.dtype)
    for v in np.unique(folds):
        tr = case_idx[folds != v]
        te_pos = np.flatnonzero(folds == v)
        X = np.concatenate([rep_by_fold[v][i][steps_of(i)] for i in tr])
        y = np.concatenate([np.full(len(steps_of(i)), case_sites[i]) for i in tr])
        g = np.concatenate([np.full(len(steps_of(i)), i) for i in tr])
        rng = probe_rng(tag, kind, int(v), root=root)
        if kind == "linear":
            model = fit_multinomial_cv(X, y, g, rng, PENALTY_GRID_E2)
            model_classes = model.classes
        else:
            yk = np.searchsorted(classes, y)
            model = MLP("multi", **MLP_PROBE).fit(X, yk, rng, g, n_classes=len(classes))
            model_classes = classes
        for p in te_pos:
            i = case_idx[p]
            prob = model.predict_proba(rep_by_fold[v][i][steps_of(i)]).mean(0)
            pred[p] = model_classes[int(np.argmax(prob))]
    return sites, pred


def ba_with_ci(sites, pred, boot_name, n_boot=N_BOOTSTRAP, root=SEED_BOOTSTRAP):
    classes = np.unique(sites)
    ba = balanced_accuracy(sites, pred, classes=classes)
    Wt = bootstrap_case_weights(sites, n_boot, boot_rng(boot_name, root))
    boots = np.array([balanced_accuracy(sites, pred, Wt[b], classes) for b in range(n_boot)])
    return dict(ba=ba, lo_2p5=float(np.percentile(boots, 2.5)), hi_97p5=float(np.percentile(boots, 97.5)),
                upper_one_sided_95=float(np.percentile(boots, 95.0)), n_cases=int(len(sites)))


def e1(rep_by_fold, case_idx, case_sites, case_folds, steps_of, tag, roots=(SEED_FOLDS, SEED_BOOTSTRAP)):
    s, p = site_probe_case_predictions(rep_by_fold, case_idx, case_sites, case_folds, steps_of, "linear", tag, roots[0])
    r = ba_with_ci(s, p, f"E1:{tag}", root=roots[1])
    r["pass"] = bool(r["ba"] >= E1_BA and r["lo_2p5"] > E1_LOWER)
    return r


def e3_site(repC_by_fold, case_idx, case_sites, case_folds, steps_of, tag, roots=(SEED_FOLDS, SEED_BOOTSTRAP)):
    out = {}
    for kind in ("linear", "mlp"):
        s, p = site_probe_case_predictions(repC_by_fold, case_idx, case_sites, case_folds, steps_of, kind,
                                           f"E3:{tag}", roots[0])
        out[kind] = ba_with_ci(s, p, f"E3:{tag}:{kind}", root=roots[1])
    out["pass"] = bool(out["linear"]["upper_one_sided_95"] <= E3_UPPER)
    out["mlp_exceeds_margin"] = bool(out["mlp"]["upper_one_sided_95"] > E3_UPPER)
    return out


# ---------------------------------------------------------------------------------------------------------------------
# E2 state recovery beyond time
# ---------------------------------------------------------------------------------------------------------------------
def ns_basis(x, knots):
    x = np.asarray(x, float)
    k = np.unique(np.asarray(knots, float))
    K = len(k)

    def d(j):
        return (np.maximum(x - k[j], 0) ** 3 - np.maximum(x - k[K - 1], 0) ** 3) / (k[K - 1] - k[j])

    return np.column_stack([x] + [d(j) - d(K - 2) for j in range(K - 2)])


def spline_knots(x_train):
    x = np.asarray(x_train, float)
    return [x.min(), *np.quantile(x, [0.25, 0.5, 0.75]), x.max()]


def e2_auc(rows, rep_by_fold, case_folds, case_sites, tag, extra=None, roots=(SEED_FOLDS, SEED_BOOTSTRAP),
           n_boot=N_BOOTSTRAP):
    """rows: DataFrame with columns case (index into rep arrays), step (row index into the case's rep), time, S.

    extra: optional (n_rows, q) array added to the base (E2 secondary with H). Returns AUCs, ΔAUC and its CI.
    """
    case = rows.case.to_numpy()
    folds = np.asarray(case_folds)[case]
    y = rows.S.to_numpy().astype(float)
    p_base = np.empty(len(rows)); p_full = np.empty(len(rows))
    for v in np.unique(folds):
        tr = np.flatnonzero(folds != v); te = np.flatnonzero(folds == v)
        knots = spline_knots(rows.time.to_numpy()[tr])
        B = ns_basis(rows.time.to_numpy(), knots)
        if extra is not None:
            B = np.hstack([B, extra])
        R = np.vstack([rep_by_fold[v][c][s] for c, s in zip(case, rows.step.to_numpy())])
        F = np.hstack([B, R])
        rng = probe_rng(tag, "E2", int(v), root=roots[0])
        mb = fit_logistic_cv(B[tr], y[tr], case[tr], rng, PENALTY_GRID_E2)
        mf = fit_logistic_cv(F[tr], y[tr], case[tr], rng, PENALTY_GRID_E2)
        p_base[te] = mb.logit(B[te]); p_full[te] = mf.logit(F[te])
    auc_b, auc_f = weighted_auc(y, p_base), weighted_auc(y, p_full)
    ucase, inv = np.unique(case, return_inverse=True)
    Wt = bootstrap_case_weights(np.asarray(case_sites)[ucase], n_boot, boot_rng(f"E2:{tag}", roots[1]))
    d = np.array([weighted_auc(y, p_full, Wt[b][inv]) - weighted_auc(y, p_base, Wt[b][inv]) for b in range(n_boot)])
    lo, hi = np.percentile(d, [2.5, 97.5])
    delta = auc_f - auc_b
    return dict(auc_base=auc_b, auc_full=auc_f, delta_auc=delta, ci_lo=float(lo), ci_hi=float(hi),
                n_rows=int(len(rows)), n_cases=int(len(ucase)),
                **{"pass": bool(delta >= E2_DELTA_AUC and (lo > 0 or hi < 0))})


def e3_state_retention(e2_pre, e2_post):
    if not e2_pre["pass"]:
        return dict(applicable=False, pass_=None, note="E2 primary failed: retention of state information could not "
                                                        "be assessed")
    ratio = e2_post["delta_auc"] / e2_pre["delta_auc"]
    return dict(applicable=True, retained_fraction=float(ratio), pass_=bool(ratio >= E3_RETENTION))


def fm_conditions(e1_278, e1_158, e3_278, e3_158, e3_state):
    """Conditions of P1b-FM / P2-FM (§5.3, §12.2)."""
    return {"E1": bool(e1_278["pass"] and e1_158["pass"]), "E3-site": bool(e3_278["pass"] and e3_158["pass"]),
            "E3-state": bool((not e3_state["applicable"]) or e3_state["pass_"])}


# ---------------------------------------------------------------------------------------------------------------------
# G-SITE (§5.4)
# ---------------------------------------------------------------------------------------------------------------------
def eta2(groups, y):
    """One-way η² (between-group SS / total SS); identical to data_audit/lead/ss_gsite_perW.py."""
    y = np.asarray(y, float)
    m = y.mean()
    tot = ((y - m) ** 2).sum()
    if not tot:
        return 0.0
    return float(sum(len(g) * (g.mean() - m) ** 2 for _, g in pd.Series(y).groupby(np.asarray(groups)))) / tot


def gsite(centre, offset, cells):
    """η² of S at the window start on C (gate), and of Σ_{window∪post} S on C for every (K, P) in ``cells``."""
    centre, offset = np.asarray(centre), np.asarray(offset)
    s0 = (offset >= 0).astype(float)
    g = eta2(centre, s0)
    per_kp = {}
    for c in cells:
        key = f"K{c.K}_P{c.P}"
        if key not in per_kp:
            j = np.arange(0, c.K + c.P)
            per_kp[key] = eta2(centre, (offset[:, None] + j[None, :] >= 0).sum(1))
    return dict(n=int(len(centre)), eta2_S_window_start=g, gate_pass=bool(g <= GSITE_MAX_ETA2),
                P_S1_window_start=float(s0.mean()), eta2_sum_S_window_post=per_kp)
