# Repo Doctrine Guide

This guide contains the worker procedures and reference pointers that were previously in the root `AGENTS.md` and `tools/AGENTS.md` (now `.devin/rules/tools.md`). It is a guide, not operative law; the root `AGENTS.md` and `.agents/docs/mesh-policy.md` remain the rule surfaces.

## Testing instructions

This repo uses test-driven development. See `.agents/guides/testing-guide.md` and invoke `/test-driven-development` before writing implementation code.

## Code style guidelines

Skill and marketplace shape standards are in `docs/skill-standards-policy.md`.
General code style and writing conventions are in `.agents/guides/code-style-guide.md`.

## Review guidelines

For Devin Review and the full review methodology, see `REVIEW.md` and `.agents/guides/code-review-guide.md`.

## PR instructions

PRs must include publication proof per the root `AGENTS.md` "Publication proof for repo work" section.
For the PR workflow, see `.agents/guides/pr-guide.md`.
For what reviewers check, see `.agents/guides/code-review-guide.md`.

## Contributing

For the implementation and contribution workflow, see `CONTRIBUTING.md`.

## Build and test commands

Canonical validation and regeneration commands are `py -3 tools/run.py ci --check` and `py -3 tools/run.py marketplace --apply`.
For the full `tools/run` target matrix and the implementation verification workflow, see `.agents/guides/implementing-guide.md`.
