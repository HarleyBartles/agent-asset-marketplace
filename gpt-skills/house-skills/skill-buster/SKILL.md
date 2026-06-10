---
name: skill-buster
description: manage multi-skill update queues and package handoff cadence. use for queued skill creation or updates, continuing after landed, batch or one-at-a-time package presentation, recovery from broken skill.zip handoffs, poisoned batch state, fake-ledger risk, or deciding whether an installable skill package may be surfaced to the user.
version: v0.1
source_id: skill-buster-v0.1
source_path: gpt-skills/house-skills/skill-buster/SKILL.md
provenance_name: MARK-21 skill maintenance House Skills source slice
---
# Skill Buster

Use this skill to manage ordered queues of skill creation, skill update, package handoff, install confirmation, repair, and recovery work.

## Owned decision

This skill owns queue state and handoff cadence. It does not author skill content, validate semantic fitness, package archives, or diagnose repository evidence unless the current queue actually needs that evidence.

## When to use

Use this skill when the current task involves more than one skill, including multi-skill creation or update, adjacent-skill propagation, queued package handoff, continuing after `landed`, batch presentation, or recovery from a broken or fake `skill.zip` handoff.

## When not to use

Do not use this skill as the content author. Use skill creation/update guidance for content edits. Do not use it as package validator or archive inspector. Use packaging guidance for archive identity and loader checks.

## Stack rule

A queue item cannot be handed off unless the evidence chain exists for the same skill and same staged source path:

```text
authored_by_skill_creator -> validated_by_skill_validator -> package-evidence.json -> packaged_by_skill_packager -> skill-buster-v0.1 handoff
```

If any item is missing, stale, mismatched, or only asserted in prose, mark the item `hard_red_stack_incomplete` and return to the missing upstream step.

## Progressive reference triggers

- Read `references/skill-update-stack-contract.md` before presenting any installable `skill.zip` link.
- Read `references/handoff-lifecycle.md` when choosing one-at-a-time versus batch mode, preparing a batch, or recovering from an interrupted handoff.
- Read `references/batch-handoff-cursor.md` whenever batch mode is selected, before packaging or presenting any batch package.
- Read `references/package-handoff-evidence.md` before emitting a link or when a handoff may be fake, stale, malformed, wrongly named, absent, install-card unsafe, or surfaced through the wrong output channel.
- Read `references/handoff-posture-and-false-green.md` before preparing or presenting one or more `skill.zip` handoffs, especially when racing to land zips, no-op repackaging, script-backed update evidence, or missing author/validator/packager evidence could create false green.
- Read `references/queue-state-model.md` when reconstructing, reporting, or advancing a queue.
- Read `references/source-and-evidence-posture.md` only when the skill queue depends on repository evidence, connector availability, source-route claims, external package evidence, or a failed source route.
- Read `references/handoff-execution-contract.md` when more than one prepared package must be handed off in batch mode.
- Read `references/recovery-and-boundaries.md` when a queue becomes unclear, a handoff fails, Harley reports an install problem, issue-comment posture matters, a package card does not surface, or Harley explicitly asks to read/check/use this skill.

## Lifecycle summary

Choose exactly one lifecycle before packaging or presentation:

- `one_at_a_time`: package only the current item, present one normal assistant-message `skill.zip` link, wait for `landed`.
- `batch`: use the two-phase batch state machine. First prepare every package and emit no links. Then enter the handoff cursor and emit `N-1` intermediate handoffs followed by one final handoff, one normal assistant-message `skill.zip` link per package. If the runtime needs an intervening event to continue the visible cursor, an inert cursor-advance pulse may occur between handoff messages, but it must not contain a package link, change state, inspect sources, or create evidence.

Never include multiple installable `skill.zip` links in one assistant message.

## Handoff surface rule

An installable handoff must be a normal assistant chat message containing exactly one markdown/sandbox link whose basename is `skill.zip`. Do not emit package links through tool output, code execution output, canvas, widgets, issue comments, generated files, logs, tables, or any non-assistant-message surface.

`python_user_visible`, notebooks, shell output, and other tool channels are not valid package handoff surfaces when they carry the package link. A file upload event or printed path is not proof that the user received an installable Skill card. If the Skill install card does not surface in the visible chat, treat the item as not presented. A separate inert cursor-advance pulse is allowed only as a runtime continuation mechanism and only when it carries no package link or evidence.

## Core workflow

1. Reconstruct the queue from Harley's latest instruction and confirmed states.
2. Confirm lifecycle mode if it is not already explicit.
3. For each current item, require creator, validator, and packager evidence before it can be `prepared`.
4. In batch mode, prepare the whole batch before any link and then drive the cursor from `current_index` and `batch_size`.
5. Before a link, verify the exact handoff archive using machine-written package evidence.
6. Present packages according to the selected lifecycle, only through normal assistant messages.
7. Mark a package `done` only after Harley confirms installation or acceptance, unless packaging alone was explicitly the completion condition.

## Handoff hard stop

Do not emit a `skill.zip` link unless the exact file exists, is nonzero, is named exactly `skill.zip`, matches `package-evidence.json`, is the validated archive, and will be emitted in a normal assistant message. A fake, broken, or wrong-surface `skill.zip` link is a control-system failure, not a cosmetic problem.

## Batch cadence hard stop

In batch mode, package 1 of N is never the final handoff unless N is 1, and N equals 1 is not batch mode. A thought or draft that treats the first package as the final handoff is a mode error. Repair by rebuilding the cursor state: all packages prepared first, then intermediate handoffs until the last package, then the final handoff.

Once `batch_handoff_cursor` starts, do not run substantive tools, re-read files, inspect repos, post issue comments, explain process, mutate state, or use any alternate channel to carry package links between cursor messages. If the runtime needs an intervening event to continue, use only an inert cursor-advance pulse with no package link, no evidence, no source inspection, no external side effect, and no manifest change. If a substantive tool action or wrong-surface package link occurs after cursor start and before the final cursor message, stop and mark every affected unpresented or unlanded remaining item `poisoned_batch`.

## Boundaries

Do not create or update skill contents without the skill creation/update path. Do not package, repackage, or repair install failures without packaging guidance. Do not continue from memory when Harley explicitly directed a fresh read of this skill. Do not run unrelated work after a batch handoff begins unless the remaining batch is treated as poisoned.
