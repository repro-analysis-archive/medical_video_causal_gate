# Role-Switch Robustness — Result (closed form E1–E3; Gauss–Hermite quadrature E4; no random draws)

* **Spec:** `SPEC.md`, committed **`04859b2`** before computing.
* **Base:** `checks/role_switch` (spec `0810087`, result `47a49ea`).
* **Code:** `role_switch_robustness.py`. Run time 2 min 47 s.
* **Data:**
  * `ROBUSTNESS_GRID.csv`: 7 settings × 135 cells, with absolute and relative biases;
  * `ROBUSTNESS_CROSSOVER.csv`;
  * `ROBUSTNESS_CHECKS.json`.

## 1. Sanity checks: all PASS

| check | result |
|---|---|
| 1. Zero bias at the natural value (δ = 1; for E4, ρ = 0) | max \|bias\| ≤ 1.1e-13 |
| 2. Reduction to the base grid (E1 φ_A = 0, E2 W = 0, E3 φ_U = 1) | max \|diff\| 5.0e-10. This is the 10-significant-digit rounding of the committed base CSV |
| 3. E4 quadrature, 200 vs 400 nodes | max \|Δbias\| 7.7e-9 |
| 4. E4 K = 1, P = 0 against an independent closed form | max error 6.9e-16 |

**Decision margins.** The smallest margin, min ‖bias_H| − |bias_{H+Z}‖ over non-trivial cells, is ≥ 9.8e-6 in every
setting, and 2.8e-4 for E4. So no help / no-help decision is within numerical error.

## 2. K* maps (smallest K at which adjusting for Z reduces |bias|)

The three γ columns are shown as one entry where they coincide.

| P | α = β | base | E1 φ_A = .5 | E1 φ_A = .9 | E2 W = 5 | E2 W = 30 | E3 φ_U = .5 | E3 φ_U = .9 | E4 binary |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 0 | 0.5 | 2 | 2 | 2 | **5** | **none** | 2 | 2 | **3** |
| 0 | 1 | 5 / 3 / 3 | 5 / 5 / 3 | 5 | **15** | **none** | **2** | 3 | **15** |
| 5 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 5 | 0.5 | 1 | 1 | 1 | 1 | **15** | 1 | 1 | 1 |
| 5 | 1 | 1 | 1 | 1 | **5** | **none** | 1 | 1 | 1 |
| 30 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 30 | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 30 | 1 | 1 | 1 | 1 | 1 | **15** | 1 | 1 | 1 |

(For a / b / c entries, the order is γ = 0.5 / 1 / 2.) Every pattern is monotone: once adjusting helps, it helps at
every larger K in the grid.

## 3. Statement S: "adjusting for Z helps except at K = 1, P = 0"

The rule is frozen in SPEC §6. **The base already fails S in 3 / 27 rows** (P = 0, α = 1); this was disclosed before
computing.

| setting | rows where S holds | verdict | rows newly failing |
|---|---|---|---|
| base | 24 / 27 | — | — |
| E1 action persistence, φ_A = 0.5 | 24 / 27 | **PRESERVES** | none |
| E1 action persistence, φ_A = 0.9 | 24 / 27 | **PRESERVES** | none |
| E2 pre-window history, W = 5 | 18 / 27 | **BREAKS** | P = 0, α = 0.5 (K* = 5); P = 5, α = 1 (K* = 5) |
| E2 pre-window history, W = 30 | 12 / 27 | **BREAKS** | P = 0, α = 0.5 (never helps); P = 5, α = 0.5 (K* = 15); P = 5, α = 1 (never helps); P = 30, α = 1 (K* = 15) |
| E3 AR(1) U, φ_U = 0.5 | **27 / 27** | **PRESERVES** (and gains the 3 base-failing rows) | none |
| E3 AR(1) U, φ_U = 0.9 | 24 / 27 | **PRESERVES** | none |
| E4 binary (probit, flip-up ρ = 0.05) | 21 / 27 | **BREAKS** | P = 0, α = 0.5 (K* = 3) |

Each "newly failing" entry covers all three γ.

## 4. What survives every setting (descriptive; these models and constants only)

1. **K = 1, P = 0: adjusting for Z never helps, in all 7 settings.** It is neutral at α = 0, and amplifies the U-bias
   at α > 0.
2. **No unmeasured confounding (α = 0): adjusting for Z helps in every other cell, in all 7 settings.** That is,
   K* = 2 at P = 0 and K* = 1 at P > 0.
3. **With unmeasured persistent confounding, "helps everywhere else" is not robust.**
   * Pre-window history delays or removes the benefit. At W = 30, P = 0 and α ≥ 0.5, adjusting for Z never helps up
     to K = 15. The pre-window actions are proxies that already recover much of Z, so adjusting for Z directly adds
     mostly amplification.
   * Binary actions delay the switch, to K* = 3 at α = 0.5 and 15 at α = 1.
   * Action persistence and AR(1) confounding leave the base pattern essentially intact. φ_U = 0.5 even makes it
     cleaner.

**Relative bias** (bias / (Ψ(δ) − Ψ(1))). The median |relative bias| is lower with Z than without in every setting:

| setting | history only | history + Z |
|---|---|---|
| E1 φ_A = 0.5 | 2.20 | 0.74 |
| E1 φ_A = 0.9 | 1.38 | 0.52 |
| E2 W = 5 | 0.86 | 0.38 |
| E2 W = 30 | 0.21 | 0.09 |
| E3 φ_U = 0.5 | 2.33 | 0.20 |
| E3 φ_U = 0.9 | 2.79 | 0.78 |
| E4 binary | 2.37 | 0.95 |

Biases of the order of the true contrast or larger are common.

**Scope.**
* These are linear-Gaussian or probit toy models, with no action → state feedback. All constants are as in
  `0810087`.
* E4 uses the natural-value flip-up intervention, not IPSI (SPEC §5).
* Nothing here is a claim about real data or any other DGP.

## STOP

No further computation was done. The gate is not frozen, and the H1R and theory repositories were not touched.
