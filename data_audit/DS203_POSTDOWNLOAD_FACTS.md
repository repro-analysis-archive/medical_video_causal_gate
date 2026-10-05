# DS203 post-download, pre-protocol facts (task CC_TASK_post_download_preprotocol)

* **Governing records:** gate v4 (`baadf5c`), Amendments 1–2, Decisions 001–005.
* **Hard limits kept:**
  * no DS203 frame was decoded, extracted or embedded, and no archive was extracted;
  * DS203 bytes were read only for the LaCie read-throughput test (`dd` to `/dev/null`) and, as before, from the moov
    boxes saved in 146f69b;
  * every decode measurement ran on **synthetic** ffmpeg test videos;
  * the H1R and theory repositories were not touched;
  * the Semantic Scholar key was not used in this task. A scan of every new file found it in none.
* **No model is chosen.** The selection rule will be fixed in the SS protocol.

## 0. Download completion

`data_audit/DS203_DOWNLOAD_COMPLETE.md` (`dba9c06`):
* 11 / 11 parts VERIFIED against the host's MD5;
* 1,692.5 GB;
* run 2026-10-02T18:19:23 → 2026-10-04T18:43:39 (+0900), `failures=0`;
* process finished.

## 1. Named reference representation (Decision 005)

* **Decision 005: `3660721`**, committed before step 2. The Cosmos tokenizer of Nakamura, Breuer, Crespin, Dietrich &
  Imai (2026, arXiv 2607.06126, K4) is a named reference representation, outside the primary / secondary competition.
  * Reason: the research question.
* **Reference entry:** `lead/out/cosmos_reference_entry.json`, built by `lead/cosmos_reference_entry.py` (`39d6eeb`).
  * Quotes verified: 26 / 26 against the saved copies in `lead/fm_sources/reference/` and the Cosmos paper copy
    `lead/fm_sources/secondary/`.

| field | value (quoted sources in the JSON) |
|---|---|
| version | **nvidia/Cosmos-1.0-Tokenizer-CV8x8x8** (HF sha 5110dbb3…). K4 itself says only "the NVIDIA Cosmos tokenizer (Agarwal et al., 2025)". The checkpoint is the default (`DEFAULT_COSMOS_MODEL_ID`) of the authors' package gpi_pack (commit 8836037), whose video module implements "the representation used by the video paper" and whose documentation links this checkpoint. **The exact version is therefore the authors' package default, not a statement in the paper.** |
| weights location | huggingface.co/nvidia/Cosmos-1.0-Tokenizer-CV8x8x8 (encoder.jit, decoder.jit, autoencoder.jit, vae/diffusion_pytorch_model.safetensors); gated "auto". Not downloaded; terms not accepted |
| licence | NVIDIA Open Model License Agreement (version release date January 6, 2025); card: "This model is ready for commercial use." |
| documented training data | Described, not listed: "We use both proprietary video datasets and publicly available open-domain Internet videos to train our models."; "about 20M hours of raw videos"; nine content categories. No named dataset; no medical, surgical, endoscopic or laparoscopic term in the paper. The model card states none |
| DS203 / Appendix300 overlap | **UNKNOWN**. The sources are undisclosed, so the source recordings cannot be excluded. The checkpoint (2025-01-07) predates the OPARA release (2026-04-29) |
| input requirements | RGB; shorter side 256 px to 4K; up to 8 s at 1080p (A100 80 GB bound). Checkpoint: 8× temporal and 8×8 spatial compression, 720 short side, 121-frame context. **K4 setting:** 5-s segments; up to 121 frames uniformly selected per segment (package default); pooled (16, 40, 60), consistent with a 320×480 input. The paper does not specify resize or frame sampling |
| latent dimension | 16 channels per latent voxel. K4 representation = decoder input `post_quant_conv(latent)`, mean-pooled over latent time: 16 × 40 × 60 = **38,400 values per 5-s segment** |
| params | Not stated for this checkpoint. Proxy: 105M (card runtime table, "Cosmos-Tokenizer-CV" at 4×8×8) |
| compute per video-hour (K4 setting, encode + `post_quant_conv` only; RTX 4500 Ada) | **0.14–0.49 GPU-h** for 87,120 frames per hour at 320×480. Low: card runtime 34.8 ms/frame (A100, encode + decode, 720×1280), scaled by pixels and by the dense-BF16 ratio, encode = ½. High: the 052590c conv-VAE calibration with P = 105M. All of DS203 (150.3 h): about 21–73 GPU-h. Every native frame must be decoded (dense sampling) |

