# Role-Switch Check — Specification (COMMITTED BEFORE COMPUTING)

**Status: frozen spec. No number in the result files exists at the time of this commit.**

This is a pre-freeze check that supports the draft Data Selection Gate (§0, §5b). It does not freeze the gate.

## 1. Task as received (verbatim, 2026-10-02)

```
TASK: Closed-form check of the role switch with unmeasured confounding.
Commit this spec before computing.

Model: linear Gaussian. Z (trajectory-constant acquisition factor, no
direct effect on Y), U (unmeasured, persistent).
A_t = mu + gamma*Z + alpha*U + eps_t; Y = tau*sum(A_t over window and
post-window) + beta*U + eps_Y. Multiplicative MTP, delta = 1.05, over a
window of K steps; P post-window actions follow their natural course.

Grid: K in {1,2,3,5,15}; P in {0,5,30}; alpha = beta in {0, 0.5, 1};
gamma in {0.5, 1, 2}.
Report, per cell: truth; bias with history only; bias with history + Z;
their difference. For each (P, alpha, gamma), report the smallest K at
which adjusting for Z reduces |bias| (the crossover K*), or "none".
Closed form only, no random draws. Cross-check three cells against the
single-seed Monte Carlo in the chat (K = 1, 5, 15 at P = 0, alpha = beta
= 1, gamma = 1).
Then STOP.
```

## 2. Implementation decisions (fixed here, before computing)

The task leaves the following open. Each choice can move K*, so all are fixed now and none will be changed after
results are seen.

| # | item | fixed value |
|---|---|---|
| I-1 | constants | μ = 1, τ = 1, δ = 1.05 |
| I-2 | exogenous laws | Z ~ N(0, 1), U ~ N(0, 1), ε_t ~ N(0, 1) i.i.d., ε_Y ~ N(0, 1); all mutually independent. E[Z] = E[U] = 0 |
| I-3 | action mechanism | A_t = μ + γZ + αU + ε_t for t = 1 … K+P, exactly as given. There is **no causal effect of past actions on later actions**. Steps 1…K are the window, K+1…K+P are post-window |
| I-4 | trajectory start | the trajectory begins at the first window step; there are no pre-window actions |
| I-5 | intervention | multiplicative MTP on the natural value, A_t^d = δ·A_t^nat for t ≤ K, with natural course for t > K. Natural values do not depend on past actions (I-3), so A_t^nat = A_t |
| I-6 | truth | E[Y^d] = τ·μ·(δK + P) + β·E[U] = τμ(δK + P) |
| I-7 | arms | **history only**: H_t = (A_1, …, A_{t−1}). **History + Z**: H_t = (Z, A_1, …, A_{t−1}). U is never observed |
| I-8 | functional | the sequential g-formula for the recursive MTP, ψ_H = E_g[ E(Y │ O) ], with O = (A_1 … A_{K+P}) or (Z, A_1 … A_{K+P}). Under the g-law, Z (if included) keeps its marginal law. Each A_t is drawn from c_t × (its observed conditional law given H_t), evaluated at the g-law history, with c_t = δ (t ≤ K) or 1 (t > K) |
| I-9 | exactness | all conditionals are linear Gaussian, so the g-law means propagate exactly: m_t = c_t·(E[A_t] + b_tᵀ(m_{H_t} − E[H_t])), with b_t = Σ_{HH}⁻¹ Σ_{H,A_t}. Then ψ_H = E[Y] + w_Oᵀ(m_O − E[O]), with w_O = Σ_{OO}⁻¹ Σ_{O,Y}. **No random draws** |
| I-10 | bias | bias_arm = ψ_arm − truth (population bias of the identifying functional) |
| I-11 | difference | Δ = bias_{H+Z} − bias_{H} (signed). Also reported: Δ_abs = \|bias_{H+Z}\| − \|bias_{H}\| |
| I-12 | crossover | K* = the smallest K in {1, 2, 3, 5, 15} with \|bias_{H}\| − \|bias_{H+Z}\| > 1e-12; otherwise `none`. Also reported, descriptively: whether the reduction then holds at every larger K in the grid |
| I-13 | sanity checks (run before reporting) | (a) at δ = 1 both biases are 0 in every cell; (b) the α = 0, γ = 1 cells reproduce `prior/persistent_iv_exact.py` (K = 1, 2, 15 at P = 0, and K = 1, 15 at P = 30); (c) at K = 1, P = 0 the closed forms bias_H = βα(δ−1)μ / (γ² + α² + 1) and bias_{H+Z} = βα(δ−1)μ / (α² + 1) hold |
| I-14 | **cross-check deviation (disclosed now)** | The Monte Carlo the task names (K = 1, 5, 15, P = 0, α = β = 1, γ = 1) is **not available in this session**. The only single-seed MC here is `prior/persistent_iv.py` (seed 0, N = 2,000,000). Under the mapping Z_prior = 1 + Z, it equals this model at α = β = 0, γ = 1, μ = 1, τ = 1, P = 0, with K = 1, 2, 15. Its printed biases: H-only +0.0013 / +0.0267 / +1.2635; H+Z −0.0003 / +0.0007 / +0.0145. The cross-check is made against those three cells. The three requested cells are reported in closed form, so the investigator can compare them with their own MC. **No new random draw is made** |

## 3. Outputs (`checks/role_switch/`)

* `role_switch_closed_form.py`: the computation.
* `ROLE_SWITCH_GRID.csv`: 135 cells, with truth, bias_H, bias_HZ, Δ and Δ_abs.
* `ROLE_SWITCH_CROSSOVER.csv`: 27 (P, α, γ) rows, with K* and the descriptive monotonicity flag.
* `ROLE_SWITCH_CHECKS.json`: the sanity checks and the cross-check.
* `ROLE_SWITCH_RESULT.md`: a short write-up. **Then STOP.**
