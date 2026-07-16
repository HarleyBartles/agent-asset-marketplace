# Operating contract

This reference preserves detailed operating guidance moved out of `SKILL.md` during progressive-discovery decomposition. Load it only when the compact control plane says the current task needs the full workflow.

# Adventures Visual Bible Interpreter
## Source route discipline

When repo or connector evidence is needed, separate broad discovery from exact
operations. Use a bound `file_search` GitHub route for repo-wide discovery,
stale-pattern sweeps, and indexed corpus reads when it is available. Use live
GitHub API routes such as `api_tool` for exact issue, comment, file, commit,
compare, and authorized mutation operations.

If `file_search` is not bound and broad repository discovery would materially
reduce risk, ask Harley to bind the relevant GitHub connector before continuing
or state that the task is operating from narrower live API spot checks. Do not
treat an unbound `file_search` route as repo absence when another live GitHub
route works.


Use this shared-safe skill when Adventures GPT-side image generation, PIG image production, image preflight, visual preproduction, or image QA needs canon-backed
positive prompt blocks, negative prompt blocks, hard gates, sensitive-detail micro-specs, preserve clauses, or repair
constraints from a repo-indexed visual bible.

This skill does not generate images and does not accept or reject images. It discovers and interprets current visual
canon so downstream GPT preflight, PIG production, and image QA do not reconstruct canon from memory.


## Why this skill exists

This skill is not a generic GitHub or image-planning wrapper. It exists because GPT image prompts and PIG production briefs are materially more effective when the positive and negative constraints from a visual bible are extracted as reusable blocks and carried forward wholesale into image preflight, PIG production input, QA repair, and later prompt construction.

The visual bible stores durable relevance constraints: what must be present, what must be absent, what details are sensitive, what may vary, and what failures should be repaired or avoided. Downstream prompt writing becomes less consistent when each run rephrases those constraints from memory or reconstructs them from general style notes. This skill turns the bible into an operational packet so later stages can reuse the exact positive block, negative block, QA hard gates, preserve clauses, and repair blocks without silently weakening them.

Do not trim this role into ordinary repo lookup. The legitimate work here is interpretation: read the current bible and visual evidence, extract the reusable constraint blocks, and stop before preflight, QA, or image mutation.

## Image-credit and operation boundary

This is deterministic no-credit canon interpretation shared across GPT and PIG. It may read repo indexes, visual bibles, style guides, repo-indexed visual packages, Patch-returned asset/contact-sheet evidence, accepted references, and task context; then it may return prompt-safe constraints, PIG-usable brief constraints, QA gates,
repair blocks, preserve clauses, extrapolation rules, and blockers.

It must not call image generation, generative editing, deterministic pixel tools, contact-sheet renderers, asset-sheet
compilers, PPTX builders, or repo/comment mutation tools. A bible packet, prompt block, repair block, QA failure, visual
preproduction need, accepted bible state, or `continue` only prepares downstream work; it is not authority to spend an
image credit.

Use these operation classes:

- `deterministic_no_credit`: bible discovery, repo/source partitioning, prompt/negative/QA/repair/preserve packet
  extraction, visual evidence status, and blocker reporting.
- `non_credit_pixel_work`: deterministic contact sheets, asset-sheet compiles, crops, annotations, thumbnails, or
  layout checks owned by adjacent deterministic pixel skills. Route there instead of doing them here.
- `credit_spending_mutation`: ordinary GPT image generation, regeneration, or generative image editing owned by downstream image
  preflight/generation stages after current-turn visible-mutation authority and readiness gates; or PIG generation owned by the PIG stack after a bounded PIG job is assigned. This skill owns neither route.

If the latest user turn asks ordinary GPT for new or changed pixels, stop this skill after the interpretation packet and route to the
proper image-preflight path. If the request is a PIG production job, hand the interpretation packet to PIG as constraint input. Do not treat this skill's packet as the tool-call proof object or as PIG production completion.

## Bible-first preproduction

For a new reusable asset class, use `adventures-visual-bible-creator-v1` to create or update the minimal provisional
bible before image generation begins. Use this skill after the bible exists to interpret it into prompt, QA, repair,
and extrapolation blocks.

A minimal provisional bible should capture:

- asset class or subject;
- intended tone, function, and visual direction;
- positive prompt constraints;
- negative prompt constraints and anti-drift rules;
- material, palette, prop, motif, and text/signage posture;
- what belongs in the class;
- what does not belong in the class;
- immediate QA hard gates;
- known uncertainty.

The durable workflow is:

```text
minimal bible -> Pass A source images and deterministic overview sheet
-> update bible from accepted learning -> Pass B source images and compiled member sheets
-> update and lock bible
```

When interpreting a bible for asset-sheet production, return constraints for source-image generation or PIG production first. The final
sheet layout, captions, border, and footer belong to deterministic compile after source-image QA. Do not route layout,
caption, border, footer, contact-sheet, or template work to one-shot image generation from this skill; if Harley
explicitly requests an ordinary GPT experiment, still require the downstream adventures-visual-intent-gate and image-preflight gates to establish
current-turn mutation authority. For PIG experiments, require a bounded PIG job and keep final acceptance outside PIG.

Accepted generated images may refine a provisional bible. Failed imagery should become anti-pattern guidance only when
the failure is durable, repeated, or semantically important. At the end of the asset family pass, lock the bible
or leave it explicitly provisional with unresolved questions.

## Source discipline

Start from repo truth. Do not bundle visual bibles into this skill. Do not hard-code second-level asset paths, source
zip names, versioned filenames, project-source package names, or Slides deck IDs.

For every request:

