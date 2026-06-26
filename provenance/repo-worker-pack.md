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
- `boring-loop` is projected here from the canonical first-party source at
  `sources/first_party/skills/boring-loop/` and keeps the same retained loop
  cadence, readiness, queue grooming, and specialist-routing doctrine on the
  worker-facing plugin surface.
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
- `safe-large-file-writing` is projected here from the canonical first-party
  source at `sources/first_party/skills/safe-large-file-writing/` so safer
  large text write guidance rides with the repo baseline.
