# Harley Repo Ops Bundle

This plugin bundle packages the shared House Skills used for safe cross-repo
worker dispatch across Harley repos.

## Bundle contents

- first-party shared safety and dispatch skills under `skills/`
- provenance and source mapping in `SOURCE.md`
- bundle inventory and source mapping in `references/`

## Included skills

- `connector-safety`
- `gpt-base-doctrine`
- `work-mode-router`
- `worker-dispatch-linear`
- `linear`
- `tps-reporting`
- `tps-ingress`
- `don-logan-boundary`
- `crew`
- `crew-buster`

## Projection rules

- The bundle is a projection over canonical House Skills sources, not a new
  source of truth.
- `connector-safety` is included as the shared safety component for
  side-effecting connector/tool work.
- The bundle stays narrow and generic; project-specific skills belong in
  project packs like `adventures-pack` or `wild-bunch-project-pack`.

## Provenance

- Canonical source root: `gpt-skills/house-skills`
- Bundle source ledger: `sources/house-skills/decisions.json`
- Human registry: `sources/house-skills/decisions.md`
- Structured registry mirror: `sources/house-skills/intake.json`

The copied skill docs stay in their own directories and are exposed through the
plugin manifest only after they exist locally.
