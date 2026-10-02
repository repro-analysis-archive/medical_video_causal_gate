# Literature Gate — Search Implementation (committed before any content search)

Implements §6 of `docs/DATA_SELECTION_GATE.md`, frozen at **`baadf5c`** (2026-10-02 11:57:25 +0900). This file only
fixes mechanics the gate leaves open. It changes no claim, grade, consequence, query, database or stopping rule.

**Before this commit,** only API reachability and venue-name probes were made. Their responses (one Semantic Scholar
venue lookup per test paper, and one test query) are not screened or used.

## 1. Fixed parameters

* **Date window:** 2018-01-01 to 2026-10-02 (the freeze date).
* **Queries:** Q1–Q4 exactly as in §6.
  * Multi-word terms are treated as phrases: "medical video", "surgical video", "ultrasound video", "treatment
    effect", "foundation model", "image embedding", "deep features", "medical image", "semi-synthetic",
    "domain-invariant", "site-invariant", "time-varying".
  * Every other term is a single word.
* **Depth:** 100 records per query per database, in the engine's relevance order.

## 2. Engines

| database | engine | boolean | translation |
|---|---|---|---|
| PubMed | NCBI E-utilities `esearch` (`sort=relevance`, `retmax=100`, `datetype=pdat`), then `efetch` for abstracts | native | the query as written, with phrases in double quotes |
| arXiv (cs.CV, cs.LG, stat.ME, stat.ML) | export API (`sortBy=relevance`, `max_results=100`) | native | each term becomes `all:"term"`, combined with the query's AND / OR, plus `AND (cat:cs.CV OR cat:cs.LG OR cat:stat.ME OR cat:stat.ML) AND submittedDate:[201801010000 TO 202610022359]` |
| OpenAlex | `works?search=` (default relevance order), `filter=from_publication_date:2018-01-01,to_publication_date:2026-10-02`, `per-page=100`, page 1 | native (AND / OR, parentheses, quoted phrases) | the query as written |
| Semantic Scholar | `graph/v1/paper/search` (relevance), `publicationDateOrYear=2018-01-01:2026-10-02`, `limit=100` | **not supported, so the query is split** (see §3) | sub-queries in plain text |
| Proceedings of MICCAI, IPMI, MIDL, NeurIPS, ICML, CLeaR, UAI | the same Semantic Scholar relevance search, with the `venue` filter set to the seven venues' Semantic Scholar names (resolved by probing and recorded in the run log) | not supported, so the query is split (§3) | as for Semantic Scholar |

**Why the proceedings use Semantic Scholar.** OpenAlex was checked as an alternative and rejected: its venue records
are far from complete (for example 38 MICCAI works and 66 MIDL works, and CLeaR is absent).

## 3. Split rule for engines without boolean support

* **Sub-queries:** one sub-query for each element of the Cartesian product of the query's OR-blocks, taking one term
  from each block in the order written. That gives Q1 120 (6 × 5 × 4), Q2 36, Q3 4 and Q4 60 sub-queries.
  (Erratum, before any search: an earlier version of this line said Q1 150. The rule is unchanged; only the derived
  count was miscounted.)
* **Merge:** the ranked lists are merged round-robin by rank (rank 1 of every sub-query in order, then rank 2, and so
  on). Records are deduplicated by Semantic Scholar paper id, and the merge stops at **100 unique records per query
  per database**.
* **Logging:** every sub-query string, and its returned list, is logged.

## 4. Availability rule

* Semantic Scholar rate-limits unauthenticated use (HTTP 429 was observed during probing).
* The client paces requests and backs off on 429.
* **If Semantic Scholar remains unavailable**, the Semantic Scholar and proceedings arms are reported as **BLOCKED
  (needs an API key: investigator action)**. They are **not** replaced by another engine, because the database list
  is frozen. The other three databases still run.

## 5. Deduplication, screening and grading

* **Deduplication** across databases: by DOI, then arXiv id, then PMID, then normalized title (lower case,
  alphanumerics only).
* **Screening** (title + abstract) assigns each unique record one of:
  * **NONE** or **RELATED**, final at screening;
  * **FULLTEXT**: a possible DIRECT / PARTIAL for any of L1–L4, to be read in full.
* **When FULLTEXT applies** (any one is enough):
  * (L1) learned, foundation or generative image / video / text representations are used as **adjustment covariates
    or confounder proxies** for a causal effect of an action or treatment;
  * (L2) learned representations are analysed as carrying **acquisition information** (site, scanner, device,
    operator, batch) that affects **bias, confounding adjustment or overlap** in causal estimation;
  * (L3) a **semi-synthetic causal benchmark** built on real medical images or video;
  * (L4) the causal role of acquisition information in representations, as a function of **duration or
    persistence**, or the effect of **site-invariant, harmonized or debiased representations on causal estimation
    in longitudinal or sequential settings**.
* **RELATED:** adjacent but none of the above. Examples: site or shortcut leakage in embeddings with no causal
  estimation; causal inference with images but without learned representations as adjustment; generic
  identification theory (§6 rule).
* **Records without an abstract** are screened on title, venue and keywords. If a FULLTEXT criterion cannot be ruled
  out, the record is marked FULLTEXT.
* **Who screens:** the lead analyst, or subagents working to this rubric. A subagent may assign NONE, RELATED or
  FULLTEXT. **Only the lead analyst assigns DIRECT or PARTIAL**, and only after reading the full text, with a quoted
  passage and its page or section. A full text that cannot be obtained or read gives **UNRESOLVED**.
* **Known prior work** (§6) is graded under the same rules: full text, by the lead analyst.

## 6. Citation chasing (§6 stopping rule)

* For each DIRECT or PARTIAL hit, one level backward (its references) and one level forward (works citing it) is
  collected from **OpenAlex** (`referenced_works`, `cites:` filter), and screened under §5.
* OpenAlex is used here because the gate fixes no engine for citations and OpenAlex is available.

## 7. Files (`lit/`)

* `runs/`: raw API responses per database × query or sub-query.
* `RECORDS.csv`: every screened record, with database, query, rank, ids, title, year, venue, screening decision,
  reason and screener.
* `FULLTEXT_NOTES.md`: full-text readings, quotes and grades.
* `LIT_GATE_RESULT.md`: tables per claim L1–L4, the §6 consequence, and the UNRESOLVED list.
