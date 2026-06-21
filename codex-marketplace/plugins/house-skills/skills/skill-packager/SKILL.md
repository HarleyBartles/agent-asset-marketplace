---
name: skill-packager
description: Package, validate, inspect, and repair installable ChatGPT skill bundles. Use after skill creation or validation when a complete skill folder must become a skill.zip, when package identity or loader safety must be checked, when package evidence receipts are needed, when a timeout or failed install card occurs, or when agents need the canonical no-improvisation packaging command.
metadata:
  source-id: skill-packager
  source-path: sources/first_party/skills/skill-packager/SKILL.md
  provenance-name: MARK-21 skill maintenance House Skills source slice
license: "MIT"
---
# Skill Packager

Use this skill to package, validate, inspect, and repair ChatGPT skill bundles.

This skill owns archive shape, loader safety, package evidence, exact file identity, and the canonical packaging command. It does not design skill content, judge semantic quality, control queue cadence, or decide batch handoff presentation.

Package evidence proves that an archive was built and verified from a stated source path. It does not prove that the source contains the intended skill update, that the issue goal is satisfied, or that the package remains presentation-safe after a handoff lifecycle break. Those are validation and queue-handoff concerns.

## Progressive reference triggers

- Read `references/skill-update-stack-contract.md` before packaging, package repair, or handoff.
- Read `references/package-validation-contract.md` before normal packaging, timeout diagnosis, package identity checks, script architecture lint results, or failed handoff repair.
- Read `references/frontmatter-loader-discipline.md` when repairing loader failures, auditing frontmatter, or preparing existing-skill updates.
- Read `references/batch-packaging-workflow.md` when preparing more than one package or operating under `skill-handoff` batch mode.
- Read `references/source-and-evidence-posture.md` only when packaging work depends on repository evidence, connector availability, source-route claims, external package evidence, or a failed source route.

## Stack-order contract

Do not package update work unless there is a structured validator `pass` object for the same skill name and staged source path. Prose claims such as `validator passed`, checklist summaries, or ledger fields without the required object are not enough.

Before packaging, confirm the validator object includes `target_skill`, `staged_source_path`, `reviewed_skill_creator_contract: true`, `reviewed_skill_quality_gate: true`, `decision: pass`, `handoff_allowed: true`, and `next_required_step: skill-packager`. If any field is absent or mismatched, stop with `hard_red_stack_incomplete`.

## Normal execution command

For ordinary packaging, run the wrapper. Do not hand-run the internal scripts or build an equivalent script unless debugging a wrapper failure.

```bash
python /home/oai/skills/skill-packager/scripts/package_and_verify_skill.py <skill-folder> <external-dist-dir>
```

The wrapper runs frontmatter lint, editor-stability lint, quick validation, package creation, zip integrity, archive inspection, evidence reread, exact stat, and SHA-256 verification in one integrated single-target process. It writes `package-run-receipt.json` and `package-evidence.json` beside the external `skill.zip`, including `current_step` while a step is active and total elapsed timing on success.

If a substep times out or the wrapper budget is exceeded, the wrapper reports the active step and leaves a failure receipt when possible. Treat that receipt as diagnostic evidence, not handoff evidence. Reduce the preparation window, retry the same item in isolation, and repair the named step or source tree if it repeats; do not improvise a parallel packaging path.

## Handoff lifecycle scope

Package evidence proves archive identity at packaging time. It does not by itself prove that an archive remains lawful to present after a skill-handoff handoff lifecycle has been broken.

`skill-handoff` owns queue state, handoff cadence, cursor-driver behavior, and whether a prepared package is still presentation-safe. This skill supplies identity facts: intended skill, staged source path, exact package path, top-level folder, frontmatter name, exact filename, final SHA-256, archive inspection result, external dist directory, and stale dist reuse check.

Do not let this skill forbid or require cursor-advance pulses. An inert cursor-advance pulse is not package evidence and does not change package validity. A package link still must be emitted through the skill-handoff-controlled assistant-message handoff surface.

## Broken installer card hard stop

A package handoff is invalid unless the exact linked archive is named `skill.zip`, exists at the exact linked path, has nonzero size, and has passed checks on that exact path. A handoff also requires matching machine-written evidence; assistant-authored ledger text is not evidence.

Never hand off a sandbox link, markdown link, or package path from memory, planned output, expected output, prior logs, or a manually typed ledger. Immediately before writing the user-facing link, verify that the file name is exactly `skill.zip`, the file exists, has nonzero size, and is the same archive that passed wrapper verification.

## Batch preparation

When used under `skill-handoff`, run the wrapper once per skill into an external, target-specific dist directory. Batch work is repeated single-target preparation, not one multi-skill packaging operation. Mark a package prepared only after the wrapper returns success and the receipt/evidence match the exact archive. If package preparation is slow or times out, reduce the preparation window and retry the same item in isolation rather than bypassing the wrapper or overloading the batch.

After package identity facts are returned to `skill-handoff`, this skill is no longer in control of handoff cadence. Re-enter this skill only for a concrete package failure.

## Script boundaries

The bundled scripts are executable implementation. For normal execution, do not read them. Use the wrapper command above and the package validation contract. Inspect individual scripts only after wrapper failure, timeout diagnosis, package validation, or explicit script editing.

Bundled scripts:

- `scripts/package_and_verify_skill.py` is the canonical normal packaging wrapper. It is single-target and integrated to avoid duplicate subprocess/lint work.
- `scripts/frontmatter_lint.py`, `scripts/editor_stability_lint.py`, `scripts/quick_validate.py`, `scripts/package_skill.py`, and `scripts/inspect_skill_zip.py` are wrapper substeps and targeted-debug tools.
- `scripts/safe_skill_tree.py` provides bounded traversal and skip rules for the packaging scripts.
- `scripts/init_skill.py` initializes a normal skill folder when needed.

