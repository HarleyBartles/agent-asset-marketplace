# Ops Connectors Pack

This plugin bundle projects retained ECC connector/ops skills into an installable Codex marketplace pack.

## Bundle contents

- ECC connector/ops skills:
  - `automation-audit-ops`
  - `email-ops`
  - `jira-integration`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- `automation-audit-ops` carries automation audit operations patterns and guidance.
- `email-ops` carries email operations patterns and best practices.
- `jira-integration` carries Jira integration patterns and workflow guidance.
- The pack is sourced from retained `affaan-m/ECC` connector/ops skills under the retained `ecc` custody root.
- The bundle does not own language patterns, frontend, architecture, security, repo governance, CI, or generic engineering doctrine.
- The bundle is a projection over retained source custody, not a new source of truth.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/ops-connectors-pack/automation-audit-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/email-ops/skill.zip`
- `generated/skill-zips/ops-connectors-pack/jira-integration/skill.zip`

and can be installed directly from those artifacts.
