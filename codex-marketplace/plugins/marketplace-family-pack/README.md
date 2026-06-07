# Marketplace Family Pack

This plugin bundle is the market-consumable output for MARK-59.

It adapts the upstream `jeremylongshore/claude-code-plugins-plus-skills`
family surface into repo-held Codex skills that can be consumed from the
`codex-marketplace/` source tree.

## Bundle contents

- `skills/skill-enhancers/SKILL.md`
- `skills/productivity/SKILL.md`
- `skills/ai-agency/SKILL.md`
- `skills/ai-ml/SKILL.md`
- `skills/design/SKILL.md`
- `skills/api-development/SKILL.md`
- `skills/database/SKILL.md`
- `skills/devops/SKILL.md`
- `skills/performance/SKILL.md`
- `skills/security/SKILL.md`
- `skills/testing/SKILL.md`
- `skills/enterprise-workflows-curriculum/SKILL.md`

## Provenance

Upstream source:

- `jeremylongshore/claude-code-plugins-plus-skills`
- pinned commit `e773501f1dfb409fc71fccdaf6ac2898fedf66d6`

Source custody and license evidence are recorded in `SOURCE.md` and in the
repository provenance note for MARK-59.

## Consumption

The bundle is discoverable through `codex-marketplace/manifest.json` as a local
plugin source. It is meant to be installed or mirrored as a real plugin asset,
not treated as a documentation-only record.
