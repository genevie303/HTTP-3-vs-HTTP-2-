# 2. Background: TCP + TLS vs QUIC

**Writer:** A · **Due:** Dec 17 · **Target:** about 250 words

## What to cover

- HTTP/2 runs over TCP + TLS; HTTP/3 runs over QUIC, which runs over UDP
- Head-of-line blocking: one lost TCP packet stalls every HTTP/2 stream; QUIC streams are independent
- Handshake round trips: TCP + TLS 1.3 needs 2 RTTs before data, QUIC needs 1 (0 on resumption)
- QUIC runs in user space: easier to update, but uses more CPU
- How a browser discovers HTTP/3 (Alt-Svc header)
- A small figure comparing the two protocol stacks

## References to cite

- RFC 9000 (QUIC), RFC 9114 (HTTP/3)
- Langley et al., "The QUIC Transport Protocol", SIGCOMM 2017

## Draft

TODO
