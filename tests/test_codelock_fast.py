"""Code-lock fast tests (CC_TASK_SS_code_lock_v2.md A2). Engineering checks, not endpoints; criteria fixed by the task.

Seeds and N (recorded before the first run; every seed is 99990001 or a SeedSequence stream derived from it, except
test 4 (protocol fold seed 20261006 on real case IDs) and test 7 (real centre + offset, G-SITE)):

| test | data | seeds | N |
|---|---|---|---|
| 1 truth vs MC | PLACEHOLDER primary design (158 synthetic cases) tiled to N cases; cells K ∈ {1,5,15} × φ_A ∈ {0, 0.5}, P = 5, W = 5, α = 0.5, γ = 1 | SeedSequence(99990001) child ("test1", K, 10·φ_A) for the replicate draws (c-permutation, U, ε, ε_Y streams) | N = 1,000,000 simulated cases per cell |
| 2 SDR smoke | PLACEHOLDER large design ("sdr-smoke", 2,000 cases; centres, offsets, folds from 99990001 streams); cell K = 5, P = 5, W = 5, α = 0.5, γ = 1, φ_A = 0; FULL arm; learner mode "select" | replicate SeedSequence(root = SeedSequence(99990001) child "test2" state, spawn_key = (cell index 135, r)), r = 0..19 | n = 2,000 cases, M = 20 |
| 3 LEACE | synthetic Gaussian features, d = 16, planted linear 4-level label (class means 2.5·e_k) | SeedSequence(99990001) child "test3" (data, split), probe streams child "test3-probe" | 2,000 train + 2,000 test rows |
| 4 folds | real case IDs only (278-case set; primary 158, W0 204, W5 201, single-file 123) | protocol fold seed 20261006 | 278 cases |
| 5 time order | synthetic frame timestamps: CFR 25, 30, 30000/1001 and 50 fps; jittered VFR (gaps < 0.5 s); a two-file case | SeedSequence(99990001) child "test5" (jitter) | 600 s per video; L ∈ {1, 8, 10, 16, 17, 33, 64} |
| 6 determinism | gate stage (--smoke: 6 gate cells × 2 replicates) twice with 3 and 5 workers; PLACEHOLDER dry run twice (n_boot = 200); G-SITE twice | as in the code (99990001 streams; G-SITE none) | — |
| 7 G-SITE | real primary set: centre and offset only | none | 158 cases |
"""
import hashlib
import multiprocessing as mp
import os
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

from ss_benchmark import (arms, checks, design, dgp, extract, grid, learners, preprocess, reduce,  # noqa: E402
                          sdr, seeds)
from ss_benchmark.constants import DELTA, PENALTY_GRID_E2  # noqa: E402

PY = sys.executable
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1",
           MKL_NUM_THREADS="1", PYTHONHASHSEED="0")

TEST1_N = 1_000_000
TEST2_N, TEST2_M = 2000, 20
TEST3_N, TEST3_D = 2000, 16


# ---------------------------------------------------------------------------------------------------------------------
# 1. truth vs Monte Carlo
# ---------------------------------------------------------------------------------------------------------------------
def _tiled_design(D, n):
    return design.Design(label=D.label + f":tiled{n}", ids=np.arange(n), centre=np.resize(D.centre, n),
                         offset=np.resize(D.offset, n), folds=np.zeros(n, int))


@pytest.mark.parametrize("phi", [0.0, 0.5])
@pytest.mark.parametrize("K", [1, 5, 15])
def test_1_truth_vs_monte_carlo(K, phi):
    D = _tiled_design(design.placeholder_design("primary"), TEST1_N)
    cell = grid.Cell(-1, K, 5, 5, 0.5, 1.0, phi)
    seq = seeds.placeholder_seq("test1", K, int(10 * phi))
    d = dgp.draw(D, cell, seq)
    _, Y, _, Y_d = dgp.simulate(D, cell, d, delta=DELTA)
    diff = Y_d - Y
    mc, se = diff.mean(), diff.std(ddof=1) / np.sqrt(TEST1_N)
    S = D.state(dgp.rel_steps(cell))
    if phi == 0:
        truth = dgp.truth_closed_form(d["c"], S[:, cell.W:cell.W + K], cell)
    else:
        truth = dgp.truth_recursion(d["c"], S, cell)
    print(f"K={K} phi={phi}: truth {truth:.8f}  MC {mc:.8f}  SE {se:.2e}  |diff|/SE {abs(truth - mc) / se:.2f}")
    assert abs(truth - mc) <= 4 * se + 1e-8


