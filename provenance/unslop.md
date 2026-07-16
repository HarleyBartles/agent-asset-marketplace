# Unslop Provenance

## Summary

MARK-99 adds an Asset Marketplace-owned `unslop` GPT/Codex package at `codex-marketplace/plugins/unslop/`.

The package adapts the upstream idea of sampling outputs, detecting repetitive AI defaults, and producing a reusable anti-slop profile. Runtime execution is self-contained in bundled Python scripts and uses local samples rather than fetching source code or depending on a provider-specific CLI.

## Upstream Evidence

- **Upstream repo**: `mshumer/unslop`
- **Pinned commit**: `edcb62386d129c65e4395f0cfcc9168eb1ba2148`
- **License**: MIT
- **Source custody**: `sources/third_party/unslop/upstream/`
- **Marketplace package**: `codex-marketplace/plugins/unslop/`

## Adaptation Notes

- **GPT skill install path**: `codex-marketplace/plugins/unslop/skills/unslop/`
- **Codex plugin install path**: `codex-marketplace/plugins/unslop/.codex-plugin/plugin.json`
- **Text mode**: Uses Python standard library analysis over inline samples, fixture samples, or a sample directory
- **Visual mode**: Checks for Playwright and Chromium before attempting visual evidence; missing optional dependencies are recorded as skipped in the output manifest and validation report
- **Output contract**: Documented in `skills/unslop/references/output-contract.md`

## Marketplace Adaptation

- **Status**: `adapted`
- **Plugin name**: `unslop`
- **Display name**: `Unslop`
- **Marketplace category**: `Productivity`
- **Content mode**: Mixed `adapted` (main skill) and `verbatim` (profiles)
- **Adaptation note**: Reimplemented as an Asset Marketplace GPT/Codex skill with bundled Python scripts, local sample orchestration, output manifests, validators, and optional visual dependency smoke checks

## Rights and Attribution

- **Upstream source**: mshumer/unslop
- **License**: MIT
- **Redistribution rights**: Per MIT license terms
- **Modifications**: Asset Marketplace adaptation with self-contained Python runtime

## Validation Expectations

- **Package validator**: Checks required GPT skill files and rejects forbidden shipped runtime instructions
- **Output validator**: Checks `unslop-output/` for manifest, prompts, samples, counted analysis, draft profile strength, and visual evidence status
- **Repo marketplace validation**: Checks the plugin manifest, registry entry, source snapshot, and bundle manifest

## Notes

This is the standardized provenance file for the unslop plugin. The original Linear issue record is preserved at `provenance/MARK-99-unslop.md` for historical reference.