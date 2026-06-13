# Skill Handoff Lifecycle

Use this reference when a skill queue is packaging or presenting more than one installable `skill.zip`, when choosing one-at-a-time versus batch mode, or when recovering from an interrupted handoff.

## Lifecycle modes

### One-at-a-time mode

Use this when Harley will install packages and confirm `landed` between items. Package only the current skill, verify that exact archive, present exactly one `skill.zip` link in a normal assistant message, then wait. Do not prepackage later queue items.

### Batch mode

Use this only when Harley explicitly selects continuous batch handoff or when the queue was approved as batch mode.

Batch mode has two phases:

1. `batch_preparation`: package and verify the whole batch before any installable link is emitted.
2. `batch_handoff_cursor`: present the prepared packages as `N-1` intermediate handoff messages and one final handoff message, exactly one installable `skill.zip` link per normal assistant message.

Read `references/batch-handoff-cursor.md` before packaging or presenting a batch. Cursor arithmetic decides the message type. Package 1 of N is never the final handoff unless N is 1, and N is 1 is not batch mode.

Once batch presentation begins, do not run substantive tools, use `python_user_visible` to carry a package link, re-read files, search repositories, post comments, re-plan, wait for `landed`, use alternate output channels for package links, or chatter between package handoffs. The package handoff message itself is the progress update. If the runtime needs an intervening event to continue the visible cursor, an inert cursor-advance pulse is allowed between handoff messages. It must carry no package link, create no evidence, inspect no sources, trigger no external side effect, and leave the manifest unchanged. Either deliver the whole batch through the cursor sequence or poison the affected remaining package artifacts.


## Batch preparation window

Batch mode has a handoff size, not a requirement to overload upstream packaging. Before the handoff cursor starts, preparation should be serial and interruptible. Use a bounded preparation window:

```yaml
batch_preparation_window:
  default_after_timeout_or_heavy_context: 1
  may_increase_only_when_recent_wrapper_runs_are_quick_and_clean: true
  package_unit: one_skill_one_wrapper_invocation_one_dist_dir
```

A package-preparation timeout before the cursor starts is a `preparation_efficiency_failure`, not `poisoned_batch`. Preserve already prepared package facts, reduce the window to one, retry the slow item in isolation, and continue the queue serially after success. Park only the slow item if its receipt shows a real source defect that requires repair.

Do not convert this efficiency recovery into a bypass. Manual zipping, stale package reuse, skipped validator evidence, or package links emitted during preparation remain invalid.

## Poisoned batch rule

If a batch of skill updates was packaged and only part of it was handed off before the handoff stopped, every remaining unpresented or unlanded package artifact from that batch is no longer presentation-safe.

Poison triggers include:

- a final-style response after only part of a prepared batch was presented;
- substantive tool calls, repo work, skill reads, explanatory chatter, wrong-surface package links, or alternate output channels carrying package links after batch handoff began;
- attempting to resume from unpresented prebuilt package files after the batch stopped;
- assistant-side queue state saying one skill while the linked `skill.zip` contains another;
- multiple installable `skill.zip` links in one message;
- waiting for `landed` between intermediate handoffs in batch mode;
- printing a package link through `python_user_visible`, notebook output, shell output, canvas, widgets, issue comments, logs, or tables instead of a normal assistant message;
- a file upload event occurring without the expected visible Skill install card surfacing for Harley.

Recovery: discard assistant-side assumptions for affected items, treat remaining prebuilt archives as poisoned, rebuild the next target from its actual source directory, verify archive identity, and present only that rebuilt package or a fresh explicitly approved batch.

## Multiple-link install-card rule

Never include multiple installable `skill.zip` links in one handoff message. Plain text package names may be listed together; installable links may not.
