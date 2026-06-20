# Ops Connectors Pack Provenance

## Summary

The Ops Connectors Pack projects 3 connector/ops skills from the ECC (affaan-m/ECC) upstream as part of MARK-241 ECC projection.

## Source Custody

### Third-Party Custody (ECC)

- **Upstream repository**: affaan-m/ECC
- **Upstream commit**: ceca28852e5b31edbbf66ebccc8fd163dd14208e
- **Source custody record**: `sources/third_party/ecc/upstream/source-custody.md`
- **Upstream manifest**: `sources/third_party/ecc/upstream/manifest.json`
- **Provenance note**: MARK-241 ECC projection
- **Projected skills**:
  - automation-audit-ops
  - email-ops
  - jira-integration

## Pack Shape

- **Codex plugin root**: `codex-marketplace/plugins/ops-connectors-pack/`
- **Skill root**: `codex-marketplace/plugins/ops-connectors-pack/skills/`
- **Generated install units**: `generated/skill-zips/ops-connectors-pack/<skill-name>/skill.zip`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `ops-connectors-pack`
- **Display name**: `Ops Connectors Pack`
- **Marketplace category**: `Productivity`
- **Content mode**: `verbatim` from ECC custody
- **Adaptation note**: Projected verbatim from retained ECC custody with MIT license attribution

## Rights and Attribution

- **Upstream source**: affaan-m/ECC (ECC connector/ops skills)
- **License**: MIT
- **Third-party projection**: MARK-241 ECC projection (ECC connector/ops skills)
- **Redistribution rights**: Per upstream license terms with third-party custody evidence

## Boundary

Only the 3 ECC connector/ops skills listed in MARK-241 are projected; other ECC skills are out of scope for this pack. The pack does not absorb language patterns, frontend, architecture, security, repo governance, CI, or generic engineering doctrine. The pack is a projection over retained ECC source custody, not a new source of truth.
