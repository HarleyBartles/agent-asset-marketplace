# Handoff Execution Contract

Read this reference before emitting package links when two or more prepared `skill.zip` packages must be handed off or re-presented.

## Stack evidence gate

Before presenting any installable package link, require observable evidence for the queue item:

```text
skill:
  creator: authored_by_skill_creator / source path
  validator: validated_by_skill_validator / pass
  packager: package-evidence.json / exact archive path / sha256 match
  buster: ready_to_present
```

A missing, source-mismatched, hash-mismatched, wrongly named, wrong-surface, or prose-only evidence entry is `hard_red_stack_incomplete` or `hard_red_invalid_handoff`. The validator entry must be the structured `validated_by_skill_validator` decision object, not a sentence or summary. The packager entry must be a machine-written `package-evidence.json` receipt, not assistant-authored ledger text.

A fake or broken `skill.zip` link can render a Skill preview card that looks installable but fails. A link printed by a tool can also fail to surface the install card. Either failure wastes Harley's install attempt and undermines the control stack.

## Handoff surface versus cursor driver

The handoff surface is where the package link appears. It must be a normal assistant message.

The cursor driver is how the runtime advances from one visible handoff message to the next. If needed, the cursor driver may include an inert cursor-advance pulse between handoffs. The pulse is lawful only when it contains no package link or package path, creates no evidence, inspects no source, has no external side effect, and leaves the manifest unchanged.

Do not confuse the two. A tool output may be an inert cursor driver only if it does not carry the handoff. It is never a handoff surface.

## Cursor protocol

Before the first handoff message, materialize a handoff manifest in working memory:

- `packages`: ordered list of prepared package names and paths.
- `cursor`: one-based index of the next package to present.
- `total`: count of packages in `packages`.
- `presenting`: `true`.
- `batch_phase`: `batch_handoff_cursor`.
- `handoff_surface`: `assistant_message`.
- `cursor_driver`: `assistant_message_or_inert_pulse`.

Do not start the cursor unless every package in the manifest is already prepared and exact archive evidence has been verified.

Choose the assistant message cadence from cursor arithmetic before each handoff:

1. Let `remaining_after_this_message = total - cursor`.
2. If `remaining_after_this_message > 0`, the next handoff is `intermediate_handoff`.
3. If `remaining_after_this_message == 0`, the next handoff is `final_handoff`.
4. Package 1 of N is never `final_handoff` unless N is 1, and N is 1 is not batch mode.
5. Count only assistant messages containing exactly one package link as handoffs.
6. The stack is complete only when `cursor > total`.

## Presenting lock

While `presenting = true`, allowed actions are only:

- emit the next package handoff at the current cursor through a normal assistant message;
- use an inert cursor-advance pulse after an intermediate handoff when needed by the runtime;
- report an exact missing-file blocker for the current cursor package;
- stop because Harley explicitly interrupted with a side question or stop request.

Do not use a pulse for source reads, package checks, issue comments, repo operations, replanning, explanation, validation, or evidence creation.

## Message contract

Every handoff message must contain exactly one installable `skill.zip` link in a normal assistant message. The archive basename must be exactly `skill.zip`. Multiple installable ZIP links in one message are invalid because the UI may materialize only the first one as a Skill install card.

Never use tool output, code output, canvas, widgets, issue comments, generated files, logs, tables, or any non-assistant-message surface as the handoff surface. A file upload event is not the same as a surfaced install card.

## Pre-send check

Before sending each assistant handoff message:

1. Confirm `batch_phase: batch_handoff_cursor`, `presenting: true`, and the manifest exists.
2. Confirm the message presents `packages[cursor]` only.
3. Confirm any intervening event since the prior handoff was an inert cursor-advance pulse only.
4. Confirm no intervening event carried a `skill.zip` link, package path, evidence, source inspection, external side effect, or manifest change.
5. Load the machine-written `package-evidence.json` for `packages[cursor]`; do not use assistant-authored ledger text.
6. Verify the exact package path exists as a regular, nonzero file and has basename exactly `skill.zip`.
7. Recompute SHA-256 and verify it matches `package_sha256`.
8. Compute `remaining_after_this_message = total - cursor` and choose `intermediate_handoff` or `final_handoff` from cursor arithmetic.
9. Count installable links ending in `/skill.zip` in the drafted message.
10. If the count is not exactly one, do not send the message.

## Interruptions and recovery

If Harley interrupts with a stop request or side question, stop the stack and mark every unpresented or unlanded package in the active batch `poisoned_batch` unless Harley explicitly authorizes a bounded retry or override lane.

If a package link is surfaced through the wrong channel, that item is not presented. If a substantive action occurs between handoffs, the affected remaining packages are not presentation-safe until rebuilt or explicitly reauthorized by Harley.

## Valid three-package example

Manifest before message 1:

```text
packages = [skill-a, skill-b, skill-c]
cursor = 1
total = 3
presenting = true
handoff_surface = assistant_message
```

Message 1, intermediate:

```markdown
Batch prepared and validated: `skill-a`, `skill-b`, and `skill-c`.

`skill-a`: [skill.zip](sandbox:/mnt/data/.../skill.zip)
```

Optional inert pulse with no package link.

Message 2, intermediate:

```markdown
`skill-b`: [skill.zip](sandbox:/mnt/data/.../skill.zip)
```

Optional inert pulse with no package link.

Message 3, final:

```markdown
`skill-c`: [skill.zip](sandbox:/mnt/data/.../skill.zip)
```
