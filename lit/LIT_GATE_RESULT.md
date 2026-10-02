# Literature Gate Result (gate `baadf5c` §6)

**Verdict:** **GO, conditional on two BLOCKED arms.** No source puts L1 and L2 together, and no source reaches L2,
L3 or L4 at DIRECT or PARTIAL. The benchmark-novelty claim (L3) and the duration headline (L4) are retained.
**Closest prior work to cite:**
* **K4**, Nakamura et al. 2026: L1 DIRECT, in non-medical video.
* For the L2 mechanism (RELATED):
  * Roberts et al. 2020;
  * K2 Supplement S2;
  * the site-leakage literature.

**Condition.** The Semantic Scholar arm and the proceedings arm (MICCAI, IPMI, MIDL, NeurIPS, ICML, CLeaR, UAI) could
not be run (HTTP 429), and one work is UNRESOLVED (§5). The verdict holds for the three databases searched plus one
level of citation chasing.

## 1. What was run

| arm | status | records |
|---|---|---|
| PubMed (Q1–Q4, boolean, relevance, first 100) | done | Q1 100 of 14,745 · Q2 28 · Q3 21 · Q4 100 of 459 |
| arXiv (cs.CV, cs.LG, stat.ME, stat.ML; 2018-01-01 to freeze) | done | Q1 14 · Q2 17 · Q3 24 · Q4 49 (all hits) |
| OpenAlex (boolean search, relevance, first 100) | done | 100 per query (of 12,657 / 24,890 / 9,729 / 92,427) |
| **Semantic Scholar** (split into 120 + 36 + 4 + 60 = 220 sub-queries) | **BLOCKED** | 0 of 220 sub-queries returned. The first sub-query got HTTP 429 continuously, 03:37–04:07 UTC, through backoffs of 120–900 s |
| **Proceedings: MICCAI, IPMI, MIDL, NeurIPS, ICML, CLeaR, UAI** (Semantic Scholar venue filter; 220 sub-queries) | **BLOCKED** | 0 of 220. A venue-name defect was found and fixed before any query ran (`SEARCH_IMPLEMENTATION.md` §9) |
| Citation chasing: one level backward and forward from every DIRECT / PARTIAL hit (K1–K4, N0712) via OpenAlex | done | 298 records |

* **Native search:** 753 hits, which deduplicate to **721 unique records**. Screening: 571 NONE, 133 RELATED,
  17 FULLTEXT.
* **Citation chasing:** 298 records. Screening: 138 NONE, 105 RELATED, 55 FULLTEXT. The 55 FULLTEXT records are 30
  distinct works.
* **Log.** Every screened record (1,019) is in `RECORDS.csv`, with database, query, rank, ids, title, year, venue,
  decision, reason and screener. Lead grades for FULLTEXT records are in the same file.
* **Full texts.** The lead analyst read in full all four known works (K1–K4) and 18 other works, and scanned the
  full text of 4 more. The quotes are in
  `FULLTEXT_NOTES.md`, sections K1–K4 and S1–S4.

## 2. Per-claim tables

### L1. Generative or foundation video representations used as adjustment covariates for the effect of an action or treatment