## 2. Site-overlap check

Builder: `lead/site_overlap.py` → `lead/out/site_overlap.json`, `site_overlap_table.md`, `site_overlap_sources.md`.
**236 / 236 quotes verified** (whitespace-normalised substring of the saved copy).

### 2.1 DS203 centres (descriptor, Sci Data 2026, PMC13263317; readme)

* Descriptor: "The participating centers comprise four public hospitals (Asklepios-ASB Krankenhaus Radeberg,
  Diakonissenkrankenhaus Dresden, Krankenhaus St. Joseph Stift Dresden, St. Elisabethen-Krankenhaus Ravensburg) and one
  academic surgical department (Department of Pediatric Surgery, University Hospital Carl Gustav Carus Dresden)."
* Table 1: "Center 1 Center 2 Center 3 Center 4 Center 5 Clinical Institution public academic public public public
  Patient Demographics adult pediatric adult pediatric and adult adult".
* The readme names no institution ("Data from five distinct surgical centers.").

| centre | institution | basis |
|---|---|---|
| C1 | one of the four public hospitals | Table 1 "public" |
| **C2** | **Department of Pediatric Surgery, University Hospital Carl Gustav Carus Dresden** | the only "academic" centre in Table 1 and the only academic department in the text; "pediatric" |
| C3 | one of the four public hospitals | Table 1 "public" |
| C4 | one of the four public hospitals | Table 1 "public" (pediatric and adult) |
| C5 | one of the four public hospitals | Table 1 "public" |

* **Which public hospital is C1, C3, C4 or C5 is not stated** in the descriptor or the readme. The author affiliation
  "Department of General and Visceral Surgery, Dresden-Friedrichstadt General Hospital" is not one of the five centres.
* **Verification copies:**
  * quotes are verified against the PMC text copy on LaCie (sha256 in the JSON);
  * the PDF text copy contains the first quote verbatim, but its Table 1 layout differs, so the Table 1 quote is checked
    against the PMC text only.

### 2.2 Pretraining sources and their institutions

* **Candidates:**
  * all 19 eligible primary and 11 eligible secondary candidates (052590c), plus the Cosmos reference;
  * SurgeNet's procedure variants and EndoSSL's laparoscopy and colonoscopy checkpoints get their own rows.
* **Lineage rule (as in the survey):**
  * the training data of the released weights, plus the initialisation or base weights;
  * distillation teachers are recorded only.
* **Recording sites of the named public datasets:** quoted from their own publications, fetched for this step into
  `lead/fm_sources/datasets/` (45 copies, manifest with sha256). Output: `lead/out/dataset_provenance.json`, 51 / 51
  quotes verified by the agent and re-verified by the lead.
  * **18 of 26 datasets have a quoted recording site.**
  * **Not stated or not obtainable:**
    * LapGyn4, GLENDA, SurgicalActions160 (dataset pages name only the "originator of the videos", Prof. J.
      Keckstein, Ulm University affiliation);
    * the hSDB gastrectomy part;
    * Colonoscopic;
    * LDPolypVideo;
    * the 5 in-house CholecT50 videos;
    * EndoSSL colonoscopy (six unnamed centres);
    * CMR Versius clinical cases;
    * non-clinical sets: SurgToolLoc porcine, SutureBot phantom, EndoMamba porcine bronchoscopy.
* **Per-candidate source lists with institutions:** `lead/out/site_overlap_sources.md`. The quotes are in
  `site_overlap.json`.
