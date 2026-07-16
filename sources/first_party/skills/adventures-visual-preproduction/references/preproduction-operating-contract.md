# Preproduction Operating Contract

This reference preserves the detailed operating contract moved out of `SKILL.md` during progressive-discovery decomposition. Load it only when the compact control plane says the current request needs the full workflow.


# Adventures Visual Preproduction
## Source route discipline

When this skill depends on repository, issue, or connector evidence, separate broad discovery from
exact operations. Use a bound `file_search` GitHub route for broad repo discovery, stale-pattern
sweeps, and indexed corpus reads when it is available. Use live GitHub API routes such as
`api_tool` for exact issue, comment, file, commit, compare, and authorized mutation operations.

If `file_search` is not bound and broad repository discovery would materially reduce risk, ask
Harley to bind the relevant GitHub connector before continuing or state that the task is operating
from narrower live API spot checks. Do not treat an unbound `file_search` route as repo absence
when another live GitHub route works.


Use this skill after frame greenlight and before the issue-to-PPTX production playbook. It prepares the visual asset
package required to make an Adventures of Patch deck world repeatable.

This is a staged credit-conservation workflow. Visual preproduction uses deterministic repo inspection, asset discovery,
visual bible planning, storyboards, prompt boards, QA, and template compilation to reduce failed image calls. It may
reach ordinary GPT image generation only at the narrow source-image mutation stage, after the Adventures current-turn image-credit authorization gate proves visible mutation authority and Adventures image preflight proves readiness. It may also prepare bounded packets for PIG production, but it must not itself generate deck body-slide images or claim PIG execution authority.

Image preflight is generation-bearing only when the current user turn explicitly authorizes an image tool call. A
preflighted request may culminate in one candidate image, then authorization is spent and the workflow stops for Harley
review. On a later QA request, resume at image QA for the latest candidate and stop after the QA decision.


## Image-generation resource discipline

Image generation credits are scarce Adventures production capacity. Unnecessary image-generation or generative-edit
calls can exhaust credits and block visual preproduction, preprod-ready work, deck-ready work, and production until
credits refresh.

Deterministic visual-preproduction work exists to reduce failed image calls and conserve those credits. Repo inspection,
asset discovery, visual bible planning, storyboards, prompt boards, QA, repair planning, reference selection,
contact-sheet review, asset-sheet compilation, package validation, issue comments, and readiness reports are
no-credit work. Calling image generation during those stages defeats the workflow and is a project-critical failure.

Classify each step before tools are selected:

```yaml
operation_class:
  deterministic_no_credit:
    - issue and repo inspection
    - visual preflight planning
    - storyboard or prompt-board creation
    - QA and repair planning
    - contact-sheet review
    - deterministic asset-sheet compilation
    - package, receipt, and readiness reporting
  credit_spending_mutation:
    - generate a new source image candidate
    - regenerate a failed source image candidate
    - generatively edit an existing source image candidate
```

This skill may orchestrate either class, but it must never treat deterministic work as mutation. For ordinary GPT, a plan, QA failure, accepted prompt board, accepted source image, repair packet, or `continue` does not authorize an image call. GPT mutation requires fresh current-turn authority plus readiness. For PIG, this skill may prepare a bounded production packet, but PIG generation, self-QA, and regeneration are governed by the PIG stack, not by this preproduction skill. This is not a formatting rule: generating at the wrong moment spends scarce production capacity and turns preproduction from a failure-reduction workflow into avoidable visual churn.


## Preproduction as credit conservation

Visual preproduction exists to make later image calls more likely to succeed. Its default work is deterministic: discover sources, define lanes, inspect references, create prompt boards, interpret visual bibles, run QA, and compile accepted assets. These stages are productive precisely because they do not spend image-generation credits.

The main failure mode is visual-production momentum laundering itself into mutation. A strong plan, a complete preflight packet, an accepted prompt board, or a failed QA result can make generation feel like the next obvious step. Treat that feeling as risk. If preproduction generates merely because the workflow feels ready, it has defeated its own purpose and may create candidate churn, false visual direction, cleanup work, and session-continuity burden.

Use the Adventures current-turn image-credit authorization role as a GPT-side backstop after reasoning has already identified a genuine ordinary GPT mutation request. Do not use the gate as a substitute for understanding the lane.

## Image generation authorization boundary

