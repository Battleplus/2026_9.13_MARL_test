#!/usr/bin/env bash
set -euo pipefail

# Install StarCraft II 4.10 and SMAC maps without assuming a pymarl checkout.
# Usage: bash scripts/install_sc2.sh [--sc2-root PATH] [--download-dir PATH]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SC2_ROOT="${SC2_ROOT:-$REPO_ROOT/third_party/StarCraftII}"
DOWNLOAD_DIR="${DOWNLOAD_DIR:-$REPO_ROOT/third_party/downloads}"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --sc2-root) SC2_ROOT="$2"; shift 2 ;;
        --download-dir) DOWNLOAD_DIR="$2"; shift 2 ;;
        -h|--help)
            echo "usage: $0 [--sc2-root PATH] [--download-dir PATH]"
            exit 0
            ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done

mkdir -p "$DOWNLOAD_DIR" "$(dirname "$SC2_ROOT")"
export SC2PATH="$SC2_ROOT"

if [[ ! -x "$SC2_ROOT/SC2_x64" ]]; then
    archive="$DOWNLOAD_DIR/SC2.4.10.zip"
    [[ -f "$archive" ]] || curl -fL --retry 3 -o "$archive" \
        http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.10.zip
    tmp_dir="$(mktemp -d)"
    trap 'rm -rf "$tmp_dir"' EXIT
    unzip -q -P iagreetotheeula "$archive" -d "$tmp_dir"
    if [[ -d "$tmp_dir/StarCraftII" ]]; then
        mv "$tmp_dir/StarCraftII" "$SC2_ROOT"
    else
        echo "SC2 archive did not contain StarCraftII/" >&2
        exit 1
    fi
fi

map_archive="$DOWNLOAD_DIR/SMAC_Maps.zip"
[[ -f "$map_archive" ]] || curl -fL --retry 3 -o "$map_archive" \
    https://github.com/oxwhirl/smac/releases/download/v0.1-beta1/SMAC_Maps.zip
mkdir -p "$SC2_ROOT/Maps"
unzip -q -o "$map_archive" -d "$DOWNLOAD_DIR"
if [[ -d "$DOWNLOAD_DIR/SMAC_Maps" ]]; then
    rm -rf "$SC2_ROOT/Maps/SMAC_Maps"
    mv "$DOWNLOAD_DIR/SMAC_Maps" "$SC2_ROOT/Maps/SMAC_Maps"
fi

echo "SC2PATH=$SC2PATH"
echo "StarCraft II 4.10 and SMAC maps are ready."
