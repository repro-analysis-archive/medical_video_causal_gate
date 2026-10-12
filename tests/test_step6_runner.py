"""Fast tests of the step-6 runner helpers and the mechanical §13 application (no real data, no grid run).

    /home/user/miniconda3/bin/python3 -m pytest -p no:cacheprovider tests/test_step6_runner.py
"""
import copy
import json
import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
import apply_section13 as s13  # noqa: E402
import step6_orchestrate as orch  # noqa: E402


def fixture_checks(**over):
    """FIXTURE checks.json with the locked field layout (pipeline.run_checks); every check passing."""
    ok = {"pass": True}
    fm = {"E1_278": dict(ok), "E1_primary": dict(ok), "E2_primary": dict(ok),
          "E3_site_278": {"pass": True, "mlp_exceeds_margin": False},
          "E3_site_primary": {"pass": True, "mlp_exceeds_margin": False},
          "E3_state_primary": {"applicable": True, "pass_": True},
          "fm_conditions_primary": {"E1": True, "E3-site": True, "E3-state": True}}
    c = {k: copy.deepcopy(fm) for k in ("P", "S", "REF")}
    c["P-nat"] = {"E1_278": dict(ok), "E1_primary": dict(ok), "E2_primary": dict(ok)}
    for path, v in over.items():
        k, *rest = path.split(".")
        d = c[k]
        for r in rest[:-1]:
            d = d[r]
        d[rest[-1]] = v
    return c


def triggered(checks, gsite_pass=True):
    rules, cond, tested = s13.evaluate(checks, {"gate_pass_primary": gsite_pass})
    return {(r["rule"], r["scope"]) for r in rules if r["triggered"]}, cond, tested


def test_all_pass_triggers_only_wording():
    t, cond, tested = triggered(fixture_checks())
    assert {r for r, _ in t} == {"E3site_passes_wording"}
    assert all(cond.values()) and all(tested.values())


def test_e1_fail_278_and_158_fail_rules():
    t, _, _ = triggered(fixture_checks(**{"S.E1_278.pass": False}))
    assert ("E1_fails", "FM-S / FM-S−C") in t
    t, cond, tested = triggered(fixture_checks(**{"P.E3_site_primary.pass": False,
                                                  "P.fm_conditions_primary.E3-site": False}))
    assert ("pass278_fail158", "FM-P / FM-P−C") in t
    assert cond["E3-site"] is False and tested["P1b-FM"] is False and tested["P2-FM"] is False


def test_mlp_margin_state_and_gsite():
    t, _, _ = triggered(fixture_checks(**{"REF.E3_site_278.mlp_exceeds_margin": True}))
    assert ("mlp_margin", "REF / REF−C, 278-case set") in t
    t, _, _ = triggered(fixture_checks(**{"P.E3_state_primary.applicable": False}))
    assert ("E3state_na", "FM-P / FM-P−C") in t and ("E3state_fails", "FM-P / FM-P−C") not in t
    t, _, _ = triggered(fixture_checks(**{"P.E3_state_primary.pass_": False}))
    assert ("E3state_fails", "FM-P / FM-P−C") in t
    t, _, tested = triggered(fixture_checks(), gsite_pass=False)
    assert ("GSITE_fails", "design (code lock)") in t and not tested["P2-SITE"] and tested["P1b-SITE"]


def test_non_boolean_field_stops():
    with pytest.raises(SystemExit):
        s13.evaluate(fixture_checks(**{"P.E1_278.pass": None}), {"gate_pass_primary": True})


def test_records_written(tmp_path):
    cp = tmp_path / "checks.json"
    gp = tmp_path / "gsite.json"
    cp.write_text(json.dumps(fixture_checks()))
    gp.write_text(json.dumps({"gate_pass_primary": True}))
    s13.main(["--checks", str(cp), "--gsite", str(gp), "--out-dir", str(tmp_path / "o")])
    assert sorted(os.listdir(tmp_path / "o")) == ["SECTION13_RECORD.md", "grid_conditions.json", "section13.json"]
    assert json.load(open(tmp_path / "o" / "grid_conditions.json")) == {
        "primary": {"E1": True, "E3-site": True, "E3-state": True}}


def test_memory_guard_ignores_swap_and_fires_on_real_pressure():
    G = 2**30
    total = 125.6 * G
    ok = {"MemTotal": total, "MemAvailable": 80 * G}
    assert orch.pressure_reasons(ok, {"some": 0.25, "full": 0.25}, 3 * G, 0.8 * total) == []     # 6 Oct situation
    assert orch.pressure_reasons({"MemTotal": total, "MemAvailable": 4 * G}, None, 3 * G, 0.8 * total)
    assert orch.pressure_reasons(ok, {"some": 30.0, "full": 12.0}, 3 * G, 0.8 * total)
    assert orch.pressure_reasons(ok, None, 101 * G, 0.8 * total)


def test_step7_never_called_by_launcher():
    src = open(os.path.join(REPO, "scripts", "step6_grid_units.py")).read()
    assert "grid_driver.aggregate = _no_step7" in src
    orch_src = open(os.path.join(REPO, "scripts", "step6_orchestrate.py")).read()
    assert "aggregate(" not in orch_src and "families.json" in orch_src     # only named in the docstring / record


def test_runner_refuses_without_expect_commit(tmp_path):
    r = subprocess.run(["bash", os.path.join(REPO, "scripts", "run_step6.sh"), "--out", str(tmp_path)],
                       capture_output=True, text=True)
    assert r.returncode == 3 and "refused" in r.stderr
