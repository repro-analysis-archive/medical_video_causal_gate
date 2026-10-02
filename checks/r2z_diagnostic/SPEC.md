# Recoverability Diagnostic R2_Z — Specification (COMMITTED BEFORE COMPUTING)

**Status: frozen spec. No R2_Z value or rule has been computed at the time of this commit.**

## 1. Task as received (verbatim, 2026-10-02)

```
TASK: Does recoverability of Z from history predict the sign? Commit this
spec before computing.
Use the cells already computed in 47a49ea and 6165ece (no new settings).
For each cell compute R2_Z = 1 - Var(Z | H) / Var(Z) at the first window
step, in closed form (base, E1, E2, E3) or by quadrature (E4).
Report: help/hurt (sign of |bias with Z| - |bias without Z|) against
(R2_Z, alpha, K, P), and the best single threshold rule on R2_Z within each
alpha, with its misclassification count.
Stop rule (fixed now): if one rule on (R2_Z, alpha) misclassifies <= 10% of
cells across all seven settings, it becomes the candidate diagnostic.
Otherwise the theory track stops here and the paper uses the conditional
map as is. No further extensions in either case.
Then STOP.
```

## 2. Disclosures (structural facts known before computing)

1. **R2_Z at the first window step is identically 0 in the base, E1, E3 and E4.**
   * In those models there is no action before the first window step, so H is empty (SPEC `0810087` I-4; `04859b2`
     §4).
   * Only E2 has a non-empty history there: W pre-window actions. Its value is
     R2_Z = γ²W / (1 + W(γ² + α²)), which does not depend on K or P.
   * Consequently, within every setting other than E2, a rule on (R2_Z, α) gives the same prediction for all K and P.
2. **The help / no-help labels are already known.** They follow from the committed K* maps (`47a49ea`, `6165ece`).
   Implied by those maps: "always help" misclassifies the cells where Z does not help, about 18–19 % of the 945 cells
   of the seven `6165ece` settings. This test is therefore **not blind to the labels**. It is a mechanical
   evaluation of a rule family fixed in advance.

## 3. Definitions (fixed here)

| # | item | definition |
|---|---|---|
| R-1 | cells | the 945 cells of the seven `6165ece` settings: E1 φ_A ∈ {0.5, 0.9}, E2 W ∈ {5, 30}, E3 φ_U ∈ {0.5, 0.9}, and E4. **"All seven settings" in the stop rule = these seven.** The 135 base cells (`47a49ea`) are reported separately, together with a descriptive 8-setting total, and are **not** part of the stop rule |
| R-2 | biases | read from the committed CSVs (`ROLE_SWITCH_GRID.csv`, `ROBUSTNESS_GRID.csv`). No recomputation |
| R-3 | label | **help** iff \|bias_{H+Z}\| < \|bias_H\| − tol, with tol = 1e-12 for continuous settings and 1e-8 for E4 (as for K*). Otherwise **no help**. Exact ties are counted inside "no help" and also reported separately |
| R-4 | R2_Z (primary, binding) | R2_Z = 1 − E_H[Var(Z │ H)] / Var(Z), with H = all observed actions before the first window step, under the observational law. For a linear-Gaussian model Var(Z │ H) is constant, so this is the stated formula. For E4 the history is empty (R2_Z = 0), so no quadrature is needed; the quadrature path is kept for completeness |
| R-5 | rule family | for each α separately: predict **help** iff R2_Z > c, or **help** iff R2_Z ≤ c, with c ∈ {−∞} ∪ {the distinct R2_Z values at that α}. Constant rules (always help / never help) are included. The minimiser of misclassifications within α is chosen; ties go to the smallest c, then to "help iff R2_Z > c". The **rule on (R2_Z, α)** is the triple of per-α thresholds, and its misclassification count is the sum over α |
| R-6 | stop rule (from the task) | **CANDIDATE DIAGNOSTIC** iff the R-5 rule misclassifies ≤ 10 % of the 945 cells, i.e. ≤ 94 cells. Otherwise **THEORY TRACK STOPS**, and the paper uses the conditional map as is. No further extension either way |
| R-7 | secondary (non-binding, descriptive only) | R2_Z at the **last window step**: H = W pre-window actions + the K − 1 earlier window actions, observational law, E_H[Var(Z │ H)]. For E4 this uses Gauss–Hermite quadrature (200 nodes, 400-node check) over the binary history count. The same R-5 rule family is evaluated and reported. **It cannot change the R-6 outcome**, which is decided on R-4 only |

## 4. Outputs (`checks/r2z_diagnostic/`)

* `r2z_diagnostic.py`;
* `R2Z_CELLS.csv`: setting, K, P, α, γ, R2_Z (primary and secondary), label;
* `R2Z_RULES.json`;
* `R2Z_RESULT.md`.

**Then STOP.**
