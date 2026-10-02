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
