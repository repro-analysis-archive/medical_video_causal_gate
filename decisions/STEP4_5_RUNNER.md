# STEP4_5_RUNNER: unattended §14 steps 4–5 runner (orchestration only)

* **Recorded:** 2026-10-05.
* **Authority:**
  * `CC_TASK_SS_step4_5_prep_v2.md`;
  * `CC_TASK_SS_resource_policy_v1.md`;
  * `CC_TASK_SS_step4_5_resume_v1.md`.
* **Base:**
  * frozen protocol `4c86dc5`;
  * final code lock `98cba1e` (SDR `af56777`);
  * CODELOCK_CORRECTION_001 `ad8833a`;
  * selection record `ba73820`.
* **Selected models:**
  * primary: SurgeNetCholec;
  * secondary: LeanVAE-4ch;
  * reference: Cosmos-1.0-Tokenizer-CV8x8x8.
* **DS203 status:** no DS203 frame has been decoded. Step 4 begins only when the investigator launches the runner.

## 1. Orchestration only

Files added after the code lock:

| file | role |
|---|---|
| `scripts/run_step4_5.sh` | Entry point. Holds the run lock (`flock`), offers `--status`, and execs the orchestrator. |
| `scripts/step4_5_orchestrate.py` | Sequencing, provenance checks, retries, memory watchdog, resource log, records, the records-only commit, and status. |
| `scripts/step4_5_launch.py` | Sets torch threads and the deterministic GPU flags, then calls the locked `ss_benchmark.pipeline.main` unchanged. |
| `scripts/stage_ds203_videos.py` | Byte copy of the 278 cases' archive members, checked against the archive's CRC-32. No decoding, no re-encoding. |
| `scripts/make_step4_5_fixture.py` | FIXTURE generator, for smoke tests only. |
| `tests/test_step4_cosmos_equivalence.py` | Cosmos equivalence test (§3). |
| `tests/test_step4_5_runner.py` | Fast tests of the STOP and provenance helpers. |

**Every computation is a call to the locked CLI.**
* The only pipeline subcommands the runner can call are `mask-check`, `extract`, `near-uniform`, `build-reps` and `checks` (whitelist `PIPELINE_COMMANDS`).
* The runner contains no estimator, DGP, grid or step-6 entry.
* The CLI runs from a `git archive` snapshot of the launch commit, plus the two adapter third-party trees `third_party/LeanVAE` and `third_party/SurgeNet`. Both trees are pinned by tree digest; per-file SHA-256 values are recorded in `code_snapshot.json`.

**Diff stat against `ba73820`.** No file under `ss_benchmark/`, `docs/` or any earlier record changed:

```
 decisions/STEP4_5_RUNNER.md            | 380 ++++++++++++++++++++++++++++
 scripts/make_step4_5_fixture.py        | 223 +++++++++++++++++
 scripts/run_step4_5.sh                 |  52 ++++
 scripts/stage_ds203_videos.py          | 228 +++++++++++++++++
 scripts/step4_5_launch.py              |  33 +++
 scripts/step4_5_orchestrate.py         | 851 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_step4_5_runner.py           | 127 ++++++++++
 tests/test_step4_cosmos_equivalence.py |  98 ++++++++
 8 files changed, 1992 insertions(+)
```

## 2. The two execution-order points

1. **Automatic step-4 commit before step 5.**
   * After 4b, the runner writes the step-4 records to `results/step4/`. These are exactly ten files: the representation manifest, the four locked per-arm manifests, the mask-check record, the near-uniform record, the staging manifest, `run_meta.json` and `STEP4_RECORD.md`.
   * It commits them alone, using the repository-scoped identity.
   * It then verifies that the commit's parent is the launch commit and that its diff is exactly those ten files, and persists the commit hash.
   * Only then does step 5 start. If any of this fails, the runner STOPs.
   * Step 5 is never committed automatically: its record goes to `results/step5/`, uncommitted.
2. **A post-lock orchestration runner.**
   * The runner was written after the final code lock and is not part of it. It adds no analysis code (§1).
   * It runs the locked code exactly as locked, from a snapshot of the launch commit.
   * It is therefore a separate, recorded component: the locked analysis files are byte-identical to `ba73820`.

