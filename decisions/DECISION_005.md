# Decision 005: Cosmos tokenizer of Nakamura et al. (2026) as a named reference representation

Investigator decision, recorded by the lead analyst.
* Committed before the site-overlap check (task step 2) and before the tokenizer's fields are collected.

## Decision

* **What is designated.** The Cosmos tokenizer used by Nakamura, Breuer, Crespin, Dietrich & Imai (2026), "Causal
  Inference with Video Features as Treatments", arXiv:2607.06126 (known prior work K4), is a **named reference
  representation**.
* **Outside the competition.** It sits outside the primary / secondary candidate competition of Decisions 003 and 004.
  It is neither a primary nor a secondary candidate, and it is not subject to their eligibility rule (in the secondary
  survey the base Cosmos tokenizer fails the documented-pretraining-data criterion).
* **Reason:** the research question. It is the representation of the paper this work responds to. The designation does
  not rest on any result: no representation has been extracted and no embedding computed.

## Scope

* For the exact tokenizer version that paper used, the same fields are collected as for the other candidates, with
  quoted sources:
  * version;
  * weights location (not downloaded);
  * licence;
  * documented training data;
  * DS203 / Appendix300 overlap (NO / UNKNOWN, with reason);
  * input requirements;
  * latent dimension;
  * compute estimate per hour of video.
* How the reference representation is used is fixed in the SS protocol, not here.
