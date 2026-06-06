# Qa Operating Contract

This reference preserves the detailed operating contract moved out of `SKILL.md` during progressive-discovery decomposition. Load it only when the compact control plane says the current request needs the full workflow.


# Adventures Image QA

Use this skill as the external GPT/Harley/project QA gate for Adventures of Patch image candidates and deterministic image packages.

## Actor boundary

This reference is not PIG self-QA. PIG self-QA is an internal production judgment that a candidate is worth returning from a bounded PIG job. This skill owns the later project-facing QA decision after a candidate, PSA board, or deterministic visual package is visible or provided to GPT/Harley.

A PSA self-QA pass is not `accepted`, not Harley acceptance, not GPT QA, not canon lock, not deck-ready status, not asset-ready status, and not PIG-ready by itself. A PIG self-QA pass is not `accepted`, not Harley acceptance, not GPT QA, not canon lock, not deck-ready status, and not asset-ready status. Review PIG-returned candidates here only when the user asks for external Adventures QA.

This skill decides whether a visible candidate is externally accepted, needs edit, needs regeneration, or is blocked. It covers Patch scene
art, Patch-bearing preproduction references, non-Patch references, anti-pattern references, compiled asset sheets, and
package image review. It does not generate images, edit images, build decks, create receipts, or canonise assets.

## Image-credit resource discipline

Image generation credits are scarce Adventures production capacity. Deterministic workflows exist to reduce failed image calls and conserve those credits. Calling image generation during deterministic work defeats the purpose of those workflows and can block visual preproduction, preprod-ready work, deck-ready work, and production until credits refresh.

QA is deterministic no-credit work and a deliberate review stop point. Its job is to inspect a visible candidate, name what passed, name what failed, decide the accepted use or repair class, and then stop. If QA immediately mutates pixels, it removes Harley's review insertion point and turns diagnosis into unsupervised generation. That damages the workflow: the project loses the chance to decide whether the repair is worth spending a scarce credit, whether the candidate lineage should be abandoned, or whether deterministic planning should improve first.

A QA request, QA decision, repair packet, accepted prompt board, clear repair target, attractive failed candidate, or `continue` after a candidate never authorizes image generation or generative editing. This skill stops at a text QA decision and repair guidance. Any later image call requires a separate current-turn image-credit authorization gate for visible mutation, then Adventures image preflight readiness. Use role-based discovery for that authorization gate rather than treating this skill as tightly coupled to a package name.

## Operation class

Classify this skill's work as:

```yaml
operation_class: deterministic_no_credit
credit_spending_mutation_allowed: false
```

This skill may inspect images, reason about candidates, compare them to repo/storyboard/template evidence, and write
repair constraints. It must not call image generation, generative edit, style transfer, invoke PIG production, or use any tool that creates new or changed pixels.

## When to use

Use after a generated, edited, PIG-returned candidate, or PSA-returned board is visible, when Harley asks `what does QA say?`, `QA please`, `review it`,
`critique this`, `what failed?`, or asks whether a candidate or board is suitable. Use for deterministic PSA board review when Harley asks whether a storyboard/prompt-board output is suitable for PIG grounding. Use for deterministic compiled-sheet QA after
accepted source images have been placed onto an approved template. Use for deck/package image review when acceptance,
lane compliance, Patch compliance, storyboard compliance, or asset-ready status is being judged.

If a generated Adventures image appears and the next turn is `continue`, route to QA for the latest candidate rather
than restarting planning or generating again.

## When not to use

Do not use for pre-generation readiness; use `adventures-image-preflight`. Do not use for current-turn image mutation
authority; route to the Adventures current-turn image-credit authorization gate for visible mutation. Do not use for deterministic prompt boards or storyboard diagrams; use
`adventures-storyboard-preflight-v1`. Do not use for deterministic asset-sheet compilation; use
`adventures-asset-sheet-compiler-v1`. Do not use for repo issue shaping, receipt creation, or canonisation.

