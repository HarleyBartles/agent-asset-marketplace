# Template package authoring contract

Use this reference when creating a new blank asset-sheet template package for Adventures of Patch.

## Purpose

GPT must produce template packages that are ready for Patch to verify and ingest. Patch should not have to re-author the
sidecar, infer the layout, rename project-source files, or reconstruct slot geometry from a PNG.

## Required package shape

The package filename, PNG filename, and JSON filename must share the same template id stem.

```text
template_asset_sheet_<name>_vN.zip
  template_asset_sheet_<name>_vN.png
  template_asset_sheet_<name>_vN.json
  README.md  # optional but recommended
```

Do not use `_spec.json` unless the actual project-source package uses that exact filename. The current project-source
contract uses `<template_id>.json`.

## Required sidecar fields

The sidecar must include these fields:

```json
{
  "template_id": "template_asset_sheet_<name>_vN",
  "template_name": "template_asset_sheet_<name>_vN",
  "version": "vN",
  "status": "candidate",
  "png_filename": "template_asset_sheet_<name>_vN.png",
  "project_source_package_filename": "template_asset_sheet_<name>_vN.zip",
  "project_source_png_filename": "template_asset_sheet_<name>_vN.png",
  "project_source_spec_filename": "template_asset_sheet_<name>_vN.json",
  "canvas": {"width": 1536, "height": 1008},
  "layout_type": "short_machine_readable_layout_type",
  "supported_layout": "short human-readable use case",
  "text_regions": [],
  "slots": [],
  "compile_rules": {
    "read_sidecar_before_compile": true,
    "use_matching_project_source_png": true,
    "use_matching_project_source_spec": true,
    "do_not_infer_slots_from_recent_session_memory": true,
    "do_not_infer_geometry_from_filename": true
  },
  "consistency_checks": []
}
```

If the template has known non-image title, notes, guidance, or label areas, list them under `text_regions`. If the
areas are decorative only, leave `text_regions` empty rather than inventing editable text fields.


## Reusable-template neutrality and baked-text policy

Blank templates are reusable layout contracts. They must not encode a specific adventure, issue, deck, character, scene,
or one-off use case unless Harley explicitly asks for a non-reusable special-purpose template. Prefer generic names and
neutral geometry for reusable shapes, for example `template_asset_sheet_4up_equal_header_v2` rather than
`template_asset_sheet_dugout_4view_v1`.

Do not bake explanatory wording into the PNG. Avoid text such as `generic four-up template`, `slot meanings are supplied
by the manifest`, `four equal image views`, adventure titles, panel purposes, issue numbers, process notes, or future
compiler instructions. Those are sidecar or README facts, not template pixels.

The only normal baked wording allowed in a blank asset-sheet template is stable sheet chrome that should remain present
on every compiled sheet, such as the approved `ASSET SHEET` header. Title, subtitle, metadata, labels, guidance, and
caption areas should be blank visual regions in the PNG and described under `text_regions` so compilers can fill them
per output.

For a reusable four-up template, use neutral slot names such as `image_1`, `image_2`, `image_3`, and `image_4`. The
compile manifest supplies context-specific meanings like `establishing_view`, `interaction_view`, or `outcome_artifact`.
Do not bake those meanings into the template id, slot names, or visible text unless the template is explicitly approved
as a special-purpose one-off.

## Version and stale-output discipline

When revising a template after user feedback, do not overwrite and relink the previous package path if there is any
risk that ChatGPT, the UI, or the filesystem will serve a stale preview. Use one of these safe paths:

- increment the template id/version, usually the minor version suffix, and produce a new package stem; or
- write to a fresh output directory and verify the exact linked files.

Before responding, remove or avoid stale same-name copies, open the exact PNG path that will be linked, and validate the
exact zip path that will be linked. If the preview still shows the old image, stop and fix the output path instead of
claiming the package is corrected.

## Slot rules

Each slot object must include:

```json
{
  "slot_id": "hero",
  "box": [x0, y0, x1, y1],
  "default_fit": "cover",
  "role": "hero",
  "group": "main"
}
```

Use integer pixel coordinates. Coordinates are left, top, right, bottom. The right and bottom values must be greater
than the left and top values. Every rectangle must fit inside the canvas.

If a template has a decorative frame and an inner image placement area, include both:

```json
{
  "slot_id": "hero",
  "box": [54, 205, 1482, 575],
  "image_box": [70, 221, 1466, 559],
  "default_fit": "cover",
  "role": "hero",
  "group": "main"
}
```

The `image_box` must fit inside the parent `box`.

## Naming and status

Use `status: candidate` for a new template package that has not been ingested into the repo. Patch may promote the
status to `approved` during repo publication if the package is accepted.

Do not include stale ingress paths in a newly authored package. Patch may add `source_ingress_package` during ingress,
but GPT-authored project-source packages should point to their own zip, PNG, and JSON filenames.

## README guidance

`README.md` is recommended for human legibility, but the JSON sidecar is the binding contract. If included, README.md
should state:

- the template id;
- intended layout and sheet use;
- package contents;
- that the JSON sidecar is the compile contract;
- that deterministic compilers should read the sidecar before using the PNG;
- that Patch should verify geometry before repo publication.

## Validation before handoff

Run `scripts/validate_template_package.py` on the zip. The package is not ready for Patch ingress until the validator
passes. If the validator fails, repair the package rather than asking Patch to fix it during ingress.
