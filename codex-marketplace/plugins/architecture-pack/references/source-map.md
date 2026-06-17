# Architecture Pack Source Map

This bundle projects the MARK-172 `cqrs-event-sourcing` seed from a selective
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

Projected pack skill:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| cqrs-event-sourcing | `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/SKILL.md` | `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/SKILL.md` | Mirrored unchanged from the retained Codex Cortex custody surface into the installable Architecture Pack. |

The pack root is an installable Codex plugin projection. It does not replace
the `codex-cortex` custody surface or the first-party import ledger.

