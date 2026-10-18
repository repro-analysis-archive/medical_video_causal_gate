"""Tests of the §14 step-7 runner (scripts/run_step7.sh, scripts/step7_orchestrate.py); PLACEHOLDER only.

Fast tests (no grid run):

    /home/user/miniconda3/bin/python3 -m pytest -p no:cacheprovider tests/test_step7_runner.py

The integration test R1-R7 is opt-in (a few minutes). It clones this repository into a temporary directory, adds the
step-7 files from the working tree to the clone if they are not committed yet, runs a tiny PLACEHOLDER step 6 there
(cell 0, 1 replicate) into a temporary output directory, and exercises run_step7.sh against it. The real repository
and the real step-6 output are never touched (the step-6 runner itself refuses PLACEHOLDER output under the real
step-6 directory; the test also checks that the real repository's HEAD and status are unchanged):

    SS_STEP7_INTEGRATION=1 /home/user/miniconda3/bin/python3 -m pytest -p no:cacheprovider -s -v \
        tests/test_step7_runner.py
"""
import os
import shutil
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
import step7_orchestrate as s7  # noqa: E402

REAL_OUT6 = "/media/user/LaCie/medvideo_gate/ss_step6"
STEP7_FILES = ("scripts/run_step7.sh", "scripts/step7_orchestrate.py", "decisions/STEP7_PROCEDURE.md",
               "decisions/PRESENTATION_DECISIONS.md", "decisions/OPERATIONS_LOG_ADDENDUM_STEP4_5.md",
               "tests/test_step7_runner.py")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", GIT_OPTIONAL_LOCKS="0")


def run(cmd, cwd=None, timeout=3600):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=ENV, timeout=timeout)


def git(repo, *args):
    r = run(["git", "-C", repo, *args])
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


# ---------------------------------------------------------------------------------------------------------- fast --
def test_refuses_without_expect_commit(tmp_path):
    r = run(["bash", os.path.join(REPO, "scripts", "run_step7.sh"), "--out6", str(tmp_path)])
    assert r.returncode == 3 and "refused" in r.stderr
    assert os.listdir(tmp_path) == []                                   # nothing written


def test_status_not_started(tmp_path):
    r = run(["bash", os.path.join(REPO, "scripts", "run_step7.sh"), "--status", "--out6", str(tmp_path)])
    assert r.returncode == 0 and r.stdout.strip() == "step 7: not started"


def test_preflight_refuses_incomplete_step6(tmp_path):
    (tmp_path / "state.json").write_text('{"status": "running"}')
    a = type("A", (), dict(repo=REPO, out6=str(tmp_path), expect_commit="0" * 40))()
    with pytest.raises(s7.Refuse, match="step 6 is not complete"):
        s7.Step7(a).preflight()


def test_records_only_and_no_analysis_writes():
    assert set(s7.RECORDS) == {"results/step6/run_record.json", "results/step6/shard_sha256.txt.gz",
                               "results/step7/families.json", "results/step7/cell_metrics.csv",
                               "results/step7/step7_manifest.json", "results/step7/STEP7_RECORD.md"}
    src = open(os.path.join(REPO, "scripts", "step7_orchestrate.py")).read()
    assert "ss_benchmark.grid_driver" in src and "cwd=self.snap" in src     # locked driver, step-6 snapshot
    for bad in ('open(os.path.join(self.repo, "ss_benchmark', "git(self.repo, \"add\", \"-A\"",
                "git(self.repo, \"add\", \".\""):
        assert bad not in src
    assert s7.STEP6_FILES == ("scripts/run_step6.sh", "scripts/step6_orchestrate.py", "scripts/step6_grid_units.py")


