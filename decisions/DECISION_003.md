# Decision 003: DS203 pre-protocol facts (scope extension) and foundation-model selection rule

Investigator instruction, recorded by the lead analyst.
* Committed **before** any DS203 sample video is downloaded and before any foundation-model candidate is searched.
* No protocol drafting, no embedding, no synthetic data.

## 1. Pre-protocol scope extension: one sample video per centre (centres 2–5)

* **What is downloaded:** ONE full sample video per centre, for centres 2, 3, 4 and 5, to
  `/media/user/LaCie/medvideo_gate/DS203/samples/` (not the H1R disk).
* **How:** each file is extracted from the OPARA split zip by HTTP range requests over its stored (uncompressed) entry.
  Its sha256 is recorded.
* **Sample rule (fixed now):**
  * Among the centre's **single-file** cases (one full-video file) that are in the counted set of `146f69b`, take the
    case whose total duration is closest to the centre's median total duration.
  * Ties go to the lower OP number.
* **Viewing:**
  * A few frames of each sample are viewed: 6 frames at 5, 20, 40, 60, 80 and 95 % of the duration, decoded with
    `ffmpeg` and written as JPEGs scaled to 960 px width for viewing only.
  * Recorded, descriptively:
    * black borders or circular masks;
    * on-screen overlays (text, timestamps, logos);
    * their positions.
* **No computation on frames beyond viewing:** no statistics, no pixel measurements, no embedding, no model.

## 2. Foundation-model selection rule (fixed before listing candidates)

A candidate is eligible only if ALL of these hold:
1. **Open weights:** the weights are publicly downloadable.
2. **Licence permits research use.**
3. **Domain:**
   * **primary:** pretrained on surgical or endoscopic **video** (or video frames);
   * **secondary:** a **generic video generative** model (a generative or tokenizer/autoencoder video model trained on
     general video).
4. **Documented pretraining data:** a model card or paper lists the pretraining datasets or sources.

For each candidate, the record states, with a verbatim quote and its source, whether DS203 / Appendix300 (or its
source recordings) appears in its pretraining data. If the documentation does not allow this to be decided, the
answer is UNKNOWN.

## 3. Estimates (no execution)

* Download time for the full 1.69 TB, extrapolated from the measured throughput of the sample downloads.
* Embedding compute per eligible model on the available GPU (one NVIDIA RTX 4500 Ada, 24 GB), from published model
  sizes / throughput or FLOPs. Nothing is run.
