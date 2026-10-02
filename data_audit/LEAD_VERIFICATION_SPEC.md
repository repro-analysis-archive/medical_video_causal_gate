# Lead Verification and D8 Computation Spec (committed before any parquet or annotation value is read)

Gate `baadf5c`, §2, §4 and §5. This file fixes how the lead analyst verifies the audit agents' eligibility-deciding
verdicts and computes D8 / the §4 cross-tabulation. It adds operational definitions only where the gate leaves a term
open, and says so. Nothing here relaxes a criterion.

## 1. Scope

* **Lead verification.** Every dataset that an audit output (`audits/A_*_audit.json`) reports as SS-eligible pending
  D8, or as RA-eligible. At the time of writing that is **DS024** (Open-H `Surgical/jhu/lcsr/smarts`, SurgSyncExt
  SMARTS), with 4 of 8 batches returned. Datasets from the remaining batches are handled by the same rules.
* **§4 cross-tabulation and Cramér's V.** Every dataset with D4 PASS **and** D7 PASS, whether or not it is eligible.
  The gate requires V "for each eligible pair". At the time of writing: DS024 and DS113 (Cataract-101).

## 2. Files (no video)

* **DS024:**
  * the 2,509 episode parquet files (kinematics, robot state, ROS timestamps; 0.435 GB) at Open-H revision
    `e29dda7cabf2a2626634c7822db27695553ae523`;
  * downloaded to `/media/user/LaCie/medvideo_gate/DS024/parquet/` (not the H1R disk);
  * **no mp4 is downloaded.**
  * **Why these files are allowed.** The parquet files are the dataset's sensor-annotation files. They hold the D7
    variable (PSM kinematics, "sensor ground truth of scene state") and the timestamps that D3 depends on. Gate §4
    requires the cross-tabulation "from metadata and annotation files only".
* **DS113:** `videos.csv` and `annotations.csv`, already saved by the audit agent under
  `/media/user/LaCie/medvideo_gate/DS113/zip_members/`.
* **No video frame** is decoded, and no representation or model of any kind is computed.

## 3. DS024: unit and D3 verification (operational definition of "contiguous", fixed now)

* **Unit.** A trajectory is a case, keyed by (leaf directory, `case_id`), with its episodes ordered by
  `episode_index`. This is the audit's unit: one full task execution, whose consecutive subtask episodes count once.
* **Real time** of a frame: `observation.meta.ros_time_sec + 1e-9 * observation.meta.ros_time_nsec`.
* **Gap.** Within a case, consecutive frames are taken in (`episode_index`, row order). A gap is the real-time
  difference between consecutive frames, **including across episode boundaries**.
* **Contiguous case.** A case is contiguous if both:
  * (a) its largest gap is **≤ 1.0 s**;
  * (b) it has no real-time decrease larger than 0.001 s.
* **Why 1.0 s.** The gate says "time-aligned and contiguous, not isolated clips" but gives no tolerance.
  * 1.0 s is 4× the documented online-recorder mean interval (1 / 4.04 Hz ≈ 0.25 s) and 10× the offline interval
    (0.1 s).
  * A one-second stretch with no frame is treated as a break in the recording.
  * This threshold is the gating value. The gap distribution, and the counts at 0.5, 2 and 5 s, are reported
    descriptively only.
* **Time-aligned.** Read as: every frame carries a real timestamp on a clock shared with the other recorded streams.
  * The recorder documents this: SurgSync, with NTP-synchronised ROS and a time tolerance per online frame.
  * It is confirmed if every frame has a non-missing ROS time.
  * The README's single manual video–kinematic delay measurements (+200 to +1200 ms, one per leaf) are reported to the
    investigator. They do not gate, because the README itself says they include physical response time and do not
    establish alignment per episode.
* **Consequence.**
  * Only contiguous cases count as D3 trajectories.
  * The ≥200 count, the D4 qualifying levels and the D1 count are recomputed on contiguous cases only.
  * If fewer than 200 cases are contiguous, DS024 fails ≥200 (SS arm) and D1 (RA arm).

## 4. D8 and §4 cross-tabulation (gate §2 D8, applied as written)

* **Weights.** Every frame of a trajectory gets weight 1 / (number of frames of that trajectory), so each trajectory
  sums to 1.
* **Acquisition factor.** Every factor graded D4 PASS, with **all recorded levels** of that factor among the counted
  trajectories:
  * DS024: operator (`user_id`);
  * DS113: surgeon (`Surgeon` in `videos.csv`).
  * As a descriptive, non-gating table, the same V is also given restricted to levels with ≥ 20 trajectories.
* **Content variables** (those graded D7 PASS in the audit outputs):
  * **DS024:** eight continuous variables, binned at their pooled weighted quartiles:
    * `observation.cartesian_state.psm1.pose.position.{x,y,z}`;
    * `observation.cartesian_state.psm2.pose.position.{x,y,z}`;
    * `observation.state.psm1.gripper`;
    * `observation.state.psm2.gripper`.

    `instruction_text` is **not** used: the audit could not establish that it is a human annotation (D7 not shown).
  * **DS113:** surgical phase per frame, from `annotations.csv` (the phase in force at each frame, frames counted as in
    `videos.csv`), categorical, used as is.
* **Cramér's V** on the weighted table P (proportions):
  * φ² = Σ (P_ij − P_i· P_·j)² / (P_i· P_·j);
  * V = sqrt(φ² / (min(r, c) − 1)).

  Frames with a missing content value are dropped before the weights are formed, and the dropped count is reported.
* **D8 PASS** if at least one (D4 factor, D7 variable) pair has V ≤ 0.5 (gate §2). Every V is reported.

## 5. Then §5, mechanically

* Apply gate §5 to the verified verdicts: SS arm, then RA arm.
* Ranking keys:
  * qualifying levels;
  * then total trajectories;
  * then D7 annotation density (the fraction of frames with a non-missing D7 value);
  * then access without registration.
* A remaining tie goes to human decision. None passes: SS → STOP for human decision; RA → deferred.
* **No criterion is relaxed.** Any UNKNOWN on a required criterion means not passing.
