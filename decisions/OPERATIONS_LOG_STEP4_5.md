# OPERATIONS_LOG_STEP4_5: operation of computation A (§14 steps 4–5 runner) and the decisions on chaining to step 6

* **Drafted:** 2026-10-07, in `/srv/ss_step6_prep/` while A was running. The repository was not touched.
* **Authority:** `CC_TASK_SS_step6_chain_prep_v1.md`. The investigator is the sole approver.
* **Run:** A = `scripts/run_step4_5.sh`, launch commit `9e1aa715af3067a912bb69733ab79df106877b53`, output `/media/user/LaCie/medvideo_gate/ss_step4_5/`.

**Labels.** "Reported" = stated by the investigator in the task file. "Verified" = checked read-only on 2026-10-07 at about 08:15 +0900, without reading anything under LaCie and without any git command in the repository.

## 1. Events

| when (+0900) | event | source |
|---|---|---|
| 2026-10-06 16:35 | A's memory guard stopped A with "memory pressure". **False positive:** about 80 GiB of RAM was available. | reported |
| 2026-10-06 | `vm.swappiness` changed from 60 to 10 | reported; verified: `/proc/sys/vm/swappiness` = 10 |
| 2026-10-06 17:28 | A resumed with the same launch commit | reported; verified: the orchestrator process started 17:28:48, the mask-check process 17:28:52 (`ps`) |
| 2026-10-06 17:28 → | the 4a mask check restarted from scratch | reported; consistent with the runner design (the locked mask check is a single unit with no internal checkpoint; `STEP4_5_RUNNER.md` §5); verified still running at 2026-10-07 08:15 |
| — | a watchdog, `~/ops/runner_watchdog_v1.sh`, relaunches A after a "memory pressure" stop | reported; **not verified:** at 2026-10-07 08:15 the file, `~/ops/` itself, a cron entry and a watchdog process were all absent; its log location is therefore not recorded here |

**Cause of the false positive.**
* The step 4–5 guard (`scripts/step4_5_orchestrate.py`, `Runner.pressure`) declares pressure if any of:
  * the run's resident memory exceeds the cap (100.5 GiB);
  * `MemAvailable` falls below 5 % of RAM;
  * more than 64 MiB is swapped out within 60 s.
* With one process running (the mask check), three consecutive strikes stop the runner.
* With about 80 GiB available, only the swap-out criterion can have fired. Swap-out also counts paging by other processes on the machine. Swappiness 10 reduces it.
* The step-6 runner does not use swap-out as a criterion (`STEP6_RUNNER.md` §3).

## 2. Decisions (investigator)

1. **Chain steps 5 → 6 automatically.** After A completes successfully:
   * commit the step-5 record (records only);
   * apply §13 mechanically (`scripts/apply_section13.py`) and commit the §13 record;
   * commit the step-6 runner and these records;
   * launch §14 step 6.

   On any A stop other than success, take no action; a "memory pressure" stop is waited out for the watchdog. The basis is `STEP6_RUNNER.md` §1: step 6's computation does not depend on step-5 outcomes, and §13 applies mechanically.
2. **Step-6 worker count: 18**, on CPUs 0–17, with code-lock thread settings. Projection: 6.6–6.7 days (`STEP6_RUNNER.md` §2).

## 3. ffmpeg "non monotonically increasing dts" warnings: QC check (`/srv/ss_checks/`)

**Source.**
* QC task `CC_TASK_SS_dts_frame_check_v1`, 2026-10-07 08:40–09:15 +0900, run outside the step 4–5 runner while A was running (`nice -n 19`, `ionice -c3`, `-threads 2`, one file at a time, no frame written to disk).
* Record: `/srv/ss_checks/QC_DECODE_RECORD.log` (SHA-256 `b5bf9aabc8d020d55b3642cad65966571e4f8a7abb407fbf87ffccd6aa6e0b3e`).
* Outputs: `out/scan_dts.jsonl` (`1ffc013e…659849`) and `out/count_locked.jsonl` (`e7903316…f182d`).
* Scripts: `scan_dts.py` (`21424dfc…2c6e`), `count_locked.py` (`7a2afb9e…cf3e`), `impact.py` (`9ffe0912…d976`).
* The checks ran on 21 staged files: Center4_001–008, Center5_001–010, Center2_005 and Center2_010, Center3_023. Each was packet-scanned with ffprobe (no decode); four were also decoded in full through the locked ffmpeg command (plus `-threads 2`).

