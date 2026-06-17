# Architecture Pack Source Map

This bundle projects the MARK-172 `cqrs-event-sourcing` seed, the MARK-200
`event-driven-architecture` candidate, and the MARK-201
`database-design-patterns` candidate from the retained Codex Cortex custody
plugin.

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
- `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/SKILL.md`
- `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/references/event-fundamentals.md`
- `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/references/event-sourcing.md`
- `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/references/cqrs.md`
- `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/references/message-brokers.md`
- `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/references/saga-pattern.md`
- `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/references/choreography-orchestration.md`
- `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/references/eventual-consistency.md`
- `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/references/best-practices.md`
- `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/SKILL.md`
- `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/references/core-principles.md`
- `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/references/schema-design-patterns.md`
- `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/references/indexing-strategies.md`
- `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/references/partitioning-patterns.md`
- `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/references/replication-patterns.md`
- `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/references/query-optimization.md`

First-party custody:

- `sources/first_party/skills/codex-cortex/intake.json`
- `sources/first_party/skills/codex-cortex/decisions.json`
- `sources/first_party/skills/codex-cortex/decisions.md`
- `provenance/codex-cortex.md`

Projected pack skill:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| cqrs-event-sourcing | `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/SKILL.md` | `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/SKILL.md` | Mirrored unchanged from the Codex Cortex custody plugin into the installable Architecture Pack. |
| event-driven-architecture | `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/SKILL.md` | `codex-marketplace/plugins/architecture-pack/skills/event-driven-architecture/SKILL.md` | Mirrored unchanged from the Codex Cortex custody plugin into the installable Architecture Pack. |
| database-design-patterns | `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/SKILL.md` | `codex-marketplace/plugins/architecture-pack/skills/database-design-patterns/SKILL.md` | Mirrored unchanged from the Codex Cortex custody plugin into the installable Architecture Pack. |

The pack root is an installable Codex plugin projection. It does not replace
the `codex-cortex` custody plugin or the first-party import ledger.
