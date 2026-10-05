#!/usr/bin/env bash
# §14 steps 4-5 unattended runner (orchestration only): staging -> 4a mask check -> 4b extraction (four arms) ->
# step-4 records + automatic records-only commit -> step 5 (E1-E3, probes, reporting paths; not committed).
# Never runs any part of §14 step 6. All computation is the locked ss_benchmark.pipeline CLI, run from a code snapshot
# of the launch commit; sequencing, provenance checks, records and logging are in scripts/step4_5_orchestrate.py.
#
#   launch / resume (detached; survives closing the terminal):
#     setsid nohup scripts/run_step4_5.sh --expect-commit <SHA> > /dev/null 2>&1 < /dev/null &
#   progress counts and resource readings only:
#     scripts/run_step4_5.sh --status
#
# Refuses to start or resume unless the provenance checks pass (HEAD == --expect-commit and a clean tree at launch;
# after the step-4 commit: HEAD == that commit, its parent == the launch commit, its diff records-only, tree clean)
# and the run lock ($OUT/runner.lock) is free. Options (defaults are the real run): --out DIR, --archive-zip FILE,
# --weights DIR.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY=/home/user/.venvs/ss_extract/bin/python
OUT=/media/user/LaCie/medvideo_gate/ss_step4_5
ARCHIVE=/media/user/LaCie/medvideo_gate/DS203/archive/Appendix300_Full_Videos.zip
WEIGHTS=/media/user/LaCie/medvideo_gate/weights
EXPECT=""
MODE=run
while [[ $# -gt 0 ]]; do
  case "$1" in
    --expect-commit) EXPECT="$2"; shift 2 ;;
    --status) MODE=status; shift ;;
    --out) OUT="$2"; shift 2 ;;
    --archive-zip) ARCHIVE="$2"; shift 2 ;;
    --weights) WEIGHTS="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 64 ;;
  esac
done

if [[ $MODE == status ]]; then
  exec "$PY" "$REPO/scripts/step4_5_orchestrate.py" status --out "$OUT"
fi

refuse() { echo "$(date -Is) refused: $*" >&2; exit 3; }
[[ -n $EXPECT ]] || refuse "--expect-commit is required"
EXP="$(git -C "$REPO" rev-parse --verify --quiet "${EXPECT}^{commit}")" || refuse "unknown commit $EXPECT"
[[ "$(git -C "$REPO" rev-parse --verify --quiet HEAD:scripts/run_step4_5.sh)" == \
   "$(git -C "$REPO" hash-object "${BASH_SOURCE[0]}")" ]] || refuse "this script is not the one in HEAD"

mkdir -p "$OUT/logs"
exec 9>"$OUT/runner.lock"
flock -n 9 || refuse "another runner holds $OUT/runner.lock"
cd "$REPO"
export PYTHONDONTWRITEBYTECODE=1
exec "$PY" "$REPO/scripts/step4_5_orchestrate.py" run --repo "$REPO" --expect-commit "$EXP" --out "$OUT" \
  --archive-zip "$ARCHIVE" --weights "$WEIGHTS" >> "$OUT/logs/runner_stdout.log" 2>&1
