# MARK-171 Claude-Cortex Upstream Inventory Record

**Issue:** MARK-171
**Branch:** `codex/mark-171-claude-cortex-upstream-candidates`
**Starting main SHA:** `116120743d0060e58c88758a740ec58a63202ed2`
**Implementation commit SHA:** `c24cdd5e2e58d9ecb0e9f3b8c2c3e03f2f7d1e2a`
**PR URL:** [https://github.com/HarleyBartles/agent-asset-marketplace/pull/107](https://github.com/HarleyBartles/agent-asset-marketplace/pull/107)
**Publication state:** Published on the worker branch and tracked by draft PR #107 against `main`. This record captures the upstream source inventory and the first import-candidate selection for MARK-171. It does not implement a plugin or generate skill zips.

## Upstream evidence

- Upstream repository: `NickCrew/Claude-Cortex`
- Upstream default branch: `main`
- Upstream exact commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- Declared upstream license: MIT
- Evidence clone: shallow GitHub clone of `main` into the local temp workspace for inspection only

## Source surfaces inspected

- `LICENSE`
- `README.md`
- `skills/cqrs-event-sourcing/SKILL.md`
- `skills/event-driven-architecture/SKILL.md`
- `skills/database-design-patterns/SKILL.md`
- `skills/registry.yaml`
- `skills/skill-index.json`
- `skills/dependencies.map`
- `docs/reference/moved-readmes/skills.md`

## Candidate classification

| Candidate | Evidence inspected | Classification | Reason | MARK-172 recommendation |
| --- | --- | --- | --- | --- |
| `cqrs-event-sourcing` | `skills/cqrs-event-sourcing/SKILL.md`, `skills/dependencies.map`, `skills/registry.yaml`, `skills/skill-index.json` | `import now` | The skill is self-contained, explicitly targets CQRS/event sourcing/audit/temporal-query work, and the dependency map marks it as standalone. It is the narrowest evidence-backed seed candidate. | Use as the first seed for MARK-172. Keep the first slice focused on command/query separation, immutable events, projections, and snapshots. |
| `event-driven-architecture` | `skills/event-driven-architecture/SKILL.md`, `skills/registry.yaml`, `skills/skill-index.json` | `import later` | Broader than the CQRS/ES seed. It covers brokers, sagas, and eventual consistency, so it is useful support material after the core CQRS seed is in place. | Defer until MARK-172 has a concrete event-store/projection shape. |
| `database-design-patterns` | `skills/database-design-patterns/SKILL.md`, `skills/registry.yaml`, `skills/skill-index.json` | `import later` | It is relevant once the persistence model is concrete, but it is not required to justify the first `codex-cortex` seed candidate. | Defer until the storage and indexing requirements are known. |

## `cqrs-event-sourcing` seed decision

`cqrs-event-sourcing` is suitable as MARK-172's first implementation seed.

The upstream evidence supports that decision because:

- it is a standalone skill, not part of a dependency chain;
- it is narrowly scoped around the exact patterns named by the issue packet;
- its references already break the work into predictable slices: CQRS patterns, event sourcing, event-store technology, consistency, and best practices;
- the skill's own guidance aligns with an incremental first slice rather than a whole-repo import.

## MARK-172 constraints

If MARK-172 uses `cqrs-event-sourcing` as the first seed, the implementation slice should stay within these boundaries:

- keep command and query concerns separate from the start;
- model events as immutable facts and keep event names in past tense;
- define projections/read models as the first query surface, not a full marketplace import;
- keep event-store and snapshot support explicit in the scope;
- defer adjacent concerns such as broker choreography and broader database design until the seed is stable.

## Non-goals

- No plugin implementation.
- No generated zips.
- No whole-repo import.
- No `codex-cortex` plugin creation in this issue.
- No `architecture-superpowers` creation in this issue.

## Validation

- `git ls-remote --symref https://github.com/NickCrew/Claude-Cortex.git HEAD`
  - Result: upstream default branch resolved to `main` and the exact HEAD commit resolved to `7892d00e7cb6adf00144a535103b930c772fb2c0`.
- `git ls-remote --heads https://github.com/NickCrew/Claude-Cortex.git`
  - Result: confirmed the upstream branch set and the `main` head.
- `git clone --depth 1 --branch main https://github.com/NickCrew/Claude-Cortex.git $env:TEMP\claude-cortex-upstream`
  - Result: shallow source clone created for inspection.
- `git diff --check`
  - Result: pending after final file edits.

## Files changed

- `docs/superpowers/plans/2026-06-17-mark-171-claude-cortex-upstream-inventory.md`
- `docs/superpowers/records/2026-06-17-mark-171-claude-cortex-upstream-inventory.md`

## Notes

- No marketplace manifests were changed.
- No generated skill zips were produced.
- No plugin implementation files were added.
