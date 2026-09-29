# Marketplace Distribution

This agent-facing reference covers how to build and consume the marketplace products. Canonical skills live under `skills/`, reusable resources under `shared/`, product membership under `src/plugin-definitions/`, Python package source under `src/packages/`, and assembly logic under `src/marketplace/`. The self-contained installable products are committed under `dist/plugins/`; wheels are under `dist/wheels/`.

Use `py -3 tools/run.py marketplace --apply` to build the packages and catalog, or `py -3 tools/run.py marketplace --check` to detect stale generated output. Build the Markdown formatting wheel with `py -3 src/packages/mdformat-safe-link-labels/build_wheel.py`.

The root `.agents/plugins/marketplace.json` is Codex's catalog entry point and points at products in `dist/plugins/`. This repository declares no skill subscriptions, so `.agents/skills/` is absent; runtime ambient plugin availability does not change repository policy.

Consumers pin marketplace source by immutable Git commit SHA in the `marketplace-source` submodule and in selected standard revisions. Plugin package versions are not source revisions. This repository does not publish semantic-version tags or GitHub Releases; use the merged source SHA reported for a completed release. For consumers migrating from copied ambient plugins or the retired index mesh, see the [consumer runner migration guide](../../skills/repo-shape/references/consumer-runner-migration.md).
