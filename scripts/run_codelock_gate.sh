#!/usr/bin/env bash
# Code-lock Part B runner (SS protocol DS203 §14 step 2): (a) estimator gate on the PLACEHOLDER design, (b) compute-
# budget projection, (c) G-SITE record (real design metadata), (d) machine-readable pass/fail record.
#
#   scripts/run_codelock_gate.sh --expect-commit <hash> [--smoke] [--workers N] [--out DIR]   run / resume
#   scripts/run_codelock_gate.sh --status [--smoke] [--out DIR]                                progress only
#
# Executes exactly the committed code: it refuses to run unless HEAD equals --expect-commit and no tracked file is
# modified, then runs Python from a `git archive` snapshot of that commit inside the run directory, so later edits of
# the working tree cannot affect a running or resumed run. Detached use (survives closing the terminal):
#   setsid nohup scripts/run_codelock_gate.sh --expect-commit <hash> > /dev/null 2>&1 < /dev/null &
# Re-running the same command resumes (finished units are skipped). All output goes to <out>/runner.log and
# <out>/progress.log. --status reports progress without showing any estimate or verdict.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY=/home/user/miniconda3/bin/python3
EXPECT=""; SMOKE=0; STATUS=0; WORKERS="$(nproc)"; OUT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --expect-commit) EXPECT="$2"; shift 2;;
    --smoke) SMOKE=1; shift;;
    --status) STATUS=1; shift;;
    --workers) WORKERS="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    *) echo "unknown argument: $1" >&2; exit 2;;
  esac
done
if [[ -z "$OUT" ]]; then
  if [[ $SMOKE -eq 1 ]]; then OUT="$REPO/results/codelock_gate_SMOKE"; else OUT="$REPO/results/codelock_gate"; fi
fi

export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
       NUMEXPR_NUM_THREADS=1

if [[ $STATUS -eq 1 ]]; then
  SNAP="$OUT/code_snapshot"
  if [[ -d "$SNAP/ss_benchmark" ]]; then CODE="$SNAP"; else CODE="$REPO"; fi
  cd "$CODE" && exec "$PY" -m ss_benchmark.codelock_gate --out "$OUT" --status
fi

[[ -n "$EXPECT" ]] || { echo "--expect-commit <hash> is required" >&2; exit 2; }
cd "$REPO"
HEAD="$(git rev-parse HEAD)"
FULL="$(git rev-parse --verify "$EXPECT^{commit}")"
[[ "$HEAD" == "$FULL" ]] || { echo "HEAD $HEAD != expected $FULL" >&2; exit 3; }
git diff --quiet HEAD -- || { echo "tracked files modified; refusing to run" >&2; exit 3; }

mkdir -p "$OUT"
exec 9>"$OUT/.lock"
flock -n 9 || { echo "another runner holds $OUT/.lock" >&2; exit 4; }
LOG="$OUT/runner.log"
SNAP="$OUT/code_snapshot"
if [[ -f "$SNAP/COMMIT" && "$(cat "$SNAP/COMMIT")" != "$FULL" ]]; then
  echo "existing snapshot is of a different commit" >&2; exit 3
fi
if [[ ! -f "$SNAP/COMMIT" ]]; then
  rm -rf "$SNAP"; mkdir -p "$SNAP"
  git archive "$FULL" ss_benchmark scripts data_audit/lead/out/DS203_d8_cases.csv \
      data_audit/lead/out/ss_window_offsets.csv data_audit/lead/out/ss_window_offsets_perW.csv | tar -x -C "$SNAP"
  echo "$FULL" > "$SNAP/COMMIT"
fi
echo "$$ $(date '+%F %T %z')" > "$OUT/runner.pid"
ARGS=(--out "$OUT" --workers "$WORKERS")
[[ $SMOKE -eq 1 ]] && ARGS+=(--smoke)
echo "=== $(date '+%F %T %z') runner start: commit $FULL, workers $WORKERS, smoke $SMOKE, pid $$" >> "$LOG"
cd "$SNAP"
set +e
SS_CODE_COMMIT="$FULL" SS_CODE_SNAPSHOT="$SNAP" "$PY" -m ss_benchmark.codelock_gate "${ARGS[@]}" >> "$LOG" 2>&1
RC=$?
set -e
echo "=== $(date '+%F %T %z') runner finished (exit $RC)" >> "$LOG"
exit $RC
