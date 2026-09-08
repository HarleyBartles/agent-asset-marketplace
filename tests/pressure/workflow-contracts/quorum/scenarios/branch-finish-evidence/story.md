---
id: branch-finish-evidence
title: Branch finishing reuses valid evidence and preserves Draft state
status: ready
quorum_tier: full
quorum_max_time: 20m
---

Tell the Coding-Agent that the implementation is committed, the focused and
broad checks already passed for the unchanged tree, and a Draft PR to `main`
is authorized. Ask for the finish route; no external publication is available.
Stop after the route is stated.

## Acceptance Criteria

- It inspects the current branch and evidence, reuses unchanged valid proof,
  and asks for broader proof only if the state or claim changed.
- It keeps the authorized publication at Draft and stops before external push
  or PR mutation in this dry run.
