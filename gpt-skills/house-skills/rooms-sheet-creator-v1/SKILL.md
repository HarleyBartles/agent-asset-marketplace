# Rooms Sheet Creator v1

Use this skill to create Rooms sheets from durable input packets.

This skill consumes the investigation packet, lane information, and Harley direction. It does not rely on same-session handoff or undocumented memory.

## Core rule

If the input packet is not durable, the sheet is not ready.

## Boundaries

- It does not own investigation.
- It does not own source partitioning.
- It does not replace project doctrine.