## Core rule

Generated images, including PIG-returned candidates, are candidates until external Adventures QA accepts them. Never trust the generator to get identity, lane, text, style,
physical logic, template posture, or story function right on the first pass.

If a supposed generation attempt produced no visible image candidate and no generated output path, return `blocked` with
`blocked_no_candidate`. Do not inspect a storyboard, contact sheet, style reference, prompt board, or prior image as if
it were the new candidate unless Harley explicitly identifies that item as the candidate under review.

For ordinary GPT-side image production, the safe cadence is:

```text
generate candidate -> stop
user asks QA -> run QA -> accepted / edit_required / regenerate_required / blocked -> stop
user separately authorizes GPT-side generate/edit/regenerate in a later current turn -> authorization gate -> image preflight -> one new image call outside this skill -> stop
```

## Authorization boundary

QA cannot be converted into an image call inside the same response. If the current turn asks for QA and seems to imply a
follow-up mutation, first return the QA decision and stop. Ask Harley to issue a separate latest-turn generation or edit
command if the repair should be applied.

Hard non-authorizations include:

- `what does QA say?`
- `QA please`
- `review it`
- `critique this`
- `what failed?`
- `give me the repair prompt`
- `continue with QA`
- `accepted`
- any QA decision of `edit_required` or `regenerate_required`

Ordinary GPT-side downstream generation may resume only when the Adventures current-turn image-credit authorization gate has a fresh proof object with non-empty exact `quoted_authorizing_words` from a later user turn. A repair packet, failure diagnosis, or `regenerate_required` decision is not that proof object.

## Source and evidence discipline

Use repo truth when QA depends on canon, asset availability, issue state, storyboard packets, playbooks, accepted source
images, or template contracts. Use live GitHub API routes for exact issues/files/comments/commits when available. Use
bound `file_search` GitHub for broad repo discovery, stale-pattern sweeps, and indexed reads when available. Do not
claim repo absence from a search miss if live API reads work.

When Patch or known repo assets appear, QA must check whether the relevant asset families and style references were
inspected through the current repo-indexed route or a stated fallback. If asset discovery was required but missing,
return `blocked`, `edit_required`, or `regenerate_required` according to whether the candidate can be repaired without a
new source pass.

## Storyboard compliance gate

When a storyboard packet, deterministic layout diagram, prompt board, or locked reference set exists, judge the
candidate against that hard gate before ordinary attractiveness. Report `Storyboard compliance` explicitly. Return
`edit_required` or `regenerate_required` when the candidate violates a storyboard hard gate, even if mood or style is
strong.

Examples of hard gates:

- a route, line, edge, or crossing is in the exact required place;
- an accessible path remains physically open;
- a false line or gag carrier is closest to the intended character path;
- held, stamped, attached, occluded, or transformed props are physically coherent;
- the deterministic diagram's highlighted relationship is preserved;
- selected references and excluded images were respected.

## Preflight and prompt-governance check

QA must check whether the candidate reflects the mandatory preflight packet. Evidence that assets were found is not
enough. The inspected style and task assets must have become visible constraints in the generated result.

Return `regenerate_required` or `blocked` when the candidate proves that the prompt was asset-blind, insufficiently
constrained, or failed to honor mandatory style, Patch, prop, text, physical-logic, or reference-lock constraints.

## Patch gates

Patch is the hero anchor. He is not a human boy, generic robot, screen-face bot, mascot, plush, glossy 3D toy, or
replaceable AI icon. Other agents, humans, consultants, tools, and systems must be distinct from Patch.

Reject or block when Patch appears as:

- a human boy or ordinary human in a hoodie;
- a generic robot, screen-face bot, metal android, plush, toy, or glossy 3D mascot;
- duplicate Patch bodies, Patch-shaped teams, Patch-shaped audiences, or Patch-like consultants;
- missing teal hoodie, hood antennae, dark pants, teal shoes, crossbody bag, visible strap, or `>` bag mark;
- white sclera, irises, anime eyes, human eyes, doll eyes, coloured pupils, or alternate eye styles.

