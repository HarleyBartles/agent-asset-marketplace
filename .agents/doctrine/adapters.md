
## Scope

`adapters/`

This scope covers adapter surfaces that sit between upstream third-party source and the marketplace plugin shape.

Defer to the repository root `AGENTS.md` for global repo doctrine.

Adapters are source/projection boundaries, not source custody. Keep source truth in `codex-marketplace/plugins/<plugin>/skills/` and provenance, and keep generated or mechanically synchronized outputs derived from that truth.

The marketplace currently runs two lanes only: first-party source under `codex-marketplace/plugins/<plugin>/skills/` (edited directly) and retained third-party material recorded in `provenance/` (verbatim custody with an adaptation path). The historical `overlay.yaml` adaptation machinery has been retired; do not reintroduce `overlay.yaml` line-edit files. If a third-party skill needs adaptation, update the plugin skill tree or the generator instead of adding an overlay surface.

When an adapter needs both Bash and PowerShell script siblings, keep both implementations together in the adapter surface so agents can choose the runtime they have available.

When an adapter changes review or SDD output placement, make the plan-scoped path explicit, such as `sdd/<plan_name>/`, instead of leaving the location implicit.

Do not insert `INDEX.md` into skill roots. Use generated navigation only at container boundaries.
