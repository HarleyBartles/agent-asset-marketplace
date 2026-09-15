---
name: generating-images
description: Use when an authorised image capability must generate, edit, vary, or inspect a raster image from a creative brief or an existing image while preserving explicit visual decisions and reporting truthful asset custody.
metadata:
  source-id: generating-images
  source-path: codex-marketplace/plugins/visual-storytelling-pack/skills/generating-images/SKILL.md
  provenance-name: Generating Images adapted derivative
  source-category: skills-with-source
  status: active
  owner: Harley Bartles
  scope: Provider-neutral raster generation, editing, inspection, and custody after creative direction.
  use_when:
  - an approved visual direction must become a generated or edited raster asset.
  do_not_use_when:
  - crop, viewpoint, lighting, palette, or story intent remains unresolved.
---

# Generating Images

This is a portable, capability-based image generation and editing workflow. It is
a substantially modified Apache-2.0 derivative of the `imagegen` skill named in
[`NOTICE.md`](NOTICE.md), with Codex-harness, provider, and environment assumptions
removed.

## Boundary

Use `directing-visual-stories` first when crop, scale, viewpoint, perspective,
focus, lighting, palette, attention, or story intent is unresolved. This skill
translates an approved direction into generation or editing work; it does not
quietly make those creative decisions by omission.

Use this skill when the requested output is a raster image: new image, variation,
edit, inpaint/outpaint, composite, cutout, or format conversion. Prefer native
vector, HTML, CSS, or canvas workflows for code-native results.

## Route by operation

| Need | Read next |
| --- | --- |
| Discover whether the environment can perform the required operation | [`references/capability-routing.md`](references/capability-routing.md) |
| Turn a direction into a provider-ready brief | [`references/prompt-contract.md`](references/prompt-contract.md) |
| Choose generate, edit, variation, compositing, or conversion | [`references/generation-and-editing.md`](references/generation-and-editing.md) |
| Preserve crop, pose, lighting, palette, or other locked decisions | [`references/preserving-frame-invariants.md`](references/preserving-frame-invariants.md) |
| Inspect, compare, iterate, or report a failed result | [`references/validation-and-iteration.md`](references/validation-and-iteration.md) |
| Place, attribute, and hand off the selected asset | [`references/asset-handoff-and-custody.md`](references/asset-handoff-and-custody.md) |

Read only references needed for the operation. Provider or harness details belong
in a routed adapter, never this entrypoint.

## Required flow

1. Identify operation, intended use, output format, and whether the result is
   preview-only or project-bound.
2. Confirm the creative direction exists. Record unresolved creative choices as
   open decisions for `directing-visual-stories`; do not invent them.
3. Label each input image by role: edit target, content/reference source,
   identity/character, composition, style/material, palette, mask, or composite
   insert.
4. Select an authorised capability by behaviour: the required generation/edit
   operation, reference support, transparency or mask support, output delivery,
   and provider constraints. Use an adapter only after this requirement is known.
5. Translate the direction into a concise prompt or operation specification,
   preserving exact text, invariants, avoid items, and output requirements.
6. Generate or edit without overwriting source assets. Inspect the full frame and
   relevant details against the direction and invariants.
7. Iterate one material defect at a time. Keep variants comparable and report
   capability failure, unresolved defects, or missing custody evidence plainly.
8. Hand off the selected asset with its actual location or provider result,
   operation and capability used, references and roles, prompt/brief trace,
   inspection result, unresolved defects, and licence/provenance.

## Terminal outcomes

The workflow ends with exactly one truthful state: `selected and handed off`,
`generated but unresolved`, `blocked by missing capability`, or `not generated
because the brief is incomplete`. Never imply an image exists when the selected
capability did not return one, and never leave a project-bound asset only in an
untracked provider or temporary location.

Record real uses in [`assets/field-trial-notes.md`](assets/field-trial-notes.md);
one Portfolio preference is not automatically a universal rule.
