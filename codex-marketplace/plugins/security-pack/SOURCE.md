# Source

This plugin projects the MARK-210 `threat-modeling-techniques` slice from the
retained Codex Cortex custody plugin into a Codex marketplace pack.

## Source custody

- Retained upstream root: `sources/third_party/codex-cortex/upstream/`
- Retained skill root:
  `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/`
- First-party ledgers:
  - `sources/first_party/skills/codex-cortex/intake.json`
  - `sources/first_party/skills/codex-cortex/decisions.json`
  - `sources/first_party/skills/codex-cortex/decisions.md`
- Provenance note: `provenance/codex-cortex.md`

## Projection surfaces

- Codex Cortex projection:
  `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/`
- Security Pack projection:
  `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/`
- Security Pack source map: `codex-marketplace/plugins/security-pack/references/source-map.md`
- Generated install unit:
  `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`

## Boundary

`threat-modeling-techniques` stays focused on pre-implementation risk framing,
attack surfaces, abuse cases, and security design choices. Generic compliance
theatre, infra security, repo governance, and audit-prep-only material stay out
of scope.