| source | grade | quote | location |
|---|---|---|---|
| **K4** Nakamura, Breuer, Crespin, Dietrich & Imai (2026), arXiv:2607.06126 | **DIRECT (non-medical video)** | "we first reproduce each video using a deep generative model and leverage the model's internal representations as learned, low-dimensional summaries of video content for causal estimation." | Abstract, p. 1; also §1 p. 3, §4.2 p. 21 |
| K1 Imai & Nakamura (2026a), JASA; arXiv:2410.00903 | PARTIAL (text) | "internal representations extracted from GenAI models can be leveraged within a causal machine learning framework to estimate the causal effects of interest." | §1, p. 2 |
| K2 Imai & Nakamura (2026b), PNAS; arXiv:2507.03897 | PARTIAL (text, images) | "Text as confounder: Estimating the causal effects of a treatment variable by adjusting for latent confounders embedded in textual data" | §1, p. 2 |
| K3 Nakamura & Imai (2026), arXiv:2605.07834 | PARTIAL (text; sequential) | "internal representations extracted from an open-source generative AI model can be leveraged to nonparametrically estimate a deconfounder … at each point in the sequence." | §1, p. 2 |
| Rao et al. (2022) Targeted-BEHRT, IEEE TNNLS (N0712) | PARTIAL (EHR) | "T-BEHRT first extracts latent EHR features … with BEHRT. Second, the model predicts propensity of exposure and conditional outcome using these grasped features" | §II.D, p. 4 |
| Veitch, Sridhar & Blei (2020), UAI | PARTIAL (text) | "We combine these two ideas to adapt modern methods for language modeling — BERT and topic models — in service of causal inference" | §1, p. 2 |
| Pryzant et al. (2021), NAACL | PARTIAL (text) | "We approximate this confounding information in the text … with a learned representation b(W) … We use DistilBERT … to produce a representation of the text" | §5.2, p. 4 |
| Gui & Veitch (2023), ICLR | PARTIAL (text) | "use supervised representation learning to produce a data representation that preserves confounding information while eliminating information that is only predictive of the treatment. This representation then suffices for adjustment" | Abstract, p. 1; §4.2, p. 6 |
| Ahrens et al. (2021), EMNLP | PARTIAL (text; generative topic model) | "a supervised text representation Zi = g(Wi, yi, ti, Ci), which … together with Ci blocks all 'backdoor path' between yi and ti" | §2.1, p. 2 |
| Roberts, Stewart & Nielsen (2020), AJPS | PARTIAL (text; generative topic model) | "estimate a low-dimensional summary of the text and condition on this summary via matching"; "TIRM uses a structural topic model … as the measurement model" | Abstract, p. 1; p. 5 |
| Klaassen et al. (2024), arXiv:2402.01785 | PARTIAL (text, images) | "We use pre-trained transformer-based models such as BERT … For the image processing, we rely on transformer-based models such as BEIT … or Vision Transformers" | §4, p. 4 |
| Lin, Morency & Ben-Michael (2024/25), ICML | PARTIAL (text) | "Sentence embeddings from transformer-based language models" for the non-focal language adjusted for | §4.2, p. 6 |
| Feldman et al. (2026), arXiv:2602.15730 | PARTIAL (text) | "we control for such unwanted variations by adjusting for dense contextual embeddings using robust causal machine learning" | §1, p. 2 |
| Guo et al. (2025), IJCNLP-AACL | PARTIAL (text) | "(1) a BERT encoder for textual representation, (2) an outcome predictor … (3) a domain predictor … ensuring domain-invariant embeddings" | §3, p. 5 |
| Rao et al. (2023) Hypertension; Heart; Eur Heart J (T-BEHRT applications) | PARTIAL (EHR) | e.g. "the patient representation vector is used as input to jointly learn the propensity score … and the outcome of interest" | EHJ, Methods: Statistical methods (PMC10635668) |
| RELATED (23 works) | RELATED | not adjustment with generative / foundation representations (TF-IDF, task-specific CNNs, text as treatment, moderators, reviews), e.g. Daoud 2022, Mozer 2020 / 2024, Jerzak 2023a / b, Egami 2022, N0105, N0217, N0235, N0587, N0596 | S1, S3 |

**L1 summary.**
* **DIRECT:** one source, K4, in non-medical video.
* **No medical-video source reaches L1 DIRECT or PARTIAL.**
* All 16 PARTIAL sources differ in modality (text, images or EHR) instead of video.

### L2. Representations carry instrument-like acquisition information (site, device, operator) that amplifies bias or degrades overlap

