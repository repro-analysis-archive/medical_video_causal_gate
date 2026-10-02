# DATA SELECTION GATE — Medical Video Causal Track (v4)

**Status: consolidated v4.** It becomes frozen when this file alone is committed. Nothing is searched, read or
downloaded under this gate before that commit.

## 0. Disclosure of pre-freeze information

- **C-US (US-PPNR)** was assessed against these criteria BEFORE freezing, from commit 8e059cf (repository
  `~/projects/us_ppnr_0A`).
  - Under D7 as defined below, its NDI poses would pass D7.
  - Its exclusion rests on D4 for the SS arm, and on D1 and D4 for the RA arm.
  - C-US is EXCLUDED from both arms and listed for transparency only.
- **C-CATH:** the CathAction dataset card was read earlier (action classes; collision data in a separate structure).
  No D-criterion verdict was made.
- **Pre-freeze theory checks.** Each was committed in this repository, with its spec committed before computing:
  - **role switch:** spec 0810087, result 47a49ea;
  - **robustness** (E1 action persistence, E2 pre-window history, E3 AR(1) unmeasured confounding, E4 binary
    actions): spec 04859b2, result 6165ece;
  - **R2_Z recoverability diagnostic:** spec a45298d, result 6665b4c. It failed its pre-fixed stop rule (136 / 945
    cells misclassified, above 10 %), so the theory track is closed and the paper uses the conditional map as is.
- **Basis of §5b:** `checks/role_switch/prior/persistent_iv_exact.py` (committed in 0810087). It is a closed-form
  check, with no random draws, that a trajectory-constant factor is a confounder, not an instrument, under a sustained
  intervention with history-dependent recursion.
- "Fixed before any audit result" applies to all other candidates.

## 1. Purpose

Select public data for the first paper: "When do generative/foundation video representations improve or degrade
sequential confounding adjustment in medical video?"
- **SS arm (primary):** real medical video; treatment and outcome synthesized by pre-frozen rules; true effect known.
- **RA arm (secondary):** real human actions and real linked outcomes.

One dataset may serve both arms. This gate authorizes the literature search of §6 and metadata inspection,
within the limits of §7.

## 2. Criteria

**Unit:** one trajectory = one continuous recording of one procedure. Clips from the same procedure count once. All
counts below use this unit.

**Subset:** a documented release unit with its own directory or README. A subset that is entirely human-teleoperated
or entirely clinician-performed is eligible on its own.

- **D1 Human decisions.**
  - A time-stamped action variable is recorded per trajectory, and actions are chosen by clinicians or human
    operators for >= 200 trajectories.
  - Collection mode is identifiable per trajectory, OR the documentation states that no programmatic/state-machine
    collection exists in the dataset.
- **D2 Linked outcome.**
  - An outcome on the same trajectory after the action, from human annotation or from a sensor measurement
    independent of the video.
  - Human annotation of post-action frames qualifies.
  - Model-derived labels do not qualify.
- **D3 Continuous trajectories.** Frames time-aligned and contiguous, not isolated clips.
- **D4 Heterogeneity.** For at least one factor among site, device and operator, >= 2 levels each having >= 20
  trajectories, recorded per trajectory.
- **D5 Access.** The license permits research use and release of derived features.
- **D6 Storage.** The total size including video fits a disk other than the H1R raw disk with >= 3x headroom.
- **D7 Content variable.** A frame- or segment-level variable describing video content (human annotation, OR sensor
  ground truth of scene state) that (a) varies within trajectories, and (b) is not acquisition metadata.
- **D8 Separability (SS arm).**
  - **Pass if,** for at least one pair of an acquisition factor that meets D4 and a content variable that meets D7,
    Cramér's V between them is <= 0.5.
  - **Weighting:** frames are weighted so that each trajectory sums to 1.
  - **Content variable:** continuous content is binned at the pooled weighted quartiles; categorical content is used
    as is.
  - The cross-tabulation is used for D8 and nothing else.

**Arm requirements:**
- **SS arm:** D3, D4, D5, D6, D7, D8, and >= 200 trajectories.
- **RA arm:** D1, D2, D3, D4, D5, D6.

