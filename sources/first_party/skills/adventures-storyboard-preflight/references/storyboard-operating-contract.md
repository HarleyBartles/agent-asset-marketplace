# Storyboard Operating Contract

This reference preserves the detailed operating contract moved out of `SKILL.md` during progressive-discovery decomposition. Load it only when the compact control plane says the current request needs the full workflow.


# Adventures Storyboard Preflight

Use this GPT/project-side skill to produce deterministic pre-generation custody surfaces for Adventures of Patch image work:

1. a storyboard packet and, when useful, a deterministic layout diagram;
2. a prompt board that combines the storyboard, style/world references, supporting references, prompt-safe constraints,
   selected references, excluded references, and QA gates into one generation-control surface.

This skill never calls image generation or image editing. It exists to reduce failed ordinary GPT image-generation calls and produce clean handoff surfaces by resolving
layout, reference-role, and prompt-control risks before GPT spends a credit or before a bounded packet is handed to PIG.

## Resource discipline

For ordinary GPT/project workflow, image generation credits are scarce Adventures production capacity. Deterministic storyboards, diagrams, and prompt
boards are credit-conservation infrastructure. They exist so the later GPT image call, if authorized, or the later PIG production job, if bounded and assigned, has a better chance of
advancing production rather than creating churn.

Calling image generation while this skill is doing deterministic planning defeats the purpose of this skill. This skill
may create or inspect files with deterministic tooling only, such as PIL diagrams, prompt-board PNGs, YAML packets, and
zip packages. It must not use image generation, generative image editing, or style transfer.

Classify the current work before tool choice:

```yaml
operation_class: deterministic_no_credit
allowed_work:
  - storyboard planning
  - deterministic layout diagram
  - prompt board
  - reference selection and exclusion
  - prompt carry-forward block
  - QA gate definition
  - package/zip of deterministic artifacts
forbidden_work:
  - generate image candidate
  - regenerate image candidate
  - generatively edit image candidate
```

`generation_allowed` is always false in this skill. A storyboard packet, prompt board, accepted reference lock, or high
confidence estimate is not ordinary GPT image-generation authority and is not PIG execution authority. For PIG, this output is only an input packet for PIG's own production stack.

## Ownership

Own these decisions:

- whether storyboard planning is required before generation;
- whether a deterministic diagram is needed;
- whether a prompt board is required before generation;
- what geometry, action, prop, text, and route logic must survive generation;
- how style references, geometry references, and supporting references are separated;
- which images are selected for the final image call and which available images are excluded;
- what prompt-safe block should be carried forward to image preflight;
- what QA gates must be checked after generation.

Do not own current-turn image mutation authority for ordinary GPT. Use `adventures-visual-intent-gate` for GPT-side current-turn Adventures image-credit authorization and
`adventures-image-preflight` for final readiness. Do not own post-generation acceptance; use `adventures-image-qa-v1`.

## Mandatory trigger

Run this skill before Adventures image generation when any risk factor is present:

- spatial mechanics or route/path logic;
- cause and effect action;
- held, touched, occluded, transformed, or physically constrained props;
- character/object interaction or scale relationship;
- readable or semi-readable text that carries the gag or acceptance logic;
- multiple plausible interpretations;
- layout-sensitive asset sheets or source images;
- multiple visual references that can conflict;
- confidence improvement or prompt-board work before generation;
- reference-selection hesitation or risk of over-attaching available images;
- prior generation churn or QA failures for the same image.

If none of these apply, a compact storyboard packet may still be useful, but a deterministic diagram and
prompt board are optional.

## When not to use

Do not use this skill for post-generation QA, acceptance, or repair decisions. Use `adventures-image-qa-v1`.
Do not use it to decide whether the latest user turn authorizes ordinary GPT image generation. Use `adventures-visual-intent-gate`. Do not use it to decide whether PIG may generate inside an assigned bounded PIG job; use PIG doctrine and generation skills there.
Do not use it to run ordinary GPT image preflight after authorization. Use `adventures-image-preflight`. PIG production jobs use the PIG stack instead.
Do not use it for asset-sheet compilation after source images are accepted. Use `adventures-asset-sheet-compiler-v1`.

If the user asks for QA, critique, durable-rule planning, repo updates, skill updates, asset-sheet compilation, or
package validation, route there and do not treat the visual context as permission to generate.

## Normal deterministic execution path

For normal storyboard or prompt-board creation, use this path without reading script source:

