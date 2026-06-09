---
name: wild-bunch-domain-modeling
description: Apply Wild Bunch domain guidance for GameSession, player state, travel, clues, horses, and hidden culprit handling.
---

# Wild Bunch Domain Modeling

## Overview

Use this skill when the task touches live gameplay state or domain language.
Keep the model close to the current source and avoid introducing generic game
inventory abstractions that flatten the project-specific design.

## Rules

- `GameSession` is the live-play aggregate or root route unless the current
  source proves otherwise.
- Mutations should flow through the aggregate route, not ad hoc services.
- Wallet and Inventory are concrete player state.
- Hidden culprit truth stays internal.
- Clue, journal, and wanted-poster flows should remain stable unless directly
  scoped.
- Horse and saddle are separate inventory concepts.
- Horse condition vocabulary: Healthy, Hungry, Exhausted, Lame, Dead.
- Mounted travel needs a living, non-lame horse plus a saddle.
- Water should not become an ordinary stackable inventory good unless the
  design is explicitly revised.
- Travel is trending toward a journey or trail-day loop rather than a single
  immediate multi-day town leap.

## References

- [Wild Bunch domain notes](references/domain-model.md)
