# Repo Worker Pack Provenance

## Origin

- Local source path: `codex-marketplace/plugins/<plugin>/skills/repo-worker-base`
- Scope: first-party repo hygiene entrypoint for Codex workers in Harley's workspace
- Marketplace package: `codex-marketplace/plugins/repo-worker-pack/`

## Preservation notes

- The marketplace projection keeps the plugin thin and market-canonical.
- No upstream third-party source is imported into the baseline bundle.
- The plugin content is limited to fresh-main discipline, worker branching,
 validation evidence, publication reporting, and the generic safety/proof
 helpers that repo-backed work needs.
- `base-doctrine` is projected here from the canonical first-party source at
 `codex-marketplace/plugins/<plugin>/skills/base-doctrine/` so cross-project doctrine,
 evidence honesty, and output-shape guards travel with the worker pack.
- `work-mode-router` was previously projected here from the canonical first-party
 source at `codex-marketplace/plugins/<plugin>/skills/work-mode-router/` but was retired in
 2026-08 as part of the superpowers-plus consolidation. Worker route
 classification is now owned by `using-superpowers-plus`.
- `linear-issue-shaping` is projected here from the canonical first-party
 source at `codex-marketplace/plugins/<plugin>/skills/linear-issue-shaping/` so Linear worker
 readiness and route-state handling stay on the repo-facing worker surface.
- `boring-loop` was previously projected here from the canonical first-party
 source at `codex-marketplace/plugins/<plugin>/skills/boring-loop/` but was retired on
 2026-07-16 as part of the buster framework consolidation. The loop cadence
 and finish-line enforcement functions are now covered by
 `verification-before-completion` and `repo-worker-base`.
- `connector-safety` is projected here from the canonical first-party source
 at `codex-marketplace/plugins/<plugin>/skills/connector-safety/` so connector and tool
 writes stay narrow, auditable, and recoverable.
- `using-github-mcp` is projected here from the canonical first-party source
 at `codex-marketplace/plugins/<plugin>/skills/using-github-mcp/` so GitHub surface selection,
 publication proof, and merge/readiness checks have a canonical non-House-Skills
 home.
- `unslop-profiles` is projected here from the canonical first-party source at
 `codex-marketplace/plugins/<plugin>/skills/unslop-profiles/` so worker-facing anti-slop profiles
 are available on the repo baseline surface.
- `context-safety` is projected here from the canonical first-party
 source at `codex-marketplace/plugins/<plugin>/skills/context-safety/` so safer
 large text write guidance rides with the repo baseline.
- `cleanup-custody` is projected here from the canonical first-party
 source at `codex-marketplace/plugins/<plugin>/skills/cleanup-custody/` so workspace
 and repository surface custody classification rides with the repo
 baseline.
- `risk-gates` is projected here from the canonical first-party source at
 `codex-marketplace/plugins/<plugin>/skills/risk-gates/` so generic pre-action risk gates
 remain available on the repo-facing worker surface.
- `writing-with-clarity` is projected here from the canonical first-party
 source at `codex-marketplace/plugins/<plugin>/skills/writing-with-clarity/`; its compact
 references route human-facing prose tasks while the bundled 1918 HTML remains
 a reference-only fallback with its upstream custody record.
