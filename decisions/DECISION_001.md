# Decision 001: Amendment 1 trigger met; Amendment 1 ACTIVE

Investigator decision, recorded by the lead analyst.

## 1. The trigger is met

* The three access-gated datasets named in Amendment 1 are audited, and none passes the SS arm:
  * SAGES CVS: Erratum 002;
  * CathAction: Erratum 003;
  * Trauma THOMPSON: Erratum 004.
* **The v4 criteria were not relaxed.** Amendment 2 (`ebc097d`) adds a requirement and does not relax v4.
* **Under v4 alone, the result is the same.** UNKNOWN is not PASS (`data_audit/DATA_AUDIT_TABLE.csv`):
  * Trauma THOMPSON: D4 UNKNOWN;
  * CathAction: D4 not documented (UNKNOWN);
  * SAGES CVS: D3 FAIL and D5 FAIL.

## 2. Amendment 1 is ACTIVE

The SS' arm of Gate Amendment 1 (`6e78eca`) applies, together with Amendment 2's requirement of in-vivo human clinical
video.

## 3. When ranking happens

* The SS' ranking is applied **once**, after the Semantic Scholar arms of gate §6 (literature) and §3 (dataset search)
  have run.
* **No partial ranking before then.**
