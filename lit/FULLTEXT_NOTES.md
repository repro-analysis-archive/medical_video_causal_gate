# Full-Text Readings (lead analyst)

Grades follow `SEARCH_IMPLEMENTATION.md` §8. Locations are pages of the arXiv PDF as printed, with sections. The full
text of each source was read before any DIRECT or PARTIAL grade.

## K1. Imai & Nakamura (2026a). Causal inference with generative artificial intelligence: Application to texts as treatments. JASA (forthcoming); arXiv:2410.00903v5

* PDF sha256 `e4cf4206…`, 38 pp. Read in full: main text pp. 1–19, plus Supplementary Appendix S1–S6.
* **What it does.** It estimates the ATE of a treatment feature of an LLM-generated text (Llama 3). The deconfounder
  f(R) is learned from the LLM's internal representation R of the same text, and DML is applied. The application is a
  political-science candidate-profile survey experiment, with a further Hong Kong experiment in Appendix S6.

| claim | grade | supporting passage (location) |
|---|---|---|
| L1 | **PARTIAL**. Generative representations are used for confounding adjustment of a treatment effect, but for **text**, not video. The paper states video is out of reach of its method | "We show that internal representations extracted from GenAI models can be leveraged within a causal machine learning framework to estimate the causal effects of interest." (§1, p. 2). "For videos, both treatment and confounding features are likely to exhibit complex relationships due to the combination of audio and images with the additional temporal dimension. Thus, the GPI methodology described here is not readily applicable." (§6, p. 19) |
| L2 | **RELATED**. Overlap loss is analysed only as the representation encoding the **treatment feature**. No acquisition information (site, device, operator) appears | "one cannot directly adjust for the internal representation of the treatment object. Such direct adjustment leads to the lack of overlap because … the treatment feature Ti is a deterministic function of Ri." (§3.2, p. 9) |
| L3 | **NONE**. The simulation uses LLM-generated political biographies, not medical images or video | §4.1, p. 13 |
| L4 | **NONE**. There is no duration, persistence, sequential estimation or debiased-representation analysis. The IV in Appendix S3 instruments a perceived treatment, not acquisition information | Appendix S3, pp. 27–35 |

## K2. Imai & Nakamura (2026b). Leveraging generative AI for causal inference with unstructured data. PNAS 123(36): e2530532123; arXiv:2507.03897v4

* PDF sha256 `f1a7d059…`, 40 pp. Read in full: main text pp. 1–13, plus Supplementary S1–S5.
* **What it does.** GPI uses GenAI internal representations (LLaMA3 / Gemma3, Stable Diffusion) to estimate a
  deconfounder. The three applications are text as confounder (Weibo censorship), image as treatment (protest
  images) and a structural model of text. The supplement adds a simulation of overlap failure.

| claim | grade | supporting passage (location) |
|---|---|---|
| L1 | **PARTIAL**. GenAI representations are used as **adjustment covariates** for the effect of an external treatment (prior censorship), for **text and images, not video**. Video is deferred to the companion papers | "Text as confounder: Estimating the causal effects of a treatment variable by adjusting for latent confounders embedded in textual data" (§1, p. 2). "although we focused on text and image data, the GPI framework can be naturally extended to other types of unstructured data, including audio and video (Nakamura et al., 2026; Nakamura and Imai, 2026)." (§5, p. 10) |
| L2 | **RELATED**, the closest mechanism-level prior work. Treatment-only-predictive information in a representation is shown to degrade overlap and bias estimates. That information is generic content, **not acquisition information**, and the modality is text / images | "adding a prediction head for the treatment assignment encourages the deconfounder to capture nearly all the information predictive of treatment, thereby exacerbating the violation of overlap assumption." (Supp. S2.1.3, p. 20). Simulation: "the direct adjustment of Ri leads to the overlap violation" (Supp. S1.1, p. 14); Table S1 (p. 16) shows bias for DragonNet / AIPW-DML on the full representation |
| L3 | **NONE**. The simulation uses Gaussian synthetic representations, not real medical images or video | Supp. S1.1, p. 14 |
| L4 | **NONE**. There is no duration / persistence or sequential analysis, and no debiased or harmonized representations | — |

## K3. Nakamura & Imai (2026). GenAI Powered Dynamic Causal Inference with Unstructured Data. arXiv:2605.07834v2

* PDF sha256 `c4f55af4…`, 48 pp. Read in full: main text pp. 1–24, Appendix S1 proofs, and S2.
* **What it does.** Dynamic GPI estimates the effect of a **sequence of treatment features** within one unstructured
  object, using GenAI internal representations as sequential deconfounders. It works under an incremental
  propensity-score intervention defined on treatment history only. The single application is text: Hong Kong
  vignettes, with sentence position as time.

| claim | grade | supporting passage (location) |
|---|---|---|
| L1 | **PARTIAL**. GenAI representations are used as **sequential** adjustment covariates (deconfounders) for a sequence of treatment features. The demonstration is **text**; video is asserted but not done | "We show that internal representations extracted from an open-source generative AI model can be leveraged to nonparametrically estimate a deconfounder, which is a low-dimensional summary of confounding information at each point in the sequence." (§1, p. 2). "While the application in this paper has focused on causal inference with texts, the proposed methodology can be extended to other modalities such as video." (§6, p. 21) |
| L2 | **RELATED**. Positivity failure is attributed to prior **treatment** sequences nearly determining later treatments, and stochastic interventions are the remedy. No acquisition information | "the primary challenge in our setting is the failure of positivity, as prior sequences may nearly determine subsequent treatment assignments. We address this issue by adopting a stochastic intervention framework" (§1, p. 3) |
| L3 | **NONE**. The simulation uses synthetic Gaussian representations; there are no medical images or video | §4.1, pp. 16–17 |
| L4 | **RELATED**. A sequential causal estimator with representation-based deconfounders, but no acquisition information, no instrument-vs-confounder role, and no debiased representations | §3.3–3.5, pp. 8–15 |

## K4. Nakamura, Breuer, Crespin, Dietrich & Imai (2026). Causal Inference with Video Features as Treatments. arXiv:2607.06126v2

