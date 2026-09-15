# Translating to image generation

Use this route after the creative direction has settled the story job and frame.
The image brief is a translation boundary: `directing-visual-stories` owns the
meaningful visual decisions; `generating-images` owns provider syntax, execution,
inspection, and durable asset custody.

## Frame-direction handoff

Return a labelled frame direction before writing a provider prompt:

```text
Audience change / beat:
Subject hierarchy and evidence:
Composition (crop, scale, aspect, viewpoint, perspective, placement, negative space):
Depth and focus (foreground, middle-ground, background, occlusion):
Attention path (first, second, final read):
Light / palette / material / atmosphere:
Motion or stillness / off-frame implication / withheld evidence:
Containing field or sequence relation:
Rationale / rejected alternatives / avoid list:
Locked invariant:
```

One frame may be a complete field. If it is an inset or one frame of a sequence,
also state its relation to the containing page, spread, screen, or world. Do not
leave crop, camera, focus, palette, or story meaning for the generator to invent.

## Handoff to `generating-images`

Pass the approved direction into the exact relevant field order in
[`generating-images` prompt contract](../../generating-images/references/prompt-contract.md):
`Intent/story job`, `Operation`, `Asset/use`, `Subject/action`, `Composition`,
`Attention`, `Environment`, `Lighting/mood`, `Palette/material`, `Input images`,
`Locked invariants`, `Allowed changes`, `Avoid`, `Text`, and `Output`.

The director supplies intent/story job, subject/action, composition, attention,
environment, lighting/mood, palette/material, input-image roles, invariants,
allowed changes, avoid items, and exact text or creative constraints. Task or
adapter context supplies operation, asset/use, output, and provider details; do not
invent those as creative choices. Use only fields relevant to the operation. If a
creative field is unknown, stop at `not generated because the brief is incomplete`;
if an operational capability or destination is unknown, remain blocked without
silently changing the direction.

Label every input image by role (edit target, content/source, identity/character,
composition, style/material, palette/light, mask, or composite insert). Specify
whether the influence is strict or suggestive. Never let a reference image quietly
replace the approved subject, story, or composition.

## Result and custody boundary

`generating-images` translates, runs the authorised capability, validates the
result against the invariant ledger, and reports the actual durable destination.
This skill may reject a result whose story job, hierarchy, crop, or attention path
did not survive, but it does not own provider configuration or asset placement.
Keep the human direction and translated prompt together in the brief trace so a
later review can distinguish a creative choice from an adapter default.

### Avoid

- prompting with a medium label such as “cinematic” instead of a camera and story;
- adding props, characters, slogans, or side placements to make a scene feel full;
- treating a canonical work or artist as a style prompt;
- accepting attractive pixels that lose the beat, crop, or invariant;
- claiming a preview, temporary URL, or UI label is a project-bound asset.
