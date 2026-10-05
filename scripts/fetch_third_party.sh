#!/usr/bin/env bash
# Retrieve the third-party SOURCE code used by the secondary-model adapters, at the pinned commits (code only).
#
# PROHIBITED before the final code-lock commit (decisions/CODELOCK_INCIDENT_001_third_party_weight_files.md): the
# script refuses to run unless --after-final-code-lock is given. third_party/ as used at code lock already exists.
#
# Single authorised exception (decisions/CODELOCK_AUTH_002_videomae_source.md): --authorized-videomae-source fetches
# exactly the two VideoMAE architecture source files listed in VIDEOMAE_FILES, as raw files from
# raw.githubusercontent.com at the pinned commit (no clone, no archive, no LFS), into third_party/VideoMAE/; only *.py
# names on that list, at most 1 MB each, no NUL bytes, SHA-256 equal to the recorded values.
#
# Mechanism (incident prevention; no "download then strip"): a depth-1 partial fetch of the pinned commit with
# --filter=blob:none, then a non-cone sparse checkout whose patterns exclude every weight-type file, so the blobs of
# excluded files are never fetched or written. After checkout, `git rev-list --missing=print` (which does not fetch)
# must show every weight-type blob of the commit as missing, and no weight-type file may exist in the tree; otherwise
# the script aborts and deletes the directory.
#
#   scripts/fetch_third_party.sh --after-final-code-lock [--dest DIR] [--list FILE]
#   scripts/fetch_third_party.sh --authorized-videomae-source [--dest DIR]
#   (--list: lines "name url commit"; default: the four repositories below)
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$REPO/third_party"; LIST=""; OK=0; VMAE=0
VIDEOMAE_REPO="MCG-NJU/VideoMAE"
VIDEOMAE_COMMIT="14ef8d856287c94ef1f985fe30f958eb4ec2c55d"
VIDEOMAE_FILES=("modeling_pretrain.py" "modeling_finetune.py")
declare -A VIDEOMAE_SHA256=([modeling_pretrain.py]=5689f93f72d7764d13e27f17ca3a6a096c89e7ee0e3fd8e63dffde6ab11ad593 [modeling_finetune.py]=ce9a11ff05c7a1b5085addf6c73b71ffb68933564164f7b250dedad91f6e29b8)  # CODELOCK_AUTH_002
while [[ $# -gt 0 ]]; do
  case "$1" in
    --authorized-videomae-source) VMAE=1; shift;;
    --after-final-code-lock) OK=1; shift;;
    --dest) DEST="$2"; shift 2;;
    --list) LIST="$2"; shift 2;;
    *) echo "unknown argument: $1" >&2; exit 2;;
  esac
done
if [[ $VMAE -eq 1 ]]; then
  [[ $OK -eq 0 && -z "$LIST" ]] || { echo "--authorized-videomae-source cannot be combined" >&2; exit 2; }
  d="$DEST/VideoMAE"; mkdir -p "$d"
  for f in "${VIDEOMAE_FILES[@]}"; do
    [[ "$f" == *.py && "$f" != */* ]] || { echo "refused: $f" >&2; exit 2; }
    url="https://raw.githubusercontent.com/$VIDEOMAE_REPO/$VIDEOMAE_COMMIT/$f"
    curl -fsSL --max-filesize 1048576 -o "$d/$f.part" "$url"
    if LC_ALL=C grep -qaP '\x00' "$d/$f.part"; then rm -f "$d/$f.part"; echo "binary content refused: $f" >&2; exit 3; fi
    sha="$(sha256sum "$d/$f.part" | cut -d' ' -f1)"
    if [[ -n "${VIDEOMAE_SHA256[$f]:-}" && "${VIDEOMAE_SHA256[$f]}" != "$sha" ]]; then
      rm -f "$d/$f.part"; echo "sha256 mismatch: $f" >&2; exit 3
    fi
    mv "$d/$f.part" "$d/$f"
    echo "$VIDEOMAE_REPO@$VIDEOMAE_COMMIT/$f $(stat -c %s "$d/$f") bytes sha256 $sha"
  done
  exit 0
fi
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
