# SS protocol DS203: code-lock implementation notes

* **Protocol:** `docs/SS_PROTOCOL_DS203.md`, frozen at 4c86dc5 (unchanged).
* **Task:** `CC_TASK_SS_code_lock_v2.md`, Part A. The protocol governs wherever the two differ.
* **What this file records:** where each protocol section is implemented, the implementation choices the protocol text does not fix, and the differences that are reported but not acted on.

## 1. Where things are

| protocol | module |
|---|---|
| §2 folds, case sets, §7.2 window design (real and PLACEHOLDER) | `ss_benchmark/design.py` |
| §3 preprocessing (2-fps grid, crop, resize, mask, mask check, near-uniform flag, native arm, decoding) | `ss_benchmark/preprocess.py` |
| §4.2 extraction (frame pooling, clip windows, Cosmos reference path) | `ss_benchmark/extract.py`; step-4 orchestration `ss_benchmark/pipeline.py` |
| §4.1.5 eligible models and the reference | `ss_benchmark/models/` (random initialisation at code lock), `ss_benchmark/feasibility.py` (registry; §4.1.4 rule-4 test; §10.4 extraction projection) |
| §4.2–4.3 PCA (64) and LEACE | `ss_benchmark/reduce.py` |
| §5 E1, E2, E3, MLP probe, bootstrap; §5.4 G-SITE | `ss_benchmark/checks.py`; step-5 orchestration `ss_benchmark/pipeline.py` |
| reporting-only paths, all wired into `pipeline.run_checks` / `pipeline.near_uniform`: pre-removal MLP site probe (§4.3), E2 on all 278 videos, E2 with past actions, normalised-time reference (§5.2), near-uniform summary (§3.1 step 4) | `ss_benchmark/checks.py` |
| §11 small-truth flag "at code lock" (truth only, real centre + offset) | `ss_benchmark/dgp.py` `small_truth_check`; runner stage (c2) |
| frozen per-model extraction specification | `docs/CODELOCK_EXTRACTION_SPEC.md`, `docs/codelock_extraction_spec.json` |
| §6–7 DGP and truth | `ss_benchmark/dgp.py` |
| §8 arms | `ss_benchmark/arms.py` |
| §9 SDR estimator and nuisance learners | `ss_benchmark/sdr.py`, `ss_benchmark/learners.py` |
| §10–12 grid, seeds, families, aggregation | `ss_benchmark/grid.py`, `ss_benchmark/seeds.py`, `ss_benchmark/grid_driver.py` |
| §14 step 2: estimator gate, compute projection, G-SITE record | `ss_benchmark/codelock_gate.py`, `scripts/run_codelock_gate.sh` |
| §14 step 2: dry run on PLACEHOLDER features | `ss_benchmark/dryrun.py`; also the projection stage, which runs every arm on PLACEHOLDER features |
| fast tests (task A2) | `tests/test_codelock_fast.py` |
| reporting-path and small-truth tests | `tests/test_codelock_reporting.py` |
| extra engineering checks, including extraction-spec consistency | `tests/test_codelock_extra.py` (run in the extraction venv) |

**Environments:**
* Causal code: `/home/user/miniconda3/bin/python3`.
* Extraction: `/home/user/.venvs/ss_extract`, which uses the base torch; package list in `env/ss_extract_requirements.txt`.
* Secondary-model code: the pinned commits fetched by `scripts/fetch_third_party.sh` into the git-ignored `third_party/`.

## 2. Implementation choices the protocol does not fix

**General choices.** The `IMPLEMENTATION_NOTES` in `ss_benchmark/constants.py` define N1–N12; they are summarised here:
* **N1 (MLP depth).** "2-layer MLP" means two linear layers with one ReLU hidden layer: 128 units for the nuisances, 256 for the probe.
* **N2 (MLP training).**
  * Mini-batch min(200, n).
  * Weight decay added to the gradient (torch Adam semantics).
  * PyTorch default initialisation.
  * Early stopping on the inner-validation loss, with the best epoch restored.
* **N3 (density-ratio penalty grid).** The L2-logistic density-ratio penalty grid is the §9 ridge grid {1e-3..1e3}.
* **N4 (learner choice).** Each learner is a procedure, scored by 5-fold group cross-validation inside the training fold. Ties go to the linear learner.
* **N5 (penalty conventions).** scikit-learn conventions on z-scored features.
* **N6 (SDR).** The Díaz et al. (2021) SDR recursion:
  * classification density ratios, r = exp(logit), with no trimming;
  * IF = V₀ − Y;
  * Wald interval.
* **N7 (cross-fitting).** The fixed §2 folds of the analysis set, with in-sample training-fold pseudo-outcomes.
* **N8 (seeds).** Named seed streams are SeedSequence children with spawn key `int.from_bytes(name)`, for example "c-permutation".
* **N9 (linear site probe).** Multinomial L2 logistic using the E2 learner settings.
* **N10 (bound percentiles).**
  * E1 lower bound: 2.5th percentile.
  * E3-site upper bound: 95th percentile (one-sided, as stated).
  * E2 CI: 2.5th / 97.5th percentiles.