1. Read this `SKILL.md` once.
2. Read `references/prompt-board-contract.md` once when creating or judging a prompt board.
3. Do not read files under `scripts/` during normal creation. Scripts are executable implementation, not doctrine.
4. Write a JSON spec from the contract and current task.
5. Run the prompt-board builder when a board is needed:

```bash
python /home/oai/skills/adventures-storyboard-preflight-v1/scripts/make_prompt_board.py \
  <spec.json> <output.png>
```

6. Run the storyboard-diagram builder only when a deterministic diagram is needed:

```bash
python /home/oai/skills/adventures-storyboard-preflight-v1/scripts/make_storyboard_diagram.py \
  <spec.json> <output.png>
```

7. Inspect the exact output PNG path that will be linked or used downstream.
8. Write the storyboard or prompt-board packet YAML, including `locked_reference_set`.
9. Zip or return the packet artifacts as requested.

The prompt-board contract owns the normal JSON shape. `SKILL.md` owns routing and the short command recipe. Scripts own
execution only. A normal task must not require reading script source to discover input shape, CLI arguments, or output
rules.

## Script read-loop hard stop

Do not read script source for normal storyboard or prompt-board creation. Do not repeatedly read
`scripts/make_prompt_board.py`, `scripts/make_storyboard_diagram.py`, or any other script to gain confidence before
running them. If the contract has been read and the task is ordinary deterministic board creation, create the smallest
valid JSON spec and run the script.

Read script source only after an actual script execution failure, and only for targeted debugging of the failing line or
argument.

## Workflow

### Phase 1: storyboard and geometry custody

Create or verify a storyboard packet. Create or request a deterministic diagram when pass/fail depends on exact
placement. Use a diagram for paths, lines, prop relationships, before/after state, occlusion, or any
spatial relationship that prose could be prettified away. The diagram may be crude. It is a blocking
diagram, not final art.

### Phase 2: prompt board and reference custody

Create a prompt board when the generation attempt has any of these conditions:

- a storyboard diagram plus one or more style/world references;
- multiple references with different roles;
- a style-versus-geometry conflict risk;
- a task that should reach high confidence before spending a credit;
- a user asks for a prompt board, prompt sheet, generation board, or reference board;
- prior image churn shows prose alone is not controlling output.

A prompt board is not decoration. It states which reference controls style, which controls geometry, what must show,
what must not show, the selected minimum reference set, deliberately excluded images, prompt-safe carry-forward, and QA
gates.

## Required storyboard packet

Return or carry this packet before downstream generation:

```yaml
storyboard_required: true | false
reason: <why storyboard is or is not required>
lane: <adventures image lane>
must_show:
  - <hard visual requirement>
must_not_show:
  - <forbidden visual failure>
layout_diagram_path: <path, or null>
style_reference:
  role: style_only
  source: <accepted style/world reference, or null>
geometry_reference:
  role: layout_hard_gate
  source: <deterministic diagram or layout reference, or null>
layout_hard_gates:
  - <geometry requirement the generator must preserve>
prompt_board_required: true | false
prompt_board_path: <path, or null>
selected_generation_references:
  - path: <local path, repo path, or generated-board path>
    role: generation_control_surface | geometry_hard_gate | style_only | bounded_support
    required: true | false
locked_reference_set:
  status: locked
  lock_owner: adventures-storyboard-preflight-v1
  reference_policy: minimum_sufficient_references
  use_all_available_images: false
  allowed_image_call_references:
    - path: <exact local path, repo path, or generated-board path>
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
  - path: <available image not selected>
    reason: <why it should not be attached>
prompt_carry_forward: <concise prompt-safe block>
qa_gates:
  - <exact generated-image check>
generation_allowed: false
```

## Required prompt-board packet

When a prompt board is required, return or carry this packet:

```yaml
prompt_board:
  status: complete | waived | blocked
  board_path: <path or null>
  waiver_reason: <reason or null>
  lane: <adventures image lane>
  style_reference:
    role: style_only
    source: <repo path, uploaded file, view surface, or package path>
  geometry_reference:
    role: layout_hard_gate
    source: <storyboard diagram or deterministic layout reference>
  supporting_references:
    - role: <world_continuity | prop_continuity | character_continuity | anti_pattern | other>
      source: <path or surface>
  selected_generation_references:
    - path: <local path, repo path, view surface, or package path>
      role: generation_control_surface | geometry_hard_gate | style_only | bounded_support
      required: true | false
  locked_reference_set:
    status: locked
    lock_owner: adventures-storyboard-preflight-v1
    reference_policy: minimum_sufficient_references
    use_all_available_images: false
    allowed_image_call_references:
      - path: <exact local path, repo path, view surface, or package path>
        role: generation_control_surface | geometry_hard_gate | style_only | bounded_support
        required: true | false
    if_reference_change_seems_needed: stop and revise prompt board; do not call image_gen
  excluded_available_images:
    - path: <available image not selected>
      reason: <why attaching it would dilute or conflict with the target>
  must_show:
    - <hard requirement>
  must_not_show:
    - <forbidden false-green>
  prompt_carry_forward: <prompt-safe block>
  qa_gates:
    - <exact generated-image check>
  generation_allowed: false
```