## 3. Candidates

- **C-COL:** multi-center colonoscopy full-procedure video.
- **C-SURG:** surgical video with linked labels. This includes surgical subsets with recorded kinematics (e.g.,
  Open-H), the main route to a recorded action variable under D1.
- **C-CATH:** CathAction.
- (C-US excluded; see §0.)

For C-COL and C-SURG, list every dataset found, then audit each.

**Dataset search scope for C-COL and C-SURG:**
- **Sources:** OpenAlex; Semantic Scholar; Hugging Face; Grand-Challenge; Synapse; PhysioNet; Zenodo; Figshare.
- **EndoVis:** every MICCAI EndoVis challenge dataset, with the list taken from the Grand-Challenge EndoVis pages.
- **Queries:**
  - "colonoscopy video dataset"
  - "full-procedure colonoscopy"
  - "endoscopy video dataset multi-center"
  - "surgical video dataset"
  - "surgical kinematics video dataset"
- **Stopping:** the first 50 results per query per source, plus every EndoVis dataset. Every screened record is
  logged.

## 4. Per-dataset audit (metadata, documentation and annotation files only)

- **D1–D8:** each PASS / FAIL / UNKNOWN, with the exact quoted source line or file path. UNKNOWN is not PASS.
- **Counts:** by collection mode, site, device, operator and annotation type.
- **Cross-tabulation:** the D7 content variable by each acquisition factor, from metadata and annotation files only.
  It is weighted as in D8 and reported with Cramér's V for each eligible pair.

## 5. Decision rule (fixed before any audit result on §3 candidates)

"Qualifying levels" = the maximum, over site, device and operator, of the number of levels with >= 20 trajectories.

**SS arm:**
- Rank the datasets passing all SS requirements by:
  1. qualifying levels;
  2. then total trajectory count;
  3. then D7 annotation density;
  4. then access without registration.
- Select the top-ranked dataset. A remaining tie goes to human decision.
- None passes: STOP for human decision. Do not relax the criteria.

**RA arm:**
- The same procedure among the datasets passing all RA requirements, with the D1 trajectory count ranked first.
- None passes: the RA arm is deferred, and the SS arm proceeds alone.

## 5b. Constraints carried to the separate SS synthesis protocol

These are not defined here. They are frozen before any representation is extracted.

- **Persistence.** Trajectory-constant acquisition factors are persistent. With a history containing past actions,
  for K >= 2, or for any K when the outcome depends on post-window actions (P >= 1), they lie on a back-door path
  through later actions and are confounders, not instruments. They must not be called instruments.
- **Net effect of adjusting.** Adjusting for them removes that confounding, but can amplify bias from unmeasured
  confounding.
  - The net effect depends on K, P, the length of the pre-window history, the action type, and the confounding
    strength. The constants are in SPEC files 0810087 and 04859b2, and the maps in 47a49ea and 6165ece.
  - The SS protocol states its predictions conditionally on these factors.
- **Bias** is reported relative to the true contrast Psi(delta) - Psi(1).
- **Design axes.** Intervention duration K, the number of post-window
  actions P, and the pre-window history length are primary design axes.
  They must include K = 1 with P = 0, the only case in which a
  trajectory-constant factor can be instrument-like.
- **Pure instrument.** A pure instrument condition, if used, must be a within-trajectory, serially independent
  variable active only at window steps (FUTURE_INSTRUMENT_CONDITION.md). It must pass the simulator's verification
  checks 3–4 before being called an instrument. Until then, it is "instrument-like".
- **Confounder.** The confounder is built from the D7 content variable.
- **Scope.** The SS arm is a benchmark of adjustment sets, not a re-commissioning of DR-FLEX.

## 6. Literature gate (fixed before reading)

**Claims:**
- **L1:** Generative or foundation video representations used as adjustment covariates for the causal effect of an
  action or treatment.
- **L2:** Analysis showing that such representations carry instrument-like acquisition information (site, device,
  operator) that amplifies bias or degrades overlap.
