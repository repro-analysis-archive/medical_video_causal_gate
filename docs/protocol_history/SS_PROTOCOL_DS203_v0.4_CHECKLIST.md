# SS protocol v0.4: checklist (task item → section in SS_PROTOCOL_DS203_DRAFT_v0.4.md)

**Diffs:**
* v0.2 → v0.4 consolidated: `SS_PROTOCOL_DS203_v0.2_to_v0.4.diff`. No v0.3 draft existed; neither v0.3 task had been
  applied.
* Final pre-freeze edits only: `SS_PROTOCOL_DS203_v0.4_final_prefreeze_edits.diff`. The superseded
  `CC_TASK_SS_protocol_v0.4_D6_and_prefreeze.md` was never received or applied.

Eligibility facts: current d3563e7; prior 6245f25 → e81ab5f → a437225 → ca04c5b / d3563e7

## A. Consolidated task (CC_TASK_SS_protocol_v0.4_consolidated.md)

| item | requirement | where in v0.4 |
|---|---|---|
| P1 D-1 | adopt v0.2 rule | §7.2 |
| P1 D-1 | offsets fixed once per case, unchanged across cells, arms, replicates | §7.2 |
| P1 D-1 | "deliberately constructed orthogonal benchmark using real video and real acquisition heterogeneity" | §1, §7.2, §13, §16 |
| P1 D-1 | disclosure text, verbatim | §7.2 |
| P1 D-1 | rejected rules (fixed 280-s anchor; uniform random) kept | §7.2 |
| P1 D-3 | 320×320 after crop and mask; pooled 16×40×40 | §4.2 |
| P1 D-3 | "paper-linked Cosmos reference …"; not a pixel-level replication | §4.2, §8, §13 |
| P1 D-4 | upper 95 % bound ≤ 0.35 | §5.3 |
| P1 D-4 | "no longer exceeds the prespecified linear site-encoding boundary"; never "equivalent to chance" / "eliminated" | §5.3, §13 |
| P1 D-4 | "linearly site-removed" and the nonlinear-residual ceiling | §4.3, §5.3, §13 |
| P1 D-5 | primary common n = 158 | §2 |
| P1 D-5 | per-W sensitivity sets 204 / 201 / 158, with scope | §2, §10.3 |
| P2.1 | source hierarchy levels 1–5; NO only with level-1–3 support; UNK ineligible | §4.1.1 |
| P2.2 | clip-level definition, verbatim | §4.1.2 |
| P2.3 | mutually exclusive classes | §4.1.3 |
| P2.4 | class-definition disclosure | §0, §4.1.3 |
| P2.5 | eligibility re-determined with level-1–3 quotes; lists; no ranking; no selection | §4.1.5; commit 6245f25 (historical) |
| P3.1 | post-window S statement replaced by 1{O_i + j ≥ 0} text | §7.2, §16 |
| P3.2 | P1b relabelled (superseded by B.2: all families theory-motivated) | §12.1, §12.2, §18 |
| P3.3 | P1a reason (now stated as an identification correspondence, not a directional proof; see B.2) | §12.1 |
| P3.4 | P2 families unchanged (cells / predictions / conditions) | §12.2 |
| P4 | E1 / E3 on 278 and 158 | §5, §5.1, §5.3 |
| P4 | 158 results never used for model selection | §5, §15 |
| P4 | 278 pass / 158 fail → FM vs FM−C descriptive | §13 |
| P5.A | 7-day budget; reductions (a)–(c); family cells never reduced; STOP | §10.4, §14 step 2 |
| P5.B | conditioning set H_t + step-t covariates | §8 |
| P5.C | folds on 278 (seed 20261006); PCA / LEACE on 278 training folds; nuisances on 158 training folds | §2, §4.2, §4.3, §9 |
| P5.D | G-SITE as a design verification; marginal-independence note | §5.4 |
| P5.E | site loadings: pre-fixed permutation seed, same mapping for all arms, generic site-identity signal | §6 |
| P5.F | fixed cells; within-cell replicate resampling with paired indices | §12.3 |
| P5.G | FULL = exchangeability oracle / implementation sanity reference | §8, §13 |
| P5.H | in-house SDR; DR-FLEX / V3-C05 not used; estimator gate | §9, §14 step 2 |

## B. Final pre-freeze task (CC_TASK_SS_protocol_v0.4_final_prefreeze.md)

| item | requirement | where in v0.4 |
|---|---|---|
| 1.A | rule A: YES / NO / UNK definitions; UNK ineligible | §4.1.1 |
| 1.B | rule B: generic web origin does not change NO to UNK; limitation text verbatim | §4.1.1, §16 |
| 1.C | rule C: same-hospital rule for clinical / endoscopic sources only | §4.1.1, §4.1.4 rule 2 |
| 1 | justification (consistency with 052590c; purpose; strict reading leaves none) and disclosure sentence, verbatim | §4.1.1, §0 |
| 2 | all six families relabelled "theory-motivated prespecified hypotheses"; none "theory-derived" | §12.1, §12.2 |
| 2 | reason (DGP differences; no transport proof) | §12.1 |
| 2 | "consistent / inconsistent with the theory-motivated direction"; verdict rules unchanged | §1, §12.1, §12.3, §13 |
| 2 | earlier labels and reason kept in version history | §18 |
| 3 | primary / secondary / reference claim wording; "video-derived representations"; no "temporal video foundation model" for a frame-level primary | §1, §4.1.3, §4.2, §13, §16 |
| 4 | GPU feasibility: parameter count / checkpoint size = prior screen; synthetic-input test (inference, batch 1, bf16, protocol input and clip length, extraction stack, no DS203 frame); ≤ 20.0 GB peak reserved; failing → next-ranked | §4.1.4 rule 4, §4.1.5, §14 step 3 |
| 5 | extraction compute fallback: synthetic-input throughput + measured disk / decode (2012acd); > 7 days → next-ranked; no quality / real-frame / causal input | §10.4, §4.1.4 rule 5, §14 step 3 |
| 6 | tie-breaks: level-1 authors' default (not inferred) → lower compute → lower synthetic-input peak memory → lexical identifier; no DS203 quality / throughput / causal input | §4.1.4, §4.1.5 |
| 7 | exact SDR code commit recorded at code lock and referenced before the grid; estimator gate synthetic only | §9, §14 steps 2 and 6 |
| 8 | eligibility facts committed as one commit before, and separate from, the protocol; hash in §0 and §4.1 | 6245f25 (historical); header, §0, §4.1.5 |
| 9.1 | checklist updated | this file |
| 9.2 | eligible lists under the two-level rule, with tie-break order; no ranking; no selection | §4.1.5 |
| 9.3 | key scan clean; H1R and theory repositories untouched | verified (report) |

