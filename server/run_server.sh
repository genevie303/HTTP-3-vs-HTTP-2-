#!/usr/bin/env bash
# Starts the testbed at https://localhost:8443 (HTTP/2 over TCP and HTTP/3 over UDP).
# Leave this terminal open; stop with Ctrl+C.
set -euo pipefail

if [ ! -f "$HOME/h3proj/Caddyfile" ]; then
  echo "~/h3proj/Caddyfile not found. Run: bash server/setup_server.sh" >&2
  exit 1
fi

# UDP buffers reset on every reboot, so set them each time.
sudo sysctl -w net.core.rmem_max=7500000 net.core.wmem_max=7500000 >/dev/null

cd "$HOME/h3proj"
exec caddy run --config Caddyfile --adapter caddyfile
