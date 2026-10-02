# SS' Arm Result (Amendment 1 with Amendment 2; Decision 001; spec `957aa25`)

Applied once, mechanically, after the Semantic Scholar arms of gate §6 and §3 had run (`8f8f163`).

**Selected dataset: DS203, Appendix300**, the only dataset passing the SS' arm.
* A multi-centre laparoscopic appendectomy video dataset with patient metadata.
* TU Dresden OPARA, doi 10.25532/OPARA-1173.
* Data descriptor: Sci Data 2026, 13:886.
* **Two lead adjudications (§4) and one open question about Amendment 1's premise (§5) need the investigator's
  review.**

## 1. Pool

* **230 datasets:**
  * the 194 of the `dd142f6` audit log (`DATA_AUDIT_TABLE.csv`, DS024 after lead verification);
  * plus the 36 new C-COL / C-SURG datasets found by the Semantic Scholar dataset arm (DS194–DS229, audits
    `A_s2a`–`A_s2d`).
* No video was downloaded, no computation on video was done, and no representation was extracted.

## 2. v4 part: D3, D5, D6, D7 and ≥200 trajectories all PASS

34 of 230 datasets pass (`lead/out/ss_prime_v4part.json`).

## 3. Amendment 2: in vivo human patients, clinical procedures (judged for the 34 only)

