# ADR 0004: Skill source and plugin build

**Status:** Accepted

## Context

Plugin-owned source prevented one skill or shared reference from being reused cleanly across installable plugins. A single repository `tests/` collection also mixed repository checks, skill scripts, and pressure evaluations into the commit gate.

## Decision

Canonical first-party maintained skills live under `skills/`. Shared authored resources live under `shared/`. `src/plugin-definitions/` declares plugin identity, composition, provenance, and static package files. A deterministic build assembles complete plugin packages under `dist/plugins/`; those packages are committed for marketplace consumers. Plugins carry skills but do not own their source.

Each skill owns its executable tests and pressure cases under its source `tests/` directory. The build carries ship-ready tests with each installed skill and excludes evaluator-only material, caches, and run results. The commit and PR gate runs separate repository, build, and shipped-package suites under the root `tests/` directory. Skill tests and evaluation-harness tests run when their owner changes.

## Consequences

One source skill can be included in multiple plugins. Shared references are copied into each built skill that declares them. Source edits require a build and freshness check. Attribution and license terms travel with every built copy. Test ownership determines when a suite runs; the default gate does not collect every skill evaluation.

## Current authority

Root `AGENTS.md`, `.agents/contracts/skill-tests.md`, and `.agents/doctrine/custody-and-marketplace-doctrine.md`.
