# Architecture Pack Source Map

This bundle projects the MARK-172 `cqrs-event-sourcing` seed from the retained
Codex Cortex custody plugin.

Retained custody evidence:

- `codex-marketplace/plugins/codex-cortex/README.md`
- `codex-marketplace/plugins/codex-cortex/SOURCE.md`
- `codex-marketplace/plugins/codex-cortex/references/bundle-manifest.json`
- `codex-marketplace/plugins/codex-cortex/references/source-map.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/SKILL.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/references/cqrs-patterns.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/references/event-sourcing.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/references/event-store-tech.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/references/consistency-patterns.md`
- `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/references/best-practices.md`

First-party custody:

- `sources/first_party/skills/codex-cortex/intake.json`
- `sources/first_party/skills/codex-cortex/decisions.json`
- `sources/first_party/skills/codex-cortex/decisions.md`
- `provenance/codex-cortex.md`

Projected pack skill:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| cqrs-event-sourcing | `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/SKILL.md` | `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/SKILL.md` | Mirrored unchanged from the Codex Cortex custody plugin into the installable Architecture Pack. |

The pack root is an installable Codex plugin projection. It does not replace
the `codex-cortex` custody plugin or the first-party import ledger.
