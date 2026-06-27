---
name: adventures-asset-sheet-compiler
description: Use when compile Adventures asset sheets through deterministic no-credit
  template work. Use when Harley asks to compile, assemble, lay out, inspect, package,
  or QA externally accepted source images on an approved template, or to author a
  blank reusable asset-sheet template package using bundled PIL tooling. Do not treat
  PIG self-QA as acceptance.
metadata:
  source-id: adventures-asset-sheet-compiler
  source-path: sources/first_party/skills/adventures-asset-sheet-compiler/SKILL.md
  provenance-name: Adventures Asset Sheet Compiler first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when compile Adventures asset sheets through deterministic no-credit
    template work. Use when Harley asks to compile, assemble, lay out, inspect, package,
    or QA externally accepted source images on an approved template, or to author
    a blank reusable asset-sheet template package using bundled PIL tooling. Do not
    treat PIG self-QA as acceptance.
  use_when:
  - Use when compile Adventures asset sheets through deterministic no-credit template
    work. Use when Harley asks to compile, assemble, lay out, inspect, package, or
    QA externally accepted source images on an approved template, or to author a blank
    reusable asset-sheet template package using bundled PIL tooling. Do not treat
    PIG self-QA as acceptance.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
  projection_targets:
  - codex-marketplace/plugins/adventures-pack/skills/adventures-asset-sheet-compiler
  - codex-marketplace/plugins/house-skills/skills/adventures-asset-sheet-compiler
license: MIT
---

# Adventures Asset Sheet Compiler

Use this skill for deterministic Adventures asset-sheet work: compiling accepted source images onto an approved template, inspecting compiled layout, packaging rendered sheets, or authoring reusable blank template packages.

## Owned decision

Decide whether the request is a deterministic compile, blank-template authoring task, compiled-sheet QA handoff, or blocked because source images/templates are missing or unaccepted.

## Hard boundaries

Do not generate, regenerate, restyle, or creatively edit source art. This skill may use only deterministic no-credit work and non-credit pixel operations such as PIL placement, crop, trim, annotation, or template rendering. If source art needs repair or new pixels, route to image QA/preflight and stop.

PIG output is candidate production art until external Adventures/GPT/Harley acceptance says otherwise. Do not compile a PIG candidate or PIG self-QA pass into an asset sheet as accepted source art. Use only images whose acceptance/source status is explicit for the target sheet, or return a blocker identifying the missing external acceptance evidence.

## Progressive references

Read `references/compiler-operating-contract.md` when compiling sheets, authoring templates, checking template sidecars, running bundled commands, packaging outputs, or diagnosing failures.

Read `references/manifest-schema.md` when creating or validating a compile manifest.

Read `references/template-package-authoring.md` when creating or validating a reusable blank template package.

For normal deterministic execution, do not read scripts. Use the command recipes in `references/compiler-operating-contract.md`; inspect scripts only after execution failure, package validation, or explicit script editing.

## Minimal workflow

1. Classify Lane A compile vs Lane B template authoring vs blocked/reroute.
2. Verify accepted source images and matching repo/project-source template inputs.
3. Create or validate the required manifest or template package.
4. Run the deterministic bundled command.
5. Inspect exact outputs and return rendered/package links.
