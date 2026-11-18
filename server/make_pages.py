#!/usr/bin/env python3
"""Write the three test pages into the site folder given as the first argument.

small.html  50 small images              -> many-small-files workload
big.html    one 5 MB download via fetch   -> single-large-file workload (sets window.done)
grid.html   200 tiles + a big label       -> live demo; label comes from ?label=...
"""
import sys
from pathlib import Path

site = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / "h3proj" / "site")
site.mkdir(parents=True, exist_ok=True)

small_imgs = "".join(f'<img src="img/{i}.jpg" width="100">' for i in range(1, 51))
(site / "small.html").write_text(
    f"<!doctype html><meta charset=\"utf-8\"><title>small</title>{small_imgs}\n"
)

(site / "big.html").write_text(
    "<!doctype html><meta charset=\"utf-8\"><title>big</title>\n"
    "<script>fetch('big.bin', {cache: 'no-store'})"
    ".then(r => r.arrayBuffer())"
    ".then(() => { window.done = performance.now(); });</script>\n"
)

grid_imgs = "".join(f'<img src="img/{i % 50 + 1}.jpg?v={i}" width="60" height="60">' for i in range(200))
(site / "grid.html").write_text(
    "<!doctype html><meta charset=\"utf-8\"><title>grid</title>\n"
    "<style>body{margin:8px;font-family:sans-serif}h1{margin:0 0 8px;font-size:40px}"
    "img{display:inline-block;margin:1px;background:#ddd}</style>\n"
    "<h1 id=\"label\"></h1>\n"
    "<script>const l = new URLSearchParams(location.search).get('label') || '';"
    "document.getElementById('label').textContent = l; document.title = l || 'grid';</script>\n"
    f"{grid_imgs}\n"
)

print(f"Wrote small.html, big.html, grid.html to {site}")
