"""Code-lock remediation tests (SS_CODELOCK_PARTA_AUDIT_REMEDIATION.md): the five reporting-only paths and the
truth-only small-truth design check. Engineering checks, not endpoints. Base environment:

    /home/user/miniconda3/bin/python3 -m pytest -p no:cacheprovider tests/test_codelock_reporting.py

Seeds: every random draw comes from a SeedSequence(99990001) stream named in the test ("rep-test", ...); the PLACEHOLDER
design uses its own 99990001 streams. Real metadata: none (the real small-truth path runs in the Part-B runner).
End-to-end determinism of the wired paths (pipeline.run_checks, pipeline.near_uniform) is covered by fast test 6,
which runs the PLACEHOLDER dry run twice and compares the bytes of its output.
"""
import os
import sys

import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

from ss_benchmark import checks, design, dgp, grid, pipeline, seeds  # noqa: E402


def test_near_uniform_summary_exact():
    flags = [np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0] + [1] * 10, bool),     # case A: s = 1
             np.array([0] * 10 + [0, 1] + [0] * 8, bool)]                     # case B: s = 0
    res = checks.near_uniform_summary(flags, centres=[2, 3], switch_steps=[1, 0])
    cs = {(r["centre"], r["S"]): (r["n_frames"], r["n_near_uniform"]) for r in res["by_centre_S"]}
    assert cs == {(2, 0): (10, 1), (2, 1): (10, 10), (3, 0): (0, 0), (3, 1): (20, 1)}
    assert res["overall"] == dict(n_frames=40, n_near_uniform=12, proportion=0.3)
    assert {r["S"]: r["n_near_uniform"] for r in res["by_S"]} == {0: 1, 1: 11}
    assert res["reporting_only"] and checks.near_uniform_summary(flags, [2, 3], [1, 0]) == res


def test_e2_rows_and_normalized_time():
    rows = checks.e2_rows([0, 2], lambda i: np.arange(3) + i, switch_step=np.array([1, 0, 3]),
                          n_steps=np.array([10, 10, 20]))
    assert rows.S.tolist() == [0, 1, 1, 0, 1, 1]      # case 0: steps 0-2, s = 1; case 2: steps 2-4, s = 3
    nt = checks.normalized_time_rows(rows)
    assert np.allclose(nt.time, rows.step / np.array([10, 10, 10, 20, 20, 20]))
    assert (nt.step == rows.step).all() and (nt.S == rows.S).all()


def test_history_rows_lags():
    D = design.placeholder_design("primary")
    cell = grid.find_cell(5, 0, 5, 0.5, 1.0)
    d = dgp.draw(D, cell, seeds.placeholder_seq("rep-test", "history"))
    A, _ = dgp.simulate(D, cell, d)
    idx = np.arange(D.n) + 1000
    rows, H = checks.history_rows(idx, D, A, cell.W, cell.K)
    assert len(rows) == D.n * cell.K and H.shape == (D.n * cell.K, cell.W + cell.K - 1)
    w = D.window_start()
    for k in (0, 7, D.n - 1):
        for t in range(cell.K):
            r = k * cell.K + t
            assert rows.case[r] == idx[k] and rows.step[r] == w[k] + t
            assert rows.S[r] == int(D.offset[k] + t >= 0)
            for ell in range(1, cell.W + cell.K):
                col = cell.W + t - ell
                assert H[r, ell - 1] == (A[k, col] if col >= 0 else 0.0)


def test_reporting_marker_drops_pass():
    out = pipeline._reporting({"delta_auc": 0.1, "pass": True})
    assert "pass" not in out and out["reporting_only"] is True and out["delta_auc"] == 0.1


def test_small_truth_matches_replicate_truth_and_is_deterministic():
    D = design.placeholder_design("primary")
    cells = [grid.all_cells()[i] for i in (0, 9, 117, 171, 216, 230)]
    for c in cells:
        seq = seeds.placeholder_seq("rep-test", "small-truth", c.index)
        d = dgp.draw(D, c, seq)
        perm = seeds.rng(seq, "c-permutation").permutation(4)
        assert abs(dgp.truth_for_permutation(D, c, perm) - dgp.truth(D, c, d)) < 1e-12
    r1 = dgp.small_truth_check(D, cells)
    assert r1 == dgp.small_truth_check(D, cells)
    for r in r1:
        assert r["flag"] == (r["min_abs"] < 0.025) and r["min"] <= r["mean"] <= r["max"]


def test_small_truth_flag_triggers():
    """37 of 40 cases in one centre, S = 0 (offset −15), K = 1, P = 0, W = 0, γ = 1, φ = 0: under the permutation that
    gives that centre −3/√5, truth = (δ − 1) mean(1 + c_i) ≈ −0.012, so |truth| < 0.025 and the flag must be raised;
    a balanced design at K = 15 is not flagged."""
    n = 40
    D = design.Design(label="PLACEHOLDER:flag-test", ids=np.arange(n), centre=np.repeat([101, 102, 103, 104], 10),
                      offset=np.full(n, -15), folds=np.zeros(n, int))
    cell = grid.Cell(-1, 1, 0, 0, 0.0, 1.0, 0.0)
    D1 = design.Design(label="PLACEHOLDER:flag-test-1", ids=np.arange(n), centre=np.r_[np.full(37, 101), [102, 103, 104]],
                       offset=np.full(n, -15), folds=np.zeros(n, int))
    res = dgp.small_truth_check(D1, [cell])[0]
    assert res["flag"] and res["min_abs"] < 0.025
    assert not dgp.small_truth_check(D, [grid.find_cell(15, 0, 0, 0.0, 1.0)])[0]["flag"]