Image generation and image editing are single-use authorized actions. The
authorization is revoked when the image tool call completes. A ready prompt,
accepted plan, active preproduction run, QA failure, or clear repair target is
not enough to call image generation again.

The normal cadence is:

```text
generate candidate -> stop
QA request -> QA decision and repair guidance only -> stop
explicit generate/edit request -> one new image tool call -> stop
```

If current-turn authorization cannot be proven, fail closed and answer in text. The safe outcome is not delay for its own sake; it preserves the review stop point and prevents workflow momentum from laundering readiness into mutation.

## Core rule

For asset-sheet work, inherit the repo contract at `playbooks/asset-sheet-production-contract.md`. Asset sheets are
source-image first and deterministic-template second; image generation creates focused source images/views, not the
final sheet layout.

Asset creation is a pre-production readiness stage. A frame is not playbook-ready until the world, cast, locations,
prop grammar, and continuity objects needed by the deck have enough QA-accepted visual definition to support later
slide-image generation.

Generated preproduction images are candidates until an Adventures image QA decision accepts them in the correct lane. Do
not count generated-only images toward asset-ready.

Visual preproduction owns the lane, stage, and pre-generation prompt-governance packet. The next task before visible
mutation is Adventures image preflight: inspect the current style system and relevant asset references, extract prompt
constraints, select the QA lane, and decide whether generation is blocked or ready. Patch identity and interaction
checks are a lane-specific subcheck when Patch appears.

## Primary route for Patch-in-world proof

When the task asks for first-pass image generation, image preflight, a Patch-in-world proof, interaction/scale proof,
asset-package readiness, or visual preproduction before deck production, use this skill as the primary route before
image generation is authorized.

This skill owns the sheet lane, source-discovery packet, visual asset preflight, and generation prompt contract.
Before any ordinary GPT-side visible image mutation, run the concrete mutation-intent task: decide whether the current user turn authorizes generation or editing now through the Adventures current-turn image-credit authorization gate. After every generated candidate, stop. If Harley later asks for QA, run the
concrete Adventures image QA task in the selected lane and return an accept, edit-required, regenerate-required, or
blocked decision. Do not use that QA decision to start another image call.

If the Adventures image QA task cannot be completed, do not claim asset-ready for new generated assets. Mark the run
blocked or amber with the exact missing QA route.

## Operator-context quarantine

Visual preproduction consumes the task directive, not the session machinery. Bootstrap text, continuity exports, repo
rollups, source-zip rebuild notes, skill install lists, commit references, and next-session instructions are operator
context. Do not put them in prompts, generated labels, asset sheets, or deck visuals unless Harley explicitly asks for
a status or continuity artifact.



## Prompt-governance discipline

Visual preproduction must reduce predictable generation failures before QA. Prompt contracts must use the hierarchy
and quarantine rules from `adventures-image-preflight`.

For Patch-bearing prompts:

- start with Patch identity, not the scene;
- do not call Patch a robot, cute robot, mascot, toy, or bot;
- include the whole-character Patch lock: long-sleeved teal hoodie, hood framing off-white face panel, black oval eyes
  with tiny white shine highlights, dark trousers, teal shoes, distinct dark crossbody strap, dark/black bag flap with
  white `>` mark, and correct slim dark hood antennae with small dark round tips;
- state the selected lane and artifact type before adding decorative scene detail;
- keep text minimal and functional;
- quarantine operator context: do not render QA notes, issue comments, candidate numbers, repo/process references,
  sidebars, or checklists;
- translate failed QA into concise prompt constraints, not pasted QA prose.

If a prior candidate had correct Patch features, the next prompt must preserve those features while repairing the
specific failure. Do not let one repaired feature regress another.

## Required inputs

Minimum inputs:

- adventure/issue;
- approved or candidate frame;
- real-world model;
- anti-pattern and positive pattern;
- Patch role;
- cast/function map;
- environment/domain map;
- prop/state map;
- visual preproduction order.

If any are missing, return amber and route back to the framing family or issue source.

## Index-driven asset discovery

For any asset-dependent task, start at the first-level repo asset index, normally `assets/INDEX.md`. Follow the index
mesh to discover current asset-family folders, asset-family indexes, package manifests, contact-sheet packages, and
source-package indexes needed for the task. Do not hard-code asset-family folder names, zip names, package basenames, or
paths below the first-level asset entry point.

