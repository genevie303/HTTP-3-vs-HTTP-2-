#!/usr/bin/env python3
"""Summarize the lab results and draw the main charts (Step 7).

Usage:  python scripts/analyze.py [results.csv] [output_folder]
Default: data/results.csv -> data/figures/
Writes summary.csv, lines_<page>.png and heatmap_<page>.png.
Speedup = median HTTP/2 time / median HTTP/3 time; above 1 means HTTP/3 is faster.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

src = Path(sys.argv[1] if len(sys.argv) > 1 else "data/results.csv")
out = Path(sys.argv[2] if len(sys.argv) > 2 else "data/figures")
out.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(src)
df = df[df["error"].isna() & (df["proto_got"] == df["proto_wanted"])].copy()
df["time_ms"] = df["done_ms"].where(df["page"] == "big.html", df["load_ms"])

summary = (df.groupby(["page", "rtt_ms", "loss_pct", "proto_wanted"])["time_ms"]
             .median().unstack("proto_wanted"))
summary["speedup"] = summary["h2"] / summary["h3"]
summary.round(2).to_csv(out / "summary.csv")
print(summary.round(2))

for page in df["page"].unique():
    name = page.replace(".html", "")
    rtts = sorted(df["rtt_ms"].unique())

    fig, axes = plt.subplots(1, len(rtts), figsize=(4 * len(rtts), 3.5), sharey=True, squeeze=False)
    for ax, rtt in zip(axes[0], rtts):
        s = summary.loc[(page, rtt)]
        ax.plot(s.index, s["h2"], marker="o", label="HTTP/2")
        ax.plot(s.index, s["h3"], marker="o", label="HTTP/3")
        ax.set_title(f"RTT {rtt} ms")
        ax.set_xlabel("Packet loss (%)")
    axes[0][0].set_ylabel("Median load time (ms)")
    axes[0][0].legend()
    fig.suptitle(page)
    fig.tight_layout()
    fig.savefig(out / f"lines_{name}.png", dpi=200)
    plt.close(fig)

    heat = summary.loc[page]["speedup"].unstack("loss_pct")
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    im = ax.imshow(heat.values, cmap="RdYlGn", vmin=0.5, vmax=1.5)
    ax.set_xticks(range(len(heat.columns)), [f"{c:g}" for c in heat.columns])
    ax.set_yticks(range(len(heat.index)), heat.index)
    ax.set_xlabel("Packet loss (%)")
    ax.set_ylabel("RTT (ms)")
    for i in range(heat.shape[0]):
        for j in range(heat.shape[1]):
            ax.text(j, i, f"{heat.values[i, j]:.2f}x", ha="center", va="center")
    fig.colorbar(im, label="HTTP/2 time / HTTP/3 time")
    ax.set_title(f"{page}: above 1 means HTTP/3 is faster")
    fig.tight_layout()
    fig.savefig(out / f"heatmap_{name}.png", dpi=200)
    plt.close(fig)

print(f"Charts and summary.csv written to {out}")
