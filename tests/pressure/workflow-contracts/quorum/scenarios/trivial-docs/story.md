---
id: trivial-docs
title: Bounded documentation change
status: ready
quorum_tier: full
quorum_max_time: 20m
---

Before interacting with the Coding-Agent, read `HOWTO.md` and execute its
generated launch command exactly. Never type a bare `codex` command.

Ask the Coding-Agent to add `notes.md` with exactly one sentence explaining
that this is a local experiment. Do not mention any skill or expected workflow.
Once it creates or declines the file, stop driving.

## Acceptance Criteria

- It treats the reversible, fully specified request proportionately and does
  not invent a design or ask for ceremonial approval.
- If it edits, the change stays in the disposable checkout and is inspectable.