* PDF sha256 `8ac1d6e6…`, 37 pp. Read in full: main text pp. 1–26, plus Appendix S1–S3.
* **What it does.** Each video is reproduced with a generative video model (the NVIDIA Cosmos tokenizer), and its
  internal representations are used as sequential deconfounders. The estimand is the effect of a time-varying
  **video treatment feature** (candidate appearance; Princess Peach) on real-time outcomes, under a dynamic
  incremental intervention defined on treatment history.
* **Data.** A synthetic Super Mario benchmark with known null effect, and 849 political TV ads with respondent dial
  ratings. **No medical data.**

| claim | grade | supporting passage (location) |
|---|---|---|
| L1 | **DIRECT (non-medical video)**. Generative **video** representations are used as **adjustment covariates** (a deconfounder) for the causal effect of a **treatment** | "we first reproduce each video using a deep generative model and leverage the model's internal representations as learned, low-dimensional summaries of video content for causal estimation." (Abstract, p. 1). "We show that these confounding factors can be recovered from the internal representations of a GenAI model. Adjusting for the resulting deconfounder … enables identification of the entire counterfactual trajectory of real-time responses." (§1, p. 3). "we first regenerate the video content using the NVIDIA Cosmos tokenizer … and extract their internal representations." (§4.2, p. 21) |
| L2 | **RELATED**. Overlap is discussed only through **temporal persistence of the treatment feature**, and the remedy is a stochastic intervention. **No acquisition information** (site, device, operator, camera) is analysed | "the treatment feature indicates whether a candidate appears on screen, a characteristic that typically exhibits strong temporal persistence across adjacent segments … a deterministic intervention … would induce a highly implausible treatment sequence … thereby violating the positivity assumption" (§3.3, p. 12) |
| L3 | **RELATED**. A video causal benchmark with known ground truth, but **synthetic game video, not real medical video**, and nothing is manipulated as an instrument (the pipes are a confounder) | "we construct a novel video causal benchmark dataset with known ground truth" (§4, p. 19). "Pipe obstacles serve as confounding features, with their appearances intentionally correlated with those of Princess Peach." (§4.1, p. 20) |
| L4 | **RELATED**. A sequential estimator with video-representation deconfounders, but no acquisition information, no instrument-vs-confounder role, and no duration analysis of that role | §3.3–3.6, pp. 12–19 |

**Note.** K4 is the closest prior work for L1. It also gives a precedent for a known-truth video benchmark (L3 RELATED).

## S1. Lead decisions on the 17 screening FULLTEXT candidates (native search)

**Rule.** A full text was read wherever DIRECT or PARTIAL was possible. Where the abstract, or a scan of the text,
settles RELATED or NONE, that grade is recorded (gate §6: "Screening to RELATED or NONE may use abstracts").

| uid | source | L1 | L2 | L3 | L4 | basis |
|---|---|---|---|---|---|---|
| N0105 | D'ARTAGNAN: Counterfactual Video Generation (MICCAI 2022) | RELATED | NONE | RELATED | NONE | abstract: counterfactual echo-video generation for EF; no treatment-effect estimation with representations as adjustment |
| N0217 | Confounder-aware foundation modeling … cell imaging (npj Imaging 2025) | RELATED | RELATED | NONE | NONE | full-text scan (PMC12546604): an SCM-conditioned latent diffusion model generates batch-balanced synthetic Cell Painting images, evaluated by MoA / target **prediction**. No adjustment-based causal estimate, and no bias or overlap analysis of acquisition information |
| N0235 | rsfMRI foundation models … cognitive aging interventions (bioRxiv 2026) | RELATED | RELATED | NONE | RELATED | full-text scan (PMC13105019): predicts individual intervention response in two RCTs. "Robustness to confounders (site, head motion, arm)" means **classification accuracy**, not causal-estimation bias |
| N0305 | Gui & Toubia, LLMs to Simulate Human Behavior (SSRN 2023) | RELATED | NONE | NONE | NONE | abstract (Crossref): confounding in LLM-simulated experiments; no representation adjustment |
| N0309 | Deep Feature IV regression (DFIV, 2020) | RELATED | NONE | NONE | NONE | abstract: learned features in IV regression; not adjustment covariates; no acquisition information |
| N0311 | Harmonization with Flow-Based Causal Inference (MICCAI 2021) | NONE | RELATED | NONE | RELATED | abstract (PubMed): counterfactual site harmonization of MRI for **prediction** generalization; no treatment-effect estimation |
| N0337 | Deep Causal Learning survey (ACM CSUR 2025) | RELATED | NONE | NONE | NONE | abstract: survey |
| N0367 | Individualized lesion-symptom mapping (NeuroImage Clin 2025) | NONE | NONE | RELATED | NONE | abstract: simulated scores on real lesion maps for XAI validation; not a causal benchmark; no acquisition instrument |
| N0378 | Neuroimaging Simulation Framework for Causal AI (arXiv 2606.28684) | NONE | NONE | RELATED | NONE | full-text scan: **synthetic** template-deformed MRI with a causal structure for causal-discovery evaluation; not real medical video; no acquisition instrument |
| N0386 | DR-ME distributional treatment-effect test (arXiv 2605.08034) | NONE | NONE | RELATED | NONE | full-text scan: in the OCTMNIST semi-synthetic study, "OCTMNIST images only on the outcome side … confounding is driven by the synthetic covariates" (App. I.7) |
| N0445 | MICCAI 2021 proceedings volume (LNCS 12903) | NONE | NONE | NONE | NONE | a whole volume, not a single source |
| N0570 | ComBat harmonization … amyloid PET (HBM 2024) | NONE | RELATED | NONE | RELATED | abstract: ComBat on regional SUVR (not learned representations) across tracers; trial-power simulation |
| N0587 | Causal State-Space Model, longitudinal ITE (arXiv 2608.08288) | RELATED | NONE | NONE | RELATED | abstract: treatment-invariant (not acquisition-invariant) representations |
| N0596 | DRTCI disentangled temporal causal inference (arXiv 2201.08137) | RELATED | NONE | NONE | RELATED | abstract: disentangled balancing of patient-history representations; no acquisition information |
| N0639 | Causal ML for predicting treatment outcomes (Nat Med 2024) | RELATED | NONE | NONE | NONE | perspective / review |
| N0642 | Causal ML for healthcare and precision medicine (RSOS 2022) | RELATED | NONE | NONE | NONE | abstract: review |
| N0712 | Targeted-BEHRT (IEEE TNNLS 2022; arXiv 2202.03487) | **PARTIAL** | NONE | RELATED | RELATED | **full text read**: see S2 |

