# Codex Cortex Source Map

This bundle holds the MARK-172 `cqrs-event-sourcing` seed, the MARK-200
`event-driven-architecture` import, the MARK-201
`database-design-patterns` import, the MARK-204 `api-design-patterns` import,
and the MARK-205 `openapi-specification` import from a selective retained
snapshot of `NickCrew/Claude-Cortex`.

Retained upstream evidence:

- `sources/third_party/codex-cortex/upstream/README.md`
- `sources/third_party/codex-cortex/upstream/LICENSE`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/cqrs-patterns.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/event-sourcing.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/event-store-tech.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/consistency-patterns.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/best-practices.md`
- `sources/third_party/codex-cortex/upstream/skills/event-driven-architecture/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/event-driven-architecture/references/event-fundamentals.md`
- `sources/third_party/codex-cortex/upstream/skills/event-driven-architecture/references/event-sourcing.md`
- `sources/third_party/codex-cortex/upstream/skills/event-driven-architecture/references/cqrs.md`
- `sources/third_party/codex-cortex/upstream/skills/event-driven-architecture/references/message-brokers.md`
- `sources/third_party/codex-cortex/upstream/skills/event-driven-architecture/references/saga-pattern.md`
- `sources/third_party/codex-cortex/upstream/skills/event-driven-architecture/references/choreography-orchestration.md`
- `sources/third_party/codex-cortex/upstream/skills/event-driven-architecture/references/eventual-consistency.md`
- `sources/third_party/codex-cortex/upstream/skills/event-driven-architecture/references/best-practices.md`
- `sources/third_party/codex-cortex/upstream/skills/database-design-patterns/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/database-design-patterns/references/core-principles.md`
- `sources/third_party/codex-cortex/upstream/skills/database-design-patterns/references/schema-design-patterns.md`
- `sources/third_party/codex-cortex/upstream/skills/database-design-patterns/references/indexing-strategies.md`
- `sources/third_party/codex-cortex/upstream/skills/database-design-patterns/references/partitioning-patterns.md`
- `sources/third_party/codex-cortex/upstream/skills/database-design-patterns/references/replication-patterns.md`
- `sources/third_party/codex-cortex/upstream/skills/database-design-patterns/references/query-optimization.md`
- `sources/third_party/codex-cortex/upstream/skills/api-design-patterns/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/api-design-patterns/references/design-process.md`
- `sources/third_party/codex-cortex/upstream/skills/api-design-patterns/validation/rubric.yaml`
- `sources/third_party/codex-cortex/upstream/skills/openapi-specification/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/openapi-specification/references/spec-patterns.md`
- `sources/third_party/codex-cortex/upstream/skills/openapi-specification/validation/rubric.yaml`

First-party custody:

- `sources/first_party/skills/codex-cortex/intake.json`
- `sources/first_party/skills/codex-cortex/decisions.json`
- `sources/first_party/skills/codex-cortex/decisions.md`
- `provenance/codex-cortex.md`

Retained custody skill:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| cqrs-event-sourcing | `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/SKILL.md` | `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/SKILL.md` | Imported into the Codex Cortex custody plugin and retained as the canonical MARK-172 seed. |
| event-driven-architecture | `sources/third_party/codex-cortex/upstream/skills/event-driven-architecture/SKILL.md` | `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/SKILL.md` | Imported into the Codex Cortex custody plugin and retained as the MARK-200 architecture follow-on. |
| database-design-patterns | `sources/third_party/codex-cortex/upstream/skills/database-design-patterns/SKILL.md` | `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/SKILL.md` | Imported into the Codex Cortex custody plugin and retained as the MARK-201 database guidance follow-on. |
| api-design-patterns | `sources/third_party/codex-cortex/upstream/skills/api-design-patterns/SKILL.md` | `codex-marketplace/plugins/codex-cortex/skills/api-design-patterns/SKILL.md` | Imported into the Codex Cortex custody plugin and retained as the MARK-204 contract-doctrine follow-on. |
| openapi-specification | `sources/third_party/codex-cortex/upstream/skills/openapi-specification/SKILL.md` | `codex-marketplace/plugins/codex-cortex/skills/openapi-specification/SKILL.md` | Imported into the Codex Cortex custody plugin and retained as the MARK-205 OpenAPI companion follow-on. |

The pack root is the installable custody home. It does not replace the
first-party import ledger or the downstream `architecture-pack` and
`api-contracts-pack` projections.
