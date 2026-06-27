---
name: adventures-visual-preproduction
description: Use when prepare source-first Adventures visual planning packets, frame
  breakdowns, and readiness checks before image generation or editing, keeping deterministic
  planning separate from downstream production.
metadata:
  source-id: adventures-visual-preproduction
  source-path: sources/first_party/skills/adventures-visual-preproduction/SKILL.md
  provenance-name: Adventures Visual Preproduction first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when prepare source-first Adventures visual planning packets, frame breakdowns,
    and readiness checks before image generation or editing, keeping deterministic
    planning separate from downstream production.
  use_when:
  - Use when prepare source-first Adventures visual planning packets, frame breakdowns,
    and readiness checks before image generation or editing, keeping deterministic
    planning separate from downstream production.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
  projection_targets:
  - codex-marketplace/plugins/adventures-pack/skills/adventures-visual-preproduction
  - codex-marketplace/plugins/house-skills/skills/adventures-visual-preproduction
license: MIT
---
# Adventures Visual Preproduction

Use this skill for source-first visual planning, frame breakdowns, and readiness checks.

## Owned decision

Decide whether the request is ready for deterministic visual planning, needs more source discovery, or should route to another Adventures skill.

## Hard boundaries

Deterministic planning is separate from image generation and editing.

This skill does not authorize another image call.

## Minimal workflow

1. Gather the source basis and the visual goal.
2. Produce or review a deterministic planning packet.
3. Confirm which lane owns the next step.
4. Stop before generation or editing.