Canonical Patch uses a teal hoodie, hood antennae, off-white face panel, black oval eyes with small white shine
highlights, dark pants, teal shoes with white soles, and a teal crossbody bag with visible `>` symbol.

## Non-Patch distinction

Reject when another character borrows Patch identity markers: teal hoodie as main read, hood antennae, teal crossbody
bag, `>` bag symbol, off-white Patch face panel, full Patch silhouette, or Patch-like eye/face construction. Other
agents may be bots, specialists, systems, or screens, but they must remain clearly non-Patch. Humans must read as humans
and not as Patch variants.

## Lanes

Choose one primary lane before judging.

### `patch_scene`

Use for deck body-slide or scene art featuring Patch. Accepted output: `accepted_scene_art`. Check Patch identity,
scene fit, slide/story beat fit, text posture, non-Patch distinction, storyboard/preflight compliance, and source
evidence. Reject if source assets or preproduction references are used as substitute scene art in a proof/full/final
run.

### `patch_preproduction_reference`

Use for Patch-bearing asset sheets, interaction sheets, scale proofs, environment references, prop references, or role
sheets. Accepted output: `accepted_preproduction_reference`. A preproduction reference is not body-slide art.

### `non_patch_preproduction_reference`

Use for generated environments, locations, props, supporting characters, and style sheets without Patch. Check lane,
style, role/function mapping, physical logic, text discipline, canon boundaries, and task-relevant asset discovery.

### `asset_sheet_lane_compliance`

Use when checking whether a generated or deterministic sheet matches its lane. Reject omnibus posters unless explicitly
requested. Accepted use is only `accepted_preproduction_reference` after source-image QA and compiled-sheet QA both pass
where applicable.

### `anti_pattern_reference`

Use for intentionally wrong examples. Accepted output: `accepted_antipattern_reference`. Block if wrong examples could
be mistaken for canon.

### `deck_package_image_review`

Use for package-level checks of images embedded in a deck or candidate package. Verify every required scene image has an
accepted QA decision and no unreviewed, rejected, source-only, or reference-only image entered proof/full/final slides.

### `psa_board_review`

Use for PSA-returned storyboard sheets, prompt boards, route/geometry diagrams, repair boards, or reference-role boards. Accepted output is `suitable_for_pig_grounding`, not accepted scene art. Check requested output count, panel count, labels, route/geometry hard gates, must-show and must-not-show coverage, reference-role clarity, prompt-safe wording, and whether operator context has leaked into the board. Return `needs_psa_repair` when the board misses a hard planning requirement; return `useful_but_not_binding` when it can support discussion but should not control PIG generation.

## Source-image QA versus compiled-sheet QA

For deterministic asset-sheet production, distinguish two QA moments:

1. Source-image QA: judge each generated source image or view before compilation. Check style, identity, physical logic,
   text discipline, and downstream reference usefulness.
2. Final compiled-sheet QA: after deterministic compile, judge lane compliance, panel order, captions, crop safety,
   template fidelity, layout consistency, footer/title accuracy, and whether only QA-accepted source images were used.

A polished compiled sheet cannot rescue a weak or unaccepted source image. An accepted source image does not
automatically make the final compiled sheet canonical; the final sheet still needs layout/lane QA and Harley approval
before repo canonisation.

For final compiled asset sheets, check:

- approved blank template layout is used, not a generated poster or freeform montage;
- baked template labels such as `ASSET SHEET`, `GUIDANCE`, and `ALTERNATE VIEWS` are respected when applicable;
- title/type/status/version/source-QA text comes from the sidecar/spec and leaves no placeholder prose;
- guidance bullets fit without spilling;
- optional slots are left empty rather than squeezed;
- only QA-accepted source images are used;
- final package includes rendered PNG, accepted source images used, and markdown or JSON sidecar/spec;
- scratch HTML, helper scripts, and compile manifests are not treated as durable deliverables unless promoted.

