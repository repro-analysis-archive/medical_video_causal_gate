# Erratum 003: CathAction (DS000) settled under Amendment 2 on public documentation

* **Verdict: FAIL under Gate Amendment 2** (`ebc097d`). The recordings are not "video recorded in vivo from human
  patients during clinical procedures".
* **Primary-source evidence** (public; nothing behind the access form was read):
  * **CathAction paper** (Huang et al., arXiv:2408.13126, PDF saved at
    `/media/user/LaCie/medvideo_gate/DS000/cathaction_2408.13126.pdf`):
    * §III.A, p. 3: "the acquisition of extensive human data is often impractical and time-consuming due to privacy
      constraints. To address this challenge, we suggest an alternative approach involving the collection of data from
      two distinct sources: i) utilizing vascular soft silicone phantoms modeled after the human body and ii) employing
      animal subjects, specifically pigs."
    * Table I, p. 2, lists CathAction as "X-ray Video 500,000+ Phantom".
    * §IV, p. 7: "we train the model on the phantom data and then test them on real animal data."
  * **Repository file listing**:
    * Source: `huggingface.co/api/datasets/airvlab/CathAction/tree/main`, read in the v4 audit.
    * Human-labelled data appear only as a separate archive, `segmentation_human_train.zip` (143,049,194 bytes).
    * That archive is distinct from the action videos, `video_action_understanding.zip` (41,808,377,811 bytes).
    * The dataset card describes the collision splits only by "phantom" and "animal" sources.
* **Wording note.** "On a silicone phantom or live pig" (Amendment discussion, Erratum 002 report) was the audit
  agent's paraphrase in `audits/A_col2_audit.json` (`trajectory_unit`). The quotes above are the primary wording.
* **No access will be sought.**
* **Trigger count.** This counts as the second of the three gated audits named in Amendment 1's trigger. SAGES CVS
  (Erratum 002) was the first.
