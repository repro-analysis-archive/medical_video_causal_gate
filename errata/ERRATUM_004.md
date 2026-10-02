# Erratum 004: Trauma THOMPSON (DS173) settled under Amendment 2 on public material

* **Verdict: FAIL under Gate Amendment 2** (`ebc097d`). All 220 videos are simulated procedures, not "video recorded
  in vivo from human patients during clinical procedures". **No access will be sought.**
* **Trigger count.** This counts as the third of the three gated audits named in Amendment 1's trigger, after SAGES
  CVS (Erratum 002) and CathAction (Erratum 003).
* **Material read (public only; nothing behind the consent form):**
  * Scientific Data 2025 full text, PMC12815934 (doi 10.1038/s41597-025-06365-y);
  * MELBA 2025:048;
  * BMVC 2025 paper 1135;
  * GitHub `zhuoyp/TTD` and `zhuoyp/T3Challenge2025` READMEs;
  * the public sample file `mmaction_train_annotations.txt`.

  Copies are in `/media/user/LaCie/medvideo_gate/DS173/`.

## a) Recording subjects: simulation models

* Scientific Data, Methods › Data Collection: "All participants provided written informed consent prior to
  participation, agreeing to be video-recorded from an egocentric perspective while performing simulated medical
  procedures for research and dataset development purposes."
* Scientific Data, Methods › Recording: "Filming was conducted across various simulation models and environments,
  including those that resemble field conditions."
* MELBA 2025:048 §3.2, p. 3, and BMVC 2025 §3, p. 5, use the same wording: "to capture first-person views filmed
  across various simulation models and environments."
* No passage describes patients, cadavers or animals as subjects.

## b) Ethics and consent

* Scientific Data, Methods › Data Collection: "This study was approved by the Institutional Review Board (IRB) under
  protocol number 223046, reviewed and overseen by the Geneva Foundation team. Participants were medical
  professionals recruited through internal invitations at the Madigan Army Medical Center and the University of
  Calgary".
* Consent is the **participants'** (the clinicians filmed). **No patient consent statement exists**, consistent with
  there being no patients.
* MELBA (Ethical Standards, p. 8): "The IRB approval was conducted by the Geneva team and obtained with the protocol
  number 223046."

## c) Site, operator or device per video

* **Device:** a single model, "commercial GoPro Hero7 Black cameras" (Scientific Data, Recording). One level.
* **Operator:** "No physician-identifying or personally traceable information was included in the final dataset"
  (Scientific Data, Data Collection). No per-video operator field is documented.
* **Site:** two recruiting institutions, Madigan Army Medical Center and the University of Calgary, at dataset level
  only. No per-video site field is documented.
* **Video identifiers.** The public sample annotation file uses video ids with five prefixes, P01–P05, which matches
  the five procedures. They are not documented as participant, site or device.
* **Not settled publicly.** Whether the gated `annotations.csv` holds a per-video site or participant field. This
  does not affect the verdict (see d).

## d) Trajectory count after exclusion under Amendment 2

* 220 videos (GitHub `zhuoyp/TTD`: "177 videos of standard (regular) emergency procedures", "43 videos of
  *just-in-time* (JIT) procedures").
* All are of simulated procedures on simulation models. **After exclusion: 0.**

## Conclusion

The public facts alone decide FAIL. Question (c) remains open, but it cannot change the outcome, because no trajectory
survives Amendment 2.
