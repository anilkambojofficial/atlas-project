"""Platform identifier generation.

Governing documents:
- IP-001 §15 — UUID v7 is the canonical identifier standard.
- RFC 9562 §5.7 — UUID version 7 bit layout.

The Python standard library does not provide ``uuid.uuid7`` on the
platform's supported runtime, so the generator is implemented here
against RFC 9562: 48-bit big-endian Unix timestamp in milliseconds,
4-bit version (7), 12 random bits, 2-bit variant (0b10), 62 random bits.
"""

from __future__ import annotations

import os
import time
import uuid

_TIMESTAMP_MASK = 0xFFFF_FFFF_FFFF  # 48 bits
_RAND_A_MASK = 0x0FFF  # 12 bits
_RAND_B_MASK = 0x3FFF_FFFF_FFFF_FFFF  # 62 bits


def uuid7() -> uuid.UUID:
    """Generate a time-ordered UUID version 7 (RFC 9562)."""
    timestamp_ms = time.time_ns() // 1_000_000
    random_bits = int.from_bytes(os.urandom(10), "big")  # 80 random bits

    value = (timestamp_ms & _TIMESTAMP_MASK) << 80
    value |= 0x7 << 76  # version 7
    value |= ((random_bits >> 62) & _RAND_A_MASK) << 64
    value |= 0b10 << 62  # RFC 9562 variant
    value |= random_bits & _RAND_B_MASK
    return uuid.UUID(int=value)
