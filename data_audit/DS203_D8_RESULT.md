# DS203 (Appendix300) D8 Result (Decision 002, spec `cdbbc6e`)

**D8 PASS. Cramér's V = 0.155** (≤ 0.5): site × appendix-visible state, on 278 counted trajectories.

**Branch taken (pre-fixed in Decision 002):** DS203 D8 PASS, so it passes the original v4 SS arm (with Amendment 2).
* **Amendment 1 is VOID.**
* The SS arm with the **real site factor** applies to DS203.
* The SS' selection of `27136df` is superseded by this branch. The dataset is the same (DS203); the arm is now v4 SS,
  not SS'.

## 1. Container probe (Decision 002 §4; `lead/probe_ds203_containers.py`)

* **Archive:** the OPARA split zip `Appendix300_Full_Videos.z01`–`.z05` + `.zip` (doi 10.25532/OPARA-1173), read by
  HTTP range requests (server returns 206).
* **Entries:** the zip64 central directory has 739 entries, of which **403 are full-video mp4s, all stored (method 0)**.
* **What was read per file:** its local header, the MP4 top-level box headers (`ftyp`, `free`, `mdat`, `moov`; `moov`
  comes after `mdat`) and **the `moov` box only**.
* **Totals:** 403 of 403 files probed in 2,016 requests, 213.9 MB read. That is the `moov` boxes (about
  0.6 MB each) plus headers.
* **Not done:** **no `mdat` byte read, no frame decoded, no pixel computed.**
* **Stored:** `moov` boxes on LaCie (`DS203/moov/`); per-file results in `lead/out/DS203_container_probe.json`.
* **Values per file:**
  * duration = video-track `mdhd` duration / timescale;
  * frames = `stsz` sample count;
  * fps = frames / duration.

  Frame rates: 50.0 fps × 227, 25.0 fps × 124, and a few at about 29.3–29.95 fps.
* **Coverage:** 330 of 330 cases have all their files probed.

## 2. D8 computation (exactly as frozen; `lead/d8_ds203.py`)

* **Factor:** site = `Center`, all levels among the counted trajectories.
* **Content:** appendix-visible state.
  * 0 before the annotated `Timestamp` in the file named by `Video`, and for earlier files of the case;
  * 1 from it onwards, and for later files.
* **Weights:** frame weight 1 / frames in its trajectory, so each trajectory sums to 1.
* **Counted trajectories:** centres 2–5, the D3-passing set of `27136df`: 279 cases.
  * **1 excluded by the spec's check:** case Center 3 OP 20, whose timestamp (304.1 s) is later than the duration of
    `Center3_020.mp4` (255.8 s). It is listed, not repaired.
  * That leaves **278**, still ≥ 200.
  * D4 still holds: 4 site levels, each with ≥ 20 trajectories (49 / 41 / 71 / 117).

| site | trajectories | weighted "before" | weighted "after" | mean fraction before |
|---|---|---|---|---|
| 2 | 49 | 13.633 | 35.367 | 0.278 |
| 3 | 41 | 11.059 | 29.941 | 0.270 |
| 4 | 71 | 19.126 | 51.874 | 0.269 |
| 5 | 117 | 16.742 | 100.258 | 0.143 |

Total frames in the counted trajectories: 22,008,906.

| set | trajectories | Cramér's V |
|---|---|---|
| **counted (centres 2–5), gating** | 278 | **0.155** |
| strict single-file (descriptive) | 226 | 0.151 |
| all 330 incl. centre-1 clips (descriptive) | 329 | 0.228 |

## 3. DS203 against the v4 SS arm (with Amendment 2)

| requirement | verdict |
|---|---|
| D3 | PASS (full-length recordings, centres 2–5; `27136df`) |
| D4 | PASS (site per case; 4 qualifying levels) |
| D5 | PASS (CC BY 4.0) |
| D6 | PASS (1.69 TB ≤ 2.02 TB) |
| D7 | PASS (Decision 002) |
| D8 | **PASS (V = 0.155)** |
| ≥ 200 trajectories | PASS (278) |
| Amendment 2 (in vivo human clinical) | PASS |

* **Gate §5 (SS arm).** No other dataset in the 230-dataset pool passes all SS requirements with Amendment 2: DS024
  fails ≥ 200 and Amendment 2, and every other dataset fails D4 or Amendment 2. **DS203 is the top-ranked and only
  dataset: selected for the SS arm.**
* **Qualifying levels:** 4. **Total trajectories:** 278. **Access:** no registration.
* **Limitation carried to the SS protocol (Decision 002 §1):** D7 has one human boundary, so two segments per
  trajectory.
* **RA arm:** unchanged. DS203 fails D1 and D2; no dataset passes D1–D6, so the RA arm stays deferred.

## 4. UNRESOLVED literature (not retrieved now; Decision 002 §5)

* C0288 OmniNet
* S0058 PSM-DID semantic embedding
* S0340 TIDAL
* S0373 LLMCE
* S0242 Synthetic ground-truth counterfactuals (MICCAI 2025)
* C0377 Tesei et al. 2023

See `lit/LIT_GATE_RESULT.md` §5.

## 5. Not done

* No video download beyond container headers, no frame decoding, no representation extraction, no model.
* The H1R and theory repositories are unchanged.