- **L3:** A semi-synthetic causal benchmark on real medical video in which acquisition information is manipulated as
  an instrument.
- **L4:** Analysis of how the causal role of acquisition information encoded in representations (instrument-like vs
  confounder) depends on intervention duration or persistence. This includes the effect of
  acquisition-information-removed (site-invariant, harmonized or debiased) representations on sequential causal
  estimation.

**Grading per source:** DIRECT / PARTIAL / RELATED / NONE.
- For a condition combining several claims in one paper, the paper's grade is the lowest of its component grades.
- **Generic identification results** (e.g., Richardson & Robins 2013; Young, Hernán & Robins 2014) are graded
  RELATED, unless they address acquisition information encoded in representations or the role switch.
- DIRECT or PARTIAL may be assigned only after the full text has been read
  directly; the supporting passage is quoted with page or section.
  Screening to RELATED or NONE may use abstracts. A source whose full text
  cannot be read is UNRESOLVED and listed for the investigator.

**Consequences:**
- L1 and L2 DIRECT in the same paper, in medical video: NO-GO for the headline.
- L1 and L2 in the same paper, but in static medical images or non-medical video: PARTIAL; GO with the claim narrowed
  to sequential medical video.
- L1 and L2 in different papers: GO; cite both.
- L3 DIRECT: drop the benchmark-novelty claim and cite.
- L4 DIRECT: the duration-dependence headline is dropped and cited.
- L4 PARTIAL: GO; narrow the claim to what the source does not cover, and
  cite.

**Search scope:**
- **Databases:** PubMed; arXiv (cs.CV, cs.LG, stat.ME, stat.ML); OpenAlex; Semantic Scholar; proceedings of MICCAI,
  IPMI, MIDL, NeurIPS, ICML, CLeaR, UAI.
  - Google Scholar is replaced by OpenAlex and Semantic Scholar.
  - Where a source does not support boolean queries, a query is split into sub-queries, and each sub-query is
    logged.
- **Dates:** 2018-01-01 to the freeze date.
- **Query families:**
  - **Q1** (medical video OR surgical video OR endoscopy OR colonoscopy OR ultrasound video OR fluoroscopy) AND
    (causal OR treatment effect OR confounding OR propensity OR counterfactual) AND (representation OR embedding OR
    foundation model OR generative)
  - **Q2** (image embedding OR foundation model OR deep features) AND (site OR scanner OR batch OR acquisition) AND
    (confounding OR causal OR propensity)
  - **Q3** (semi-synthetic OR benchmark) AND causal AND (medical image OR medical video)
  - **Q4** (domain-invariant OR site-invariant OR harmonization OR debiasing OR adversarial) AND (causal OR treatment
    effect OR propensity OR confounding) AND (longitudinal OR sequential OR time-varying)
- **Stopping:** the first 100 results per query per database by relevance, plus one level of backward and forward
  citation for every DIRECT or PARTIAL hit. Every screened record is logged.

**Known prior work:**
- Nakamura, Breuer, Crespin, Dietrich & Imai (2026). Causal Inference with Video Features as Treatments.
  arXiv:2607.06126.
- Nakamura & Imai (2026). GenAI Powered Dynamic Causal Inference with Unstructured Data. arXiv:2605.07834.
- Imai & Nakamura (2026a). Causal inference with generative artificial intelligence: Application to texts as
  treatments. Journal of the American Statistical Association, forthcoming.
- Imai & Nakamura (2026b). Leveraging generative AI for causal inference with unstructured data. Proceedings
  of the National Academy of Sciences 123(36): e2530532123.
- The investigator's pathology foundation-model site audit (related to L2 for static images). To be replaced by its
  preprint reference when available.

## 7. Not authorized by this gate

- Downloads beyond metadata, annotations and one sample video per dataset.
- For the sample video:
  - allowed: container metadata inspection, and viewing a few frames to confirm format;
  - not allowed: any further decoding, any computation, or any representation extraction.
- Creating accounts, registering, or accepting data use agreements. These are done by the investigator.
- Any change to the H1R or theory repositories.
