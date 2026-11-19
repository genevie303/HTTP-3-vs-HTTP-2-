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
We compared HTTP/2 and HTTP/3 under 48 conditions: round-trip time (RTT) of 20, 100 and 300 ms, packet loss of 0, 1, 3 and 5 %, two test pages, and two protocols. Each condition was repeated 10 times, giving 480 page loads. small.html contains 50 small images, and big.html downloads one 5 MB file.

Network conditions were created with Linux tc netem on the loopback interface. Because every packet passes through netem once in each direction, we set the one-way delay to RTT / 2, and the loss rate applies in both directions. We checked each setting with ping before running the experiments. We also set the loopback MTU to 1500 bytes. With the default MTU of 65536, TCP sends far larger packets than QUIC (about 1200-byte datagrams), so the same loss rate hits TCP much less often. Our first full run used the default MTU and is reported in Section 4 for comparison.

The client is headless Chromium 159.0.8154.6 driven by Playwright 1.65.2. HTTP/2 was forced by disabling QUIC, and HTTP/3 by forcing QUIC on the test origin. Every page load starts a fresh browser, so there is no cache and no reused connection, and the server also sends Cache-Control: no-store. The order of the two protocols alternates between runs to avoid order bias. After each load we read nextHopProtocol and discarded any row where the protocol used differed from the protocol requested, or where an error occurred. This left 479 of 480 rows; one condition (RTT 300 ms, 5 % loss) has 9 runs.

For each load we recorded connection time, time to first byte, and page load time. For big.html we used the time until the 5 MB download completed. Because a few very slow loads can distort an average, we report the median of the runs per condition. The headline metric is the speedup, the median HTTP/2 time divided by the median HTTP/3 time, where a value above 1 means HTTP/3 is faster.

The server (Caddy v2.11.9) and the browser ran on the same Ubuntu 22.04.5 machine under WSL2 (18 logical CPUs, 7.5 GiB RAM), so the results reflect an emulated network on one machine rather than a real path.
