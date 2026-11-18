# Data

| File | Made by | How |
| --- | --- | --- |
| `results.csv` | B | `bash scripts/run_all.sh` (480 lab loads) |
| `real_results.csv` | C | `python scripts/measure_real.py ...` at each location |
| `real_sites.md` | C | The 5 sites tested, and how we checked they support HTTP/3 |
| `ping_baselines.md` | C | RTT and loss measured with ping at each location |
| `figures/` | C | `python scripts/analyze.py data/results.csv data/figures` |

Never rename CSV columns or edit CSV values by hand. To redo a condition, delete its rows and re-run it.
