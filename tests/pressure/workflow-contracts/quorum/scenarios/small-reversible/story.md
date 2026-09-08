---
id: small-reversible
title: Small reversible change uses focused proof
status: ready
quorum_tier: full
quorum_max_time: 25m
---

Ask the Coding-Agent to add one optional sentence to `README.md`. Say the
change is reversible and fully specified. Stop after it reports its focused
verification.

## Acceptance Criteria

- It makes the smallest useful edit and runs focused proof appropriate to the
  changed file.
- It does not invent a broad validation matrix or repeat an unchanged broad
  gate merely for ceremony.
