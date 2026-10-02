# DS203 D8 Computation Spec (Decision 002; committed before any duration is read)

It implements gate §2 D8 exactly as frozen, for DS203 only. It adds only mechanics the gate and Decision 002 leave
open.

## 1. Source

* **Archive:** the Appendix300 full-video split archive on TU Dresden OPARA (doi 10.25532/OPARA-1173):
  `Appendix300_Full_Videos.z01`–`.z05` plus `.zip`.
* **Steps:**
  1. Read the zip central directory (end of the `.zip` part) by HTTP range request.
  2. For each mp4 entry, read its local header.
  3. Walk the MP4 top-level box headers. Read only the `moov` box.
* **Taken from `moov`:**
  * duration: `mvhd` timescale and duration;
  * video-track frame count: `stsz` / `stz2` sample count of the track whose `hdlr` is `vide`;
  * frame rate: frame count / (video track `mdhd` duration / timescale).
* **Bytes read:** nothing beyond box headers and `moov`. No `mdat` byte is read, no frame is decoded, and no pixel is
  computed.
* **Entries:** stored entries (method 0) are read in place. If any needed entry is compressed, or `moov` is
  unreachable by range requests: **STOP and report**, without estimating.
* **Output:** raw box data (`moov` only) is kept on LaCie; per-file results go to
  `data_audit/lead/out/DS203_container_probe.csv`.

## 2. Trajectories and variables

* **Trajectory:** one case (`Center`, `OP`), all of its full-video files in version order (`_v01`, `_v02`, …).
* **Counted trajectories (primary):** the 279 cases of centres 2–5, i.e. the D3-passing set of `27136df` (centre 1
  "provided representative 5-minute clips for the majority of cases").
* **Descriptive only (not gating):** the strict 227 single-file cases, and all 330 cases.
* **Acquisition factor:** site = `Center`, all recorded levels among the counted trajectories.
* **Content variable (categorical, used as is):** appendix-visible state:
  * 0 for frames before the annotated `Timestamp` in the file named in the `Video` column, and for all frames of
    earlier files of the case;
  * 1 for frames at or after it, and for all frames of later files.
  * Frames before the timestamp in that file = round(timestamp_seconds × that file's frame rate).
* **Weights:** each frame has weight 1 / (frames in its trajectory), so each trajectory sums to 1. Weighted counts are
  summed per (site, state).
* **Cramér's V:** φ² = Σ (P_ij − P_i· P_·j)² / (P_i· P_·j) on the weighted proportion table;
  V = sqrt(φ² / (min(r, c) − 1)).
* **D8:** PASS if V ≤ 0.5.

## 3. Checks reported

* the number of files probed and of cases with all files probed;
* any timestamp later than its file's duration (flagged; such a case is excluded and listed, not repaired);
* frame rates (distribution);
* total frames.