* **Dresden-linked sources found:**
  * **DSAD.** 32 robot-assisted rectal resections: "performed at the University Hospital Carl Gustav Carus Dresden".
    The authors are in the "Department of Visceral, Thoracic and Vascular Surgery". It is in EndoViT, SurgeNetXL and
    SurgeNet / SurgeNetPublic.
  * **Open-H TUNDRA.** In vivo porcine data. Institutions: NCT/UCC Dresden and the Department of Visceral, Thoracic
    and Vascular Surgery, Carus.
    * It is in the Open-H collection, but **not in the documented training mixture** of Cosmos-H-Surgical-Simulator.
    * Cosmos-H-Dreams inherits that mixture.
* **No source from the four public hospitals.**
  * A keyword search (Radeberg, Ravensburg, Diakonissen, Joseph-Stift, Elisabethen, Asklepios, Carus, Friedrichstadt)
    over the 45 new dataset copies and all candidate copies found no recording-site hit.
  * "Dresden" matched only author affiliations and the DSAD citation.
  * The LEMON oEmbed check of its 252 appendectomy entries also found no hit (`keyword_hits: []`).

### 2.3 Candidate × DS203 centre

**Cell codes:**

| code | meaning |
|---|---|
| **SAME DEPT** | a source was recorded in that centre's department (none found) |
| **SAME HOSP** | same hospital, different department |
| **UNK-web** | a web-scale source (YouTube, web lecture platforms, stock / social / Internet video), or a base model whose training data are undocumented |
| **UNK-site** | all sources are named, but at least one human clinical set has no stated recording site |
| **NO** | every source has a named site (or is non-clinical, or a fixed general benchmark) and none is a DS203 institution |

