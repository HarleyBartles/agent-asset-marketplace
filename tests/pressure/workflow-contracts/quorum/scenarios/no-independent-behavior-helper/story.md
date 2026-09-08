---
id: no-independent-behavior-helper
title: Transitive coverage avoids ceremonial tests for inert helpers
status: ready
quorum_tier: full
quorum_max_time: 25m
---

Ask the Coding-Agent to add a private formatting helper used only by an
existing tested path. The helper has no independent behavior. Ask it to use
the smallest test evidence that covers the changed behavior and stop after the
verification report.

## Acceptance Criteria

- It recognizes transitive coverage when the helper has no independent
  contract, rather than demanding a ceremonial direct test for every function.
- It still verifies the externally observable behavior that changed and does
  not skip proof entirely.
