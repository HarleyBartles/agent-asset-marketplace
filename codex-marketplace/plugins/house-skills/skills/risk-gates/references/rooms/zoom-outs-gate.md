---
name: rooms-zoom-outs-buster
description: Use when rooms zoom-out compression checks against artifacts and source
  surfaces.
metadata:
  source-id: rooms-zoom-outs-buster
  source-path: sources/first_party/skills/rooms-zoom-outs-buster/SKILL.md
  provenance-name: Rooms Zoom Outs Buster first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when rooms zoom-out compression checks against artifacts and source surfaces.
  use_when:
  - Use when rooms zoom-out compression checks against artifacts and source surfaces.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
license: MIT
---
# Rooms Zoom Outs Buster

Use this Skill for Rooms, Mostly zoom-out checks. A zoom-out is a compressed behavioural, emotional, structural, or
interaction model for a character, room, event, or system.

This is not generic character analysis, thematic essay writing, lore summary, psychological diagnosis, or symbolic
interpretation. It is a bidirectional compression-validity test: zoom out into a compressed model, then zoom back in and
test whether actual artifacts still behave like that model.

## Core question

Ask: can this entity survive compression without losing identity?

A model is not fully green merely because it feels elegant. It must regenerate artifact shape: voice, timing, behaviour,
interaction pattern, failure mode, and distinction from nearby entities or events.

## Workflow

1. Identify the entity or pattern under discussion.
2. State the proposed zoom-out: behavioural truth, emotional posture, interaction mechanic, compression mode, or
structural role.
3. Check whether the model is only conversation-derived or already artifact-grounded.
4. Zoom back in: test the model against relevant artifacts, voice surfaces, room/system docs, canon/world surfaces,
manuscript excerpts, or archive-derived evidence when lawful and needed.
5. Mark status using the readiness levels below.
6. If the model is a persistence candidate, compose with `rooms-project-doctrine`, `canon-buster`,
`rooms-ambiguity-buster`, and `invariant-buster` before dispatch or canon/world persistence.

## Status levels

- `green_artifact_verified`: compression survives return to persisted artifact behaviour.
- `green_model_only`: compression is plausible for conversation but not artifact-verified; do not persist as truth
  without further checks.
- `green_internal_misalignment`: artifacts support belonging plus stable imperfect execution or rhythm divergence.
- `amber_artifact_needed`: the model may be right, but source surfaces have not been checked.
- `amber_overfit_risk`: the compression may be flattening distinction, assigning shared forms too exclusively, or making
  one entity carry a pattern.
- `red_flattening`: the zoom-out erases meaningful distinction.
- `red_overresolution`: the zoom-out resolves awareness, motive, identity, or ambiguity beyond artifact support.
- `red_externalising`: the model incorrectly treats internal participants as outsiders or observers.
- `red_symbolic_drift`: the model becomes symbolic shorthand instead of behaviour regeneration.
- `red_regeneration_failure`: the compressed model cannot plausibly reproduce artifact behaviour.
- `blocked_source_unavailable`: required artifact/canon/source surfaces are unavailable.

## Source and verification discipline

Artifacts are regeneration test surfaces, not optional examples. Use the smallest sufficient source set.

Prefer, in order, when relevant and available:

1. The actual artifact under discussion: tweet/thread/sketch/room doc/voice artifact/manuscript excerpt/system surface.
2. Brian/World character, room, systems, and canon surfaces.
3. Manuscript surfaces for prose/scene behaviour, preserving Derek authority.
4. Pit/archive evidence only as evidence, with provenance and partiality preserved.
5. Reports only as reports.
6. Conversation-derived material only as candidate compression, not artifact verification.

Do not treat memory, conversation, reports, or analogy as artifact verification.

## GitHub source-route discipline

Before repo-dependent judgment, identify the available GitHub route. Use bound `file_search` GitHub for broad
repo discovery, unknown-path searches, stale-reference inventories, and corpus-style reads across multiple repo
surfaces. Use the live GitHub API connector route, such as `api_tool` when exposed, for exact issue threads,
comments, file-by-path reads, commit/ref comparison, PR details, remote-head checks, and authorized GitHub
mutations.

If `file_search` is unavailable or not bound, do not treat that as loss of GitHub access when a live API route is
available. Use the live API route for exact reads and operations. If broad repo discovery would materially improve
safety or completeness, ask Harley to bind `file_search` GitHub to the relevant repo set before doing the scan.

Search results are discovery, not final truth. Inspect the relevant file, issue, commit, or source surface before
making affirmative repo-grounded claims.

## Internal mode

Run internally when the answer, plan, or dispatch depends on a zoom-out. Do not show a queue when there is one
legitimate path. Internally downgrade unverified models to `green_model_only` or `amber_artifact_needed`; do not present
them as artifact-verified.

## Interactive mode

Use an interactive queue when Harley must decide among real modelling or persistence choices. Inherit visible queue
mechanics and conversational item formatting from `buster-framework`. Domain-specific zoom-out item content should
include the proposed compression, artifact gap or failure risk, green condition, and GPT's strong recommendation. See
`references/queue-patterns.md`.

## Internal Misalignment Green

A character can fully belong to a room, understand it, and still not execute its rhythm perfectly. This is not outsider
status, misunderstanding, or conscious anxiety when artifacts support internal belonging plus stable rhythm divergence.
Use `green_internal_misalignment` for this pattern.

## Failure modes

Consult `references/zoom-out-failure-modes.md` when judging flattening, overresolution, externalising, symbolic drift,
or regeneration failure.

## Event and lifecycle modelling

Zoom-outs apply to events and rooms as well as characters. Event models must regenerate artifact structure, timing,
boundary conditions, and lifecycle phases. See `references/compression-validity-test.md`.

## Persistence boundary

This Skill does not persist canon. A verified zoom-out may become a persistence candidate. Before persistence, compose
with:

- `rooms-project-doctrine` for evidence/conversation/report/canon separation.
- `canon-buster` for canon pressure.
- `rooms-ambiguity-buster` for unresolved scope, source, actor, or terminology ambiguity.
- `invariant-buster` for protected surfaces, authority, and repo/governance invariants.
- `linear-issue-shaping` if worker execution is needed.

Do not simulate Brian, Albert, Derek, Chris, or Will. Do not mutate repos from chat.
