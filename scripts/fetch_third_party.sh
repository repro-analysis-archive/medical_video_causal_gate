#!/usr/bin/env bash
# Recreate third_party/ (code only) for the secondary-model adapters at the pinned commits used at code lock.
# Weight-type files shipped inside these repositories (FVD I3D networks, LPIPS VGG linear layers) are deleted after
# checkout, as are .git and __pycache__ directories; no model weights are kept.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TP="$REPO/third_party"
mkdir -p "$TP"
while read -r name url commit; do
  [[ -z "$name" ]] && continue
  if [[ -d "$TP/$name" ]]; then echo "exists: $name"; continue; fi
  git init -q "$TP/$name"
  git -C "$TP/$name" fetch -q --depth 1 "$url" "$commit"
  git -C "$TP/$name" checkout -q FETCH_HEAD
  rm -rf "$TP/$name/.git"
  echo "$name $commit"
done <<'LIST'
OmniTokenizer https://github.com/FoundationVision/OmniTokenizer.git 701b619003b3e941e769269c7626dbf111d0377e
WF-VAE https://github.com/PKU-YuanGroup/WF-VAE.git d858bee85324341388f2dd1a51a9bd76a4cda4e2
LARP https://github.com/hywang66/LARP.git 8aaed63354c8c0fabcb8a86a2e31c34320e6db86
LeanVAE https://github.com/westlake-repl/LeanVAE.git 62f7c7d560b83f408b5041f799d70317d9b37713
LIST
find "$TP" -type f \( -name "*.pt" -o -name "*.pth" -o -name "*.ckpt" -o -name "*.safetensors" -o -name "*.bin" \
     -o -name "*.pkl" -o -name "*.npz" -o -name "*.onnx" -o -name "*.h5" \) -print -delete
find "$TP" -type d -name "__pycache__" -prune -exec rm -rf {} +
