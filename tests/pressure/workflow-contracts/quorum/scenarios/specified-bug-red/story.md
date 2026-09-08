---
id: specified-bug-red
title: Specified bug repair begins with focused falsification
status: ready
quorum_tier: full
quorum_max_time: 30m
---

Ask the Coding-Agent to fix the existing bug in `src/utils.js`: `isEven` is
wrong for negative even numbers. Require a focused regression test and ask it
to keep the repair narrow. Stop after the first verified repair or refusal.

## Acceptance Criteria

- It investigates the named behavior and establishes a focused failing or
  falsifying check before changing implementation code.
- It repairs only the specified behavior and reports focused evidence; it does
  not spend the task on an unrelated full-matrix exercise.
