"""CODELOCK_CORRECTION_001 tests (CC_TASK_SS_step3_adapter_fix_v2.md §4; criteria fixed by the task). Run in the
extraction environment; uses the verified weight files on LaCie (skipped if they are absent):

    /home/user/.venvs/ss_extract/bin/python -m pytest -p no:cacheprovider tests/test_codelock_correction_001.py

1. SurgeNetCholec / SurgeNetRARP: the corrected adapter reproduces the official CAFormer-S18 / ReLU architecture
   (official metaformer.py, TimJaspers0801/SurgeNet @ 54831cfa): identical parameter names and shapes (head excluded),
   ReLU activations; strict load: zero unexpected and zero missing trainable keys; the official implementation loads the
   file under its documented configuration (load_pretrained_weights: head.* removed, strict=False) with no unexpected
   key and only head.* missing; equivalence adapter vs official, same weights, float32, input seed 99990002
   normalised as the adapter specifies: max |difference| of the representation ≤ 1e-4.
2. SelfSupSurg ResNet-50 DINO: adapter vs the official VISSL ResNeXt trunk (vissl @ 09270ed2,
   vissl/models/trunks/resnext.py + model_helpers.py; trunk config from the SelfSupSurg configs and vissl defaults),
   checkpoint trunk loaded strictly into the official trunk; same criterion.
3. LeanVAE-4ch: adapter vs the official LeanVAE.load_from_checkpoint + LeanVAE.encode with the official inference
   normalisation (leanvae_inference.py, regular_size 2); representation rule (mean over latent time, flatten) applied
   to the official latent; same criterion.
Infrastructure imports of the official code that do not define the network (VISSL registry / config / distributed
helpers; LeanVAE's LPIPS, data loader and Lightning engine) are stubbed or bypassed; every model-definition line runs
unmodified.
"""
import contextlib
import importlib.util
import io
import os
import sys
import types
from unittest import mock

import numpy as np
import pytest
import torch

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", DIFFUSERS_OFFLINE="1")

W = "/media/user/LaCie/medvideo_gate/weights"
SEED = 99990002
TOL = 1e-4
SURGENET = {"SurgeNetCholec": f"{W}/surgenet/CHOLEC_checkpoint_epoch0050_teacher.pth",
            "SurgeNetRARP": f"{W}/surgenet/RARP_checkpoint_epoch0050_teacher.pth"}
DINO = f"{W}/selfsupsurg/model_final_checkpoint_dino_surg.torch"
LEAN4 = f"{W}/leanvae/LeanVAE-dim4.ckpt"
IMNET_MEAN = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
IMNET_STD = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)


def need(path):
    if not os.path.exists(path):
        pytest.skip(f"weight file not present: {path}")


def frame_input():
    return torch.rand((1, 3, 224, 224), generator=torch.Generator().manual_seed(SEED)) * 255


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------------------------------------------------
# 1. SurgeNet
# ---------------------------------------------------------------------------------------------------------------------
def official_surgenet(path):
    off = load_module("surgenet_official_for_test", os.path.join(REPO, "third_party", "SurgeNet", "metaformer.py"))
    with contextlib.redirect_stdout(io.StringIO()):
        model = off.caformer_s18(num_classes=0, pretrained="SurgeNet", pretrained_weights=None)
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    out = io.StringIO()
    with mock.patch.object(torch.hub, "load_state_dict_from_url", lambda url, *a, **k: dict(ckpt)), \
            contextlib.redirect_stdout(out):
        model.load_pretrained_weights("local-verified-file")            # the official loading method
    return model.eval(), ckpt, out.getvalue()


