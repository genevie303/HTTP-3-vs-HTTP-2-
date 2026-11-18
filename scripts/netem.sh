#!/usr/bin/env bash
# Network emulation on the loopback interface (Step 2).
# On loopback every packet crosses netem once per direction, so delay = RTT / 2.
#
# Usage:
#   bash scripts/netem.sh set <rtt_ms> <loss_pct>   e.g. set 100 3
#   bash scripts/netem.sh reset
#   bash scripts/netem.sh show
set -euo pipefail

case "${1:-}" in
  set)
    rtt="${2:?missing rtt_ms}"
    loss="${3:?missing loss_pct}"
    sudo tc qdisc del dev lo root 2>/dev/null || true
    sudo tc qdisc add dev lo root netem delay "$((rtt / 2))ms" loss "${loss}%"
    echo "lo: RTT ${rtt} ms, loss ${loss}%"
    ;;
  reset)
    sudo tc qdisc del dev lo root 2>/dev/null || true
    echo "lo: netem removed"
    ;;
  show)
    tc qdisc show dev lo
    ;;
  *)
    echo "usage: $0 set <rtt_ms> <loss_pct> | reset | show" >&2
    exit 1
    ;;
esac
