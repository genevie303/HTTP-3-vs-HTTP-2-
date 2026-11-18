# 3. Testbed and method

**Writers:** A (testbed), B (method) · **Due:** Dec 17 · **Target:** about 250 words

## 3.1 Testbed (A)

- Diagram: browser (Chromium) and Caddy server on the same Ubuntu VM, netem on loopback
- Caddy configuration: HTTP/1.1, HTTP/2 and HTTP/3 on port 8443, self-signed certificate
- Test pages: small.html (50 images, 200x200 px), big.html (one 5 MB file), grid.html (demo)
- Versions and VM specs (copy from `notes/environment.md`)

### Draft

TODO

## 3.2 Method (B)

- Conditions: RTT 20, 100, 300 ms × loss 0, 1, 3, 5 % × 2 pages × 2 protocols × 10 runs = 480 loads
- How netem works on loopback (delay = RTT / 2, loss in both directions)
- Metrics: page load time, connection time, time to first byte, download time for big.html
- A fresh browser for every load; protocol order alternated; protocol verified with nextHopProtocol
- Why medians, not means

### Draft

TODO
