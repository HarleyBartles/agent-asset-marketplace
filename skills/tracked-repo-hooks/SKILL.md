---
name: tracked-repo-hooks
description: Use when changing or assessing a repository's tracked pre-commit hook and hosted-CI parity under its adopted standard.
metadata:
  source-id: tracked-repo-hooks
  source-path: skills/tracked-repo-hooks/SKILL.md
  provenance-name: Tracked Repo Hooks first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
license: MIT
---

# Tracked Repo Hooks

For explicit adoption or assessment, inspect the repository's pinned subscription and certification through `repo-standards`, then follow the [tracked hook and CI definition](references/standard.md). Ambient availability does not adopt the standard.

The pledge is one complete gate on Windows before commit and Linux in hosted CI. The checks are the same in both places: tests, lint, build, and other configured CI gates do not move exclusively to paid hosted CI or exclusively to a developer hook. The tracked hook must be maintained, hook skipping is prohibited for agents, and hosted CI runs the equivalent gate against the proposed commit.

Preserve repository content across platforms. Normalize line endings and file endings so Windows authoring and Linux hosted execution do not create avoidable churn. Validate the candidate commit state and report failures clearly. A repository chooses the hook implementation and its commands; use the command bus only when that standard is also adopted, and make hook integration an explicit bus target/module deployment into the repository-owned bus.

The optional starter hook is a deployable seed. A repository may adapt it or implement another approach that meets the pinned invariants. V1 consumers continue to follow their pinned definition, including any historical command contract, until an explicit upgrade.
