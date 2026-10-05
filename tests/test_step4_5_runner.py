"""Fast tests of the step 4-5 runner's STOP / provenance helpers (no video, no GPU, no DS203 data).

    /home/user/.venvs/ss_extract/bin/python -m pytest -p no:cacheprovider tests/test_step4_5_runner.py
"""
import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
import step4_5_orchestrate as orch  # noqa: E402


def mc(rho, r, n_frames=10):
    return dict(visible_radius={c: v for c, v in rho.items()}, r=r,
                profiles={c: dict(n_frames=n_frames) for c in rho})


def test_mask_check_rule_and_single_fallback():
    ok, msg = orch.validate_mask_check(mc(dict(zip("2345", (0.47, 0.5, 0.49, 0.46))), 0.45))
    assert ok and "stands" in msg
    ok, msg = orch.validate_mask_check(mc(dict(zip("2345", (0.40, 0.5, 0.49, 0.46))), 0.98 * 0.40))
    assert ok and "fallback" in msg
    assert not orch.validate_mask_check(mc(dict(zip("2345", (0.40, 0.5, 0.49, 0.46))), 0.45))[0]   # not the rule
    assert not orch.validate_mask_check(mc(dict(zip("2345", (0.0, 0.5, 0.49, 0.46))), 0.0))[0]     # fallback fails
    assert not orch.validate_mask_check(mc(dict(zip("234", (0.47, 0.5, 0.49))), 0.45))[0]           # centre missing
    assert not orch.validate_mask_check(mc(dict(zip("2345", (0.47, 0.5, 0.49, 0.46))), 0.45, 0))[0]


def test_step6_unreachable_and_records_only_set():
    assert orch.PIPELINE_COMMANDS == {"mask-check", "extract", "near-uniform", "build-reps", "checks"}
    src = open(os.path.join(REPO, "scripts", "step4_5_orchestrate.py")).read()
    for word in ("grid_driver", "run_grid", "causal grid run"):
        assert word not in src
    assert all(p.startswith("results/step4/") for p in orch.RECORD_FILES) and len(orch.RECORD_FILES) == 10


def test_launch_rejects_other_pipeline_commands(tmp_path):
    r = orch.Runner.__new__(orch.Runner)
    r.snap = str(tmp_path)
    with pytest.raises(orch.Stop):
        r.launch(1, "grid")
    assert r.launch(2, "checks", "--out", "x")[-3:] == ["checks", "--out", "x"]


def test_third_party_digest_pinned():
    for d, dig in orch.THIRD_PARTY_DIGEST.items():
        p = os.path.join(REPO, "third_party", d)
        if not os.path.isdir(p):
            pytest.skip("third_party not present")
        assert orch.third_party_digest(p)[0] == dig


def test_runner_script_refuses_without_expect_commit(tmp_path):
    r = subprocess.run(["bash", os.path.join(REPO, "scripts", "run_step4_5.sh"), "--out", str(tmp_path)],
                       capture_output=True, text=True)
    assert r.returncode == 3 and "refused" in r.stderr


def _git(repo, *a):
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout.strip()


def test_verify_record_commit_records_only(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.name", "t"); _git(repo, "config", "user.email", "t@example.invalid")
    (repo / "a.txt").write_text("a")
    _git(repo, "add", "."); _git(repo, "commit", "-q", "-m", "launch")
    launch = _git(repo, "rev-parse", "HEAD")
    r = orch.Runner.__new__(orch.Runner)
    r.repo = str(repo)

    def record_commit(extra=None, prefix=orch.RECORD_PREFIX):
        _git(repo, "checkout", "-q", "--detach", launch)
        for p in orch.RECORD_FILES:
            (repo / p).parent.mkdir(parents=True, exist_ok=True)
            (repo / p).write_text(p)
        if extra:
            (repo / extra).write_text("x")
        _git(repo, "add", "-A"); _git(repo, "commit", "-q", "-m", f"{prefix}: test")
        return _git(repo, "rev-parse", "HEAD")

    r.verify_record_commit(record_commit(), launch)                                    # exactly the ten files
    with pytest.raises(orch.Refuse):
        r.verify_record_commit(record_commit(extra="a.txt"), launch)                   # a non-record path changed
    with pytest.raises(orch.Refuse):
        r.verify_record_commit(record_commit(prefix="other"), launch)                  # not the runner's commit
    rec = record_commit()
    with pytest.raises(orch.Refuse):
        r.verify_record_commit(rec, rec)                                               # parent is not the launch


def test_step5_record_written_not_committed(tmp_path):
    import threading
    repo = tmp_path / "r"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.name", "t"); _git(repo, "config", "user.email", "t@example.invalid")
    (repo / "a.txt").write_text("a")
    _git(repo, "add", "."); _git(repo, "commit", "-q", "-m", "record")
    head = _git(repo, "rev-parse", "HEAD")
    s5 = tmp_path / "s5"
    s5.mkdir()
    for f in ("checks.json", "reps_report.json"):
        (s5 / f).write_text("{}")
    (s5 / "reps.npz").write_bytes(b"x")
    r = orch.Runner.__new__(orch.Runner)
    r.repo, r.out, r.state = str(repo), str(tmp_path / "out"), {"record_commit": head}
    r.state_p, r.lock = str(tmp_path / "state.json"), threading.RLock()
    os.makedirs(r.out)
    r.write_step5_record(str(s5))
    got = sorted(os.listdir(repo / "results" / "step5"))
    assert got == ["STEP5_RECORD.md", "checks.json", "reps_report.json", "step5_manifest.json"]
    assert _git(repo, "rev-parse", "HEAD") == head                          # never committed
    assert _git(repo, "status", "--porcelain").startswith("?? results/")
    assert r.state["stages"]["step5_record"]["status"] == "done"


def test_completed_run_refuses_relaunch():
    r = orch.Runner.__new__(orch.Runner)
    r.state = {"status": "complete"}
    with pytest.raises(orch.Refuse):
        r.run()
