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

## Step 2 — third-party e-mail addresses replaced (2026-11-04)

* Rule: four e-mail addresses of third parties (three personal professional addresses, one organisational address), quoted in four derived audit records — quotations of published dataset-access instructions and of a paper's corresponding-author line — are replaced by the literal `[e-mail address removed]` in every version of these files in the whole history. Files (one version each in the history; 10 occurrences): `data_audit/DATA_AUDIT_TABLE.csv`, `data_audit/audits/A_col2_audit.json`, `data_audit/audits/A_surg3_audit.json`, `data_audit/lead/out/dataset_provenance.json`. Not changed: the authors' contact address, `noreply@anthropic.com` in the commit trailers, and the placeholder `t@example.invalid` in a test. In `dataset_provenance.json` the keyword-context windows that contained an address are therefore no longer of fixed width.
* Tool: git-filter-repo a40bce548d2c (git-filter-repo 2.47.0); in a fresh copy of the release repository, `git filter-repo --replace-text <expressions file> --preserve-commit-hashes --force` (the expressions file lists the four literal addresses and is not published). An earlier pre-release build of 2026-11-04 (private repository and unpublished archive draft only) is superseded; its commit IDs were never public.

| check | result |
|---|---|
| commits before → after (pruned) | 70 → 70 (0) |
| commits keeping their ID | 16 (commits 1–16); commits 17–70 get new IDs (the first is the commit that added `A_col2_audit.json`) |
| paths with changed content in any commit (trees compared commit by commit) | the four files above only |
| every changed file = its previous version with the literal replacement applied | yes (byte comparison) |
| JSON files | valid; same keys, nesting, types and non-string values; only the 6 strings that contained an address differ |
| CSV file | 195 rows (header included), same columns; 4 cells differ, each only by the replacement |
| commit messages, authors, committers, author / commit dates | unchanged (all 70); parents map one to one |
| the four addresses in any reachable object (case-insensitive; also `%40`, `[at]`, `(at)`) | 0 |
| `git fsck --full --strict` | no problems |
| frozen protocol `docs/SS_PROTOCOL_DS203.md`, SHA-256 | `cd7e1402…d748926` at the mapped freeze commit `e312b8b71c7568cc5b8e36967c597288942e3eea` and at HEAD |

`COMMIT_ID_MAP.md` maps every original ID to the ID after both steps.
