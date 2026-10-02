# Role-Switch Check — Result (closed form, no random draws)

**Spec:** `SPEC.md`, committed **`0810087`** before computing.
**Code:** `role_switch_closed_form.py`.
**Data:**
* `ROLE_SWITCH_GRID.csv`: 135 cells;
* `ROLE_SWITCH_CROSSOVER.csv`: 27 rows;
* `ROLE_SWITCH_CHECKS.json`.

**Fixed constants** (SPEC I-1, I-2): μ = τ = 1 and δ = 1.05; Z, U and all noise terms are independent N(0, 1).

## 1. Sanity checks (SPEC I-13): all PASS

| check | result |
|---|---|
| (a) δ = 1 gives zero bias in all 270 cell × arm evaluations | max \|bias\| = 0 |
| (b) α = 0, γ = 1 reproduces `prior/persistent_iv_exact.py` (5 cells × 2 arms) | max \|diff\| < 1e-10 |
| (c) K = 1, P = 0 closed forms βα(δ−1)μ/(γ²+α²+1) and βα(δ−1)μ/(α²+1) | max error < 1e-12 |

## 2. Cross-check (SPEC I-14, the disclosed substitution)

**The MC the task names was not available in this session.** That MC is the investigator's, at α = β = 1, K = 1, 5,
15. The cross-check was made instead against the only single-seed MC here, `prior/persistent_iv.py` (seed 0,
N = 2,000,000), which is this model at α = β = 0, γ = 1, P = 0.

| K | arm | MC (printed) | closed form | MC SE (exact g-law variance / N) | z |
|---|---|---|---|---|---|
| 1 | history | +0.0013 | 0 | 0.00105 | +1.24 |
| 2 | history | +0.0267 | +0.02625 | 0.00184 | +0.24 |
| 15 | history | +1.2635 | +1.25956 | 0.01243 | +0.32 |
| 1 | history + Z | −0.0003 | 0 | 0.00105 | −0.29 |
| 2 | history + Z | +0.0007 | 0 | 0.00182 | +0.38 |
| 15 | history + Z | +0.0145 | 0 | 0.01150 | +1.26 |

All |z| ≤ 1.26, consistent with Monte Carlo error.

**The cells requested for comparison with the investigator's MC** (P = 0, α = β = 1, γ = 1), in closed form:

| K | truth | bias, history | bias, history + Z |
|---|---|---|---|
| 1 | 1.05 | +0.016667 | +0.025000 |
| 5 | 5.25 | +0.294573 | +0.271787 |
| 15 | 15.75 | +1.576136 | +1.385162 |

## 3. Crossover K* (smallest K at which adjusting for Z reduces |bias|)

| P | α = β | γ = 0.5 | γ = 1 | γ = 2 |
|---|---|---|---|---|
| 0 | 0 | 2 | 2 | 2 |
| 0 | 0.5 | 2 | 2 | 2 |
| 0 | 1 | **5** | **3** | **3** |
| 5 | 0, 0.5, 1 | 1 | 1 | 1 |
| 30 | 0, 0.5, 1 | 1 | 1 | 1 |

In every (P, α, γ) row, once Z helps it helps at every larger K in the grid (`reduction_at_all_larger_K = True`).

## 4. What the grid shows (descriptive; this model and these constants only)

* **Role switch with P = 0.**
  * At **K = 1**, adjusting for Z **increases** |bias| whenever α > 0. This is the classical amplification of
    U-bias by an instrument: (α² + 1)⁻¹ against (γ² + α² + 1)⁻¹. With α = 0 both arms are unbiased, so there is no
    reduction.
  * From **K = 2** (α ≤ 0.5), or from **K = 3–5** (α = 1), adjusting for Z **reduces** |bias|. Z confounds the
    action-to-next-action step of the recursion, and that effect overtakes the amplification.
* **Stronger U delays the switch, and a weaker instrument delays it further.**
  * With α = 1: K* = 5 at γ = 0.5, and 3 at γ = 1 or 2.
  * The γ = 0.5, K = 3 cell is a near-tie: Z is worse by only 2.6e-5.
* **With any post-window natural actions (P = 5 or 30), K* = 1 everywhere.** Even at K = 1, Z confounds through
  the later actions it drives: the simulator's J mechanism. In this grid that dominates the amplification. At
  α = 1, P = 30, γ = 2, adjusting for Z cuts the bias from 1.258 to 0.775.
* **Adjusting for Z never removes the U-driven bias.** With α = 1, bias_{H+Z} is independent of γ and stays large
  (1.385 at K = 15, P = 0).

**Implications for the gate's §5b** (for the investigator; nothing is decided here):
* A trajectory-constant factor behaves as an amplifier only when **K = 1 and P = 0**.
* Under unmeasured persistent confounding, the region where it is a confounder can begin later than K = 2, at K = 3
  or 5 in this grid.
* All values depend on the fixed constants (μ, τ, the variances, δ). K* is not claimed outside them.

## STOP

No further computation was done. Nothing in the gate was frozen, and the H1R and theory repositories were not
touched.
