# Handoff posture and false-green prevention

Use this reference when preparing, repairing, or reviewing one or more installable `skill.zip` handoffs.

## Goal and non-goal

`skill-buster-v0.1` is not a zip-link emission race. Its goal is to preserve the handoff control system so every surfaced archive is installable, current, and contains the intended authored and validated update.

Non-goal:

```yaml
non_goal: race_to_emit_zip_links
```

Goal:

```yaml
goal: hand_off_installable_skill_zips_that_contain_the_intended_validated_update
```

A run is not green merely because one or more `skill.zip` links appeared. It is green only when the relevant capability stack was discovered, invoked, and evidenced for the same target skill, staged source path, intended update, and package path.

## Capability stack, not link stack

Before handoff, prove the capabilities were applied in order:

```yaml
capability_stack_applied:
  author_or_update_capability_discovered_and_used: true
  semantic_validation_capability_discovered_and_used: true
  packaging_identity_capability_discovered_and_used: true
  queue_handoff_capability_discovered_and_used: true
```

The current normal stack is the skill authoring/update capability, the skill validation capability, the skill packaging/identity capability, and then `skill-buster-v0.1` handoff. The posture is capability-based so future renamed or wrapped skills do not bypass it.

Do not treat a prepared dist folder, expected package path, previous package, or package wrapper success as evidence that the authoring or validation capability was actually used for the requested update.

## No-op false green

A package can be real and still be false green. Rebuilding an existing skill folder into a fresh valid archive without applying the intended update is a control-system failure.

Before any handoff, check:

```yaml
no_op_prevention:
  intended_update_named: true
  modified_surfaces_match_intended_update: true
  validation_reviewed_the_modified_source: true
  package_built_from_modified_staged_source: true
  package_evidence_matches_that_source: true
```

Invalid pattern:

```text
Rebuild the currently installed skill as skill.zip, present the link, and call it complete even though the requested edit was not applied.
```

Repair by discarding that package for handoff, returning to the author/update capability, applying the actual change, rerunning validation on the modified staged source, repackaging from that source, and only then re-entering the handoff cursor.

## Fake-link false green

A handoff is also false green when the link appears but the archive is absent, stale, wrongly named, hash-mismatched, not backed by machine package evidence, not the same archive that passed checks, or not surfaced through a normal assistant message.

Packaging evidence proves archive identity, not user-visible handoff success and not semantic update conformance. Validation proves semantic fitness of the reviewed staged source, not that a later package was built from that source unless the packaging receipt and path match.

## Pre-handoff posture check

Use this compact check before every one-at-a-time or batch handoff:

```yaml
handoff_posture_check:
  non_goal_acknowledged: race_to_emit_zip_links
  intended_update_named: true
  author_update_evidence_same_skill_and_path: true
  validator_pass_same_skill_path_and_update: true
  package_receipt_same_skill_path_and_archive: true
  no_op_false_green_checked: true
  fake_link_false_green_checked: true
  handoff_surface_is_normal_assistant_message: true
```

If any item is not true, do not emit a `skill.zip` link. Return to the missing capability or classify the item as blocked.


## Script-backed update posture

When a queued skill create/update adds, removes, or changes files under `scripts/`, handoff preparation must include evidence that the script surface was checked through the author/update, validation, and packaging/identity capabilities.

Before presenting a script-backed skill package, require:

```yaml
script_backed_update_check:
  script_changes_identified: true
  normal_use_recipe_outside_script_source: true
  validator_reviewed_script_architecture_and_efficiency: true
  packager_receipt_includes_script_architecture_lint_when_scripts_exist: true
  no_agent_improvisation_route_left_open: true
```

Do not treat a valid `skill.zip` as enough when the requested change involved scripts. A script-backed false green can be an installable package that still leaves agents litigating whether to read scripts, write helper scripts, bypass slow wrappers, or trust undocumented outputs. Return to validation or packaging if script architecture evidence is absent.