* **N11 (secondary representations).**
  * KL-VAEs: the posterior mean.
  * VQ tokenizers: the codebook-lookup input (L2-normalised).
  * Both are averaged over latent time and flattened.
  * VideoMAE: the token-mean of the last hidden states.
* **N12 (reduction b).** Reduction (b), "ridge only", is applied as linear learners only: ridge plus L2-logistic density ratios.

**PCA and LEACE are fitted per fold.** For fold v, every case is transformed by the fold-v maps. PCs fitted on different folds share no coordinate system, so a fold-v nuisance or probe must see one map.

**Placeholder design.** Synthetic centres 101–104, switch steps, lengths, offsets and folds, all drawn from SeedSequence(99990001) streams. The set sizes match the protocol (278 / 158 / 204 / 201 / 123).

**Per-model input settings.** The full frozen specification, with checkpoint identifiers, source priority (R1: released code / config over paper prose; R2: never chosen by DS203 output), layers, pooling and stochastic layers, is `docs/CODELOCK_EXTRACTION_SPEC.md` / `docs/codelock_extraction_spec.json`. Summary:

| model | kind | input | clip L | representation | judgement calls |
|---|---|---|---|---|---|
| SurgeNetCholec / RARP | frame | 224² | — | CAFormer-S18 pooled normalised features (512) | input 224 and ImageNet normalisation; no level-1–3 SurgeNet source states the pretraining input or normalisation (224×399 is for downstream fine-tuning) |
| SelfSupSurg ResNet-50 | frame | 224² | — | pooled trunk (2048) | — |
| VideoMAE (ViT-B / ViT-L; HF and original-repository K400 / SSv2 / UCF101 pre-training checkpoints) | clip | 224² | 16 | final-LayerNorm last hidden state, mean over all 1,568 patch tokens (no CLS token) | normalisation from the checkpoint's `preprocessor_config.json` (HF) or ImageNet; ViT-S / ViT-H not covered |
| OmniTokenizer imagenet_k600 | clip | 256² | 17 | L2-normalised pre-VQ latent (8×32×32) | enc_block "ttww" follows the eval script; the paper text says 4 window layers |
| WF-VAE-L 16ch | clip | 256² | 33 | posterior mean (16×32×32) | 33 frames = the authors' evaluation clip; training used 25, then 49 |
| LARP-L-Long | clip | 128² | 16 | L2-normalised SVQ input (1024×16); no latent time axis | released config `bottleneck_dim` 16 versus paper d′ = 8; 16 used |
| LeanVAE 16ch / 4ch | clip | 256² | 17 | posterior mean (16 or 4 × 32×32) | — |
| Cosmos CV8x8x8 (reference) | native clip | 320² | ≤ 121 | post_quant_conv mean over latent time (16×40×40) | diffusers default config = CV8x8x8; the gated HF config was not read |

## 3. Differences between the task file and the protocol

1. **§11 small-truth flag (resolved by the audit remediation).**
   * §11 says cells with |truth| < 0.025 "are flagged at code lock".
   * Following the audit (`SS_CODELOCK_PARTA_AUDIT_REMEDIATION.md`, blocker 2), the runner computes this truth-only design check at code lock as stage (c2). It uses the real centre and offset only; the audit added this as a narrow exception to the metadata hard limit.
   * The truth depends on a replicate only through its c permutation. It is therefore computed exactly for all 24 permutations, with no seed drawn, and a cell is flagged if min |truth| < 0.025.
   * The public output holds flags and counts only. The truth values are kept in a provenance file.
   * `grid.cell_metrics` also flags cells when the real grid runs.
2. **§14 step 2 dry run.**
   * The dry run on PLACEHOLDER features runs in Part A: the `dryrun` module, which now drives `pipeline.run_checks` / `near_uniform`, and fast test 6.
   * The runner's projection stage is itself an all-arm SDR dry run on PLACEHOLDER features.
   * The audit accepts this, provided its execution and PASS are recorded: see `decisions/CODELOCK_PARTA_TEST_RECORD.md`.
3. **Grid-frame time order.**
   * The §3.1 grid rule ("first decoded frame whose presentation time is ≥ the grid time") selects a frame after the step end only when a source has a frame gap > 0.5 s. DS203 streams are constant-frame-rate at 25–50 fps.
   * The extraction counts such frames (`grid_frames_after_step_end`) and does not alter the rule.

## 4. Incidents

* **Incident 001 (procedural hard-limit incident):** evaluation-tool weight files arrived bundled with the third-party source code and were deleted. Full record: `decisions/CODELOCK_INCIDENT_001_third_party_weight_files.md`.
  * No weights of any eligible model or of the reference were downloaded.
  * No further third-party retrieval is permitted before the final code-lock commit. `scripts/fetch_third_party.sh` now refuses to run without `--after-final-code-lock`, and it uses a partial, sparse fetch that never materialises weight blobs.
* **Packages installed.** Python packages (timm, transformers, diffusers, einops) were installed into the separate venv only. The base environment is unchanged.
