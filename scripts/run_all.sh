#!/usr/bin/env bash
# Runs the full experiment matrix (Step 4): 3 RTTs x 4 loss rates x 2 pages x 2 protocols x 10 runs.
# Start the server first in another terminal:  bash server/run_server.sh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$REPO_DIR/data/results.csv"
# shellcheck disable=SC1091
source "$HOME/h3proj/.venv/bin/activate"

# Ask for sudo once, then keep it alive for the whole (long) run.
sudo -v
while true; do sudo -n true; sleep 60; done 2>/dev/null &
KEEP=$!
trap 'bash "$REPO_DIR/scripts/netem.sh" reset; kill "$KEEP" 2>/dev/null || true' EXIT

for rtt in 20 100 300; do
  for loss in 0 1 3 5; do
    bash "$REPO_DIR/scripts/netem.sh" set "$rtt" "$loss"
    python3 "$REPO_DIR/scripts/measure.py" --rtt "$rtt" --loss "$loss" --runs 10 --out "$OUT"
  done
done

echo "All conditions done. Results: $OUT"
