---
name: wild-bunch-project-doctrine
description: Bootstrap the Wild Bunch repo posture before any change. Use when you need the project truth model, worker return contract, or guidance on how to treat live source versus chat summaries.
---

# Wild Bunch Project Doctrine

## Overview

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

- [Live repo posture](references/repo-posture.md)
