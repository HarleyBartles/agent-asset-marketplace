# Planning Pack Provenance

## Current projection

The `planning-pack` now projects first-party skills under
`sources/first_party/skills/`:

- `release-engineering`
- `requirements-elicitation`
- `estimation`
- `mermaid-diagramming`

## Retired upstream custody

The retired planning skills (`requirements-discovery`, `development-estimation`,
`release-prep`, `release-analysis`) were removed in Task 8; see
`provenance/ecc-domain-packs.md`.

## Projection surface

- Installable plugin projection: `codex-marketplace/plugins/planning-pack/`
- Generated install units: `generated/skill-zips/<skill-name>.zip`

## Boundary

The active `planning-pack` projection is sourced from first-party skills.
Retired upstream snapshots are no longer part of the active projection set.
