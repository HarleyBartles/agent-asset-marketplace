---
name: skill-validator
description: validate skill fitness after skill-creator and before skill-packager. use for skill create, update, repair, package-handoff, or no-op review when semantic discovery, compact control-plane design, progressive references, mutation authorization gates, image-credit stewardship, deterministic execution contracts, script architecture and efficiency checks, protected targets, fake-ledger resistance, broken skill.zip install-card prevention, exact skill.zip naming, wrong-surface package handoff prevention, no-op repackaging prevention, bounded skill-read anti-loop rules, project-wrapper compatibility, or locked stack-order proof could affect whether a skill may be packaged or handed off.
version: v1
source_id: skill-validator-v1
source_path: gpt-skills/house-skills/skill-validator/SKILL.md
provenance_name: MARK-21 skill maintenance House Skills source slice
---
# Skill Validator

Use this skill to decide whether a skill source is good enough to package or hand off.

`skill-creator` is the authorship and spec source for good skills. This skill reviews the authored source after that step and before `skill-packager`. It does not author skill content, package archives, control queue cadence, or replace project-specific doctrine.

## Owned decision

Return one structured validation decision for the same target skill and staged source path that `skill-creator` authored.

Decisions:

- `pass`: packaging may proceed.
- `repair_required`: GPT must repair ordinary quality defects and rerun validation.
- `blocked_requires_harley`: an external input, authority, connector, or product choice is missing.
- `reject_before_handoff`: the target or concept is invalid, unsafe, immutable, redundant, or incompatible.

## Required references

Read `references/skill-update-stack-contract.md` before validating any create, update, repair, packaging, or handoff path. The locked order is `skill-creator`, then `skill-validator`, then `skill-packager`, then `skill-buster`. A validator pass is invalid without an `authored_by_skill_creator` token for the same skill name and staged source path.

Read `references/skill-quality-gate.md` before deciding. It owns the detailed review lenses: semantic discovery, compact `SKILL.md` control planes, progressive reference triggers, mutation-tool authorization, image-credit stewardship, deterministic execution recipes, fake-ledger resistance, broken install-card prevention, wrong-surface package handoff prevention, lifecycle poison, composition boundaries, and protected targets.

## Hard stops

Do not validate from prose-only evidence. If the creator token is absent, stale, source-path mismatched, or only asserted in narrative text, return `blocked_requires_harley` with `hard_red_stack_incomplete` and require restart from `skill-creator`.

Do not package, unzip, lint archives, or inspect package identity. That belongs to `skill-packager` after a structured pass.

Do not manage multi-skill queue state, batch cadence, or one-link-per-message handoff. That belongs to `skill-buster`.

Do not validate immutable system skills as update targets. Use them as specification sources only and redirect enforcement into mutable adjacent skills.

## Output contract

For create, update, repair, packaging, or handoff work, return this exact object shape:

```yaml
target_skill: <skill-name>
staged_source_path: <same source path reviewed>
reviewed_skill_creator_contract: true
reviewed_skill_quality_gate: true
decision: pass | repair_required | blocked_requires_harley | reject_before_handoff
handoff_allowed: true | false
blocking_reasons:
  - concrete reason, or [] only when decision is pass
required_repairs:
  - exact repair GPT should apply, or [] only when no repairs are required
validator_summary: <short basis for the decision>
next_required_step: skill-packager
```

For `pass`, `handoff_allowed` must be `true`, both reviewed fields must be `true`, and both arrays must be empty. For every other decision, `handoff_allowed` must be `false`.

For diagnostic-only reviews, add `diagnostic_only: true` and do not set `handoff_allowed: true`.
