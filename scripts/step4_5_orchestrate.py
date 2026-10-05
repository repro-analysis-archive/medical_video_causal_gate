"""§14 steps 4-5 orchestrator behind scripts/run_step4_5.sh (orchestration only; no analysis logic).

Every computation is a call of the locked CLI ``ss_benchmark.pipeline`` (mask-check, extract, near-uniform,
build-reps, checks) through scripts/step4_5_launch.py, run from a code snapshot of the expected commit. This file only
sequences those calls, checks their completion, writes manifests / records, commits the step-4 record, and logs.

Order (CC_TASK_SS_step4_5_prep_v2.md §2; CC_TASK_SS_resource_policy_v1.md):
  preflight -> snapshot -> stage (byte copy of the 278 cases' files out of the split archive, CRC-32 checked)
  -> 4a mask check (one unit); r must follow the frozen rule (0.45, or the single fallback 0.98 x min_c rho_c) and be a
     usable radius, else STOP before any extraction
  -> 4b extraction in two lanes (at most 2 concurrent readers): lane 1 = reference (Cosmos); lane 2 = primary
     standardized, primary native, secondary; resumable per case (the locked manifest.json)
  -> near-uniform record (locked near-uniform on the primary standardized arm)
  -> step-4 record (representation manifest, mask-check and near-uniform records, run settings) written to
     results/step4/ and committed (records only, repository-scoped identity); if the commit fails, STOP: step 5 never
     starts before it
  -> step 5: build-reps (fold-wise PCA / LEACE), checks (E1, E2 all variants, E3-site, E3-state-retention, probes and
     reporting paths on the 278- and 158-case sets); step-5 record written to results/step5/, NOT committed
  -> stop. No part of §14 step 6 exists here.

Resources: worker CPUs = all logical CPUs of (physical cores - 2) cores; the two highest-numbered cores are reserved
for the OS, I/O and this process. Threads (torch / OpenMP / OpenBLAS / MKL) = workers / 2 = 6 for every pipeline
process: two extraction lanes use all 12 workers; for single-process stages more threads do not help the locked code
(12 BLAS threads made the locked multinomial site-probe fit 2.5-7x slower than 4-8 on synthetic features).
Memory: the run's resident memory is capped at 80 % of physical RAM; on pressure (cap, MemAvailable < 5 %, or
swap-out) with two lanes the most recently started lane is stopped and resumed after the other finishes; with one
process the runner stops. Failures: retried with backoff 60 / 300 / 900 s; three consecutive failures without progress
stop the runner. Resource samples (CPU, RAM, swap, GPU memory / temperature / utilisation, CPU temperature, disk
throughput) go to the progress log every 10 min; no estimate or result is logged.

    python scripts/step4_5_orchestrate.py run --repo REPO --expect-commit SHA --out DIR --archive-zip ZIP --weights DIR
    python scripts/step4_5_orchestrate.py status --out DIR
"""
import argparse
import datetime
import hashlib
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time

PY = "/home/user/.venvs/ss_extract/bin/python"
ARMS = {  # arm: (model key, acquisition, weights path relative to the weights directory)
    "P": ("SurgeNetCholec", "standardized", "surgenet/CHOLEC_checkpoint_epoch0050_teacher.pth"),
    "P-nat": ("SurgeNetCholec", "native", "surgenet/CHOLEC_checkpoint_epoch0050_teacher.pth"),
    "S": ("LeanVAE-4ch", "standardized", "leanvae/LeanVAE-dim4.ckpt"),
    "REF": ("Cosmos-CV8x8x8", "standardized", "cosmos/Cosmos-1.0-Tokenizer-CV8x8x8"),
}
ARM_ORDER = ("P", "P-nat", "S", "REF")
LANES = (("REF",), ("P", "P-nat", "S"))
WEIGHT_SHA256 = {  # MODEL_SELECTION_RECORD.md §4 / §8; STEP4_5_RUNNER.md (Cosmos)
    "surgenet/CHOLEC_checkpoint_epoch0050_teacher.pth":
        "9bc446addbf92e8c4e8b237eb3ec8917dbbc526ca5af042d657340ea8bb945d4",
    "leanvae/LeanVAE-dim4.ckpt": "cd54560ca3e713e8aee69fddca21519a19d6bf9a46ee380e523e12f716aa5963",
    "cosmos/Cosmos-1.0-Tokenizer-CV8x8x8/vae/config.json":
        "17ea012aa67ad5e3d381604cfa2e05431f2058edabc650163ffc96db4d69ccbc",
    "cosmos/Cosmos-1.0-Tokenizer-CV8x8x8/vae/diffusion_pytorch_model.safetensors":
        "59dca00bd6d3f20b8201d54dd6697da63cbcf768513004acd4216bd45a56a241",
}
THIRD_PARTY_DIGEST = {  # tree digest (third_party_digest) of the adapters' git-ignored official code
    "LeanVAE": "c354a4a7f7cc91b288a1fde4021f8fd87ebb811040edbcbb3d16d48e9d51abdd",
    "SurgeNet": "a7d3cab6532f44eae4515c6e12cb9774ca42608b73ef05f6e9713ff8e7789252",
}
RECORD_PREFIX = "SS §14 step 4 record (automated, scripts/run_step4_5.sh)"
RECORD_FILES = frozenset(f"results/step4/{f}" for f in (
    "STEP4_RECORD.md", "representation_manifest.json", "mask_check.json", "near_uniform.json", "staged_manifest.json",
    "run_meta.json", *(f"extract_manifests/{a}.json" for a in ("P", "P-nat", "S", "REF"))))
