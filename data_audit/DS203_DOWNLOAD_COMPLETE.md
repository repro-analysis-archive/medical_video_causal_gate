# DS203 (Appendix300) Bulk Download: Complete

* **Authorization:** Decision 004 (`314cd94`). Launched manually by the investigator with
  `scripts/download_ds203.sh` (`3c2eb51`).
* **Archive:** all 11 OPARA parts (doi 10.25532/OPARA-1173), **1,692.5 GB**. Each part is **VERIFIED against the host's
  MD5**; no size or MD5 failure.
* **Run:** started **2026-10-02T18:19:23+0900**, ended **2026-10-04T18:43:39+0900**, with `failures=0`. That is
  about 48.4 h, an average of about 9.7 MB/s with 3 parts in parallel.
* **Process:** finished (no lock held at the time of the status below).
* **Location:** `/media/user/LaCie/medvideo_gate/DS203/archive/`, with one `<part>.verified` file per part.
* **Not done:** no archive has been extracted, and no video content has been decoded (Decision 004).

## Final `--status` output (2026-10-05)

```
DS203 download status  (2026-10-05T08:04:08+0900)   dest: /media/user/LaCie/medvideo_gate/DS203/archive
  Appendix300_Full_Videos.z01        268.4 /   268.4 GB  VERIFIED
  Appendix300_Full_Videos.z02        268.4 /   268.4 GB  VERIFIED
  Appendix300_Full_Videos.z03        268.4 /   268.4 GB  VERIFIED
  Appendix300_Full_Videos.z04        268.4 /   268.4 GB  VERIFIED
  Appendix300_Full_Videos.z05        268.4 /   268.4 GB  VERIFIED
  Appendix300_Full_Videos.zip         18.1 /    18.1 GB  VERIFIED
  Appendix300_Images.zip             251.4 /   251.4 GB  VERIFIED
  Appendix300_Video_Snippets.zip      80.8 /    80.8 GB  VERIFIED
  archive_listing.txt                  0.0 /     0.0 GB  VERIFIED
  overall_merged.csv                   0.0 /     0.0 GB  VERIFIED
  readme_Appendix300.md                0.0 /     0.0 GB  VERIFIED
  TOTAL 1692.5 / 1692.5 GB (100.0 %)
  process: not running
```

## Completion lines from `download.log`

```
2026-10-02T18:19:23+0900 === run start (pid 116283, PARALLEL=3) ===
2026-10-03T11:34:01+0900 Appendix300_Full_Videos.z02: VERIFIED md5 94f4a2d15f92d3b77917877745ca726a
2026-10-03T14:07:22+0900 Appendix300_Full_Videos.z01: VERIFIED md5 e3f89e775c340419da45ba51a602a39e
2026-10-04T04:47:51+0900 Appendix300_Full_Videos.z03: VERIFIED md5 ca25754a42590c6f0452a54e9acefc9b
2026-10-04T05:01:13+0900 Appendix300_Full_Videos.z04: VERIFIED md5 01384d017d32a20fe5c783a59dc46165
2026-10-04T05:57:33+0900 Appendix300_Full_Videos.z05: VERIFIED md5 b3a7425103ea255592932a1269e2d751
2026-10-04T06:09:41+0900 Appendix300_Full_Videos.zip: VERIFIED md5 9124523698214d5a7ef5d0b8822896cf
2026-10-04T06:09:46+0900 archive_listing.txt: VERIFIED md5 318aa213ed0667b759d36ca5a5a8dbff
2026-10-04T06:09:48+0900 overall_merged.csv: VERIFIED md5 6daddbbd2b5dbb28d1b025963bf93ed6
2026-10-04T06:09:50+0900 readme_Appendix300.md: VERIFIED md5 3788f4415d7346649cc6596f3c84c902
2026-10-04T12:34:27+0900 Appendix300_Video_Snippets.zip: VERIFIED md5 d8f7eacd7bddffbec63b9bfd177d7e88
2026-10-04T18:43:39+0900 Appendix300_Images.zip: VERIFIED md5 53dcf58b5e1e59a47d6b754d9b444328
2026-10-04T18:43:39+0900 === run end: failures=0 ===
```

**Log artefact.** The status block that the script appended to its own log at run end reads "process: RUNNING (lock
held)". The script was still holding its own lock when it wrote that block. The status above, taken afterwards, shows
the process finished.
