# Data Audit Result (gate `baadf5c` §§2–5)

**Decision:**
* **SS arm:** no dataset passes all SS requirements, so the result is **STOP for human decision** (§5).
* **RA arm:** no dataset passes D1–D6, so the RA arm is **deferred** (§5).

No criterion was relaxed.

**Basis.**
* All 194 listed datasets were audited.
* The only dataset the audit agents found eligible for either arm, DS024 (JHU LCSR SMARTS), was re-verified by the lead
  analyst under a spec committed before any of its data were read (`LEAD_VERIFICATION_SPEC.md`, commit `4a6f2b1`).
* Only **162 of its 236 cases** meet the pre-fixed contiguity rule, so it fails ≥200 (SS) and the D1 trajectory count (RA).

## 1. What was done

* **Search (gate §3).**
  * Sources: OpenAlex, Hugging Face, Grand-Challenge (complete listing), Synapse, PhysioNet, Zenodo and Figshare, plus
    every EndoVis page. 1,360 records were screened.
  * The candidate list (`DATASETS.json`) has **194 entries**:
    * C-COL: 32;
    * C-SURG: 78;
    * C-CATH: 1, CathAction;
    * Open-H: 83 surgical and endoscopy subsets at revision `e29dda7c`.
  * The **Semantic Scholar arm** of the dataset search was not run. It shares the literature-search client, which is
    BLOCKED by HTTP 429 (`lit/LIT_GATE_RESULT.md` §5).
* **Audit (gate §4).**
  * Eight audit agents worked under fixed instructions (`audits/AGENT_INSTRUCTIONS.md`, `AUDIT_TEMPLATE.md`).
  * Every D1–D7 verdict carries a verbatim quote and its source. Each agent machine-checked its quotes against saved
    copies of the sources.
  * Outputs: `audits/A_*_audit.json`, consolidated in `DATA_AUDIT_TABLE.csv`, one row per dataset with verdict, quote,
    source and counts by collection mode, site, device, operator and annotation type.
* **Lead verification** (`lead/`):
  * DS024: D3 contiguity, recounts, D8;
  * DS113: Cramér's V;
  * re-checks from saved files of CAS-Colon devices, REAL-Colon sites and devices, ROSMA operators, CathAction schema
    and Open-H DS193 per-episode keys (§6).
* **Restrictions kept (gate §7).**
  * No account, registration, form submission or data-use acceptance.
  * **No video downloaded for any dataset.** No sample video was needed.
  * Only documentation, metadata and annotation files were downloaded, plus the DS024 kinematics/timestamp parquet
    files (0.435 GB, no mp4), all on LaCie.
  * No computation on video, no representation, no model.
  * The H1R and theory repositories were not touched.

## 2. Verdict counts (all 194 datasets, after lead verification)

| criterion | PASS | FAIL | UNKNOWN |
|---|---|---|---|
| D1 | 33 | 136 | 25 |
| D2 | 50 | 129 | 15 |
| D3 | 95 | 75 | 24 |
| D4 | 3 | 174 | 17 |
| D5 | 149 | 6 | 39 |
| D6 | 153 | 0 | 41 |
| D7 | 150 | 26 | 18 |

* **D4** passes for only three datasets:
  * DS024: operator, recorded per episode;
  * DS113: surgeon, in `videos.csv`;
  * DS155: laparoscope type / country, documented per video but registration-gated.
* Everywhere else, site, device and operator are either single-valued or stated only at dataset level. This holds for
  every Open-H subset: its `episodes.jsonl` holds only `episode_index`, `tasks` and `length`.

## 3. Cramér's V for each eligible pair (gate §4; D4 PASS × D7 PASS)

### DS024: operator (`user_id`) × PSM kinematics, the 162 contiguous cases

Frames are weighted so each case sums to 1, and the variable is binned at pooled weighted quartiles.

| D7 variable | V, all 13 recorded operators (gating) | V, operators with ≥20 cases (descriptive) |
|---|---|---|
| psm1.x | 0.291 | 0.275 |
| psm1.y | 0.467 | 0.336 |
| psm1.z | 0.497 | 0.472 |
| psm2.x | 0.449 | 0.302 |
| psm2.y | 0.445 | 0.245 |
| psm2.z | 0.575 | 0.546 |
| psm1.gripper | 0.472 | 0.195 |
| psm2.gripper | 0.520 | 0.307 |

D8 would pass: the minimum V is 0.291, which is ≤ 0.5. **It does not matter for the decision, because
DS024 fails ≥200.**

### DS113 (Cataract-101): surgeon × phase

* 101 videos; surgeons 1–4 have 25 / 24 / 32 / 20 videos.
* A 4 × 10 table.
* **V = 0.073**.
* 29,237 frames before the first annotated phase were dropped.
* Not SS-eligible: 101 < 200.

