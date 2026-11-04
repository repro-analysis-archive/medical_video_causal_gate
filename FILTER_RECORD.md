# FILTER_RECORD — 01 `medical_video_causal_gate`

* Rule: §0 uniform rule: whole copies of third-party material (decision D9 final) — 1,636 paths: `data_audit/lead/fm_sources/` in full (1,068 files), raw API responses / saved pages in `data_audit/runs/` (73) and `lit/runs/` (473), and 22 LLM-screening input batches that consist of the fetched abstracts (`lit/screening/`, `data_audit/screening/`). Kept: the authors' notes, scripts, decisions, derived audit tables / records (117 of them embed some third-party quotation → `CHECKS/01_derived_tables_questions.md`), `lit/runs/**/*.log`, `venues_resolved.json`, `seed_candidates.json`, the adapters (decision (a)).
* Tool: git-filter-repo a40bce548d2c (git-filter-repo 2.47.0); `git clone --no-hardlinks <original bundle> repo/`; `git filter-repo --invert-paths --paths-from-file removed_paths.txt --preserve-commit-hashes --force` (log: `filter-repo.log`).
* `repo/` is the filtered repository (clean working tree, no remote, not to be modified before push day; push-day additions are made in a copy). `removed_paths.txt`: exact paths removed from the whole history. `commit-map.raw`: filter-repo's commit map. `COMMIT_ID_MAP.md`: old → new with subjects. `verification.json`: the checks below.

## Checks (all passed)

| check | result |
|---|---|
| commits original → public (pruned / unmapped) | 67 → 67 (0 / 0) |
| `git fsck --full --strict` | exit 0, no output |
| `git log --all -- <every removed path>` | 0 commits |
| `git rev-list --objects --all`: blobs of removed files present / removed path names present | 0 / 0 (the empty blob is shared with a kept 0-byte file: not removed material) |
| removed paths ever in the history (blob versions) | 1583 (1586) |
| HEAD files original → public; only in original | 2069 → 433; 1636 (all in the removed list: True) |
| HEAD: files only in public / with changed content | 0 / 0 |
| every commit: tree differs from the original tree only by the removed paths | yes (all 67) |
| commit messages and commit / author dates unchanged | yes |
| identities (author \| committer) | Hisashi Nakano <hisashi-nakano@nuhw.ac.jp> | Hisashi Nakano <hisashi-nakano@nuhw.ac.jp> |
| remotes in `repo/` | 0 |
| HEAD original → public | `2880d73` → `f72a7db` |
| frozen protocol file `docs/SS_PROTOCOL_DS203.md`, SHA-256 | `cd7e1402…d748926` equal in the original at `4c86dc5` and in the public copy at the mapped commit `2661846` and at HEAD |