PIPELINE_COMMANDS = frozenset({"mask-check", "extract", "near-uniform", "build-reps", "checks"})   # no step-6 entry
MEM_CAP_FRACTION = 0.80
MAX_FAILS = 3
BACKOFF = tuple(int(x) for x in os.environ.get("SS_RUNNER_BACKOFF_S", "60,300,900").split(","))   # tests override
RES_INTERVAL = int(os.environ.get("SS_RUNNER_RES_INTERVAL_S", "600"))                              # tests override
WATCH_INTERVAL = 15


class Stop(Exception):
    pass


class Refuse(Stop):
    """Launch / resume refused by the provenance checks; the run state is not touched."""


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_file(p, bs=16 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(bs), b""):
            h.update(b)
    return h.hexdigest()


def third_party_digest(d):
    """sha256 over the sorted lines '<relative path> <sha256>' of every file under d (no __pycache__)."""
    lines = []
    for root, dirs, files in os.walk(d):
        dirs[:] = sorted(x for x in dirs if x != "__pycache__")
        for f in sorted(files):
            p = os.path.join(root, f)
            lines.append(f"{os.path.relpath(p, d)} {sha256_file(p)}")
    return hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest(), lines


def cpu_layout():
    """(physical cores, worker cores, worker logical CPUs, reserved logical CPUs) from lscpu -p."""
    out = subprocess.run(["lscpu", "-p=CPU,CORE"], capture_output=True, text=True, check=True,
                         env=dict(os.environ, LC_ALL="C")).stdout
    core_of = {}
    for line in out.splitlines():
        if line and not line.startswith("#"):
            cpu, core = (int(x) for x in line.split(","))
            core_of.setdefault(core, []).append(cpu)
    cores = sorted(core_of)
    reserved = cores[-2:]
    workers = [c for c in cores if c not in reserved]
    return (len(cores), len(workers), sorted(x for c in workers for x in core_of[c]),
            sorted(x for c in reserved for x in core_of[c]))


def meminfo():
    m = {}
    for line in open("/proc/meminfo"):
        k, v = line.split(":", 1)
        m[k] = int(v.split()[0]) * 1024
    return m


def vmstat(key):
    for line in open("/proc/vmstat"):
        k, v = line.split()
        if k == key:
            return int(v)
    return 0