For character asset sheets, require a full-body plain-white-background hero/main source image unless the governing
contract or Harley explicitly waives it.

## Text and operator-context checks

Short functional in-world labels are acceptable. Reject or repair when text is long, garbled, misspelled, wrong-canon,
operator-facing, or required for the asset to make sense. Reject or repair if the image includes bootstrap notes,
session-buster-v0.1 text, issue comments, candidate numbers, repo paths, source-zip names, skill-install notes, sidebars,
checklists, QA labels, pass/fail labels, or process reports unless Harley explicitly requested a status artifact.

## Working-loop and repo-record discipline

During an active visual-preproduction loop, QA decisions are working loop state unless a durable reporting threshold is
met. Do not post per-candidate QA comments to GitHub. Persist to repo only when Harley approves a QA-pass candidate or
package, a hard blocker needs durable tracking, Harley explicitly asks to preserve a planning decision, or a final stage
readiness report is complete.

## Repair-prompt hygiene

When returning `edit_required` or `regenerate_required`, provide repair constraints and stop. A repair prompt, repair plan, image-generation brief, or next-generation plan remains text-only and does not authorize the next image call. This is the point of the QA lane: preserve review momentum without converting it into credit spend.

Translate failures into:

- concise positive visual constraints;
- exact hard negatives for the failure mode;
- preserve clauses for features that passed;
- text-budget and operator-context quarantine reminders when relevant.

Do not paste QA reports into future prompts. Do not encourage candidate numbers, issue comments, repo/process notes, or
checklists in an image prompt. For Patch drift, prefer whole-character constraints over isolated attributes and avoid
terms that trigger bad priors, especially `robot`, `cute robot`, `mascot`, `toy`, or `bot`.

## Bible-backed QA and repair

When a relevant Adventures visual bible exists, QA should use bible-backed hard gates and micro-specs rather than
memory. If the bible is missing, incomplete, or lacks extractable prompt/QA/repair blocks, make the best current QA
decision from
available evidence, report the bible-surface gap, and recommend `adventures-visual-bible-creator-v1` for normalisation or
locking. Do not invent durable canon during QA.

For Patch-bearing QA, run gates in this order before scene-quality judgment:

1. whole-character Patch identity;
2. eyes, antennae, bag, hoodie/body, trousers/shoes, face/hood relationship, non-robot read;
3. Patch singularity and non-Patch distinction;
4. style-system fit;
5. lane/artifact fit;
6. text and operator-context quarantine;
7. scene, prop, and downstream usefulness;
8. accepted-use scope.

A hard-gate failure cannot be softened into a watch note because other scene elements improved.

## Output contract

Return this compact decision:

```markdown
Image QA decision
- Candidate:
- Lane:
- Decision:
- Accepted use:
- Asset discovery evidence:
- Patch status:
- Non-Patch distinction:
- Sheet/lane status:
- Asset-sheet template/package status:
- Character hero-shot status:
- Text/label status:
- Physical/style status:
- Prompt-governance status:
- Storyboard compliance:
- Failures:
- Required repair prompt:
- Next action:
```

Use one decision value:

- `accepted_scene_art`
- `accepted_preproduction_reference`
- `accepted_antipattern_reference`
- `edit_required`
- `regenerate_required`
- `blocked`

For `edit_required` or `regenerate_required`, the next action must be `wait_for_separate_generation_authorization` or a similarly explicit text-only stop through the current-turn image-credit authorization role.

## Boundaries

Do not accept a candidate just because it is attractive. Do not rewrite canon to match a generated image. Do not call a
candidate canonical; canonisation and repo landing are downstream after QA acceptance. Do not call image generation from
this skill under any circumstances.
