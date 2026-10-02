"""Toy check (exact, Gaussian): does a trajectory-constant factor Z that drives every step of the natural
policy, with NO direct effect on Y, remain a valid instrument for a recursive natural-value MTP when
(i) the intervention is sustained through the outcome time and the outcome depends only on window actions?
Z ~ N(mu,1); A_k = g*Z + e_k (k=1..K, no causal A_{k-1}->A_k); Y = sum_k A_k + noise.
MTP: every A_k -> delta * A_k^natural(counterfactual history). Truth E[Y^d] = delta*K*g*mu.
Estimators: sequential g-formula / IPW with exact Gaussian conditionals, history H_k = past actions (as H^P
contains past commands), or H_k = past actions + Z, or H_k = empty."""
import numpy as np
def run(K, g=1.0, mu=1.0, delta=1.05, s=1.0):
    # joint Gaussian of (Z, A_1..A_K); exact sequential g-formula for linear-Gaussian with E[Y|.] = sum a_k
    # Q-recursion: Q_k(h) = E_{a_k ~ push-forward of f(A_k|h)}[...]; linear in h, so propagate means exactly
    import itertools
    n = K + 1
    mean = np.r_[mu, np.full(K, g * mu)]
    C = np.zeros((n, n)); C[0, 0] = 1.0
    for i in range(1, n):
        C[0, i] = C[i, 0] = g
        for j in range(1, n):
            C[i, j] = g * g + (s * s if i == j else 0.0)
    def gform(include_Z, use_past):
        # simulate the g-formula exactly by Monte Carlo on the *g-formula* law (not the truth), large N
        rng = np.random.default_rng(0); N = 2_000_000
        Zc = rng.normal(mu, 1.0, N) if include_Z else None
        hist = []; total = np.zeros(N)
        for k in range(1, K + 1):
            idx_h = ([0] if include_Z else []) + ([i for i in range(1, k)] if use_past else [])
            if idx_h:
                Shh = C[np.ix_(idx_h, idx_h)]; Sah = C[k, idx_h]; b = np.linalg.solve(Shh, Sah)
                hv = np.column_stack(([Zc] if include_Z else []) + ([hist[i - 1] for i in range(1, k)] if use_past else []))
                m = mean[k] + (hv - mean[idx_h]) @ b; v = C[k, k] - Sah @ b
            else:
                m = np.full(N, mean[k]); v = C[k, k]
            a_nat = m + np.sqrt(v) * rng.standard_normal(N)      # natural law at the counterfactual history
            a = delta * a_nat; hist.append(a); total += a
        return total.mean()
    truth = delta * K * g * mu
    return truth, gform(False, True), gform(True, True), gform(False, False)
for K in (1, 2, 15):
    t, past, pastZ, empty = run(K)
    print(f"K={K:2d} truth={t:.4f}  H=past actions: {past:.4f} (bias {past-t:+.4f})  H=past+Z: {pastZ:.4f} ({pastZ-t:+.4f})  H=empty: {empty:.4f} ({empty-t:+.4f})")