| candidate | arm | C1 | C2 | C3 | C4 | C5 | web-scale / undocumented sources | clinical sources without stated site |
|---|---|---|---|---|---|---|---|---|
| Endo-FM | primary | UNK-site | UNK-site | UNK-site | UNK-site | UNK-site | - | Colonoscopic (Mesejo et al. 2016); LDPolypVideo; CholecTriplet / CholecT50 |
| EndoViT | primary | UNK-site | SAME HOSP (DSAD) + UNK-site | UNK-site | UNK-site | UNK-site | - | LapGyn4; hSDB-instrument / hSDB-Gastric (gastrectomy part); GLENDA v1.0; SurgicalActions160 |
| SurgeNetXL | primary | UNK-web | SAME HOSP (DSAD) + UNK-web | UNK-web | UNK-web | UNK-web | Surgical YouTube dataset (SurgeNetXL) | GLENDA v1.0; LapGyn4; hSDB-instrument / hSDB-Gastric (gastrectomy part) |
| SurgeNet / SurgeNetPublic | primary | UNK-site | SAME HOSP (DSAD) + UNK-site | UNK-site | UNK-site | UNK-site | - | GLENDA v1.0; LapGyn4; hSDB-instrument / hSDB-Gastric (gastrectomy part) |
|   SurgeNetCholec variant | primary | NO | NO | NO | NO | NO | - | - |
|   SurgeNetRAMIE variant | primary | NO | NO | NO | NO | NO | - | - |
|   SurgeNetRARP variant | primary | NO | NO | NO | NO | NO | - | - |
| SurgVLP / HecVL / PeskaVLP | primary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | SVL lectures (WebSurg, EAES, YouTube) | - |
| EndoMamba | primary | UNK-site | UNK-site | UNK-site | UNK-site | UNK-site | - | Colonoscopic (Mesejo et al. 2016); LDPolypVideo; CholecTriplet / CholecT50; GLENDA v1.0; hSDB-instrument / hSDB-Gastric (gastrectomy part) |
| LemonFM | primary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | LEMON (YouTube) | - |
| EndoSSL (laparoscopy weights) | primary | NO | NO | NO | NO | NO | - | - |
| EndoSSL (colonoscopy weights) | primary | UNK-site | UNK-site | UNK-site | UNK-site | UNK-site | - | EndoSSL Private Colonoscopy |
| SelfSupSurg | primary | NO | NO | NO | NO | NO | - | - |
| SurgLIME | primary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | LEMON (YouTube) | - |
| PL-Stitch | primary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | LEMON (YouTube) | - |
| Basel V-JEPA ViT-L | primary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | V-JEPA base: VideoMix2M (HowTo100M + Kinetics + SSv2) | - |
| Cosmos-H-Surgical v0.3.1 | primary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | Cosmos-H synthetic cholecystectomy videos; base Cosmos3-Nano | - |
| Cosmos-H-Surgical Predict/Transfer 2.5 | primary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | SATA 'credentialed YouTube surgical channels'; base Cosmos-Predict2.5-2B / Cosmos-Transfer2.5-2B | CholecTriplet / CholecT50; SurgicalActions160 |
| Cosmos-H-Surgical-Simulator | primary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | base Cosmos-Predict2.5-2B / Cosmos-Transfer2.5-2B | Open-H CMR Versius clinical procedures |
| Cosmos-H-Dreams | primary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | base Cosmos-Predict2.5-2B / Cosmos-Transfer2.5-2B | Open-H CMR Versius clinical procedures |
| MedSora | primary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | MedSora base '3D causal VAE' | Colonoscopic (Mesejo et al. 2016); CholecTriplet / CholecT50 |
| SG2VID | primary | NO | NO | NO | NO | NO | - | - |
| KVLR | primary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | KVLR base video generator | - |
| Open-Sora VAE v1.2 | secondary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | Pexels / Pixabay / Mixkit stock video; SD / SDXL / SD2.1 image-VAE initialisation | - |
| VideoMAE | secondary | NO | NO | NO | NO | NO | - | - |
| VideoMAE V2 | secondary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | WebVid; self-crawled Instagram | - |
| OmniTokenizer | secondary | NO | NO | NO | NO | NO | - | - |
| Open-MAGVIT2 video | secondary | NO | NO | NO | NO | NO | - | - |
| Open-Sora-Plan v1.2 VAE | secondary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | Pexels / Pixabay / Mixkit stock video; SD / SDXL / SD2.1 image-VAE initialisation | - |
| WF-VAE-L | secondary | NO | NO | NO | NO | NO | - | - |
| CV-VAE | secondary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | LAION-COCO / Unsplash images; WebVid; SD / SDXL / SD2.1 image-VAE initialisation | - |
| LARP | secondary | NO | NO | NO | NO | NO | - | - |
| LeanVAE | secondary | NO | NO | NO | NO | NO | - | - |
| Reducio-VAE | secondary | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | Pexels / Pixabay / Mixkit stock video; SD / SDXL / SD2.1 image-VAE initialisation | - |
| Cosmos tokenizer CV8x8x8 (Decision 005 reference) | reference | UNK-web | UNK-web | UNK-web | UNK-web | UNK-web | Cosmos tokenizer data: proprietary + open-domain Internet video (~20M h raw) | - |

* **SAME HOSP (DSAD), the only institutional overlap found:**
  * candidates: EndoViT, SurgeNetXL, SurgeNet / SurgeNetPublic;
  * centre: **C2 only**;
  * DSAD is Carus Visceral, Thoracic and Vascular Surgery (rectal resection), while C2 is Carus Pediatric Surgery
    (appendectomy);
  * **no same-department overlap was found.**
* **Strict reading.** Fixed general benchmarks (ImageNet, Kinetics, SSv2, UCF-101) are web-derived. Counting them as
  web-scale would turn these NO rows into UNK-web: SurgeNetCholec / RAMIE / RARP, SelfSupSurg, VideoMAE, OmniTokenizer,
  Open-MAGVIT2, WF-VAE-L, LARP and LeanVAE.
  * The following stay NO under either reading:
    * SG2VID, whose initialisation is not stated;
    * EndoSSL-laparoscopy, which is NO by its geographic statement ("eight different medical centers in Israel").

