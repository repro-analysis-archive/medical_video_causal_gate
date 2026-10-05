#!/usr/bin/env bash
# Retrieve the third-party SOURCE code used by the secondary-model adapters, at the pinned commits (code only).
#
# PROHIBITED before the final code-lock commit (decisions/CODELOCK_INCIDENT_001_third_party_weight_files.md): the
# script refuses to run unless --after-final-code-lock is given. third_party/ as used at code lock already exists.
#
# Mechanism (incident prevention; no "download then strip"): a depth-1 partial fetch of the pinned commit with
# --filter=blob:none, then a non-cone sparse checkout whose patterns exclude every weight-type file, so the blobs of
# excluded files are never fetched or written. After checkout, `git rev-list --missing=print` (which does not fetch)
# must show every weight-type blob of the commit as missing, and no weight-type file may exist in the tree; otherwise
# the script aborts and deletes the directory.
#
#   scripts/fetch_third_party.sh --after-final-code-lock [--dest DIR] [--list FILE]
#   (--list: lines "name url commit"; default: the four repositories below)
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$REPO/third_party"; LIST=""; OK=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --after-final-code-lock) OK=1; shift;;
    --dest) DEST="$2"; shift 2;;
    --list) LIST="$2"; shift 2;;
    *) echo "unknown argument: $1" >&2; exit 2;;
  esac
done
[[ $OK -eq 1 ]] || { echo "refused: third-party retrieval is prohibited before the final code-lock commit" >&2; exit 2; }
WEIGHT_GLOBS=('*.pt' '*.pth' '*.ckpt' '*.safetensors' '*.bin' '*.pkl' '*.pickle' '*.npz' '*.npy' '*.onnx' '*.h5' \
              '*.hdf5' '*.tar' '*.torch' '*.pb' '*.tflite' '*.msgpack' '*.zip' '*.gz')
DEFAULT_LIST="OmniTokenizer https://github.com/FoundationVision/OmniTokenizer.git 701b619003b3e941e769269c7626dbf111d0377e
WF-VAE https://github.com/PKU-YuanGroup/WF-VAE.git d858bee85324341388f2dd1a51a9bd76a4cda4e2
LARP https://github.com/hywang66/LARP.git 8aaed63354c8c0fabcb8a86a2e31c34320e6db86
LeanVAE https://github.com/westlake-repl/LeanVAE.git 62f7c7d560b83f408b5041f799d70317d9b37713"

is_weight() {  # path -> 0 if it matches a weight glob
  local f; f="$(basename "$1")"
  for g in "${WEIGHT_GLOBS[@]}"; do [[ "$f" == $g ]] && return 0; done
  return 1
}

fetch_one() {
  local name="$1" url="$2" commit="$3" d="$DEST/$1"
  if [[ -e "$d" ]]; then echo "exists, skipped: $name"; return 0; fi
  git init -q "$d"
  git -C "$d" config core.repositoryformatversion 1
  git -C "$d" config extensions.partialClone origin
  git -C "$d" remote add origin "$url"
  git -C "$d" config remote.origin.promisor true
  git -C "$d" config remote.origin.partialclonefilter blob:none
  git -C "$d" config core.sparseCheckout true
  { echo '/*'; for g in "${WEIGHT_GLOBS[@]}"; do echo "!$g"; done; } > "$d/.git/info/sparse-checkout"
  git -C "$d" fetch -q --depth 1 --filter=blob:none origin "$commit"
  git -C "$d" checkout -q FETCH_HEAD
  local missing n_weight=0 bad=0
  missing="$(git -C "$d" rev-list --objects --missing=print FETCH_HEAD | sed -n 's/^?//p')"
  while read -r mode type sha path; do
    [[ "$type" == blob ]] || continue
    if is_weight "$path"; then
      n_weight=$((n_weight + 1))
      grep -qx "$sha" <<< "$missing" || { echo "weight blob present: $path" >&2; bad=1; }
    fi
  done < <(git -C "$d" ls-tree -r FETCH_HEAD)
  while IFS= read -r f; do is_weight "$f" && { echo "weight file in tree: $f" >&2; bad=1; }; done \
    < <(find "$d" -path "$d/.git" -prune -o -type f -print)
  if [[ $bad -ne 0 ]]; then rm -rf "$d"; echo "ABORTED: $name" >&2; return 1; fi
  rm -rf "$d/.git"
  find "$d" -type d -name "__pycache__" -prune -exec rm -rf {} +
  echo "$name $commit: checked out without weight blobs ($n_weight weight-type paths in the commit, all unfetched)"
}

mkdir -p "$DEST"
while read -r name url commit; do
  [[ -z "${name:-}" ]] && continue
  fetch_one "$name" "$url" "$commit"
done <<< "$(if [[ -n "$LIST" ]]; then cat "$LIST"; else echo "$DEFAULT_LIST"; fi)"
