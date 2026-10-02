#!/usr/bin/env bash
# DS203 (Appendix300) pre-protocol bulk download to LaCie (Decision 004). Launched manually by the investigator.
#   bash download_ds203.sh            download (resumable; safe to re-run)
#   bash download_ds203.sh --status   print per-part progress / verification and the last log lines
#   bash download_ds203.sh --check    space + mount + server checks only, no download
# Behaviour:
#   * Destination is on LaCie only (refuses to run if LaCie is not mounted or DEST is on another filesystem).
#   * Space rule: LaCie free space >= 3 x 1.69 TB, else exit. On a resumed run, bytes already downloaded into DEST
#     are credited (free + already_downloaded >= 3 x total), so that a partial download can resume.
#   * Each part: curl byte-range resume (-C -), retried with exponential backoff (30 s .. 15 min) on network
#     errors; PARALLEL parts at a time.
#   * After a part completes: size check, then MD5 against the OPARA checksum; the result is logged and written
#     to <part>.verified (OK) or <part>.md5fail (FAIL; the file is kept, not deleted).
#   * Log: $DEST/download.log on LaCie. A lock prevents two concurrent runs.
# Nothing in this script decodes, extracts or computes on video content.
set -u
LACIE=/media/user/LaCie
DEST=$LACIE/medvideo_gate/DS203/archive
LOG=$DEST/download.log
PARALLEL=${PARALLEL:-3}
B=https://opara.zih.tu-dresden.de/server/api/core/bitstreams
# name|uuid|bytes|md5   (OPARA ORIGINAL bundle of doi 10.25532/OPARA-1173, read 2026-10-02)
MANIFEST="Appendix300_Full_Videos.z01|79c7da37-1528-4b4c-a2bc-cd5902e9d7a3|268435456000|e3f89e775c340419da45ba51a602a39e
Appendix300_Full_Videos.z02|58fedbb8-217c-4dbc-a5dd-0aa05db33462|268435456000|94f4a2d15f92d3b77917877745ca726a
Appendix300_Full_Videos.z03|45ddcca7-0ee0-46de-bad6-88602192fcce|268435456000|ca25754a42590c6f0452a54e9acefc9b
Appendix300_Full_Videos.z04|a97390ae-438b-41fd-a0d3-44917a505a3b|268435456000|01384d017d32a20fe5c783a59dc46165
Appendix300_Full_Videos.z05|c444b1d6-f6e9-4974-a479-54075e95c06c|268435456000|b3a7425103ea255592932a1269e2d751
Appendix300_Full_Videos.zip|19c0d57a-389a-4579-b8b3-9ef5f18586e1|18145831801|9124523698214d5a7ef5d0b8822896cf
Appendix300_Images.zip|7a921473-9fff-4f29-80cd-81f9c358a9bc|251375012538|53dcf58b5e1e59a47d6b754d9b444328
Appendix300_Video_Snippets.zip|8a6fcaa0-9026-4744-9f6f-883fe6be78a0|80773037109|d8f7eacd7bddffbec63b9bfd177d7e88
archive_listing.txt|8f99986f-e0d2-4580-a3ef-075be804de3f|118045|318aa213ed0667b759d36ca5a5a8dbff
overall_merged.csv|93cb72d3-b1d5-40f0-bb46-08b6d486f3fd|83727|6daddbbd2b5dbb28d1b025963bf93ed6
readme_Appendix300.md|b10ee28b-d1a7-4a80-b110-34e6bedfa817|5467|3788f4415d7346649cc6596f3c84c902"
UA="gate-audit/1.0 (mailto:hisashi-nakano@nuhw.ac.jp)"
ts() { date '+%Y-%m-%dT%H:%M:%S%z'; }
log() { echo "$(ts) $*" >> "$LOG"; }
fsize() { stat -c %s "$1" 2>/dev/null || echo 0; }
total_bytes() { echo "$MANIFEST" | awk -F'|' '{s+=$3} END{printf "%d", s}'; }
have_bytes() {
  local s=0 n
  while IFS='|' read -r n _ _ _; do
    if [ -f "$DEST/$n" ]; then s=$((s + $(fsize "$DEST/$n"))); elif [ -f "$DEST/$n.part" ]; then s=$((s + $(fsize "$DEST/$n.part"))); fi
  done <<< "$MANIFEST"; echo "$s"
}
status() {
  echo "DS203 download status  ($(ts))   dest: $DEST"
  local done_b=0 n u sz md5 state cur
  while IFS='|' read -r n u sz md5; do
    if [ -f "$DEST/$n.verified" ]; then state="VERIFIED"; cur=$sz
    elif [ -f "$DEST/$n.md5fail" ]; then state="MD5-FAIL"; cur=$(fsize "$DEST/$n")
    elif [ -f "$DEST/$n" ]; then state="complete, verifying"; cur=$(fsize "$DEST/$n")
    elif [ -f "$DEST/$n.part" ]; then state="downloading"; cur=$(fsize "$DEST/$n.part")
    else state="pending"; cur=0; fi
    done_b=$((done_b + cur))
    awk -v n="$n" -v c="$cur" -v t="$sz" -v s="$state" 'BEGIN{printf "  %-32s %7.1f / %7.1f GB  %s\n", n, c/1e9, t/1e9, s}'
  done <<< "$MANIFEST"
  awk -v d="$done_b" -v t="$(total_bytes)" 'BEGIN{printf "  TOTAL %.1f / %.1f GB (%.1f %%)\n", d/1e9, t/1e9, 100*d/t}'
  if [ -e "$DEST/.lock" ] && ! flock -n "$DEST/.lock" true; then echo "  process: RUNNING (lock held)"; else echo "  process: not running"; fi
  echo "--- last log lines ---"; tail -n 12 "$LOG" 2>/dev/null
}
preflight() {
  mountpoint -q "$LACIE" || { echo "LaCie not mounted at $LACIE"; exit 2; }
  mkdir -p "$DEST" || exit 2
  [ "$(df --output=target "$DEST" | tail -1)" = "$LACIE" ] || { echo "DEST is not on the LaCie filesystem"; exit 2; }
  local free need have; free=$(df --output=avail -B1 "$LACIE" | tail -1); have=$(have_bytes); need=$((3 * $(total_bytes)))
  log "preflight: free=$free already=$have need(3x total)=$need"
  if [ $((free + have)) -lt "$need" ]; then log "EXIT: insufficient space"; echo "insufficient space: free+already=$((free + have)) < $need"; exit 3; fi
  curl -s -o /dev/null -w '%{http_code}' -A "$UA" -r 0-0 "$B/19c0d57a-389a-4579-b8b3-9ef5f18586e1/content" | grep -q 206 || { log "EXIT: server range check failed"; echo "server range check failed"; exit 4; }
}
fetch_one() {   # name uuid bytes md5
  local n=$1 u=$2 sz=$3 md5=$4 f="$DEST/$1" k=0 rc w
  if [ -f "$f.verified" ]; then log "$n: already verified, skip"; return 0; fi
  if [ ! -f "$f" ]; then
    log "$n: start (have $(fsize "$f.part") of $sz bytes)"
    while [ "$(fsize "$f.part")" -lt "$sz" ]; do
      curl -sS -fL -C - -A "$UA" --connect-timeout 30 --speed-limit 20000 --speed-time 300 -o "$f.part" "$B/$u/content" 2>> "$LOG"; rc=$?
      [ "$(fsize "$f.part")" -ge "$sz" ] && break
      k=$((k + 1)); w=$((30 * 2 ** (k < 5 ? k : 5))); [ $w -gt 900 ] && w=900
      log "$n: curl rc=$rc at $(fsize "$f.part")/$sz bytes; retry $k in ${w}s"; sleep "$w"
    done
    if [ "$(fsize "$f.part")" -ne "$sz" ]; then log "$n: SIZE MISMATCH $(fsize "$f.part") != $sz"; mv "$f.part" "$f.sizefail"; return 1; fi
    mv "$f.part" "$f"; log "$n: download complete ($sz bytes)"
  fi
  local got; got=$(md5sum "$f" | cut -d' ' -f1)
  if [ "$got" = "$md5" ]; then echo "$got  $n  $(ts)" > "$f.verified"; log "$n: VERIFIED md5 $got"; return 0
  else echo "expected $md5 got $got $(ts)" > "$f.md5fail"; log "$n: MD5 FAIL expected $md5 got $got (file kept)"; return 1; fi
}
case "${1:-}" in
  --status) status; exit 0 ;;
  --check) preflight; echo "preflight OK (no download)"; exit 0 ;;
esac
mkdir -p "$DEST"; exec 9> "$DEST/.lock"; flock -n 9 || { echo "another download_ds203.sh is running"; exit 5; }
preflight
log "=== run start (pid $$, PARALLEL=$PARALLEL) ==="
fails=0
while IFS='|' read -r n u sz md5; do
  while [ "$(jobs -rp | wc -l)" -ge "$PARALLEL" ]; do wait -n || fails=$((fails + 1)); done
  fetch_one "$n" "$u" "$sz" "$md5" &
done <<< "$MANIFEST"
while [ "$(jobs -rp | wc -l)" -gt 0 ]; do wait -n || fails=$((fails + 1)); done
log "=== run end: failures=$fails ==="
status >> "$LOG"
[ "$fails" -eq 0 ]