## 3. Decode and I/O throughput (no DS203 frame decoded)

Scripts are in `lead/ds203_codec_facts.py` and `lead/throughput/`. Outputs are in `lead/out/`:
`DS203_codec_facts.json`, `synthetic_videos.json`, `throughput_decode.json`, `throughput_decode_addendum.json`,
`lacie_read_throughput.json`, `ds203_wall_time_estimate.json` and `ds203_wall_time_table.md`.

### 3.1 Container facts per centre (from the moov boxes saved in 146f69b; no `mdat` byte read)

All 403 files are **avc1 (H.264)**, 4:2:0 8-bit, progressive (frame_mbs_only = 1), with B-frames (ctts present in
402 / 403), muxer tag Lavf58.x. The readme calls them "Re-encoded, de-identified laparoscopic video". **The codec
parameters therefore describe the re-encode, not the camera stream.**

| centre | files | profile / level (avcC) | resolution × frame rate | keyframe interval (stss): median of file medians [range] | bitrate median [range] | hours / TB |
|---|---|---|---|---|---|---|
| C1 | 52 | High 5.0 (48), High 4.0 (3), Baseline 4.1 (1) | 1920×1080 at ~28.7–30 fps (49) and ~47.7–48.9 fps (3); 7 files VFR | 4.5 s [0.5–8.5 s]; 15–250 frames | 6.2 Mbps [3.8–11.8] | 4.7 h / 0.014 |
| C2 | 82 | High 5.0 (63), 4.0 (11), 5.1 (8) | 1920×1080 at 25 (74 files, 20.8 h); **3840×2160 at 25 (8 files, 2.6 h)** | 2.4 s [1.2–4.8 s] | 16.0 Mbps (1080p) / 73.1 Mbps (4K) | 23.4 h / 0.199 |
| C3 | 42 | High 5.1 (41), 5.0 (1) | **3840×2160 at 25 (41 files, 23.0 h)**; 1920×1080 at 25 (1 file) | 1.5 s [1.2–4.8 s] | 75.0 Mbps (4K) | 23.2 h / 0.781 |
| C4 | 71 | High 5.0 (61), 4.2 (10) | 1920×1080 at 50 | 1.9 s [0.7–5.0 s] | 7.8 Mbps [3.7–11.7] | 40.2 h / 0.141 |
| C5 | 156 | High 5.0 (153), 4.2 (3) | 1920×1080 at 50 | 4.3 s [0.7–5.0 s] | 8.5 Mbps [1.4–11.3] | 58.8 h / 0.225 |

* The longest keyframe interval is 250 frames in every centre.
* max_num_ref_frames is 5 (372 files), 4 (30 files) or 1 (1 file).
* All files together: 150.3 h, 1.36 TB.

### 3.2 Synthetic test videos (no DS203 byte used)

`lead/throughput/make_synthetic.py`:
* **Source:** ffmpeg `testsrc2` plus temporal noise.
* **Encoder:** libx264 High, yuv420p, 3 B-frames, 5 references, fixed GOP; 60 s each.
* **Targets:** the median bitrate and median keyframe interval of each centre format.
* **Storage:** the files are in the session scratchpad and are not committed; their sha256 values are in
  `synthetic_videos.json`.

| test video | stands for | target Mbps / GOP | achieved Mbps / GOP | profile / level |
|---|---|---|---|---|
| C1_1080p30 | C1 | 6.2 / 135 | 6.04 / 128.6 (partial last GOP) | High 5.0 |
| C2_1080p25 | C2 1080p (and the single C3 1080p file) | 16.0 / 60 | 15.80 / 60 | High 5.0 |
| C2_2160p25 | C2 4K | 73.1 / 30 | 73.46 / 30 | High 5.1 |
| C3_2160p25 | C3 4K | 75.0 / 36 | 74.49 / 35.7 | High 5.1 |
| C4_1080p50 | C4 | 7.8 / 96 | 7.81 / 93.8 | High 5.0 |
| C5_1080p50 | C5 | 8.5 / 214 | 8.45 / 200 | High 5.0 |