# ---------------------------------------------------------------------------------------------- integration R1-R7 --
@pytest.mark.skipif(os.environ.get("SS_STEP7_INTEGRATION") != "1", reason="opt-in: SS_STEP7_INTEGRATION=1")
def test_step7_runner_placeholder_clone(tmp_path):
    real_head, real_status = git(REPO, "rev-parse", "HEAD"), git(REPO, "status", "--porcelain", "--untracked-files=all")
    clone, out6, empty = str(tmp_path / "repo"), str(tmp_path / "out6"), str(tmp_path / "empty")
    os.makedirs(empty)
    assert not out6.startswith(REAL_OUT6)
    git(tmp_path, "clone", "--quiet", "--no-hardlinks", REPO, clone)
    for k in ("user.name", "user.email"):
        git(clone, "config", k, git(REPO, "config", "--get", k))
    for f in STEP7_FILES:                                     # the step-7 commit, if not yet in the real HEAD
        os.makedirs(os.path.dirname(os.path.join(clone, f)), exist_ok=True)
        shutil.copy2(os.path.join(REPO, f), os.path.join(clone, f))
    if git(clone, "status", "--porcelain", "--untracked-files=all"):
        git(clone, "add", "--", *STEP7_FILES)
        git(clone, "commit", "-q", "-m", "PLACEHOLDER test: step-7 runner files")
    head = git(clone, "rev-parse", "HEAD")
    r7 = os.path.join(clone, "scripts", "run_step7.sh")

    def step7(exp, out=out6):                                  # run_step7.sh tees the orchestrator's 2>&1
        r = run(["bash", r7, "--expect-commit", exp, "--out6", out], cwd=clone)
        r.stderr = (r.stdout + r.stderr).strip()
        return r

    r = step7(head, empty)
    print(f"R1 step 6 not complete (empty out6): exit {r.returncode} | {r.stderr.strip()[-90:]}")
    assert r.returncode == 3 and "step 6 is not complete" in r.stderr

    r = run(["bash", os.path.join(clone, "scripts", "run_step6.sh"), "--expect-commit", head, "--out", out6,
             "--placeholder", "--cells", "0", "--max-reps", "1", "--workers", "1"], cwd=clone)
    st = run(["bash", os.path.join(clone, "scripts", "run_step6.sh"), "--status", "--out", out6]).stdout
    print(f"PLACEHOLDER step 6 (cell 0, 1 replicate): exit {r.returncode} | {' | '.join(st.splitlines()[:2])}")
    assert r.returncode == 0 and "state complete" in st and "PLACEHOLDER" in st

    r = step7(git(clone, "rev-parse", "HEAD^"))
    print(f"R2 --expect-commit != HEAD: exit {r.returncode} | {r.stderr.strip()[-90:]}")
    assert r.returncode == 3 and "is not --expect-commit" in r.stderr

    open(os.path.join(clone, "stray.txt"), "w").write("x")
    r = step7(head)
    os.remove(os.path.join(clone, "stray.txt"))
    print(f"R3 untracked file: exit {r.returncode} | {r.stderr.strip()[-90:]}")
    assert r.returncode == 3 and "working tree not clean" in r.stderr

    work = os.path.join(out6, "grid", "work")
    sd = sorted(os.listdir(work))[0]
    shard = os.path.join(work, sd, sorted(os.listdir(os.path.join(work, sd)))[0])
    orig = open(shard, "rb").read()
    open(shard, "ab").write(b" ")
    r = step7(head)
    open(shard, "wb").write(orig)
    print(f"R4 tampered shard: exit {r.returncode} | {r.stderr.strip()[-90:]}")
    assert r.returncode == 3 and "digest mismatch" in r.stderr

    with open(os.path.join(clone, "ss_benchmark", "constants.py"), "a") as f:
        f.write("\n# PLACEHOLDER test change\n")
    git(clone, "commit", "-q", "-am", "PLACEHOLDER test: analysis change")
    r = step7(git(clone, "rev-parse", "HEAD"))
    git(clone, "reset", "-q", "--hard", head)
    print(f"R5 analysis file changed since step 6: exit {r.returncode} | {r.stderr.strip()[-90:]}")
    assert r.returncode == 3 and "changed since step 6" in r.stderr

    r = step7(head)
    new = git(clone, "rev-parse", "HEAD")
    files = set(git(clone, "diff-tree", "--no-commit-id", "--name-only", "-r", new).splitlines())
    rec = open(os.path.join(clone, "results", "step7", "STEP7_RECORD.md")).read()
    status = run(["bash", r7, "--status", "--out6", out6]).stdout.strip()
    print(f"R6 full step 7 (PLACEHOLDER): exit {r.returncode}; record commit {new[:12]}, parent "
          f"{git(clone, 'rev-parse', 'HEAD^')[:12]} (= HEAD {head[:12]}), {len(files)} files = RECORDS: "
          f"{files == set(s7.RECORDS)}, tree clean: {not git(clone, 'status', '--porcelain', '--untracked-files=all')}"
          f"; {status}")
    assert r.returncode == 0 and git(clone, "rev-parse", "HEAD^") == head and files == set(s7.RECORDS)
    assert not git(clone, "status", "--porcelain", "--untracked-files=all") and "PLACEHOLDER" in rec
    assert git(clone, "log", "-1", "--format=%an <%ae>") == f"{git(REPO, 'config', '--get', 'user.name')} <" \
                                                           f"{git(REPO, 'config', '--get', 'user.email')}>"
    assert "no unit recomputed" in open(os.path.join(out6, "logs", "step7.log")).read()

    r = step7(new)
    print(f"R7 relaunch after completion: exit {r.returncode} | {r.stderr.strip()[-90:]}")
    assert r.returncode == 3 and "already complete" in r.stderr

    assert git(REPO, "rev-parse", "HEAD") == real_head
    assert git(REPO, "status", "--porcelain", "--untracked-files=all") == real_status
    print("real repository unchanged (HEAD and status identical before/after)")