**Provenance logic** (`step4_5_orchestrate.py` `preflight`, `verify_record_commit`, `commit_step4_record`):
* **Launch:**
  * HEAD must equal `--expect-commit`;
  * HEAD must contain `scripts/run_step4_5.sh`, byte-identical to the script being run;
  * the tree must be clean (`git status --porcelain --untracked-files=all` empty);
  * no process of an earlier run may still be alive;
  * the run lock is acquired, then the launch commit is persisted in `state.json`.
* **Resume before the step-4 commit:** the same checks. The only untracked files tolerated are step-4 record files that this run wrote and listed with their SHA-256 in `state.json`. They cover the window between writing and committing the records.
* **Resume after the step-4 commit:** HEAD must equal the recorded step-4 commit; its parent must equal the launch commit; its message must carry the runner prefix; its diff must be exactly the ten record files; the tree must otherwise be clean. Anything else is refused.
* **What a refusal does:** exits with status 3 and changes nothing in the run state.
* **After a completed run:** a relaunch is refused ("already complete").

## 3. Cosmos reference: weights, official code, equivalence

**Weights.**
* Repository `nvidia/Cosmos-1.0-Tokenizer-CV8x8x8`, revision `5110dbb3c94a9eb6648eabbbccc19c76180fe426`.
* Downloaded with the investigator's existing Hugging Face login (`hf_hub_download`, `huggingface_hub` 0.36.2, not upgraded; the token was never printed, logged or copied).
* Location: `/media/user/LaCie/medvideo_gate/weights/cosmos/Cosmos-1.0-Tokenizer-CV8x8x8/`; log: `weights/download_step4_prep.log`.

| file | bytes | SHA-256 |
|---|---:|---|
| `vae/config.json` | 13,258 | `17ea012aa67ad5e3d381604cfa2e05431f2058edabc650163ffc96db4d69ccbc` |
| `vae/diffusion_pytorch_model.safetensors` | 211,344,392 | `59dca00bd6d3f20b8201d54dd6697da63cbcf768513004acd4216bd45a56a241` (= published LFS SHA-256) |
| `autoencoder.jit` | 212,300,573 | `b9ae035599336bcd092d3106f25c02ba934191dec4f196f7412deb785fe2acb1` (= published LFS SHA-256) |
| `config.json` | 52 | `edad7b66daff1a31f45f61da542d03599432536efa9b2d03dbab0a213a0e9161` |
| `model_config.yaml` | 92 | `69bc6fabb030be2ddba76c0a6944882348c3db0426baf31ced29ca02aeaba679` |

* The reference adapter (diffusers `AutoencoderKLCosmos`) reads `vae/`.
* `autoencoder.jit` is the official repository's released format of the same checkpoint. It is used only by the equivalence test.

**Official code.**
* Repository: NVIDIA/Cosmos-Tokenizer @ `3584ae752ce8ebdbe06a420bf60d7513c0e878cc`, 17 raw files in `third_party/Cosmos-Tokenizer/cosmos_tokenizer/` (git-ignored, no weight files).
* Combined digest of the 17 `sha256 path` lines: `cd8827c6cd5de8697790fd83c69e88335f1536eaf5c69b91b2c469e597b78409`.
* Retrieved 2026-10-05 16:55 +0900.

