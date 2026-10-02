"""Consolidate the eight audit outputs into DATA_AUDIT_TABLE.csv (one row per dataset: verdict, quote and source per
criterion; counts), apply the lead verification (DS024, LEAD_VERIFICATION_SPEC.md) and gate §5 mechanically."""
import csv, glob, json, os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
order = ["col1", "col2", "surg1", "surg2", "surg3", "surg4", "openh1", "openh2"]
rows = []
for b in order:
    inp = json.load(open(f"{H}/audits/A_{b}_input.json")); inp = inp if isinstance(inp, list) else inp["datasets"]
    out = json.load(open(f"{H}/audits/A_{b}_audit.json"))
    assert [x["id"] for x in inp] == [x["id"] for x in out], b
    for x in out: x["batch"] = b; rows.append(x)
assert len(rows) == 194 and len({r["id"] for r in rows}) == 194
v = lambda r, k: (r.get(k) or {}).get("verdict", "") if isinstance(r.get(k), dict) else str(r.get(k, ""))
# lead verification override for DS024 (data_audit/lead/out/DS024_verification.json)
L = json.load(open(f"{H}/lead/out/DS024_verification.json"))
for r in rows:
    r["lead_note"] = ""
    if r["id"] == "DS024":
        r["lead_note"] = (f"LEAD (spec 4a6f2b1): {L['n_contiguous']}/{L['n_cases']} cases contiguous at 1.0 s (online {L['contiguous_by_recorder']['online (multitask)']}/140, "
                          f"offline {L['contiguous_by_recorder']['offline (stitch-coldcut)']}/96) -> ge200 FAIL, D1 FAIL (162 < 200); D4 PASS (3 qualifying levels on contiguous cases); "
                          f"D8 PASS (min V {min(x['all_levels']['V'] for x in L['D8'].values()):.3f})")
        r["lead_D1"], r["lead_D3"], r["lead_ge200"], r["lead_D8"] = "FAIL", "PASS for 162 contiguous cases; 74 online cases not contiguous", "FAIL", "PASS"
D = lambda r, k: r.get(f"lead_{k}") or v(r, k)
G = lambda r: r.get("lead_ge200") or str(r.get("ge200_trajectories", ""))
cols = ["id", "batch", "name", "category", "n_trajectories", "ge200", "registration"] + [f"{k}_{f}" for k in ["D1", "D2", "D3", "D4", "D5", "D6", "D7"] for f in ("verdict", "quote", "source")] + ["D8_verdict", "D8_reason", "counts", "lead_note", "notes"]
with open(f"{H}/DATA_AUDIT_TABLE.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows:
        row = dict(id=r["id"], batch=r["batch"], name=r.get("name", ""), category=r.get("category", ""), n_trajectories=r.get("n_trajectories"),
                   ge200=G(r), registration=r.get("registration_required", ""), counts=json.dumps(r.get("counts"), ensure_ascii=False),
                   D8_verdict=D(r, "D8"), D8_reason=(r.get("D8") or {}).get("reason", ""), lead_note=r["lead_note"], notes=r.get("notes", ""))
        for k in ["D1", "D2", "D3", "D4", "D5", "D6", "D7"]:
            o = r.get(k) or {}; row[f"{k}_verdict"] = D(r, k); row[f"{k}_quote"] = o.get("quote", ""); row[f"{k}_source"] = o.get("source", "")
        w.writerow(row)
P = lambda s: str(s).upper().startswith("PASS")
ss = [r for r in rows if all(P(D(r, k)) for k in ["D3", "D4", "D5", "D6", "D7", "D8"]) and P(G(r))]
ra = [r for r in rows if all(P(D(r, k)) for k in ["D1", "D2", "D3", "D4", "D5", "D6"])]
summ = dict(n=len(rows), SS_passing=[r["id"] for r in ss], RA_passing=[r["id"] for r in ra],
            D4_pass=[r["id"] for r in rows if P(D(r, "D4"))], ge200_pass=[r["id"] for r in rows if P(G(r))],
            ge200_unknown=[r["id"] for r in rows if G(r).upper().startswith("UNK")],
            verdict_counts={k: {s: sum(1 for r in rows if D(r, k).upper().startswith(s)) for s in ("PASS", "FAIL", "UNKNOWN", "PENDING")} for k in ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]})
json.dump(summ, open(f"{H}/lead/out/section5_inputs.json", "w"), indent=1); print(json.dumps(summ, indent=1))
for r in rows:
    if P(G(r)) or G(r).upper().startswith("UNK"):
        print(r["id"], "|", r.get("name", "")[:40], "| n", r.get("n_trajectories"), "| ge200", G(r), "| D3", D(r, "D3"), "| D4", D(r, "D4"), "| D5", D(r, "D5"), "|", ((r.get("D4") or {}).get("reason") or "")[:150])