# ---------------------------------------------------------------------------------------------------------------------
# 2. SDR smoke test
# ---------------------------------------------------------------------------------------------------------------------
def _test2_unit(r):
    D = design.placeholder_large_design(TEST2_N, "sdr-smoke")
    cell = grid.find_cell(5, 5, 5, 0.5, 1.0)
    root = int(seeds.placeholder_seq("test2").generate_state(1)[0])
    seq = seeds.replicate_seq(cell.index, r, root)
    d = dgp.draw(D, cell, seq)
    A, Y = dgp.simulate(D, cell, d)
    res = sdr.sdr_mtp(A, Y, arms.arm_covariates("FULL", D, cell, d), cell.W, cell.K, D.folds,
                      seeds.child(seq, "learners"), "select")
    return dgp.truth(D, cell, d), res


def test_2_sdr_smoke():
    assert grid.find_cell(5, 5, 5, 0.5, 1.0).index == 135
    with mp.get_context("fork").Pool(min(TEST2_M, os.cpu_count())) as pool:
        out = pool.map(_test2_unit, range(TEST2_M))
    truth = np.array([t for t, _ in out])
    est = np.array([r["est"] for _, r in out])
    se = np.array([r["se"] for _, r in out])
    ratios_ok = [r["ratio_all_finite_positive"] for _, r in out]
    bias = float(np.mean(est - truth))
    print(f"mean truth {truth.mean():.4f}  mean bias {bias:.4f}  rel {bias / truth.mean():.3f}  "
          f"ratio range [{min(r['ratio_min'] for _, r in out):.3f}, {max(r['ratio_max'] for _, r in out):.3f}]")
    assert np.isfinite(est).all()
    assert np.isfinite(se).all() and (se > 0).all()
    assert all(ratios_ok)
    assert abs(bias) < 0.10 * abs(truth.mean())


# ---------------------------------------------------------------------------------------------------------------------
# 3. LEACE
# ---------------------------------------------------------------------------------------------------------------------
def test_3_leace():
    rng = seeds.rng(seeds.placeholder_seq("test3"))
    n = 2 * TEST3_N
    y = rng.integers(0, 4, size=n)
    means = np.zeros((4, TEST3_D)); means[np.arange(4), np.arange(4)] = 2.5
    X = means[y] + rng.standard_normal((n, TEST3_D)) @ rng.standard_normal((TEST3_D, TEST3_D)) * 0.5
    perm = rng.permutation(n)
    tr, te = perm[:TEST3_N], perm[TEST3_N:]

    def linear_ba(Xtr, ytr, Xte, yte, tag):
        m = learners.fit_multinomial_cv(Xtr, ytr, np.arange(len(ytr)), seeds.rng(seeds.placeholder_seq(
            "test3-probe", tag)), PENALTY_GRID_E2)
        pred = m.classes[np.argmax(m.predict_proba(Xte), axis=1)]
        return checks.balanced_accuracy(yte, pred)

    pre = linear_ba(X[tr], y[tr], X[te], y[te], "pre")
    le, _ = reduce.fit_leace(X[tr], y[tr])
    ident = reduce.leace_identities(le, X[tr], y[tr])
    post = linear_ba(le.transform(X[tr]), y[tr], le.transform(X[te]), y[te], "post")
    print(f"pre BA {pre:.3f}  post BA {post:.3f}  identities {ident}  rank {le.rank}")
    assert pre >= 0.90
    assert post <= 0.30
    assert max(ident.values()) <= 1e-8


# ---------------------------------------------------------------------------------------------------------------------
# 4. folds
# ---------------------------------------------------------------------------------------------------------------------
def test_4_folds_restricted():
    f278 = design.representation_folds()
    assert len(f278) == 278 and set(f278.unique()) == set(range(5))
    for s in ("primary", "W0", "W5", "single_file"):
        got = design.analysis_set_folds(s)
        expected = {cid: int(f278[cid]) for cid in got.index}
        assert len(got) == design.SET_SIZES[s]
        assert all(int(got[cid]) == expected[cid] for cid in got.index), s


# ---------------------------------------------------------------------------------------------------------------------
# 5. time order
# ---------------------------------------------------------------------------------------------------------------------
def _pts_cases():
    rng = seeds.rng(seeds.placeholder_seq("test5"))
    dur = 600.0
    cases = {f"cfr{fps:.3f}": np.arange(0, dur, 1 / fps) for fps in (25.0, 30.0, 30000 / 1001, 50.0)}
    gaps = rng.uniform(0.02, 0.06, size=int(dur / 0.02))
    cases["vfr_jitter"] = np.cumsum(np.r_[0.0, gaps])[np.cumsum(np.r_[0.0, gaps]) < dur]
    cases["two_files"] = preprocess.physical_pts([np.arange(0, 250.0, 0.04), np.arange(0, 350.0, 0.04)],
                                                 [250.0, 350.0])
    return cases