| file | bytes | SHA-256 |
|---|---:|---|
| `cosmos_tokenizer/__init__.py` | 678 | `57bf220665b8cad4b7b8ff8b1a863aa0a500553c179b32ede49e6e816c35780e` |
| `cosmos_tokenizer/utils.py` | 13510 | `518055285c6b623e25442227fd65c92afebc0b39c660831c5c19d6673f575dff` |
| `cosmos_tokenizer/video_lib.py` | 6022 | `22cdfc1cdc1457429adf46f26598ce1f4099b79f0e163c4de9fd25acc19af1ac` |
| `cosmos_tokenizer/image_lib.py` | 4784 | `48759d26aa994544684226b71d706ed3c99bcd8be2296e662b52179e59db4fbb` |
| `cosmos_tokenizer/modules/__init__.py` | 1639 | `cb86988dffb9b7063d14ac61dcd61ab5d338cb633dbde003be68d7b224a3b45f` |
| `cosmos_tokenizer/modules/distributions.py` | 1538 | `555fc512200b59ef0f6c9d29fd67d40feeea3f85e408a42e7c22c65de10fe67c` |
| `cosmos_tokenizer/modules/layers2d.py` | 12086 | `5145bc16d02b1ca6f6fb55c9993f8ecccaa0dbdd55d6d490a9eed4da20b5456d` |
| `cosmos_tokenizer/modules/layers3d.py` | 33996 | `3b62fc404dac38dba37e662d0c7ea134887d612e2a7b88b8d67a63297371cd8e` |
| `cosmos_tokenizer/modules/patching.py` | 13422 | `07ee9574674daa01cff64f1ed1fcdc6b3d579eafa89f2861ccfe84023519cef1` |
| `cosmos_tokenizer/modules/quantizers.py` | 20267 | `5a4b84a03b128f215c96addced856d90248ae04d2188560314bbcc2a72db7b09` |
| `cosmos_tokenizer/modules/utils.py` | 3239 | `ae8997f3b85f92b455819c4b61bd5dab2e0f5c1d81ee3616c891a9151309e3e0` |
| `cosmos_tokenizer/networks/__init__.py` | 1753 | `339a6092b05b524cdd38e2a2c2d1a4f9f3041aa8f02b507a1f49f4cf99693aec` |
| `cosmos_tokenizer/networks/configs.py` | 4633 | `6ed86cc10e112df5b3acdeb774b97c670d8b8866c295dba7ade708e4eb0800b9` |
| `cosmos_tokenizer/networks/continuous_image.py` | 3673 | `3e8c74e320137678be6d90695c1f1933e74b701916e4129d679f95683b0d3825` |
| `cosmos_tokenizer/networks/continuous_video.py` | 4051 | `27d689b2c9d8ab2318982ff1e9ee6ffb3546d9bfacacc344297e12c479b5276e` |
| `cosmos_tokenizer/networks/discrete_image.py` | 5185 | `bc3982db1dbef29d6fcdeab0e78d41b48acc79fab38aedbd4c02bbb408d6e275` |
| `cosmos_tokenizer/networks/discrete_video.py` | 5470 | `8abc956f872cac4cecebad121c368eee825a34b91402de7d3fc9e21e4ceac430` |

**Equivalence.**
* Test: `tests/test_step4_cosmos_equivalence.py`, run in the extraction venv.
* Inputs: the same released checkpoint (the safetensors for ours, the JIT for the official model; all tensors are stored in bfloat16 and loaded into float32), float32 on CPU, synthetic input from seed 99990002.
* The input is 121 frames of 270 × 480, prepared by the adapter's own preprocessing to (1, 3, 121, 320, 320).
* Official comparator: `cosmos_tokenizer.utils.load_model(autoencoder.jit, tokenizer_config=TokenizerConfigs.CV with spatial and temporal compression 8)` → `post_quant_conv(encode(x)[0])`, averaged over latent time.
* **Result: max |difference| of the 16 × 40 × 40 representation = 3.725e-7, against a limit of 1e-4. PASS.**

**What the official loader omits.** The official loader is `strict=False` by design (`utils.py` lines 50, 71 and 92: `load_state_dict(ckpts.state_dict(), strict=False)`). The test pins exactly what this leaves unmatched; every other tensor (310) loads and is asserted equal.
* **12 parameters in the official model but not in the checkpoint:**
  * `encoder.down.1.downsample.conv{1,2,3}.conv3d.{weight,bias}`;
  * `decoder.up.2.upsample.conv{1,2,3}.conv3d.{weight,bias}`.
* **Why the 12 are never used:**
  * Downsampling: `layers3d.py` line 758 gives `num_spatial_downs = log2(8) − log2(patch_size 4) = 1`, and line 765 gives the same temporally. A downsample module is built at every level except the last (line 815), with `spatial_down = i_level < num_spatial_downs` (line 816). At level 1, both flags are False, and `CausalHybridDownsample3d.forward` returns its input unchanged (line 240). In the released trace, `encoder.down.1.downsample.forward` is empty.
  * Upsampling: at `up.2`, `i_level_reverse = 0`, so `temporal_up = 0 < 0 < …` is False (line 1001, `legacy_mode=False`) and `spatial_up` is False. `CausalHybridUpsample3d.forward` returns its input (line 181).
  * The decoder is outside the representation in any case: encoder → `quant_conv` → `post_quant_conv`.
