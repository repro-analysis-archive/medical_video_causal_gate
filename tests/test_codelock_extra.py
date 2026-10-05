"""Code-lock extra engineering checks (not among the seven A2 fast tests). Run in the extraction environment:

    /home/user/.venvs/ss_extract/bin/python -m pytest -p no:cacheprovider tests/test_codelock_extra.py

* every registry adapter builds with random initialisation (no weights) and encodes a synthetic input at its protocol
  input size / clip length on CUDA in bf16 (the §4.1.4 rule-4 test code path); output finite;
* the extraction compute projection code runs on a measured synthetic throughput (code path only; no decision);
* the decode path (ffprobe / ffmpeg) on a synthetic lavfi test video (not DS203): 2-fps grid by presentation time,
  standardized frames, near-uniform flag, mask-check accumulation, frame- and clip-level extraction and the Cosmos
  native-frame selection.
Seeds: torch / numpy seed 0 for random initialisation; the lavfi test pattern is deterministic.
"""
import os
import subprocess
import sys

import numpy as np
import pytest
import torch

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", DIFFUSERS_OFFLINE="1")

from ss_benchmark import extract, feasibility, preprocess  # noqa: E402

cuda = pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")


@cuda
@pytest.mark.parametrize("key", list(feasibility.REGISTRY))
def test_adapter_random_init_gpu_memory(key):
    res = feasibility.gpu_memory_test(key)
    print(res)
    assert res["output_dim"] > 0 and res["peak_reserved_gb"] > 0


@cuda
def test_extraction_projection_code_path():
    thr = feasibility.synthetic_throughput("SelfSupSurg-ResNet50", batch=32, n_batches=3)
    proj = feasibility.extraction_projection("SelfSupSurg-ResNet50", thr["inputs_per_second"])
    print(thr, proj)
    assert proj["serial_hours"] > 0


@pytest.fixture(scope="module")
def synthetic_video(tmp_path_factory):
    p = str(tmp_path_factory.mktemp("vid") / "testsrc.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=640x360:rate=25:duration=32",
                    "-pix_fmt", "yuv420p", "-c:v", "libx264", "-g", "50", "-bf", "2", p], check=True)
    return p


