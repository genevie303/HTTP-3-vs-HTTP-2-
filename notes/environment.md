# Environment and versions

Fill this in once the testbed works. It goes into report section 3.

## Testbed VM (A)

- Ubuntu version (`lsb_release -a`): Ubuntu 26.04.1 LTS (kernel 7.0.0-34-generic)
- CPUs (`nproc`): 4
- RAM (`free -h`): 3.3 GiB
- Caddy version (`caddy version`): v2.11.9
- Python version: 3.14 (venv in ~/h3proj/.venv)
- Playwright version (`pip show playwright`): 1.65.x — confirm with `pip show playwright`
- Chromium (Chrome for Testing, installed by Playwright): 159.0.8154.6

### Setup notes

- The VM clock was wrong (Sep 29) after a saved state; fixed with `sudo date -u -s ...`. Shut the VM down with `sudo shutdown now`, not "Save state".
- pypi.org timed out from campus; the Tsinghua mirror works (now the default in `scripts/setup_client.sh`).
- Caddy needed `auto_https disable_redirects`, otherwise it tries to open port 80 and fails without root.

### First sanity check (2026-11-18, no netem, 1 run)

| Page | Protocol | proto_got | connect_ms | load_ms | done_ms |
| --- | --- | --- | --- | --- | --- |
| small.html | h2 | h2 | 6.1 | 247.5 | |
| small.html | h3 | h3 | 8.1 | 311.2 | |
| big.html | h2 | h2 | 5.4 | 47.4 | 219.9 |
| big.html | h3 | h3 | 7.2 | 64.1 | 260.0 |

One run only, so no conclusions yet. On a perfect network HTTP/3 was slightly slower, which fits QUIC running in user space (more CPU per packet). The interesting part is what happens once loss and delay are added.

## Measurement VM (B)

- Ubuntu version:
- CPUs / RAM:
- Python version (`python3 --version`):
- Playwright version (`pip show playwright`):
- Chromium version (printed by Playwright, or `chrome://version` in the demo window):

## Campus laptop (C)

- OS:
- Python and Playwright versions:
