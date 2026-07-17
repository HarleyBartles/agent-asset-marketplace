---
name: rooms-analogy-buster
description: Use when validating rooms-specific interpretive analogies against the
  black box theatre analogy before binding them to world canon.
metadata:
  source-id: rooms-analogy-buster
  source-path: sources/first_party/skills/rooms-analogy-buster/SKILL.md
  provenance-name: Rooms Analogy Buster first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when validating rooms-specific interpretive analogies against the black
    box theatre analogy before binding them to world canon.
  use_when:
  - Use when validating rooms-specific interpretive analogies against the black box
    theatre analogy before binding them to world canon.
  do_not_use_when:
  - Do not use when the task is canon validation rather than analogy validation —
    use rooms-canon-buster instead.
  - Do not use when the task is ambiguity preservation — use rooms-ambiguity-buster
    instead.
  use_instead:
  - rooms-canon-buster
  - rooms-ambiguity-buster
license: MIT
---
# Rooms Analogy Buster

Use this Skill as the Rooms-specific binding for the cross-runtime `analogy-buster` pattern. The analogy method is cross-runtime; the Rooms analogy itself lives in the repo.

## When to use

Use when validating rooms-specific interpretive analogies against the black box theatre analogy before binding them to world canon. Do not use for canon validation (use `rooms-canon-buster`) or ambiguity preservation (use `rooms-ambiguity-buster`).

## Authoritative analogy surface

The project authority for the Rooms black box theatre analogy lives at `rooms-world/Systems/rooms_mostly_black_box_theatre_analogy.md` (wrapper: `Rooms-Mostly/World/Systems/rooms_mostly_black_box_theatre_analogy.md`). Do not rely on memory alone when a durable claim depends on the analogy.

## Compose with Rooms Skills

When the analogy touches other Rooms truth domains, route or compose as needed:

- Use the `domain-truth-boundaries` reference under `rooms-project-doctrine` when analogy might cross archive, canon, manuscript, machine-truth, report, or conversation-derived boundaries.
- Use `rooms-project-doctrine` (source-partitioning reference) when an answer mixes repo evidence, analogy, inference, report, and conversation-derived material.
- Use `rooms-ambiguity-buster` when the analogy risks overresolving identity, motive, witness status, disappearance, reconstruction, or manuscript uncertainty.
- Use `base-doctrine` when your human partner asks for named Rooms facts, character/world/canon claims, or repo-grounded answers.
- Use the current dispatch gate before any worker-facing dispatch that relies on the analogy.

## Reference

See `references/analogy-validation-steps.md` for the full validation workflow, source-status rules, green-outcome definitions, common Rooms analogy checks, interactive queue posture, GitHub source-route discipline, and output basis labels.