def test_decode_grid_extract(synthetic_video):
    info = preprocess.probe_video(synthetic_video)
    pts = info["pts"]
    n_steps = int(np.floor(info["duration"] / 5.0))
    gidx = preprocess.grid_frame_indices(pts, n_steps)
    assert preprocess.complete_steps(gidx) == n_steps
    frames = preprocess.decode_selected(synthetic_video, gidx, info["width"], info["height"])
    grid = np.stack([frames[k] for k in gidx])
    assert grid.shape == (10 * n_steps, info["height"], info["width"], 3)
    assert (pts[gidx] < 5.0 * (np.arange(10 * n_steps) // 10) + 5.0).all()
    x = preprocess.standardize(grid, 224)
    assert x.shape == (10 * n_steps, 3, 224, 224) and float(x[:, :, 0, 0].abs().max()) == 0.0
    flags, sd = preprocess.near_uniform_flags(grid)
    assert flags.shape == (10 * n_steps,) and not flags.any()
    mc = preprocess.MaskCheck()
    mc.add(2, grid[preprocess.MaskCheck.selected_grid_frames(len(grid))])
    r = mc.result()
    assert 0 < r["r"] <= 0.45 + 1e-12
    nat = preprocess.native(grid, (224, 224))
    assert nat.shape == x.shape
    from ss_benchmark.models import prim_resnet50, sec_videomae
    torch.manual_seed(0)
    m = prim_resnet50.build()
    E = extract.embed_frames(x, lambda b: prim_resnet50.encode(m, b), batch=32)
    steps = extract.frame_level_steps(E, n_steps)
    assert steps.shape == (n_steps, 2048) and np.isfinite(steps).all()
    v = sec_videomae.build()
    C, clips = extract.embed_clips(x, lambda b: sec_videomae.encode(v, b), 16, n_steps, batch=2)
    assert C.shape == (n_steps, 768) and np.isfinite(C).all()
    idx = preprocess.step_native_indices(pts, 1)
    nf = preprocess.decode_selected(synthetic_video, idx, info["width"], info["height"])
    video, sel = extract.cosmos_input(np.stack([nf[k] for k in idx]))
    assert len(idx) == 125 and len(sel) == 121 and video.shape == (1, 3, 121, 320, 320)
    assert float(video.min()) >= -1.0 and float(video.max()) <= 1.0


# ---------------------------------------------------------------------------------------------------------------------
# pipeline glue (synthetic videos in a fake Full_Videos tree; PLACEHOLDER representations)
# ---------------------------------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def fake_tree(tmp_path_factory):
    root = tmp_path_factory.mktemp("Full_Videos")
    specs = {("Center9_001", "Center9_001.mp4"): 41, ("Center9_02", "Center9_002_v01.mp4"): 25,
             ("Center9_02", "Center9_002_v02.mp4"): 21}
    for (d, f), dur in specs.items():
        os.makedirs(root / "Center9" / d, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                        f"testsrc2=size=480x270:rate=25:duration={dur}", "-pix_fmt", "yuv420p", "-c:v", "libx264",
                        "-bf", "2", str(root / "Center9" / d / f)], check=True)
    return str(root)


def test_pipeline_extract_case(fake_tree):
    from ss_benchmark import pipeline
    from ss_benchmark.models import prim_resnet50, sec_videomae
    files = pipeline.case_files(fake_tree, 9, 2)
    assert [os.path.basename(f) for f in files] == ["Center9_002_v01.mp4", "Center9_002_v02.mp4"]
    torch.manual_seed(0)
    m = prim_resnet50.build()
    with torch.inference_mode():
        out, flags, info = pipeline.extract_case(files, "SelfSupSurg-ResNet50", m, prim_resnet50, "standardized",
                                                 0.45, 16, "cpu")
    assert out.shape == (9, 2048) and info["n_steps"] == 9 and info["grid_frames_after_step_end"] == 0
    infos, pts, fid, local, dur = pipeline.case_timeline(files)
    gidx = preprocess.grid_frame_indices(pts, 9)
    frames = {}
    for k, f in enumerate(files):
        want = local[gidx][fid[gidx] == k]
        got = preprocess.decode_selected(f, want, infos[k]["width"], infos[k]["height"])
        frames.update({(k, j): v for j, v in got.items()})
    grid = np.stack([frames[(int(fid[g]), int(local[g]))] for g in gidx])
    with torch.inference_mode():
        E = extract.embed_frames(preprocess.standardize(grid, 224), lambda b: prim_resnet50.encode(m, b), 16)
    np.testing.assert_allclose(out, extract.frame_level_steps(E, 9), rtol=1e-4, atol=1e-5)
    v = sec_videomae.build()
    with torch.inference_mode():
        out2, _, info2 = pipeline.extract_case(files, "VideoMAE-base", v, sec_videomae, "native", 0.45, 4, "cpu")
    assert out2.shape == (9, 768) and np.isfinite(out2).all()


@cuda
def test_pipeline_extract_cosmos(fake_tree):
    from ss_benchmark import pipeline
    from ss_benchmark.models import ref_cosmos
    files = pipeline.case_files(fake_tree, 9, 1)
    torch.manual_seed(0)
    vae = ref_cosmos.build(device="cuda", dtype=torch.bfloat16)
    with torch.inference_mode():
        out, _, info = pipeline.extract_case(files, "Cosmos-CV8x8x8", vae, ref_cosmos, "standardized", 0.45, 1,
                                             "cuda")
    assert out.shape == (8, 25600) and np.isfinite(out).all()


def test_pipeline_build_reps_checks_grid_load(tmp_path):
    import pandas as pd
    from ss_benchmark import design as dsg, grid_driver, pipeline, placeholder, seeds
    rep_set = dsg.placeholder_representation_set()
    designs = {s: dsg.placeholder_design(s, rep_set) for s in ("primary", "W0", "W5", "single_file")}
    raw = placeholder.raw_representations(rep_set, "P")
    d = tmp_path / "extract_P"
    os.makedirs(d)
    for cid, x in zip(rep_set.case_id, raw):
        np.save(d / f"{cid}.npy", x.astype(np.float32))
    cases = pd.DataFrame(dict(case_id=rep_set.case_id, center=rep_set.centre))
    out = str(tmp_path / "reps.npz")
    pipeline.build_reps({"P": str(d)}, out, cases=cases, folds=rep_set.fold.to_numpy(), designs=designs)
    reps, ids = grid_driver.load_reps(out, ("primary", "W0", "W5", "single_file"))
    assert reps["primary"]["P"].shape == (5, 158, 15, 64) and reps["W0"]["P-C"].shape == (5, 204, 15, 64)
    assert list(ids["primary"]) == list(designs["primary"].ids)
    roots = (int(seeds.placeholder_seq("extra", "probe").generate_state(1)[0]),
             int(seeds.placeholder_seq("extra", "boot").generate_state(1)[0]))
    res = pipeline.run_checks({"P": out.replace(".npz", "_full_P.npz")}, str(tmp_path / "checks.json"), cases=cases,
                              folds=rep_set.fold.to_numpy(), designs=designs, roots=roots, n_boot=100)
    assert set(res["P"]["fm_conditions_primary"]) == {"E1", "E3-site", "E3-state"}
