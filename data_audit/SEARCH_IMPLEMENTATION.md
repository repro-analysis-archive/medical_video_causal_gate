# Data Audit — Dataset Search Implementation (committed before any dataset search)

Implements §3 of `docs/DATA_SELECTION_GATE.md` (frozen `baadf5c`). It fixes only mechanics the gate leaves open.
Before this commit, only reachability probes were made (one request per source); their responses are not used.

## 1. Queries and depth

* **Queries:** the five fixed queries, as plain-text keyword queries in each engine's default relevance order:
  * "colonoscopy video dataset"
  * "full-procedure colonoscopy"
  * "endoscopy video dataset multi-center"
  * "surgical video dataset"
  * "surgical kinematics video dataset"
* **Depth:** the first 50 results per query per source.
* **No record-type filter** is applied. Screening decides whether a record describes a dataset.

## 2. Sources

| source | mechanism | note |
|---|---|---|
| OpenAlex | `works?search=<query>&per-page=50` (relevance) | |
| Semantic Scholar | `graph/v1/paper/search?query=<query>&limit=50` | runs on the same paced client as the literature search, after it, because of HTTP 429 limits. If unavailable, reported as BLOCKED |
| Hugging Face | `api/datasets?search=<query>&limit=50` | engine default. The HF search matches repository ids, so multi-word queries may return few or no records; that is logged as is |
| Grand-Challenge | `api/v1/challenges/`, **the complete public listing** (all pages) | the API has no search filter (probe: the same 264 records for any query). Every challenge is screened, which is a superset of "first 50 per query" |
| Synapse | `repo/v1/search`, with `queryTerm` = the query's words, `size=50` | anonymous search |
| PhysioNet | `physionet.org/content/?q=<query>` (HTML), the first 50 project links | |
| Zenodo | `api/records?q=<query>&size=50&sort=bestmatch` | |
| Figshare | `POST v2/articles/search`, with `search_for=<query>` and `page_size=50` | |
| EndoVis | every sub-challenge linked from `endovis.grand-challenge.org` and its year pages | the gate's "every EndoVis dataset" |

## 3. Screening and audit

* **Screening:** each record is screened on title and description into **DATASET-C-COL**, **DATASET-C-SURG**,
  **DATASET-OTHER** (a dataset, but not C-COL / C-SURG) or **NOT-DATASET**.
  * Records describing the same dataset are merged into one dataset entry.
  * CathAction (C-CATH) is audited regardless of search hits.
  * Every screened record is logged in `data_audit/RECORDS.csv`.
* **Audit:** every C-COL / C-SURG dataset entry, plus C-CATH, gets a D1–D8 audit (gate §4).
  * The audit uses documentation, metadata and annotation files only.
  * Each verdict quotes its source line, or names the file path.
  * UNKNOWN is not PASS.
  * Datasets that need registration are audited from public documentation only. No account is created and no terms
    are accepted.
* **Downloads:** annotation and metadata files only, plus at most one sample video per dataset, placed under
  `/media/user/LaCie/medvideo_gate/` (not the H1R raw disk).
  * Allowed on the sample: container metadata and a few frames.
  * Nothing more: no computation on video, no representation extraction, no model.
