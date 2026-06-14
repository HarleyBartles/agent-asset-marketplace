---
name: wild-bunch-project-doctrine
description: bootstrap the wild bunch repo posture before any repo-sensitive change. use when work touches harleybartles/wild-bunch, worker dispatch, worker return verification, source-truth claims, issue-goal conformance, or when chat summaries, session busters, worker reports, or issue comments might be mistaken for live repo truth.
---

# Wild Bunch Project Doctrine

Use this skill first when working on `HarleyBartles/wild-bunch`. The live repo
state on current `main` is the source of truth. Chat summaries, issue comments,
session busters, and worker reports are support material only.

## Rules

- Treat `HarleyBartles/wild-bunch` as a mainline-only C#/.NET game project.
- Inspect live source before claiming current state.
- GPT prepares worker packets; Harley sends them; workers execute.
- Returns must include branch, commit, PR, validation, and issue-goal
  conformance notes.

## References

Read [Live repo posture](references/repo-posture.md) when a task needs source-truth posture, worker route boundaries, or return/verification expectations.