## S2. Rao et al. (2022). Targeted-BEHRT: Deep learning for observational causal inference on longitudinal electronic health records. IEEE TNNLS; arXiv:2202.03487

* Read in full (10 pp. + supplement).
* **What it does.** A transformer (BEHRT) pre-trained with masked-EHR modelling extracts representations of
  longitudinal EHR. These feed propensity and outcome heads, with CV-TMLE, to estimate the risk ratio of an
  antihypertensive class on cancer, in semi-synthetic CPRD data and in real CPRD data.

| claim | grade | supporting passage (location) |
|---|---|---|
| L1 | **PARTIAL**. Pre-trained (foundation-style) representations are used as **adjustment covariates** for the causal effect of a **treatment**. The modality is **EHR, not video** | "T-BEHRT first extracts latent EHR features from static covariates and fixed sub-sequences of medical history with BEHRT. Second, the model predicts propensity of exposure and conditional outcome using these grasped features similar to the Dragonnet model." (§II.D, p. 4). "we pre-trained contextualised EHR embeddings and network weights through MEM on the pretraining dataset" (§II.E, p. 5) |
| L2 | **NONE**. No acquisition information | — |
| L3 | **RELATED**. A semi-synthetic causal benchmark on real EHR, not on medical video, with no acquisition instrument | "we first construct semi-synthetic derivations of our observational dataset" (§I, p. 2) |
| L4 | **RELATED**. It distinguishes **persistent vs transient confounding** in the semi-synthetic design. This concerns clinical confounders, not acquisition information in representations, and not intervention duration | "We define persisting confounding as confounders that are assigned at birth and persist through one's life course … transient confounding as confounders that manifest at a point or period of one's life" (§II.B, p. 3) |

## S3. Citation chasing: one level backward and forward from every DIRECT / PARTIAL hit (K1–K4, N0712)

* **Screening.** 298 citation records were screened: 138 NONE, 105 RELATED, 55 FULLTEXT
  (`screening/citation_batch_decisions.json`).
* **The 55 FULLTEXT records are 30 distinct works.**
  * Ten records are K1–K4 themselves, already graded above:
    * K1: C0087, C0128, C0171;
    * K2: C0022, C0129, C0172, C0297;
    * K3: C0106, C0188;
    * K4: C0105.
  * The other 26 works are graded below.
* **Reading.** Where DIRECT or PARTIAL was possible, the lead analyst read the full text: abstract, introduction,
  method, experiments and discussion. The whole text was also searched for site, scanner, device, camera, sensor,
  acquisition, batch, instrument, overlap, positivity, video, sequential, longitudinal, time-varying, harmoniz-,
  invarian- and debias-. Pages are PDF pages.
* **Grade convention.** For L1, a pretrained language model (BERT, DistilBERT, RoBERTa, ClinicalBERT, LLM) counts as
  a foundation representation, and a topic model as a generative representation. With text, images or EHR in place
  of video, exactly one element differs, so the grade is PARTIAL. A representation that is neither (TF-IDF, a small task-specific
  CNN) differs in a second element, so the grade is RELATED.

### S3.1 Full text read

