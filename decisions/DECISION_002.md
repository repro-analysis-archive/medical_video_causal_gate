# Decision 002: DS203 D7; evaluating DS203 against the original v4 SS arm; scope extension for D8

Investigator decision, recorded by the lead analyst. Committed before any DS203 duration is read.

## 1. D7 for DS203

* D7 is **PASS** under the literal frozen wording: a human-marked segment boundary that varies within trajectories and
  is not acquisition metadata.
* Content richness is not a D7 criterion.
* Its weakness (one boundary, two segments per trajectory) is carried to the SS protocol as a limitation.

## 2. DS203 is evaluated against the original v4 SS arm (with Amendment 2)

* Decision 001 confirmed Amendment 1's trigger before the v4 search was complete: the Semantic Scholar arm had not
  run.
* With the v4 search now complete, DS203 is evaluated against the original v4 SS arm, with Amendment 2.

## 3. Pre-fixed branch

* **DS203 D8 PASS:** it passes the v4 SS arm. **Amendment 1 is VOID.** The SS arm with the real site factor applies to
  DS203.
* **DS203 D8 FAIL:** **Amendment 1 stays ACTIVE.** SS' applies to DS203, as already selected (`27136df`).

## 4. Scope extension, for DS203 only

* Read the container-level duration and frame rate of every DS203 video file.
* Use HTTP range requests or container probing.
* No frame decoding, no pixel computation, and no full download beyond what reading the container header requires.
* **If durations cannot be obtained this way, STOP and report.** Do not estimate them.

## 5. Not now

The six blocked PDFs (C0288, S0058, S0340, S0373, S0242, C0377) remain **UNRESOLVED** and are not retrieved now.
