#!/usr/bin/env bash
# Creates ~/h3proj/.venv with Playwright, pandas and matplotlib, and downloads Chromium.
set -euo pipefail

mkdir -p "$HOME/h3proj"
python3 -m venv "$HOME/h3proj/.venv"
# shellcheck disable=SC1091
source "$HOME/h3proj/.venv/bin/activate"
pip install --upgrade pip
pip install playwright pandas matplotlib
python3 -m playwright install --with-deps chromium

echo
echo "Done. Activate the venv in each new terminal with:  source ~/h3proj/.venv/bin/activate"
