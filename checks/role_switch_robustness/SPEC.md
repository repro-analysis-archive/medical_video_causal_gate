# Role-Switch Robustness — Specification (COMMITTED BEFORE COMPUTING)

**Status: frozen spec. No extension result exists at the time of this commit.**

## 1. Task as received (verbatim, 2026-10-02)

```
TASK: Robustness of the role switch. Commit this spec before computing.
Base: the role-switch model and constants of 0810087.
Extensions, one at a time:
 E1 action persistence: A_t also depends on A_{t-1} with coefficient
    phi_A in {0.5, 0.9}.
 E2 pre-window history: W in {5, 30} natural actions before the window.
 E3 time-varying unmeasured confounding: U_t is AR(1), phi_U in {0.5, 0.9}.
 E4 binary actions: probit assignment, quadrature, same grid where feasible.
For each: the K* map over P in {0, 5, 30}, alpha = beta in {0, 0.5, 1},
gamma in {0.5, 1, 2}; biases reported relative to Psi(delta) - Psi(1).
Report whether "adjusting for Z helps except at K = 1, P = 0" survives each
extension. Closed form or quadrature only. Then STOP.
```

## 2. Prior information (disclosed)

The base map is `checks/role_switch/ROLE_SWITCH_CROSSOVER.csv` (`47a49ea`). It already gives K* = 3 or 5, not 2, in the three rows P = 0, α = β = 1. **The statement is therefore already false in 3 / 27 base rows**, and the base is reported alongside every extension.

## 3. Base (unchanged from `0810087`)

* μ = τ = 1 and δ = 1.05.
* Z, U, ε_t and ε_Y are independent N(0, 1).
* A_t = μ + γZ + αU + ε_t.
* Y = τ·Σ(window + post-window A_t) + βU + ε_Y.
* Window steps 1…K carry the multiplicative MTP A^d = δ·A^nat (natural value at the counterfactual history). The P post-window steps follow their natural course.
* Arms:
  * **history only**: H_t = all past actions;
  * **history + Z**: H_t = Z + all past actions.
* Functional: the sequential g-formula, ψ = E_g[E(Y │ O)], where O is all actions, plus Z in the history + Z arm. It is computed exactly by propagating means (SPEC `0810087` I-8, I-9).

## 4. Extensions (one at a time; everything not listed is the base)

| id | change | settings | truth Ψ(δ) |
|---|---|---|---|
| **E1** | A_t = μ + φ_A·A_{t−1} + γZ + αU + ε_t, with A_0 := 0 (no pre-window actions). Natural values respond to the counterfactual past: A_t^d = c_t(μ + φ_A·A_{t−1}^d + γZ + αU + ε_t), with c_t = δ in the window and 1 after it | φ_A ∈ {0.5, 0.9} | τ·Σ_t e_t, with e_t = c_t(μ + φ_A·e_{t−1}) and e_0 = 0 |
| **E2** | W natural pre-window actions, with the base mechanism, precede the window. They are in both arms' histories and in O, and they do **not** enter Y (c = 1) | W ∈ {5, 30} | τμ(δK + P) |
| **E3** | U_t is stationary AR(1) with unit variance: U_1 ~ N(0, 1), U_t = φ_U·U_{t−1} + √(1 − φ_U²)·η_t. A_t = μ + γZ + αU_t + ε_t, and **Y = τΣA_t + β·U_N + ε_Y, with U taken at the last action step N = K + P** | φ_U ∈ {0.5, 0.9} | τμ(δK + P) |
| **E4** | A_t = 1{μ_b + γZ + αU + ε_t > 0} (probit), with μ_b = 0, so P(A = 1) = 0.5. **Intervention: the binary analogue chosen here (see §5).** For window steps, the natural-value "flip-up" A_t^d = A_t^nat + (1 − A_t^nat)·B_t, with B_t ~ Bernoulli(ρ) independent of everything and **ρ = δ − 1 = 0.05**. Post-window steps are natural. Arm-specific g-law: q_H(1 │ h) = π_H(h) + (1 − π_H(h))·ρ | one setting | τ[(K + P)p̄ + Kρ(1 − p̄)], with p̄ = 0.5 |