| source | grade | quote | location |
|---|---|---|---|
| Roberts, Stewart & Nielsen (2020) | **RELATED: closest statement of the mechanism.** Text, generic content, qualitative, no acquisition information | "if the text is an instrument, meaning it explains the outcome only through the treatment, conditioning on the text can amplify the bias of unconditioned confounders (Pearl 2011)"; "conditioning on Z would amplify bias from U" | p. 3; p. 4 |
| K2 Imai & Nakamura (2026b) | RELATED. Treatment-predictive content, not acquisition information | "adding a prediction head for the treatment assignment encourages the deconfounder to capture nearly all the information predictive of treatment, thereby exacerbating the violation of overlap assumption." | Supp. S2.1.3, p. 20 |
| K1, K3, K4 | RELATED. Overlap lost through the treatment feature or treatment persistence | e.g. K4: "a characteristic that typically exhibits strong temporal persistence … thereby violating the positivity assumption" | K1 §3.2 p. 9; K3 §1 p. 3; K4 §3.3 p. 12 |
| Gui & Veitch (2023); Feldman et al. (2026); Lin et al. (2024); Daoud et al. (2022) | RELATED. The treatment attribute encoded in text breaks overlap | Feldman: "Using such embeddings as controls will … lead to a positivity violation" | Gui §1 p. 2; Feldman §1 p. 2; Lin §3.3 p. 5; Daoud §2.1.1 p. 3 |
| Jerzak et al. (2023a) | RELATED. Sensor resolution under-captures confounders (residual bias), not an instrument | "resolution is a key driver of the residual confounding" | §3.5, p. 10 |
| Site / scanner leakage in learned or foundation features, e.g. N0219 (TCGA site prediction), N0230 (acquisition confounding of frozen CT FM features), N0240 (scanner variability in 14 pathology FMs), N0241, N0244, N0246, N0253, N0268, N0314, N0651 | RELATED. Static images or EEG; **prediction** shortcuts, not causal-estimation bias or overlap (S4) | N0230: "acquisition-related confounding … is not evidence of malignancy discrimination" | abstracts (S4) |
| Investigator's pathology foundation-model site audit (gate §6 known prior work) | not graded: no preprint yet. The gate records it as "related to L2 for static images" | — | to be replaced by its preprint reference |

**L2 summary.** No DIRECT or PARTIAL. No source shows **acquisition information** in a representation **used as an
adjustment covariate** acting **as an instrument** in causal estimation.

### L3. Semi-synthetic causal benchmark on real medical video, with acquisition information manipulated as an instrument

| source | grade | quote | location |
|---|---|---|---|
| K4 (Mario benchmark) | RELATED. Synthetic game video; confounder, not instrument | "we construct a novel video causal benchmark dataset with known ground truth"; "Pipe obstacles serve as confounding features" | §4 p. 19; §4.1 p. 20 |
| Targeted-BEHRT (N0712) | RELATED. Semi-synthetic, on real EHR | "we first construct semi-synthetic derivations of our observational dataset" | §I, p. 2 |
| N0386 DR-ME (OCTMNIST semi-synthetic) | RELATED. Real images, outcome side only | "OCTMNIST images only on the outcome side … confounding is driven by the synthetic covariates" | App. I.7 |
| N0378 neuroimaging simulation framework; N0367 lesion-symptom mapping; N0105 D'ARTAGNAN (counterfactual echo video) | RELATED. Synthetic MRI / XAI validation / video generation without effect estimation | — | S1 |
| Semi-synthetic text / image benchmarks: Veitch 2020, Pryzant 2021, Gui & Veitch 2023, Ahrens 2021, Roberts 2020, Klaassen 2024, Lin 2024, Feldman 2026, Guo 2025, Jerzak 2023a / b | RELATED. Real text or images, not medical video; no instrument manipulated | e.g. Klaassen: semi-synthetic from "the IMDB dataset" and "the CIFAR-10 dataset" | §5.1, p. 5 |

**L3 summary.** No DIRECT or PARTIAL. No benchmark on **real medical video**, and none **manipulates acquisition
information as an instrument**.

### L4. Duration / persistence dependence of the role of acquisition information; acquisition-removed representations in sequential estimation