@pytest.mark.parametrize("name", list(_pts_cases()))
def test_5_time_order(name):
    import torch
    pts = _pts_cases()[name]
    n_steps = int(np.floor((pts[-1] + 1e-9) / 5.0))
    gidx = preprocess.grid_frame_indices(pts, n_steps)
    n_ok = preprocess.complete_steps(gidx)
    assert n_ok >= n_steps - 1
    gpts = pts[gidx[:10 * n_ok]]
    step_end = 5.0 * (np.arange(10 * n_ok) // 10) + 5.0
    assert (gpts < step_end).all()                                      # frame-level steps
    grid = torch.from_numpy(gpts.astype(np.float64)).view(-1, 1, 1, 1).expand(-1, 3, 2, 2).contiguous()
    for L in (1, 8, 10, 16, 17, 33, 64):
        mx, clips = extract.embed_clips(grid, lambda x: x.amax(dim=(1, 2, 3, 4))[:, None], L, n_ok, batch=7)
        ends = 5.0 * np.arange(n_ok) + 5.0
        assert (mx[:, 0] < ends).all(), L                               # no clip frame after its step end
        assert all(c[-1] == 10 * t + 9 and len(c) == L for t, c in enumerate(clips))
        assert all((c[c < 0]).size == 0 for c in clips)
        assert (clips[0][: max(0, L - 10)] == 0).all()                  # first-frame repetition at video start
    for t in range(n_ok):                                               # Cosmos reference: native [5t, 5t+5)
        idx = preprocess.step_native_indices(pts, t)
        sel = idx[extract.cosmos_frame_selection(len(idx))]
        assert len(sel) <= 121 and (pts[sel] >= 5 * t - 1e-9).all() and (pts[sel] < 5 * t + 5).all()
    E = np.repeat(gpts[:, None], 4, axis=1)                             # frame-level pooling uses only 10t..10t+9
    pooled = extract.frame_level_steps(E, n_ok)
    assert (pooled[:, 0] < 5.0 * np.arange(n_ok) + 5.0).all()


# ---------------------------------------------------------------------------------------------------------------------
# 6. determinism
# ---------------------------------------------------------------------------------------------------------------------
def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _tree_hashes(root, rels):
    out = {}
    for rel in rels:
        p = os.path.join(root, rel)
        if os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                out[os.path.join(rel, f)] = _sha(os.path.join(p, f))
        else:
            out[rel] = _sha(p)
    return out


def test_6_determinism(tmp_path):
    procs = []
    for k, workers in ((1, 3), (2, 5)):
        out = tmp_path / f"run{k}"
        procs.append(subprocess.Popen([PY, "-m", "ss_benchmark.codelock_gate", "--out", str(out), "--smoke",
                                       "--workers", str(workers), "--stage", "gate"], cwd=REPO, env=ENV,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT))
        procs.append(subprocess.Popen([PY, "-m", "ss_benchmark.dryrun", "--out", str(tmp_path / f"dry{k}.json"),
                                       "--n-boot", "200"], cwd=REPO, env=ENV, stdout=subprocess.DEVNULL,
                                      stderr=subprocess.STDOUT))
    assert all(p.wait() == 0 for p in procs)
    for k in (1, 2):
        assert subprocess.run([PY, "-m", "ss_benchmark.codelock_gate", "--out", str(tmp_path / f"run{k}"),
                               "--smoke", "--stage", "gsite"], cwd=REPO, env=ENV, capture_output=True).returncode == 0
    rels = ["gate_PLACEHOLDER_replicates.csv", "gate_PLACEHOLDER_cells.json", "gsite_record.json", "work/gate"]
    h1 = _tree_hashes(tmp_path / "run1", rels)
    h2 = _tree_hashes(tmp_path / "run2", rels)
    assert len(h1) == 3 + 12 and h1 == h2
    assert _sha(tmp_path / "dry1.json") == _sha(tmp_path / "dry2.json")


# ---------------------------------------------------------------------------------------------------------------------
# 7. G-SITE
# ---------------------------------------------------------------------------------------------------------------------
def test_7_gsite_primary():
    centre, offset = design.gsite_inputs("primary")
    g = checks.gsite(centre, offset, [c for c in grid.all_cells() if c.phi == 0])
    print(f"eta2 primary = {g['eta2_S_window_start']:.6f}")
    assert round(g["eta2_S_window_start"], 4) == 0.0014
