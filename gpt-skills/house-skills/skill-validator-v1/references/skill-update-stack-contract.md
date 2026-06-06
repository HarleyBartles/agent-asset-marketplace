# Skill Update Stack Contract

Use this contract for every skill create, update, repair, packaging, or package-handoff task.

## Locked order

The approved stack order is:

```text
skill-creator, then skill-validator-v1, then skill-packager-v1, then skill-buster-v0.1
```

Do not use these skills as independent substitutes for one another during skill update work. A later stack step cannot
claim that an earlier step happened from memory, narrative summary, expected workflow state, or a prose note that says a
prior step was done.

Reading a skill's `SKILL.md` proves only that the instructions were loaded. It is not evidence that the step completed.
A completed step must leave the structured object described below, for the same skill name and source path.

## Required state objects

Each transition needs a concrete object that the next step can inspect or cite.

### `authored_by_skill_creator`

```yaml
target_skill: <skill-name>
staged_source_path: <absolute-or-workspace-source-path>
authored_by_skill_creator: true
edit_summary:
  - <specific content/resource edit>
next_required_step: skill-validator-v1
```

### `validated_by_skill_validator`

```yaml
target_skill: <skill-name>
staged_source_path: <same source path reviewed>
reviewed_skill_creator_contract: true
reviewed_skill_quality_gate: true
decision: pass | repair_required | blocked_requires_harley | reject_before_handoff
handoff_allowed: true | false
blocking_reasons:
  - <empty only when decision is pass>
required_repairs:
  - <empty only when no repairs are required>
validator_summary: <short basis for the decision>
next_required_step: skill-packager-v1
```

Only `decision: pass` with `handoff_allowed: true` may advance to `skill-packager-v1`. A phrase such as
`validator passed`, a checklist summary, or a ledger field without this object is prose-only and must be treated as
missing validation.

### `packaged_by_skill_packager`

```yaml
target_skill: <skill-name>
staged_source_path: <same source path validated>
validator_decision_seen: pass
package_path: <exact external skill.zip path>
package_size_bytes: <nonzero integer>
frontmatter_lint: pass
editor_stability_lint: pass
quick_validate: pass
unzip_test: pass
archive_inspection: pass
exact_file_exists: true
exact_file_nonzero: true
top_level_folder_matches_skill: true
next_required_step: skill-buster-v0.1
```

`skill-packager-v1` may only create this object after checking the exact archive path and the machine-written `package-evidence.json`. The archive path must be named exactly `skill.zip`. The object is invalid if the package path is guessed, stale, absent, empty, wrongly named, not the archive that passed unzip and inspection, or not byte-identical to the evidence hash. This exact-name rule is functional: a renamed or versioned zip may not present the expected Skill install UI.

A fake or broken `skill.zip` handoff is a control-system failure. The validator/packager/buster stack exists to prevent invalid skill packages from reaching Harley. If assistant-written ledger text can still create a broken Skill preview card, the stack failed at its core purpose.

### `presented_by_skill_buster`

```yaml
target_skill: <skill-name>
creator_token_seen: true
validator_decision_seen: true
packager_token_seen: true
one_link_only: true
exact_package_path: <exact package path handed off>
status: ready_to_present | hard_red_stack_incomplete | blocked
```

If any upstream object is missing, stale, mismatched by `target_skill` or `staged_source_path`, or only asserted in
prose, the status must be `hard_red_stack_incomplete` and no package link may be presented.

## Hard-red rule

If any required prior object is absent, stale, for a different skill, for a different source path, or only asserted in
prose, stop. Mark the item `hard_red_stack_incomplete`. Do not validate, package, hand off, or claim install readiness
from narrative state.

## Ledger

Before any installable `skill.zip` link is handed off, the queue item must have a compact ledger backed by the objects
above:

```text
skill:
  creator: authored_by_skill_creator / target_skill / staged_source_path
  validator: validated_by_skill_validator / pass / same staged_source_path
  packager: packaged_by_skill_packager / exact archive path / file exists nonzero
  buster: ready_to_present / one_link_only
```

A missing ledger field, source-path mismatch, skill-name mismatch, prose-only field, non-`skill.zip` filename, or unverified UI-installable archive blocks handoff. The reason is practical: broken `skill.zip` links can render failing Skill preview cards, while wrongly named zip files may not present the install UI. Either outcome defeats the control system built to stop invalid skill handoffs.