A waived prompt board is valid only for simple images where a board would not materially increase confidence or control.
For geometry-sensitive or multi-reference images, waiver should be rare and explicit.

## Reference selection custody

Use a minimum sufficient reference set. The prompt board must narrow the image call, not widen it. Do not attach every
available image merely because it appeared in the conversation, zip, contact sheet, or source package.

When a prompt board exists, it is the authority for the final image-call reference list. It must state selected
references, excluded available images, `reference_policy: minimum_sufficient_references`, and
`use_all_available_images: false` unless Harley explicitly asks for broad synthesis or audit.

Select references by role:

- prompt board: `generation_control_surface`, normally required;
- deterministic storyboard or layout diagram: `geometry_hard_gate`, required when layout matters;
- one or two accepted world/style images: `style_only`, required when visual style is not captured by the board;
- bounded supporting references only when they add specific continuity.

Exclude broad contact sheets, unrelated trial images, old candidates, character sheets, Patch canon sheets, stakeholder
sheets, or asset packs unless the current image explicitly needs them. Extra images can create false carryover, dilute
the prompt, or make the model blend conflicting environments.

When a prompt board is accepted, its selected references become locked. Do not reopen reference selection at image-call
time because new uploads, contact sheets, source zips, prior candidates, or broad asset packages are visible. If another
reference seems necessary, stop and revise the prompt board first.

## Reference hierarchy for downstream prompts

When a diagram or prompt board exists, downstream image preflight must state:

1. accepted style or world references control rendering style only;
2. storyboard diagrams control spatial layout and hard geometry;
3. supporting references supply only the named continuity, prop, palette, or comparison role;
4. if style and geometry conflict, preserve the diagram geometry and simplify scenery before changing hard gates.

Never paste operator notes, QA labels, issue numbers, candidate numbers, repo chatter, or process comments into image
prompts. Convert them into visual constraints.

## Output behavior

If Harley asks for a storyboard, plan, confidence improvement, prompt board, prompt sheet, generation board, reference
board, or pre-generation layout, answer with the relevant packet and produce requested deterministic artifacts. Do not
call image generation.

If Harley asks what QA says, do not use this skill as permission to mutate. Route to `adventures-image-qa-v1`.

If Harley accepts a prompt board, stop. Acceptance of a prompt board means the deterministic control
surface is accepted; it is not authorization to call image generation.

If a later image-generation request arrives and the image has storyboard or prompt-board risk factors, confirm that the
storyboard packet and prompt-board packet exist before allowing Adventures image preflight to return generation-ready.

## Anti-patterns

Do not:

- treat a polished prose prompt as a substitute for a required diagram;
- treat a diagram alone as enough when reference-role confusion is the main risk;
- let the diagram or prompt board become final art;
- use generated images as geometry proof when deterministic layout is needed;
- let QA repair guidance authorize generation;
- make image generation autonomous after the storyboard or prompt board is produced;
- accept a generated result that violates hard gates because the scene is attractive;
- put operator context, skill notes, issue comments, or process labels into the prompt carry-forward block;
- spend image credits during deterministic prompt-board or storyboard work.

## Execution handoff fields

When this skill feeds a later generation attempt, make reference roles explicit enough for image preflight to use
without reinterpretation:

- `style_reference` controls rendering style only;
- `geometry_reference` controls spatial layout and hard geometry;
- `supporting_references` control only the named continuity or comparison role;
- `selected_generation_references` locks the minimum image set for the later image call;
- `excluded_available_images` records why tempting but wrong images must not be attached;
- `layout_hard_gates` names geometry that must survive generation;
- `prompt_carry_forward` is prompt-safe, not image authorization;
- `prompt_board_path` records the deterministic board when one exists;
- `generation_allowed` remains false.

If a required reference role or locked reference set is unknown for a geometry-sensitive image, return a storyboard or
prompt-board blocker. Do not let image preflight resolve missing references or decide which available images to attach
after authorization has already been granted for an image call.
