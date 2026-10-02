# Decision 004: pre-protocol bulk download of DS203; no video computation until the SS protocol is frozen

Investigator decision, recorded by the lead analyst.

**Filing note.** The investigator asked for this text as `decisions/DECISION_003.md`. That file already exists: it was
committed in `67d8fcf` (DS203 sample-video scope extension and the foundation-model selection rule), and committed
decision files are never edited. This decision is therefore filed as Decision 004. Its foundation-model rule repeats
Decision 003 §2 unchanged.

## 1. Bulk download

* A pre-protocol bulk download of DS203 (all Appendix300 archive parts on TU Dresden OPARA, 1.69 TB) to LaCie is
  **authorized**.
* It is **launched manually by the investigator**, via `scripts/download_ds203.sh`.

## 2. No computation on video content until the SS protocol is frozen

Not allowed:
* decoding;
* embedding;
* frame extraction;
* synthetic data.

Exceptions:
* archive integrity checks (size and the OPARA MD5 per part);
* viewing a few frames of one sample video per centre, for preprocessing design, recorded descriptively. This was
  already done under Decision 003 §1: six frames per centre, centres 2–5.

## 3. Foundation-model selection rule (fixed; identical to Decision 003 §2)

1. open weights;
2. a licence permitting research use;
3. domain: surgical or endoscopic video for the **primary**, a generic video generative model for the **secondary**;
4. documented pretraining data.