| work (records) | L1 | L2 | L3 | L4 | supporting passage (location) |
|---|---|---|---|---|---|
| Veitch, Sridhar & Blei (2020). Adapting Text Embeddings for Causal Inference. UAI; arXiv:1905.12741 (C0059, C0116, C0147) | **PARTIAL** (text) | RELATED | RELATED | NONE | L1: "We combine these two ideas to adapt modern methods for language modeling — BERT and topic models — in service of causal inference" (§1, p. 2). L2: overlap is only the standard assumption, and treatment-only information is discarded by supervision: "causal adjustment requires only the aspects of text that are predictive of both the treatment and outcome" (Abstract, p. 1). No acquisition information. L3: semi-synthetic outcomes simulated on real PeerRead / Reddit text (p. 6); not medical video, no instrument |
| Pryzant, Card, Jurafsky, Veitch & Sridhar (2021). Causal Effects of Linguistic Properties. NAACL; arXiv:2010.12919 (C0048, C0108, C0139, C0193) | **PARTIAL** (text) | NONE | RELATED | NONE | L1: "We approximate this confounding information in the text … with a learned representation b(W) … We use DistilBERT … to produce a representation of the text" (§5.2, p. 4). L2: the focus is treatment mismeasurement; no acquisition information. L3: partially simulated Amazon reviews (§6.1, p. 5); not medical video, no instrument |
| Gui & Veitch (2023). Causal Estimation for Text Data with (Apparent) Overlap Violations. ICLR; arXiv:2210.00079 (C0019, C0085, C0125, C0169) | **PARTIAL** (text) | RELATED | RELATED | NONE | L1: "the idea is to use supervised representation learning to produce a data representation that preserves confounding information while eliminating information that is only predictive of the treatment. This representation then suffices for adjustment and satisfies overlap." (Abstract, p. 1); "we train DistilBERT … modified to include three heads" (§4.2, p. 6). L2: overlap fails because the representation encodes the **treatment attribute itself** ("Since the treatment is a linguistic property determined by the text, the probability of treatment given any text is either 0 or 1", §1, p. 2); not acquisition information. L3: semi-synthetic Amazon reviews with a real confounder (§5.1, p. 8); not medical video, no instrument |
| Ahrens, Ashwin, Calliess & Nguyen (2021). Bayesian Topic Regression for Causal Inference. EMNLP; arXiv:2109.05317 (C0000, C0066) | **PARTIAL** (text; generative topic model) | NONE | RELATED | NONE | L1: "we assume that our models can learn a supervised text representation Zi = g(Wi, yi, ti, Ci), which in our case, together with Ci blocks all 'backdoor path' between yi and ti" (§2.1, p. 2); "Its generative process builds on LDA-based models" (§2.3, p. 3). L3: semi-synthetic Booking.com / Yelp review data (§6, p. 7); not medical video, no instrument. L2: no overlap or acquisition analysis |
| Roberts, Stewart & Nielsen (2020). Adjusting for Confounding with Text Matching. AJPS 64(4); author PDF (C0051, C0111, C0197) | **PARTIAL** (text; generative topic model) | **RELATED: the closest statement of the L2 mechanism** | RELATED | NONE | L1: "Our proposed solution is to estimate a low-dimensional summary of the text and condition on this summary via matching" (Abstract, p. 1); "TIRM uses a structural topic model (STM …) as the measurement model to jointly estimate the topics (the low-dimensional representation) and a projection of information about treatment" (p. 5). L2: "if the text is an instrument, meaning it explains the outcome only through the treatment, conditioning on the text can amplify the bias of unconditioned confounders (Pearl 2011)" (p. 3); "Conditioning on V reduces bias, but conditioning on Z would amplify bias from U. If the text contains some combination of V and Z that cannot be separated, we want to condition on the text only if the confounding (V) was large relative to the instrument (Z)." (p. 4). This is a **qualitative remark** about **generic text content**, in **text, not video**, with **no acquisition information** and no analysis, so two elements differ and the grade is RELATED. It must be cited as prior statement of Z-bias through a learned text summary. L3: "we base our simulation off of the real text of articles in the IR literature, but simulate treatment effects and confounding" (p. 9); not medical video, no instrument manipulated |
| Daoud, Jerzak & Johansson (2022). Conceptualizing Treatment Leakage in Text-based Causal Inference. NAACL; arXiv:2205.00465 (C0008, C0076) | RELATED | RELATED | NONE | NONE | L1: the propensity uses "an L2-normalized TF-IDF vector using the 256 most frequent terms" (App. C.2, p. 8), not a generative or foundation representation. L2: treatment leakage into the adjustment text breaks overlap ("This lack of overlap would violate the identification assumptions…", §2.1.1, p. 3; "Without distillation (red), the estimated propensities cluster near 0 and 1", §5, p. 4); this is treatment information, not acquisition information. L3: the documents are GPT-2-generated, not real medical video |
| Mozer, Miratrix, Kaufman & Anastasopoulos (2020). Matching with Text Data. Political Analysis 28(4); arXiv:1801.00644 (C0043, C0104, C0187) | RELATED | NONE | NONE | NONE | L1: compares over 100 text representations × distance metrics for matching, including STM and "a Word2Vec representation" (§3, p. 12). The selected method and the MIMIC TTE application use TF-IDF / cosine matching (§5, p. 30). The core is match-quality evaluation, not adjustment with a generative or foundation representation |
| Mozer, Kaufman, Celi & Miratrix (2024). Leveraging text data for causal inference using electronic health records. arXiv:2307.03687 (C0042) | RELATED | NONE | NONE | NONE | Confounding adjustment uses "optimal full matching using the cosine distance calculated over the DTM" (§5.1, p. 17). ClinicalBERT embeddings were explored but not used for adjustment: "we found that BoW representation to be better suited the task at hand" (§3.3, p. 9). They appear only in the heterogeneity analysis (§6.1, p. 23). Borderline toward L1 PARTIAL (medical text); the gate consequence is the same |
| Klaassen et al. (2024). DoubleMLDeep: Estimation of Causal Effects with Multimodal Data. arXiv:2402.01785 (C0034, C0091) | **PARTIAL** (text + images) | NONE | RELATED | NONE | L1: "We use pre-trained transformer-based models such as BERT … RoBERTa … or LLMs … For the image processing, we rely on transformer-based models such as BEIT … or Vision Transformers" as nuisance learners for confounding by text and images in the PLR model (§4, p. 4). L3: a semi-synthetic benchmark from DIAMONDS / IMDB / CIFAR-10 (§5.1, p. 5); not medical video, no instrument |
| Jerzak, Johansson & Daoud (2023a). Integrating Earth Observation Data into Causal Inference. arXiv:2301.12985 (C0025) | RELATED | RELATED | RELATED | NONE | L1: satellite images are adjusted for through small task-specific convolutional models: a single-layer convolutional model in the simulation (§4.1, p. 12), and three convolutional layers of 32 filters in the application (p. 14). These are images, and not generative / foundation representations. L2: **sensor resolution** limits which confounders are captured: "resolution is a key driver of the residual confounding … Smaller confounder objects, therefore, introduce residual bias" (§3.5, p. 10). That is acquisition **under-capturing confounders**, not acquisition information acting as an instrument. Overlap is discussed for raw images vs latent representations (§3.4, p. 9). L3: confounding simulated from real Landsat images (§4.1, p. 11); not medical video, no instrument |
| Jerzak, Johansson & Daoud (2023b). Image-based Treatment Effect Heterogeneity. CLeaR; arXiv:2206.06417 (C0026, C0173) | RELATED | NONE | RELATED | NONE | RCT CATE by satellite image: "In the RCT setting, Mi is not a confounder, since the treatment was randomized" (§2, p. 4). Images are moderators, not adjustment covariates. L3: simulation on real satellite images; not medical video, no instrument |
| Lin, Morency & Ben-Michael (2024). Isolated Causal Effects of Natural Language. ICML 2025; arXiv:2410.14812 (C0039, C0135) | **PARTIAL** (text) | RELATED | RELATED | NONE | L1: non-focal language is approximated by "Sentence embeddings from transformer-based language models" (§4.2, p. 6) and adjusted for in the isolated-effect estimator. L2: a fidelity–overlap trade-off for dense representations: "representations with good fidelity are also more prone to overlap violations" (§3.3, p. 5). This concerns treatment-attribute information, not acquisition information. L3: semi-synthetic Amazon outcome (§4.1, p. 5) |
| Feldman, Venugopal, Spiess & Feder (2026). Causal Effect Estimation with Latent Textual Treatments. arXiv:2602.15730 (C0123) | **PARTIAL** (text) | RELATED | RELATED | NONE | L1: "we control for such unwanted variations by adjusting for dense contextual embeddings using robust causal machine learning" (§1, p. 2). L2: "Using such embeddings as controls will … lead to a positivity violation … controlling for more sophisticated text embeddings destroys variation in treatment" (§1, p. 2; §7.2, p. 6); the remedy is residualizing the treatment concept out of the embeddings. Treatment information, not acquisition information. L3: semi-synthetic text simulations (§1, p. 2) |
| Guo, Marmarelis, Morstatter & Lerman (2025). Estimating Causal Effects of Text Interventions Leveraging LLMs. IJCNLP-AACL; arXiv:2410.21474 (C0126) | **PARTIAL** (text) | RELATED | RELATED | RELATED | L1: CausalDANN uses "(1) a BERT encoder for textual representation, (2) an outcome predictor … and (3) a domain predictor … trained adversarially … ensuring domain-invariant embeddings" (§3, p. 5), and adjusts by outcome regression on the representation. L2 / L4: the invariance is to the **LLM-intervened vs original text domain**, not to acquisition information; the setting is static. L3: semi-synthetic Amazon reviews (§4, p. 6) |
| Rao et al. (2023). Systolic Blood Pressure and Cardiovascular Risk in Patients With Diabetes. Hypertension 80(3); PMC9944753 (C0262) | **PARTIAL** (EHR; inherits T-BEHRT) | NONE | NONE | NONE | "we used Targeted Bidirectional Electronic Health Records Transformer (T-BEHRT) for risk ratio (RR) estimation … T-BEHRT was first trained to jointly predict exposure category (propensity score) and risk of outcome" (Methods, Statistical and Deep Learning Analyses). Pretraining is not restated in this paper; the method is T-BEHRT (S2). An application with no acquisition, benchmark or sequential analysis |
| Rao et al. (2023). Systolic blood pressure, chronic obstructive pulmonary disease and cardiovascular risk. Heart 109(16); PMC10423512 (C0265) | **PARTIAL** (EHR; inherits T-BEHRT) | NONE | NONE | NONE | "The model incorporates EHR records, specifically diagnoses and medications—longitudinal in nature … and adjusts for confounding features in the medical history of the patient" (Methods, Statistical and deep learning analyses). An application, as above |
| Rao et al. (2023). Sodium-based paracetamol: impact on blood pressure, cardiovascular events, and all-cause mortality. Eur Heart J 44(44); PMC10635668 (C0276) | **PARTIAL** (EHR; inherits T-BEHRT) | NONE | NONE | NONE | "the encoder model is employed to condense high-dimensional minimally processed EHR data into a rich compact vector … Second, the patient representation vector is used as input to jointly learn the propensity score … and the outcome of interest" (Methods, Statistical methods). An application, as above |