def tree_rss(root_pid):
    """Resident bytes of root_pid and all its descendants."""
    parent, rss = {}, {}
    page = os.sysconf("SC_PAGE_SIZE")
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            st = open(f"/proc/{d}/stat").read()
            fields = st[st.rindex(")") + 2:].split()
            parent[int(d)] = int(fields[1])
            rss[int(d)] = int(fields[21]) * page
        except (OSError, ValueError, IndexError):
            continue
    keep, frontier = {root_pid}, [root_pid]
    while frontier:
        p = frontier.pop()
        for c, pp in parent.items():
            if pp == p and c not in keep:
                keep.add(c)
                frontier.append(c)
    return sum(rss.get(p, 0) for p in keep)


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
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and r.returncode:
        raise Stop(f"git {' '.join(args)} failed: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def validate_mask_check(res, centres=("2", "3", "4", "5"), r0=0.45, shrink=0.98):
    """(ok, message). The frozen rule: r = 0.45 if min_c rho_c >= 0.45, else the single fallback 0.98 x min_c rho_c;
    the fallback fails when it gives no usable radius (a centre without frames, rho non-finite or 0)."""
    rho = res.get("visible_radius", {})
    prof = res.get("profiles", {})
    if sorted(rho) != sorted(centres) or any(prof.get(c, {}).get("n_frames", 0) <= 0 for c in centres):
        return False, "mask check: a centre has no frames"
    rmin = min(float(v) for v in rho.values())
    r = float(res.get("r", float("nan")))
    expect = r0 if rmin >= r0 else shrink * rmin
    if not (math.isfinite(rmin) and math.isfinite(r)) or abs(r - expect) > 1e-12:
        return False, "mask check: r does not follow the frozen rule"
    if not (0.0 < r <= r0):
        return False, "mask check: the frozen fallback gives no usable radius"
    return True, "r = 0.45 stands" if r == r0 else "single frozen fallback applied (r = 0.98 x min_c rho_c)"


def npy_header(path):
    import numpy as np
    with open(path, "rb") as f:
        major, _ = np.lib.format.read_magic(f)
        shape, fortran, dtype = (np.lib.format.read_array_header_1_0(f) if major == 1
                                 else np.lib.format.read_array_header_2_0(f))
    return list(shape), dtype.str


# ---------------------------------------------------------------------------------------------------------------------
class Runner:
    def __init__(self, a):
        self.a = a
        self.repo = os.path.abspath(a.repo)
        self.out = os.path.abspath(a.out)
        self.logs = os.path.join(self.out, "logs")
        self.snap = os.path.join(self.out, "code_snapshot")
        self.staged = os.path.join(self.out, "staged")
        self.videos = os.path.join(self.staged, "Full_Videos")
        self.state_p = os.path.join(self.out, "state.json")
        os.makedirs(self.logs, exist_ok=True)
        self.state = json_read(self.state_p, {}) or {}
        self.lock = threading.RLock()
        self.stopping = threading.Event()
        self.procs = {}                       # name -> (Popen, start time, lane)
        self.lanes = []
        self.n_cores, self.n_workers, self.worker_cpus, self.reserved_cpus = cpu_layout()
        self.mem_cap = int(MEM_CAP_FRACTION * meminfo()["MemTotal"])
        self.threads = max(1, self.n_workers // 2)

    # -- logging / state --------------------------------------------------------------------------------------------
    def log(self, msg):
        line = f"{now()} {msg}"
        with self.lock:
            with open(os.path.join(self.logs, "progress.log"), "a") as f:
                f.write(line + "\n")
        print(line, flush=True)

    def save(self):
        with self.lock:
            json_write(self.state_p, self.state)

    def stage_status(self, name):
        return self.state.get("stages", {}).get(name, {}).get("status")

    def set_stage(self, name, status, **kw):
        with self.lock:
            st = self.state.setdefault("stages", {}).setdefault(name, {})
            st.update(status=status, **kw)
            st[f"t_{status}"] = now()
        self.save()

    # -- processes --------------------------------------------------------------------------------------------------
    def env(self, threads):
        e = dict(os.environ)
        e.update(PYTHONDONTWRITEBYTECODE="1", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", DIFFUSERS_OFFLINE="1",
                 CUBLAS_WORKSPACE_CONFIG=":4096:8", OMP_NUM_THREADS=str(threads), MKL_NUM_THREADS=str(threads),
                 OPENBLAS_NUM_THREADS=str(threads), OMP_WAIT_POLICY="PASSIVE", PYTHONHASHSEED="0",
                 CUDA_VISIBLE_DEVICES=e.get("CUDA_VISIBLE_DEVICES", "0"))
        return e

    def spawn_and_wait(self, name, cmd, threads, lane=None):
        """Run cmd on the worker CPUs; returns (exit code, 'ok' | 'failed' | 'deferred' | 'stopping')."""
        logf = open(os.path.join(self.logs, f"{name}.log"), "a")
        logf.write(f"\n===== {now()} start: {' '.join(cmd)} (threads {threads})\n")
        logf.flush()
        cpus = ",".join(str(c) for c in self.worker_cpus)
        p = subprocess.Popen(["taskset", "-c", cpus, *cmd], stdout=logf, stderr=subprocess.STDOUT,
                             env=self.env(threads), cwd=self.snap)
        with self.lock:
            self.procs[name] = (p, time.time(), lane)
        rc = p.wait()
        with self.lock:
            self.procs.pop(name, None)
        logf.write(f"===== {now()} exit {rc}\n")
        logf.close()
        if self.stopping.is_set():
            return rc, "stopping"
        if lane is not None and lane.defer_kill:
            lane.defer_kill = False
            return rc, "deferred"
        return rc, "ok" if rc == 0 else "failed"

    def run_unit(self, name, cmd, threads, progress=lambda: 0, lane=None):
        fails, last = 0, progress()
        self.set_stage(name, "running")
        while True:
            if lane is not None and lane.deferred:
                while any(l is not lane and l.is_alive() for l in self.lanes):
                    if self.stopping.wait(10):
                        raise Stop("interrupted")
            self.log(f"{name}: start (attempt {fails + 1})")
            rc, how = self.spawn_and_wait(name, cmd, threads, lane)
            if how == "stopping":
                raise Stop("interrupted")
            if how == "deferred":
                self.log(f"{name}: stopped for memory pressure; resumes after the other lane finishes")
                continue
            if how == "ok":
                self.set_stage(name, "done")
                self.log(f"{name}: done")
                return
            p = progress()
            if p > last:
                fails, last = 0, p
            fails += 1
            if fails >= MAX_FAILS:
                self.set_stage(name, "failed", exit=rc)
                raise Stop(f"{name}: {fails} consecutive failures without progress (last exit {rc}); "
                           f"see logs/{name}.log")
            wait = BACKOFF[min(fails - 1, len(BACKOFF) - 1)]
            self.log(f"{name}: exit {rc}; retry in {wait} s ({fails}/{MAX_FAILS - 1} retries without progress)")
            if self.stopping.wait(wait):
                raise Stop("interrupted")

    def launch(self, threads, *pipeline_args):
        if pipeline_args[0] not in PIPELINE_COMMANDS:
            raise Stop(f"pipeline command {pipeline_args[0]!r} is not part of steps 4-5")
        return [PY, os.path.join(self.snap, "scripts", "step4_5_launch.py"), "--threads", str(threads), "--",
                *pipeline_args]

    # -- monitor ------------------------------------------------------------------------------------------------------
    def disk_name(self):
        st = os.stat(self.out)
        try:
            return os.path.basename(os.path.realpath(f"/sys/dev/block/{os.major(st.st_dev)}:{os.minor(st.st_dev)}"))
        except OSError:
            return None

    def disk_sectors(self, dev):
        for line in open("/proc/diskstats"):
            f = line.split()
            if f[2] == dev:
                return int(f[5]), int(f[9])
        return 0, 0

    def cpu_times(self):
        f = open("/proc/stat").readline().split()[1:]
        v = [int(x) for x in f]
        return sum(v[:8]) - v[3] - v[4], sum(v[:8])

    def cpu_temp(self):
        base = "/sys/class/hwmon"
        try:
            for h in sorted(os.listdir(base)):
                if open(os.path.join(base, h, "name")).read().strip() == "coretemp":
                    return int(open(os.path.join(base, h, "temp1_input")).read()) / 1000
        except OSError:
            pass
        return None

    def gpu(self):
        try:
            r = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total,temperature.gpu,utilization.gpu",
                                "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=30)
            return [x.strip() for x in r.stdout.strip().splitlines()[0].split(",")]
        except (OSError, subprocess.SubprocessError, IndexError):
            return None

    def resource_line(self, prev):
        dev = self.disk_name()
        busy, total = self.cpu_times()
        rd, wr = self.disk_sectors(dev) if dev else (0, 0)
        t = time.time()
        m = meminfo()
        line = None
        if prev:
            dt = t - prev["t"]
            cpu = 100.0 * (busy - prev["busy"]) / max(1, total - prev["total"])
            g = self.gpu()
            line = (f"RES cpu {cpu:.0f}% load {os.getloadavg()[0]:.1f} | ram used "
                    f"{(m['MemTotal'] - m['MemAvailable']) / 2**30:.1f} GiB avail {m['MemAvailable'] / 2**30:.1f} GiB "
                    f"run_rss {tree_rss(os.getpid()) / 2**30:.1f} GiB (cap {self.mem_cap / 2**30:.1f}) swap_used "
                    f"{(m['SwapTotal'] - m['SwapFree']) / 2**30:.2f} GiB | gpu mem "
                    f"{g[0] + '/' + g[1] + ' MiB' if g else 'n/a'} temp {g[2] + ' C' if g else 'n/a'} util "
                    f"{g[3] + '%' if g else 'n/a'} | cpu temp {self.cpu_temp()} C | disk {dev} read "
                    f"{(rd - prev['rd']) * 512 / dt / 1e6:.1f} MB/s write {(wr - prev['wr']) * 512 / dt / 1e6:.1f} MB/s"
                    f" | active {sorted(self.procs)}")
        return line, dict(t=t, busy=busy, total=total, rd=rd, wr=wr)

    def pressure(self, swap_hist):
        m = meminfo()
        swap_hist.append((time.time(), vmstat("pswpout")))
        while swap_hist and swap_hist[0][0] < time.time() - 60:
            swap_hist.pop(0)
        swapped = (swap_hist[-1][1] - swap_hist[0][1]) * os.sysconf("SC_PAGE_SIZE")
        rss = tree_rss(os.getpid())
        reasons = []
        if rss > self.mem_cap:
            reasons.append(f"run resident memory {rss / 2**30:.1f} GiB > cap {self.mem_cap / 2**30:.1f} GiB")
        if m["MemAvailable"] < 0.05 * m["MemTotal"]:
            reasons.append(f"MemAvailable {m['MemAvailable'] / 2**30:.1f} GiB < 5 %")
        if swapped > 64 << 20:
            reasons.append(f"swap-out {swapped / 2**20:.0f} MiB in 60 s")
        return reasons

    def monitor(self):
        prev, swap_hist, strikes, last_res = None, [], 0, 0.0
        _, prev = self.resource_line(None)
        while not self.stopping.wait(WATCH_INTERVAL):
            if time.time() - last_res >= RES_INTERVAL:
                line, prev = self.resource_line(prev)
                if line:
                    self.log(line)
                last_res = time.time()
            reasons = self.pressure(swap_hist)
            if not reasons:
                strikes = 0
                continue
            with self.lock:
                active = [(start, name, p, lane) for name, (p, start, lane) in self.procs.items()]
            lanes_active = [x for x in active if x[3] is not None]
            if len(lanes_active) >= 2:
                start, name, p, lane = max(lanes_active)
                self.log(f"memory pressure ({'; '.join(reasons)}): concurrency 2 -> 1, stopping {name}")
                lane.deferred = True
                lane.defer_kill = True
                p.terminate()
                swap_hist.clear()
                strikes = 0
                continue
            strikes += 1
            self.log(f"memory pressure with one process ({'; '.join(reasons)}), strike {strikes}/3")
            if strikes >= 3:
                self.shutdown("memory pressure with a single process")
                return

    def shutdown(self, why):
        with self.lock:
            if self.stopping.is_set():
                return
            self.stopping.set()
            self.state["stop_reason"] = why                      # the first reason is kept
            self.save()
        self.log(f"shutting down: {why}")
        with self.lock:
            procs = [p for p, _, _ in self.procs.values()]
        for p in procs:
            p.terminate()
        deadline = time.time() + 60
        for p in procs:
            try:
                p.wait(max(1, deadline - time.time()))
            except subprocess.TimeoutExpired:
                p.kill()

    # -- stages ---------------------------------------------------------------------------------------------------------
    def verify_record_commit(self, rec, launch):
        """The step-4 commit: parent = launch commit, message prefix, diff = exactly the step-4 record files."""
        if git(self.repo, "rev-parse", f"{rec}^") != launch:
            raise Refuse(f"refused: the parent of {rec[:12]} is not the launch commit {launch[:12]}")
        if not git(self.repo, "log", "-1", "--format=%s", rec).startswith(RECORD_PREFIX):
            raise Refuse(f"refused: {rec[:12]} is not a step-4 record commit of this runner")
        changed = set(git(self.repo, "diff-tree", "--no-commit-id", "--name-only", "-r", rec).splitlines())
        if changed != RECORD_FILES:
            raise Refuse(f"refused: the diff of {rec[:12]} is not records-only: {sorted(changed ^ RECORD_FILES)[:3]}")

    def own_uncommitted_records(self):
        """Untracked step-4 record files written by this run before an interruption (paths and SHA-256 in state)."""
        written = self.state.get("step4_record_files") or {}
        return {p for p, sha in written.items()
                if os.path.exists(os.path.join(self.repo, p)) and sha256_file(os.path.join(self.repo, p)) == sha}

    def stray_workers(self):
        hits = []
        for d in os.listdir("/proc"):
            if d.isdigit() and int(d) != os.getpid():
                try:
                    cmd = open(f"/proc/{d}/cmdline", "rb").read().decode(errors="replace").split("\0")
                except OSError:
                    continue
                if any(x.startswith(self.out) for x in cmd) and any(
                        x.endswith(("step4_5_launch.py", "stage_ds203_videos.py", "step4_5_orchestrate.py"))
                        for x in cmd):
                    hits.append(int(d))
        return hits

    def preflight(self):
        """Provenance checks (CC_TASK_SS_step4_5_resume_v1.md §1), then inputs. Raises Refuse; changes nothing."""
        repo, exp = self.repo, self.a.expect_commit
        head = git(repo, "rev-parse", "HEAD")
        launch, rec = self.state.get("launch_commit"), self.state.get("record_commit")
        if launch and launch != exp:
            raise Refuse(f"refused: this output directory belongs to launch commit {launch[:12]}, not {exp[:12]}")
        if rec:
            if head != rec:
                raise Refuse(f"refused: HEAD {head[:12]} is not this run's step-4 record commit {rec[:12]}")
            self.verify_record_commit(rec, exp)
        elif head != exp:
            raise Refuse(f"refused: HEAD {head[:12]} is not --expect-commit {exp[:12]}")
        if git(repo, "show", f"{head}:scripts/run_step4_5.sh", check=False) == "":
            raise Refuse("refused: HEAD does not contain scripts/run_step4_5.sh")
        own = set() if rec else self.own_uncommitted_records()
        dirty = [l for l in git(repo, "status", "--porcelain", "--untracked-files=all").splitlines()
                 if not (l.startswith("?? ") and l[3:] in own)]
        if dirty:
            raise Refuse(f"refused: working tree not clean: {dirty[:3]}")
        stray = self.stray_workers()
        if stray:
            raise Refuse(f"refused: processes of an earlier run are still alive: {stray[:5]}")
        for rel, sha in WEIGHT_SHA256.items():
            p = os.path.join(self.a.weights, rel)
            if not os.path.exists(p) or sha256_file(p) != sha:
                raise Refuse(f"refused: weight file missing or SHA-256 differs: {rel}")
        for d, dig in THIRD_PARTY_DIGEST.items():
            got, _ = third_party_digest(os.path.join(repo, "third_party", d))
            if got != dig:
                raise Refuse(f"refused: third_party/{d} differs from the pinned tree digest")
        if not os.path.exists(self.a.archive_zip):
            raise Refuse("refused: archive not found")
        for tool in ("ffmpeg", "ffprobe", "nvidia-smi", "git", "taskset"):
            if shutil.which(tool) is None:
                raise Refuse(f"refused: {tool} not found")
        if not git(repo, "config", "--local", "user.email", check=False):
            raise Refuse("refused: no repository-scoped git identity (git config --local user.email)")
        return head

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
        arch = subprocess.run(["git", "-C", self.repo, "archive", "--format=tar", exp], capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", self.snap], input=arch.stdout, check=True)
        for d in THIRD_PARTY_DIGEST:
            shutil.copytree(os.path.join(self.repo, "third_party", d), os.path.join(self.snap, "third_party", d),
                            ignore=shutil.ignore_patterns("__pycache__"))
        files = {}
        for root, dirs, fs in os.walk(self.snap):
            for f in fs:
                p = os.path.join(root, f)
                files[os.path.relpath(p, self.snap)] = sha256_file(p)
        json_write(meta_p, dict(commit=exp, created=now(), files=files))
        self.log(f"code snapshot of {exp[:12]} created ({len(files)} files, incl. third_party/LeanVAE, SurgeNet)")

    def expected_cases(self):
        if "case_ids" not in self.state:
            code = ("import json,sys; sys.path.insert(0, '.'); from ss_benchmark import design; "
                    "print(json.dumps(list(design.representation_cases().case_id)))")
            r = subprocess.run([PY, "-c", code], cwd=self.snap, capture_output=True, text=True, check=True,
                               env=self.env(1))
            self.state["case_ids"] = json.loads(r.stdout)
            self.save()
        return self.state["case_ids"]

    def staged_count(self):
        return len(json_read(os.path.join(self.staged, "staged_manifest.json"), {}) or {})

    def arm_dir(self, arm):
        return os.path.join(self.out, "extract", arm)

    def arm_count(self, arm):
        return len(json_read(os.path.join(self.arm_dir(arm), "manifest.json"), {}) or {})

    def run(self):
        if self.state.get("status") == "complete":
            raise Refuse("this run is already complete")
        head = self.preflight()                                   # refuses before anything is changed
        self.state.setdefault("launch_commit", self.a.expect_commit)
        self.state.pop("stop_reason", None)
        self.state.update(pid=os.getpid(), last_start=now(), status="running")
        self.state.setdefault("settings", dict(
            physical_cores=self.n_cores, workers=self.n_workers, worker_cpus=self.worker_cpus,
            reserved_cpus=self.reserved_cpus, threads_per_process=self.threads,
            memory_cap_bytes=self.mem_cap, lanes=[list(x) for x in LANES], max_concurrent_readers=len(LANES),
            determinism=dict(cudnn_deterministic=True, cudnn_benchmark=False,
                             use_deterministic_algorithms="True (warn_only)", CUBLAS_WORKSPACE_CONFIG=":4096:8"),
            batch=64, device="cuda", dtype_on_cuda="bfloat16 (locked extract_all)"))
        self.save()
        os.sched_setaffinity(0, set(self.reserved_cpus))
        threading.Thread(target=self.monitor, daemon=True).start()
        self.log(f"preflight passed: HEAD {head[:12]} (launch commit {self.a.expect_commit[:12]}"
                 f"{', step-4 record commit ' + self.state['record_commit'][:12] if self.state.get('record_commit') else ''}"
                 f"); clean tree; weights and third_party verified; {self.n_cores} physical cores, {self.n_workers} "
                 f"workers on CPUs {self.worker_cpus}, reserved CPUs {self.reserved_cpus}; memory cap "
                 f"{self.mem_cap / 2**30:.1f} GiB")
        self.snapshot()
        cases = self.expected_cases()
        w = self.threads
        # staging (byte copy, CRC-32 checked; no decoding)
        if self.stage_status("stage") != "done":
            self.run_unit("stage", [PY, os.path.join(self.snap, "scripts", "stage_ds203_videos.py"), "--zip",
                                    os.path.abspath(self.a.archive_zip), "--dest", self.staged], 1, self.staged_count)
        # 4a mask check
        mc = os.path.join(self.out, "step4", "mask_check.json")
        os.makedirs(os.path.dirname(mc), exist_ok=True)
        if self.stage_status("mask_check") != "done":
            self.run_unit("mask_check", self.launch(w, "mask-check", "--videos", self.videos, "--out", mc), w)
        ok, msg = validate_mask_check(json_read(mc, {}))
        if not ok:
            self.state["mask_check_valid"] = False
            raise Stop(f"{msg}; STOP before any extraction")
        self.state["mask_check_valid"] = True
        self.log(f"mask check valid ({msg})")
        r = repr(float(json_read(mc)["r"]))
        # 4b extraction, two lanes
        self.lanes = [Lane(self, arms, cases, r) for arms in LANES]
        for lane in self.lanes:
            lane.start()
        for lane in self.lanes:
            while lane.is_alive():
                lane.join(5)
        errs = [lane.error for lane in self.lanes if lane.error]
        if errs:
            raise errs[0]
        for arm in ARM_ORDER:
            man = json_read(os.path.join(self.arm_dir(arm), "manifest.json"), {})
            if sorted(man) != sorted(cases) or not all(
                    os.path.exists(os.path.join(self.arm_dir(arm), f"{c}.npy")) for c in cases):
                raise Stop(f"extraction {arm}: manifest does not cover the {len(cases)} cases")
        nu = os.path.join(self.out, "step4", "near_uniform.json")
        if self.stage_status("near_uniform") != "done":
            self.run_unit("near_uniform", self.launch(w, "near-uniform", "--extract", self.arm_dir("P"), "--out", nu),
                          w)
        # step-4 record and commit (execution-order safeguard: step 5 needs this commit)
        if not self.state.get("record_commit"):
            self.write_step4_record(cases, mc, nu)
            self.commit_step4_record()
        if git(self.repo, "rev-parse", "HEAD") != self.state["record_commit"]:
            raise Stop("HEAD is not the step-4 record commit; step 5 not started")
        # step 5
        s5 = os.path.join(self.out, "step5")
        os.makedirs(s5, exist_ok=True)
        reps = os.path.join(s5, "reps.npz")
        if self.stage_status("build_reps") != "done":
            self.run_unit("build_reps", self.launch(w, "build-reps", "--extract",
                                                    *[f"{a}={self.arm_dir(a)}" for a in ARM_ORDER], "--out", reps), w)
        if self.stage_status("checks") != "done":
            self.run_unit("checks", self.launch(w, "checks", "--reps-full",
                                                *[os.path.join(s5, f"reps_full_{a}.npz") for a in ARM_ORDER],
                                                "--out", os.path.join(s5, "checks.json")), w)
        self.write_step5_record(s5)
        self.state["status"] = "complete"
        self.save()
        self.log("run complete: step-4 record committed, step-5 record written (not committed); "
                 "§14 step 6 is not part of this runner")

    # -- records --------------------------------------------------------------------------------------------------------
    def write_step4_record(self, cases, mc, nu):
        d = os.path.join(self.repo, "results", "step4")
        os.makedirs(os.path.join(d, "extract_manifests"), exist_ok=True)
        rep = {}
        for arm in ARM_ORDER:
            key, acq, wrel = ARMS[arm]
            files = []
            for f in sorted(os.listdir(self.arm_dir(arm))):
                if f.endswith(".npy"):
                    p = os.path.join(self.arm_dir(arm), f)
                    shape, dtype = npy_header(p)
                    files.append(dict(path=os.path.relpath(p, self.out), shape=shape, dtype=dtype,
                                      sha256=sha256_file(p)))
            man_p = os.path.join(self.arm_dir(arm), "manifest.json")
            shutil.copy2(man_p, os.path.join(d, "extract_manifests", f"{arm}.json"))
            rep[arm] = dict(model=key, acquisition=acq, weights=wrel, weights_sha256=self._wsha(wrel),
                            locked_manifest_sha256=sha256_file(man_p), n_cases=len(cases), files=files)
        json_write(os.path.join(d, "representation_manifest.json"),
                   dict(root=self.out, note="paths relative to root (LaCie); representations are not in the "
                                            "repository", arms=rep))
        shutil.copy2(mc, os.path.join(d, "mask_check.json"))
        shutil.copy2(nu, os.path.join(d, "near_uniform.json"))
        shutil.copy2(os.path.join(self.staged, "staged_manifest.json"), os.path.join(d, "staged_manifest.json"))
        snap = json_read(os.path.join(self.out, "code_snapshot.json"))
        json_write(os.path.join(d, "run_meta.json"), dict(
            expect_commit=self.a.expect_commit, code_snapshot_files=len(snap["files"]),
            code_snapshot_sha256=hashlib.sha256(json.dumps(snap["files"], sort_keys=True).encode()).hexdigest(),
            third_party_digest=THIRD_PARTY_DIGEST, settings=self.state["settings"],
            stages={k: v for k, v in self.state.get("stages", {}).items()}, mask_check_valid=True))
        n_files = sum(len(v["files"]) for v in rep.values())
        with open(os.path.join(d, "STEP4_RECORD.md"), "w") as f:
            f.write(f"""# §14 step 4 record (written by scripts/run_step4_5.sh)

* Code: expected commit `{self.a.expect_commit}` (run from a code snapshot; `run_meta.json`).
* 4a mask check: `mask_check.json` (locked `pipeline mask-check`; validity checked against the frozen rule).
* 4b extraction: four arms x {len(cases)} cases; `representation_manifest.json` lists {n_files} files (path, shape,
  dtype, SHA-256), relative to `{self.out}`; the locked per-arm manifests are in `extract_manifests/`.
* Near-uniform: `near_uniform.json` (locked `pipeline near-uniform` on the primary standardized arm); per-frame flags
  are the `*.near_uniform.npy` files in the manifest.
* Staging: `staged_manifest.json` (archive members byte-copied, CRC-32 checked; no re-encoding).
* This record is committed before step 5 starts (execution-order safeguard).
""")
        self.state["step4_record_files"] = {
            os.path.relpath(os.path.join(r_, f), self.repo): sha256_file(os.path.join(r_, f))
            for r_, _, fs in os.walk(d) for f in fs}
        self.save()

    def _wsha(self, wrel):
        return {k: v for k, v in WEIGHT_SHA256.items() if k == wrel or k.startswith(wrel + "/")}

    def commit_step4_record(self):
        repo, launch = self.repo, self.a.expect_commit
        try:
            if git(repo, "rev-parse", "HEAD") != launch:
                raise Stop("HEAD moved during the run")
            own = self.own_uncommitted_records()
            if own != RECORD_FILES:
                raise Stop("the step-4 record files are not exactly the expected set")
            dirty = [l for l in git(repo, "status", "--porcelain", "--untracked-files=all").splitlines()
                     if not (l.startswith("?? ") and l[3:] in own)]
            if dirty:
                raise Stop(f"working tree has other changes: {dirty[:3]}")
            git(repo, "add", "--", *sorted(RECORD_FILES))
            if set(git(repo, "diff", "--cached", "--name-only").splitlines()) != RECORD_FILES:
                raise Stop("staged paths are not exactly the step-4 records")
            git(repo, "commit", "-q", "-m", f"{RECORD_PREFIX}: representation manifest, mask check, near-uniform; "
                                            f"records only\n\nRun output: {self.out}\nLaunch commit: {launch}\n")
            head = git(repo, "rev-parse", "HEAD")
            self.verify_record_commit(head, launch)
        except Stop as e:
            raise Stop(f"step-4 record commit failed ({e}); step 5 not started")
        self.state["record_commit"] = head
        self.save()
        self.log(f"step-4 record committed: {head}")

    def write_step5_record(self, s5):
        """Written under the run output first, then copied to results/step5/ as the last action; never committed."""
        d = os.path.join(self.out, "step5_record")
        os.makedirs(d, exist_ok=True)
        for f in ("checks.json", "reps_report.json"):
            shutil.copy2(os.path.join(s5, f), os.path.join(d, f))
        files = {f: dict(bytes=os.path.getsize(os.path.join(s5, f)), sha256=sha256_file(os.path.join(s5, f)))
                 for f in sorted(os.listdir(s5)) if f.endswith((".npz", ".json"))}
        json_write(os.path.join(d, "step5_manifest.json"), dict(root=s5, record_commit=self.state["record_commit"],
                                                               files=files))
        with open(os.path.join(d, "STEP5_RECORD.md"), "w") as f:
            f.write(f"""# §14 step 5 record (written by scripts/run_step4_5.sh; NOT committed)

* Inputs: the step-4 representations of record commit `{self.state['record_commit']}`.
* `checks.json`: locked `pipeline checks` (E1, E2 all variants, E3-site, E3-state-retention, probes and reporting
  paths; 278- and 158-case sets) on `reps_full_<P|P-nat|S|REF>.npz` from locked `pipeline build-reps`.
* `reps_report.json`: the fold-wise PCA / LEACE report; `step5_manifest.json`: sizes and SHA-256 of the step-5 files
  in `{s5}`.
* Not committed by the runner. §13 and §14 step 6 are outside this runner.
""")
        shutil.copytree(d, os.path.join(self.repo, "results", "step5"), dirs_exist_ok=True)
        self.set_stage("step5_record", "done")


class Lane(threading.Thread):
    def __init__(self, runner, arms, cases, r):
        super().__init__(daemon=True)
        self.runner, self.arms, self.cases, self.r = runner, arms, cases, r
        self.deferred = False
        self.defer_kill = False
        self.error = None

    def run(self):
        R = self.runner
        try:
            for arm in self.arms:
                if R.stage_status(f"extract_{arm}") == "done":
                    continue
                key, acq, wrel = ARMS[arm]
                cmd = R.launch(R.threads, "extract", "--videos", R.videos, "--model", key, "--acq", acq,
                               "--r", self.r, "--out", R.arm_dir(arm), "--weights", os.path.join(R.a.weights, wrel),
                               "--batch", "64", "--device", "cuda")
                R.run_unit(f"extract_{arm}", cmd, R.threads, lambda arm=arm: R.arm_count(arm), lane=self)
        except Stop as e:
            self.error = e
            R.shutdown(str(e))
        except Exception as e:                                                   # noqa: BLE001
            self.error = Stop(f"lane {self.arms}: {e!r}")
            R.shutdown(str(e))


# ---------------------------------------------------------------------------------------------------------------------
def status(out):
    st = json_read(os.path.join(out, "state.json"), {}) or {}
    stages = st.get("stages", {})
    pid = st.get("pid")
    alive = False
    if pid:
        try:
            os.kill(pid, 0)
            alive = "step4_5_orchestrate" in open(f"/proc/{pid}/cmdline").read()
        except OSError:
            alive = False
    n = len(st.get("case_ids", [])) or "?"
    plan = json_read(os.path.join(out, "staged", "staged_plan.json"), {}) or {}
    staged = len(json_read(os.path.join(out, "staged", "staged_manifest.json"), {}) or {})
    lines = [f"runner: {'running (pid %d)' % pid if alive else 'not running'}; state "
             f"{st.get('status', 'not started')}" + (f"; STOPPED: {st['stop_reason']}" if st.get("stop_reason") else ""),
             f"staging: {staged}/{plan.get('members', '?')} files ({stages.get('stage', {}).get('status', 'pending')})",
             f"4a mask check: {stages.get('mask_check', {}).get('status', 'pending')}"]
    for arm in ARM_ORDER:
        k = len(json_read(os.path.join(out, "extract", arm, "manifest.json"), {}) or {})
        lines.append(f"extract {arm}: {k}/{n} cases ({stages.get('extract_' + arm, {}).get('status', 'pending')})")
    lines.append(f"near-uniform record: {stages.get('near_uniform', {}).get('status', 'pending')}")
    lines.append(f"step-4 record commit: {st.get('record_commit') or 'pending'}")
    for s in ("build_reps", "checks", "step5_record"):
        lines.append(f"step 5 {s}: {stages.get(s, {}).get('status', 'pending')}")
    try:
        log = open(os.path.join(out, "logs", "progress.log")).read().splitlines()
    except OSError:
        log = []
    lines.append(f"last progress-log entry: {log[-1][:25] if log else 'none'}")
    res = [l for l in log if " RES " in l]
    lines.append(f"resources: {res[-1] if res else 'no sample yet'}")
    print("\n".join(lines))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    for k in ("--repo", "--expect-commit", "--out", "--archive-zip", "--weights"):
        r.add_argument(k, required=True)
    s = sub.add_parser("status")
    s.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "status":
        return status(a.out)
    run = Runner(a)

    def on_signal(signum, _frame):
        threading.Thread(target=run.shutdown, args=(f"interrupted by signal {signum}",), daemon=True).start()

    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
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
