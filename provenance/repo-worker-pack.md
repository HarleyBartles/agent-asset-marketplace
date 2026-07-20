# Repo Worker Pack Provenance

## Origin

- Local source path: `sources/first_party/skills/repo-worker-base`
- Scope: first-party repo hygiene entrypoint for Codex workers in Harley's workspace
- Marketplace package: `codex-marketplace/plugins/repo-worker-pack/`

## Preservation notes

- The marketplace projection keeps the plugin thin and market-canonical.
- No upstream third-party source is imported into the baseline bundle.
- The plugin content is limited to fresh-main discipline, worker branching,
  validation evidence, publication reporting, and the generic safety/proof
  helpers that repo-backed work needs.
- `base-doctrine` is projected here from the canonical first-party source at
  `sources/first_party/skills/base-doctrine/` so cross-project doctrine,
  evidence honesty, and output-shape guards travel with the worker pack.
- `work-mode-router` is projected here from the canonical first-party source at
  `sources/first_party/skills/work-mode-router/` so durable worker route
  classification stays on the repo-facing worker surface.
- `linear-issue-shaping` is projected here from the canonical first-party
  source at `sources/first_party/skills/linear-issue-shaping/` so Linear worker
  readiness and route-state handling stay on the repo-facing worker surface.
- `boring-loop` was previously projected here from the canonical first-party
  source at `sources/first_party/skills/boring-loop/` but was retired on
  2026-07-16 as part of the buster framework consolidation. The loop cadence
  and finish-line enforcement functions are now covered by
  `verification-before-completion` and `repo-worker-base`.
- `connector-safety` is projected here from the canonical first-party source
  at `sources/first_party/skills/connector-safety/` so connector and tool
  writes stay narrow, auditable, and recoverable.
- `github-operations` is projected here from the canonical first-party source
  at `sources/first_party/skills/github-operations/` so GitHub evidence,
  publication proof, and merge/readiness checks have a canonical non-House-Skills
  home.
- `unslop-plus` is projected here from the canonical first-party source at
  `sources/first_party/skills/unslop-plus/` so worker-facing anti-slop profiles
  are available on the repo baseline surface.
- `context-safety` is projected here from the canonical first-party
  source at `sources/first_party/skills/context-safety/` so safer
  large text write guidance rides with the repo baseline.
- `cleanup-custody` is projected here from the canonical first-party
  source at `sources/first_party/skills/cleanup-custody/` so workspace
  and repository surface custody classification rides with the repo
  baseline.
- `risk-gates` is projected here from the canonical first-party source at
  `sources/first_party/skills/risk-gates/` so generic pre-action risk gates
  remain available on the repo-facing worker surface.
- `writing-with-clarity` is projected here from the canonical first-party
  source at `sources/first_party/skills/writing-with-clarity/`; its compact
  references route human-facing prose tasks while the bundled 1918 HTML remains
  a reference-only fallback with its upstream custody record.
