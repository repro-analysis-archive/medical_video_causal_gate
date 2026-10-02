# Literature Gate Result (gate `baadf5c` §6): updated after the Semantic Scholar and proceedings arms

**Verdict: GO.**
* No source puts L1 and L2 together, and no source reaches L2, L3 or L4 at DIRECT or PARTIAL.
* The headline, the benchmark-novelty claim (L3) and the duration claim (L4) are retained.
* The verdict is unchanged from `01be89e`. That version was conditional on the BLOCKED Semantic Scholar and proceedings
  arms, which have now been run in full (keyed client, `0ac6aee`; 440 / 440 sub-queries).
* Six works remain UNRESOLVED (full text unobtainable, §5). None can change the verdict: each is open only on L1 at
  most PARTIAL, or on L3.

## 1. What was run

| arm | status | records |
|---|---|---|
| PubMed, arXiv (4 categories), OpenAlex: Q1–Q4 | done (`01be89e`) | 753 hits → 721 unique (N0000–N0720) |
| Citation chasing from K1–K4 and N0712 (OpenAlex; PDF reference lists) | done (`01be89e`) | 298 (C0000–C0297) |
| **Semantic Scholar**, Q1–Q4 split into 120 + 36 + 4 + 60 = 220 sub-queries | **done 2026-10-02** | 220 / 220 returned; 100 merged per query |
| **Proceedings: MICCAI, IPMI, MIDL, NeurIPS, ICML, CLeaR, UAI** (S2 venue filter, venue erratum §9), 220 sub-queries | **done 2026-10-02** | 220 / 220 returned; 100 merged per query |
| Citation chasing from the new PARTIAL hits (S0414, S0209, S0446, S0460) | done 2026-10-02 | 227 (C0298–C0524) |

* **Semantic Scholar and proceedings arms:** 800 hits → 748 unique (S0000–S0747). 49 duplicate already-screened
  records and inherit those decisions. Of the 699 screened: 37 FULLTEXT (S5), the rest NONE or RELATED.
* **Rate limits:** 262 HTTP 429 responses, all resolved within the 2–32 s backoff; no stop.
* **API key:** never logged or stored. A scan of the repository, LaCie and the scratchpad found it in 0 files.
* **New citation records:** 30 FULLTEXT, of which 9 are works already graded (S6).
* **Log:** every screened record (1,994) is in `RECORDS.csv`, with lead grades for every FULLTEXT record.
* **Full texts:** read by the lead analyst for 4 known works and 35 others (18 + 7 + 10), plus 4 full-text scans;
  quotes in `FULLTEXT_NOTES.md` K1–K4 and
  S1–S6.

## 2. Per-claim tables (DIRECT and PARTIAL in full; RELATED summarized)

### L1. Generative or foundation video representations used as adjustment covariates for the effect of an action or treatment

| grade | sources (location of quote in FULLTEXT_NOTES) |
|---|---|
| **DIRECT (non-medical video)** | **K4** Nakamura, Breuer, Crespin, Dietrich & Imai (2026), arXiv:2607.06126: "we first reproduce each video using a deep generative model and leverage the model's internal representations as learned, low-dimensional summaries of video content for causal estimation" (Abstract, p. 1) |
| PARTIAL, non-medical **video**, with representations as the **outcome model** in randomized experiments (not adjustment covariates) | **S0414** Cadei et al. 2025, Prediction-Powered Causal Inferences (§5, p. 8). **C0306** Cadei et al. 2024, Smoke and Mirrors (pp. 2, 4). **C0332** Yao et al. 2025, ICLR (§5.1, p. 9). **C0320** Yao et al. 2025, NeurIPS (§5.2, p. 8) |
| PARTIAL, **images** | **S0209** Israel et al. 2023 (generative backdoor adjustment, X-ray confounder). **S0446** Rahman & Kocaoglu 2024 (conditional generative models, image / text). **C0424** Rahman & Kocaoglu 2024 (Modular-DCM). **C0460** Deshpande et al. 2022 (multi-modal generative SEM). **K2** Imai & Nakamura 2026b (text + images). **Klaassen** et al. 2024 (text + images) |
| PARTIAL, **text** | **K1**; **K3** (sequential); Veitch 2020; Pryzant 2021; Gui & Veitch 2023; Ahrens 2021; Roberts 2020; Lin 2024; Feldman 2026; Guo 2025; **S0460** Ma et al. 2025; **C0452** Chen, Bhattacharya & Keith 2024; **C0462** Dhawan et al. 2024 (NATURAL); **C0494** CausalNLP; **C0507** Sridhar & Getoor 2019 |
| PARTIAL, **EHR** | Targeted-BEHRT (N0712) and its applications C0262, C0265, C0276 |
| RELATED | about 70 works: representations trained from scratch or on tabular / network data, text as treatment, moderators, prediction-side debiasing, reviews (S1–S6) |

