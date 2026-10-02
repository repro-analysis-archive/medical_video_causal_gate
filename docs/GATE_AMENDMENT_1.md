# GATE AMENDMENT 1 — Contingent fallback (DRAFT)
Frozen before any file of CathAction, Trauma THOMPSON or SAGES CVS is
accessed.

## Disclosure
Drafted after the v4 data audit (dd142f6), which found no public dataset
with per-trajectory acquisition metadata meeting D4 at the required counts.
This is a feasibility outcome, not a result on the causal question.

## Trigger
Active only if, after the three access-gated datasets are audited under v4
unchanged, no dataset passes the SS arm. Otherwise this amendment is void.

## SS' arm (replaces the SS arm when active)
- Acquisition factor: synthetic, applied per trajectory by a known rule.
  Transform family, frozen now: contrast/gamma, Gaussian blur, compression
  level, down-up resampling, colour temperature. Four levels per factor.
  Assignment independent of content, so D8 holds by construction.
- Encoding check, before use: a transform is used only if the chosen
  representation decodes its level with balanced accuracy >= 0.90 on
  held-out trajectories. Transforms failing this are excluded, and the
  exclusions are reported.
- Requirements: D3, D5, D6, D7 and >= 200 trajectories. D4 and D8 are
  replaced by the synthetic factor.
- Candidate pool: every dataset in the dd142f6 audit log, plus any found by
  the completed Semantic Scholar arm.
- Ranking: total trajectories; then D7 annotation density; then access
  without registration; remaining tie to human decision.
- None passes: STOP for human decision.

## Claim ceiling when active
Results concern acquisition-like information introduced by known
transforms. They do not establish how real site, device or operator
differences behave. Any dataset with real per-trajectory acquisition labels
(e.g., Cataract-101, surgeon) may be analysed descriptively as a sanity
check, never as a primary result.

## Unchanged
All of v4 §5b, §6 and §7.
