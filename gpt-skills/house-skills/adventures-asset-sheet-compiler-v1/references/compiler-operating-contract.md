# Compiler Operating Contract

This reference preserves the detailed operating contract moved out of `SKILL.md` during progressive-discovery decomposition. Load it only when the compact control plane says the current request needs the full workflow.


# Adventures Asset Sheet Compiler

Use this skill for deterministic asset-sheet work only. It is the positive no-credit route after source images have been
accepted and Harley asks to compile, assemble, lay out, package, or place those images onto an approved asset-sheet
template.

This skill has two lanes:

1. Compile approved source images onto an already approved template.
2. Author or validate a new blank, reusable asset-sheet template package for later repo ingress.

Do not generate, regenerate, reinterpret, restyle, improve, or creatively edit source art. Treat approved images as
fixed inputs and use Pillow/PIL only for deterministic placement, cropping, annotation, or blank-template construction.

## Image-generation resource discipline

Image generation credits are scarce Adventures production capacity. Deterministic asset-sheet compilation exists to
preserve accepted source images without spending image-generation credits. Calling image generation during template
compilation defeats the purpose of the deterministic workflow and is a project-critical failure.

Classify every request before acting:

```yaml
operation_class:
  deterministic_no_credit:
    - compile accepted images onto a template
    - assemble an asset sheet
    - lay out source images in approved slots
    - package rendered sheet plus sources and manifest
    - inspect or QA the compiled sheet layout
    - author a blank reusable template package
  non_credit_pixel_work:
    - PIL contain-fit or cover-fit placement
    - deterministic crop, trim, callout, or annotation
    - deterministic template rendering
  credit_spending_mutation:
    - generate a new source image
    - regenerate a failed source image
    - generatively edit or restyle source art
```

This skill may only perform `deterministic_no_credit` and `non_credit_pixel_work`. If source art is missing, weak,
unaccepted, or needs visual repair, stop and route back to the owning image generation or QA workflow. Do not fill the
gap by calling image generation.

## Strong trigger examples

Use this skill for requests like:

- `Accepted. Proceed to compilation onto the template please.`
- `Compile the approved images onto the four-up template.`
- `Put these images on the canonical asset sheet.`
- `Assemble the source images into the template and package it.`
- `Create a reusable blank template package for this sheet shape.`

These are not image-generation requests. They are deterministic compile or template-authoring requests.

## Source route discipline

When template or asset availability depends on repo state, start from `assets/INDEX.md`, follow the template or asset
index mesh, and read the relevant repo JSON sidecar before acting. Use live GitHub API routes for exact file, issue,
commit, compare, and mutation checks. Use bound GitHub search only for broad stale-pattern sweeps when available.

For template work, repo and project sources are both required:

- The repo sidecar is the discovery and compile contract.
- The matching project-source PNG/spec package supplies the local template bytes for deterministic compile.
- If either side is missing, stale, or points to different filenames or geometry, stop and report the mismatch.

Do not use Slides, view surfaces, or session memory for template discovery or geometry.

## Lane A: compile an asset sheet

Use `scripts/compile_asset_sheet.py` as the default execution path. Do not hand-roll a fresh compiler unless the
bundled script cannot support the requested lane after a small manifest adjustment.

Workflow:

1. Read the repo template JSON sidecar for the selected template.
2. Confirm the matching project-source PNG/spec filenames named by the sidecar are available locally.
3. Confirm source images have been QA-accepted or explicitly scoped by Harley as accepted inputs.
4. List available source images in `/mnt/data` and map each to the intended sidecar slot id.
5. Create a JSON manifest following `references/manifest-schema.md`.
6. Run the compiler with the manifest.
7. Inspect the rendered PNG before responding.
8. Return links to the rendered PNG and the zip package.

Run with the container shell:

```bash
python /home/oai/skills/adventures-asset-sheet-compiler-v1/scripts/compile_asset_sheet.py /mnt/data/manifest.json
```

If the user asks for source-image repair, style changes, a new image, or regenerated pixels, do not compile over the
problem. Route back to image QA/preflight and wait for a separate current-turn image-generation authorization.

## Lane B: author a new template package

Use this lane when Harley asks to create a new blank asset-sheet template, create a template for a new sheet shape, or
prepare a template zip for Patch to ingest.