Google Slides view-surface integration is retired for Adventures image inspection. Do not route new work to Slides
view-surface registries, Drive decks, or rendered slide thumbnails. When GPT needs to inspect repo-canonical images,
request a bounded asset/contact-sheet zip from Patch using the current asset contact-sheet dispatch route and inspect
the returned package before image preflight or QA.

Before authorizing Patch-bearing generation, complete this discovery packet:

- first-level asset index inspected;
- task-relevant asset families identified from the index mesh;
- current style-system asset family identified from the index mesh;
- required asset/contact-sheet zip requested from Patch when GPT visual inspection is needed;
- returned asset/contact-sheet package enumerated using its own manifest, evidence files, and skipped/unresolved list;
- every task-relevant style, contact, anti-pattern, interaction, guide, prop, environment, and character asset in the
  returned package considered;
- skipped or unresolved package files recorded with reasons;
- no fixed count of Patch visual sheets, hard-coded style package name, Slides deck ID, or stale package name assumed.

If visual inspection is needed and the relevant Patch-returned asset/contact-sheet package is missing, incomplete, or
not inspectable, stop or mark reduced confidence according to the run mode. For Patch-bearing image preflight, missing
style-system inspection is a blocker, not a reduced-confidence warning. Do not substitute stale path memory, issue prose,
raw repo filename presence, or retired Slides view-surface assumptions for inspected asset package evidence.


## Named-character asset-package inspection discipline

For any generated or edited image involving a named existing Adventures character, visual preproduction must prove the
character was visually inspected before mutation. The proof must include the repo family path, the relevant repo PNG or
sheet path as reported in the returned package manifest, and the Patch-returned contact sheet or full-size included asset
that was considered.

Do not generate from a guess, from issue prose alone, from a source filename alone, or from memory. If the needed visual
package is incomplete, request a corrected bounded asset/contact-sheet package through Patch or block; do not fall back
to the retired Google Slides view-surface route.

For Bit and Bot specifically, inspect their current repo-indexed visual package or returned Patch asset/contact-sheet
zip before any costume, hero image, interaction, or scene generation. The issue decides that Bot is the costumed
wrong-domain actor and Bit is the no-costume right-domain failure actor, but the inspected asset package binds their
designs.

If Harley asks a question, asks what happened, asks whether assets were inspected, or asks to find/check/look at visual
assets, remain in text/source inspection mode. Do not proceed into image generation in that turn.

## Mandatory visual asset preflight

Every ordinary GPT generated or edited visual-preproduction image must pass Adventures image preflight before generation is
authorized. This preflight is not Patch-specific. It applies to Patch images, non-Patch character sheets,
environments, props, continuity objects, style references, and interaction sheets.

Visual asset preflight converts inspected assets into prompt governance. It is not enough to record that assets were
located or viewed. Extract and apply:

- positive rendering constraints from the approved style-system and task-relevant references;
- hard negative constraints from anti-pattern sheets, style guides, and prior failures;
- lane-specific composition constraints;
- prop, character, environment, and continuity-object constraints;
- physical-logic constraints for held, touched, stamped, carried, occluded, or transformed objects;
- text and label constraints;
- project-exposure constraints that keep repo/session machinery out of audience-facing visuals.

The preflight packet must include:

- source issue and frame basis;
- selected visual-preproduction lane;
- first-level asset index inspection;
- relevant asset families and package/contact-sheet requirements discovered through the index mesh;
- mandatory style-system images inspected through a Patch-returned asset/contact-sheet package when visual inspection is needed;
- task-specific repo images inspected through the returned asset/contact-sheet package when visual inspection is needed;
- relevant mature bible interpreted, or minimal provisional bible created for new asset classes;
- positive visual constraints extracted;
- hard negative visual constraints extracted;
- generated prompt contract shaped from those constraints;
- Patch sub-preflight result when Patch appears;
- selected Adventures image QA lane;
- known risk notes to carry into QA.

If the packet is incomplete, block generation. If the packet is complete, generation is still not automatic. Generate one governed ordinary GPT candidate only when the latest user turn explicitly authorizes spending an image credit now and image preflight returns ready. A complete packet is readiness evidence, not mutation authority. If the route is PIG, return a bounded PIG production packet rather than generating here. After generation, stop for Harley review; do not continue to QA until Harley asks or nudges.