| source | grade | quote | location |
|---|---|---|---|
| K3; K4 | RELATED. Sequential estimators with representation deconfounders; no acquisition information, no role switch | — | K3 §3.3–3.5; K4 §3.3–3.6 |
| Targeted-BEHRT (N0712) | RELATED. Persistent vs transient **clinical** confounding | "We define persisting confounding as confounders that are assigned at birth and persist through one's life course" | §II.B, p. 3 |
| Guo et al. (2025) | RELATED. Domain-invariant (adversarial) embeddings, but invariant to the LLM-intervened text domain; static | "ensuring domain-invariant embeddings" | §3, p. 5 |
| N0311 flow-based harmonization; N0570 ComBat PET; N0235 rsfMRI FM; N0587 causal state-space; N0596 DRTCI | RELATED. Harmonization for prediction, or balancing (treatment-invariant) representations over time | — | S1 |

**L4 summary.** No DIRECT or PARTIAL. No source analyses how the **causal role** of acquisition information in
representations **depends on intervention duration or persistence**. No source tests **site-invariant or harmonized
representations in sequential causal estimation**.

## 3. Consequence under gate §6 (applied mechanically)

| gate condition | met? | consequence |
|---|---|---|
| L1 and L2 DIRECT in the same paper, in medical video | no (no L2 DIRECT anywhere) | NO-GO not triggered |
| L1 and L2 in the same paper, static medical images or non-medical video | no. K4 has L1 DIRECT but L2 only RELATED; the combined grade is RELATED | PARTIAL narrowing not triggered |
| L1 and L2 in different papers | L1 yes (K4 DIRECT, plus PARTIALs). L2: RELATED only | **GO; cite K4 for L1, and the L2-RELATED works as nearest mechanism** |
| L3 DIRECT | no | benchmark-novelty claim retained |
| L4 DIRECT | no | duration-dependence headline retained |
| L4 PARTIAL | no | no narrowing |

**Literature-gate verdict: GO.**
* The headline, the benchmark-novelty claim and the duration claim are all retained.
* **Required citations:**
  * K4, as L1 DIRECT in non-medical video and the precedent for a video causal benchmark;
  * K1–K3;
  * Roberts et al. 2020 and K2 Supp. S2, for Z-bias and overlap through learned summaries;
  * the site-leakage literature (N0219, N0230, N0240), for acquisition information in foundation features.
* **Condition:** the BLOCKED arms and the one UNRESOLVED work below.

## 4. What the result does not establish

* It covers PubMed, arXiv (four categories), OpenAlex and one citation level. **Semantic Scholar and the seven
  proceedings were not searched.** MICCAI 2024–2026 and MIDL papers indexed only there could change L2 or L3.
* Screening to RELATED or NONE used abstracts, by screening subagents under a fixed rubric. Every FULLTEXT record was
  decided by the lead analyst. The L2 RELATED decisions were re-checked by the lead analyst (S4).

## 5. UNRESOLVED and investigator actions

| item | what is open | needed |
|---|---|---|
| **Semantic Scholar arm** (220 sub-queries) | all of L1–L4 for records indexed only there | a Semantic Scholar API key; then re-run `lit/search_s2.py` (resumable, cached) |
| **Proceedings arm**: MICCAI, IPMI, MIDL, NeurIPS, ICML, CLeaR, UAI (220 sub-queries) | as above, the venue-restricted ranking | the same key (it runs after the Semantic Scholar arm in the same script) |
| C0288: OmniNet (Neural Comput Appl 2025, doi 10.1007/s00521-025-11202-9) | L1 only (PARTIAL possible). L2–L4 NONE from the abstract | full text: the Springer OA PDF returns a bot challenge. A manual download by the investigator is needed |
| Investigator's pathology FM site audit | its L2 grade | the preprint reference, when available |

**Earlier list corrected.** C0262, C0265 and C0276 had been listed as unreadable. They were read in full from PMC
and graded L1 PARTIAL (EHR); they are not UNRESOLVED.
