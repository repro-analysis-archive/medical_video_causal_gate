# Per-Dataset Audit Template and Verdict Rules (fixed before any dataset documentation is read)

Applies gate `baadf5c` §§2–5 to every entry of `DATASETS.json`. The list contains 194 entries:
* 110 from the §3 search, after merging records that describe the same dataset;
* CathAction (C-CATH);
* the 83 Open-H surgical and endoscopy subsets. §3 names Open-H explicitly, and the HF search returned no records for
  the fixed queries.

## Output per dataset (JSON)

```
{id, name, category, sources_consulted: [urls / file paths],
 trajectory_unit: "...", n_trajectories: <int or null>, n_trajectories_quote: "...",
 D1..D7: {verdict: PASS|FAIL|UNKNOWN, quote: "exact text", source: url-or-path},
 D8: {verdict, reason},
 ge200_trajectories: PASS|FAIL|UNKNOWN,
 counts: {collection_mode, site, device, operator, annotation_type},
 registration_required: yes|no|unknown, notes}
```

## Verdict rules (verbatim criteria from §2; mechanics added here)

* **Unit.** One trajectory is one continuous recording of one procedure. Clips from the same procedure count once.
* **D1.** PASS only if all three hold:
  * a time-stamped action variable is recorded per trajectory;
  * actions are chosen by clinicians or human operators for at least 200 trajectories;
  * collection mode is identifiable per trajectory, OR the documentation states that no programmatic / state-machine
    collection exists.
* **D2.** PASS only if the outcome is on the same trajectory, after the action, and comes from human annotation or a
  sensor measurement independent of the video. Model-derived labels do not qualify.
* **D3.** PASS only if the frames are time-aligned and contiguous: continuous procedure recordings, not isolated
  clips or frames.
* **D4.** PASS only if, for at least one of site / device / operator, at least 2 levels each have at least 20
  trajectories, **recorded per trajectory**. Documentation that gives only dataset-level counts fails.
* **D5.** PASS only if the licence permits research use **and** release of derived features. Unclear licence:
  UNKNOWN.
* **D6.** PASS only if the total size including video is at most 2.02 TB. That limit is the 6.07 TB free on LaCie, the
  non-H1R disk, divided by 3. Size not documented: UNKNOWN.
* **D7.** PASS only if a frame- or segment-level content variable exists (human annotation or sensor ground truth of
  scene state) that varies within trajectories and is not acquisition metadata.
* **D8.** Evaluated only if at least one factor meets D4 and at least one variable meets D7. Otherwise it is **FAIL**,
  with the reason stated. When it is evaluated, it is computed by the lead analyst from the annotation and metadata
  files: trajectory-weighted Cramér's V.
* **UNKNOWN is not PASS.** Each verdict carries the exact quote and its source.

## Restrictions (§7)

* Documentation, metadata and annotation files only.
* No video download by audit agents. At most one sample video per dataset, and only by the lead analyst if needed.
* No account creation, registration or acceptance of data-use agreements. Registration-gated material is audited from
  public pages only, and the need for registration is recorded.
