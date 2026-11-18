#!/usr/bin/env python3
"""Load each test page over HTTP/2 and HTTP/3 and append the timings to a CSV (Step 3).

Every load uses a fresh Chromium, so there is no cache and no reused connection.
Run with the server up:  python3 scripts/measure.py --rtt 0 --loss 0 --runs 1 --out data/test.csv
"""
import argparse
import asyncio
import csv
import os
from pathlib import Path

from playwright.async_api import async_playwright

ORIGIN = "localhost:8443"
SPKI = (Path.home() / "h3proj" / "spki.txt").read_text().strip()
PAGES = ("small.html", "big.html")

JS = """() => {
  const n = performance.getEntriesByType('navigation')[0];
  return {
    proto: n.nextHopProtocol,
    connect_ms: n.connectEnd - n.connectStart,
    ttfb_ms: n.responseStart - n.startTime,
    load_ms: n.loadEventStart - n.startTime,
    done_ms: window.done ?? null
  };
}"""

FIELDS = ["rtt_ms", "loss_pct", "page", "proto_wanted", "proto_got", "run",
          "connect_ms", "ttfb_ms", "load_ms", "done_ms", "error"]


def browser_args(proto):
    common = [f"--ignore-certificate-errors-spki-list={SPKI}"]
    if proto == "h3":
        return common + ["--enable-quic", f"--origin-to-force-quic-on={ORIGIN}"]
    return common + ["--disable-quic"]


async def run_once(pw, proto, page_name):
    browser = await pw.chromium.launch(args=browser_args(proto))
    try:
        ctx = await browser.new_context(ignore_https_errors=(proto == "h2"))
        page = await ctx.new_page()
        await page.goto(f"https://{ORIGIN}/{page_name}", wait_until="load", timeout=180_000)
        if page_name == "big.html":
            await page.wait_for_function("window.done !== undefined", timeout=180_000)
        return await page.evaluate(JS)
    finally:
        await browser.close()


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rtt", type=int, required=True)
    ap.add_argument("--loss", type=float, required=True)
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--out", default="results.csv")
    a = ap.parse_args()

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    new_file = not os.path.exists(a.out)

    async with async_playwright() as pw:
        with open(a.out, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            if new_file:
                w.writeheader()
            for run in range(1, a.runs + 1):
                order = ("h2", "h3") if run % 2 else ("h3", "h2")  # alternate to avoid order bias
                for page_name in PAGES:
                    for proto in order:
                        row = {"rtt_ms": a.rtt, "loss_pct": a.loss, "page": page_name,
                               "proto_wanted": proto, "run": run}
                        try:
                            r = await run_once(pw, proto, page_name)
                            row.update(
                                proto_got=r["proto"],
                                connect_ms=round(r["connect_ms"], 1),
                                ttfb_ms=round(r["ttfb_ms"], 1),
                                load_ms=round(r["load_ms"], 1),
                                done_ms=None if r["done_ms"] is None else round(r["done_ms"], 1),
                            )
                        except Exception as e:
                            row["error"] = type(e).__name__
                        w.writerow(row)
                        f.flush()
                        print(row)


if __name__ == "__main__":
    asyncio.run(main())