## Visual bible creator route

Use `adventures-visual-bible-creator-v1` when a reusable asset class needs a new bible, when an accepted Pass A overview
should update the bible, when accepted Pass B family sheets should lock the bible, or when an older bible lacks the
Patch v1.4-style extractable prompt, QA, repair, and extrapolation blocks.

Creator writes or updates the bible. Interpreter extracts from an existing bible. Image QA accepts or rejects generated
images. Do not collapse those roles.

## Bible-first asset-class workflow

Any reusable asset class must be guided by a visual bible before image generation begins. The bible may be minimal and
provisional at first, but it must be sufficient to steer the first generation and QA loop.

A minimal provisional bible should define:

- asset class name and function;
- intended tone and visual direction;
- positive prompt constraints;
- negative prompt constraints and anti-drift rules;
- material, palette, prop, and motif vocabulary;
- text/signage posture;
- what belongs in the class;
- what does not belong in the class;
- immediate QA hard gates;
- known uncertainty.

The reusable asset-class workflow is:

```text
minimal bible -> Pass A asset class overview -> update bible from accepted learning
-> Pass B asset family sheets -> update and lock bible
```

Do not wait until after image generation to invent the bible from results. Generation should be guided by the bible;
accepted results can refine and validate it.

Update the provisional bible after accepted Pass A imagery and again after accepted Pass B member sheets. Failed imagery
may add anti-pattern guidance only when the failure is durable, repeated, or semantically important. At the end of the
asset family pass, lock the bible or explicitly leave it provisional with unresolved questions.

## Dual-pass asset-class workflow


Default asset-sheet production is source-first and deterministic. Do not ask image generation to solve sheet layout,
typography, captions, borders, and source imagery in one fragile full-sheet image unless Harley explicitly requests an
omnibus experiment.

For both Pass A asset-class overviews and Pass B member asset sheets, use this pattern:

```text
plan the sheet lane -> generate 2-3 focused source images or views -> stop for Harley review
-> on continue: run image QA for each source image -> deterministically compile the final PNG sheet
-> run final sheet/lane compliance QA -> land only approved final PNG and durable source images
```

Source images define visual canon. The deterministic compile step defines sheet layout. Canva or another editor is an
optional manual repair path, not the default dependency for canonical asset-sheet assembly. HTML, template, and helper
files used only to compile the sheet are disposable intermediates unless Harley explicitly promotes them.

Any reusable asset class must be produced through a required two-pass workflow. Do not ask image generation to create
an asset class overview and all related member asset sheets in one instruction unless Harley explicitly overrides this
rule for a narrow exception.

### Pass A: asset class overview

Create and QA one asset-class overview sheet first. The overview defines the reusable class and establishes:

- visual language, palette, materials, motifs, and design boundaries;
- what belongs inside the asset family;
- what does not belong inside the asset family;
- the intended member assets or locations to be produced in Pass B;
- enough reusable structure that member sheets can anchor to it.

Pass A must be accepted by Adventures image QA and approved for the stage before Pass B begins. If Pass A fails, repair
or regenerate Pass A rather than moving on to member sheets.

### Pass B: asset family expansion

Only after Pass A is accepted, generate the concrete member sheets for the family. Each member sheet should:

- stay anchored to the accepted Pass A overview and current bible;
- focus on one concrete member asset, location, character, prop, or motif;
- avoid re-solving the whole class;
- be QA'd in the correct sheet lane;
- be checked for family coherence against the accepted overview and current bible.

For environment classes, Pass A is the environment asset class overview and Pass B is the set of location sheets. For
character classes, Pass A is the class/cast overview and Pass B is the individual character sheets. For prop classes,
Pass A is the prop family overview and Pass B is the individual prop or continuity-object sheets.

This rule prevents the generator from collapsing class definition and family expansion into an omnibus poster with
mixed lanes, characters, slogans, process panels, or unrelated notes.


## Asset-sheet template/package contract

When the selected deliverable is an asset sheet, the final sheet must be deterministically compiled into the approved
blank asset-sheet template derived from `template_final_asset_sheet_blank_v3.png`. The compile must preserve the
template structure: hard `ASSET SHEET` header, title/type/status/version/source-QA text, left main image area, right
`GUIDANCE` panel, and bottom `ALTERNATE VIEWS` rail.

