---
name: skill-handoff
description: Control GPT skill package handoff cadence, install-card safety, and landed confirmation. Use when one or more skills have been authored, validated, and packaged and Harley needs installable skill.zip links, batch or one-at-a-time handoff, recovery from broken/fake package links, or confirmation tracking. It owns queue state and handoff surface only; it does not author, validate, package, inspect repo source, or install skills itself.
---

# Skill Handoff

## Owned decision

Manage ordered skill package handoff from verified package evidence to Harley's visible install opportunity and eventual `landed` confirmation.

This skill owns the package handoff surface for the current House Skills stack. It is not a buster-framework-derived buster and must not present itself as one.

## What this skill does not own

Do not author or edit skill contents. Use `skill-creator`.

Do not judge semantic skill quality. Use `skill-validator`.

Do not build or inspect package archives. Use `skill-packager`.

Do not fetch marketplace source. Use `asset-market`.

Do not claim GPT installed a skill. Only Harley can confirm `landed` after installing or accepting the package.

## Stack rule

A queue item cannot be handed off unless this evidence chain exists for the same skill and same staged source path:

```text
authored_by_skill_creator -> validated_by_skill_validator -> package-evidence.json -> packaged_by_skill_packager -> skill-handoff handoff
```

If any item is missing, stale, mismatched, or only asserted in prose, mark the item `hard_red_stack_incomplete` and do not emit a package link.

## Lifecycle modes

Choose exactly one lifecycle before package presentation.

### One-at-a-time

Use when Harley will install packages and confirm `landed` between items. Package only the current item, verify that exact archive, present one normal assistant-message `skill.zip` link, then stop.

### Batch

Use only when Harley explicitly approves continuous batch handoff. Prepare every package first. Then present packages through a cursor: one normal assistant-message `skill.zip` link per message, with no substantive tool calls or package-link side channels after cursor start.

Never include multiple installable `skill.zip` links in one assistant message.

## Handoff surface rule

An installable handoff must be a normal assistant chat message containing exactly one markdown/sandbox link whose basename is `skill.zip`.

Do not emit package links through tool output, code execution output, notebooks, canvas, widgets, issue comments, generated files, logs, or tables. Those surfaces do not prove the Skill install card appeared.

## Pre-link verification

Immediately before writing the user-facing link, verify:

- the exact file exists;
- the basename is exactly `skill.zip`;
- the file is nonzero;
- machine-written package evidence names the same path;
- the package hash matches the evidence;
- archive inspection passed;
- the archive contains exactly one top-level folder matching the target skill.

## Handoff object

Before presenting, establish:

```yaml
presented_by_skill_handoff:
  target_skill: <skill-name>
  creator_token_seen: true
  validator_decision_seen: true
  packager_token_seen: true
  one_link_only: true
  exact_package_path: <exact /skill.zip package path>
  output_surface: assistant_message
  status: ready_to_present
```

If compatibility with an older stack contract is required, map `presented_by_skill_buster` to this object without reviving the old name in user-facing language.

## Completion states

- `prepared`: package passed packager verification but has not been presented.
- `presented`: one valid package link was emitted on the assistant-message surface.
- `landed`: Harley confirms the skill is installed or accepted.
- `poisoned`: a batch lifecycle or handoff surface was broken; rebuild before presenting again.

Mark an item Done only after `landed`, unless Harley explicitly says packaging alone is the completion condition.

## Recovery

If a package link is wrong, missing, not named `skill.zip`, appears through the wrong surface, or fails to render as an installable card, treat the handoff as failed. Rebuild or reverify the exact package through `skill-packager` before trying again.

If a batch cursor is interrupted by substantive work, explanation, repo inspection, or wrong-surface package links, mark unpresented or unlanded remaining batch artifacts `poisoned` and rebuild the next package from source before handoff.
