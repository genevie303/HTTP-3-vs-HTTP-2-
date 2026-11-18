# Report outline (at least 1000 words)

Working title: *Can HTTP/3 Save Your Campus WiFi? Measuring QUIC vs TCP under Real and Simulated Network Conditions*

| Section | Writer | Due |
| --- | --- | --- |
| 1. Introduction and motivation | C | Dec 18 |
| 2. Background: TCP + TLS vs QUIC, head-of-line blocking, handshakes | A | Dec 17 |
| 3. Testbed and method: diagram, conditions, metrics, versions | A (testbed), B (method) | Dec 17 |
| 4. Controlled results: line charts and heatmaps | B | Dec 17 |
| 5. Real-world results on campus | C | Dec 18 |
| 6. Discussion and limitations | C | Dec 18 |
| 7. Conclusion and recommendation | C | Dec 18 |

Each writer drafts their section as `report/<number>-<name>.md`; C merges them into the final report.

## Facts to record for section 3

- Caddy version:
- Chromium version (Playwright):
- VM: CPUs, RAM, Ubuntu version:
- Test pages: small.html = 50 images of 200x200 px; big.html = 5 MB; grid.html = 200 tiles