## 5. E4 design note (decided now)

* The multiplicative MTP δ·A is undefined for a binary A.
* **The flip-up is a fixed, history-free transformation of the natural value.** The estimand therefore stays the same across adjustment sets, which is the property established for the continuous MTP (`us_ppnr_0A/docs/DRFLEX_MTP_ESTIMAND_AUDIT.md` §3).
* The incremental propensity-score intervention (IPSI) is **not** used. Its policy is defined through the propensity on a history, so it would change the estimand between arms. That is the binary-IPSI question, which is route (a) and off the critical path.

**Computation:**
* Given (Z, U), actions are i.i.d. Bernoulli(Φ(γZ + αU)). The observational conditionals therefore depend only on the count of past ones. The g-formula is a dynamic program over (step, count).
* All moments E[pˢ(1 − p)ⁿ⁻ˢ (·)] use Gauss–Hermite quadrature (`scipy.special.roots_hermitenorm`):
  * the history-only arm uses 2-D quadrature over (Z, U);
  * the history + Z arm uses U-quadrature at each Z node, then integrates over Z.
* **Nodes:** 200 per dimension (primary), with 400 as the convergence check.

## 6. Reported quantities and rules

* **Grid:** K ∈ {1, 2, 3, 5, 15}, P ∈ {0, 5, 30}, α = β ∈ {0, 0.5, 1}, γ ∈ {0.5, 1, 2}. That is 135 cells per extension setting, over 7 settings: E1 × 2, E2 × 2, E3 × 2, E4 × 1.
* **Bias:** ψ_arm(δ) − Ψ(δ).
* **Relative bias:** bias / (Ψ(δ) − Ψ(1)), with Ψ(1) = E[Y], the natural mean (for E4, ρ = 0). Sanity check (a) verifies that ψ_arm(1) = Ψ(1) exactly, so this is also the relative bias of the contrast.
* **K\*:** the smallest K in the grid with |bias_H| − |bias_{H+Z}| > tol, where tol = 1e-12 for E1–E3 and 1e-8 for E4. Otherwise `none`. The pattern string over the K grid is reported too.
* **Statement S** ("adjusting for Z helps except at K = 1, P = 0") holds in a (P, α, γ) row iff:
  * for P = 0, adjusting does **not** help at K = 1 and helps at every K ≥ 2;
  * for P > 0, adjusting helps at every K.

  For each setting, the report gives the rows where S holds (count / 27) and lists the failures, against the base's 24 / 27.
* **Survival verdict:**
  * an extension setting **preserves** S if S holds in every row where it holds in the base;
  * it **breaks** S otherwise, and every newly failing row is listed;
  * rows that **gain** S are also listed.

## 7. Sanity checks (run before reporting; any failure → that setting is UNRESOLVED)

1. **Exact at the natural value:** δ = 1 (ρ = 0 for E4) gives zero bias in every cell and arm (closed form < 1e-10; E4 < 1e-8).
2. **Reduction to the base:**
   * E1 at φ_A = 0;
   * E2 at W = 0;
   * E3 at φ_U = 1.

   Each reproduces `checks/role_switch/ROLE_SWITCH_GRID.csv` (`47a49ea`) to < 1e-9.
3. **E4 quadrature:** 200 vs 400 nodes, max |Δbias| < 1e-8.
4. **E4 independent closed form at K = 1, P = 0:**
   * bias_H = βαρ·0.797885 / √(1 + γ² + α²);
   * bias_{H+Z} = βρ(α / √(1 + α²))·E_Z[φ(c)/Φ(c)], with c = γZ / √(1 + α²), by 1-D quadrature.

   The DP must agree within 1e-8.

## 8. Outputs (`checks/role_switch_robustness/`)

* `role_switch_robustness.py`;
* `ROBUSTNESS_GRID.csv`: setting × 135 cells, with absolute and relative biases;
* `ROBUSTNESS_CROSSOVER.csv`;
* `ROBUSTNESS_CHECKS.json`;
* `ROBUSTNESS_RESULT.md`.

**Then STOP.**
