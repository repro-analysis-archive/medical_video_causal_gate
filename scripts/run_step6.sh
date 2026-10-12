#!/usr/bin/env bash
# §14 step 6 unattended runner (orchestration only): the locked causal grid (ss_benchmark.grid_driver, real design,
# primary set + §10.3 sensitivity sets), run unit by unit with the code-lock thread settings. Never runs §14 step 7
# (aggregation, family verdicts). Sequencing, preconditions, memory guard and logging: scripts/step6_orchestrate.py.
#
#   launch / resume (detached; survives closing the terminal):
#     setsid nohup scripts/run_step6.sh --expect-commit <SHA> > /dev/null 2>&1 < /dev/null &
#   progress counts and resource readings only:   scripts/run_step6.sh --status
#   stop on request (resumable):                   scripts/run_step6.sh --stop
#
# Refuses to start or resume (exit 3, nothing changed) unless HEAD == --expect-commit, the tree is clean, the step-5
# and §13 records are committed, ss_benchmark is the SDR commit af56777 (CODELOCK_CORRECTION_001 adapter excepted)
# and the reps file matches the committed step-5 manifest. Options (defaults are the real run): --out DIR,
# --reps FILE, --workers N (default 18), --cpus LIST; smoke tests only: --placeholder --cells LIST --max-reps M.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY=/home/user/miniconda3/bin/python3
OUT=/media/user/LaCie/medvideo_gate/ss_step6
REPS=/media/user/LaCie/medvideo_gate/ss_step4_5/step5/reps.npz
WORKERS=18
EXPECT=""
MODE=run
EXTRA=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --expect-commit) EXPECT="$2"; shift 2 ;;
    --status) MODE=status; shift ;;
    --stop) MODE=stop; shift ;;
    --out) OUT="$2"; shift 2 ;;
    --reps) REPS="$2"; shift 2 ;;
    --workers) WORKERS="$2"; shift 2 ;;
    --cpus) EXTRA+=(--cpus "$2"); shift 2 ;;
    --placeholder) EXTRA+=(--placeholder); shift ;;
    --cells) EXTRA+=(--cells "$2"); shift 2 ;;
    --max-reps) EXTRA+=(--max-reps "$2"); shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 64 ;;
  esac
done

if [[ $MODE == status ]]; then
  exec "$PY" "$REPO/scripts/step6_orchestrate.py" status --out "$OUT"
fi
if [[ $MODE == stop ]]; then
  PID="$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1])).get("pid", ""))' "$OUT/state.json" 2>/dev/null || true)"
  if [[ -n $PID ]] && grep -q step6_orchestrate "/proc/$PID/cmdline" 2>/dev/null; then
    kill -TERM "$PID"; echo "stop requested (pid $PID); resumable with the same launch command"
  else
    echo "no running step-6 runner for $OUT"
  fi
  exit 0
fi

refuse() { echo "$(date -Is) refused: $*" >&2; exit 3; }
[[ -n $EXPECT ]] || refuse "--expect-commit is required"
export GIT_OPTIONAL_LOCKS=0
EXP="$(git -C "$REPO" rev-parse --verify --quiet "${EXPECT}^{commit}")" || refuse "unknown commit $EXPECT"
[[ "$(git -C "$REPO" rev-parse --verify --quiet HEAD:scripts/run_step6.sh)" == \
   "$(git -C "$REPO" hash-object "${BASH_SOURCE[0]}")" ]] || refuse "this script is not the one in HEAD"

mkdir -p "$OUT/logs"
exec 9>"$OUT/runner.lock"
flock -n 9 || refuse "another runner holds $OUT/runner.lock"
cd "$REPO"
export PYTHONDONTWRITEBYTECODE=1
exec "$PY" "$REPO/scripts/step6_orchestrate.py" run --repo "$REPO" --expect-commit "$EXP" --out "$OUT" \
  --reps "$REPS" --workers "$WORKERS" "${EXTRA[@]}" >> "$OUT/logs/runner_stdout.log" 2>&1
