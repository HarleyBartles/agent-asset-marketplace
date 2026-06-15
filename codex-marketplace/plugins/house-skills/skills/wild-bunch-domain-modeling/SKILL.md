---
name: wild-bunch-domain-modeling
description: apply Wild Bunch project-scoped domain guidance when work touches gameplay state, GameSession aggregate boundaries, player wallet or inventory, clue or journal flows, wanted posters, hidden culprit truth, horse and saddle rules, water handling, town or trail travel, journey state, or trail-day progression. Use to keep C#/.NET game-domain modeling aligned with live repo source and to prevent generic inventory, service, database, or travel abstractions from flattening Wild Bunch-specific design.
---

# Wild Bunch Domain Modeling

## Overview

Use this skill when the task touches live gameplay state or Wild Bunch domain language. Keep the model close to the current source and avoid introducing generic game abstractions that flatten the project-specific design.

## Rules

- Treat `GameSession` as the live-play aggregate root or aggregate route unless the current source proves otherwise.
- Route game mutations through the aggregate route, not through ad hoc services that mutate state elsewhere.
- Keep Wallet and Inventory as concrete player state; do not reintroduce generic supplies.
- Keep hidden culprit truth internal.
- Keep clue, journal, and wanted-poster flows stable unless the current task directly changes them.
- Keep horse and saddle as separate inventory concepts.
- Use the horse condition vocabulary: Healthy, Hungry, Exhausted, Lame, Dead.
- Require a living, non-lame horse plus saddle for mounted travel.
- Do not make water an ordinary stackable inventory good unless the design is explicitly revised.
- Treat travel as moving toward an active journey or trail-day loop, not a single immediate multi-day town leap.
- Model journey state with origin, destination, route profile, remaining days or distance, travel mode, player and horse condition, resources, and pending encounter state when the slice needs that detail.
- Advance travel one trail day at a time and pause when player choice is needed.
- When gameplay decision loops or initial world state are in play, classify difficulty, entropy, and seeded setup as in scope, explicitly deferred, or irrelevant before choosing structure.
- Use the installed `wild-bunch-project-doctrine` skill reference when domain modeling needs the world-start identity or randomness boundary.

## Reference trigger

Read `references/domain-model.md` when a task needs the compact domain anchor list for implementation, issue shaping, review, or validation. Do not reread the reference repeatedly after the relevant domain constraints have been extracted.
Consult the installed `wild-bunch-project-doctrine` skill reference when a task touches initial world state, difficulty envelopes, entropy, or seed identity.

## Composition

Use repository or GitHub evidence for current source truth before claiming live code state. This skill supplies domain constraints only; it does not verify branches, commits, PRs, tests, package state, issue closure, or worker reports.
