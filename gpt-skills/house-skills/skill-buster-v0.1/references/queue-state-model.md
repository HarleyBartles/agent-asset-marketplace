# Skill Queue State Model

Use this reference when reconstructing or reporting a multi-skill queue.

## States

- `todo` - not started yet.
- `current` - the item currently being inspected or packaged.
- `prepared` - package produced and validated with creator token, validator token, machine-written package evidence, and packager summary, but not yet handed off.
- `presented` - package link handed off through a normal assistant message, but Harley has not confirmed installation or acceptance.
- `done` - Harley confirmed installation or acceptance, or made packaging alone the completion condition.
- `skipped` - inspected and no package was needed, or intentionally skipped by instruction.
- `blocked` - cannot proceed without a specific blocker being resolved.
- `hard_red_stack_incomplete` - a required stack object is missing, stale, mismatched, or only asserted in prose.
- `poisoned_batch` - a prepared batch was interrupted, partially handed off, resumed unlawfully, or routed through an alternate output surface after cursor start.
- `hard_red_invalid_handoff` - a package handoff was attempted or drafted with no valid real file behind the exact linked path, with the wrong filename, with a hash mismatch, or through a non-assistant output surface.

Never mark a create or update item `done` merely because ChatGPT returned a package link. Never mark an item `presented` merely because a file upload event occurred; the installable package must surface through the normal assistant chat handoff.

## Planning output

For planning and approval, show:

- each queued skill and target action;
- package order;
- expected skips or no-op inspections;
- validation and package-identity checks;
- compatibility, wrapper, retirement, or blocker posture.
