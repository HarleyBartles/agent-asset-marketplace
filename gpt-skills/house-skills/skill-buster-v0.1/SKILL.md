# Skill Buster v0.1

Use this skill to break down, verify, and close skill-maintenance work without allowing broad adjacent imports or unreliable batch handoff to masquerade as completion.

This skill remains v0.1. Treat it as a boring operational posture, not a mature automation framework.

## Reliable boring path

One-at-a-time is the reliable boring path. When a source slice contains multiple skills, handle each skill as a separate observable unit:

1. identify the exact source skill and allowed path;
2. import or update only that unit;
3. validate the unit against its rules and repo rules;
4. record provenance and intake changes required for that unit;
5. check for residue and adjacent-scope drift;
6. then move to the next unit.

Do not call the batch complete until every unit has durable file and validation evidence.

## Batch handoff warning

Batch handoff is unreliable and non-closure-critical. It may help organize work, but it is not proof of completion. Closure depends on repo-visible source files, validation output, commit evidence, and publication or PR evidence when required.

If a batch handoff summary conflicts with observed repo state, observed repo state wins.

## Scope guard

For issue-backed skill maintenance, preserve the issue boundary. Do not import nearby skills, retired skills, reference-only skills, plugin projections, packaging artifacts, or unrelated overlays merely because they appear in the same workspace or source bundle.

When a task names include-only paths, treat those paths as the ceiling unless the owner explicitly expands scope.

## Buster checks

Run these checks before declaring closure:

- changed files match the allowed slice;
- source identities and versions match the issue;
- validation-before-packaging rules were honored;
- no repo-import ZIP packaging was added unless explicitly required;
- retired or reference-only skills were not imported;
- batch notes are not used as the sole proof;
- residue and TODOs are named.

## Return format

Report:

- issue or source slice reviewed;
- units handled one at a time;
- changed files;
- validation commands and results;
- batch handoff caveats;
- out-of-scope material intentionally left untouched;
- final closure state: `PASS`, `AMBER`, or `FAIL`.
