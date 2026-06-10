# Package Handoff Evidence

Use this reference before presenting any installable `skill.zip` link or when repairing a broken or fake handoff.

## Required evidence chain

A valid handoff requires observable evidence in order:

```text
authored_by_skill_creator -> validated_by_skill_validator -> machine-written package-evidence.json -> packaged_by_skill_packager summary -> skill-buster handoff
```

The stack evidence must name the same `target_skill`, the same staged source path, and the exact archive path that will be linked. Prose is never enough.

Before a link is emitted, consume the machine-written `package-evidence.json`, re-stat the exact `package_path`, recompute SHA-256, and confirm it matches the receipt.

## Broken installer card hard stop

A sandbox link to a ZIP named exactly `skill.zip` can render as an installable Skill preview card. If the archive is absent, stale, malformed, hash-mismatched, or not a valid skill archive, Harley sees a failing install card. If the package link is printed through a tool or alternate surface, Harley may not see an install card at all. Both are control-system failures, not cosmetic link problems.

A package link is not handoff-ready unless the exact linked archive:

- is named exactly `skill.zip`;
- exists at the exact linked path;
- is a regular nonzero file;
- matches the SHA-256 in `package-evidence.json`;
- is the same archive that passed unzip integrity and archive inspection;
- contains exactly one top-level folder matching the skill name;
- is emitted as a normal assistant message link, not tool output or another non-chat handoff surface.

If any condition is missing or unproven, classify the item as `hard_red_invalid_handoff` and do not emit the link.

## Fake-ledger hard stop

Assistant-authored ledger text is not a stack token. Ask: could the claimed ledger have been typed without the archive existing? If yes, it is not evidence.

Do not repair a fake ledger by rewriting it. Repair only by rerunning the missing creator, validator, packager, and evidence checks until real same-target evidence exists.

## Wrong-surface hard stop

A file upload event is not the same as a package handoff. A valid handoff requires the user-facing assistant message to surface the installable package link. Do not use `python_user_visible`, notebook output, shell output, canvas, widgets, issue comments, logs, tables, or generated files to emit the package link.

If Harley reports that the Skill card did not appear, do not argue from file existence or upload evidence. Treat the item as not presented, mark any active batch lifecycle broken, and rebuild or re-present according to the recovery rules.

## Surface distinction

Package evidence proves the archive exists and matches its receipt. It does not prove that the handoff surfaced correctly. A package is presented only when its `skill.zip` link appears in a normal assistant message. Inert cursor-advance pulses may occur between batch handoffs, but they must not contain package links or evidence.

## Upload telemetry is not negative proof

Assistant-side file-upload telemetry can support confidence that a package surfaced, but missing, delayed, hidden, or unavailable upload telemetry is not authoritative negative evidence. The user-visible UI is the real install surface. If the assistant message contained the correct `skill.zip` link and the pre-send package evidence was valid, absent upload telemetry creates `surface_unconfirmed`, not `hard_red_invalid_handoff` by itself.

Use this state model after an assistant-message handoff:

```yaml
handoff_surface_state:
  pre_send_package_evidence: required_and_authoritative
  assistant_message_link_emitted: required
  assistant_upload_telemetry: helpful_but_not_authoritative_negative_evidence
  user_surface_confirmation: authoritative_for_surface_and_landing_state
```

Poison or invalidate only when there is a real handoff defect: wrong output surface, missing or mismatched archive evidence, no assistant-message `skill.zip` link, a user-reported failed or absent install card, or a substantive cursor-breaking action. Do not stop a clean cursor solely because the assistant cannot see upload telemetry that Harley can see in the UI.