## C. Freeze repairs (CC_TASK_SS_protocol_v0.4_freeze_repairs.md; marked [v0.4-final2])

Stage 1 of the superseded `…_last_edits_and_freeze.md` was never received, so Parts A and B were applied together.
Diff of this task only: `SS_PROTOCOL_DS203_v0.4_freeze_repairs.diff`.

| item | requirement | where in v0.4 |
|---|---|---|
| A1 | per-W offsets check: missing (46 for W = 0, 43 for W = 5) → rule, new file, counts, max V; committed before the protocol | §7.2 (rule), §10.3 (file, counts, max V), header, §0; commit adf9160 |
| A2 | clip-level temporal-sampling sentence, verbatim | §4.2, §16 |
| B1 | Rule-B override text, verbatim | §4.1.1 |
| B1 | re-check of §4.1.5 | §4.1.5; commit e81ab5f. **Change:** Basel V-JEPA ViT-L becomes eligible (primary, clip-level) |
| B1 (added) | determinism sentence: the override does not lift Rule A's clinical / site-provenance clause (LEMON, SVL stay UNK) | §4.1.1 (flagged as not in the task text) |
| B2 | §1 question: "site-associated information … video-derived representations" | §1 |
| B2 | acquisition heterogeneity is one source; E1 / LEACE do not isolate acquisition information | §1, §16 |
| B2 | "acquisition shortcuts" kept in the §13 native-arm item | §13 (unchanged) |
| B2 | other listed sections (§4.3, §5, §12, §13, §16): no unqualified "acquisition information" occurred, so nothing to replace | — |
| B3 | "real foundation-model representations" → "real pretrained video-derived representations"; foundation-model naming condition | §1 |
| B4 | E3-site (278 and 158) / E3-state-retention (158 only; not applicable when E2 primary fails, with report statement) | §5, §5.3 |
| B4 | FM−C interpretation / P1b-FM / P2-FM conditions use the new names | §5.3, §12.2, §13 |
| all | one §18 line per change | §18 |
| Stage 2 | not started (awaits "FREEZE GO") | — |

## D. Content-boundedness Rule B (CC_TASK_SS_protocol_v0.4_B1_content_bounded.md; marked [v0.4-final3])

The `…_accept_B1` task was never received or applied, so there was nothing to reverse. Diff of this task only:
`SS_PROTOCOL_DS203_v0.4_final3_content_bounded.diff`.

| item | requirement | where in v0.4 |
|---|---|---|
| 1 | Rule B replaced verbatim; no benchmark or model named inside the rule; the v0.4-final2 override and determinism sentence removed | §4.1.1 |
| 2 | per-source boundedness with quotes for every source of every candidate; rule applied; secondary sources re-checked | commit a437225 (`per_candidate_source_boundedness`, `ontology_term_check`); §4.1.5 |
| 2 | result: HowTo100M UNK (Health category) → Basel V-JEPA ineligible; secondary unchanged | §4.1.5 |
| 2 | recomputed facts committed separately, before the protocol; hash in §0 and §4.1.5 | a437225; header, §0, §4.1.5 |
| 3 | §4.1.5 lists | §4.1.5 |
| 3 | §1 and §16 frame-level statements restored | §1, §16 |
| 3 | §16 generic-web list restricted to benchmarks relied on by eligible candidates | §16 |
| 4 | per-W G-SITE values (W = 0 0.0037; W = 5 0.0045) and interpretation rule | §10.3 (rule and values), §5.4 (pointer); commit b987010 |
| 5 | version-history text, verbatim | §18 |
| D-init | EndoSSL initialization check (CC_TASK_SS_protocol_v0.4_EndoSSL_init_check.md): initialization of every eligible model checked against level-1–3 sources; EndoSSL laparoscopy ViT-B / ViT-L / ViT-S not stated → ineligible; all others stated (quotes) | §4.1.5; facts ca04c5b + d3563e7 (in force); header, §0; §18 line; diff `SS_PROTOCOL_DS203_v0.4_endossl_init_check.diff` |
| D-fix | §0 editing correction ("eligible lists are therefore known" sentence returned to the eligibility bullet) | §0, §18 |
| D-loss | loss-network clause, verbatim (CC_TASK_SS_protocol_v0.4_loss_network_clause.md); auxiliary networks of every eligible model checked; no eligibility change (facts in force d3563e7) | §4.1.1; §18 line |
