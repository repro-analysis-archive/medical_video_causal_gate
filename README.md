# medical_video_causal_gate

**SS-DS203 main analysis: protocol, locked code and run records.** Main analysis repository of the SS-DS203 semi-synthetic evaluation: the frozen protocol, the locked analysis code, the code-lock gate, model selection, and the runners and records of protocol steps 4–7.

Part of the code and records of the manuscript *Semi-synthetic evaluation of site information and linear erasure in clinical video representations for sequentially doubly robust causal effect estimation* (Nakano H, Shiinoki T; article DOI: [TO FILL]). The six repositories of this release are archived together, as git bundles at tag `v1.0.0-submission`, on Zenodo: https://doi.org/10.5281/zenodo.23934337.

Repositories of this release:

* [`medical_video_causal_gate`](https://github.com/repro-analysis-archive/medical_video_causal_gate)
* [`ss_exploratory`](https://github.com/repro-analysis-archive/ss_exploratory)
* [`ss_exploratory_B`](https://github.com/repro-analysis-archive/ss_exploratory_B)
* [`step7_prep`](https://github.com/repro-analysis-archive/step7_prep)
* [`jbi_figures_tables`](https://github.com/repro-analysis-archive/jbi_figures_tables)
* [`ss-ds203-records`](https://github.com/repro-analysis-archive/ss-ds203-records)

Release: tag `v1.0.0-submission` (2026-11-04).

## Contents

`docs/` (the protocol `SS_PROTOCOL_DS203.md`, code-lock specifications, gate amendments, `protocol_history/`), `decisions/` (freeze record, code-lock records, model selection, runner and operations records), `ss_benchmark/` (the locked analysis package, with the `models/` adapters), `scripts/` (runners; `fetch_third_party.sh`), `tests/`, `results/` (code-lock gate, step-4 to step-7 records), `checks/` (role-switch and R2Z diagnostics), `errata/`, `env/`, `data_audit/` (dataset download and container facts, window design, case-level offsets, foundation-model candidate survey), `lit/` (literature search records and screening).

## Commit identifiers cited in the manuscript (Supplementary Methods) and records

Each identifier can be checked with `git show <ID>` in a clone of this repository.

| meaning | original ID (cited in the Supplementary Methods / records) | ID in this repository |
|---|---|---|
| protocol freeze | `4c86dc5` (`4c86dc5f7df357a09311198f34e141972fe0175a`) | `2661846c5757c2cc351037d75549861d3966c2ba` |
| freeze record | `8f63e43` (`8f63e4390a36ed6585f74d70b05e841976f94ce5`) | `52ec937fb19386f9caa507a51cd29944af68e7ae` |
| SDR implementation | `af56777` (`af56777e0f52b5c350dd7ba557d55b2394cbd4bf`) | `62d355748a8f0c865a559f16aac94cf0925bc08c` |
| final code lock | `98cba1e` (`98cba1e9907c99377890b47b2078f0b6c4270e79`) | `6e3f2fd806690009b9a788432066dfd872ea03a0` |
| model selection (superseded) | `cb78391` (`cb783913a1ab0175bda2cef2a62fd78040bf7ffd`) | `01542f49a730d7fec1d87a6987bfa8175b90fe08` |
| post-lock correction CODELOCK_CORRECTION_001 | `ad8833a` (`ad8833a53b9a41b1f20dd96f9410f80d9b7ab5d3`) | `c487e0c85c1f89aa98fb50e2ee5c22cdde8f0086` |
| model reselection | `ba73820` (`ba73820c1303f723da7dba8f49f432962d3a37a1`) | `8c12b5213042b7d0e499ac61d07cce5dbaf7eb66` |
| steps 4–5 runner | `9e1aa71` (`9e1aa715af3067a912bb69733ab79df106877b53`) | `1ed8f0533db23eb07e932372f6b79d145388e38d` |
| step-4 record | `8d4c61a` (`8d4c61a0163e836c5df363166e4b1aee4352c174`) | `200f13679305160452304fd781ae7a7db1dda585` |
| step-5 record | `0ebf2cf` (`0ebf2cf632d752cdf5136473a3b6e368c0e5094c`) | `6fbac3c83e0b647ce6ad28668dc7ee8f68ba4cde` |
| §13 record | `0667430` (`066743094ebc0d74b283fee4b6fb4afd282709ba`) | `db1a1930d3376131fcc24828eb18eda70bb8d47c` |
| step-6 runner | `7adaf13` (`7adaf133f8eaac9cf790d5320c2dd4b48d0b05cc`) | `e5759effe5ad12f30ce09ee7f25410c6037dc493` |
| step-7 record | `2880d73` (`2880d736c75fbaaed8abbce233e82229b65e4c2f`) | `f72a7db3e40463c12adc573b5f40c95e379f17d6` |
| video container facts | `2012acd` (`2012acdb8fdecce12e5bc7c62af633a716511eec`) | `698643e2fb62e927d8014b63406e7c24d68c62aa` |
| window offsets per W | `adf9160` (`adf916023a8cc2da04e4cb12cc896719a0e60314`) | `1af70709e5b6d2b186afd828a5435e40a1c208a2` |
| per-W G-SITE record | `b987010` (`b9870103eb3644cfd1a7fb4fca4861c74af10a7e`) | `3d8c8cb31131d8e72edb9a97866c46c711db7993` |
| model facts | `d3563e7` (`d3563e703ae15241970e99c37a82c7c26697e800`) | `b4d34be01f4795281fa0037f843b30bc91a030d4` |
| download completeness | `dba9c06` (`dba9c068b753e67a135061e0059e07f1caf87da6`) | `b08f999d0bfdc4c3ebb15217b1a8e2f04a6b90d6` |
| window rule | `dbd5984` (`dbd598441f039d6235443bc396faeae5326b2f08`) | `53e208e33f6685f9b2e7e36d0b5dcd8b38ed6dac` |
| step-7 runner (task table; not in SM v4) | `80998c1` (`80998c127a887202794645c91ece4cb624d5b555`) | `ac642b70d1eebaac2af7cf7e49535bd034c13b21` |

## History filtering and commit identifiers

This repository is a filtered copy of the original history (`git filter-repo`): all third-party material (fetched papers and their extracted text, copies of third-party READMEs / documentation / code / configuration / licences, raw API responses and saved web pages, and 22 screening input batches consisting of fetched abstracts — 1,636 paths) was removed from the whole history (decision D9). 67 commits → 67; the 13 oldest keep their IDs, all later IDs change, including all 19 identifiers cited in the Supplementary Methods (table above). The frozen protocol `docs/SS_PROTOCOL_DS203.md` is identified by its content hash, SHA-256 `cd7e14026c6ace5b2e2e6987c9e73421401cc6b168b3d25830d116b12d748926`, equal at the original freeze commit and at the mapped public commit. Commit messages and dates are unchanged, so messages still name original IDs.

* `COMMIT_ID_MAP.md` — original → public ID of every commit;
* `removed_paths.txt` — the exact paths removed from the whole history;
* `FILTER_RECORD.md` — tool, command and the checks performed when the copy was built (2026-10-28).

The unfiltered original history is not distributed (it contains the removed third-party material). It is kept by the authors as a git bundle (SHA-256 `5072e7bb9e92c5a8760dcb896c79e26b55ccc04b44dafe61ca90b699a1f87f83`) so that the original identifiers can be verified; requests to the corresponding author.

## Not included

* video files and per-frame representations of Appendix300 (representations can be regenerated from the public data with the released code)
* video frames and staged video archives
* step-6 / X unit shards and X1 features (their SHA-256 lists are in the records)
* model weights and checkpoints, and upstream source code (see *Upstream models and licences*)
* third-party material removed from the whole history (see *History filtering*); the authors' audit notes, scripts and derived tables are kept — derived files quote third-party text only in quotations of ≤ 150 words with their source

Case-level derived data (the case list, per-case window offsets, per-file probes and the per-case file lists of the step-4 record) are published as they are: Appendix300 is CC BY 4.0 and the case IDs are the dataset's own identifiers.

Scripts and records contain absolute paths of the machines on which the analysis ran (for example `/home/user/…`, `/srv/…`, `/media/user/LaCie/…`, `/Volumes/ADDATA/…`). They are recorded as they were; adapt them to re-run.

## Upstream models and licences

The eight model adapters in `ss_benchmark/models/` are **the authors' original code** (MIT). They contain **no upstream source file, configuration file or weight file**: upstream code is obtained by the user from the upstream repositories at the pinned commits (secondary models and VideoMAE: `scripts/fetch_third_party.sh` in `medical_video_causal_gate`; SurgeNet `metaformer.py`: `decisions/CODELOCK_CORRECTION_001_SURGENET_ADAPTER.md` there) and weights are loaded from local paths under the upstream licences. What the adapters do contain is **upstream material quoted for provenance** (short verbatim quotations, each with its source, in `SPEC["sources"]` and the docstrings), two upstream configuration dictionaries (`sec_larp.py` `CONFIG`, `sec_wfvae.py` `CONFIG`) and one function adapted from Hugging Face transformers (`sec_videomae.py`). **This upstream material is not licensed under MIT**; it remains under the upstream licences below and is reproduced with attribution for non-commercial research use. Each adapter starts with a comment header stating this.

| adapter | upstream model | upstream code (pinned) — licence | weights / configuration — licence | paper |
|---|---|---|---|---|
| `ss_benchmark/models/prim_caformer.py` | SurgeNetCholec / SurgeNetRARP (CAFormer-S18) | [TimJaspers0801/SurgeNet](https://github.com/TimJaspers0801/SurgeNet) @ `54831cfa` — MIT (© 2025 Cris Claessens) | [TimJaspersTue/SurgeNetModels](https://huggingface.co/TimJaspersTue/SurgeNetModels) @ `cc21f4a1` — CC BY-NC 4.0 (HF card); the GitHub `LICENSE_MODELS.txt` states CC BY-NC-SA 4.0 | Jaspers et al., Med Image Anal 2026;108:103873, doi:10.1016/j.media.2025.103873 |
| `ss_benchmark/models/prim_resnet50.py` | SelfSupSurg ResNet-50 (MoCo v2 / SimCLR / SwAV / DINO) | [CAMMA-public/SelfSupSurg](https://github.com/CAMMA-public/SelfSupSurg) (`main` @ `8a03d289`) — CC BY-NC-SA 4.0 | same — CC BY-NC-SA 4.0 (code, models and datasets); architecture: torchvision ResNet-50 | Ramesh et al., Med Image Anal 2023;102844 |
| `ss_benchmark/models/ref_cosmos.py` | NVIDIA Cosmos-1.0-Tokenizer-CV8x8x8 (reference) | [NVIDIA/Cosmos-Tokenizer](https://github.com/NVIDIA/Cosmos-Tokenizer) @ `3584ae75` — Apache-2.0 (equivalence check only); quoted: [gpi-pack/gpi_pack](https://github.com/gpi-pack/gpi_pack) @ `8836037d` — MIT (© 2025 Kentaro Nakamura) | [nvidia/Cosmos-1.0-Tokenizer-CV8x8x8](https://huggingface.co/nvidia/Cosmos-1.0-Tokenizer-CV8x8x8) @ `5110dbb3` — NVIDIA Open Model License (gated) | arXiv:2501.03575 |
| `ss_benchmark/models/sec_larp.py` | LARP-L-Long tokenizer | [hywang66/LARP](https://github.com/hywang66/LARP) @ `8aaed633` — MIT (© 2024 Hanyu Wang) | [hywang66/LARP-L-long-tokenizer](https://huggingface.co/hywang66/LARP-L-long-tokenizer) @ `c93a7e2d` — no licence declared | arXiv:2410.21264 |
| `ss_benchmark/models/sec_leanvae.py` | LeanVAE (16ch / 4ch) | [westlake-repl/LeanVAE](https://github.com/westlake-repl/LeanVAE) @ `62f7c7d5` — MIT (© 2025 westlake-repl) | [Yumic/LeanVAE](https://huggingface.co/Yumic/LeanVAE) @ `4585e461` — MIT | arXiv:2503.14325 |
| `ss_benchmark/models/sec_omnitokenizer.py` | OmniTokenizer (ImageNet + K600, VQVAE / VAE) | [FoundationVision/OmniTokenizer](https://github.com/FoundationVision/OmniTokenizer) @ `701b6190` — MIT (© 2024 FoundationVision) | [Daniel0724/OmniTokenizer](https://huggingface.co/Daniel0724/OmniTokenizer) @ `9ebde216` — no licence declared | arXiv:2406.09399 |
| `ss_benchmark/models/sec_videomae.py` | VideoMAE pre-training checkpoints | [MCG-NJU/VideoMAE](https://github.com/MCG-NJU/VideoMAE) @ `14ef8d85` — CC BY-NC 4.0; adapted code from [huggingface/transformers](https://github.com/huggingface/transformers) v4.46.3 — Apache-2.0 | official checkpoints of `MODEL_ZOO.md` — CC BY-NC 4.0 (repository licence) | arXiv:2203.12602 |
| `ss_benchmark/models/sec_wfvae.py` | WF-VAE-L 16ch | [PKU-YuanGroup/WF-VAE](https://github.com/PKU-YuanGroup/WF-VAE) @ `d858bee8` — Apache-2.0 | [chestnutlzj/WF-VAE-L-16Chn](https://huggingface.co/chestnutlzj/WF-VAE-L-16Chn) @ `8c0aa9ce` — Apache-2.0 | arXiv:2411.17459 |

* **Apache-2.0 material:** `sec_videomae.py` (`_rename_key` and the `qkv` split of `convert_original`, adapted from transformers v4.46.3 `convert_videomae_to_pytorch.py`, Copyright 2022 The HuggingFace Inc. team; modified: encoder rules only) and `sec_wfvae.py` (`CONFIG` = the released `config.json`, private keys `_class_name` / `_diffusers_version` dropped). Licence text: `LICENSES/Apache-2.0.txt`. Neither upstream project ships a NOTICE file at the pinned revision.
* **Non-commercial licences:** quotations from VideoMAE (CC BY-NC 4.0) and SelfSupSurg (CC BY-NC-SA 4.0) are verbatim excerpts shared for non-commercial research with attribution; the corresponding weights are licensed for non-commercial use only.
* **Built on NVIDIA Cosmos.** The Cosmos tokenizer weights are licensed by NVIDIA Corporation under the NVIDIA Open Model License; they are not included here and must be obtained (and the licence accepted) from Hugging Face.
* Full notices: `NOTICE`, `THIRD_PARTY_NOTICES.md`, `LICENSES/` (upstream licence texts as fetched from the pinned revisions on 2026-11-04).

## Data source and attribution

The video data are Appendix300 (CC BY 4.0), used with attribution (manuscript references 1 and 45):

* Kolbinger FR, Kirchner M, Pfeiffer K, Bodenstedt S, Jenke AC, Barthel J, et al. Appendix300: Surgical video and patient metadata of 330 laparoscopic appendectomy cases from five institutions [dataset]. Technische Universität Dresden, OPARA; 2026-04-29. doi:10.25532/OPARA-1173. License: CC BY 4.0.
* Kolbinger FR, Kirchner M, Pfeiffer K, Bodenstedt S, Jenke AC, Barthel J, et al. Appendix300: Surgical video and patient metadata of 330 laparoscopic appendectomy cases from five institutions. Sci Data. 2026;13:886. doi:10.1038/s41597-026-07593-6.

No video file, video frame or per-frame representation is redistributed here.

## Licence

* **Original code** (`ss_benchmark/`, `scripts/`, `tests/`, `checks/**/*.py`, `data_audit/**/*.py`, `lit/*.py`): MIT License — see `LICENSE`. Copyright (c) 2026 Hisashi Nakano.
* **Records, results and figure data** (the protocol, decision and run records, results, audits and literature records): Creative Commons Attribution 4.0 International (CC BY 4.0) — see `LICENSE-CC-BY-4.0`.
* **Not covered by either licence:** third-party material quoted or embedded in this repository remains under its own terms (quotations in derived audit records; the upstream material in the model adapters — see *Upstream models and licences*, `NOTICE`, `THIRD_PARTY_NOTICES.md`).

## How to cite

Please cite the article (DOI: [TO FILL]) and the Zenodo archive https://doi.org/10.5281/zenodo.23934337; machine-readable metadata: `CITATION.cff`.

## Use of AI tools

Most commits carry a `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` line: code and records were produced with Claude Code under the investigator's instructions, as declared in the manuscript. Automated record commits made by the runners carry no such line. The lines are kept unchanged.

## Authors and contact

* Hisashi Nakano (ORCID [0000-0002-9023-880X](https://orcid.org/0000-0002-9023-880X)), Department of Health Data Science, Niigata University of Health and Welfare — hisashi-nakano@nuhw.ac.jp (corresponding)
* Takehiro Shiinoki (ORCID [0000-0002-0246-8489](https://orcid.org/0000-0002-0246-8489)), Department of Radiation Oncology, Yamaguchi University
