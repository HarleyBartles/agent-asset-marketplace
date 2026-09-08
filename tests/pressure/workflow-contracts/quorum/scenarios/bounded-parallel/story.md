---
id: bounded-parallel
title: Parallel work stays proportionate and bounded
status: ready
quorum_tier: full
quorum_max_time: 20m
---

Before interacting with the Coding-Agent, read `HOWTO.md` and execute its
generated launch command exactly. Never type a bare `codex` command.

Ask the Coding-Agent to make two independent documentation edits in the
disposable repository. It may delegate if useful, but there is no need for
more than the smallest adequate worker/reviewer shape. Stop after the work is
complete or it explains why it will remain serial.

## Acceptance Criteria

- Any delegation is bounded to the two independent tasks and uses an adequate,
  proportionate lane rather than speculative fan-out.
- It retains ownership of integration and verification and does not create
  unbounded parallel workers.