**L1 summary.**
* One DIRECT source, K4, in **non-medical** video.
* **No medical-video source reaches L1 DIRECT or PARTIAL.**
* The video PARTIALs (ant-behaviour RCTs) use foundation representations as **outcome models**, not adjustment
  covariates.

### L2. Representations carry instrument-like acquisition information (site, device, operator) that amplifies bias or degrades overlap

| grade | source | basis |
|---|---|---|
| RELATED, **borderline**: the closest L2 evidence in **medical video** | **S0008** Field-of-view confounding shapes genetic discovery from self-supervised cardiac-imaging phenotypes (medRxiv 2026) | A video masked-autoencoder on 69,932 cine-MRI studies encodes "imaging centre (linear-probe R2 = 0.55 for site)", causing "phenotype-level confounding" of GWAS (Abstract, p. 1). Two elements differ: (i) the representations are **outcomes (phenotypes)**, not adjustment covariates for an action's effect; (ii) site acts as a **confounder**, not an instrument |
| RELATED, **borderline**: the closest in **video** (non-medical) | **S0414** Cadei et al. 2025; **C0306** Cadei et al. 2024 | Recording-setup and background information (plate markings, lighting, nests) in fine-tuned foundation encoders biases the ATE and threatens positivity (S0414 Example 1, p. 5; C0306 p. 4). Two elements differ: an outcome model, not adjustment; a shortcut confounder, not an instrument |
| RELATED: the closest **statement** of Z-bias through learned summaries | **Roberts** et al. 2020 | "conditioning on Z would amplify bias from U" (p. 4); text, qualitative, no acquisition information |
| RELATED | K1–K4, Gui & Veitch, Feldman, Lin, Daoud; S0446 and C0424 (hospital as a **confounder**); site-leakage literature N0219, N0230, N0240 and others (S4); Jerzak 2023a (sensor resolution) | overlap lost through treatment information, or acquisition information analysed for **prediction** |

**L2 summary.**
* No DIRECT or PARTIAL.
* No source shows acquisition information, in a representation **used as an adjustment covariate**, acting **as an
  instrument** in causal estimation.

### L3. Semi-synthetic causal benchmark on real medical video, with acquisition information manipulated as an instrument

**No DIRECT or PARTIAL.**
* RELATED: K4 Mario (synthetic game video, confounder); ISTAnt (S0414, C0306: real ant video, RCT ground truth, no
  instrument).
* RELATED: semi-synthetic benchmarks on real static images or text (S0209 MedMNIST X-ray, S0446 Colored-MNIST,
  Klaassen, Targeted-BEHRT, Veitch, Pryzant and others). None is on real medical video, and none manipulates acquisition
  information as an instrument.
* UNRESOLVED: S0242 (§5).

### L4. Duration / persistence dependence of the role of acquisition information; acquisition-removed representations in sequential estimation

**No DIRECT or PARTIAL.**
* RELATED:
  * K3 and K4 (sequential deconfounders, no acquisition information);
  * Targeted-BEHRT (persistent vs transient **clinical** confounding);
  * S0008 (removal of acquisition information from representations, but static association);
  * S0299, S0335, S0361, S0373, S0340 (treatment-invariant representations over time, not acquisition-invariant);
  * the harmonization literature (S1).

