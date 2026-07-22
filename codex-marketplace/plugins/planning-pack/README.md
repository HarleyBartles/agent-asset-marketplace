# Planning Pack

This plugin bundle projects first-party planning skills into an installable
Codex marketplace pack.

## Bundle contents

### First-party skills
- `release-engineering`
- `requirements-elicitation`
- `estimation`
- `mermaid-diagramming`

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary
- `release-engineering` covers CI/CD, container and release workflows, rollback, and deployment patterns.
- `requirements-elicitation` covers stakeholder interviews, user stories, acceptance criteria, validation, and traceability.
- `estimation` covers effort estimation, confidence ranges, and risk buffers.
- `mermaid-diagramming` carries diagramming guidance for planning and architecture.
- The bundle projects first-party source custody under `sources/first_party/skills/`.
- Retired upstream snapshots were removed in Task 8; see `provenance/ecc-domain-packs.md`.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/release-engineering.zip`
- `generated/skill-zips/requirements-elicitation.zip`
- `generated/skill-zips/estimation.zip`
- `generated/skill-zips/mermaid-diagramming.zip`

and can be installed directly from those artifacts.
