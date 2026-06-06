# Skill Validator v1

Use this skill to validate GPT-native House Skills before they are treated as ready for import, packaging, publication, or operational use.

This validator is an authority gate. Validator requirements are authoritative over creator output: if a creator, worker, or generator says a skill is done but this validator finds a mismatch, the validation result wins until the defect is corrected or explicitly routed.

## Validation posture

Validate the skill as source material, not as a sales pitch. Prefer boring, observable checks over intent claims.

Require these lanes:

1. `identity` — public name, version, source path, and intended scope are explicit and stable.
2. `trigger` — the skill says when to use it and when not to use it.
3. `authority` — the skill states what it can decide, what it cannot decide, and what upstream rules override it.
4. `workflow` — the reliable path is ordered, repeatable, and does not depend on hidden chat context.
5. `boundaries` — exclusions, protected surfaces, and escalation cases are explicit.
6. `evidence` — validation, publication, or handoff claims can be checked from files, commands, or durable records.
7. `residue` — packaging output, generated output, scratch files, and temporary handoffs are either absent or explicitly governed.

## Source checks

For every candidate skill, inspect the actual `SKILL.md` and any declared metadata or provenance. Do not rely only on summaries.

Check that the skill:

- has a single public identity and version;
- preserves issue-specific constraints and source-law constraints;
- does not import retired, reference-only, or system-built-in skills as new source assets;
- does not revive retired surfaces under a new label;
- does not broaden its scope beyond the issue or source slice being validated;
- does not claim packaging, publication, PR creation, or deployment without observable evidence;
- does not hide required validation behind optional prose.

## Creator-output override rule

Creator output is useful draft material, not the final authority. If creator output conflicts with validator requirements, preserve the validator requirement and require a correction.

Examples that must fail validation until corrected:

- a generated skill omits a required boundary because the creator template did not include it;
- a creator says a package is ready before repo validation has run;
- a worker imports an adjacent skill because the source bundle was nearby;
- a skill claims closure based on batch handoff status instead of durable repo evidence.

## Validation result states

Return one of:

- `PASS` — all required lanes are satisfied and evidence is durable.
- `AMBER` — usable with named risks, blockers, or missing external authority.
- `FAIL` — the skill contradicts requirements, lacks required lanes, broadens scope, or makes unverifiable closure claims.

## Return format

Report:

- skill path and public identity;
- source materials inspected;
- required lanes checked;
- defects found;
- validator-over-creator conflicts, if any;
- result state;
- exact follow-up required for AMBER or FAIL.
