# Synthetic Dogfood Plan

**Goal:** Provide a surface for the `iterative-review` fast-fix loop to find and fix a simple placeholder.

## Acceptance criteria

1. The plan file contains no `TBD`, `TODO`, or placeholder markers.
2. The plan file remains registered in `.agents/plans/INDEX.md`.
3. `py -3 tools/run.py ci --check` passes.
