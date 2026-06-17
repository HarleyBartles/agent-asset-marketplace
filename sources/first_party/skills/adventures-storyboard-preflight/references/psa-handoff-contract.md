# PSA Handoff Contract

Use this reference when ordinary GPT must route deterministic pre-visualisation work to Patch Storyboard Agent (PSA), or when GPT reviews PSA board returns.

## Route decision

Route to PSA when the request asks for planned or specialist deterministic visualisation, including:

- multiple storyboard panels or multiple PNG outputs;
- prompt boards that should visually ground a later PIG handoff;
- transition, route, crawlspace, superframe, frame-architecture, or geometry boards;
- repair boards after generation churn or QA failure;
- batch storyboard/prompt-board production;
- any board where visual layout is the useful deliverable rather than merely a quick text sketch.

Keep work inside ordinary GPT when the user only needs a small textual storyboard, a short prompt outline, or a lightweight deterministic diagram that does not need a separate specialist run.

## GPT-to-PSA packet

A PSA handoff packet must be paste-ready and self-contained. Do not rely on PSA seeing prior GPT messages, repo paths, uploads, or cross-agent workspace files unless Harley separately proves that route for the current session.

```yaml
recipient_actor: PSA
job_type: deterministic_previs_board
generation_allowed: false
output_request:
  board_count: <number>
  board_types:
    - storyboard_sheet | prompt_board | transition_diagram | route_geometry_board | reference_role_board | repair_board | other
  separate_png_files: true | false
  requested_filenames:
    - <filename or null>
format:
  aspect_ratio_or_size: <e.g. 16:9, A4 landscape, square, task-defined>
  panel_count: <number or per-board map>
  layout_intent: <plain-language layout or route/geometry objective>
visual_brief:
  title: <board title>
  scene_or_sequence: <what the board must show>
  must_show:
    - <hard visual requirement>
  must_not_show:
    - <forbidden visual failure>
  labels_or_callouts:
    - <text that should appear on board>
references:
  included_or_described:
    - path_or_description: <reference>
      role: style_only | geometry_hard_gate | supporting_context | anti_pattern | other
  unavailable_references:
    - <reference PSA should not invent>
return_requirements:
  - return artifact paths
  - include PSA self-QA status
  - list deviations or blockers
  - state how GPT/Harley should review the board
  - state how PIG should later use the board if suitable
acceptance_boundary:
  psa_output_is_planning_artifact: true
  psa_self_qa_is_not_final_acceptance: true
  pig_generation_not_authorized_by_this_packet: true
  repo_or_issue_closure_not_authorized: true
```

## Reviewing PSA returns

Classify PSA returns as deterministic planning/control artifacts. Valid review outcomes are:

- `suitable_for_pig_grounding`
- `needs_psa_repair`
- `useful_but_not_binding`
- `blocked_missing_reference_or_output`

Do not call a PSA board `accepted_scene_art`, `deck-ready`, `canon-locked`, `published`, or `issue-closable` without a separate downstream route. A suitable PSA board can be wrapped into a later PIG packet as a visual grounding input, geometry hard gate, or prompt-control surface.
