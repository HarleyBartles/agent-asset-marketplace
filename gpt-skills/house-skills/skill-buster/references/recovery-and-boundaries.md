# Recovery and Boundary Rules

Use this reference when a skill queue becomes unclear, a package handoff fails, Harley reports an install problem, the task is issue-backed, or the user explicitly asks for a fresh read.

## User-directed reread gate

If Harley explicitly says to read, re-read, check, look at, inspect, consult, or use `skill-buster-v0.1`, perform a fresh read of the skill entrypoint in the same turn before any substantive answer, package handoff, queue advancement, repair action, or process explanation. If the read is unavailable, stop and report the blocker.

## Reset and repair

If the queue becomes unclear, reconstruct it from Harley's latest explicit instruction and prior confirmed states. Ask only if a real ambiguity remains.

If a handoff contains the wrong skill, stop batch progression and mark the active batch `poisoned_batch`. Discard unpresented or unlanded artifacts from that batch. Rebuild the next target from its actual source directory and verify archive identity before re-presentation.

If a package link has no file behind it, fails to download, appears through a non-assistant output surface, appears after a broken batch lifecycle, or Harley reports that it did not surface or failed to install, treat it as `hard_red_invalid_handoff` or `poisoned_batch`, not as an ordinary loader problem.

Missing assistant-side upload telemetry is different from a user-visible install failure. If the assistant-message link was emitted from valid package evidence but the assistant cannot see upload telemetry, classify the item as `surface_unconfirmed`. Do not poison the batch on that signal alone.

If Harley reports `Could not load this skill` or an equivalent installer failure, keep the item active and route to packaging repair before marking it done.

If Harley reports that a package did not produce an install card, do not treat the underlying file upload event as success. The handoff contract includes user-visible card surfacing. The item remains not landed until a normal assistant-message handoff works and Harley confirms installation or acceptance.

If Harley confirms that a package surfaced or landed, that user-visible confirmation overrides missing or delayed assistant-side upload telemetry for surface state. Continue from the next cursor item when the archive evidence and assistant-message link were otherwise valid.

## Issue-comment discipline

Skill-buster handoff mode is chat-only unless Harley explicitly requests repo tracking for that handoff. Do not create GitHub issue comments, pull request comments, repo progress comments, or test comments while presenting packages, recording install confirmations, advancing batches, or repairing package handoffs.

## No-shit / skill-sprawl posture

Treat skill sprawl and duplicate operational entrypoints as custody risks. Prefer consolidation when it preserves trigger clarity, actor or domain authority, and package loadability. Do not use anti-bloat as a reason to erase lawful wrappers, local binding pages, inheritance mechanics, validation gates, or protected-surface safeguards.

## Cursor recovery

If a package card does not surface because the link appeared through a wrong output channel, treat that item as not presented. If the only intervening event was an inert cursor-advance pulse with no package link, no evidence, no source inspection, no external side effect, and no manifest change, do not mark the batch poisoned on that basis alone.
