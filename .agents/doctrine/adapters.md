
## Scope

`adapters/`

This scope covers adapter surfaces that sit between source custody and the marketplace projection layer.

Defer to the repository root `AGENTS.md` for global repo doctrine.

Adapters are source/projection boundaries, not source custody. Keep source truth in `sources/` and keep generated or mechanically synchronized outputs derived from that truth.

The marketplace currently runs two lanes only: first-party source under `sources/first_party/**` (edited directly) and retained third-party source under `sources/third_party/**` (verbatim custody). The historical `overlay.yaml` adaptation machinery has been retired; do not reintroduce adapter overlays or `overlay.yaml` line-edit files. If a third-party skill needs adaptation, update the projection generator instead of adding an overlay surface.

When an adapter needs both Bash and PowerShell script siblings, keep both implementations together in the adapter surface so agents can choose the runtime they have available.

When an adapter changes review or SDD output placement, make the plan-scoped path explicit, such as `sdd/<plan_name>/`, instead of leaving the location implicit.

Do not insert `INDEX.md` into skill roots. Use generated navigation only at container boundaries.
