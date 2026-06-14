# Source

This plugin adapts the upstream `mshumer/unslop` workflow into an Asset Marketplace-owned GPT/Codex package.

## Upstream Basis

- Repo: `mshumer/unslop`
- URL: <https://github.com/mshumer/unslop.git>
- Pinned commit: `edcb62386d129c65e4395f0cfcc9168eb1ba2148`
- License: `MIT`
- Source custody: `sources/third_party/unslop/upstream/`

## Marketplace Adaptation

- Reimplemented the useful empirical profile workflow for GPT/Codex orchestration.
- Replaced provider-specific subprocess generation with local sample-folder and inline-sample modes.
- Added deterministic prompt generation, counted text analysis, draft profile generation, output manifests, and validators.
- Added optional visual evidence smoke checks that skip cleanly when Playwright or Chromium is unavailable.
- Kept the upstream profiles as references and license evidence, while the runnable scripts are Asset Marketplace-owned adaptations.
- Traced the copied profile files in the bundle manifest so the market-facing package reflects every upstream-derived asset.

## Install Shape

- GPT skill package: `codex-marketplace/plugins/unslop/skills/unslop/`
- Codex plugin route: `codex-marketplace/plugins/unslop/.codex-plugin/plugin.json`
- Marketplace registry: `.agents/plugins/marketplace.json`
