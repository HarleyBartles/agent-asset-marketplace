# Codex Cortex Source Map

This bundle holds the MARK-172 `cqrs-event-sourcing` seed from a selective
retained snapshot of `NickCrew/Claude-Cortex`.

Retained upstream evidence:

- `sources/third_party/codex-cortex/upstream/README.md`
- `sources/third_party/codex-cortex/upstream/LICENSE`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/SKILL.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/cqrs-patterns.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/event-sourcing.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/event-store-tech.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/consistency-patterns.md`
- `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/best-practices.md`

First-party custody:

- `sources/first_party/skills/codex-cortex/intake.json`
- `sources/first_party/skills/codex-cortex/decisions.json`
- `sources/first_party/skills/codex-cortex/decisions.md`
- `provenance/codex-cortex.md`

Retained custody skill:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| cqrs-event-sourcing | `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/SKILL.md` | `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/SKILL.md` | Imported into the Codex Cortex custody plugin and retained as the canonical MARK-172 seed. |

The pack root is the installable custody home. It does not replace the
first-party import ledger or the downstream `architecture-pack` projection.