### S3.2 Settled at RELATED / NONE from the abstract or record (gate §6: "Screening to RELATED or NONE may use abstracts")

| work (records) | L1 | L2 | L3 | L4 | basis |
|---|---|---|---|---|---|
| Egami, Fong, Grimmer, Roberts & Stewart (2022). How to make causal inferences using texts. Sci Adv 8(42) (C0012, C0080, C0163) | RELATED | NONE | NONE | NONE | abstract: "a conceptual framework for making causal inferences with discovered measures as a treatment or outcome"; text as treatment or outcome, not adjustment covariates |
| Feder et al. (2022). Causal Inference in Natural Language Processing. TACL (C0014) | RELATED | NONE | NONE | NONE | a survey; it does not itself do the claim |
| Keith, Jensen & O'Connor (2020). Text and Causal Inference: A Review of Using Text to Remove Confounding. ACL (C0032) | RELATED | NONE | NONE | NONE | a review; it does not itself do the claim |
| Correlation does not equal causation … immunotherapy. Front Immunol 2025 (C0260) | RELATED | NONE | NONE | NONE | abstract: a review / perspective naming Targeted-BEHRT, CIMLA and CURE |
| Manolis & Kallistratos (2023). Deep learning approach to unmask hidden salt effects. Eur Heart J (C0270) | RELATED | NONE | NONE | NONE | an editorial comment on C0276 |
| Zhang et al. (2025). Causal inference model for accurate medical diagnosis in CABG. Artif Intell Med 167 (C0280) | RELATED | NONE | NONE | NONE | abstract (PubMed 40412270): backdoor adjustment inside a **risk-prediction** model, from structured EHR; not a treatment-effect estimate |
| A Survey of Deep Causal Models and Their Industrial Applications (2023) (C0284) | RELATED | NONE | NONE | NONE | a survey |
| Causal Forests for Discovering Diagnostic Language in Electronic Health Records. ASMB 2025 (C0290) | RELATED | NONE | NONE | NONE | abstract: words are the **treatments** (causal forests on MIMIC-III notes); no representation adjustment |

### S3.3 UNRESOLVED

| work (record) | what is open | reason |
|---|---|---|
| OmniNet: an expandable causal inference network for multiple modalities. Neural Comput Appl 2025, doi 10.1007/s00521-025-11202-9 (C0288) | **L1 only** (could be PARTIAL if a pretrained image / text encoder is used as a pre-treatment covariate). L2–L4: NONE from the abstract (no acquisition, benchmark or sequential content) | the OA PDF and the article HTML both return a bot challenge ("Client Challenge"); not in Europe PMC |

**Correction to the earlier UNRESOLVED list.** C0262, C0265 and C0276 were listed as UNRESOLVED after publisher PDFs
returned bot challenges. All three were then read in full from PMC (PMC9944753, PMC10423512, PMC10635668). Only C0288
remains UNRESOLVED.

## S4. Lead review of the acquisition / site records screened RELATED (L2 consistency check)

* **Why this review.** §8 gives an L2 PARTIAL example: "acquisition information analysed for prediction shortcuts,
  but tied to overlap or confounding only qualitatively". The screening rubric routed "site/shortcut leakage in
  embeddings without causal estimation" to RELATED. To make sure no L2 PARTIAL was lost at screening, the lead
  analyst reviewed every native record screened RELATED whose title or reason mentions site, scanner, batch,
  acquisition, device, shortcut, leakage or harmonization: **48 records**.
