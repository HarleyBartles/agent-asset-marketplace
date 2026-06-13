# Batch Handoff Cursor

Use this reference whenever batch mode is selected, before any batch package is built or handed off.

## Core lesson

Batch mode is a two-phase state machine: prepare every package first, then walk a visible cursor through the prepared manifest. The package handoff surface and the cursor driver are different things. Package links must be visible normal assistant-message links. The runtime may use an inert cursor-advance pulse between visible handoffs when needed to keep the cursor moving, but that pulse is not a handoff, not evidence, and not progress by itself.

## Phase 1: batch_preparation

Do all package work before any installable link appears.

Required state:

```yaml
batch_phase: batch_preparation
batch_size: N
packages_prepared: 0..N
installable_links_emitted: 0
```

Rules:

- Build, validate, package, and verify every package in the declared batch.
- Do not emit any `skill.zip` link during this phase.
- Do not call a package `presented` during this phase.
- If any item times out or runs slowly before handoff begins, classify it as preparation efficiency state, reduce the preparation window to one, and retry the same item in isolation before continuing. If the receipt shows a real source/package defect, park that item or report the blocker; do not emit any links.
- A batch is handoff-ready only when every item has creator evidence, validator pass evidence, machine-written package evidence, and exact archive verification.


### Preparation efficiency state

The handoff cursor is poisoned only after presentation begins or a wrong-surface/fake link is emitted. Before cursor start, slow packaging is a preparation concern.

```yaml
packaging_timeout_behavior:
  classification: preparation_efficiency_failure
  not: batch_poison
  response:
    - reduce_preparation_window_to_1
    - retry_same_item_in_isolation
    - use_wrapper_receipt_to_identify_slow_step
  forbidden:
    - manual_zip_bypass
    - stale_package_reuse
    - skipped_validator_or_creator_evidence
    - continuing_large_window_packaging
  allowed:
    - continue_queue_serially_after_success
    - park_only_the_slow_item_if_source_repair_is_needed
```

Timeout recovery should minimize wasted wall-clock time while preserving the canonical stack.

## Phase 2: batch_handoff_cursor

Start only after all packages are prepared.

Required state:

```yaml
batch_phase: batch_handoff_cursor
presenting: true
batch_size: N
current_index: i
current_package: packages[i]
remaining_after_this_message: N - i
handoff_surface: assistant_message
cursor_driver: assistant_message_or_inert_pulse
```

Rules:

- Emit exactly one installable `skill.zip` link per assistant handoff message.
- Messages 1 through N-1 are `intermediate_handoff`.
- Message N is `final_handoff`.
- Do not wait for `landed` between cursor messages.
- Do not emit package links through `python_user_visible`, notebook output, shell output, canvas, widgets, issue comments, logs, tables, or any tool response.
- If the runtime needs an intervening event to continue the cursor, an inert cursor-advance pulse may occur after an intermediate handoff and before the next assistant handoff.
- An inert cursor-advance pulse must contain no package link, no package path, no evidence, no source inspection, no external side effect, no repo mutation, no issue comment, and no manifest change.
- If a substantive tool call, wrong-surface package link, state-changing action, or explanatory detour occurs during the cursor, stop and mark affected unpresented or unlanded items `poisoned_batch`.
- If upload telemetry is absent or delayed after a valid assistant-message link, record `surface_unconfirmed` rather than `poisoned_batch`. Continue only when Harley has pre-authorized override or confirms the package surfaced or landed; otherwise pause or switch to one-at-a-time recovery.

## Handoff kind selection

Before drafting each batch handoff message, compute:

```yaml
remaining_after_this_message: batch_size - current_index
```

Then select the cadence deterministically:

```yaml
if remaining_after_this_message > 0:
  handoff_kind: intermediate_handoff
  must_not_wait_for_landed: true

if remaining_after_this_message == 0:
  handoff_kind: final_handoff
  batch_cursor_complete_after_send: true
```

Do not use assistant feeling, ordinary final-answer habits, package size, package importance, user install cadence, file upload events, or tool output to choose the handoff kind. Only cursor arithmetic chooses it.

## Surface telemetry state

Track upload telemetry separately from handoff validity:

```yaml
cursor_item_state:
  emitted: true
  assistant_message_link_valid: true
  upload_telemetry_seen: true | false | unknown
  user_confirmed_surfaced: true | false
  user_confirmed_landed: true | false
```

`upload_telemetry_seen: false` or `unknown` is not a poison condition by itself. It is only a reason to pause for confirmation unless Harley has already authorized continuation or confirms the package surfaced or landed.

## Cursor-advance pulse

A cursor-advance pulse is an optional runtime continuation event between assistant handoff messages. It exists only because some runtimes do not reliably continue a multi-message cursor without an intervening event.

Allowed pulse properties:

```yaml
cursor_advance_pulse:
  contains_skill_zip_link: false
  contains_package_path: false
  creates_or_changes_evidence: false
  inspects_sources_or_repos: false
  external_side_effect: false
  manifest_changed: false
```

The pulse is not a handoff. It cannot repair a missing assistant-message package link. It cannot mark a package presented. It cannot carry validation, package evidence, progress commentary, or issue updates.

## Invalid patterns

### First as final

Invalid: package 1 of N as `final_handoff` when N > 1.

Repair: use intermediate handoffs until package N.

### Tool-output package link

Invalid: print or surface a `skill.zip` link from `python_user_visible`, notebook output, shell output, canvas, widgets, issue comments, logs, tables, or any tool response.

Repair: emit the package link only in the next normal assistant message. Treat the wrong-surface item as not presented.

### Substantive tool between handoffs

Invalid: after cursor start, inspect sources, re-read skills, post issue comments, run repo operations, re-plan, or create evidence before the cursor completes.

Repair: stop and mark affected remaining items `poisoned_batch` unless Harley explicitly authorizes a new override lane.

### Inert pulse mistaken for handoff

Invalid: count a cursor-advance pulse as one of the N package handoffs.

Repair: count only normal assistant messages containing exactly one `skill.zip` link.

## Pre-cursor checklist

Before the first batch handoff message, all fields must be true:

```yaml
batch_mode_explicit: true
batch_size: N
N_greater_than_1: true
all_packages_prepared: true
all_package_evidence_verified: true
installable_links_emitted_during_preparation: 0
manifest_order_locked: true
current_index: 1
presenting: true
handoff_surface_locked: assistant_message
```

If any field is false, do not emit a link.

## Pre-send cursor check

Before each assistant handoff message, all fields must be true:

```yaml
cursor_message_check:
  current_index: i
  batch_size: N
  handoff_kind: intermediate_handoff | final_handoff
  handoff_surface: assistant_message
  exactly_one_skill_zip_link: true
  link_skill_matches_current_package: true
  intervening_events_are_inert_pulses_only: true
  manifest_unchanged_since_preparation: true
  assistant_upload_telemetry_required_for_valid_send: false
```

If any field is false, do not emit the link. If an intervening event carried a package link, changed state, inspected sources, or created evidence, stop and mark the affected batch `poisoned_batch`.

## Message contract

Each batch handoff message should contain:

- the current package name;
- exactly one installable link ending in `/skill.zip`;
- no links for any other package;
- no request to wait for `landed` unless this is the last handoff and Harley's workflow asks for post-batch install confirmation.

The first intermediate handoff may include a compact batch summary in plain text. Later intermediate handoffs and the final handoff should be minimal.
