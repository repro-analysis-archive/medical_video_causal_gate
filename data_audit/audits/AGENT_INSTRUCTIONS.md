# Instructions for dataset-audit agents (fixed; applies to every batch)

Read first:
- /home/user/projects/medical_video_causal_gate/docs/DATA_SELECTION_GATE.md (frozen gate; §2 criteria, §4, §7)
- /home/user/projects/medical_video_causal_gate/data_audit/AUDIT_TEMPLATE.md (verdict rules and output schema)

For EVERY dataset in your batch input file:
1. Find the official documentation: dataset paper, official dataset/challenge page, README, data card, licence page.
   Use WebSearch/WebFetch as needed. Prefer primary sources (authors' paper/page) over secondary ones.
2. Fill one JSON object per the template. Every D-verdict must carry an EXACT verbatim quote and its source URL/path.
   If documentation does not establish a criterion, the verdict is UNKNOWN (UNKNOWN is not PASS). Do not relax criteria.
3. Interpretation notes (apply consistently):
   - D1: human-annotated, time-stamped action labels (e.g. gestures, action triplets) or recorded robot/teleoperation
     commands/kinematics count as a "time-stamped action variable"; still state which. D1 also needs >=200 such
     trajectories by humans and the collection-mode condition.
   - D2: name the candidate outcome (e.g. task success, skill score, complication, error, a non-video sensor measurement
     after the action). Model-derived labels never qualify.
   - D3: continuous full recordings of a procedure/task episode = PASS; short clips or sampled frames only = FAIL.
   - D4: the factor must be recorded PER TRAJECTORY (per-video metadata, file naming documented as such, a per-case
     table). Dataset-level statements ("data from 3 centres") without per-trajectory assignment = FAIL or UNKNOWN
     (UNKNOWN if a per-trajectory file may exist but you could not inspect it publicly; say so).
   - D6: if only a number of videos is given, estimate size only when the documentation gives it; otherwise UNKNOWN.
   - D8: do not compute. Set FAIL with reason if no factor meets D4 or no variable meets D7; otherwise "PENDING-LEAD".
4. Restrictions: NO account creation, registration or acceptance of data-use terms; NO video download; you may fetch
   public documentation pages and small (<50 MB) public metadata/annotation files only if needed to verify a criterion,
   saving any file under /media/user/LaCie/medvideo_gate/<dataset id>/. Do not modify any repository file other than
   your output file. Do not touch ~/projects/video_causal_sim_1A or ~/projects/incremental_policy_bias_theory.
5. Write your output to /home/user/projects/medical_video_causal_gate/data_audit/audits/<BATCH>_audit.json as a JSON list
   (same order and ids as the input) and verify the count. Use /home/user/miniconda3/bin/python3 for writing.
6. Reply with a compact table: id | name | n_trajectories | D1..D8 | ge200 | registration, and list any dataset that
   (a) passes D3, D4, D5, D6, D7 and ge200 (SS-eligible pending D8), or (b) passes D1–D6 (RA-eligible).
