#!/usr/bin/env bash
set -euo pipefail

# Reproducible entry point for upstream SMAC policy training.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MAPT_ROOT="$REPO_ROOT/upstream/MAPT"
PREFERENCE_MODEL_DIR="${PREFERENCE_MODEL_DIR:-$REPO_ROOT/results/pref_reward/smac/3m/MultiPrefTransformerDivide/reward_model_15.pt}"

export PYTHONPATH="$MAPT_ROOT${PYTHONPATH:+:$PYTHONPATH}"
exec python "$MAPT_ROOT/mat/scripts/train_policy/train_smac.py" \
    --preference_model_dir "$PREFERENCE_MODEL_DIR" \
    --log_interval 5 \
    "$@"
