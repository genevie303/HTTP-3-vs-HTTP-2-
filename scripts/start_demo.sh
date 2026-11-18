#!/usr/bin/env bash
# Opens two Chromium windows side by side for the live demo (Step 6):
# left = HTTP/2, right = HTTP/3, both loading grid.html.
# Needs: server running (bash server/run_server.sh) and scripts/setup_client.sh done.
set -euo pipefail

# shellcheck disable=SC1091
source "$HOME/h3proj/.venv/bin/activate"
CHROME="$(python3 -c 'from playwright.sync_api import sync_playwright as s; p = s().start(); print(p.chromium.executable_path); p.stop()')"
SPKI="$(cat "$HOME/h3proj/spki.txt")"
BASE="https://localhost:8443/grid.html"

rm -rf /tmp/demo-h2 /tmp/demo-h3

"$CHROME" --user-data-dir=/tmp/demo-h2 --window-position=0,0 --window-size=800,900 \
  --disable-quic --ignore-certificate-errors-spki-list="$SPKI" \
  "$BASE?label=HTTP/2" >/dev/null 2>&1 &

"$CHROME" --user-data-dir=/tmp/demo-h3 --window-position=810,0 --window-size=800,900 \
  --enable-quic --origin-to-force-quic-on=localhost:8443 --ignore-certificate-errors-spki-list="$SPKI" \
  "$BASE?label=HTTP/3" >/dev/null 2>&1 &

echo "Left window: HTTP/2. Right window: HTTP/3."
echo "Check each window's DevTools > Network > Protocol column once (h2 / h3)."
echo "Then: bash scripts/netem.sh set 100 3   and reload both windows together."
