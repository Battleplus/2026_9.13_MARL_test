#!/usr/bin/env bash
set -euo pipefail

# Reproducible entry point for the upstream reward trainer. This wrapper keeps
# the unlicensed upstream source in its submodule and supplies all local paths.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MAPT_ROOT="$REPO_ROOT/upstream/MAPT"
DATASET_PATH="${DATASET_PATH:-$REPO_ROOT/data/smac/3m_replaybuffer_5w_len16_diff0.5/preference_pair_data.pkl}"

export PYTHONPATH="$MAPT_ROOT${PYTHONPATH:+:$PYTHONPATH}"
exec python "$MAPT_ROOT/mat/scripts/train_reward/train_reward_model.py" \
    --dataset_path "$DATASET_PATH" \
    "$@"