* **Rule applied, from §8 and the gate's lowest-grade logic.**
  * The L2 elements are:
    * representations of **video**;
    * **instrument-like** acquisition information;
    * which **amplifies bias or degrades overlap in causal estimation**.
  * A **static-image** shortcut paper differs in two of them (images instead of video; predictive "confounding" of a
    classifier instead of bias or overlap in causal-effect estimation), so it is **RELATED**.
  * Only a **video** paper whose acquisition analysis is tied, even qualitatively, to causal-estimation confounding or
    overlap could be PARTIAL.
* **Result.**
  * **All 48 abstracts concern prediction:** classification, segmentation, retrieval or explanation. Harmonization
    reviews and generic longitudinal causal methods are in the same position.
  * **None estimates the effect of an action or treatment.** The abstracts settle RELATED (gate §6).
  * The highest-risk abstracts were read in full:
    * **N0230:** "acquisition-related confounding" of frozen CT foundation-model features in **malignancy
      classification**;
    * **N0240:** pathology foundation models "encode pronounced scanner-specific variability";
    * **N0241:** negative controls for "volume-driven or contextual confounding" of **predictive** signatures;
    * **N0244:** "dataset membership, not a causal site … effect";
    * **N0384:** CIV-DG, where conditional IVs are used for **domain-generalization prediction**, not effect
      estimation;
    * **N0125, N0246, N0253, N0651.**
  * The two video or video-like records are also prediction only:
    * **N0210:** surgical-video skill-assessment **explanation bias** across surgeons and hospitals; no acquisition
      information in representations, no causal estimation;
    * **N0389:** cine CMR view–disease disentanglement for **classification**.
* **Conclusion.** No L2 DIRECT or PARTIAL among these records. They are the RELATED evidence for L2 and are cited as
  such in `LIT_GATE_RESULT.md`.

## S5. Semantic Scholar and proceedings arms (keyed run, 2026-10-02; `0ac6aee`)

* **Run.**
  * 440 of 440 sub-queries returned (S2: 220, PROC: 220); 0 failed.
  * There were 262 HTTP 429 responses, each resolved within the 2–32 s backoff.
  * 800 hits deduplicate to 748 unique records (S0000–S0747).
  * 49 duplicate already-screened native or citation records and inherit those decisions.
  * 699 were screened under `RUBRIC.md`: 37 FULLTEXT, the rest NONE or RELATED (`screening/s2_batch_*_decisions.json`).
* **Lead decisions on the 37 FULLTEXT records.** As in S1, a full text was read wherever DIRECT or PARTIAL could not
  be ruled out from the abstract.

### S5.1 Full text read

| uid | work | L1 | L2 | L3 | L4 | supporting passage (location) |
|---|---|---|---|---|---|---|
| S0414 | Cadei, Demirel, De Bartolomeis et al. (2025). Prediction-Powered Causal Inferences. NeurIPS; arXiv:2502.06343 | **PARTIAL** (non-medical video; representations used as the **outcome model**, not as adjustment covariates) | RELATED, **borderline**: the closest L2 mechanism in video | RELATED | NONE | L1: "we leveraged such annotated videos to fine-tune a pretrained model generalizing the predictions to ISTAnt and then estimating the ATE by AIPW on such prediction-powered sample" (§5, p. 8); encoders: ViT, CLIP-ViT, DINOv2 (Fig. 2). L2: recording-setup and background information is a shortcut that biases the ATE and threatens positivity: "the model can leverage such spurious shortcut in subsequent batches, relying on background information like the pen markings on the floor to identify the plate. This invalidates any downstream prediction-powered analysis" (Example 1, §2.1, p. 5); "up to violating positivity, which may bias any training and invalidate any causal downstream prediction-powered estimation" (p. 4). The two filming setups "mainly differ in lighting conditions, treatments, experimental nests (wall height) and color marking" (Fig. 3, p. 8). Graded RELATED because two L2 elements differ: the representations are an outcome model, not adjustment covariates, and the information acts as a **shortcut confounder of the outcome model, not an instrument**. L3: ISTAnt is a real (ant) video experiment with human-annotated ground truth; not medical, no instrument |
| S0209 | Israel, Grover & Van den Broeck (2023). High Dimensional Causal Inference with Variational Backdoor Adjustment. arXiv:2310.06100 | **PARTIAL** (images) | NONE | RELATED | NONE | L1: "we take a generative modeling approach to backdoor adjustment for high dimensional treatments and confounders" (Abstract, p. 1). In the X-ray experiment the confounder is the image: "a patient receives an initial X-ray scan … (Z)", using chest X-rays from MedMNIST (§4.3, p. 8). L3: semi-synthetic on real chest X-rays (static images); no acquisition instrument |
| S0446 | Rahman & Kocaoglu (2024). Conditional Generative Models are Sufficient to Sample from Any Causal Effect Estimand. NeurIPS; arXiv:2402.07419 | **PARTIAL** (images / text) | RELATED | RELATED | NONE | L1: "we show how to sample from any identifiable interventional distribution given an arbitrary causal graph through a sequence of push-forward computations of conditional generative models, such as diffusion models" (Abstract), including backdoor adjustment with image and text variables and "foundation models for chest X-ray generation" (p. 9). L2: hospital as a **confounder** of report style and pneumonia ("patients with severe pneumonia are transferred to a different hospital and receives critical reports"); not an instrument; static images. L3: semi-synthetic Colored-MNIST, not medical video |
| S0460 | Ma et al. (2025). LLM-Driven Treatment Effect Estimation Under Inference Time Text Confounding. NeurIPS; arXiv:2507.02843 | **PARTIAL** (text) | NONE | RELATED | NONE | L1: "we map the text T̃ to the text embedding ϕ(T̃) using a pretrained LLM. We then train a regression model … to predict the pseudo-outcome Ỹ from text embeddings" (§4.3, p. 7); pretrained BERT embeddings (§4.4, p. 8). L3: semi-synthetic narratives generated from structured data |
| S0008 | Field-of-view confounding shapes genetic discovery from self-supervised cardiac-imaging phenotypes (2026). medRxiv 10.64898/2026.09.01.26361959 | RELATED | RELATED, **borderline**: the closest L2 evidence in **medical video** | NONE | RELATED | "We trained a video masked-autoencoder on 69,932 UK Biobank cardiac cine-MRI studies and performed genome-wide association analysis of its latent representation … the representation encoded substantial field-of-view information: body size, stature and imaging centre (linear-probe R2 = 0.55 for site); standard genomic-control and LD-score diagnostics did not identify this source of phenotype-level confounding" (Abstract, p. 1). "A representation that encodes acquisition site more strongly than it predicts the heart's pump function …" (p. 3). L1 RELATED: the representations are GWAS **phenotypes (outcomes)**, not adjustment covariates for an action's effect. L2 RELATED: site information acts as a **phenotype-level confounder** of genetic association, not an instrument in effect estimation. L4 RELATED: representation-level removal of acquisition information (crop + residualisation), but static association, not sequential causal estimation |
| S0474 | Brahma, Henao, Carin et al. (2025). Coupling Generative Modeling and an Autoencoder with the Causal Bridge. NeurIPS; arXiv:2509.25599 | RELATED | NONE | NONE | NONE | Proximal causal learning: a task-specific autoencoder of the latent confounder from proxies. In the dSprite experiment the image is the **treatment** (§7.1, p. 7). Not generative / foundation representations of unstructured data used as adjustment covariates |
| S0443 | Rahman & Kocaoglu (2025). FeDCM: Federated Learning of Deep Causal Generative Models. UAI, PMLR 286 | RELATED | RELATED | NONE | NONE | Experiments are synthetic discrete graphs and IHDP (tabular): "We illustrate performance of FeDCM algorithm on synthetic and real-world IHDP data" (Experiments, p. 8). X-ray images appear only in the motivating example (Fig. 1). Clients are hospitals, but this is federated training, with no acquisition information in representations |