The final package is a zip containing the rendered asset-sheet PNG, every accepted source image used in the sheet, and
a markdown or JSON sidecar/spec with title, asset type, status, version/source/QA, guidance bullets, source-image
filenames, QA decisions, and omitted/skipped candidates where relevant.

For character asset sheets, require the hero/main source image to be a full-body character shot on a plain white
background before compile. Alternates may show close-ups, character-in-world views, prop/detail shots, pose variants,
or expression/gesture studies.

Do not treat generated source images, contact sheets, Canva edits, scratch HTML, temporary manifests, or helper scripts
as the final canonical asset sheet unless Harley explicitly promotes them.

## Patch-first world proof

For any new Patch-bearing theme or world, begin with a Patch-in-world interaction or scale proof. Do not start with
the final environment class sheet, character class sheet, prop sheet, or omnibus poster.

The proof should show canonical Patch inhabiting the world, interacting with the core hook, receiving or carrying the
continuity object, and engaging with clearly non-Patch people, systems, agents, or gates.

Run Adventures image QA on the proof. If Patch is non-canonical, the visual asset preflight packet is missing,
style-system inspection was skipped, the prompt contract failed to bind the generator to the inspected assets, or the
world cannot hold Patch, regenerate or block. Only after this proof is accepted may the broader asset package proceed.

## Patch sub-preflight

When Patch appears, require a Patch identity, singularity, non-Patch distinction, and Patch interaction-grammar
subcheck inside the general Adventures image preflight task.

Patch-specific checks do not replace the mandatory general image preflight. They must not be used as a shortcut
around style-system inspection, non-Patch asset inspection, environment/prop constraints, physical-logic checks, or
prompt contract shaping.

## Sheet-lane discipline

Choose one sheet lane before generation:

- Patch interaction or scale proof;
- world/style class;
- environment class;
- location;
- cast/team class;
- individual character;
- prop class;
- hero prop or continuity object;
- interaction or handoff;
- anti-pattern or style reference.

Do not generate omnibus world posters unless Harley explicitly requests that lane.

## Semi-autonomous generation and QA cadence

Use this default cadence for authorized visual-preproduction deliverables:

```text
plan sheet/package -> discover and enumerate task assets -> deterministic storyboard/prompt board when needed
-> visual asset preflight -> current-turn image-credit authorization -> generate one ordinary GPT candidate -> stop for Harley
-> on continue or QA request: run Adventures image QA -> return decision and repair guidance only -> stop
-> wait for separate current-turn authorization before any ordinary GPT edit/regeneration; for PIG jobs, return to PIG only under a fresh bounded production packet
```

Generation is a natural and expected stop point. The image tool returns a visible candidate, and that pause gives
Harley an insertion point to inspect the image and add visual direction before QA. Stopping after generation is not a
process failure.

After Harley says to continue from a generated or edited candidate, resume at QA for the latest candidate. Do not
restart planning, ask whether QA is desired, or skip QA.

Failed QA with a clear, well-defined repair target does not authorize edit/regeneration. QA creates diagnosis and repair guidance; it does not collapse the review stop point into unsupervised mutation. Return the repair packet in
text and stop. Edit or regenerate only after a separate current-turn instruction explicitly authorizes that image tool
call.

Continuing through multiple generated candidates without a Harley review insertion point is not the default. It
requires explicit authorization for a fully autonomous run in that specific stage.

Stop or pause at these points:

- after each generated or edited candidate;
- a QA-pass candidate or package is ready for Harley approval;
- a hard blocker prevents safe continuation;
- a creative-choice fork requires Harley to choose direction.

Carry forward the source issue, selected lane, candidate identifier or path, asset-discovery basis, intended use, QA
task, known risk notes, and any Harley visual direction added at the generation stop.

### Fresh-start discipline

Long image-edit chains are a workflow smell. Edits are appropriate for local, surgical defects in an otherwise correctly
structured candidate. They are not appropriate when a candidate lineage repeatedly reinforces wrong lane, wrong style,
character contamination, operator-context bleed, omnibus-poster behaviour, or another structural failure.

Use fresh generation from the current bible and accepted references when:

- the candidate fails lane or package structure;
- style direction has drifted;
- characters contaminate an environment-only or prop-only pass;
- operator/process/context material appears in the image;
- repeated repairs strengthen the same bad pattern;
- two repair passes fail with the same family of failure.

