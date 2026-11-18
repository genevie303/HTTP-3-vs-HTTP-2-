# Demo script (3 minutes)

**Owner:** A · **Rehearsed:** [ ] once [ ] twice

## Before the presentation

1. Start the VM, then the server: `bash server/run_server.sh`
2. Make sure netem is off: `bash scripts/netem.sh reset`
3. Open the two windows: `bash scripts/start_demo.sh`
4. Check DevTools > Network > Protocol: `h2` on the left, `h3` on the right

## During the presentation

| Time | Action | What to say |
| --- | --- | --- |
| 0:00 | Reload both windows on a good network | TODO |
| 0:45 | `bash scripts/netem.sh set 100 3` | TODO |
| 1:00 | Reload both windows at the same moment | TODO |
| 2:00 | Point at the difference | TODO |
| 2:45 | `bash scripts/netem.sh reset` | TODO |

## If something breaks

Switch to the backup video (link in `demo/README.md`).
