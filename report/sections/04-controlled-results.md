# 4. Controlled results

**Writer:** B · **Due:** Dec 17 · **Target:** about 250 words

## What to cover

- Heatmap of speedup for small.html, then for big.html (`data/figures/heatmap_*.png`)
- Line charts of load time vs loss per RTT (`data/figures/lines_*.png`)
- Key numbers from `data/figures/summary.csv`: where HTTP/3 wins most, where it does not
- Connection time difference (handshake)
- Anything surprising, and a possible reason

## Draft
Figures 1 and 2 show the speedup (median HTTP/2 time divided by median HTTP/3 time) for each of the 12 network conditions. Values above 1 mean HTTP/3 was faster. All results are from runs with the loopback MTU set to 1500 bytes (see Section 3).

Speedup heatmap, small.html
<img width="1100" height="700" alt="image" src="https://github.com/user-attachments/assets/4caadc46-f952-46f6-b186-c8073d567e0d" />
Speedup heatmap, big.html
<img width="1100" height="700" alt="image" src="https://github.com/user-attachments/assets/07458510-2b11-4c21-a43d-63511ce0b834" />

Research question 1: effect of loss and latency. HTTP/3 was faster than HTTP/2 in 21 of the 24 conditions. Even without packet loss, HTTP/3 was ahead at RTT 100 and 300 ms, with speedups of 1.26 to 1.30 on both pages. At RTT 20 ms the gain was 1.21 for small.html but only 1.04 for big.html. With 3 % and 5 % loss the advantage was largest: speedups were between 1.30 and 2.68 for small.html and between 1.51 and 2.16 for big.html. For example, small.html at RTT 20 ms and 3 % loss took 1.64 s with HTTP/2 and 0.61 s with HTTP/3.

Exceptions. HTTP/3 was slower in three conditions, all with 1 % loss: big.html at RTT 20 ms (0.91) and 300 ms (0.85), and small.html at RTT 300 ms (0.72). With 1 % loss only a few packets are lost in each load, so a handful of loss events can decide the median of 10 runs. We therefore do not claim a trend at 1 % loss.

Research question 2: many small files vs one large file. Both pages showed the same overall pattern. HTTP/3 gained more on the small-file page at low RTT (2.52 and 2.68 at RTT 20 ms with 1 % and 3 % loss), while the large file gained about 2× at RTT 100 ms and 5 % loss. A possible explanation, which we did not test separately, is that QUIC's independent streams avoid head-of-line blocking when many small objects are in flight.

Median load time vs loss, small.html
![Uploading image.png…]()
Median load time vs loss, big.html

Effect of the loopback MTU. In our first full run the loopback MTU was the default 65536 bytes, and HTTP/3 was much slower under loss (speedups of 0.06 to 0.58). After setting the MTU to 1500 the result reversed. We believe this is because TCP sends very large segments on a 65536-byte MTU, so a given loss rate hits far fewer TCP packets than QUIC's roughly 1200-byte datagrams. This shows that emulation settings can change the conclusion.

One condition (RTT 300 ms, 5 % loss) has 9 valid runs instead of 10, because one load failed. All results come from one machine, so Chapter 5 tests whether they hold on real networks.