Read `references/template-package-authoring.md` before creating the package.

The required output package shape is:

```text
template_asset_sheet_<name>_vN.zip
  template_asset_sheet_<name>_vN.png
  template_asset_sheet_<name>_vN.json
  README.md
```

The JSON sidecar must already be repo-ready. Patch should verify and publish it, not reconstruct it. The sidecar must
name the exact package, PNG, and JSON filenames inside the zip. Do not use `_spec.json` unless the package really
contains a file with that exact name.

Before handing a template package to Harley or Patch, run:

```bash
python /home/oai/skills/adventures-asset-sheet-compiler-v1/scripts/validate_template_package.py /path/to/template.zip
```

A template package is not ready if validation fails.

## Template authoring anti-regression gates

For Lane B template packages, enforce these gates before handing off any zip:

- Keep templates generic and reusable. Do not create adventure-specific, issue-specific, deck-specific,
  character-specific, or one-scene templates when a neutral layout serves the same sheet shape.
- Do not bake explanatory copy, placeholder copy, template-use notes, adventure wording, process notes, issue titles,
  or slot meanings into the PNG. Stable sheet chrome such as `ASSET SHEET` is allowed when part of the family.
- Describe fillable title, subtitle, metadata, label, and guidance areas in `text_regions` in the JSON sidecar. Leave
  those regions blank in the PNG so the compiler can fill them for each asset sheet.
- Use neutral slot IDs and roles for reusable templates, such as `image_1`, `image_2`, `image_3`, `image_4`, unless
  the layout itself is inherently typed. Put adventure-specific meanings in the compile manifest, not the template.
- When revising a candidate template after visual feedback, increment the template id/version or write to a fresh output
  directory. Do not overwrite and relink a previous path if a stale preview or stale zip could survive.
- Before returning links, delete or avoid stale same-name outputs, open the exact PNG path that will be linked, and run
  the template package validator on the exact zip path that will be linked.

## Existing approved lanes

For current deterministic compiles, discover approved templates through the repo sidecars first. Older bundled lane
names remain supported for compatibility with existing manifests:

- `character-v4`: one main hero image, six alternate images, metadata, guidance, and optional captions.
- `three-hero-six-alt-v4`: three hero groups with two alternate images beneath each hero.
- `four-column-four-hero-eight-alt-v2`: four hero groups with two alternate images beneath each hero.

If a requested sheet shape does not match an indexed template, say that no approved template fits and create a new blank
template package first. Do not silently force the work into a recent or familiar template.

## QA checklist

Before final response for a compiled asset sheet, verify:

- The rendered asset sheet exists and opens.
- Every requested source image is copied into the output package under `sources/`.
- The zip package contains the rendered sheet, copied source images, manifest, and compile spec.
- Images are placed in the intended sidecar slots without distortion.
- Contain-fit was used by default unless the manifest or source role requires cover-fit.
- No source image was overwritten.
- No image generation was used.

Before final response for a new template package, verify:

- The zip has exactly one template PNG and one matching JSON sidecar.
- README.md is present when useful, but lack of README is not a blocker if the JSON is complete.
- The PNG canvas dimensions match `canvas.width` and `canvas.height`.
- The sidecar package, PNG, and JSON filename fields match the actual zip entries.
- Slot ids are unique and every slot rectangle is inside the canvas.
- Any `image_box` rectangles are inside their parent slot boxes and inside the canvas.
- `compile_rules.read_sidecar_before_compile`, `use_matching_project_source_png`, and
  `use_matching_project_source_spec` are true.
- The validator script passes.

## Failure behavior

If a required source image, repo sidecar, project-source template PNG/spec, or template package field is missing, stop
and report the missing item exactly. Do not substitute another template, generated image, or memory-derived geometry.
If a new template geometry is needed, create the template PNG and JSON sidecar package first, validate it, then proceed.

If the latest user turn asks for new or changed generated pixels, stop this skill and route to `adventures-visual-intent-gate` and
`adventures-image-preflight`. Treat `adventures-visual-intent-gate` as the locked Adventures image-credit safety gate; this compiler remains deterministic and must not spend image credits. If the latest user turn asks for QA of a candidate or compiled sheet, route to
`adventures-image-qa-v1` for the decision and return here only after accepted source images or a compiled-sheet
task exists.
