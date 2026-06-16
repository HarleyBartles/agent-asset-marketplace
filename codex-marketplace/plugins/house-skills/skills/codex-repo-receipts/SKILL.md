---
name: codex-repo-receipts
description: Use when a repo-backed Codex task needs durable plan and implementation-record receipts for non-trivial work.
---

# Codex Repo Receipts

Use this skill for non-trivial repo-backed work that should leave durable repo-resident receipts.

## Core job

Publish two artifacts:

1. a plan under the repository's local convention, or `docs/superpowers/plans/` by default;
2. a matching implementation record under the repository's local convention, or `docs/superpowers/records/` by default.

Use the narrowest local convention that already exists. If the repository has no local convention, use the default paths above.

## What the plan should contain

- one observable goal;
- likely changed files or source seams;
- bite-sized implementation steps;
- validation commands or observable proof for major steps;
- non-goals and safety boundaries.

## What the implementation record should contain

- issue identifier;
- branch name;
- starting `main` SHA;
- final head SHA;
- PR URL if one was created;
- exact files changed;
- generated artifacts;
- validation commands and results;
- skipped checks with reasons;
- surprises, deviations from the plan, and follow-ups.

Keep the record factual. It is not a transcript, and it should not include secrets, raw private tool output, or worker chatter.

## Linkage rule

The PR body or final worker report should link both durable artifacts:

- Plan: `docs/superpowers/plans/...`
- Implementation record: `docs/superpowers/records/...`

## Narrow omission rule

Tiny mechanical changes may omit repo-resident receipts only when the omission is explicit and justified in the PR body or final worker report. Silent omission is not acceptable for non-trivial repo-backed work.

## Boundary

Do not duplicate cross-repo doctrine into repository `AGENTS.md` files. Keep this skill focused on receipt publishing and evidence capture.
