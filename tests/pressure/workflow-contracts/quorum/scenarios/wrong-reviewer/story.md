---
id: wrong-reviewer
title: Review evidence selects the owning reviewer
status: ready
quorum_tier: full
quorum_max_time: 20m
---

Ask the Coding-Agent to review the repository for a security-sensitive change
that is not present in the fixture. Tell it to report what evidence is needed
before making a ruling. Stop after it produces its review route and first
finding.

## Acceptance Criteria

- It chooses a reviewer or review lane based on the actual claim and evidence,
  not by blindly dispatching the first available profile.
- It does not claim a green review from a superficial “looks good” scan.