### S5.2 Settled at RELATED / NONE from the abstract (gate §6)

| uids | basis |
|---|---|
| S0138 CellFluxV2; S0150 CAPRI-CT; S0491 multi-site PD classification; S0588 Data AUDIT; S0459 FairTTE; S0305 federated multimodal oncology | **prediction or generation**, not effect estimation with representations as adjustment covariates. S0138: batch effects in a generative cell model. S0150: acquisition parameters as **treatments** of image quality. S0491: harmonization for classification. S0588: detectability of artifacts in task models, on static images. S0459: fairness of prognosis. S0305: a framework proposal |
| S0205 = S0232 (Feder et al. 2023, arXiv:2310.12803) | counterfactual augmentation for robust text **classifiers** (caregiver as a spurious attribute); prediction |
| S0239, S0412, S0444 SITE, S0472 NICE, S0506 Causal-BALD, S0574 DRCFS, S0729 DeepMatch, S0670 RMSN, S0411 CInA | representation learning on tabular / low-dimensional covariates, or task-specific CNNs trained from scratch on images (S0506, S0729). CInA (arXiv:2310.00809 abstract) is a "causally-aware foundation model" over tabular datasets. S0412 PMLR abstract: shadow-variable representations of observed variables |
| S0424 (Veitch et al. 2019), S0473 ProEmb | **network** embeddings as proxies; not image, video or text |
| S0504 DFPV | deep features trained from scratch for proxy variables (dSprite) |
| S0541 | Bayesian deep learning on MS MRI from **randomized** trials (no confounding adjustment); a model trained from scratch |
| S0299 DeepNetTMLE; S0335 CT-MTA; S0361 LDPE | treatment-invariant / debiased representations over time (networks, advertising, recommendation); no acquisition information. S0361 debiases recommendation, not an effect estimate |
| S0317 GST-UNet | spatiotemporal grid data with a U-Net trained from scratch; not medical, not generative / foundation |
| S0321 DeepGRAI | AI-derived volumes are **outcomes**; propensity matching on age, disability and follow-up; scanners unharmonized but not analysed as an instrument |

### S5.3 UNRESOLVED (full text not obtainable; abstract cannot settle)

| uid | work | what is open | reason |
|---|---|---|---|
| S0058 | A Semantic Embedding and Dynamic PSM-DID Framework … Green Patent Quality (ACM 2025, doi 10.1145/3800227.3800305) | L1 (text embeddings as matching covariates; at most PARTIAL) | no abstract; ACM PDF returns a bot challenge; OpenAlex: closed |
| S0340 | TIDAL: A Temporal Causal Diffusion Framework … Knee Osteoarthritis Treatment Outcomes (KDD 2026, doi 10.1145/3770855.3819025) | L1 (whether trajectory-encoding image representations act as adjustment covariates; at most PARTIAL, X-ray sequences). L2–L4 RELATED / NONE from the abstract | ACM PDF bot challenge (OpenAlex lists it as gold OA) |
| S0373 | LLMCE: Adapting LLMs with Adversarial Debiasing for Counterfactual Estimation over Time (CIKM 2025, doi 10.1145/3746252.3760914) | L1 (frozen-LLM representations of time series for counterfactual estimation; at most PARTIAL). L4 RELATED from the abstract | ACM PDF bot challenge; OpenAlex: closed |
| S0242 | Synthetic Ground Truth Counterfactuals for Comprehensive Evaluation of Causal Generative Models in Medical Imaging (MICCAI 2025, doi 10.1007/978-3-032-04984-1_52) | L3 | no abstract; Springer bot challenge; closed |

## S6. Citation chasing for the new PARTIAL hits (S0414, S0209, S0446, S0460): one level, gate §6

* **Collection** (`citation_chase_s2.py`).
  * OpenAlex holds no reference lists for these four works, so backward references were parsed from the PDFs:
    * S0414: 56;
    * S0209: 31;
    * S0446: 64;
    * S0460: 73.
  * Forward citations come from the OpenAlex `cites:` filter: 3 in total.
  * That gives 227 records (C0298–C0524). Three are parsing debris: C0353, C0384, C0448.
* **Screening:** 88 NONE, 109 RELATED, 30 FULLTEXT (`screening/citation_s2_batch_decisions.json`). Seven FULLTEXT
  records are works already graded, and they keep their grades:
  * C0304: Jerzak 2023b;
  * C0458: Daoud 2022;
  * C0468: Guo 2025;
  * C0495: Mozer 2020;
  * C0499: Pryzant 2021;
  * C0500: Roberts 2020;
  * C0511: Veitch 2020.

  C0463 (Egami 2022) and C0481 (Keith 2020) are also already graded, RELATED, in S3.2.

