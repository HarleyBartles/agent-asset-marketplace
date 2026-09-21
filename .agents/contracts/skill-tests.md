# Skill Tests Contract

This contract defines custody and distribution for test material owned by an installable marketplace skill.

## Governing rule

Skills are code, and code ships with its tests. Skill-owned tests therefore ship in the canonical skill directory and every installed projection. Code does not ship test results, and skills do not ship test results.

## Location and contents

Keep skill-owned maintainer verification under `<skill>/tests/`. The directory may contain automated checks, evaluation scenarios, complete lightweight fixture trees, materialization helpers, rubrics, and stable expected results.

Do not put run-specific transcripts, scores, verdicts, generated repositories, or other execution output in the skill. Keep those results transient and off-repo.

A skill without useful test material need not contain an empty `tests/` directory. Do not invent low-value tests merely to satisfy the convention.

## Distribution and invocation

Marketplace generation and installed-skill refresh must preserve the complete `tests/` tree byte-for-byte. The directory ships so maintainers can verify the skill in the environment where it is installed.

`tests/` is not part of the skill's behavioral interface. Ordinary skill invocation must neither require nor direct an agent to load it. In a blinded behavioral evaluation, the worker may read `SKILL.md` and ordinary behavioral resources, but must not receive hidden rubrics, expected results, or prior run output. Evaluators and materializers may read the test package.

## Directory boundaries

- `assets/` contains templates, authority evidence, and other resources used during ordinary skill execution.
- `references/` contains behavioral knowledge loaded on demand.
- `scripts/` contains runtime capability code.
- `tests/` verifies the skill itself and ships with it for maintainers.

Repository-root test directories may own shared orchestration and generic campaign checks. They must not duplicate a skill's portable prompts, fixtures, rubrics, or deterministic assertions as a second source of truth.
