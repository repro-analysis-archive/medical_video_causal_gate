"""Write the per-dataset verdict appendix (markdown) from DATA_AUDIT_TABLE.csv."""
import csv, os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = list(csv.DictReader(open(f"{H}/DATA_AUDIT_TABLE.csv")))
ab = lambda s: {"PASS": "P", "FAIL": "F", "UNKNOWN": "U", "PENDING-LEAD": "pend"}.get(s.split()[0].rstrip(";,").upper() if s else "", s[:6])
lines = ["| id | name | n | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | ≥200 | reg. |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for r in R:
    nm = r["name"].replace("|", "/")[:60]
    lines.append(f"| {r['id']} | {nm} | {r['n_trajectories'] or '—'} | " + " | ".join(ab(r[f'D{i}_verdict']) for i in range(1, 8)) + f" | {ab(r['D8_verdict'])} | {ab(r['ge200'])} | {r['registration'][:8]} |")
open(f"{H}/lead/out/appendix_table.md", "w").write("\n".join(lines) + "\n"); print(len(R))
