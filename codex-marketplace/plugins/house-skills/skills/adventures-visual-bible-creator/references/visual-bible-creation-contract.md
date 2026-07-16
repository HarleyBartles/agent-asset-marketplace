# Operating contract

This reference preserves detailed operating guidance moved out of `SKILL.md` during progressive-discovery decomposition. Load it only when the compact control plane says the current task needs the full workflow.

# Adventures Visual Bible Creator

Use this skill to author, update, normalise, or lock Adventures visual bibles for reusable visual asset classes.

This is deterministic no-credit visual doctrine work owned by GPT/project workflow. It writes visual-bible content and extractable prompt, QA, repair, extrapolation, and PIG-consumable constraint blocks. It does not generate images, edit images, accept images, run image QA, build decks, compile asset sheets, canonise assets into the repo, post issue comments, or mutate repositories. PIG may consume a current visual bible as production constraints, but PIG does not author, lock, canonise, or accept the bible.

The house pattern is the Patch v1.4 bible shape: concise visual canon plus mechanically extractable prompt, QA, repair, and extrapolation blocks. Do not copy Patch canon into other assets. Copy the operational shape and level of detail.

## Source route discipline

When repo or connector evidence is needed, separate broad discovery from exact operations. Use a bound `file_search` GitHub route for repo-wide discovery, stale-pattern sweeps, and indexed corpus reads when it is available. Use live GitHub API routes such as `api_tool` for exact issue, comment, file, commit, compare, and authorized mutation operations.

If `file_search` is not bound and broad repository discovery would materially reduce risk, ask Harley to bind the relevant GitHub connector before continuing or state that the task is operating from narrower live API spot checks. Do not treat an unbound `file_search` route as repo absence when another live GitHub route works.

## Scope

Create or update bibles for environments, locations, character classes, individual characters, prop families, continuity objects, costume/gear systems, interaction motifs, and world/theme classes.

This skill may make a bible generation-ready by preparing reusable text for a later GPT-side image-preflight, image-planning stage, or PIG production handoff. Generation-ready text is not image-generation authority for GPT. A later current-turn user request, `adventures-visual-intent-gate`, image preflight, and the proper GPT-side visual-mutation workflow must still authorize any GPT-side image generation or generative editing. For PIG, a bounded PIG production job may consume the bible as constraints under the PIG skill stack; PIG self-QA still does not equal project acceptance.

## Operation classes

Classify the work before choosing any route:

```yaml
owned_deterministic_no_credit:
  - source issue and repo evidence review
  - visual-bible creation or update
  - evidence partitioning
  - prompt-positive and prompt-negative canon block drafting
  - QA hard-gate checklist drafting
  - repair block and extrapolation rule drafting
  - bible state assessment
not_owned_non_credit_pixel_work:
  - deterministic asset-sheet compilation
  - contact-sheet rendering
  - deterministic image crop or annotation
not_owned_credit_spending_mutation:
  - generating a new image candidate
  - regenerating a failed candidate
  - generatively editing an existing image
not_owned_repo_mutation:
  - committing bible files
  - posting issue comments
  - canonising assets into repo indexes
```

If the user asks for a non-owned task, hand off to the appropriate downstream task route instead of doing it here. If the user asks for image generation or editing, stop at the bible output and require `adventures-visual-intent-gate`, image preflight, and the proper visual-mutation workflow before any image tool call.

## Source discipline

Start from repo truth when the task depends on existing project state.

1. Read the source issue or task.
2. Start asset discovery from `assets/INDEX.md`.
3. Follow the index mesh to relevant asset families, style guides, current visual package evidence, package indexes, and existing bibles.
4. Use accepted generated images or Harley-supplied images only as scoped visual evidence.
5. For repo-canonical image inspection, use the current repo-indexed visual inspection route, normally a Patch-returned asset/contact-sheet package derived from the asset index mesh when GPT needs to inspect pixels.
6. Partition evidence as repo text, current repo-indexed visual package evidence, accepted generated reference, user-supplied visual evidence, package-only evidence, inference, and uncertainty.

Do not treat session handoffs, QA prose, issue comments, or unaccepted candidates as audience-facing content.

## Bible states

Use these states:

- `minimal_provisional` - enough to steer first Pass A generation and QA.
- `updated_provisional` - refined from accepted Pass A or intermediate accepted references.
- `locked` - refined from accepted Pass B family sheets and ready as durable visual source doctrine.
- `amber_text_only` - enough text exists, but visual evidence could not be inspected.
- `blocked_missing_bible` - an expected existing bible cannot be found.