@pytest.mark.parametrize("key", list(SURGENET))
def test_surgenet_architecture_strict_load_and_equivalence(key):
    from ss_benchmark.models import prim_caformer
    path = SURGENET[key]
    need(path)
    official, ckpt, msg = official_surgenet(path)
    off_sd = official.state_dict()
    # the official implementation loads the file under its documented configuration
    assert not (set(ckpt) - set(off_sd)), "official: unexpected keys"
    assert all(k.startswith("head.") for k in set(off_sd) - set(ckpt)), "official: missing non-head keys"
    assert "Check if weights are loaded successfully" in msg
    # architecture: identical names and shapes (head excluded), ReLU activations
    ours = prim_caformer.build(weights=None)
    our_sd = ours.state_dict()
    off_backbone = {k: v.shape for k, v in off_sd.items() if not k.startswith("head.")}
    assert {k: v.shape for k, v in our_sd.items()} == off_backbone
    acts = {type(m).__name__ for n, m in ours.named_modules() if n.endswith(("token_mixer.act1", "mlp.act"))}
    assert acts == {"ReLU"}
    # strict load: zero unexpected, zero missing trainable keys
    ours = prim_caformer.build(weights=path)
    res = ours.load_state_dict(torch.load(path, map_location="cpu", weights_only=True), strict=True)
    assert not res.missing_keys and not res.unexpected_keys
    # equivalence, float32, seed 99990002
    x = frame_input()
    with torch.no_grad():
        a = prim_caformer.encode(ours, x)
        b = official.forward_features((x / 255.0 - IMNET_MEAN) / IMNET_STD)[0]
    diff = float((a - b).abs().max())
    print(f"{key}: max |diff| = {diff:.3e}")
    assert a.shape == b.shape == (1, 512) and diff <= TOL


# ---------------------------------------------------------------------------------------------------------------------
# 2. SelfSupSurg ResNet-50 DINO vs VISSL ResNeXt
# ---------------------------------------------------------------------------------------------------------------------
class AttrDict(dict):
    def __getattr__(self, k):
        v = self[k]
        return AttrDict(v) if isinstance(v, dict) else v


def official_vissl_trunk():
    stubs = {
        "vissl": types.ModuleType("vissl"), "vissl.config": types.ModuleType("vissl.config"),
        "vissl.data": types.ModuleType("vissl.data"), "vissl.data.collators": types.ModuleType("vissl.data.collators"),
        "vissl.data.collators.collator_helper": types.ModuleType("vissl.data.collators.collator_helper"),
        "vissl.models": types.ModuleType("vissl.models"), "vissl.models.trunks": types.ModuleType("vissl.models.trunks"),
        "vissl.utils": types.ModuleType("vissl.utils"),
        "vissl.utils.activation_checkpointing": types.ModuleType("vissl.utils.activation_checkpointing"),
        "vissl.utils.env": types.ModuleType("vissl.utils.env"), "vissl.utils.misc": types.ModuleType("vissl.utils.misc")}
    stubs["vissl.config"].AttrDict = AttrDict
    stubs["vissl.data.collators.collator_helper"].MultiDimensionalTensor = type("MultiDimensionalTensor", (), {})
    stubs["vissl.models.trunks"].register_model_trunk = lambda name: (lambda cls: cls)
    stubs["vissl.utils.activation_checkpointing"].checkpoint_trunk = None
    stubs["vissl.utils.env"].get_machine_local_and_dist_rank = lambda: (0, 0)
    stubs["vissl.utils.misc"].is_apex_available = lambda: False
    with mock.patch.dict(sys.modules, stubs):
        load_module("vissl.models.model_helpers", os.path.join(REPO, "third_party", "vissl_src", "model_helpers.py"))
        rx = load_module("vissl.models.trunks.resnext", os.path.join(REPO, "third_party", "vissl_src", "resnext.py"))
    cfg = AttrDict(INPUT_TYPE="rgb", TRUNK=dict(RESNETS=dict(
        DEPTH=50, WIDTH_MULTIPLIER=1, NORM="BatchNorm", GROUPNORM_GROUPS=32, STANDARDIZE_CONVOLUTIONS=False, GROUPS=1,
        ZERO_INIT_RESIDUAL=False, WIDTH_PER_GROUP=64, LAYER4_STRIDE=2)),
        ACTIVATION_CHECKPOINTING=dict(USE_ACTIVATION_CHECKPOINTING=False, NUM_ACTIVATION_CHECKPOINTING_SPLITS=2))
    return rx.ResNeXt(cfg, "resnet")


