# Domain Notes

- Prefer `GameSession` as the live-play aggregate root unless the source proves another root.
- Route mutations through the aggregate so invariants stay in one place.
- Keep wallet and inventory concrete.
- Preserve the project's internal hidden-culprit truth.
- Keep clue, journal, and wanted-poster flows stable unless the scope says otherwise.
- Keep horse and saddle separate.
- Mounted travel requires a living, non-lame horse and a saddle.
- Do not turn water into a generic stackable good by accident.
- Treat travel as a journey or trail-day loop, not a single instant leap.
- Prefer journey state that can represent origin, destination, route profile, remaining days or distance, travel mode, player condition, horse condition, resources, and pending encounter state.
- Advance travel by trail day and pause when a player decision is required.
