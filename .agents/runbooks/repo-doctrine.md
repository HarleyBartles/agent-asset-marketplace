# Repo Doctrine Runbook

This runbook contains the worker procedures and reference pointers that were previously in the root `AGENTS.md` and `tools/AGENTS.md` (now `.devin/rules/tools.md`). It is a runbook, not operative law; the root `AGENTS.md` and `.agents/docs/mesh-policy.md` remain the rule surfaces.

## Testing instructions

This repo uses test-driven development. See `.agents/runbooks/testing.md` and invoke `/test-driven-development` before writing implementation code.

## Code style guidelines

Skill and marketplace shape standards are in `docs/skill-standards-policy.md`.
General code style and writing conventions are in `.agents/runbooks/code-style.md`.

## Review guidelines

For Devin Review and the full review methodology, see `REVIEW.md` and `.agents/runbooks/code-review.md`.

## PR instructions

PRs must include publication proof per the root `AGENTS.md` "Publication proof for repo work" section.
For the PR workflow, see `.agents/runbooks/pr.md`.
For what reviewers check, see `.agents/runbooks/code-review.md`.

## Contributing

For the implementation and contribution workflow, see `CONTRIBUTING.md`.

## Build and test commands

Canonical validation and regeneration commands are `py -3 tools/run.py ci --check` and `py -3 tools/run.py marketplace --apply`.
For the full `tools/run` target matrix and the implementation verification workflow, see `.agents/runbooks/implementing.md`.
