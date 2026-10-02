# DS203 (Appendix300) Pre-Protocol Facts (Decisions 003 and 004)

* **Status:** descriptive facts for preprocessing design. No protocol is drafted, and no embedding or synthetic data is
  produced.
* **Video handling:**
  * Under Decision 003 §1, one sample video per centre (centres 2–5) was downloaded, and **six frames per sample were
    decoded only for viewing**.
  * Since Decision 004 (`314cd94`), no further decoding or frame extraction is allowed until the SS protocol is frozen.

## 1. Durations, appendix-visible timestamp, post-timestamp duration (minutes; from `146f69b`)

* **Basis:** per case, all files of the case, from the container probe (`moov` only).
* **Format:** median [IQR], range.
* **Centre 1:** mostly 5-minute clips; not a counted site.

| site | cases | total duration | appendix-visible timestamp | post-timestamp |
|---|---|---|---|---|
| 1 | 51 | 5.0 [5.0–5.0], 0.6–33.9 | 2.5 [1.0–3.3] | 2.5 [1.7–4.0] |
| 2 | 49 | 25.2 [15.0–32.8], 0.4–93.7 | 5.3 [2.2–9.3] | 16.9 [11.9–25.3] |
| 3 | 41 | 31.7 [24.8–45.1], 12.6–61.8 | 7.6 [4.1–10.7] | 22.4 [16.6–31.7] |
| 4 | 71 | 28.8 [19.5–46.8], 5.6–67.9 | 7.2 [2.3–13.5] | 22.4 [13.9–32.4] |
| 5 | 117 | 29.3 [22.9–31.8], 1.9–111.4 | 2.9 [0.3–6.1] | 24.3 [18.1–29.0] |

## 2. Recording format per site (all 403 files; `moov` of `146f69b`)

| site | files | frame rate (fps × files) | encoded resolution (× files) | display aspect | codec |
|---|---|---|---|---|---|
| 1 | 52 | 29.95×3, 29.53×2, 29.32×2, 29.25×2 | 1920x1080×52 | 1.778 | avc1 |
| 2 | 82 | 25.0×82 | 1920x1080×74, 3840x2160×8 | 1.778 | avc1 |
| 3 | 42 | 25.0×42 | 3840x2160×41, 1920x1080×1 | 1.778 | avc1 |
| 4 | 71 | 50.0×71 | 1920x1080×71 | 1.778 | avc1 |
| 5 | 156 | 50.0×156 | 1920x1080×156 | 1.778 | avc1 |

* All files are H.264 (`avc1`) with square pixels (`pasp` 1:1).
* **Site is entangled with acquisition format:**
  * centre 3 is 4K at 25 fps;
  * centre 2 is 25 fps, mostly 1080p;
  * centres 4–5 are 1080p at 50 fps.
* The SS protocol's preprocessing (resize, frame-rate normalisation) has to take this into account.

## 3. Sample videos (one per centre; Decision 003 §1 rule: the single-file counted case closest to the centre median duration)

| site | file | size | download rate | sha256 |
|---|---|---|---|---|
| 2 | `Center2_011.mp4` | 0.89 GB | 7.8 MB/s | `c5987792d87b7be4…` |
| 3 | `Center3_024.mp4` | 19.30 GB | 8.8 MB/s | `4b4bd6797757aa70…` |
| 4 | `Center4_042.mp4` | 0.81 GB | 6.5 MB/s | `ccfa2960be0fda7c…` |
| 5 | `Center5_003.mp4` | 1.67 GB | 9.1 MB/s | `19b144ce09b941e5…` |

* **Location:** the files are on LaCie at `/media/user/LaCie/medvideo_gate/DS203/samples/`; full hashes are in
  `lead/out/DS203_sample_download.json`.
* **Viewed frames:** 6 per sample, at 5 / 20 / 40 / 60 / 80 / 95 % of the duration, plus two crops of the centre-5
  overlay. These are JPEG/PNG for viewing only, in `samples/frames/`.

## 4. Viewed frames: descriptive record (no computation)

| site | field of view / mask | overlays and positions | other |
|---|---|---|---|
| 2 (`Center2_011`, 1080p 25 fps) | **circular endoscope image inside a black surround.** The circle is roughly as tall as the frame and centred horizontally. A small notch marker sits at the top (12 o'clock) of the circle | none seen | **3 of 6 sampled frames are uniform single-colour frames** (dark grey, grey-green, pinkish grey): no image content |
| 3 (`Center3_024`, 4K 25 fps) | **circular image wider than the frame height** (cut at top and bottom), with black left / right margins | a **small green camera icon at the bottom right** (lower right margin) in every frame | one frame heavily blurred (lens fog or smoke) |
| 4 (`Center4_042`, 1080p 50 fps) | **full-frame rectangular image** (no circular mask) | none seen | **4 of 6 sampled frames (40–95 %) are uniform single-colour frames** (dark slate, navy, black, black) |
| 5 (`Center5_003`, 1080p 50 fps) | **full-frame rectangular image** | an **opaque black rectangle at the top right** (about x 1645–1845, y 35–270 of 1920 × 1080; a privacy mask). A **status bar along the bottom edge** (about the bottom 2.5 %): "x1.0", icons, an image counter, "1 ● REC", the **elapsed recording time** (e.g. "00:01:27"), "(>7h)" and "(99%)" | the bar's timestamp and counters change over time |

* **Observed, not inferred.** The uniform frames are recorded as observed. The descriptor says "All extracorporeal
  sequences have been removed"; whether the uniform frames are de-identified segments was not determined, and no frame
  statistic was computed.
* **For the SS protocol** (no decision taken here):
  * site-specific overlays (centre 5 status bar and mask, centre 3 icon);
  * mask geometry (circular vs full-frame);
  * resolution and frame rate;
  * uniform / blank segments.

  All of these are site-linked, so they would let a representation decode site trivially.

## 5. Download estimate

* **Measured:** the four sample downloads (range requests, 4 connections) ran at **8.7 MB/s** aggregate (6.5–9.1
  MB/s per file).
* **Projection:**
  * all 1.69 TB of archive parts: **about 54 h**;
  * the full-video parts only (1.36 TB of the 1.69 TB; the rest is images and snippets): **about 43 h**.
* `scripts/download_ds203.sh` (`3c2eb51`) fetches 3 parts in parallel; per-connection speed on a single part was not
  measured, so the real time may differ.

## 6. Foundation-model candidates and embedding compute

**Pending.** The candidate searches under the Decision 003 / 004 rule are not finished, so this is left for Monday.
