"""§14 step 6 orchestrator behind scripts/run_step6.sh (orchestration only; no analysis logic).

The causal grid is the locked `ss_benchmark.grid_driver` (real design, replicate root 20261007), run through
scripts/step6_grid_units.py, which suppresses the driver's final aggregation: replicates.csv, cell_metrics.csv and
families.json (family verdicts) belong to §14 step 7, which this runner never runs.

Preconditions (refused before anything changes; exit 3):
* HEAD == --expect-commit, HEAD contains scripts/run_step6.sh, clean tree (no untracked file either);
* the step-5 record and the §13 record are committed (results/step5/);
* §14 step 6, "confirm that the SDR commit recorded at step 2 is the one in use": every file under ss_benchmark/ is
  byte-identical to af56777 (the SDR implementation commit, CODELOCK_FINAL_RECORD.md §1), except the extraction
  adapter ss_benchmark/models/prim_caformer.py (CODELOCK_CORRECTION_001), which the grid does not import;
* the step-5 reps file has the SHA-256 recorded in the committed results/step5/step5_manifest.json;
* the code-lock projection record passed with no reduction; no process of an earlier step-6 run is alive.
The resume checks are the same (the runner never commits, so HEAD stays the launch commit).

Execution: a `git archive` snapshot of the launch commit runs the locked driver with the code-lock thread settings
(OPENBLAS / OMP / MKL / NUMEXPR threads = 1, PYTHONHASHSEED = 0, the base Python), --workers N on N pinned logical
CPUs; the orchestrator runs on the remaining CPUs. Each (set, cell, replicate) unit is one shard; a resume skips
finished shards. Failures are retried with backoff 60 / 300 / 900 s; three consecutive failures without progress stop
the runner.

Memory guard: pressure = MemAvailable < 5 % of MemTotal, or PSI memory "full avg60" >= 10 %, or the run's resident
memory > 80 % of MemTotal; three consecutive 15-s checks with pressure stop the runner (resumable). Swap-out alone is
not a pressure signal (the step 4-5 guard stopped on 6 Oct with ~80 GiB available because of it).

Logging: logs/progress.log (events; a RES sample every 10 min: CPU, load, RAM used / available, PSI, run RSS against
the cap, swap, GPU, CPU temperature, disk throughput); logs/grid.log (the driver's output). No estimate, metric or
verdict is logged or shown by --status.

    python scripts/step6_orchestrate.py run --repo REPO --expect-commit SHA --out DIR --reps FILE --workers N
        [--cpus LIST] [--placeholder --cells LIST --max-reps M]          (PLACEHOLDER: smoke tests only)
    python scripts/step6_orchestrate.py status --out DIR
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time

PY = "/home/user/miniconda3/bin/python3"
SDR_COMMIT = "af56777e0f52b5c350dd7ba557d55b2394cbd4bf"
SDR_EXEMPT = frozenset({"ss_benchmark/models/prim_caformer.py"})          # CODELOCK_CORRECTION_001 (extraction only)
STEP5_FILES = ("results/step5/STEP5_RECORD.md", "results/step5/checks.json", "results/step5/reps_report.json",
               "results/step5/step5_manifest.json")
S13_FILES = ("results/step5/SECTION13_RECORD.md", "results/step5/section13.json", "results/step5/grid_conditions.json")
GSITE = "results/codelock_gate/gsite_record.json"
PROJECTION = "results/codelock_gate/projection_PLACEHOLDER.json"
SNAPSHOT_PATHS = ("ss_benchmark", "scripts", "data_audit/lead/out/DS203_d8_cases.csv",
                  "data_audit/lead/out/ss_window_offsets.csv", "data_audit/lead/out/ss_window_offsets_perW.csv",
                  "results/step5/grid_conditions.json", GSITE, PROJECTION)
DEFAULT_OUT = "/media/user/LaCie/medvideo_gate/ss_step6"
MEM_CAP_FRACTION = 0.80
MEM_AVAIL_MIN = 0.05
PSI_FULL_MAX = 10.0
MAX_FAILS = 3
BACKOFF = tuple(int(x) for x in os.environ.get("SS_RUNNER_BACKOFF_S", "60,300,900").split(","))   # tests override
RES_INTERVAL = int(os.environ.get("SS_RUNNER_RES_INTERVAL_S", "600"))                              # tests override
WATCH_INTERVAL = 15
CODELOCK_ENV = dict(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1",
                    PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")


class Stop(Exception):
    pass


class Refuse(Stop):
    """Launch / resume refused by the preconditions; the run state is not touched."""


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_file(p, bs=16 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(bs), b""):
            h.update(blk)
    return h.hexdigest()


def json_write(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True, default=str)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def json_read(path, default=None):
    try:
        return json.load(open(path))
    except (OSError, ValueError):
        return default


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True,
                       env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"))
    if check and r.returncode:
        raise Refuse(f"refused: git {' '.join(args)} failed: {r.stderr.strip()[:200]}")
    return r.stdout.strip()


def meminfo():
    m = {}
    for line in open("/proc/meminfo"):
        k, v = line.split(":", 1)
        m[k] = int(v.split()[0]) * 1024
    return m


def psi_memory():
    """{'some': avg60, 'full': avg60} from /proc/pressure/memory, or None if PSI is unavailable."""
    try:
        out = {}
        for line in open("/proc/pressure/memory"):
            kind, *fields = line.split()
            out[kind] = float(dict(f.split("=") for f in fields)["avg60"])
        return out
    except (OSError, ValueError, KeyError):
        return None


def tree_rss(root_pid):
    parent, rss = {}, {}
    page = os.sysconf("SC_PAGE_SIZE")
    for d in os.listdir("/proc"):
        if d.isdigit():
            try:
                st = open(f"/proc/{d}/stat").read()
                f = st[st.rindex(")") + 2:].split()
                parent[int(d)], rss[int(d)] = int(f[1]), int(f[21]) * page
            except (OSError, ValueError, IndexError):
                continue
    keep, todo = {root_pid}, [root_pid]
    while todo:
        p = todo.pop()
        for c, pp in parent.items():
            if pp == p and c not in keep:
                keep.add(c)
                todo.append(c)
    return sum(rss.get(p, 0) for p in keep)


def pressure_reasons(mem, psi, rss, cap):
    """Memory-pressure test (pure function; unit-tested). Swap-out is deliberately not a criterion."""
    reasons = []
    if mem["MemAvailable"] < MEM_AVAIL_MIN * mem["MemTotal"]:
        reasons.append(f"MemAvailable {mem['MemAvailable'] / 2**30:.1f} GiB < {MEM_AVAIL_MIN:.0%} of RAM")
    if psi is not None and psi.get("full", 0.0) >= PSI_FULL_MAX:
        reasons.append(f"PSI memory full avg60 {psi['full']:.1f} % >= {PSI_FULL_MAX:.0f} %")
    if rss > cap:
        reasons.append(f"run resident memory {rss / 2**30:.1f} GiB > cap {cap / 2**30:.1f} GiB")
    return reasons


def shard_counts(grid_out):
    out = {}
    w = os.path.join(grid_out, "work")
    for s in sorted(os.listdir(w)) if os.path.isdir(w) else []:
        out[s] = sum(1 for f in os.listdir(os.path.join(w, s)) if f.endswith(".json"))
    return out


class Runner:
    def __init__(self, a):
        self.a = a
        self.repo, self.out = os.path.abspath(a.repo), os.path.abspath(a.out)
        self.logs, self.snap = os.path.join(self.out, "logs"), os.path.join(self.out, "code_snapshot")
        self.grid_out = os.path.join(self.out, "grid")
        self.state_p = os.path.join(self.out, "state.json")
        os.makedirs(self.logs, exist_ok=True)
        self.state = json_read(self.state_p, {}) or {}
        self.lock = threading.RLock()
        self.stopping = threading.Event()
        self.proc = None
        n = os.cpu_count()
        self.cpus = ([int(x) for x in a.cpus.split(",")] if a.cpus else list(range(min(a.workers, n))))
        self.orch_cpus = [c for c in range(n) if c not in self.cpus] or list(range(n))
        self.mem_cap = int(MEM_CAP_FRACTION * meminfo()["MemTotal"])

    def log(self, msg):
        line = f"{now()} {msg}"
        with self.lock:
            with open(os.path.join(self.logs, "progress.log"), "a") as f:
                f.write(line + "\n")
        print(line, flush=True)

    def save(self):
        with self.lock:
            json_write(self.state_p, self.state)

    # -- preconditions ---------------------------------------------------------------------------------------------
    def preflight(self):
        repo, exp = self.repo, self.a.expect_commit
        if self.state.get("status") == "complete":
            raise Refuse("refused: this step-6 run is already complete")
        launch = self.state.get("launch_commit")
        if launch and launch != exp:
            raise Refuse(f"refused: this output directory belongs to launch commit {launch[:12]}, not {exp[:12]}")
        if bool(self.state.get("placeholder", self.a.placeholder)) != bool(self.a.placeholder):
            raise Refuse("refused: PLACEHOLDER and real runs cannot share an output directory")
        if self.a.placeholder and os.path.realpath(self.out).startswith(os.path.realpath(DEFAULT_OUT)):
            raise Refuse("refused: a PLACEHOLDER run may not write to the real step-6 output directory")
        head = git(repo, "rev-parse", "HEAD")
        if head != exp:
            raise Refuse(f"refused: HEAD {head[:12]} is not --expect-commit {exp[:12]}")
        dirty = git(repo, "status", "--porcelain", "--untracked-files=all")
        if dirty:
            raise Refuse(f"refused: working tree not clean: {dirty.splitlines()[:3]}")
        for p in ("scripts/run_step6.sh", "scripts/step6_orchestrate.py", "scripts/step6_grid_units.py",
                  *STEP5_FILES, *S13_FILES, GSITE, PROJECTION):
            if subprocess.run(["git", "-C", repo, "cat-file", "-e", f"HEAD:{p}"], capture_output=True,
                              env=dict(os.environ, GIT_OPTIONAL_LOCKS="0")).returncode:
                raise Refuse(f"refused: {p} is not committed at HEAD")
        changed = set(git(repo, "diff", "--name-only", SDR_COMMIT, "HEAD", "--", "ss_benchmark").splitlines())
        if changed - SDR_EXEMPT:
            raise Refuse(f"refused: ss_benchmark differs from the SDR commit {SDR_COMMIT[:12]}: "
                         f"{sorted(changed - SDR_EXEMPT)[:5]}")
        proj = json.load(open(os.path.join(repo, PROJECTION)))
        if not proj.get("projection_pass") or proj.get("reductions_applied"):
            raise Refuse("refused: the code-lock projection record does not show a pass without reductions")
        if not self.a.placeholder:
            man = json.load(open(os.path.join(repo, "results/step5/step5_manifest.json")))
            want = man["files"]["reps.npz"]["sha256"]
            if not os.path.exists(self.a.reps) or sha256_file(self.a.reps) != want:
                raise Refuse("refused: the reps file is missing or differs from the committed step-5 manifest")
        stray = [int(d) for d in os.listdir("/proc") if d.isdigit() and int(d) != os.getpid()
                 and self._is_ours(d)]
        if stray:
            raise Refuse(f"refused: processes of an earlier step-6 run are still alive: {stray[:5]}")
        return head, sorted(changed)

    def _is_ours(self, d):
        try:
            cmd = open(f"/proc/{d}/cmdline", "rb").read().decode(errors="replace").split("\0")
        except OSError:
            return False
        return any(x.startswith(self.out) for x in cmd) and any(
            x.endswith(("step6_grid_units.py", "step6_orchestrate.py")) for x in cmd)

    # -- snapshot --------------------------------------------------------------------------------------------------
    def snapshot(self):
        exp = self.a.expect_commit
        meta_p = os.path.join(self.out, "code_snapshot.json")
        meta = json_read(meta_p)
        if meta and meta.get("commit") == exp and os.path.isdir(self.snap):
            for rel, sha in meta["files"].items():
                if sha256_file(os.path.join(self.snap, rel)) != sha:
                    raise Stop(f"code snapshot file changed: {rel}")
            return
        if os.path.exists(self.snap):
            shutil.rmtree(self.snap)
        os.makedirs(self.snap)
        arch = subprocess.run(["git", "-C", self.repo, "archive", "--format=tar", exp, *SNAPSHOT_PATHS],
                              capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", self.snap], input=arch.stdout, check=True)
        files = {os.path.relpath(os.path.join(r, f), self.snap): sha256_file(os.path.join(r, f))
                 for r, _, fs in os.walk(self.snap) for f in fs}
        json_write(meta_p, dict(commit=exp, created=now(), files=files))
        self.log(f"code snapshot of {exp[:12]} created ({len(files)} files)")

    # -- monitor -----------------------------------------------------------------------------------------------------
    def resource_line(self, prev):
        cpu = open("/proc/stat").readline().split()[1:]
        v = [int(x) for x in cpu]
        busy, total = sum(v[:8]) - v[3] - v[4], sum(v[:8])
        st = os.stat(self.out)
        dev = os.path.basename(os.path.realpath(f"/sys/dev/block/{os.major(st.st_dev)}:{os.minor(st.st_dev)}"))
        rd = wr = 0
        for line in open("/proc/diskstats"):
            f = line.split()
            if f[2] == dev:
                rd, wr = int(f[5]), int(f[9])
        t, m, psi = time.time(), meminfo(), psi_memory()
        line = None
        if prev:
            dt = t - prev["t"]
            try:
                g = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,temperature.gpu,utilization.gpu",
                                    "--format=csv,noheader,nounits"], capture_output=True, text=True,
                                   timeout=30).stdout.strip().split(", ")
            except (OSError, subprocess.SubprocessError):
                g = ["n/a"] * 3
            try:
                ct = next(int(open(f"/sys/class/hwmon/{h}/temp1_input").read()) / 1000
                          for h in sorted(os.listdir("/sys/class/hwmon"))
                          if open(f"/sys/class/hwmon/{h}/name").read().strip() == "coretemp")
            except (OSError, StopIteration, ValueError):
                ct = None
            line = (f"RES cpu {100.0 * (busy - prev['busy']) / max(1, total - prev['total']):.0f}% load "
                    f"{os.getloadavg()[0]:.1f} | ram used {(m['MemTotal'] - m['MemAvailable']) / 2**30:.1f} GiB avail "
                    f"{m['MemAvailable'] / 2**30:.1f} GiB | psi mem some/full avg60 "
                    f"{psi['some'] if psi else 'n/a'}/{psi['full'] if psi else 'n/a'} | run_rss "
                    f"{tree_rss(os.getpid()) / 2**30:.1f} GiB (cap {self.mem_cap / 2**30:.1f}) | swap_used "
                    f"{(m['SwapTotal'] - m['SwapFree']) / 2**30:.2f} GiB | gpu mem {g[0]} MiB temp {g[1]} C util "
                    f"{g[2]}% | cpu temp {ct} C | disk {dev} read {(rd - prev['rd']) * 512 / dt / 1e6:.1f} MB/s "
                    f"write {(wr - prev['wr']) * 512 / dt / 1e6:.1f} MB/s")
        return line, dict(t=t, busy=busy, total=total, rd=rd, wr=wr)

    def monitor(self):
        _, prev = self.resource_line(None)
        last_res, strikes = time.time(), 0
        while not self.stopping.wait(WATCH_INTERVAL):
            if time.time() - last_res >= RES_INTERVAL:
                line, prev = self.resource_line(prev)
                self.log(line)
                last_res = time.time()
            reasons = pressure_reasons(meminfo(), psi_memory(), tree_rss(os.getpid()), self.mem_cap)
            strikes = strikes + 1 if reasons else 0
            if reasons:
                self.log(f"memory pressure ({'; '.join(reasons)}), strike {strikes}/3")
            if strikes >= 3:
                self.shutdown(f"memory pressure: {'; '.join(reasons)}")
                return

    def shutdown(self, why):
        with self.lock:
            if self.stopping.is_set():
                return
            self.stopping.set()
            self.state["stop_reason"] = why
            self.save()
        self.log(f"shutting down: {why}")
        p = self.proc
        if p is not None and p.poll() is None:
            try:
                os.killpg(p.pid, signal.SIGTERM)
            except OSError:
                pass
            try:
                p.wait(120)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid, signal.SIGKILL)

    # -- run ----------------------------------------------------------------------------------------------------------
    def grid_cmd(self):
        cmd = [PY, os.path.join(self.snap, "scripts", "step6_grid_units.py"), "--out", self.grid_out,
               "--workers", str(self.a.workers)]
        if self.a.placeholder:
            cmd += ["--placeholder"]
            if self.a.cells:
                cmd += ["--cells", self.a.cells]
            if self.a.max_reps:
                cmd += ["--max-reps", str(self.a.max_reps)]
        else:
            cmd += ["--reps", os.path.abspath(self.a.reps),
                    "--conditions", os.path.join(self.snap, "results/step5/grid_conditions.json"),
                    "--gsite", os.path.join(self.snap, GSITE), "--projection", os.path.join(self.snap, PROJECTION)]
        return ["taskset", "-c", ",".join(map(str, self.cpus)), *cmd]

    def run_grid(self):
        fails, last = 0, sum(shard_counts(self.grid_out).values())
        env = dict(os.environ, **CODELOCK_ENV)
        while True:
            self.log(f"grid: start (attempt {fails + 1}); {last} shards present")
            with open(os.path.join(self.logs, "grid.log"), "a") as lf:
                lf.write(f"\n===== {now()} start: {' '.join(self.grid_cmd())}\n")
                lf.flush()
                self.proc = subprocess.Popen(self.grid_cmd(), stdout=lf, stderr=subprocess.STDOUT, env=env,
                                             cwd=self.snap, start_new_session=True)
                rc = self.proc.wait()
                lf.write(f"===== {now()} exit {rc}\n")
            if self.stopping.is_set():
                raise Stop("interrupted")
            if rc == 0:
                return
            n = sum(shard_counts(self.grid_out).values())
            if n > last:
                fails, last = 0, n
            fails += 1
            if fails >= MAX_FAILS:
                raise Stop(f"grid: {fails} consecutive failures without progress (last exit {rc}); see logs/grid.log")
            wait = BACKOFF[min(fails - 1, len(BACKOFF) - 1)]
            self.log(f"grid: exit {rc}; retry in {wait} s")
            if self.stopping.wait(wait):
                raise Stop("interrupted")

    def run(self):
        head, changed = self.preflight()
        self.state.setdefault("launch_commit", self.a.expect_commit)
        self.state.update(pid=os.getpid(), last_start=now(), status="running", placeholder=bool(self.a.placeholder))
        self.state.pop("stop_reason", None)
        self.state.setdefault("settings", dict(
            workers=self.a.workers, worker_cpus=self.cpus, orchestrator_cpus=self.orch_cpus,
            thread_env=CODELOCK_ENV, python=PY, memory_cap_bytes=self.mem_cap,
            memory_guard=dict(mem_available_min_fraction=MEM_AVAIL_MIN, psi_full_avg60_max=PSI_FULL_MAX,
                              strikes=3, interval_s=WATCH_INTERVAL, swap_out_rule=None),
            sdr_commit=SDR_COMMIT, ss_benchmark_files_differing_from_sdr_commit=changed,
            reps=None if self.a.placeholder else os.path.abspath(self.a.reps),
            placeholder=dict(cells=self.a.cells, max_reps=self.a.max_reps) if self.a.placeholder else None))
        self.save()
        os.sched_setaffinity(0, set(self.orch_cpus))
        threading.Thread(target=self.monitor, daemon=True).start()
        self.log(f"preflight passed: HEAD {head[:12]}; clean tree; step-5 and §13 records committed; ss_benchmark = "
                 f"SDR commit {SDR_COMMIT[:12]} (except {changed or 'nothing'}); {self.a.workers} workers on CPUs "
                 f"{self.cpus}; code-lock thread settings; memory cap {self.mem_cap / 2**30:.1f} GiB"
                 + ("; PLACEHOLDER smoke run" if self.a.placeholder else ""))
        self.snapshot()
        self.run_grid()
        plan = json_read(os.path.join(self.grid_out, "run_plan.json"), {})
        counts = shard_counts(self.grid_out)
        if sum(counts.values()) != plan.get("n_units"):
            raise Stop(f"grid finished but {sum(counts.values())} shards != {plan.get('n_units')} planned units")
        self.write_record(plan, counts)
        self.state["status"] = "complete"
        self.save()
        self.log("step 6 complete: all units present; §14 step 7 (aggregation, family verdicts) is not part of this "
                 "runner")

    def write_record(self, plan, counts):
        d = os.path.join(self.out, "step6_record")
        os.makedirs(d, exist_ok=True)
        lines = []
        w = os.path.join(self.grid_out, "work")
        for s in sorted(counts):
            for f in sorted(os.listdir(os.path.join(w, s))):
                if f.endswith(".json"):
                    lines.append(f"{s}/{f} {sha256_file(os.path.join(w, s, f))}")
        open(os.path.join(d, "shard_sha256.txt"), "w").write("\n".join(lines) + "\n")
        json_write(os.path.join(d, "run_record.json"), dict(
            launch_commit=self.a.expect_commit, sdr_commit=SDR_COMMIT, settings=self.state["settings"],
            run_plan=plan, shards=counts, shard_digest=hashlib.sha256("\n".join(lines).encode()).hexdigest(),
            note="§14 step 6 units only; replicates.csv, cell_metrics.csv and families.json are §14 step 7"))


def status(out):
    st = json_read(os.path.join(out, "state.json"), {}) or {}
    pid, alive = st.get("pid"), False
    if pid:
        try:
            alive = "step6_orchestrate" in open(f"/proc/{pid}/cmdline").read()
        except OSError:
            alive = False
    plan = json_read(os.path.join(out, "grid", "run_plan.json"), {}) or {}
    counts = shard_counts(os.path.join(out, "grid"))
    lines = [f"runner: {'running (pid %d)' % pid if alive else 'not running'}; state {st.get('status', 'not started')}"
             + (f"; STOPPED: {st['stop_reason']}" if st.get("stop_reason") else "")
             + ("; PLACEHOLDER" if st.get("placeholder") else ""),
             f"units: {sum(counts.values())}/{plan.get('n_units', '?')} "
             + "(" + ", ".join(f"{s} {n}" for s, n in counts.items()) + ")"]
    try:
        log = open(os.path.join(out, "logs", "progress.log")).read().splitlines()
    except OSError:
        log = []
    res = [x for x in log if " RES " in x]
    lines.append(f"last progress-log entry: {log[-1][:25] if log else 'none'}")
    lines.append(f"resources: {res[-1] if res else 'no sample yet'}")
    print("\n".join(lines))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    for k in ("--repo", "--expect-commit", "--out"):
        r.add_argument(k, required=True)
    r.add_argument("--reps")
    r.add_argument("--workers", type=int, required=True)
    r.add_argument("--cpus")
    r.add_argument("--placeholder", action="store_true")
    r.add_argument("--cells")
    r.add_argument("--max-reps", type=int)
    s = sub.add_parser("status")
    s.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "status":
        return status(a.out)
    run = Runner(a)
    signal.signal(signal.SIGTERM, lambda n, f: threading.Thread(
        target=run.shutdown, args=(f"interrupted by signal {n}",), daemon=True).start())
    signal.signal(signal.SIGINT, lambda n, f: threading.Thread(
        target=run.shutdown, args=(f"interrupted by signal {n}",), daemon=True).start())
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    try:
        run.run()
        return 0
    except Refuse as e:
        print(f"{now()} {e}", file=sys.stderr)
        return 3
    except Stop as e:
        run.shutdown(str(e))
        run.state["status"] = "stopped"
        run.save()
        run.log(f"STOP: {run.state.get('stop_reason', e)}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