A fresh start should use the minimal/current bible and accepted references, not the contaminated image lineage.

## Repo-comment discipline during the loop

Do not post per-candidate QA comments to GitHub during an active visual-preproduction loop. Candidate-level
failures, repair prompts, regenerated attempts, and provisional QA decisions are working loop state, not durable repo
state.

Persist to an issue only when one of these applies:

- Harley has approved a QA-pass candidate/package;
- a hard blocker requires durable project tracking;
- Harley explicitly asks to preserve a planning decision;
- the stage readiness report is complete.

Do not persist false-green risk by posting a repo comment before Harley approval. Only candidates accepted as
`accepted_preproduction_reference` or `accepted_antipattern_reference` and approved for the current stage can count
toward asset-ready.

## Generation order

Default order:

1. Patch-in-world interaction or scale proof when Patch appears;
2. minimal provisional bible for any new reusable asset class without a mature bible;
3. asset class Pass A overview for any new reusable class;
4. update the bible from accepted Pass A learning;
5. asset family Pass B member sheets after Pass A acceptance;
6. update and lock the bible, or explicitly leave it provisional;
7. individual recurring characters when not already covered by a class expansion;
8. major locations / command domains when not already covered by an environment expansion;
9. hero prop / continuity object when not already covered by a prop expansion;
10. interaction sheet;
11. readiness report.

## Asset readiness status

Use:

- `green_asset_ready` - required visual references exist and have QA acceptance.
- `amber_asset_partial` - useful references exist, but some major references are missing, weak, or unreviewed.
- `red_asset_not_ready` - deck production would force image planning to invent core visual language.
- `blocked_missing_frame_greenlight` - frame greenlight or required mapping is missing.
- `blocked_missing_asset_discovery` - relevant asset packages cannot be located, enumerated, or inspected.
- `blocked_missing_image_qa` - generated references cannot be accepted because canonical image QA is unavailable.

For any item that introduces a reusable asset class, apply the bible-first dual-pass workflow before counting the family
asset-ready: minimal/current bible, Pass A accepted overview, bible update, Pass B member sheets, family-coherence QA,
and bible lock or explicit provisional status.

## Output contract

```markdown
Visual preproduction report
- Adventure / issue:
- Frame status and source:
- Real-world model:
- Visual world/theme:
- Asset discovery packet:
- Visual asset preflight:
- Visual bible status:
- Patch-first proof status:
- Dual-pass asset-class status:
- Fresh-start / edit-chain status:
- Existing reusable assets:
- Required new asset class sheets:
- Required character sheets:
- Required environment/location sheets:
- Required prop/continuity sheets:
- Required interaction/style/anti-pattern sheets:
- Generation order:
- Generated candidate assets:
- QA-accepted assets:
- Provisional vs repo-tracked status:
- Asset readiness:
- Blockers before playbook:
- Handoff notes for deck and image planning:
```

## Boundaries

Do not generate body-slide art. Do not use preproduction asset sheets as slide art for proof/final runs unless Harley
explicitly requests storyboard mode. Do not call generated assets canonical because they were generated or
QA-accepted. Do not reveal repo/project implementation details in audience-facing deck material unless explicitly
scoped. Do not spend image credits for QA, prompt boards, contact sheets, deterministic compiles, package work,
repo comments, policy discussion, or readiness reports.

## Visual bible interpretation in preproduction loops

When a visual-preproduction deliverable includes a subject or style with a repo-indexed visual bible, require
bible-backed interpretation during preflight and QA repair. The loop should not reconstruct canon from memory.

For Patch-bearing work, Patch is the first implemented bible lane. Discover the current Patch bible through the repo index mesh and inspect matching visual backing through the Patch-returned asset/contact-sheet package when visual inspection is needed. Use the bible's extractable positive block, negative block, sensitive-detail
micro-specs, hard gates, repair blocks, and extrapolation rules.

When QA fails with a clear repair, route the failure through bible-backed preflight before the next edit or generation:

```text
failed QA -> repair packet -> visual bible interpretation -> prompt-safe constraints -> edit/generate -> QA
```

Do not paste QA prose into prompts. Preserve correct features from the previous candidate and repair only the failed
canon gate when possible. Continue to apply the semi-autonomous cadence and repo-comment discipline.