### 3.3 Decode throughput on the synthetic videos (fixed physical-time grid 0.5 / 1 / 2 / 4 fps)

`lead/throughput/decode_bench.c` is an in-process libavcodec benchmark (Ubuntu FFmpeg 4.4.2, lavc 58.134) on the RTX
4500 Ada and 20 CPU threads.

**Strategies:**

| strategy | what it does |
|---|---|
| seq | decode every frame, keep the first frame at or after each grid time |
| seek | for each grid time, seek to the preceding keyframe, flush, decode forward |
| hybrid | seek only when the grid time lies beyond the next keyframe |
| skip | as hybrid, but jumps forward by discarding packets, with no seek and no flush (added in the addendum) |
| keyonly | keyframes only; not on the grid |

**Measurement details:**
* Selected NVDEC frames are copied to host memory.
* Every run selected exactly the grid targets; there were 0 transfer failures.
* "Aggregate" means parallel streams: CPU = 5 processes × 4 threads; NVDEC = 4 sessions; CPU+NVDEC = both at once.
* Single-stream seq and hybrid use the median of 3 repetitions.
* A ~15 s correctness check of `skip` overlapped the C2_1080p25 CPU-seek / NVDEC-seq rows. Those rows were re-measured
  (e.g. CPU seek at 0.5 fps: 22.6 → 22.5×) and the re-measured values are used.

**× realtime** (video seconds decoded per wall second):

| test video | 1-stream CPU seq | 1-stream NVDEC seq | agg CPU seq | agg NVDEC seq | agg CPU+NVDEC seq | agg CPU+NVDEC skip 0.5/1/2/4 | agg CPU hybrid 0.5/1/2/4 | agg NVDEC skip 0.5/1/2/4 | 1-stream NVDEC seek 0.5/4 | keyonly CPU/NVDEC |
|---|---|---|---|---|---|---|---|---|---|---|
| C1_1080p30 | 55.5 | 30.8 | 76.4 | 51.2 | 114.8 | 147/131/122/119 | 96/84/80/72 | 66/59/55/52 | 7.6/0.9 | 915/1035 |
| C2_1080p25 | 30.7 | 31.1 | 38.2 | 51.7 | 67.9 | 106/79/70/68 | 55/41/37/30 | 76/58/52/52 | 7.7/0.9 | 555/585 |
| C2_2160p25 | 6.9 | 8.0 | 8.9 | 14.2 | 15.8 | 45/22/17/16 | 22/11/9/7 | 43/22/16/15 | 7.6/0.9 | 89/95 |
| C3_2160p25 | 7.5 | 7.9 | 9.0 | 14.0 | 16.3 | 36/21/17/16 | 17/10/8/6 | 34/20/16/15 | 7.6/0.9 | 98/112 |
| C4_1080p50 | 39.0 | 18.6 | 55.7 | 32.5 | 73.0 | 155/100/82/77 | 106/67/54/46 | 67/45/38/35 | 7.7/0.9 | 664/727 |
| C5_1080p50 | 42.2 | 18.6 | 53.9 | 32.5 | 72.6 | 93/81/78/73 | 69/59/52/47 | 42/36/35/34 | 7.6/0.9 | 1005/1144 |

**Keyframe seeking:**
* **NVDEC seek / flush costs about 0.26 s each** on this stack. NVDEC "seek" therefore stays at about 7.6× at 0.5 fps
  in every format and falls to 0.9× at 4 fps.
* At 0.5 fps, CPU hybrid beats CPU seq in every format (aggregate 1.26–2.5×). The gain is largest where the grid
  interval (2 s) exceeds the keyframe interval: C2 4K 2.5×, C4 1.9×, C3 1.9×.
* At 2–4 fps:
  * CPU hybrid lies between −31 % and +5 % of CPU seq;
  * CPU+NVDEC skip is 0 to +13 % faster than CPU+NVDEC seq.