**Results:**

| check | result |
|---|---|
| **Frame loss** | **None.** The four full decodes delivered exactly the expected number of frames: Center4_008 74,409; Center4_002 80,731; Center5_010 91,357; Center5_007 65,028. No partial frame bytes, exit code 0. |
| Source of the warning | The source packets have monotonic dts (0 non-increasing dts in all 21 files; no missing pts / dts). The warning comes from ffmpeg's rawvideo output muxer, at source frames whose **pts is duplicated**: 21 duplicate-pts events in the 21 files, in 12 of them, at most 3 per file. |
| Effect on the locked time mapping (`impact.py`) | Analytic, from the saved packet pts, replicating the locked grid and step rules; re-run on 2026-10-07 from the saved arrays with the same script. In the 12 files with duplicates, 1–5 frames per file carry a label one frame off (20 ms at 50 fps, 40 ms at 25 fps). **4 of the 74,630 grid frames** of the 21 files are shifted by one frame (Center2_010, Center4_007, Center4_008, Center5_003). |
| **Step boundaries** | **0 frames cross one.** 0 selected grid frames are displayed at or after their step end or before their step start, and 0 Cosmos-reference frames change step membership. |
| Scale to the 278 cases (1,046,620 grid frames per pass) | 4 / 74,630 × 1,046,620 ≈ **56 grid frames per pass ("about 50")**, each shifted by one frame within its step. This is a proportional extrapolation from the 21-file sample, not a census. |

* **Consequence:** none for the run. No frame is lost, and no frame changes step. The locked code and the runner are unchanged.

## Appendix: evidence extracted mechanically by chain_5_to_6.sh at 2026-10-12T14:26:41+09:00

* Watchdog `/home/user/ops/runner_watchdog_v1.sh`: present, 1302 bytes, SHA-256 1eb6f5e9d711fbae616d2d2843f474dd6990ebd1509337cb45a8a7bfbd59da4c.
* `/proc/sys/vm/swappiness` = 10.
* Step-6 launch arguments: `--workers 18`.
* Event lines of A's `/media/user/LaCie/medvideo_gate/ss_step4_5/logs/progress.log` (resource samples omitted):

```
2026-10-06T08:04:41+09:00 preflight passed: HEAD 9e1aa715af30 (launch commit 9e1aa715af30); clean tree; weights and third_party verified; 14 physical cores, 12 workers on CPUs [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], reserved CPUs [18, 19]; memory cap 100.5 GiB
2026-10-06T14:20:15+09:00 stage: done
2026-10-06T16:34:57+09:00 memory pressure with one process (swap-out 65 MiB in 60 s), strike 1/3
2026-10-06T16:35:12+09:00 memory pressure with one process (swap-out 65 MiB in 60 s), strike 2/3
2026-10-06T16:35:27+09:00 memory pressure with one process (swap-out 68 MiB in 60 s), strike 3/3
2026-10-06T16:35:27+09:00 shutting down: memory pressure with a single process
2026-10-06T16:35:27+09:00 STOP: memory pressure with a single process
2026-10-06T17:28:49+09:00 preflight passed: HEAD 9e1aa715af30 (launch commit 9e1aa715af30); clean tree; weights and third_party verified; 14 physical cores, 12 workers on CPUs [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], reserved CPUs [18, 19]; memory cap 100.5 GiB
2026-10-07T21:33:51+09:00 mask_check: done
2026-10-09T12:20:40+09:00 extract_P: done
2026-10-11T00:39:50+09:00 extract_P-nat: done
2026-10-11T12:57:19+09:00 memory pressure (swap-out 70 MiB in 60 s): concurrency 2 -> 1, stopping extract_S
2026-10-11T12:57:20+09:00 extract_S: stopped for memory pressure; resumes after the other lane finishes
2026-10-11T16:26:28+09:00 extract_REF: done
2026-10-12T13:33:00+09:00 extract_S: done
2026-10-12T13:33:03+09:00 near_uniform: done
2026-10-12T13:34:22+09:00 step-4 record committed: 8d4c61a0163e836c5df363166e4b1aee4352c174
2026-10-12T13:40:57+09:00 build_reps: done
2026-10-12T14:25:31+09:00 checks: done
2026-10-12T14:25:33+09:00 run complete: step-4 record committed, step-5 record written (not committed); §14 step 6 is not part of this runner
```