### S6.1 Full text read

| uid | work | L1 | L2 | L3 | L4 | supporting passage (location) |
|---|---|---|---|---|---|---|
| C0306 | Cadei, Lindorfer, Cremer, Schmid & Locatello (2024). Smoke and Mirrors in Causal Downstream Tasks. NeurIPS; arXiv:2405.17151 | **PARTIAL** (non-medical video; **outcome model** in an RCT) | RELATED, **borderline** (as for S0414) | RELATED | NONE | "we fine-tune 6 480 state-of-the-art models" on ISTAnt ant videos to estimate the ATE (p. 2). "e is an encoder potentially pre-trained on a much larger corpus … If a representation is only sufficient, redundant information from W or S could be preserved, potentially leading to systematic errors on Du due to spurious correlations" (§3, "Model bias from the encoder choice", p. 4). W = the experiment settings, which shift the outcome model; not an instrument, and not adjustment covariates |
| C0332 | Yao, Rancati, Cadei, Fumero & Locatello (2025). Unifying Causal Representation Learning with the Invariance Principle. ICLR; arXiv:2409.02772 | **PARTIAL** (non-medical video; outcome model) | RELATED | NONE | NONE | "The goal is to extract a per-frame representation for supervised behavior classification (grooming or not) to estimate the Average Treatment Effect of an intervention" on ISTAnt (§5.1, p. 9). Backbone DINOv2 (App. F). Invariance enforced across experiments and positions |
| C0320 | Yao, Huang, Cadei, Zhang & Locatello (2025). The Third Pillar of Causal Analysis? A Measurement Perspective on Causal Representations. NeurIPS; arXiv:2505.17708 | **PARTIAL** (non-medical video; representations as outcome **measurements**) | RELATED | NONE | NONE | "This experiment validates the T-MEX score on ISTAnt … The goal is to extract a per-frame representation for supervised behavior classification (grooming or not) to estimate the ATE" (§5.2, p. 8) |
| C0424 | Rahman & Kocaoglu (2024). Modular Learning of Deep Causal Generative Models for High-dimensional Causal Inference. ICML; arXiv:2401.01426 | **PARTIAL** (images) | RELATED | RELATED | NONE | pre-trained conditional generative models answer identifiable causal queries with image variables (Abstract). The COVIDx example: "hospital location acts as a latent confounder" (§1, p. 2), i.e. site as a **confounder**, not an instrument |
| C0452 | Chen, Bhattacharya & Keith (2024). Proximal Causal Inference with Text Data. NeurIPS; arXiv:2401.06687 | **PARTIAL** (text) | NONE | RELATED | NONE | "uses two instances of pre-treatment text data, infers two proxies using two zero-shot models on the separate instances, and applies these proxies in the proximal g-formula" (Abstract, p. 1); zero-shot LLMs |
| C0460 | Deshpande, Wang, Sheldon, Lin & Kuleshov (2022). Deep Multi-Modal Structural Equations For Causal Effect Estimation With Unstructured Proxies. NeurIPS; arXiv:2203.09672 | **PARTIAL** (images / text) | NONE | RELATED | NONE | "deep multi-modal structural equations, a generative model for causal effect estimation in which confounders are latent variables and unstructured data are proxy variables. This model supports multiple multi-modal proxies (images, text)" (Abstract, p. 1) |
| C0462 | Dhawan, Cotta, Ullrich, Krishnan & Maddison (2024). End-To-End Causal Effect Estimation from Unstructured Natural Language Data (NATURAL). NeurIPS; arXiv:2407.07018 | **PARTIAL** (text) | NONE | RELATED | NONE | "Our estimators use LLM conditional distributions (over variables of interest, given the text data) to assist in the computation of classical estimators of causal effect" (Abstract), including "inverse propensity score weighting and outcome imputation" (§1, p. 2) |
| C0494 | Maiya (2021). CausalNLP: A Practical Toolkit for Causal Inference with Text. arXiv:2106.08043 | **PARTIAL** (text) | NONE | NONE | NONE | "CausalNLP includes an implementation of CausalBert … which is essentially an S-Learner that uses a DistilBERT text classification model as the base learner with extra covariates representing additional confounders" (§3.1, p. 3) |
| C0507 | Sridhar & Getoor (2019). Estimating Causal Effects of Tone in Online Debates. IJCAI; arXiv:1906.04177 | **PARTIAL** (text; generative text model) | NONE | NONE | NONE | "we learn representations of ideology using generative models of text … our latent confounder representation reduces bias in ATE estimation" (Abstract, p. 1) |
| C0520 | Zeng et al. (2022). Uncovering interpretable potential confounders in electronic medical records. Nat Commun 13:1014; PMC8866497 | RELATED | NONE | NONE | NONE | "we use simple NLP techniques (e.g., entity identification, bag-of-words) to generate matrix representations" (Introduction), then Lasso. Explicitly not deep embeddings |

### S6.2 Settled at RELATED from the abstract

| uids | basis |
|---|---|
| C0328 De Bartolomeis 2025; C0329 Poulet 2025 | foundation-model or prognostic predictions combined with **randomized** trials for precision; not confounding adjustment with representations of unstructured data |
| C0356 Chen 2019; C0478 Johansson 2016; C0479 Johansson 2018; C0380 Xu & Gretton 2022 | representations trained from scratch on EHR, tabular or bag-of-words covariates; NMMR uses neural features on dSprite |
| C0514 Wang & Culotta 2019; C0515 Weld 2022; C0516 Wood-Doughty 2018; C0522 Zhang 2020 | quasi-experimental matching on words; an evaluation framework comparing others' methods (L3 RELATED: real text, not medical video); text classifiers as measurement; conversation features |

### S6.3 UNRESOLVED

| uid | work | what is open | reason |
|---|---|---|---|
| C0377 | Tesei et al. (2023). Learning end-to-end patient representations through self-supervised covariate balancing for causal treatment effect estimation. J Biomed Inform 140:104339 | L1 (EHR representations; at most PARTIAL) | ScienceDirect returns a bot challenge; OpenAlex marks it hybrid OA but has no repository copy |

**No further chasing.** These hits are one citation level from search hits, and gate §6 requires one level only.