* NVDEC strategies:
  * flush-based NVDEC hybrid is 0.61–1.0× NVDEC seq at 1–4 fps, so it never beats it;
  * NVDEC skip, with no flush, runs at 1.0–1.5× NVDEC seq.
* Keyframe-only decode is 90–1,100× realtime, but it does not sample on a fixed grid.

**All DS203 (150.3 h), decode only:**

| grid | best path | decode h | CPU seq | NVDEC seq | CPU+NVDEC seq |
|---|---|---|---|---|---|
| 0.5 fps | CPU+NVDEC skip | 1.81 | 5.33 | 5.36 | 3.28 |
| 1 fps | CPU+NVDEC skip | 2.65 | 5.27 | 5.37 | 3.29 |
| 2 fps | CPU+NVDEC skip | 3.06 | 5.29 | 5.40 | 3.31 |
| 4 fps | CPU+NVDEC skip | 3.25 | 5.28 | 5.44 | 3.33 |

* About 0.78 TB of the 1.36 TB, and the slowest decode, is C3's 4K (23.0 h).

### 3.4 LaCie sequential read (DS203 archive bytes, `dd iflag=direct` to /dev/null)

* **Device:** LaCie d2 Professional, USB, rotational.
* **Test:** 2 GiB at the start, middle and end of each of the six full-video parts, plus a 16 GiB sustained read.
* **Result:** **116.9 MB/s sustained** (point reads 95.3–172.2 MB/s, median 120.8).
* **Reading all 1.36 TB takes 3.23 h.**
  * Hybrid at 0.5 fps reads only the GOPs it decodes: about 2.1 h, including 12 ms per seek.

### 3.5 Wall time for all DS203 full videos (150.3 h), per model and grid rate

**Model and pipeline assumptions:**
* **Model time:** the 052590c FLOPs per input at 30 % of dense BF16 peak on the RTX 4500 Ada.
  * Inputs per video-hour = 3600·R / frames per input. Clip models take non-overlapping clips of consecutive grid
    frames.
  * "documented sampling" uses the 052590c sampling instead. When it consumes more than 4 frames/s it needs dense
    sequential decode.
* **Pipelining:** I/O, decode and model are assumed pipelined, so wall = max(component), and the decode path minimising
  wall is chosen.
* **Cell format:** wall time (bottleneck). "A ~ B" means the second component is within 10 % of the first.
* **Cosmos reference:** the high end of its 0.14–0.49 GPU-h per video-hour range is used.
* **Fit on 24 GB:** Cosmos-H-Surgical v0.3.1 (15.2B) and KVLR (12B) do not fit bf16 weights on 24 GB (052590c); their
  model times assume offload / quantisation, or the 96 GB GPU (~3.2× faster).
* **Not included:** resizing and colour conversion of the sampled frames.

