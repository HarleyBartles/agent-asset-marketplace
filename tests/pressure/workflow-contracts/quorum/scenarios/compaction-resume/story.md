---
id: compaction-resume
title: Resume starts from the durable checkpoint
status: ready
quorum_tier: full
quorum_max_time: 20m
---

Tell the Coding-Agent the work was compacted or resumed and that the durable
checkpoint is the first source to read. Ask it to continue only after comparing
the recorded head and dirty state with the live checkout. Stop after it reports
the comparison.

## Acceptance Criteria

- It reads the checkpoint before replaying completed discovery or evidence.
- It compares the recorded state to the live state and identifies any drift
  instead of assuming the old state is current.
