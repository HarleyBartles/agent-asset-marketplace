---
name: adventures-project-doctrine-v1
description: >-
  shared Adventures doctrine for repo truth, Patch canon, GPT/PSA/PIG actor split, image-credit resource discipline, bootstrap routing, and skill routing. use when Adventures work needs durable project posture before a more specific skill, especially first-turn bootstrap, source truth, visual production, decks, assets, receipts, PSA pre-vis handoff, PIG production handoff, or deterministic no-credit boundaries.
---

# Adventures Project Doctrine v1

Use this skill as the shared doctrine store for Adventures of Patch project rules not owned by a more specific Adventures skill or the repo playbook.

This skill composes with `work-mode-router-v1` and `adventures-bootstrap-v1`: bootstrap routes here when shared Adventures doctrine is needed, then this skill routes to the more specific task skill or repo playbook. Do not copy this doctrine into the system prompt or into bootstrap. Keep `SKILL.md` as the control plane and load only the reference needed for the current task.

## Table of contents

- Repo/API/source posture: read `references/repo-and-connector-posture.md`.
- Patch and visual canon: read `references/patch-and-visual-canon.md`.
- Project-source/source-zip handling: read `references/source-packages-and-project-sources.md`.
- Image-credit resource discipline and GPT/PSA/PIG actor split: read `references/image-generation-resource-discipline.md`.
- PPTX/proof/image-generation posture and PIG handoff boundary: read `references/presentation-production-posture.md`.
- Skill routing map, including PSA pre-vis and PIG production stack separation: read `references/adventures-skill-routing.md`.
- Quick map: read `references/doctrine-index.md`.

## Core rule

The canonical repo is `HarleyBartles/adventures-of-patch`. Patch is the constant protagonist unless Harley explicitly says otherwise. For ordinary GPT-side Adventures work, image generation credits are scarce production capacity and deterministic workflows exist to reduce failed image calls. Patch Storyboard Agent (PSA) is the deterministic pre-visualisation board actor: it creates storyboard, prompt-board, route/geometry, and planning/control PNGs without image generation. Patch Image Gen (PIG) is the production image actor: inside a bounded PIG production job, image generation is PIG's normal production medium. PSA boards and PIG candidates are both below final acceptance until GPT/Harley/project workflow accepts them in the correct lane. Use this skill for shared project doctrine, then route actual work to the most specific Adventures skill, PSA handoff, PIG stack, or repo playbook.

## Bootstrap relationship

System prompts should route Adventures work to `adventures-bootstrap-v1`, not duplicate this doctrine inline. `adventures-bootstrap-v1` decides which doctrine-bearing surface must be read for the task shape. This skill owns the shared Adventures lessons and reference map; it does not authorize repo mutation, image generation, dispatch, issue closure, deck building, or receipt creation by itself.

If a task is already inside a specialist Adventures skill, use this skill only for shared project posture that the specialist does not own. Prefer the most specific task skill for execution decisions.
