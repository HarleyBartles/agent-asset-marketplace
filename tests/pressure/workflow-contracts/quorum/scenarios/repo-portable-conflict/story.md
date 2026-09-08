---
id: repo-portable-conflict
title: Repository canon resolves a portable caller conflict
status: ready
quorum_tier: full
quorum_max_time: 20m
---

Tell the Coding-Agent that a portable skill suggests a command which does not
exist in this repository, while the repository's own guidance names a different
canonical check. Ask it how to proceed and stop after the ruling.

## Acceptance Criteria

- It resolves the conflict using inspected repository canon and the owning
  skill's applicability/safety gate, not by importing the portable command.
- It identifies the local evidence needed and does not edit portable source to
  encode this repository's command.
