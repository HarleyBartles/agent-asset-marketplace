---
name: rooms-canon-buster
description: Use when rooms canon pressure checks and lawful canon/item adjustment
  routing for canon, gaps, ambiguity, and layer mismatches.
metadata:
  source-id: rooms-canon-buster
  source-path: sources/first_party/skills/rooms-canon-buster/SKILL.md
  provenance-name: Rooms Canon Buster first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when rooms canon pressure checks and lawful canon/item adjustment routing
    for canon, gaps, ambiguity, and layer mismatches.
  use_when:
  - Use when rooms canon pressure checks and lawful canon/item adjustment routing
    for canon, gaps, ambiguity, and layer mismatches.
  do_not_use_when:
  - Do not use when the task is ambiguity preservation rather than canon resolution
    — use rooms-ambiguity-buster instead.
  - Do not use when the task is analogy validation — use rooms-analogy-buster instead.
  use_with:
  - rooms-project-doctrine
license: MIT
---
# Rooms Canon Buster

Use this skill to test canon pressure in Rooms, Mostly. Canon Buster protects coherence, not tidiness: do not flatten useful ambiguity, narrator limitation, archive gaps, or layered truth merely because an item is uncomfortable.

## Scope

This skill is Rooms-only. It does not answer generic continuity questions for other projects.

Use `rooms-project-doctrine` for Rooms truth boundaries, `rooms-project-doctrine` (source-partitioning reference) to separate evidence classes, `rooms-ambiguity-buster` when the right outcome is to preserve unresolved identity or motive, and `linear-issue-shaping` when a canon-safe next step turns into Linear issue readiness, worker-shaped issue status handling, external handoff text when explicitly requested, or GitHub proof handoff after a PR/branch/commit exists.

Use the GPT-wide buster framework pattern. Run internally when there is one lawful path. Switch to interactive queue mode when your human partner must decide a real creative/canon tradeoff.

## What Canon Buster Tests

Given an item under discussion, test whether it:

- fits established Rooms canon;
- conflicts with established canon;
- exposes a gap in canon;
- belongs to another truth layer rather than canon;
- should cause the item, canon, or both to move;
- should remain unresolved because ambiguity is part of the book.

Canon Buster may be used before dispatch planning, during conversation, before persistence, when reviewing manuscript/world claims, or when converting archive/conversation material into candidate world state.

## Compose With Existing Rooms Skills

Use or defer to:

- `rooms-project-doctrine` for source routing, truth boundaries, publication, and report hygiene;
- `rooms-project-doctrine` (source-partitioning reference) to separate evidence, report, synthesis, inference, missing data, and conversation-derived material;
- `rooms-ambiguity-buster` when identity, motive, authorship, witness status, narrator knowledge, reconstruction, or disappearance could be overresolved;
- `rooms-analogy-buster` when analogy is doing too much work;
- `rooms-zoom-outs-buster` when the full frame is getting lost;
- `rooms-character-investigation` for broad source lookup and source-partitioned investigation packets;
- `rooms-sheet-creator` for prompt, peek, and recall sheet creation from durable packets;
- `rooms-image-sidecars` for image evidence starter packets before Pit/archive ingestion;
- `linear-issue-shaping` for Linear worker issue readiness, worker-shaped issue status handling, external handoff text when explicitly requested, and GitHub proof handoff after a PR/branch/commit exists.

## Detailed canon-check procedure

See `references/canon-check-steps.md` for the full source ladder, GitHub source-route discipline, green/amber/red/blocked outcome taxonomy, internal and interactive queue modes, queue item shape, and boundary rules. The SKILL.md body stays a compact router; the reference holds the operational detail.