A bible may be generation-ready while provisional. Do not call it locked until accepted family imagery supports that. Do not treat `generation-ready`, `minimal_provisional`, or `locked` as permission to generate, regenerate, or edit images in this turn.

## Standard bible shape

Use this outline unless the lane has a strong reason to omit a section:

```markdown
# <Asset Name> Visual Design Guide vX.X

## Version note
## Evidence basis
## Asset overview
## Function and narrative role
## Visual style
## Palette
## Materials / construction / environment language
## Anatomy / layout / location system
## Text and signage posture
## Belongs in this asset family
## Does not belong in this asset family
## Allowed variation
## Do's and Don'ts
## Extractable Prompt and QA Blocks
### Prompt-positive canon block
### Prompt-negative canon block
### Sensitive detail micro-specs
### QA hard-gate checklist
### Feature-specific repair blocks
### Extrapolation rules
### Prompt guidance for image generation
## Reference note
```

Adapt section names by lane. Environment bibles should emphasise layout, materials, palette, signage, location system, member locations, character contamination risks, and omnibus-poster risks. Character bibles should emphasise identity-critical anatomy, wardrobe, face, props, expression, pose, and scale. Prop bibles should emphasise object states, handling, labels, continuity semantics, and success/failure variants.

## Minimal provisional bible

Before Pass A generation for a new reusable asset class, produce a minimal bible that includes at least:

- asset name, lane, source issue, and bible state;
- evidence basis and known uncertainty;
- intended tone, function, and visual direction;
- positive and negative prompt blocks;
- text/signage posture where relevant;
- belongs and does-not-belong boundaries;
- QA hard gates.

If no images exist, write from concept, repo text, and explicit user direction. If accepted images exist, extract durable palette, materials, motifs, layout rules, anti-patterns, and repair constraints from them.

## Updating and locking

After accepted Pass A source imagery and its deterministic overview sheet, update the bible from durable visual learning. After accepted Pass B source images and compiled member sheets, update and lock the bible or leave it explicitly provisional with unresolved questions.

Treat source imagery and compiled sheets as separate evidence. Source images teach visual canon; compiled sheets teach layout, panel order, captions, and usable reference structure. Do not canonise malformed text, accidental objects, distorted anatomy, one-off decorations, image-generator glitches, or composition accidents. Failed imagery should become anti-pattern guidance only when repeated, durable, or semantically important.

## Extractable block discipline

Image-facing blocks must be directly reusable.

Prompt-positive blocks should say what to draw in clean visual language. Prompt-negative blocks should say what not to draw. Repair blocks should preserve passed features and repair one failure family. Extrapolation rules should separate safe variation from canon-sensitive features.

Do not paste QA prose, candidate numbers, repo paths, issue comments, status labels, process notes, sidebars, or checklists into prompt-facing blocks.

Prompt guidance and repair blocks are later-stage inputs, not tool-call permission. They may be handed to image planning, image preflight, or QA, but this skill must stop after producing or updating the bible unless Harley separately asks for a downstream deterministic handoff.

## Output contracts

For direct bible creation, return the bible in markdown.

For planning or review, return:

```markdown
## Bible creator report

- Source issue/task:
- Asset/lane:
- Input evidence:
- Existing bible:
- Target bible state:
- Gaps found:
- Recommended updates:
- Status:
- Downstream handoff, if any:
```

## Stop conditions

Stop or hand off instead of continuing when:

- visual evidence must be QA-accepted before bible locking;
- the task requires deterministic asset-sheet compilation or contact-sheet rendering;
- the task requires repo mutation, issue comments, or canonisation;
- the task asks for image generation, regeneration, or generative editing;
- the source issue, asset index, existing bible, or visual evidence cannot be inspected sufficiently for the requested confidence.

Do not let a bible state, prompt block, QA checklist, repair block, accepted concept, or workflow momentum authorize image generation. Image-generation credits are scarce Adventures production capacity, and deterministic bible work exists to reduce failed image calls before the proper visual-mutation stage.


## Retired visual bridge guard

Do not route repo-canonical image inspection through retired Google Slides view-surface registries or rendered slide thumbnails. Non-owner skills should describe the current visual-inspection capability rather than hard-code stale bridge paths. A stale visual bridge must not launder missing visual evidence into a locked bible, prompt block, QA gate, or downstream image-readiness claim.