1. Inspect the source issue, frame, candidate, or image task.
2. Start at the first-level repo asset index, normally `assets/INDEX.md`.
3. Follow the index mesh to find the relevant asset family and bible/style guide.
4. When repo-canonical images need visual backing, use the current repo-indexed visual package route, normally a Patch-returned asset/contact-sheet package discovered through the asset index mesh.
5. Inspect relevant contact sheets, anti-pattern sheets, interaction sheets, style guides, and asset sheets from that current visual package evidence before extracting prompt, QA, or repair constraints.
6. Use source zips or project-source packages only for explicit package, import, receipt, rebuild, or integrity tasks, or as a declared fallback when the current visual package route is blocked.
7. Distinguish repo text evidence, repo-indexed visual package evidence, package-only evidence, inference, and uncertainty.

If the relevant mature bible cannot be located through indexes but the task is creating a new asset class, create a
minimal provisional bible packet instead of substituting stale path memory. If the task requires an existing canonical
bible and it cannot be found, return `blocked_missing_bible`. If visual backing is required but current source visuals
cannot be inspected, return `amber_text_only` or block according to the owning playbook.


## Creator handoff

Route to `adventures-visual-bible-creator-v1` when the task is to author a new visual bible, update a bible from accepted
imagery, lock a bible after accepted family sheets, or normalise an older bible into the Patch v1.4-style structure.

This skill resumes after creation/update and extracts the operational blocks. If a bible lacks prompt-positive,
prompt-negative, sensitive-detail, QA, repair, or extrapolation sections, report that as a bible-surface gap and
recommend creator normalisation rather than inventing missing canon from memory.

## Supported lanes

Patch is the first implemented lane because Patch has a repo-indexed style bible.

Use the same method for future lanes when their bibles exist:

- core Adventures style bible;
- Bit/Bot or other agent bible;
- Mission Control bible;
- Identity Emporium or other environment bible;
- character-class, prop, location, or asset-class bible.

Do not claim a future lane is implemented unless a relevant repo-indexed bible has been discovered and interpreted.

## Output packet

Return a compact bible-interpretation packet:

```markdown
## Visual bible interpretation packet

- Source issue/task:
- Lane:
- Bible discovered from repo index, or provisional bible created:
- Bible state: provisional / updated / locked
- Visual backing inspected:
- Evidence basis: repo text / repo-indexed visual package evidence / package-only evidence / accepted generated reference /
  inference / uncertainty
- Positive prompt block:
- Negative prompt block:
- Sensitive-detail micro-specs:
- QA hard gates:
- Repair blocks relevant to this failure:
- Preserve clauses:
- Extrapolation rules:
- Prompt-safe next constraints:
- Do-not-include block:
- Status: green / provisional / amber_text_only / blocked_missing_bible / blocked_missing_visual_evidence
```

## Provisional asset-class bible lane

For a new environment, character class, prop class, costume/gear family, interaction motif, or world/theme class without
a mature bible, create a minimal provisional bible before Pass A generation.

The provisional bible should be updated after accepted Pass A source imagery and compiled overview sheet, and again
after accepted Pass B source imagery and compiled member sheets. At the end of the family pass, lock the bible or
explicitly leave it provisional with unresolved questions.

Do not overfit the bible to one accidental generation error. Use failed imagery as anti-pattern guidance only when the
failure is repeated, durable, or semantically important.

## Patch lane

When interpreting Patch, locate the current Patch style bible through the repo index mesh and inspect current Patch visual references through the repo-indexed Patch visual package route when visual backing is needed. Use the style bible's
extractable prompt and QA blocks when present. Do not rely on remembered Patch wording.

For Patch-bearing generation or QA, prefer these bible sections when available:

- prompt-positive canon block;
- prompt-negative canon block;
- sensitive-detail micro-specs;
- QA hard-gate checklist;
- feature-specific repair blocks;
- extrapolation rules.

If these sections are missing in the discovered bible, derive the smallest needed block from the bible text, mark the
output `amber_text_only`, and recommend updating the bible for mechanical consumption.

## Repair packet support

When invoked after a failed candidate, convert the failed gate into prompt-safe repair material.

Always include:

- the exact failed canon gate;
- positive repair constraints grounded in the bible;
- exact negatives only for the failure mode;
- preserve clauses for features that passed;
- text budget and operator-context quarantine when relevant.

Never ask downstream skills to paste QA prose into image prompts. Convert analysis into visual constraints.

## Fresh-start discipline

Long image-edit chains are a workflow smell. Edits are appropriate for local, surgical defects in an otherwise correctly
structured candidate. They are not appropriate when the candidate lineage repeatedly reinforces a wrong style, wrong
lane, operator-context bleed, character contamination, or omnibus-poster behaviour.

Use a fresh generation from the current bible and accepted references when:

- the candidate fails lane or package structure;
- style direction has drifted;
- characters contaminate an environment-only or prop-only pass;
- operator/process/context material appears in the image;
- repeated repairs strengthen the same bad pattern;
- two repair passes fail with the same family of failure.

A fresh start should use the minimal/current bible and accepted references, not the contaminated image lineage.

## Do not

- Do not generate images, regenerate failed images, or generatively edit images.
- Do not treat extracted prompt blocks, repair blocks, preserve clauses, bible state, QA findings, or workflow momentum
  as authorization for an image call.
- Do not accept, reject, or certify images.
- Do not bundle Patch's style bible or visual sheets into this skill.
- Do not hard-code current repo paths below first-level indexes as permanent canon dependencies.
- Do not use stale project-source package names from memory.
- Do not treat source zips or project-source packages as the normal image-inspection truth for repo images.
- Do not treat an attractive generated image as evidence that canon was followed.
- Do not broaden a failed output into a negative rule without checking the bible or visual reference.
