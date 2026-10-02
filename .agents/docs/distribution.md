# Marketplace Distribution

This agent-facing reference covers how to build and consume the marketplace products. Canonical skills live under `skills/`, reusable resources under `shared/`, product membership under `src/plugin-definitions/`, Python package source under `src/packages/`, and assembly logic under `src/marketplace/`. The self-contained installable products are committed under `dist/plugins/`; wheels are under `dist/wheels/`.

Use `py -3 tools/run.py marketplace --apply` to build the packages and catalog, or `py -3 tools/run.py marketplace --check` to detect stale generated output.

The root `.agents/plugins/marketplace.json` is Codex's catalog entry point and points at products in `dist/plugins/`. This repository declares no skill subscriptions, so `.agents/skills/` is absent; runtime ambient plugin availability does not change repository policy.

Codex consumers subscribe to plugins through repo-native Git sources. Marketplace plugin declarations track the published `main` branch by default, and Codex's Marketplace Upgrade action refreshes the marketplace snapshot and installed plugin payload. Consumers do not need a Marketplace source submodule to install plugins. Selected deployable standards may record the source revision used to scaffold their repo-owned implementation. Plugin package versions are not source revisions; this repository does not publish semantic-version tags or GitHub Releases.

For consumer plugin installation, adopt the [repo plugin subscriptions standard](../../skills/repo-agent-assets/references/standard.md).
