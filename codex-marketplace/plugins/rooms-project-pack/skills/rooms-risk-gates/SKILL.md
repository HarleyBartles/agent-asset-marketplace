---
name: rooms-risk-gates
description: Use when working in Rooms, Mostly and a pre-action risk gate is needed
  for rooms-specific canon pressure, ambiguity preservation, analogy validation, or
  zoom-out compression. Composes with the base risk-gates skill.
metadata:
  source-id: rooms-risk-gates
  source-path: sources/first_party/skills/rooms-risk-gates/SKILL.md
  provenance-name: Rooms Risk Gates first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when working in Rooms, Mostly and a pre-action risk gate is needed for
    rooms-specific canon pressure, ambiguity preservation, analogy validation, or
    zoom-out compression. Composes with the base risk-gates skill.
  use_when:
  - Use when working in Rooms and testing canon pressure — whether an item fits, conflicts
    with, exposes a gap in, or belongs to another layer than established Rooms canon.
  - Use when working in Rooms and the action risks resolving identity, motive, authorship,
    witness status, narrator knowledge, archive gaps, disappearance, or manuscript
    uncertainty without evidence.
  - Use when working in Rooms and relying on the black box theatre analogy for a canon,
    world, manuscript, dispatch, or persistence decision.
  - Use when working in Rooms and compressing a character, room, event, or system
    into a behavioural/emotional/structural model for canon, persistence, or dispatch
    decisions.
  do_not_use_when:
  - Do not use when not working in Rooms — use the base risk-gates skill instead.
  - Do not use when the task is a broad planning or research workflow without a concrete
    action to gate.
  related_skills:
  - risk-gates
  - rooms-project-doctrine
license: MIT
---
# Rooms Risk Gates

This is the Rooms, Mostly overlay for the base `risk-gates` skill. It holds the rooms-specific risk gate profiles that were consolidated out of the retired buster framework. Use it together with `risk-gates` when the action is in Rooms and the gate question is rooms-specific (canon pressure, ambiguity preservation, analogy validation, or zoom-out compression). When the gate question is generic, use the base `risk-gates` skill instead.

## Gate routing table

Read only the gate reference docs whose use-when matches the current action. Skip gates whose do-not-use-when matches. Do not read all reference docs by default.

| Gate | Use when | Do not use when | Reference |
|------|----------|-----------------|-----------|
| rooms-ambiguity-gate | Working in Rooms and the action risks resolving identity, motive, authorship, witness status, narrator knowledge, archive gaps, disappearance, or manuscript uncertainty without evidence. | Not working in Rooms, or the ambiguity is generic (use the generic ambiguity-gate instead). | `references/rooms-ambiguity-gate.md` |
| rooms-canon-gate | Working in Rooms and testing canon pressure — whether an item fits, conflicts with, exposes a gap in, or belongs to another layer than established Rooms canon. | Not working in Rooms, or the canon question is generic (use the generic canon-gate instead). | `references/rooms-canon-gate.md` |
| rooms-analogy-gate | Working in Rooms and relying on the black box theatre analogy for a canon, world, manuscript, dispatch, or persistence decision. | Not working in Rooms, or no analogy is in play, or the analogy question is generic (use the generic analogy-gate instead). | `references/rooms-analogy-gate.md` |
| rooms-zoom-outs-gate | Working in Rooms and compressing a character, room, event, or system into a behavioural/emotional/structural model that will be used for canon, persistence, or dispatch decisions. | Not working in Rooms, or no zoom-out/compression model is being constructed or relied upon. | `references/rooms-zoom-outs-gate.md` |

## Composition

The rooms gate profiles reuse the gate modes, queue contract, output-surface boundary, and workflow defined by the base `risk-gates` skill. Read the base skill for the shared gate framework before applying a rooms-specific profile. Each rooms gate reference doc adds the rooms-specific pressure types, green outcomes, compose-with routing, and boundary rules that the generic gate does not own.

## Boundaries

Do not use rooms gates as broad planning, research, or execution workflows. Do not use a rooms gate to create permission that the user, source surface, policy, Rooms project doctrine, or downstream skill has not granted. Do not read all rooms gate reference docs by default — use the routing table to select only material gates.