| id | name | n | Amendment 2 | quote | source |
|---|---|---|---|---|---|
| DS000 | CathAction | 569 | FAIL | "two distinct sources: i) utilizing vascular soft silicone phantoms modeled after the human body and ii) employing animal subjects, specifically pigs" | arXiv:2408.13126 §III.A p. 3 (Erratum 003) |
| DS173 | Trauma THOMPSON (2023, 2025 challenges; Trauma THOMPSON Datase | 220 | FAIL | "performing simulated medical procedures"; "Filming was conducted across various simulation models and environments" | Sci Data 2025, PMC12815934, Methods (Erratum 004) |
| DS178 | A surgical dataset from the da Vinci Research Kit for task aut | 206 | FAIL | "three tasks of the Skill Building Task Set … These training platforms for clinical skill development" | ROSMA, arXiv:2102.03643 p. 2 |
| DS009 | Open-H Surgical/hamlyn/peg_transfer (Hamlyn dVRK peg transfer) | 317 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS009/README.md (Open-H rev e29dda7c) |
| DS016 | Open-H Surgical/jhu/imerse/srt_needle_pickup_handover (SRT nee | 240 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS016/README.md (Open-H rev e29dda7c) |
| DS017 | Open-H Surgical/jhu/imerse/srt_tissue_lift (SRT tissue lift) | 225 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS017/README.md (Open-H rev e29dda7c) |
| DS021 | Open-H Surgical/jhu/imerse/wound_closure/point_labeled/fausto_ | 216 | FAIL | README Data Type: Ex-Vivo (checked) | /media/user/LaCie/medvideo_gate/DS021/README.md (Open-H rev e29dda7c) |
| DS028 | Open-H Surgical/obuda/needlethreading_2 (Obuda dVRK needle thr | 204 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS028/README.md (Open-H rev e29dda7c) |
| DS029 | Open-H Surgical/obuda/pegtransfer_1 (Obuda dVRK peg transfer 1 | 216 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS029/README.md (Open-H rev e29dda7c) |
| DS031 | Open-H Surgical/obuda/pork_1 (Obuda dVRK pork shoulder tissue  | 318 | FAIL | README Data Type: Ex-Vivo (checked) | /media/user/LaCie/medvideo_gate/DS031/README.md (Open-H rev e29dda7c) |
| DS033 | Open-H Surgical/obuda/seaspike_1 (Obuda dVRK seaspike 1) | 207 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS033/README.md (Open-H rev e29dda7c) |
| DS035 | Open-H Surgical/obuda/seaspike_3 (Obuda dVRK seaspike 3) | 219 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS035/README.md (Open-H rev e29dda7c) |
| DS037 | Open-H Surgical/polyu/openh_dataset_full (PolyU simulated gall | 11520 | FAIL | README Data Type: Digital Simulation (checked) | /media/user/LaCie/medvideo_gate/DS037/README.md (Open-H rev e29dda7c) |
| DS046 | Open-H Surgical/stanford/collaborative_haptics_and_robotics_in | 700 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS046/README.md (Open-H rev e29dda7c) |
| DS047 | Open-H Surgical/stanford/collaborative_haptics_and_robotics_in | 598 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS047/README.md (Open-H rev e29dda7c) |
| DS048 | Open-H Surgical/stanford/collaborative_haptics_and_robotics_in | 698 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS048/README.md (Open-H rev e29dda7c) |
| DS049 | Open-H Surgical/stanford/collaborative_haptics_and_robotics_in | 500 | FAIL | README Data Type: Digital Simulation (checked) | /media/user/LaCie/medvideo_gate/DS049/README.md (Open-H rev e29dda7c) |
| DS050 | Open-H Surgical/stanford/collaborative_haptics_and_robotics_in | 500 | FAIL | README Data Type: Digital Simulation (checked) | /media/user/LaCie/medvideo_gate/DS050/README.md (Open-H rev e29dda7c) |
| DS053 | Open-H Surgical/turin/mitic_lerobot_ex_vivo | 799 | FAIL | README Data Type: Ex-Vivo (checked) | /media/user/LaCie/medvideo_gate/DS053/README.md (Open-H rev e29dda7c) |
| DS054 | Open-H Surgical/turin/mitic_lerobot_plastic_pad | 550 | FAIL | README Data Type: Ex-Vivo (checked) | /media/user/LaCie/medvideo_gate/DS054/README.md (Open-H rev e29dda7c) |
| DS055 | Open-H Surgical/turin/mitic_lerobot_plastic_pad_3dmed | 370 | FAIL | README Data Type: Ex-Vivo (checked) | /media/user/LaCie/medvideo_gate/DS055/README.md (Open-H rev e29dda7c) |
| DS056 | Open-H Surgical/turin/mitic_lerobot_plastic_tube | 480 | FAIL | README Data Type: Ex-Vivo (checked) | /media/user/LaCie/medvideo_gate/DS056/README.md (Open-H rev e29dda7c) |
| DS065 | Open-H Surgical/ucberkeley/debridement_lerobot | 589 | FAIL | README Data Type: Ex-Vivo (checked) | /media/user/LaCie/medvideo_gate/DS065/README.md (Open-H rev e29dda7c) |
| DS066 | Open-H Surgical/ucsd/surgical_learning_dataset | 912 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS066/README.md (Open-H rev e29dda7c) |
| DS067 | Open-H Surgical/ucsd/surgical_learning_dataset2 | 200 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS067/README.md (Open-H rev e29dda7c) |
| DS068 | Open-H Surgical/ucsd/surgical_learning_retraction_dataset3 | 598 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS068/README.md (Open-H rev e29dda7c) |
| DS069 | Open-H Surgical/ucsd/surgical_learning_retraction_failurecase | 299 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS069/README.md (Open-H rev e29dda7c) |
| DS186 | Open-H Endoscopy/cuhk/openh_dataset_full/find_greater_curvatur | 462 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS186/README.md (Open-H rev e29dda7c) |
| DS187 | Open-H Endoscopy/cuhk/openh_dataset_full/find_lesser_curvature | 200 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS187/README.md (Open-H rev e29dda7c) |
| DS188 | Open-H Endoscopy/cuhk/openh_dataset_full/find_pyloric_antrum | 204 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS188/README.md (Open-H rev e29dda7c) |
| DS190 | Open-H Endoscopy/cuhk/openh_dataset_full/track_small_round_nod | 722 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS190/README.md (Open-H rev e29dda7c) |
| DS191 | Open-H Endoscopy/cuhk/openh_dataset_full/track_white_oval_roi | 414 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS191/README.md (Open-H rev e29dda7c) |
| DS193 | Open-H Endoscopy/ut_austin/arts_lab/colonoscope_lerobot | 1894 | FAIL | README Data Type: Table-Top Phantom (checked) | /media/user/LaCie/medvideo_gate/DS193/README.md (Open-H rev e29dda7c) |
| DS203 | Appendix300 (laparoscopic appendectomy video + patient metadat | 330 | PASS | "330 laparoscopic surgery recordings, including 325 full-length laparoscopic appendectomies and 5 control recordings from non-appendectomy procedures in pediatric and adult patients treated at five German centers" | Sci Data 2026 13:886 (doi 10.1038/s41597-026-07593-6) p. 1; Ethics Statement p. 4 |

**1 of 34 passes: DS203.**

## 4. DS203: verification and lead adjudications

| criterion | verdict | evidence |
|---|---|---|
| D3 | **PASS for the full-length recordings** | "325 full-length laparoscopic appendectomies" (descriptor p. 1). The descriptor describes "the uncut, re-encoded, individual video files in their correct order". Caveat: "All extracorporeal sequences have been removed", which is the same caveat as AutoLaparo / EgoSurgery in the v4 audit. **Centre 1 is excluded from the count**: "Center 1 provided representative 5-minute clips for the majority of cases" (p. 5). Its full-video files are 26–445 MB except one, against about 1–1.7 GB elsewhere |
| ≥ 200 | **PASS** | **279** cases in centres 2–5 (49 + 42 + 71 + 117; `overall_merged.csv`). Under the strictest reading, which also excludes the 52 cases in centres 2–5 that are split across consecutive source files (`_v01`, `_v02`, …), **227**. ≥ 200 holds either way |
| D5 | PASS | "License: CC BY 4.0" (`readme_Appendix300.md`; OPARA licence file). Open download, no registration |
| D6 | PASS | 1,692,471,368,687 bytes = 1.69 TB ≤ 2.02 TB: the sum of the 11 OPARA ORIGINAL bitstreams (full videos 1.36 TB, images 0.25 TB, snippets 0.08 TB) |
| D7 | **PASS: lead adjudication** | The per-case human annotation is the "Timestamps at which the appendix is fully visible prior to invasive preparation" (README §3.2 Metadata Variables; `Timestamp` column, present for 330 / 330). It defines a two-segment, within-video content variable (before / after full appendix exposure). **The audit agents disagreed** on the same data: A_s2b (DS203) PASS "weak"; A_s2c (DS213, which uses this data) FAIL, calling it "not an annotation variable". The lead applies the v4 precedent: Cataract-101's phases, accepted as D7 PASS, are likewise defined only by human-annotated start frames. A single human-annotated boundary is the same kind of variable, with one boundary. **Weak:** two segments per trajectory. If the investigator rules D7 FAIL here, SS' has no passing dataset → STOP |
| Amendment 2 | PASS | §3 |

* **Data discrepancies recorded.**
  * The CSV flags 18 rows "Appendix recording from non-appendectomy laparoscopic surgery", against 5 controls in the
    descriptor.
  * Centre 5 has 117 rows, against 118 in descriptor Table 1.
* **DS213** (the swarm-learning cohort, 397 recordings) is Appendix300 plus an unreleased 67-recording external cohort.
  It fails the v4 part (D5, D6 UNKNOWN; D7 FAIL by A_s2c) and adds no trajectories.

## 5. Open question for the investigator: does DS203 pass the original v4 SS arm?

* **What DS203 has under v4.** It also has **D4 PASS**: site recorded per case (`Center`), with 4 qualifying levels in
  centres 2–5 (49 / 42 / 71 / 117).
* **D8 is UNKNOWN.** The trajectory-weighted cross-tabulation of site × the before / after segment needs each video's
  duration. The duration is not in the metadata files; it is available only from the video containers of all 330
  cases, and §7 allows container metadata of one sample video only.
* **Formal status.** UNKNOWN is not PASS, so no dataset passes the v4 SS arm, and the premise of Amendment 1's trigger
  still holds.
* **If D8 were computed and passed**, DS203 would pass v4 SS, and Amendment 1 says it is then "void".
* **This is not resolved here; it is a human decision.** The options include:
  * authorizing container-metadata reads (durations) for all DS203 videos;
  * obtaining durations from the authors;
  * keeping SS' as decided in Decision 001.

## 6. Ranking (Amendment 1), applied once

| rank | dataset | total trajectories | D7 annotation density | access without registration |
|---|---|---|---|---|
| 1 | **DS203 Appendix300** | 279 (strict 227) | 1 human boundary per trajectory (2 segments) | yes (open, CC BY 4.0) |

* One dataset passes, so no tie-break is needed.
* **Selected: DS203.**

## 7. Not done (outside this application)

* **Encoding check:** the Amendment 1 encoding check is not run. It needs a representation, which needs a protocol.
* **No video work:** no video was downloaded, no frame was decoded, and no representation was extracted.
* **Claim ceiling (Amendment 1).** Results concern acquisition-like information introduced by known transforms. DS203's
  real per-case site labels may be analysed descriptively as a sanity check only, never as a primary result.
