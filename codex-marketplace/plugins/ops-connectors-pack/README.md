# Ops Connectors Pack

This plugin bundle projects retained ECC connector/ops skills into an installable Codex marketplace pack.

## Bundle contents

- ECC connector/ops skills:
  - `api-connector-builder`
  - `automation-audit-ops`
  - `customer-billing-ops`
  - `email-ops`
  - `finance-billing-ops`
  - `google-workspace-ops`
  - `jira-integration`
  - `messages-ops`
  - `unified-notifications-ops`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- `api-connector-builder` carries API connector builder patterns.
- `automation-audit-ops` carries automation audit operations patterns and guidance.
- `customer-billing-ops` carries customer billing operations patterns.
- `email-ops` carries email operations patterns and best practices.
- `finance-billing-ops` carries finance billing operations patterns.
- `google-workspace-ops` carries Google Workspace operations patterns.
- `jira-integration` carries Jira integration patterns and workflow guidance.
- `messages-ops` carries messaging operations patterns.
- `unified-notifications-ops` carries unified notifications operations patterns.
- The pack is sourced from retained `affaan-m/ECC` connector/ops skills under the retained `ecc` custody root.
- The bundle does not own language patterns, frontend, architecture, security, repo governance, CI, or generic engineering doctrine.
- The bundle is a projection over retained source custody, not a new source of truth.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/ops-connectors-pack/api-connector-builder/skill.zip`
- `generated/skill-zips/ops-connectors-pack/automation-audit-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/customer-billing-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/email-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/finance-billing-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/google-workspace-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/jira-integration/skill.zip`
- `generated/skill-zips/ops-connectors-pack/messages-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/unified-notifications-ops/skill.zip`

and can be installed directly from those artifacts.
