# Source

This pack projects the MARK-251 ECC connector/ops skills slice from retained ECC source custody into a Codex marketplace pack.

## Source custody

### ECC retained skills

- Retained upstream root: `sources/third_party/ecc/upstream/`
- Retained skill roots:
  - `sources/third_party/ecc/upstream/skills/api-connector-builder/`
  - `sources/third_party/ecc/upstream/skills/automation-audit-ops/`
  - `sources/third_party/ecc/upstream/skills/customer-billing-ops/`
  - `sources/third_party/ecc/upstream/skills/email-ops/`
  - `sources/third_party/ecc/upstream/skills/finance-billing-ops/`
  - `sources/third_party/ecc/upstream/skills/google-workspace-ops/`
  - `sources/third_party/ecc/upstream/skills/jira-integration/`
  - `sources/third_party/ecc/upstream/skills/messages-ops/`
  - `sources/third_party/ecc/upstream/skills/unified-notifications-ops/`

## First-party ledgers and provenance

### ECC

- Upstream manifest: `sources/third_party/ecc/upstream/manifest.json`
- Categorization: `docs/superpowers/plans/mark-241-skill-categorization.json`
- Provenance note: `provenance/ecc.md`

## Projection surfaces

- Codex plugin root: `codex-marketplace/plugins/ops-connectors-pack/`
- Skill root: `codex-marketplace/plugins/ops-connectors-pack/skills/`
- Skill roots:
  - `codex-marketplace/plugins/ops-connectors-pack/skills/api-connector-builder/`
  - `codex-marketplace/plugins/ops-connectors-pack/skills/automation-audit-ops/`
  - `codex-marketplace/plugins/ops-connectors-pack/skills/customer-billing-ops/`
  - `codex-marketplace/plugins/ops-connectors-pack/skills/email-ops/`
  - `codex-marketplace/plugins/ops-connectors-pack/skills/finance-billing-ops/`
  - `codex-marketplace/plugins/ops-connectors-pack/skills/google-workspace-ops/`
  - `codex-marketplace/plugins/ops-connectors-pack/skills/jira-integration/`
  - `codex-marketplace/plugins/ops-connectors-pack/skills/messages-ops/`
  - `codex-marketplace/plugins/ops-connectors-pack/skills/unified-notifications-ops/`

## Generated install units

- `generated/skill-zips/ops-connectors-pack/api-connector-builder/skill.zip`
- `generated/skill-zips/ops-connectors-pack/automation-audit-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/customer-billing-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/email-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/finance-billing-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/google-workspace-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/jira-integration/skill.zip`
- `generated/skill-zips/ops-connectors-pack/messages-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/unified-notifications-ops/skill.zip`

## Boundary

Only the retained connector, workspace operations, communication, and business-ops workflow guidance is kept here. The pack does not absorb language patterns, frontend, architecture, security, repo governance, CI, or generic engineering doctrine. The pack is a projection over retained ECC source custody, not a new source of truth.
