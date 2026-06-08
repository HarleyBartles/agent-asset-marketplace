---
name: adventures-project-doctrine-v1.1
description: >-
  shared Adventures doctrine for repo truth, Patch canon, visual-work stage boundaries, skill routing, and source-backed posture. use when Adventures work needs durable project context before a more specific skill, especially first-turn bootstrap, source truth, visual planning, source discovery, QA, image readiness, deck/package work, or deterministic boundaries.
---

# Adventures Project Doctrine v1.1

Use this skill as the shared doctrine store for Adventures of Patch project rules not owned by a more specific Adventures skill or the repo playbook.

This skill composes with `work-mode-router-v1` and `adventures-bootstrap-v1.1`: bootstrap routes here when shared Adventures doctrine is needed, then this skill routes to the more specific task skill or repo playbook. Do not copy this doctrine into the system prompt or into bootstrap. Keep `SKILL.md` as the control plane and load only the reference needed for the current task.

## Core rule

The canonical repo is `HarleyBartles/adventures-of-patch`. Patch is the constant protagonist unless Harley explicitly says otherwise. For ordinary GPT-side Adventures work, keep deterministic planning separate from image generation/editing and route source discovery, QA, image readiness, acceptance, asset-sheet compilation, deck/package work, and publication to the correct capability. Use this skill for shared project doctrine, then route actual work to the most specific Adventures skill or repo playbook.

## Stage boundaries

- Deterministic planning and boards are separate from image generation/editing.
- Source discovery and source-backed claims are separate from visual readiness.
- QA does not authorize another image call by itself.
- Generated candidates and deterministic artifacts need the correct lane review before use.
- Asset-sheet compilation, deck/package work, and acceptance are downstream stages, not substitutes for planning or QA.

## Bootstrap relationship

System prompts should route Adventures work to `adventures-bootstrap-v1.1`, not duplicate this doctrine inline. `adventures-bootstrap-v1.1` decides which doctrine-bearing surface must be read for the task shape. This skill owns the shared Adventures lessons and reference map; it does not authorize repo mutation, image generation, dispatch, issue closure, deck building, or receipt creation by itself.

If a task is already inside a specialist Adventures skill, use this skill only for shared project posture that the specialist does not own. Prefer the most specific task skill for execution decisions.