## 3. Consequence under gate §6 (applied mechanically)

| gate condition | met? | consequence |
|---|---|---|
| L1 and L2 DIRECT in the same paper, in medical video | no (no L2 DIRECT anywhere) | NO-GO not triggered |
| L1 and L2 in the same paper, static medical images or non-medical video | no. Same-paper pairs: K4 (L1 DIRECT, L2 RELATED); S0414 and C0306 (L1 PARTIAL, L2 RELATED); combined grade RELATED | PARTIAL narrowing not triggered |
| L1 and L2 in different papers | L1 yes. L2: RELATED only | **GO; cite K4 for L1 and the L2-RELATED works** |
| L3 DIRECT | no | benchmark-novelty claim retained |
| L4 DIRECT / PARTIAL | no | duration headline retained; no narrowing |

**Robustness of the verdict to the borderline L2 calls.** The verdict would not change if the investigator re-graded
them as PARTIAL:
* **S0414 / C0306 as L2 PARTIAL.** Each paper would then have L1 PARTIAL and L2 PARTIAL in non-medical video. The
  consequence is "GO with the claim narrowed to sequential medical video", and the claim is already sequential
  medical video.
* **S0008 as L2 PARTIAL.** It has no L1 PARTIAL in the same paper, so the "different papers: GO; cite both" row
  applies.

**Required citations:**
* K4, as L1 DIRECT (non-medical video) and the video causal benchmark precedent;
* K1–K3;
* S0414, C0306, C0320, C0332, for foundation video representations in causal estimation and encoder or shortcut bias;
* S0008, for acquisition (site) information in a generative video representation of medical video;
* Roberts 2020 and K2 Supp. S2, for Z-bias and overlap through learned summaries;
* the site-leakage literature.

## 4. What the result does not establish

* Screening to RELATED or NONE used abstracts, by screening subagents under the fixed rubric. Every FULLTEXT record was
  decided by the lead analyst.
* The six UNRESOLVED works below were not read.

## 5. UNRESOLVED (full text not obtainable)

| uid | work | open on | reason |
|---|---|---|---|
| C0288 | OmniNet (Neural Comput Appl 2025, doi 10.1007/s00521-025-11202-9) | L1 (at most PARTIAL) | Springer bot challenge |
| S0058 | Semantic Embedding and Dynamic PSM-DID … Green Patent Quality (ACM 2025, doi 10.1145/3800227.3800305) | L1 (text; at most PARTIAL) | no abstract; ACM bot challenge |
| S0340 | TIDAL: Temporal Causal Diffusion … Knee Osteoarthritis (KDD 2026, doi 10.1145/3770855.3819025) | L1 (X-ray sequences; at most PARTIAL) | ACM bot challenge (listed gold OA) |
| S0373 | LLMCE (CIKM 2025, doi 10.1145/3746252.3760914) | L1 (time series; at most PARTIAL) | ACM bot challenge |
| S0242 | Synthetic Ground Truth Counterfactuals … Causal Generative Models in Medical Imaging (MICCAI 2025, doi 10.1007/978-3-032-04984-1_52) | L3 | no abstract; Springer bot challenge |
| C0377 | Tesei et al. 2023, J Biomed Inform 140:104339 | L1 (EHR; at most PARTIAL) | ScienceDirect bot challenge |

* **Investigator action, optional.** These six PDFs could be retrieved manually.
* **Why they cannot change the verdict.**
  * The five L1 items can reach at most L1 PARTIAL, and none is in medical video.
  * S0242 could change only the L3 benchmark-novelty claim, and only if it is a semi-synthetic benchmark on **real
    medical video** with acquisition information manipulated as an instrument. Its title says synthetic ground truth
    in medical imaging.
* The investigator's pathology foundation-model site audit (gate §6 known prior work) is still to be replaced by its
  preprint reference.