| model | arm | 0.5 fps | 1 fps | 2 fps | 4 fps | documented sampling |
|---|---|---|---|---|---|---|
| Endo-FM (ViT-B video, 121M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 4.5 h (model) |
| EndoViT (ViT-B/16, 85.8M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| SurgeNetXL CAFormer-S18 (24.3M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| SurgeNetXL DINO ViT-L/14 (~304M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| SurgeNet / Public variants (CAFormer-S18) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| SurgVLP / HecVL / PeskaVLP (ResNet-50 visual) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| EndoMamba (24.46M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| LemonFM (ConvNeXt-L, ~198M std) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| EndoSSL ViT-L (~304M std) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| SelfSupSurg (ResNet-50) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| SurgLIME (ViT-B/16 visual) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| PL-Stitch (ViT-B/16) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| Basel V-JEPA ViT-L (~304M std) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| Cosmos-H-Surgical v0.3.1 (~15.2B DiT) | primary | 4.8 h (model) | 9.7 h (model) | 19.4 h (model) | 38.7 h (model) | 154.7 h (model) |
| Cosmos-H-Surgical Predict/Transfer 2.5 (2B) | primary | 5.7 h (model) | 11.5 h (model) | 23.0 h (model) | 46.0 h (model) | 183.7 h (model) |
| Cosmos-H-Surgical-Simulator (~2B) | primary | 3.1 h (decode) | 3.2 h (I/O) | 4.5 h (model) | 9.0 h (model) | 22.4 h (model) |
| Cosmos-H-Dreams (~2B) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.6 h (model) | 7.3 h (model) | 18.2 h (model) |
| MedSora-B (86.47M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| SG2VID (U-Net ~1.24B, inferred from fp32 file size) | primary | 3.1 h (decode) | 3.2 h (I/O) | 4.0 h (model) | 8.0 h (model) | 8.0 h (model) |
| KVLR (~12.06B) | primary | 6.5 h (model) | 12.9 h (model) | 25.8 h (model) | 51.7 h (model) | 387.6 h (model) |
| Open-Sora VAE v1.2 (384M whole) | secondary | 3.1 h (decode) | 4.7 h (model) | 9.4 h (model) | 18.8 h (model) | 113.0 h (model) |
| VideoMAE-B (87M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| VideoMAE-L (305M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| VideoMAE-H (633M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| VideoMAE V2-g (1011M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| OmniTokenizer | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| Open-Sora-Plan v1.2 VAE (enc 94M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 4.6 h (model) | 28.8 h (model) |
| WF-VAE-L 16ch (enc 84M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 4.1 h (model) | 25.7 h (model) |
| CV-VAE (enc 68M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.3 h (model ~ decode) | 20.8 h (model) |
| LARP-L (173M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| LeanVAE (39.8M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| Reducio-VAE (437M whole) | secondary | 3.1 h (decode) | 5.4 h (model) | 10.7 h (model) | 21.4 h (model) | 85.7 h (model) |
| Open-MAGVIT2 video | secondary | 3.1 h (decode (model n/e)) | 3.2 h (I/O (model n/e)) | 3.2 h (I/O ~ decode (model n/e)) | 3.2 h (decode ~ I/O (model n/e)) | 3.2 h (I/O (model n/e)) |
| Cosmos tokenizer CV8x8x8 (Decision 005 reference) | reference | 3.1 h (decode) | 3.2 h (I/O ~ model) | 6.0 h (model) | 12.1 h (model) | 73.1 h (model) |

**Summary of bottlenecks:**
* **Small frame and clip encoders** (all primary encoders except Cosmos-H and KVLR, VideoMAE / V2, OmniTokenizer,
  LARP, LeanVAE):
  * the job is I/O / decode-bound at about **3.1–3.3 h** for all of DS203 at every grid rate;
  * model time is < 0.5 GPU-h at 4 fps;
  * LaCie I/O (3.23 h) and decode (1.8–3.3 h with CPU+NVDEC together) are within 10 % of each other from 2 fps up.
* **Model-bound:**
  * Cosmos-H Predict/Transfer / v0.3.1 and KVLR at every rate;
  * the conv-VAE secondaries (Open-Sora VAE, Reducio) from 1 fps;
  * Simulator / Dreams / SG2VID / Open-Sora-Plan / WF-VAE / Cosmos reference from 2–4 fps;
  * every dense documented setting of a large model, e.g. the **Cosmos reference at the K4 setting (24 fps dense):
    about 73 GPU-h**.

## 4. What this does not establish

* **Throughput** comes from synthetic videos (testsrc2 plus temporal noise) at matched codec, resolution, frame rate,
  median bitrate and median keyframe interval.
  * DS203 content, scene-cut keyframes and variable bitrate may decode at a different speed.
  * The keyframe interval is fixed in the test videos but variable in DS203.
* **Model times** are the 052590c FLOP-based estimates (30 % of dense BF16 peak), not measurements. No weight was
  downloaded.
* **Site overlap:**
  * it rests on documentation;
  * UNK cells mean that overlap cannot be excluded, not that it exists;
  * C1, C3, C4 and C5 cannot be mapped to named hospitals.
