"""§14 step 4 preparation: Cosmos reference adapter vs the official Cosmos tokenizer code (CC_TASK_SS_step4_5_prep_v2.md
item 1.3; criterion fixed by the task). Run in the extraction environment (weights on LaCie; skipped if absent):

    /home/user/.venvs/ss_extract/bin/python -m pytest -p no:cacheprovider tests/test_step4_cosmos_equivalence.py

* Ours: ss_benchmark.models.ref_cosmos (diffusers AutoencoderKLCosmos, weights vae/diffusion_pytorch_model.safetensors of
  nvidia/Cosmos-1.0-Tokenizer-CV8x8x8 @ 5110dbb3), representation extract.cosmos_representation.
* Official: NVIDIA/Cosmos-Tokenizer @ 3584ae75 (third_party/Cosmos-Tokenizer, raw source), cosmos_tokenizer.utils.
  load_model(autoencoder.jit, tokenizer_config=TokenizerConfigs.CV with spatial / temporal compression 8):
  CausalContinuousVideoTokenizer with the JIT weights; representation = post_quant_conv(encode(x)[0]) averaged over
  latent time. loguru / mediapy (logging, media IO) are stubbed only if absent.
* The official loader is strict=False by design (utils.load_model). The test pins exactly what that leaves out:
  - model-only parameters: encoder.down.1.downsample and decoder.up.2.upsample (conv1-3). With patch size 4 and
    compression 8 both modules have spatial and temporal flags False, so their forward returns the input unchanged
    (in the released trace, down.1.downsample is an empty forward); they never touch the representation;
  - JIT-only entries: the fixed Haar patcher buffers (wavelets, _arange, patch_size_buffer), registered
    non-persistent in the source; the source values rounded to the trace dtype must equal the stored ones;
  - every other tensor must load and equal the JIT's exactly.
* The JIT itself is a bfloat16 trace (dtype constants baked in), so the float32 comparison uses the official
  PyTorch source path.
* Same released checkpoint (the repository's two official formats), float32 on CPU, fixed synthetic input (seed
  99990002): 121 native frames 270 × 480 RGB, prepared by the adapter's own preprocessing (extract.cosmos_input: crop,
  mask r = 0.45, resize 320 × 320, [−1, 1]). Pass: max |difference| of the 16 × 40 × 40 representation ≤ 1e-4.
"""
import os
import sys
import types

import numpy as np
import pytest
import torch

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", DIFFUSERS_OFFLINE="1")

COSMOS = "/media/user/LaCie/medvideo_gate/weights/cosmos/Cosmos-1.0-Tokenizer-CV8x8x8"
SEED = 99990002
TOL = 1e-4


def official_cosmos(jit_path):
    for name in ("loguru", "mediapy"):
        try:
            __import__(name)
        except ImportError:
            m = types.ModuleType(name)
            if name == "loguru":
                m.logger = types.SimpleNamespace(info=lambda *a, **k: None, warning=lambda *a, **k: None,
                                                 debug=lambda *a, **k: None, error=lambda *a, **k: None)
            sys.modules[name] = m
    sys.path.insert(0, os.path.join(REPO, "third_party", "Cosmos-Tokenizer"))
    from cosmos_tokenizer.networks import TokenizerConfigs
    from cosmos_tokenizer.utils import load_model
    cfg = dict(TokenizerConfigs.CV.value)
    cfg.update(dict(spatial_compression=8, temporal_compression=8))
    model = load_model(jit_path, tokenizer_config=cfg, device="cpu")
    ckpt = torch.jit.load(jit_path, map_location="cpu").state_dict()
    return model, ckpt


def test_cosmos_adapter_vs_official():
    jit = os.path.join(COSMOS, "autoencoder.jit")
    if not (os.path.exists(jit) and os.path.exists(os.path.join(COSMOS, "vae", "diffusion_pytorch_model.safetensors"))):
        pytest.skip("Cosmos weights not present")
    from ss_benchmark import extract
    from ss_benchmark.models import ref_cosmos
    torch.set_num_threads(os.cpu_count())
    official, ckpt = official_cosmos(jit)
    off_sd = official.state_dict()
    noop = ("encoder.down.1.downsample", "decoder.up.2.upsample")
    model_only = {f"{m}.conv{i}.conv3d.{t}" for m in noop for i in (1, 2, 3) for t in ("weight", "bias")}
    patch_bufs = {f"{c}.{b}" for c, bs in (("encoder.patcher3d", ("wavelets", "_arange", "patch_size_buffer")),
                                          ("decoder.unpatcher3d", ("wavelets", "_arange"))) for b in bs}
    assert set(off_sd) - set(ckpt) == model_only
    assert set(ckpt) - set(off_sd) == patch_bufs
    for name in noop:
        mod = official.get_submodule(name)
        flags = [getattr(mod, f) for f in ("spatial_down", "temporal_down", "spatial_up", "temporal_up")
                 if hasattr(mod, f)]
        assert len(flags) == 2 and not any(flags), name
    buffers = dict(official.named_buffers(remove_duplicate=False))
    for k in patch_bufs:
        assert torch.equal(buffers[k].cpu().to(ckpt[k].dtype), ckpt[k].cpu()), k  # the trace stores them in its dtype
    for k in set(ckpt) & set(off_sd):
        assert off_sd[k].dtype == torch.float32 and torch.equal(off_sd[k], ckpt[k].float()), k
    ours = ref_cosmos.build(weights=COSMOS, device="cpu", dtype=torch.float32)
    rng = np.random.default_rng(SEED)
    frames = rng.integers(0, 256, size=(121, 270, 480, 3), dtype=np.uint8)
    video, sel = extract.cosmos_input(frames)
    assert video.shape == (1, 3, 121, 320, 320) and len(sel) == 121
    with torch.no_grad():
        a = ref_cosmos.encode(ours, video).reshape(16, 40, 40)
        latent = official.encode(video)[0]
        b = official.post_quant_conv(latent).mean(dim=2)[0]
    diff = float((a - b).abs().max())
    print(f"Cosmos: max |diff| = {diff:.3e}; |rep| max {float(b.abs().max()):.3f}")
    assert a.shape == b.shape == (16, 40, 40) and diff <= TOL
