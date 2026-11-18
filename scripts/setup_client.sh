#!/usr/bin/env bash
# Creates ~/h3proj/.venv with Playwright, pandas and matplotlib, and downloads Chromium.
# pypi.org often times out from campus, so the Tsinghua mirror is the default.
# To use another index:  PIP_INDEX_URL=https://pypi.org/simple bash scripts/setup_client.sh
set -euo pipefail

export PIP_INDEX_URL="${PIP_INDEX_URL:-https://pypi.tuna.tsinghua.edu.cn/simple}"

mkdir -p "$HOME/h3proj"
python3 -m venv "$HOME/h3proj/.venv"
# shellcheck disable=SC1091
source "$HOME/h3proj/.venv/bin/activate"
pip install --upgrade pip
pip install playwright pandas matplotlib
python3 -m playwright install --with-deps chromium

echo
echo "Done. Activate the venv in each new terminal with:  source ~/h3proj/.venv/bin/activate"
