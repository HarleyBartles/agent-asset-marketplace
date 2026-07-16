# Prompt Board Contract

Use this reference when an Adventures image generation attempt needs a prompt board before image preflight can be green.

## Purpose

A prompt board is a deterministic pre-generation artifact for GPT/project planning and a possible bounded input for PIG. It combines visual references, reference roles, hard layout
requirements, prompt-safe constraints, and QA gates in one image surface so the image model is not asked to infer which
reference controls what.

The board is not final art, not a deck slide, not a contact sheet, not ordinary GPT generation authorization, and not PIG execution authority.

## Required inputs

A prompt board should include:

- one primary style/world reference when available;
- one geometry reference when exact placement matters;
- optional supporting references for continuity or anti-patterns;
- concise must-show requirements;
- concise must-not-show requirements;
- selected generation references with explicit roles;
- available images intentionally excluded from the image call;
- prompt carry-forward text that is safe to paste into ordinary GPT image preflight or include as a bounded PIG input;
- QA gates for the generated candidate.

## Reference roles

Use explicit roles:

```yaml
style_reference:
  role: style_only
geometry_reference:
  role: layout_hard_gate
supporting_references:
  - role: world_continuity | prop_continuity | character_continuity | anti_pattern | other
```

Style references control rendering, palette, tone, linework, and finish. They do not override layout hard gates.

Geometry references control placement, pathing, crossings, adjacency, scale relationships, and hard spatial logic. They
do not control final rendering style.

Supporting references must have bounded roles. Do not let a supporting reference become a hidden substitute style or
layout control.

Use the minimum sufficient reference set. Do not attach every available image merely because it is present. A prompt
board must decide what to attach and what to exclude before image-generation authorization is consumed.

## Board contents

A useful board normally has:

- title and target image lane;
- source/file-home labels for each reference;
- role labels for each reference;
- callouts for layout hard gates;
- must-show and must-not-show lists;
- prompt carry-forward block;
- QA gates block;
- selected-reference and excluded-reference block when the board feeds an image call.

Use short board text. Put detailed reasoning in the chat response or preflight packet, not on the board.

## Mandatory prompt-board cases

For ordinary GPT/project workflow, a prompt board is mandatory before image preflight can be green when:

- a geometry-sensitive image uses both a storyboard diagram and a style/world reference;
- there are multiple references that could conflict;
- the prompt must preserve exact line semantics, path logic, object adjacency, or state transitions;
- previous attempts failed because a prompt was visually plausible but structurally wrong;
- the requested run needs to reach an 80 percent or higher confidence target and the board is the concrete missing
  confidence-raising artifact.

The prompt board may be waived for simple exploratory images, first-pass environment exploration without strong
references, or intentionally low-confidence user-authorized experiments. Waivers must be explicit and carried into image
preflight.

## Reference selection gate

Every prompt board that may feed image generation must include:

```yaml
reference_policy: minimum_sufficient_references
use_all_available_images: false
selected_generation_references:
  - path: <path or surface>
    role: generation_control_surface | geometry_hard_gate | style_only | bounded_support
    required: true | false
locked_reference_set:
  status: locked
  lock_owner: adventures-storyboard-preflight-v1
  reference_policy: minimum_sufficient_references
  use_all_available_images: false
  allowed_image_call_references:
    - path: <exact path or surface>
      role: generation_control_surface | geometry_hard_gate | style_only | bounded_support
      required: true | false
  prohibited_reference_sources:
    - conversation_uploads_not_in_locked_set
    - asset_intake_zip_images_not_in_locked_set
    - broad_contact_sheets_not_in_locked_set
    - character_sheets_not_in_locked_set
    - prior_candidates_not_in_locked_set
    - stale_session_images_not_in_locked_set
  if_reference_change_seems_needed: stop and revise prompt board; do not call image_gen
excluded_available_images:
  - path: <available image or group>
    reason: <wrong lane, conflicting trial, broad contact sheet, character sheet, not needed>
```

`use_all_available_images: true` is only valid when Harley explicitly asks for broad synthesis, overview, audit, or
contact-sheet style generation. It is not valid for normal governed image generation.

If there is a prompt board, downstream ordinary GPT image preflight should use exactly the selected references unless a required file
is unavailable. If the board is handed to PIG, it is a reference-selection and constraint packet for PIG's production stack, not a substitute for PIG production judgment. If a required file is unavailable, stop with a reference blocker rather than substituting all available
images.

The locked set is authoritative. Do not add all current uploads, all visible conversation images, all intake-zip images,
or all contact-sheet panels merely because they are available. If the locked set appears insufficient, revise the prompt
board before authorization instead of changing the image call at the last moment.

## JSON shape for deterministic board scripts

`scripts/make_prompt_board.py` accepts a JSON spec shaped like this:

```json
{
  "title": "Trial 4 image 2 prompt board",
  "subtitle": "environment asset generation",
  "width": 2400,
  "height": 1800,
  "image_slots": [
    {
      "path": "path/to/style.png",
      "title": "Style/world reference",
      "role": "style_only",
      "caption": "controls rendering style only"
    },
    {
      "path": "path/to/diagram.png",
      "title": "Geometry reference",
      "role": "layout_hard_gate",
      "caption": "controls placement and hard gates"
    }
  ],
  "must_show": ["hard requirement"],
  "must_not_show": ["forbidden failure"],
  "reference_policy": "minimum_sufficient_references",
  "use_all_available_images": false,
  "selected_generation_references": [
    {"path": "path/to/board.png", "role": "generation_control_surface", "required": true}
  ],
  "excluded_available_images": [
    {"path": "path/to/contact-sheet.png", "reason": "broad source; would dilute this image call"}
  ],
  "prompt_carry_forward": "prompt-safe block",
  "qa_gates": ["exact generated-image check"],
  "source_notes": ["optional source note"]
}
```

Paths are local filesystem paths resolved from the spec file directory unless absolute. Do not put raw repo process
notes or issue comments into `prompt_carry_forward`.

## Trial 4 image 2 exemplar

For issue #47 Trial 4 image 2:

- style reference: full-size Trial 4 long-course environment image, role `style_only`;
- geometry reference: corrected Bit false-line storyboard diagram, role `layout_hard_gate`;
- must show: service road crossing, crosswise broken road-center line, hazard-tape hole left/off-course, open shoulder,
  long course continuing beyond frame;
- must not show: characters, crash, finish banner, finish arch, medals, podium, maze, sprint spaghetti lanes, gritty
  construction realism;
- selected references: prompt board, corrected storyboard diagram, accepted long-course style reference, and at most
  one bounded continuity reference;
- excluded references: broad in-flight contact sheet, unrelated high-jump and hedge-maze images, character sheets, and
  Patch/stakeholder references because they would add false carryover;
- QA must verify the road marking and hazard tape read as false lines but neither becomes a real finish line.