### DS155 (SAGES CVS)

* **Not computable.** The per-video laparoscope and country fields are behind challenge registration.
* It fails D3 (each case is a "90-second segment") and D5 ("solely for the purpose of competing in the official CVS
  challenge") regardless.

## 4. DS024 (JHU LCSR SMARTS / SurgSyncExt): the only candidate, verified

* **Unit.** A case is (leaf, `case_id`): one full task execution, made of consecutive subtask episodes. There are 236
  cases and 2,509 episodes. Every case has one `user_id`.
* **Passes.**
  * D2: measured PSM joint effort, a non-video sensor value after each action. This is a weak outcome but literally
    within D2.
  * D4: 13 operators per episode.
  * D5: "CC BY 4.0".
  * D6: 190.10 GB.
  * D7: PSM kinematics as sensor ground truth.
  * All are quoted in the table.
* **D3: the decisive check (spec §3, fixed before reading).** A case is contiguous if its largest real-time
  (ROS-clock) gap, including across subtask-episode boundaries, is ≤ 1.0 s, with no decrease.
  * **Result: 162 / 236 contiguous.**
    * Offline recorder: 96 / 96. All gaps are 0.1 s; it is "a
      solid 10.00 FPS".
    * Online recorder: 66 / 140. It is documented as "irregular dt",
      "4.04 (+/- 1.69) Hz", "assemble everything assume 10 FPS". The per-case maximum gap has median
      1.073 s and maximum 5.938 s.
  * ROS time is never missing, and there is no decrease.
  * **Consequence:** the ≥200 count fails (162). D1 fails (162 < 200 human-operated trajectories). The D4 qualifying
    levels on contiguous cases are 3: users 2 / 11 / 13 with 38 / 28 / 20 cases.
* **Sensitivity to the tolerance (descriptive only; the gating value was fixed at 1.0 s before the data were read).**

  | max-gap tolerance | contiguous cases (online + offline) | operators with ≥20 cases |
  |---|---|---|
  | 0.5 s | 106 (10 + 96) | 3 |
  | **1.0 s (gating)** | **162** (66 + 96) | 3 |
  | 2.0 s | 214 (118 + 96) | 4 |
  | 5.0 s | 235 (139 + 96) | 4 |

  **The selection outcome depends on this tolerance.** With a looser definition of "contiguous" (2 s or more), DS024
  would reach ≥200. D8 was not recomputed at any other tolerance. Changing the tolerance is a definition change for
  the investigator, not something the analyst may do after seeing the data.
* **Other facts the investigator should weigh.**
  * The data are **ex-vivo tissue and table-top phantoms**, not clinical. Gate §1 describes the SS arm as using "real
    medical video".
  * The README's manual video–kinematic delay checks (one episode per leaf) found +200 to +1,200 ms. The README says
    these include physical response time.
  * The online QC reports timestamp WARNINGs in P1 and one ERROR in P2. The ERROR is a 1 µs decrease in the nominal
    timestamp column. The ROS clock has no decrease.
  * 4 cases carry `data_collection_scenario: Clinical` although the README ticks only Ex-Vivo and Phantom.

## 5. Gate §5, applied mechanically

* **SS arm** (D3, D4, D5, D6, D7, D8, ≥200): **0 datasets pass.**
  * DS024 fails ≥200 (162).
  * DS155 fails D3 and D5.
  * DS113 fails ≥200 (101).
  * Every other dataset fails D4, or has D4 UNKNOWN.
  * → **STOP for human decision.** Nothing is ranked or selected.
* **RA arm** (D1–D6): **0 datasets pass.**
  * DS024 fails D1 (162 contiguous human trajectories).
  * Every other dataset fails or is UNKNOWN on D1 and/or D4.
  * → **RA arm deferred.**

## 6. Near misses, and what could change them

| dataset | n | blocking criterion | can investigator action change it? |
|---|---|---|---|
| DS024 JHU SMARTS | 236 cases | ≥200 / D1, through D3 contiguity (162 at 1.0 s) | only by **amending the definition** of "contiguous" (a gate amendment); 214 cases at 2.0 s |
| DS000 CathAction | 569 videos | D4 UNKNOWN (10 surgeons, 2 fluoroscopy systems stated at dataset level only); D2 UNKNOWN (collision labels stored separately, no video key documented) | **yes, partly.** Submitting the access form and licence (investigator) would show whether a per-video operator or device field exists. The documented action schema (`video_id, start_frame, stop_frame, all_action_classes`) has none |
| DS173 Trauma THOMPSON | 220 | D4 UNKNOWN (2 institutions and 15 environments at dataset level only); D2 UNKNOWN | **yes, partly.** The consent form gates the archive README and CSVs that might hold a per-video site field |
| DS155 SAGES CVS | 1,000 | D3 FAIL (90-s clips), D5 FAIL (challenge-only use) | no: D3 is a property of the data |
| DS178 ROSMA (dVRK) | 206 | D4 FAIL: 12 operators with 16–18 trials each (re-counted from `scores.csv`) | no |
| DS113 Cataract-101 | 101 | ≥200 | no |
| DS145 ORena FOCUS | 200 | D4 FAIL, D5 FAIL (challenge agreement) | no |
| Open-H pooled across institutions | — | not a unit in `DATASETS.json` (subsets were listed); the documented release is "4.5 TB" > 2.02 TB, so D6 FAIL | no |

## 7. Disclosures

* **Commit `4a6f2b1`** committed the spec together with the audit outputs then on disk.
  * Its message said "31 untitled entries"; the correct number is **11**.
  * It included `A_surg4_audit.json` before that agent reported back. The final version differs only in one quote's
    whitespace and one count inside a reason (149 → 150 of 155 cases). No verdict changed.
* **Parsing.** The DS024 parquet stores shape-[1] features as length-1 arrays. They were flattened to scalars, a
  mechanical fix, before the first and only D8 computation.
* **LaCie free space** is now 5.6 TB (6.07 TB at the freeze). The D6 limit stays as frozen (2.02 TB).

## Appendix: per-dataset verdicts

Quotes, sources and counts are in `DATA_AUDIT_TABLE.csv` and `audits/A_*_audit.json`.
* P / F / U = PASS / FAIL / UNKNOWN; pend = PENDING-LEAD.
* DS113: V = 0.073, computed (§3).
* DS155: not computable.
* DS024 rows show the verdicts after lead verification.

| id | name | n | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | ≥200 | reg. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DS076 | C3VD / C3VDv2 / C3VD-Raycasting-10k | 218 | F | F | P | F | P | U | P | F | P | no |
| DS077 | CAS-Colon | 78 | F | F | P | F | P | P | P | F | F | no |
| DS078 | CLiMB 2026 (Colonoscopy Localization and Mapping Benchmark;  | — | F | U | P | U | U | U | U | F | F | yes |
| DS079 | CLTS-GAN augmented polyp dataset | 0 | F | F | F | F | P | P | F | F | F | no |
| DS080 | Colonoscopy anonymized data, University Hospital of Bern, 20 | 8 | F | F | U | F | P | P | F | F | F | no |
| DS081 | EAD2019 (Endoscopy Artefact Detection challenge 2019) | 0 | F | F | F | F | P | P | F | F | F | no |
| DS082 | EndoCV2020 (EAD2020 / EDD2020) | 5 | F | F | F | F | P | P | P | F | F | yes |
| DS083 | EndoCV2021 (polyp generalisation; data released as PolypGen) | — | F | F | F | U | U | P | P | F | F | yes |
| DS084 | EndoCV2022 (PolypGen 2.0 / EAD 2.0) | — | F | F | F | U | U | U | P | F | F | yes |
| DS085 | EndoMapper | 96 | F | U | P | U | U | U | P | F | F | yes |
| DS086 | ENDOTEST | 10 | F | F | P | F | U | U | P | F | F | unknown |
| DS087 | EndoVis 2015 Polyp Detection (CVC-ClinicDB, ETIS-Larib, ASU- | — | F | F | F | F | U | U | P | F | F | yes |
| DS088 | FoldIt (model weights + testing frames, Zenodo 4993651) | — | F | F | F | F | P | P | F | F | U | no |
| DS089 | FoldIt Public Dataset (Zenodo 5519974) | 0 | F | F | F | F | P | P | F | F | F | no |
| DS090 | GIANA (EndoVis GIANA 2017/2018/2021; incl. EndoVis abnormal  | — | F | F | F | F | U | U | P | F | F | yes |
| DS091 | HyperKvasir | — | F | F | F | F | P | P | F | F | U | no |
| DS092 | IBD Crowdsourced Endoscopy Annotation (Digital Endoscopy DRE | — | U | U | U | U | U | U | U | F | U | unknown |
| DS093 | InfoColon | 164 | F | F | P | F | P | P | P | F | F | yes |
| DS094 | LDPolypVideo | 263 | F | F | U | F | U | U | U | F | U | no |
| DS095 | POCACO | 54 | F | F | F | F | U | U | P | F | F | yes |
| DS096 | Polyp-Size | 42 | F | F | F | F | P | P | F | F | F | no |
| DS097 | PolypsSet | 155 | F | F | F | U | P | P | P | F | F | no |
| DS098 | Procedurally Generated Colonoscopy and Laparoscopy Data | — | F | F | F | F | P | P | F | F | F | no |
| DS099 | REAL-Colon | 60 | F | F | P | F | P | P | P | F | F | no |
| DS100 | RealSynCol | 20 | F | F | P | F | P | P | F | F | F | no |
| DS101 | Renji ESD video dataset (esophagus + colorectal neoplastic l | 55 | F | P | P | F | P | P | P | F | F | no |
| DS102 | RT-GAN colonoscopy temporal dataset | 10 | F | F | F | F | P | P | U | F | F | no |
| DS103 | SegCol (EndoVis 2024) | — | F | F | F | U | U | U | P | F | U | yes |
| DS104 | SimCol / SimCol-to-3D 2022 / SimCol3D | 33 | F | F | P | F | P | P | F | F | F | no |
| DS105 | SUN-SEG | 113 | F | F | F | F | U | P | P | F | F | yes |
| DS106 | XDCycleGAN Depth Dataset | — | F | F | F | F | P | P | F | F | U | no |
| DS107 | XDCycleGAN VC Dataset | — | F | F | F | F | P | P | F | F | U | no |
| DS000 | CathAction | 569 | P | U | P | U | P | P | P | F | P | yes |
| DS108 | ADM_LSIR | 19 | F | F | F | F | P | P | F | F | F | no |
| DS109 | AJU-Set | — | U | U | U | U | F | U | U | F | U | unknown |
| DS110 | AutoLaparo | 21 | F | F | P | F | P | U | P | F | F | yes |
| DS111 | Bypass40 | 40 | F | F | P | U | U | U | P | F | F | unknown |
| DS112 | CaDIS | 25 | F | F | F | F | U | U | P | F | F | yes |
| DS113 | Cataract-101 (extended labels) | 101 | F | F | P | P | P | P | P | pend | F | no |
| DS114 | CATARACTS (incl. CATARACTS 2018, 2020, Semantic Segmentation | 50 | F | F | P | F | P | P | P | F | F | yes |
| DS115 | CDS-COSA | 50 | F | F | F | F | P | P | P | F | F | no |
| DS116 | Cholec80 (incl. Cholec80-Boxes) | 80 | F | F | P | F | P | P | P | F | F | no |
| DS117 | CholecT50 (CholecTriplet2021/2022) | 50 | F | F | P | F | P | U | P | F | F | yes |
| DS118 | CholecTrack20 | 20 | F | P | P | F | P | U | P | F | F | yes |
| DS119 | DREAMING | — | F | F | F | F | P | P | F | F | F | no |
| DS120 | DRENDS (RoDEO challenge) | 27 | F | P | P | F | P | P | P | F | F | no |
| DS121 | EgoSurgery-Phase | 20 | F | F | P | F | P | U | P | F | F | yes |
| DS122 | Endoscopic Pituitary Surgery on a High-fidelity Bench-top Ph | 15 | F | P | P | F | P | P | P | F | F | no |
| DS123 | EndoVis 2015 Instrument | 12 | F | F | F | F | U | U | P | F | F | no |
| DS124 | EndoVis 2017 Kidney Boundary Detection | — | F | F | F | F | U | U | P | F | F | yes |
| DS125 | EndoVis 2017 Robotic Instrument Segmentation | 10 | F | F | F | F | U | U | P | F | F | yes |
| DS126 | EndoVis 2017 Surgical Workflow (SensorOR; data released as H | 30 | F | P | P | F | P | U | P | F | F | yes |
| DS127 | EndoVis 2018 Robotic Scene Segmentation | 19 | F | F | F | F | U | U | P | F | F | yes |
| DS128 | EndoVis 2020 (Endoscopic Vision Challenge, MICCAI 2020 umbre | — | F | F | P | U | P | U | P | F | F | yes |
| DS129 | ESAD / SARAS-ESAD / SARAS-MESAD | 9 | F | F | U | F | P | U | P | F | F | yes |
| DS130 | Fetoscopy Placenta Dataset (Bano et al. MICCAI 2020) | 6 | F | F | F | F | P | P | P | F | F | no |
| DS131 | FetReg / FetReg 2021 | 24 | F | F | F | F | P | U | P | F | F | unknown |
| DS132 | Hashemi 2025 human robotic surgery dataset (Closing the data | 15 | F | F | P | F | U | P | P | F | F | yes |
| DS133 | HeiChole (EndoVis 2019 Surgical Workflow and Skill) / HeiSur | 33 | F | P | P | F | P | P | P | F | F | yes |
| DS134 | HeiCo (Heidelberg Colorectal Data Set) | 30 | F | U | P | F | P | P | P | F | F | yes |
| DS135 | HiSWA-RLLS (EndoVis 2024 Hierarchical Surgical Workflow Anal | 45 | F | F | P | F | U | P | P | F | F | yes |
| DS136 | iMED: A Multi-Endoscope Dataset for Surgical 3D Perception | 14 | F | F | P | F | P | P | U | F | F | no |
| DS137 | JIGSAWS (JHU-ISI Gesture and Skill Assessment Working Set) | 101 | F | P | P | F | U | U | P | F | F | yes |
| DS138 | LapSurg-230K | 52 | F | F | F | F | P | P | P | F | F | no |
| DS139 | LASK: A Dataset for Laparoscopic Skill and 7-DoF Kinematics | 37 | F | F | P | F | P | P | P | F | F | no |
| DS140 | m2cai16-tool-locations | 10 | F | F | F | F | U | P | P | F | F | no |
| DS141 | MACS: Microsurgical Aneurysm Clipping Surgery Dataset | 16 | F | F | F | F | P | P | P | F | F | no |
| DS142 | MIPO dataset (distal radius fracture MIPO surgical workflow) | 50 | F | F | P | F | P | P | P | F | F | no |
| DS143 | MISAW (MIcro-Surgical Anastomose Workflow recognition) | 27 | F | F | P | F | P | P | P | F | F | yes |
| DS144 | NeuroSurgicalTools | 14 | F | F | F | F | U | U | P | F | F | unknown |
| DS145 | ORena SAVE FOCUS (HeiCo-FOCUS + LapChole-FOCUS) | 200 | U | U | P | F | F | P | P | F | P | yes |
| DS146 | P2ILF (Preoperative to Intraoperative Laparoscopy Fusion) | 11 | F | F | F | F | U | U | P | F | F | yes |
| DS147 | PhaKIR (Surgical Procedure Phase, Keypoint, and Instrument R | 8 | F | F | P | F | P | U | P | F | F | yes |
| DS148 | PitVis (PitVis-2023) | 25 | F | F | P | F | P | P | P | F | F | no |
| DS149 | PitVQA | 25 | F | F | F | F | F | P | P | F | F | no |
| DS150 | PitVQA-Anticipation | 25 | F | F | F | F | F | P | U | F | F | no |
| DS151 | RARP-45 | 45 | F | F | P | U | U | U | P | F | F | unknown |
| DS152 | RoboTool / semi-synthetic surgical tool data | 20 | F | F | F | F | P | P | P | F | F | yes |
| DS153 | ROBUST-MIPS | 30 | F | F | F | F | P | P | P | F | F | yes |
| DS154 | ROBUST-MIS 2019 | 30 | F | U | P | F | P | P | P | F | F | yes |
| DS155 | SAGES CVS Challenge | 1000 | F | P | F | P | F | U | P | pend | P | yes |
| DS156 | SAR-RARP50 | 50 | F | F | P | F | P | P | P | F | F | no |
| DS157 | SCARED | 9 | F | F | F | F | U | U | P | F | F | yes |
| DS158 | SICS-155 | 155 | F | F | P | F | P | P | P | F | F | no |
| DS159 | SimSurgSkill | 315 | F | P | U | U | U | P | P | F | P | no |
| DS160 | SLAM (Surgical LAparoscopic Motions) | 34 | F | F | F | F | P | P | P | F | F | no |
| DS161 | Stereo Endoscopic Dataset | — | F | F | F | F | P | P | P | F | U | no |
| DS162 | StereoMIS | 3 | F | F | F | F | P | P | F | F | F | no |
| DS163 | STIR (STIR Challenge 2025/2026; STIROrig) | — | F | F | F | U | P | P | P | F | U | yes |
| DS164 | SurgHint Annotations (HeiCo, Surgical Gauze) | 47 | F | F | F | F | P | P | P | F | F | no |
| DS165 | Surgical Instrument Multi-Domain Segmentation | 42 | F | F | F | F | U | P | P | F | F | yes |
| DS166 | Surgical Instrument Multi-Domain Segmentation Challenge | 42 | F | F | F | F | U | P | P | F | F | yes |
| DS167 | SurgRIPE | 32 | F | F | F | F | U | P | U | F | F | yes |
| DS168 | SurgT (Surgical Tracking, EndoVis 2022) | 20 | F | F | F | F | P | U | P | F | F | unknown |
| DS169 | SurgToolLoc 2022 / SurgToolLoc 2023 | — | F | F | F | F | U | P | U | F | U | no |
| DS170 | SurgVisDom (Surgical Visual Domain Adaptation, EndoVis 2020) | — | F | F | F | F | P | P | U | F | U | yes |
| DS171 | SurgVU24 / SurgVU25 / SurgVU26 (Surgical Visual Understandin | 155 | F | F | P | F | U | P | P | F | F | no |
| DS172 | TrackVes | 9 | F | F | U | F | U | U | U | F | F | yes |
| DS173 | Trauma THOMPSON (2023, 2025 challenges; Trauma THOMPSON Data | 220 | P | U | P | U | P | P | P | F | P | yes |
| DS174 | Synthetic and Real Inputs for Tool Segmentation in Robotic S | 20 | F | F | F | F | P | U | P | F | F | no |
| DS175 | Learning laparoscopic video shot classification for gynecolo | 111 | F | F | F | F | F | U | P | F | F | unknown |
| DS176 | Automated tool detection with deep learning for monitoring k | 20 | F | U | F | F | U | U | U | F | F | unknown |
| DS177 | Towards Unified Surgical Skill Assessment (clinical laparosc | 20 | F | P | P | F | U | U | P | F | F | unknown |
| DS178 | A surgical dataset from the da Vinci Research Kit for task a | 206 | P | P | P | F | P | P | P | F | P | no |
| DS179 | Real-Time Segmentation and Recognition of Surgical Tasks in  | 186 | F | U | P | U | U | U | P | F | F | unknown |
| DS180 | Vision-based approaches for surgical activity recognition us | 208 | F | F | P | U | U | U | F | F | P | unknown |
| DS181 | Artificial intelligence-driven phase recognition in lung sur | 8 | F | F | F | F | P | P | U | F | F | no |
| DS182 | Closing the data gap - leveraging pretrained neural networks | 15 | F | F | U | F | U | P | P | F | F | yes |
| DS183 | Dataset and trained models for video denoising in fluorescen | — | F | F | F | F | P | P | F | F | U | no |
| DS184 | Exploring video recognition models for force estimation in s | 50 | F | P | P | F | P | P | P | F | F | no |
| DS185 | Video based Action Recognition and Skills Assessment - Porci | 130 | F | F | F | F | U | P | P | F | F | yes |
| DS001 | Open-H Surgical/cmr_surgical/cholecystectomy (cholecystectom | 99 | F | F | U | F | P | P | P | F | F | no |
| DS002 | Open-H Surgical/cmr_surgical/dry_box (dry box) | — | U | F | U | F | P | P | P | F | U | no |
| DS003 | Open-H Surgical/cmr_surgical/hysterectomy (hysterectomy) | 100 | F | F | U | F | P | P | P | F | F | no |
| DS004 | Open-H Surgical/cmr_surgical/inguinal_hernia (inguinal herni | 100 | F | F | U | F | P | P | P | F | F | no |
| DS005 | Open-H Surgical/cmr_surgical/peg_transfer (peg transfer) | — | U | P | U | F | P | P | P | F | U | no |
| DS006 | Open-H Surgical/cmr_surgical/prostatectomy (prostatectomy) | 100 | F | F | U | F | P | P | P | F | F | no |
| DS007 | Open-H Surgical/hamlyn/knot_tying (Hamlyn dVRK knot tying) | 49 | F | F | U | F | P | P | P | F | F | no |
| DS008 | Open-H Surgical/hamlyn/needle_grasp_and_handover (Hamlyn dVR | 137 | F | P | P | F | P | P | P | F | F | no |
| DS009 | Open-H Surgical/hamlyn/peg_transfer (Hamlyn dVRK peg transfe | 317 | P | P | P | F | P | P | P | F | P | no |
| DS010 | Open-H Surgical/hamlyn/suturing_1 (Hamlyn dVRK suturing sing | 180 | F | P | P | F | P | P | P | F | F | no |
| DS011 | Open-H Surgical/hamlyn/suturing_2 (Hamlyn dVRK suturing dual | 186 | F | P | P | F | P | P | P | F | F | no |
| DS012 | Open-H Surgical/hamlyn/tissue_lifting (Hamlyn dVRK tissue li | 75 | F | P | P | F | P | P | P | F | F | no |
| DS013 | Open-H Surgical/hamlyn/tissue_retraction (Hamlyn dVRK tissue | 75 | F | P | P | F | P | P | P | F | F | no |
| DS014 | Open-H Surgical/jhu/imerse/cao_cautery_combined (CAO cautery | — | U | F | U | F | P | P | P | F | U | no |
| DS015 | Open-H Surgical/jhu/imerse/nephfat/nephfat (NephFat perineph | — | U | F | U | F | P | P | P | F | U | no |
| DS016 | Open-H Surgical/jhu/imerse/srt_needle_pickup_handover (SRT n | 240 | P | F | P | F | P | P | P | F | P | no |
| DS017 | Open-H Surgical/jhu/imerse/srt_tissue_lift (SRT tissue lift) | 225 | P | F | P | F | P | P | P | F | P | no |
| DS018 | Open-H Surgical/jhu/imerse/srth_porcine_chole (SRT-H porcine | — | U | F | U | F | P | P | P | F | U | no |
| DS019 | Open-H Surgical/jhu/imerse/star_il/star_il (STAR_IL anastomo | — | U | F | U | F | P | P | P | F | U | no |
| DS020 | Open-H Surgical/jhu/imerse/suturebot (SutureBot suturing sub | — | U | F | U | F | P | P | P | F | U | no |
| DS021 | Open-H Surgical/jhu/imerse/wound_closure/point_labeled/faust | 216 | P | F | P | F | P | P | P | F | P | no |
| DS022 | Open-H Surgical/jhu/lcsr/arcade (JHU ARCADE: cholecystectomy | — | U | F | U | F | P | P | P | F | U | no |
| DS023 | Open-H Surgical/jhu/lcsr/miracle (JHU MIRACLE needle pick-up | 4 | F | F | P | F | P | P | P | F | F | no |
| DS024 | Open-H Surgical/jhu/lcsr/smarts (JHU LCSR SMARTS / SurgSyncE | 236 | F | P | P | P | P | P | P | P | F | no |
| DS025 | Open-H Surgical/moon_surgical/moon_laparoscopic_assistant (M | 65 | F | F | P | F | P | P | U | F | F | no |
| DS026 | Open-H Surgical/obuda/frs_dome_1 (Obuda dVRK FRS dome knot t | 102 | F | P | P | F | P | P | P | F | F | no |
| DS027 | Open-H Surgical/obuda/needlethreading_1 (Obuda dVRK needle t | 196 | F | P | P | F | P | P | P | F | F | no |
| DS028 | Open-H Surgical/obuda/needlethreading_2 (Obuda dVRK needle t | 204 | P | P | P | F | P | P | P | F | P | no |
| DS029 | Open-H Surgical/obuda/pegtransfer_1 (Obuda dVRK peg transfer | 216 | P | P | P | F | P | P | P | F | P | no |
| DS030 | Open-H Surgical/obuda/pegtransfer_2 (Obuda dVRK peg transfer | 184 | F | P | P | F | P | P | P | F | F | no |
| DS031 | Open-H Surgical/obuda/pork_1 (Obuda dVRK pork shoulder tissu | 318 | P | P | P | F | P | P | P | F | P | no |
| DS032 | Open-H Surgical/obuda/rollercoaster_1 (Obuda dVRK rollercoas | 95 | F | P | P | F | P | P | P | F | F | no |
| DS033 | Open-H Surgical/obuda/seaspike_1 (Obuda dVRK seaspike 1) | 207 | P | P | P | F | P | P | P | F | P | no |
| DS034 | Open-H Surgical/obuda/seaspike_2 (Obuda dVRK seaspike 2) | 153 | F | P | P | F | P | P | P | F | F | no |
| DS035 | Open-H Surgical/obuda/seaspike_3 (Obuda dVRK seaspike 3) | 219 | P | P | P | F | P | P | P | F | P | no |
| DS036 | Open-H Surgical/obuda/skinphantom_1 (Obuda dVRK skin-phantom | — | U | P | U | F | P | P | P | F | U | no |
| DS037 | Open-H Surgical/polyu/openh_dataset_full (PolyU simulated ga | 11520 | F | F | P | F | P | P | P | F | P | no |
| DS038 | Open-H Surgical/rob_surgical/all_merged_data (Rob Surgical B | 6 | F | F | U | F | P | P | P | F | F | no |
| DS039 | Open-H Surgical/sanoscience/sanoscience_v1_2_merged/expert_d | — | U | U | F | F | P | P | P | F | U | no |
| DS040 | Open-H Surgical/sanoscience/sanoscience_v1_2_merged/nonexper | — | U | U | F | F | P | P | P | F | U | no |
| DS041 | Open-H Surgical/sanoscience/sanoscience_v1_2_merged/nonexper | — | U | U | F | F | P | P | P | F | U | no |
| DS042 | Open-H Surgical/sanoscience/sanoscience_v1_2_merged/nonexper | — | U | U | F | F | P | P | P | F | U | no |
| DS043 | Open-H Surgical/sanoscience/sanoscience_v1_2_merged/nonexper | 7 | F | F | F | F | P | P | P | F | F | no |
| DS044 | Open-H Surgical/sanoscience/sanoscience_v1_2_merged/nonexper | 89 | F | F | F | F | P | P | P | F | F | no |
| DS045 | Open-H Surgical/semaphor/open_h_semaphor | 533 | U | F | U | F | P | P | U | F | U | no |
| DS046 | Open-H Surgical/stanford/collaborative_haptics_and_robotics_ | 700 | P | P | P | F | P | P | P | F | P | no |
| DS047 | Open-H Surgical/stanford/collaborative_haptics_and_robotics_ | 598 | P | P | P | F | P | P | P | F | P | no |
| DS048 | Open-H Surgical/stanford/collaborative_haptics_and_robotics_ | 698 | P | F | P | F | P | P | P | F | P | no |
| DS049 | Open-H Surgical/stanford/collaborative_haptics_and_robotics_ | 500 | P | F | P | F | P | P | P | F | P | no |
| DS050 | Open-H Surgical/stanford/collaborative_haptics_and_robotics_ | 500 | P | F | P | F | P | P | P | F | P | no |
| DS051 | Open-H Surgical/tud/260131_tundra_dataset/endoscope_guidance | 50 | F | P | P | F | P | P | P | F | F | no |
| DS052 | Open-H Surgical/tud/260131_tundra_dataset/grasping_retractio | 146 | F | P | P | F | P | P | P | F | F | no |
| DS053 | Open-H Surgical/turin/mitic_lerobot_ex_vivo | 799 | P | P | P | F | P | P | P | F | P | no |
| DS054 | Open-H Surgical/turin/mitic_lerobot_plastic_pad | 550 | P | P | P | F | P | P | P | F | P | no |
| DS055 | Open-H Surgical/turin/mitic_lerobot_plastic_pad_3dmed | 370 | P | P | P | F | P | P | P | F | P | no |
| DS056 | Open-H Surgical/turin/mitic_lerobot_plastic_tube | 480 | P | P | P | F | P | P | P | F | P | no |
| DS057 | Open-H Surgical/ubc/gauzecutting_merged | — | U | F | F | F | P | P | F | F | U | no |
| DS058 | Open-H Surgical/ubc/knottying_merged | — | U | F | F | F | P | P | F | F | U | no |
| DS059 | Open-H Surgical/ubc/needlepassing_merged | — | U | F | F | F | P | P | F | F | U | no |
| DS060 | Open-H Surgical/ubc/pegtransfering_merged | — | U | F | F | F | P | P | F | F | U | no |
| DS061 | Open-H Surgical/ubc/pickandplace_merged | — | U | F | F | F | P | P | F | F | U | no |
| DS062 | Open-H Surgical/ubc/suturing_merged | — | U | F | F | F | P | P | F | F | U | no |
| DS063 | Open-H Surgical/ubc/wirechasing3d_merged | — | U | F | F | F | P | P | F | F | U | no |
| DS064 | Open-H Surgical/ubc/wirechasing_merged | — | U | F | F | F | P | P | F | F | U | no |
| DS065 | Open-H Surgical/ucberkeley/debridement_lerobot | 589 | P | F | P | F | P | P | P | F | P | no |
| DS066 | Open-H Surgical/ucsd/surgical_learning_dataset | 912 | P | P | P | F | P | P | P | F | P | no |
| DS067 | Open-H Surgical/ucsd/surgical_learning_dataset2 | 200 | P | F | P | F | P | P | P | F | P | no |
| DS068 | Open-H Surgical/ucsd/surgical_learning_retraction_dataset3 | 598 | P | P | P | F | P | P | P | F | P | no |
| DS069 | Open-H Surgical/ucsd/surgical_learning_retraction_failurecas | 299 | P | P | P | F | P | P | P | F | P | no |
| DS070 | Open-H Surgical/uic/uic_crcd_lerobot | 18 | F | F | P | F | P | P | P | F | F | no |
| DS071 | Open-H Surgical/utenn/benchtop_datasets_round2_with_part_seg | 2 | F | F | F | F | P | P | U | F | F | no |
| DS072 | Open-H Surgical/utenn/surgical_video_datasets | — | F | F | F | F | P | P | F | F | F | no |
| DS073 | Open-H Surgical/utenn/surgical_video_datasets_round2_with_pa | — | F | F | F | F | P | P | U | F | F | no |
| DS074 | Open-H Surgical/utenn/surgical_video_datasets_with_tip_pose | — | F | F | F | F | P | P | P | F | F | no |
| DS075 | Open-H Surgical/virtual_incision/150_episodes_mira_needle_li | 150 | F | F | P | F | P | P | P | F | F | no |
| DS186 | Open-H Endoscopy/cuhk/openh_dataset_full/find_greater_curvat | 462 | P | P | P | F | P | P | P | F | P | no |
| DS187 | Open-H Endoscopy/cuhk/openh_dataset_full/find_lesser_curvatu | 200 | P | P | P | F | P | P | P | F | P | no |
| DS188 | Open-H Endoscopy/cuhk/openh_dataset_full/find_pyloric_antrum | 204 | P | P | P | F | P | P | P | F | P | no |
| DS189 | Open-H Endoscopy/cuhk/openh_dataset_full/track_orange_lesion | 156 | F | P | P | F | P | P | P | F | F | no |
| DS190 | Open-H Endoscopy/cuhk/openh_dataset_full/track_small_round_n | 722 | P | P | P | F | P | P | P | F | P | no |
| DS191 | Open-H Endoscopy/cuhk/openh_dataset_full/track_white_oval_ro | 414 | P | P | P | F | P | P | P | F | P | no |
| DS192 | Open-H Endoscopy/jhu/imerse/endosrt/endosrt | 1060 | P | P | P | F | P | P | U | F | P | no |
| DS193 | Open-H Endoscopy/ut_austin/arts_lab/colonoscope_lerobot | 1894 | P | P | P | F | P | P | P | F | P | no |
