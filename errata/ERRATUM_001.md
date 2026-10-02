# Erratum 001: commit-message errors in `4a6f2b1`

History is not rewritten. This file corrects the record.

* **Commit:** `4a6f2b1`, "Data audit: lead verification + D8 spec committed before any parquet/annotation value is
  read".
* **Error 1.**
  * The message says "DATASETS.json display names for 31 untitled entries".
  * **The correct number is 11.** Check: `git show 4a6f2b1 -- data_audit/DATASETS.json` removes `"names": [],` 11 times.
* **Error 2.**
  * The message says three batches, surg2–4, were "still running".
  * The commit nevertheless included `data_audit/audits/A_surg4_audit.json`, as it then stood on disk (13:29:50, 18
    entries), **before the surg4 agent had reported back**.
  * The final version, committed in `dd142f6`, differs in two places:
    * one quote's whitespace (DS169 D5: "proper citation. ||" → "proper citation ||");
    * one count inside a reason (DS171 D7: 149/155 → 150/155 cases).
  * **No verdict changed.**
* **Effect on results:** none. The DS024 verification and §5 application (`dd142f6`) read the final files.
