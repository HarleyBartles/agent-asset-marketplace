# Prompt contract

Translate an approved visual direction into a provider-ready operation without
quietly becoming the creative director. The direction owns the story job, frame,
attention, and intentional constraints. This contract makes those decisions
legible to a generator and records what remains open.

## Required brief

Use only fields relevant to the operation, but keep the order stable:

```text
Intent/story job: <what the image should make the audience know, feel, or do>
Operation: generate | edit | variation | inpaint | outpaint | composite | cutout | convert
Asset/use: <page, route, game screen, article, social crop, or private preview>
Subject/action: <who or what; the decisive beat>
Composition: <orientation, crop, scale, placement, viewpoint, perspective, depth layers>
Attention: <primary/secondary/tertiary read; focus and visual path>
Environment: <setting, foreground/midground/background, useful negative space>
Lighting/mood: <source, direction, contrast, colour temperature, atmosphere>
Palette/material: <role-based colours, surface and style characteristics>
Input images: <index, role, and intended influence for each input>
Locked invariants: <must remain unchanged>
Allowed changes: <the exact region or property that may change>
Avoid: <specific failure modes, unwanted objects, text, marks, or drift>
Text: <verbatim copy, placement, and legibility requirement, if any>
Output: <dimensions/aspect, format, alpha, naming, and destination>
```

The `Intent/story job`, `Operation`, `Subject/action`, `Composition`, and
`Output` fields are required for a project-bound result. If any is unknown, return
`not generated because the brief is incomplete` or route the open decision to
`directing-visual-stories`. Do not fill an omission with a tasteful guess when it
would change crop, viewpoint, scale, lighting, palette, or story meaning.

## Input-image roles

Label each input before writing the prompt. One image may have multiple roles only
when that is explicit and safe.

| Role | Preserve or borrow | Common mistake |
| --- | --- | --- |
| Edit target | The image being changed | Treating it as a loose style reference |
| Content/source | Object, setting, or factual detail | Copying its composition accidentally |
| Identity/character | Recognisable person, character, or design | Allowing face, costume, or silhouette drift |
| Composition | Crop, camera, pose, spatial arrangement | Importing its subject or palette unintentionally |
| Style/material | Rendering language, texture, medium | Replacing the approved story direction with a style |
| Palette/light | Colour relationships or illumination | Treating a colour cue as a whole-scene recolour |
| Mask | Editable region and boundary | Assuming white/black semantics without checking |
| Composite insert | Element to place into another field | Ignoring scale, perspective, and light matching |

Refer to inputs by index and role in the prompt. State whether the influence is
strict (`match`) or suggestive (`borrow the surface quality only`).

## Translate, do not inflate

Preserve the user's nouns, exact copy, and intentional awkwardness. Expand only
where the contract needs an operational description: camera distance, light
direction, layer order, mask boundary, or output format. Never add a character,
narrative beat, slogan, brand, or side placement merely because it is common in a
generator's examples.

For edits, repeat the invariants and allowed change in the operation sentence:

```text
Change only: <region/property>.
Keep unchanged: <subject, crop, viewpoint, perspective, silhouette, lighting, palette, and text as applicable>.
Reject: <specific drift that would make the edit unusable>.
```

## Prompt assembly

Use this compact order unless the selected adapter requires another syntax:

1. operation and story job;
2. subject/action and environment;
3. composition and attention path;
4. lighting, palette, material/style;
5. input roles;
6. invariants, allowed changes, and avoid list;
7. exact text and output requirements.

Keep provider parameters in the adapter record, not in the creative prompt. The
final brief trace must preserve both the human direction and the translated prompt
so later reviewers can tell which choice came from where.
