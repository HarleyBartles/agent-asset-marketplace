# MARK-239 Implementation Record

## Standard Applied

The MARK-237 standard for marketplace inventory normalization has three layers:

1. **Source custody**: Verbatim upstream snapshot in `sources/third_party/<name>/` or first-party source in `sources/first_party/`
2. **Codex projection layer**: Installable Codex plugin in `codex-marketplace/plugins/<name>/` with optional Codex-specific adaptations in `adapters/codex/<name>/`
3. **GPT export layer**: GPT-specific adaptations in `adapters/gpt/<name>/` controlled by `adapters/gpt/manifest.json` (direct/overlay/excluded per skill)

## Inventory Classification

### Fully Compliant (MARK-237 standard)
- **superpowers-plus**: Has SOURCE.md, PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries, source custody

### Normalized in this issue
- **superpowers-ecc**: Added PROJECTION.md, GPT manifest entries
- **everything-codex-code**: Added PROJECTION.md
- **codex-cortex**: Added PROJECTION.md
- **repo-worker-base**: Added PROJECTION.md
- **dotnet-kit**: Added PROJECTION.md
- **api-contracts-pack**: Added PROJECTION.md
- **architecture-pack**: Added PROJECTION.md
- **language-patterns-pack**: Added PROJECTION.md
- **security-pack**: Added PROJECTION.md
- **frontend-pack**: Added PROJECTION.md

### Already had PROJECTION.md (no changes needed)
- **wild-bunch-project-pack**: Already had PROJECTION.md, GPT manifest added via default export mode

### First-party projections (different pattern, direct export appropriate)
- **house-skills**: First-party source custody, direct GPT export appropriate
- **adventures-pack**: First-party source custody, direct GPT export appropriate
- **unslop**: Adapted third-party custody, direct GPT export appropriate
- **game-studio**: Imported third-party custody, direct GPT export appropriate

## Active Adapted Third-Party Projections

The following plugins have active adapted third-party projections with overlay routes:

- **superpowers-plus**: Has Codex overlays in `adapters/codex/superpowers-plus/` and GPT overlays in `adapters/gpt/superpowers-plus/`

## Distinguishing Tests, Validators, Generators, and Generated Outputs

- **Tests**: `tests/` directory contains test scripts
- **Validators**: `tools/validate_marketplace.py` and related validation scripts
- **Generators**: `tools/skill_packager.py`, `tools/skill_gpt_exports.py`, and related generation scripts
- **Generated outputs**: `generated/skill-zips/` contains derived skill zip artifacts that should not be hand-edited

## Validation Results

Marketplace validation passed successfully after normalization. All plugin roots, manifests, skill paths, and source custody surfaces validated correctly. No validation issues were found.

## Follow-up Issues

None required. All marketplace plugins now have clear SOURCE.md and PROJECTION.md documentation, and the GPT manifest controls export behavior for all plugins.

## Publication Proof

PR URL: https://github.com/HarleyBartles/agent-asset-marketplace/pull/139
Head SHA: 89d0fc80f21f47e5fe75f57c88bb5f7cbb20d084
