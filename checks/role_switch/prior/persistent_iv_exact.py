"""Closed-form version of persistent_iv.py (no Monte Carlo, no seed).
Z ~ N(mu,1); A_k = g*Z + e_k, e_k ~ N(0,s^2), k = 1..K+M, no causal A_{k-1}->A_k; Y = sum_k A_k + noise.
MTP: A_k -> delta * A_k^natural for k <= K (window); k > K are post-window natural actions.
Truth: E[Y^d] = delta*K*g*mu + M*g*mu.
Sequential g-formula with history H_k (past actions, optionally + Z): every conditional mean is linear, so the
g-formula mean of each action is exact: m_k = c_k * (mu_k + b_k' (m_H - mu_H)), c_k = delta (k<=K) or 1."""
import numpy as np
def gform_mean(K, M, include_Z, g=1.0, mu=1.0, delta=1.05, s=1.0):
    n = 1 + K + M
    mean = np.r_[mu, np.full(K + M, g * mu)]
    C = np.full((n, n), g * g); C[0, :] = C[:, 0] = g; C[0, 0] = 1.0
    C[np.arange(1, n), np.arange(1, n)] += s * s
    m = {0: mu}                                   # g-formula means; Z is never intervened
    for k in range(1, n):
        H = ([0] if include_Z else []) + list(range(1, k))
        cond = mean[k] + (np.linalg.solve(C[np.ix_(H, H)], C[k, H]) @ (np.array([m[i] for i in H]) - mean[H]) if H else 0.0)
        m[k] = (delta if k <= K else 1.0) * cond
    return sum(m[k] for k in range(1, n))
for K, M in ((1, 0), (2, 0), (15, 0), (1, 30), (15, 30)):
    truth = 1.05 * K * 1.0 + M * 1.0
    a, b = gform_mean(K, M, False), gform_mean(K, M, True)
    print(f"K={K:2d} post-window M={M:2d}: truth {truth:8.4f} | H=past actions bias {a-truth:+.5f} | H=past+Z bias {b-truth:+.1e}")
