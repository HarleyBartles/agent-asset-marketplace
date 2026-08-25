# Source

This plugin projects the first-party repo worker baseline skills.

## Boundary
- The first-party repo worker skills stay bundled alongside the
  compositional repo-worker entrypoint and supporting workflow skills.
- The bundle stays narrow, first-party only, and aligns to the current manifest
  repo worker baseline without absorbing broader Superpowers+ or other workflow packs.
- Writing workflow custody belongs to `writing-pack`; generic anti-slop engine
  and profile custody belongs to `unslop-plus`. This plugin does not duplicate
  either source tree.

## Provenance

- Local source path: `codex-marketplace/plugins/<plugin>/skills/repo-worker-base`
- Scope: first-party repo hygiene entrypoint for Codex workers in the asset marketplace workspace
- Marketplace package: `codex-marketplace/plugins/repo-worker-pack/`

### Preservation notes

- The marketplace bundle keeps the plugin thin and market-canonical.
- No upstream third-party source is imported into the baseline bundle.
- The plugin content is limited to fresh-main discipline, worker branching,
  validation evidence, publication reporting, and the generic safety/proof
  helpers that repo-backed work needs.
- `base-doctrine` is bundled here from the canonical first-party source at
  `codex-marketplace/plugins/<plugin>/skills/base-doctrine/` so cross-project doctrine,
  evidence honesty, and output-shape guards travel with the worker pack.
- `work-mode-router` was previously bundled here from the canonical first-party
  source at `codex-marketplace/plugins/<plugin>/skills/work-mode-router/` but was retired in
  2026-08 as part of the superpowers-plus consolidation. Worker route
  classification is now owned by `using-superpowers-plus`.
- `linear-issue-shaping` is bundled here from the canonical first-party
  source at `codex-marketplace/plugins/<plugin>/skills/linear-issue-shaping/` so Linear worker
  readiness and route-state handling stay on the repo-facing worker surface.
- `boring-loop` was previously bundled here from the canonical first-party
  source at `codex-marketplace/plugins/<plugin>/skills/boring-loop/` but was retired on
  2026-07-16 as part of the buster framework consolidation. The loop cadence
  and finish-line enforcement functions are now covered by
  `verification-before-completion` and `repo-worker-base`.
- `connector-safety` is bundled here from the canonical first-party source
  at `codex-marketplace/plugins/<plugin>/skills/connector-safety/` so connector and tool
  writes stay narrow, auditable, and recoverable.
- `using-github-mcp` is bundled here from the canonical first-party source
  at `codex-marketplace/plugins/<plugin>/skills/using-github-mcp/` so GitHub surface selection,
  publication proof, and merge/readiness checks have a canonical non-House-Skills
  home.
- `context-safety` is bundled here from the canonical first-party
  source at `codex-marketplace/plugins/<plugin>/skills/context-safety/` so safer
  large text write guidance rides with the repo baseline.
- `cleanup-custody` is bundled here from the canonical first-party
  source at `codex-marketplace/plugins/<plugin>/skills/cleanup-custody/` so workspace
  and repository surface custody classification rides with the repo
  baseline.
- `risk-gates` is bundled here from the canonical first-party source at
  `codex-marketplace/plugins/<plugin>/skills/risk-gates/` so generic pre-action risk gates
  remain available on the repo-facing worker surface.
