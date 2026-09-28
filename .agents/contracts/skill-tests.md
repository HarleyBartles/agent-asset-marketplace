# Skill Tests Contract

This contract defines custody and invocation for test material owned by an installable marketplace skill.

## Governing rule

Skill source includes executable code, instructions, and its tests under `skills/<skill-id>/tests/`. The builder copies skill tests, including pressure cases, into every plugin that carries the skill. Material under `tests/evaluator-only/`, cached Python files, and pressure run results are source or transient evaluation material and do not ship. Repository, build, and shipped-plugin suites live under `tests/repository/`, `tests/build/`, and `tests/shipping/`; only those suites run in the commit and PR gate. Evaluation-harness tests live under `tests/evaluation-harness/` and run when that harness changes. Run skill tests explicitly for the changed skill.

## Location and contents

Keep skill-owned maintainer verification under `skills/<skill-id>/tests/`. Put helper-script unit tests in `tests/scripts/`, instruction behavior cases in `tests/behavior/`, and pressure prompts and reusable fixtures in `tests/pressure/`. Use a more specific name, such as `tests/profiles/`, when the skill owns another kind of durable test data.

Do not put run-specific transcripts, scores, verdicts, generated repositories, or other execution output in the skill. Keep those results transient and off-repo.

A skill without useful test material need not contain an empty `tests/` directory. Do not invent low-value tests merely to satisfy the convention.

## Distribution and invocation

Marketplace generation and installed-skill refresh leave canonical `tests/` unchanged. The builder copies ship-ready tests into every included skill. Put blinded judge material in `tests/evaluator-only/`; the builder excludes that directory, Python caches, and transient `runs/` directories. Invoke script tests against canonical source helpers. Evaluate instruction behavior in fresh contexts using the skill's pressure cases.

Installed `tests/` is for maintainers, not part of ordinary skill invocation. A blinded worker may read `SKILL.md` and ordinary behavioral resources, but must not receive judge-only rubrics, expected results, or prior run output. Keep evaluator-only material outside the built package and restrict worker reads during the evaluation.

## Directory boundaries

- `assets/` contains templates, authority evidence, and other resources used during ordinary skill execution.
- `references/` contains behavioral knowledge loaded on demand.
- `scripts/` contains runtime capability code.
- `tests/scripts/` verifies executable skill helpers.
- `tests/behavior/` holds durable instruction behavior cases.
- `tests/pressure/` holds reusable pressure prompts and fixtures that ship with the skill.
- `tests/evaluator-only/` holds judge-only material that stays in source.

Repository-root `tests/evaluation-harness/` owns shared runner checks. It does not duplicate a skill's portable prompts or fixtures as a second source of truth.
