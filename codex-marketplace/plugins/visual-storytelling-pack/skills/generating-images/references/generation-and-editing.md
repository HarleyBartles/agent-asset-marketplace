# Generation and editing operations

Choose the operation from the user's desired change, not from the capability's
most convenient button. A reference image does not make a request an edit: it is
an edit only when an existing target must be changed while some of it remains
invariant.

## Operation choice

| User need | Operation | Composition risk |
| --- | --- | --- |
| Create a new scene or asset with no target | `generate` | High; direction must be explicit |
| Explore the same brief with comparable alternatives | `variation` | Medium; hold prompt, inputs, and output constant |
| Change a defined part of an existing target | `edit` | Medium to high; use an invariant ledger |
| Change a masked interior or local region | `inpaint` | Local geometry and light can still drift |
| Extend the field beyond an edge | `outpaint` | High; new space must obey frame and perspective |
| Merge a source into a target | `composite` | High; match scale, perspective, light, grain, and depth |
| Remove the background while preserving subject edges | `cutout` | Silhouette and alpha quality are hard requirements |
| Change dimensions or encoding only | `convert` | Composition should not change; verify pixel geometry |

If the requested change would alter a locked composition, stop and obtain a new
direction. Do not disguise outpainting as a conversion or a new generation.

## Generate

1. Confirm the story job, composition, attention path, and output contract.
2. Select references by role and state whether they are strict or suggestive.
3. Write the prompt contract, including what must remain empty or quiet.
4. Generate one comparable draft or a deliberately small variant set.
5. Inspect and record defects before asking for another version.

For a page hero, for example, “usable negative space” is an invariant only if the
direction says where copy will sit and how much field must remain calm. Do not
invent a generic centred subject because it is easier to generate.

## Edit, inpaint, and outpaint

Create an invariant ledger before editing. Name the target, editable region, mask
semantics, permitted transformation, and rejection conditions. Repeat the ledger
on every iteration. Inpainting may alter nearby edges, shadows, reflections, or
text; inspect those areas even when the mask is narrow.

Outpainting is a composition change by definition. It requires an approved new
frame boundary, horizon/perspective treatment, depth continuation, and negative
space decision. If the new boundary is not intentional, route back to the creative
direction skill.

## Variations

Use variations to test one creative variable at a time: for example, focal
distance, light contrast, or material treatment. Keep the operation, source
direction, aspect, references, and output constraints fixed. Label each variant by
the changed variable and retain enough provenance to compare it fairly.

## Compositing and cutouts

For composites, plan the layer order and match the inserted element's scale,
viewpoint, perspective, occlusion, light direction, colour temperature, contrast,
sharpness, and texture. A technically clean cutout that belongs to the wrong
depth plane is a failed composite.

For cutouts, require a real alpha channel or the selected capability's documented
transparency behaviour. Inspect hair, fine edges, semi-transparent material,
contact shadows, and the intended matte colour. A checkerboard preview is not
transparency evidence.

## Conversion

Conversion may change encoding, dimensions, or colour profile, but it must not
silently crop, sharpen, recolour, or redraw. Compare pixel dimensions, aspect,
alpha, and a visual sample. If the converter applies a creative transform, treat
it as an edit and re-open the invariant ledger.
