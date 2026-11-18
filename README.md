# HTTP/3 vs HTTP/2 Performance Comparison

ZJU Computer Networks final project (自主创新类).

**Question:** Does HTTP/3 (QUIC over UDP) load pages faster than HTTP/2 (TCP + TLS), and under which network conditions?

## Team

| Role | Person | Owns |
| --- | --- | --- |
| A · Server | Genevie | Caddy testbed, test pages, live demo |
| B · Automation | ___ | netem, measurement script, running experiments |
| C · Analysis | ___ | Campus measurements, charts, report and slides lead |

## Folder layout

```
server/     Testbed: Caddyfile, setup and run scripts, test page generator   (A)
scripts/    netem helper, measurement, experiment runner, analysis, demo      (B, C)
data/       results.csv (lab), real_results.csv (campus), figures/            (B, C)
report/     Report outline and drafts                                          (all)
```

Generated files (certificates, test pages, the Python venv) live in `~/h3proj/` on each VM and are **not** committed.

## Quick start

### A · Server (on the Ubuntu VM)

```bash
bash server/setup_server.sh     # once: installs Caddy, makes cert + test pages in ~/h3proj
bash server/run_server.sh       # every time: serves https://localhost:8443 (HTTP/2 + HTTP/3)
```

### B · Automation (on the Ubuntu VM, with the server running in another terminal)

```bash
bash server/setup_server.sh     # same server on your own VM
bash scripts/setup_client.sh    # once: venv + Playwright + Chromium
source ~/h3proj/.venv/bin/activate
python3 scripts/measure.py --rtt 0 --loss 0 --runs 1 --out data/test.csv   # sanity check: h3 rows must say h3
bash scripts/run_all.sh         # full matrix -> data/results.csv (takes hours)
```

netem helper: `bash scripts/netem.sh set 100 3` (RTT 100 ms, 3% loss), `bash scripts/netem.sh reset`.

### C · Analysis (on a laptop; Windows is fine)

```bash
pip install playwright pandas matplotlib
python -m playwright install chromium
python scripts/measure_real.py --location dorm-wifi --sites site1.com site2.com site3.com site4.com site5.com --out data/real_results.csv
python scripts/analyze.py data/results.csv data/figures
```

### Demo (A, on the VM)

```bash
bash scripts/start_demo.sh      # two windows: HTTP/2 left, HTTP/3 right
bash scripts/netem.sh set 100 3 # make the network worse, then reload both
bash scripts/netem.sh reset
```

## Rules

- Never rename the CSV columns: `analyze.py` reads them by name.
- Never commit `*.pem` keys or the venv (see `.gitignore`).
- Stress-test only our own server. Real sites: 10 loads per site, normal browsing volume.