* **5 buffers in the checkpoint but not in the official model's state dict:**
  * `encoder.patcher3d.{wavelets, _arange, patch_size_buffer}`;
  * `decoder.unpatcher3d.{wavelets, _arange}`.
* **Why the 5 are fixed constants:**
  * The source registers them with `persistent=_PERSISTENT`, and `_PERSISTENT = False` (`patching.py` line 36), so they are fixed Haar-transform constants rather than learned weights.
  * The JIT stores them in its trace dtype (bfloat16). The test asserts that the source values, rounded to that dtype, equal the stored ones.
  * The float32 comparison therefore uses the official PyTorch source path, because the JIT is a bfloat16 trace with dtype constants baked in.

## 4. Determinism (operational reproducibility setting)

* **When and why chosen:** before any DS203 extraction, as an operational reproducibility setting. It is not a protocol choice. The 25 % figure in the resource-policy addendum is an operational guideline, not a protocol criterion.
* **Settings** (in `step4_5_launch.py` and the orchestrator's environment):
  * `torch.backends.cudnn.deterministic = True`;
  * `torch.backends.cudnn.benchmark = False`;
  * `torch.use_deterministic_algorithms(True, warn_only=True)`;
  * `CUBLAS_WORKSPACE_CONFIG=:4096:8`.
* **Check:**
  * Synthetic input from `feasibility.synthetic_input`, real verified weights, bf16 on CUDA as in the locked `extract_all`.
  * Each configuration ran in its own process, twice per mode.
  * The same input was encoded twice within each process.
* **Result: bit-identical outputs for all three models.** Each model's output was the same within each process, and its SHA-256 was the same under default and deterministic settings. No determinism warning was raised.
* **Cost:**

| model | batch | default (inputs/s) | deterministic (inputs/s) | cost | output SHA-256 (first 16) default = deterministic |
|---|---:|---:|---:|---:|---|
| SurgeNetCholec | 64 | 1715.8 / 1713.4 | 1664.0 / 1665.2 | 3.0 % | `911624796164b527` = `911624796164b527` |
| LeanVAE-4ch | 1 | 222.8 / 223.8 | 213.5 / 215.2 | 4.0 % | `487f4e6db744071d` = `487f4e6db744071d` |
| Cosmos-CV8x8x8 | 1 | 5.445 / 5.428 | 5.086 / 5.097 | 6.4 % | `34ab1ff12d809837` = `34ab1ff12d809837` |

* **Fixing the result:** the committed step-4 manifest hashes fix the representations actually used.

## 5. Resource settings (`CC_TASK_SS_resource_policy_v1.md`)

* **CPU:**
  * Intel i5-14600K: 14 physical cores (6 P-cores with 2 threads each, 8 E-cores), 20 logical CPUs.
  * **Workers = 12:** logical CPUs 0–17. Cores 12–13 (logical CPUs 18, 19) are reserved for the OS, I/O, logging and the orchestrator itself.
  * Every pipeline process runs under `taskset -c 0-17`.
  * **Threads: 6 per pipeline process** (torch intra-op, OpenMP, OpenBLAS and MKL set equal; OpenMP waits passive).
    * The two extraction lanes use all 12 workers.
    * For single-process stages, more threads do not help the locked code: on synthetic features, the locked multinomial site-probe fit took 2.5–2.8 s at 2–8 threads, 3.2 s at 1 thread and 17.4 s at 12 threads (12k rows); at 84k rows it took 15.5 s (4 threads) against 38.7 s (12 threads).
    * The smoke run's step-5 checks at 12 threads had not finished after 2 h 17 min (§9).
  * **Thread count is fixed before launch.** It changes step-5 floating-point results: the fixture's build-reps at 12 versus 6 threads differed by about 1e-13 relative for P, P-nat and S, and by 1.6e-5 for REF (randomized SVD, d = 25,600). The step-4 representations are computed on the GPU with the deterministic settings of §4 and are fixed by the committed manifest hashes.
* **Memory:**
  * The run's resident memory (the orchestrator plus all descendants) is capped at 80 % of 125.6 GiB, i.e. 100.5 GiB.
  * Pressure means any of: the cap is exceeded; `MemAvailable` falls below 5 %; or more than 64 MiB is swapped out within 60 s.
  * Under pressure with two lanes, the most recently started lane is stopped and resumes after the other lane finishes.
  * Under pressure with one process (three strikes, 45 s), the runner STOPs.
  * Expected peak: step 5's REF randomized SVD, about 30–35 GiB.
* **GPU:**
  * RTX 4500 Ada, 24 GiB.
  * Peak reserved memory with both lanes active ≈ 2.14 + 0.26 GB, below the 20.0 GB feasibility bound.
  * Batch 64 for the frame model (the tested pipeline default); one step per call for the clip models, as locked.
  * Extraction is decode- and CPU-bound, so the GPU is not the bottleneck.
* **LaCie (rotational, mq-deadline, read-ahead 128 KiB):**
  * Staging is a single reader with 64 MiB sequential reads, in archive order.
  * Extraction has 2 concurrent readers (two lanes): lane 1 = REF; lane 2 = P, then P-nat, then S.
  * Measured on synthetic files on LaCie: one reader 230 MB/s; two concurrent readers with ffmpeg-sized 32 KiB reads 198 MB/s aggregate (86 %), so no seek thrashing.
* **Stability:**
  * Checkpoints: the locked per-case manifest for extraction, the staging manifest per member, and a done marker per stage. A resume skips completed units.
  * The mask check, near-uniform, build-reps and checks are each a single unit.
  * Failures are retried with backoff of 60, 300 and 900 s. Three consecutive failures without progress STOP the runner with a log message.
  * Inside the stager, I/O errors are retried after 5, 30 and 120 s, and a CRC mismatch is retried once.
* **Logging:**
  * Every 10 min, `logs/progress.log` gets a `RES` line: CPU %, load, RAM used and available, the run's RSS against the cap, swap used, GPU memory, temperature and utilisation, CPU package temperature, disk read and write MB/s.
  * No estimate or result is logged.

## 6. Run time

**Historical figure (unchanged; `MODEL_SELECTION_RECORD.md` §8).**
* The §14 step-4 projection at step 3: **(A) frozen §10.4 components 40.6 h; (B) as implemented 74.8 h.**
* Per-pass (B) figures: mask 6.67 h, P 8.98 h, P-nat 8.24 h, S 8.94 h, REF 41.94 h.

**Operational end-to-end estimate (this record).** This is an operational planning figure, not a protocol criterion.
* **Staging (1.344 TB, 350 members):**
  * A same-disk 64 MiB copy on LaCie measured 98.9 MB/s on a synthetic file in a freshly written region, where reads ran at 230 MB/s.
  * The archive region reads at 116.9 MB/s (2012acd), which gives about 70 MB/s for the copy.
  * **Estimate: about 4–5.5 h.**
* **Full-file ffprobe overhead per pass:**
  * The locked `case_timeline` runs `ffprobe -show_entries packet=pts_time` on every file before decoding it. This reads each file once in full, at 1.344 TB / 116.9 MB/s ≈ **3.2 h per pass**, disk-bound.
  * The step-3 (B) figure does not include it.
  * The decode that follows reads mostly from the page cache: files are ≤ 17 GB, against about 80 GiB available.
* **Per pass, operational ((B) + 3.2 h):**
  * mask 9.9 h; P 12.2 h; P-nat 11.4 h; S 12.1 h;
  * REF 45.5 h (including about +0.4 h from the deterministic settings).
* **4b with two lanes:**
  * Lane 2 (P, P-nat, S) ≈ 35.7 h when it runs alone.
  * When both lanes are in CPU-bound phases, CPU contention slows each lane by a factor of about 1.0–2.0 per frame (measured on synthetic frames); this estimate uses about 1.5.
  * **Estimate: about 60–68 h**, against 81.6 h if the four arms ran one after another.
* **Records and commit:** < 0.5 h (SHA-256 of about 13 GB).
* **Step 5 (build-reps + checks):** measured on the fixture at the final setting (6 threads): build-reps 57 s, checks 2.13 h for 14,982 steps.
  * The locked learners are pure numpy (Newton logistic, numpy MLP with mini-batch 200) and the bootstraps work on rows, so the cost is about linear in rows.
  * Scaled to the real 104,662 steps (× 7.0): **build-reps ≈ 0.1–0.3 h; checks ≈ 15 h (range about 12–18 h).**
  * Peak memory is about 30–35 GiB (REF randomized SVD), within the 100.5 GiB cap.
* **Total, steps 4–5: about 3.4–4.0 days (82–96 h = mask 9.9 + 4b 60–68 + records 0.5 + step 5 12–18); plus staging about 4–5.5 h.**
* The reduced-resolution smoke fixture is not a throughput benchmark. Its decode and extraction timings are not used. Its step-5 timing is used, scaled by rows, because step-5 cost depends on rows and representation dimensions, not on video resolution.
* The task header's figure of about 3.2–3.4 days for steps 4–5 did not yet include step 5's measured cost; this estimate does.

## 7. Space

* **Representation output, step 4.** The 278 cases are 145.56 video hours and 104,662 steps (Σ floor(duration / 5) from `DS203_d8_cases.csv`, an aggregate of container metadata only), with 1,046,620 grid frames per pass.

  | arm | dimension | float32 size |
  |---|---:|---:|
  | P | 512 | 0.214 GB |
  | P-nat | 512 | 0.214 GB |
  | S | 4096 | 1.715 GB |
  | REF | 25,600 | 10.718 GB |
  | near-uniform flags (P, S) | — | 0.002 GB |
  | **total** | | **≈ 12.9 GB** |

  The step-3 upper bound over all 403 files (108,238 steps) gives 13.3 GB.
* **Step 5:**
  * `reps_full_<key>.npz`: 64 PCs, float64, 5 folds, R and R-C for P, S and REF, R for P-nat: ≈ 1.9 GB.
  * `reps.npz`: ≈ 0.2 GB.
  * Total ≈ 2.1 GB.
* **Snapshot and logs:** < 0.1 GB.
* **Representation-output total ≈ 15.0 GB**, so 3 × = 45 GB.
* **LaCie free space:**
  * Before staging (2026-10-05): 4,352,813,301,760 B.
  * Staging uses 1,343,862,664,088 B (350 members).
  * **After staging: 3,008,950,637,672 B ≈ 3.01 TB**, about 200 × the representation output, so **≥ 3 × is satisfied**.
* **/home:** 24.7 GB free. The repository receives only the records (< 5 MB).

## 8. Fixture design (synthetic only)

`scripts/make_step4_5_fixture.py`, seed 99990003. Every file is labelled FIXTURE: directory names, mp4 title and comment tags, a `fixture` column in every CSV, the zip comment, and `fixture_manifest.json`. No DS203 byte, frame, case or metadata value is used; only the per-centre media formats come from the 2012acd container facts (medians).

* **Cases:**
  * 278 cases, IDs C2–C5 with op 701+: C2 62, C3 42, C4 71, C5 103.
  * Set sizes: primary 158, single-file 123, W0 204, W5 201.
  * 35 primary cases and 5 further cases have two files (`_v01`, `_v02`).
  * Window layouts satisfy the locked code:
    * primary: w in 30–34, region w−30..w+44 inside the video;
    * W0 / W5: w..w+14 inside the video.
* **Reduced-resolution videos (272 cases):**
  * 1080p formats → 256 × 144; 2160p formats → 512 × 288.
  * Matched to each format: H.264 High; level 5.0 (1080p) or 5.1 (2160p); frame rate 25 or 50; keyframe interval in frames (C2-1080p 60, C2-2160p 30, C3-2160p 36, C4 96, C5 214); 3 B-frames, 5 references; bitrate per pixel.
  * Achieved (ffprobe): C2-1080p 0.287 Mbps / GOP 59.7; C2-2160p 1.312 / 29.6; C3-2160p 1.34 / 36.0; C4 0.143 / 95.7; C5 0.155 / 205.0.
* **Full-resolution clips:** one 16.5-s clip per distinct centre / media format, as cases outside every set:

  | format | Mbps | GOP |
  |---|---:|---:|
  | C2 1080p25 | 16.3 | 59 |
  | C2 2160p25 | 75.1 | 29.5 |
  | C3 2160p25 | 77.3 | 34.4 |
  | C3 1080p25 | 7.6 | 103 |
  | C4 1080p50 | 7.9 | 92 |
  | C5 1080p50 | 8.5 | 206 |

  Short clips end with a partial GOP, which lowers the averages.
* **Content:** ffmpeg `testsrc2` with a per-case hue shift, a per-case temporal noise seed and a vignette.
* **Totals:** 318 files, 3.88 GB, 20.9 video hours.
* **Archive and metadata:**
  * DS203 layout: `Full_Videos/Center<c>/FIXTURE_Center<c>_<op>/Center<c>_<op>[_vNN].mp4`.
  * `zip -0 -fz -s`: stored, ZIP64, split into `.z01`–`.z05` plus `.zip`.
  * Metadata in the formats of `DS203_d8_cases.csv`, `ss_window_offsets.csv` and `ss_window_offsets_perW.csv`.
* **Limitations:**
  * The fixture serves orchestration, STOP conditions, the commit, interruption and resume, status and manifests. It is not a throughput benchmark.
  * A full-resolution fixture for all 278 cases would need about 21 h of video, including 4K at about 75 Mbps; hence the reduced resolution plus one full-resolution clip per format.

## 9. Smoke tests (throwaway clone; FIXTURE only)

**Setup.**
* Throwaway clone of `ba73820` in the session scratchpad (local NVMe) with:
  * a clone-only commit of the runner files under test (`a50eaf3`);
  * a clone-only commit replacing the three case-metadata CSVs with the FIXTURE versions (`11448a1`, the launch commit).
* `third_party/LeanVAE` and `third_party/SurgeNet` copied in. The verified weights were read from LaCie.
* Output and fixture archive in the scratchpad.
* Launched exactly as in §10 (`setsid nohup … --expect-commit 11448a1 --out <scratch> --archive-zip <FIXTURE archive>`). The resource-sample interval was 60 s, set for the test through `SS_RUNNER_RES_INTERVAL_S`.
* **No DS203 file was opened.** The runner's archive was the FIXTURE archive.
* The SHA-256 values of the runner files under test equal those committed here, except `step4_5_orchestrate.py`, which was changed afterwards only in its thread setting (§5; workers / 2 for single-process stages instead of 12) and docstring.

**Results** (2026-10-05).

| # | scenario | result |
|---|---|---|
| T1 | start with an untracked file in the tree | refused, exit 3; no run state created |
| T2 | start with `--expect-commit` ≠ HEAD | refused, exit 3 |
| T3 | clean launch | staging 318 / 318 members (byte copy, CRC-32 checked, 8 s) → mask check (5 min; valid: r = 0.45 stands on the fixture) → two lanes started |
| T4 | SIGTERM to the process group during 4b (P 43 / 278, REF 5 / 278) | children terminated, state `stopped: interrupted by signal 15`, no process left |
| T4b | resume with an untracked file | refused, exit 3; state unchanged |
| T5 | resume | preflight passed; staging and mask check skipped. The 43 P and 5 REF cases finished before the interruption kept identical SHA-256 and mtime; extraction continued. Lane 2: P done 18:26, P-nat 18:37, S 18:52. Lane 1: REF done 19:52. |
| — | outputs | P / P-nat 512-d, S 4096-d, REF 16 × 40 × 40 for 278 / 278 cases. Near-uniform flags only for the standardized arms. All six full-resolution clips decoded, cropped, resized and extracted (finite outputs). |
| T6 | automatic step-4 commit | `05bb975` = exactly the ten `results/step4/` files; parent = launch commit `11448a1`; repository-scoped identity; persisted in state |
| T6 | SIGKILL to the process group 2 s after the commit (during build-reps) | no process left; status `not running` |
| T7a | resume with HEAD = launch commit (detached) | refused, exit 3 |
| T7b | resume with an extra commit on top of the step-4 commit | refused, exit 3 |
| T8 | resume with a modified tracked file | refused, exit 3; state unchanged by T7a–T8 |
| T9 | resume with HEAD = step-4 commit, clean tree | preflight passed (launch and record commits verified, diff records-only); went straight to step 5: build-reps (restarted as a unit, 1.4 min), checks started; no new commit |
| T10 | SIGTERM during step 5 (checks after 2 h 17 min with the earlier 12-thread setting) | stopped cleanly; HEAD still `05bb975`, tree clean, nothing written to `results/step5/` |
| — | step 6 unreachable | the runner can call only `mask-check`, `extract`, `near-uniform`, `build-reps` and `checks` (whitelist, unit-tested); no grid or step-6 code is referenced |

**Step 5 at the final setting.**
* Locked build-reps and checks were run outside the runner, with the runner's exact launcher, environment and CPU set, on the smoke's step-4 representations (6 threads): build-reps 57 s and checks 7,681 s (2.13 h) for the fixture's 14,982 steps. `checks.json` was written with the four representation keys (P, P-nat, REF, S); its values were not inspected, being FIXTURE outputs.
* **Bit-identity at 6 threads:** a second build-reps at 6 threads gave bit-identical `reps.npz`, `reps_full_{P,P-nat,S,REF}.npz` and `reps_report.json`. Step 5 is reproducible at the fixed thread count.
* The end-of-run path (step-5 record written to `results/step5/`, never committed; a completed run refuses relaunch) is covered by unit tests (`tests/test_step4_5_runner.py`, 8 tests). The tests also cover:
  * the records-only check against forged commits (extra path, wrong prefix, wrong parent);
  * the frozen mask-check rule and the failure of its single fallback;
  * the step-6 whitelist.

**Cleanup.** The clone, the fixture (tree, archive, metadata), the smoke output and the step-5 timing output were deleted afterwards (§11).

**Expected log noise.** `Broken pipe` lines from ffmpeg in `mask_check.log` and the `extract_*.log` files are expected. The locked decoder stops reading once a case's last needed frame has arrived; these lines are not failures.


## 10. Launch (investigator; not done here)

**Launch or resume** (from the repository root; survives closing the terminal):

```
cd /home/user/projects/medical_video_causal_gate
setsid nohup scripts/run_step4_5.sh --expect-commit <COMMIT> > /dev/null 2>&1 < /dev/null &
```

* `<COMMIT>` is the full hash of the commit that adds this record and the runner (`git log -1 --format=%H -- decisions/STEP4_5_RUNNER.md`; stated in the report).
* The same command resumes after any interruption. After the step-4 commit, the runner accepts HEAD = that commit, as in §2.
* A resume must not be started with any other HEAD, and the tree must stay clean throughout. In particular, `results/step5/` appears only at the end.

**Other commands:**
* **Status** (progress counts and the latest resource sample only): `scripts/run_step4_5.sh --status`
* **Stop deliberately** (resumable): `kill -TERM -- -<pid shown by --status>`. This signals the whole process group.

**Paths** (all on LaCie under `/media/user/LaCie/medvideo_gate/ss_step4_5/`):

| path | contents |
|---|---|
| `logs/progress.log` | stage events and `RES` samples every 10 min |
| `logs/runner_stdout.log` | refusals and orchestrator output |
| `logs/<stage>.log` | stdout / stderr of each locked command: `stage`, `mask_check`, `extract_P`, `extract_P-nat`, `extract_S`, `extract_REF`, `near_uniform`, `build_reps`, `checks` |
| `state.json` | run state, launch commit, step-4 record commit |
| `runner.lock` | run lock |
| `staged/Full_Videos/` | staged copies (1.344 TB) |
| `step4/` | mask-check and near-uniform outputs |
| `extract/<arm>/` | representations and locked manifests |
| `step5/` | reps and checks |
| `step5_record/` | step-5 record before it is copied to `results/step5/` |
| `code_snapshot/` | code the run executes |

Records in the repository: `results/step4/` (committed by the runner) and `results/step5/` (not committed).


## 11. Not done here

* The runner was not launched on DS203, and no DS203 frame was decoded.
* The real archive's central directory was not read in this task. The stager reads it at launch and STOPs before copying if parsing fails. It uses the same ZIP64 / split-part logic as `data_audit/lead/probe_ds203_containers.py` (`146f69b`), which parsed the central directory of the same OPARA split archive over HTTP range requests.
* The smoke clone, the fixture, the smoke outputs and the scratch step-5 timing outputs were deleted. Benchmark scratch files on LaCie (synthetic only) were deleted right after each measurement.
