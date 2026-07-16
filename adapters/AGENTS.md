# AGENTS.md

Scope: `adapters/`

This scope covers projection overlays and adapter surfaces.

Defer to the repository root `AGENTS.md` for global repo doctrine.

Adapters are source/projection boundaries, not source custody. Keep source
truth in `sources/` and keep generated or mechanically synchronized outputs
derived from that truth.

Use adapter overlays to express deltas from immutable third-party source.
Do not edit `sources/third_party/**` for adapted content; declare the change
in the adapter and regenerate the projected surface instead.

First-party source under `sources/first_party/**` is mutable directly. Update
it in place when the requirement belongs to repo-owned source rather than an
overlay.

Prefer `overlay.yaml` line edits for bounded projected text changes. Use
explicit `edits` entries when a targeted replacement is enough, and only fall
back to full-file replacement when a line edit cannot express the change
cleanly.

When an adapter needs both Bash and PowerShell script siblings, keep both
implementations together in the adapter surface so agents can choose the
runtime they have available.

When an adapter changes review or SDD output placement, make the plan-scoped
path explicit, such as `sdd/<plan_name>/`, instead of leaving the location
implicit.

Do not insert `INDEX.md` into skill roots or overlay roots. Use generated
navigation only at container boundaries.

## Routing pointers

- `../docs/custody-and-projection-doctrine.md` before adapter or overlay work
- `../.agents/docs/mesh-policy.md` before changing adapter routing or generated navigation assumptions
