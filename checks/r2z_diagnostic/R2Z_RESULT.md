# Recoverability Diagnostic R2_Z — Result

## Outcome (stop rule fixed in the task and in `SPEC.md`, `a45298d`): **THEORY TRACK STOPS**

* The best rule on (R2_Z, α) misclassifies **136 of 945 cells (14.4 %)** across the seven `6165ece` settings. The
  limit was 94 cells (10 %).
* The paper uses the conditional map as is.
* No further extensions are made.

**Inputs and checks:**
* inputs: the committed biases only (`47a49ea`, `6165ece`). No model was re-solved; R2_Z was computed in closed form,
  plus quadrature for the E4 secondary;
* the E2 closed form R2_Z = γ²W / (1 + W(γ² + α²)) is reproduced to 4.4e-16;
* E4 secondary quadrature, 200 vs 400 nodes: 4.9e-9;
* data: `R2Z_CELLS.csv` and `R2Z_RULES.json`.

## 1. Best per-α threshold rules (primary R2_Z at the first window step; binding)

| α = β | best rule | misclassified |
|---|---|---|
| 0 | always help | 21 / 315: the K = 1, P = 0 ties, 3 per setting |
| 0.5 | help iff R2_Z ≤ 0.899 | 51 / 315 |
| 1 | help iff R2_Z ≤ 0.172 | 64 / 315 |
| **total** | | **136 / 945 (14.4 %) > 94 → STOP** |

**Reference points:**
* The constant rule "always help" misclassifies 176 / 945 (18.6 %). R2_Z improves on it by 40 cells, all in E2.
* The non-binding secondary, R2_Z at the last window step, does worse: 172 / 945 (18.2 %).
* The base alone (outside the stop rule) gives 13 / 135 (9.6 %) with the constant rule. R2_Z is 0 throughout the
  base, so it plays no part there.

## 2. Why R2_Z cannot carry the sign

**The binding R2_Z is 0 by construction** in 5 of the 7 settings (E1, E3, E4) and in the base, since there is no
history before the window (disclosed in SPEC §2).

**In E2, R2_Z varies with γ but not with K or P, while the sign follows K and P.**

Help rate, seven settings pooled (help cells / cells):

| K \ P | 0 | 5 | 30 |
|---|---|---|---|
| 1 | **0 / 63** | 54 / 63 | 60 / 63 |
| 2 | 36 / 63 | 54 / 63 | 60 / 63 |
| 3 | 43 / 63 | 54 / 63 | 60 / 63 |
| 5 | 51 / 63 | 57 / 63 | 60 / 63 |
| 15 | 57 / 63 | 60 / 63 | 63 / 63 |

By α and recoverability:

| α | R2_Z = 0 | R2_Z > 0 (E2) |
|---|---|---|
| 0 | 210 / 225 | 84 / 90 |
| 0.5 | 207 / 225 | 54 / 90 |
| 1 | 187 / 225 | 27 / 90 |

* Recoverability from pre-window history is **associated** with "no help" under unmeasured confounding. This is the
  E2 finding of `6165ece`.
* But one threshold on R2_Z within α cannot separate the cells. The K = 1, P = 0 cells and the K-dependent switch
  sit at the same R2_Z.
* The two fitted non-constant thresholds (0.899 at α = 0.5, 0.172 at α = 1) each split E2 cells by γ. They should
  be read as in-sample fits on a small set of distinct values, not as mechanisms.

## STOP

The theory track stops here, per the fixed rule. The gate is not frozen, and the H1R and theory repositories were not
touched.
