"""Code-lock checkpoint-coverage test (CC_TASK_SS_code_lock_coverage_fix.md item 3 and its addendum item 2).
Criterion fixed before the first run; run in the extraction environment:

    /home/user/.venvs/ss_extract/bin/python -m pytest -p no:cacheprovider tests/test_codelock_coverage.py

From the eligibility facts in force (d3563e7, out/ss_eligibility_v04.json) and docs/codelock_checkpoint_manifest.json:
every checkpoint of every eligible candidate that the §4.1.4 rules could select (ignoring the post-freeze memory and
throughput tests) must have exactly one adapter / registry entry and one extraction-spec entry, build with random
weights and return the documented representation dimension on synthetic input; every adapter checkpoint must appear
in the manifest; no checkpoint identifier or alias may be ambiguous. Fails if any reachable checkpoint lacks an
adapter. Seeds: torch / numpy 0 (random initialisation); no weights, no DS203 data.
"""
import json
import os
import sys

import numpy as np
import pytest
import torch

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", DIFFUSERS_OFFLINE="1")

from ss_benchmark import feasibility  # noqa: E402

FACTS = json.load(open(os.path.join(REPO, "data_audit", "lead", "out", "ss_eligibility_v04.json")))
MAN = json.load(open(os.path.join(REPO, "docs", "codelock_checkpoint_manifest.json")))
SPEC = json.load(open(os.path.join(REPO, "docs", "codelock_extraction_spec.json")))
CLASS_LINE = ("VideoMAE eligibility applies to official pre-training checkpoints of the masked-autoencoder model; "
              "supervised fine-tuned classification/action-recognition checkpoints are outside the secondary "
              "reconstructive/generative class.")
SELECTABLE = MAN["selectable"]


def test_manifest_covers_every_eligible_candidate():
    eligible = FACTS["eligible_primary"] + FACTS["eligible_secondary"]
    assert MAN["eligible_candidates"]["primary"] == FACTS["eligible_primary"]
    assert MAN["eligible_candidates"]["secondary"] == FACTS["eligible_secondary"]
    assert {r["candidate"] for r in SELECTABLE} == set(eligible)
    assert all(r["ranking_reachable"] is True and r["excluded_reason"] is None for r in SELECTABLE)


def test_one_adapter_and_one_spec_entry_per_reachable_checkpoint():
    keys = [r["registry_key"] for r in SELECTABLE]
    assert len(keys) == len(set(keys)), "a registry entry serves more than one reachable checkpoint"
    for r in SELECTABLE:
        assert r["registry_key"] in feasibility.REGISTRY, r["checkpoint_id"]
        assert r["registry_key"] in SPEC["models"], r["checkpoint_id"]
        assert SPEC["models"][r["registry_key"]]["representation_dim"] == r["representation_dim"]


def test_every_adapter_checkpoint_is_in_the_manifest():
    in_manifest = {r["registry_key"] for r in SELECTABLE} | {MAN["reference"]["registry_key"]}
    assert set(feasibility.REGISTRY) == in_manifest
    assert set(SPEC["models"]) == in_manifest


def test_no_ambiguous_identifier_or_alias():
    ids = [r["checkpoint_id"] for r in SELECTABLE]
    aliases = [a.split(" (")[0] for r in SELECTABLE for a in r["aliases"]]
    others = [r["checkpoint_id"] for r in MAN["excluded"]] + [r["file"] for r in MAN["out_of_candidate"]]
    names = ids + aliases + others + [MAN["reference"]["checkpoint_id"]]
    assert len(names) == len(set(names)), "duplicate identifier or alias"
    assert all(r["excluded_reason"] for r in MAN["excluded"]) and all(r["reason"] for r in MAN["out_of_candidate"])


def test_videomae_class_line_verbatim():
    assert MAN["videomae_class_line"] == CLASS_LINE and SPEC["videomae_class_line"] == CLASS_LINE
    for r in SELECTABLE:
        if r["candidate"].startswith("VideoMAE"):
            assert CLASS_LINE in r["class_eligibility"] and r["stage"].startswith("pre-train")
            assert SPEC["models"][r["registry_key"]]["class_line"] == CLASS_LINE
    assert all(CLASS_LINE in r["excluded_reason"] for r in MAN["excluded"] if r["candidate"].startswith("VideoMAE"))


@pytest.mark.parametrize("row", SELECTABLE, ids=[r["registry_key"] for r in SELECTABLE])
def test_reachable_checkpoint_builds_and_returns_documented_shape(row):
    mod, kw = feasibility.adapter(row["registry_key"])
    torch.manual_seed(0)
    np.random.seed(0)
    dev, dtype = ("cuda", torch.bfloat16) if torch.cuda.is_available() else ("cpu", torch.float32)
    model = mod.build(weights=None, device=dev, dtype=dtype, **kw)
    x = feasibility.synthetic_input(mod.SPEC, 1, torch.Generator().manual_seed(0)).to(dev)
    with torch.inference_mode():
        out = mod.encode(model, x)
    assert tuple(out.shape) == (1, row["representation_dim"]) and torch.isfinite(out.float()).all()
    del model
    if dev == "cuda":
        torch.cuda.empty_cache()