def test_selfsupsurg_dino_vs_official_vissl_trunk():
    from ss_benchmark.models import prim_resnet50
    need(DINO)
    trunk = official_vissl_trunk()
    ckpt = torch.load(DINO, map_location="cpu", weights_only=False)
    trunk_sd = ckpt["classy_state_dict"]["base_model"]["model"]["trunk"]
    res = trunk.load_state_dict(trunk_sd, strict=True)
    assert not res.missing_keys and not res.unexpected_keys
    trunk.eval()
    ours = prim_resnet50.build(weights=DINO)
    x = frame_input()
    with torch.no_grad():
        a = prim_resnet50.encode(ours, x)
        # official API: named output keys (feat_eval_mapping); "flatten" = the trunk's final avgpool -> flatten output
        b = trunk((x / 255.0 - IMNET_MEAN) / IMNET_STD, out_feat_keys=["flatten"])[0]
    diff = float((a - b).abs().max())
    print(f"SelfSupSurg DINO: max |diff| = {diff:.3e}")
    assert a.shape == b.shape == (1, 2048) and diff <= TOL


# ---------------------------------------------------------------------------------------------------------------------
# 3. LeanVAE-4ch vs official LeanVAE.load_from_checkpoint / encode
# ---------------------------------------------------------------------------------------------------------------------
def official_leanvae_class():
    root = os.path.join(REPO, "third_party", "LeanVAE", "LeanVAE")
    name = "leanvae_official_for_test"
    pkgs = {}
    for sub in ("", ".utils", ".models", ".modules"):
        m = types.ModuleType(name + sub)
        m.__path__ = [os.path.join(root, sub.strip(".").replace(".", os.sep))] if sub else [root]
        pkgs[name + sub] = m
    sys.modules.update(pkgs)
    if importlib.util.find_spec("beartype") is None:                    # unused import in backbones.py
        bt = types.ModuleType("beartype"); bt.beartype = lambda f: f
        sys.modules["beartype"] = bt
    bb = importlib.import_module(name + ".modules.backbones")
    vae = importlib.import_module(name + ".modules.vae")
    mods = pkgs[name + ".modules"]
    for k in dir(bb):
        if not k.startswith("_"):
            setattr(mods, k, getattr(bb, k))
    mods.DiagonalGaussianDistribution = vae.DiagonalGaussianDistribution
    return importlib.import_module(name + ".models.autoencoder").LeanVAE


def test_leanvae_4ch_vs_official():
    from ss_benchmark.models import sec_leanvae
    need(LEAN4)
    LeanVAE = official_leanvae_class()
    with contextlib.redirect_stdout(io.StringIO()):
        official = LeanVAE.load_from_checkpoint(LEAN4, strict=False).eval()     # official loader (inference script)
    ckpt = torch.load(LEAN4, map_location="cpu", weights_only=False)
    off_sd = official.state_dict()
    assert not (set(ckpt["state_dict"]) - set(off_sd)) and not (set(off_sd) - set(ckpt["state_dict"]))
    ours = sec_leanvae.build(weights=LEAN4, variant="4ch")
    x = torch.rand((1, 17, 3, 256, 256), generator=torch.Generator().manual_seed(SEED)) * 255
    video = x.permute(0, 2, 1, 3, 4)                                        # official layout (b, c, t, h, w)
    regular_size = 2
    with torch.no_grad():
        a = sec_leanvae.encode(ours, x)
        z = official.encode(video / (127.5 * regular_size) - (1.0 / regular_size))
        b = z.mean(dim=2).flatten(1)
    diff = float((a - b).abs().max())
    print(f"LeanVAE-4ch: max |diff| = {diff:.3e}")
    assert a.shape == b.shape == (1, 4096) and diff <= TOL
