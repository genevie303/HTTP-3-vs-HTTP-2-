#!/usr/bin/env python3
"""Real-network test (Step 5): load public sites over HTTP/2 and HTTP/3 from a laptop.

Example:
  python scripts/measure_real.py --location dorm-wifi --sites a.com b.com --out data/real_results.csv
Keep --runs at 10 or less: normal browsing volume, never a load test.
"""
import argparse
import asyncio
import csv
import os
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright

JS = """() => {
  const n = performance.getEntriesByType('navigation')[0];
  return {
    proto: n.nextHopProtocol,
    connect_ms: n.connectEnd - n.connectStart,
    ttfb_ms: n.responseStart - n.startTime,
    load_ms: n.loadEventStart - n.startTime
  };
}"""

FIELDS = ["time", "location", "site", "proto_wanted", "proto_got", "run",
          "connect_ms", "ttfb_ms", "load_ms", "error"]


async def run_once(pw, host, proto):
    if proto == "h3":
        args = ["--enable-quic", f"--origin-to-force-quic-on={host}:443"]
    else:
        args = ["--disable-quic"]
    browser = await pw.chromium.launch(args=args)
    try:
        ctx = await browser.new_context()
        page = await ctx.new_page()
        await page.goto(f"https://{host}/", wait_until="load", timeout=60_000)
        return await page.evaluate(JS)
    finally:
        await browser.close()


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--location", required=True, help="e.g. dorm-wifi, library, canteen, 4g")
    ap.add_argument("--sites", nargs="+", required=True, help="hostnames that support h3")
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--out", default="real_results.csv")
    a = ap.parse_args()

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    new_file = not os.path.exists(a.out)

    async with async_playwright() as pw:
        with open(a.out, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            if new_file:
                w.writeheader()
            for run in range(1, a.runs + 1):
                order = ("h2", "h3") if run % 2 else ("h3", "h2")
                for host in a.sites:
                    for proto in order:
                        row = {"time": datetime.now().isoformat(timespec="seconds"),
                               "location": a.location, "site": host,
                               "proto_wanted": proto, "run": run}
                        try:
                            r = await run_once(pw, host, proto)
                            row.update(
                                proto_got=r["proto"],
                                connect_ms=round(r["connect_ms"], 1),
                                ttfb_ms=round(r["ttfb_ms"], 1),
                                load_ms=round(r["load_ms"], 1),
                            )
                        except Exception as e:
                            row["error"] = type(e).__name__
                        w.writerow(row)
                        f.flush()
                        print(row)


if __name__ == "__main__":
    asyncio.run(main())
