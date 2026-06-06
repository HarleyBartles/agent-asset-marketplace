# Skill Packager v1

Use this skill to prepare a GPT-native skill for packaging or downstream export after the source skill has passed validation.

Packaging is downstream from validation. Always validate before packaging. Do not use packaging to bypass validator defects, scope problems, provenance gaps, or missing source review.

## Non-goals

This skill does not perform repo-import ZIP packaging. Do not add ChatGPT skill ZIPs, package archives, generated bundles, or deployment artifacts to the source repo as part of an import unless the issue explicitly asks for committed generated output.

This skill does not replace source review, provenance review, marketplace validation, or PR evidence.

## Packaging gate

Before packaging, require:

1. the source `SKILL.md` exists in the intended source path;
2. skill validation has passed or any AMBER state is explicitly accepted by the owning authority;
3. provenance and intake records are current when the repo tracks them;
4. no retired, reference-only, or adjacent skills were imported as packaging collateral;
5. generated output destinations are downstream or temporary, not mistaken for source of truth.

If any gate fails, stop packaging and return the blocker.

## Packaging posture

Package the smallest intended skill surface. Keep source identity stable and avoid adding compatibility wrappers, duplicate entrypoints, or invented metadata.

Do not include:

- unrelated House Skills;
- local caches, scratch files, test output, or previous ZIPs;
- repo-only provenance unless the package format explicitly requires it;
- plugin projections or marketplace replacements unless separately authorized.

## Repo-import boundary

For source imports, the correct outcome is usually committed source files plus validation evidence, not a ZIP. If the task is an import into this repository, keep packaging output out of the repo and report that no repo-import ZIP packaging was performed.

## Return format

Report:

- source skill path;
- validation evidence used;
- package destination or explicit no-package decision;
- files included or excluded;
- generated residue created and cleaned;
- blockers, if packaging did not proceed.
