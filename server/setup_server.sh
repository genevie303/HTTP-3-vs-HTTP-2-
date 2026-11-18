#!/usr/bin/env bash
# Builds the HTTP/2 + HTTP/3 testbed in ~/h3proj (Step 1 of the team guide).
# Safe to run more than once: existing certificate and images are kept.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$HOME/h3proj"

echo "==> 1/5 Installing Caddy, ImageMagick and OpenSSL"
if ! command -v caddy >/dev/null 2>&1; then
  sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl gnupg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
    | sudo gpg --dearmor --yes -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
    | sudo tee /etc/apt/sources.list.d/caddy-stable.list >/dev/null
  sudo apt update
  sudo apt install -y caddy
  sudo systemctl disable --now caddy || true
fi
sudo apt install -y imagemagick openssl python3 python3-venv
caddy version

echo "==> 2/5 Raising UDP buffers for QUIC"
sudo sysctl -w net.core.rmem_max=7500000 net.core.wmem_max=7500000

echo "==> 3/5 Creating certificate and SPKI hash"
mkdir -p "$RUN_DIR/certs"
if [ ! -f "$RUN_DIR/certs/cert.pem" ]; then
  openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes \
    -keyout "$RUN_DIR/certs/key.pem" -out "$RUN_DIR/certs/cert.pem" -days 90 \
    -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
fi
openssl x509 -pubkey -noout -in "$RUN_DIR/certs/cert.pem" \
  | openssl pkey -pubin -outform der \
  | openssl dgst -sha256 -binary | base64 > "$RUN_DIR/spki.txt"
echo "SPKI hash: $(cat "$RUN_DIR/spki.txt")"

echo "==> 4/5 Building test pages"
mkdir -p "$RUN_DIR/site/img"
for i in $(seq 1 50); do
  [ -f "$RUN_DIR/site/img/$i.jpg" ] || convert -size 200x200 plasma: "$RUN_DIR/site/img/$i.jpg"
done
[ -f "$RUN_DIR/site/big.bin" ] || head -c 5M /dev/urandom > "$RUN_DIR/site/big.bin"
python3 "$REPO_DIR/server/make_pages.py" "$RUN_DIR/site"

echo "==> 5/5 Installing Caddyfile"
cp "$REPO_DIR/server/Caddyfile" "$RUN_DIR/Caddyfile"

echo
echo "Done. Start the server with:  bash server/run_server.sh"
