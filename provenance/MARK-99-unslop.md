# MARK-99 Unslop Vendor Record

## Summary

MARK-99 adds an Asset Marketplace-owned `unslop` GPT/Codex package at `codex-marketplace/plugins/unslop/`.

The package adapts the upstream idea of sampling outputs, detecting repetitive AI defaults, and producing a reusable anti-slop profile. Runtime execution is self-contained in bundled Python scripts and uses local samples rather than fetching source code or depending on a provider-specific CLI.

## Upstream Evidence

- Upstream repo: `mshumer/unslop`
- Pinned commit: `edcb62386d129c65e4395f0cfcc9168eb1ba2148`
- License: MIT
- Source custody: `sources/third_party/unslop/upstream/`
- Marketplace package: `codex-marketplace/plugins/unslop/`

## Adaptation Notes

- GPT skill install path: `codex-marketplace/plugins/unslop/skills/unslop/`
- Codex plugin install path: `codex-marketplace/plugins/unslop/.codex-plugin/plugin.json`
- Text mode uses Python standard library analysis over inline samples, fixture samples, or a sample directory.
- Visual mode checks for Playwright and Chromium before attempting visual evidence; missing optional dependencies are recorded as skipped in the output manifest and validation report.
- Output contract is documented in `skills/unslop/references/output-contract.md`.

## Validation Expectations

- Package validator checks required GPT skill files and rejects forbidden shipped runtime instructions.
- Output validator checks `unslop-output/` for manifest, prompts, samples, counted analysis, draft profile strength, and visual evidence status.
- Repo marketplace validation checks the plugin manifest, registry entry, source snapshot, and bundle manifest.
