# Marketplace Inventory Classification

## MARK-237 Standard

The standard established in MARK-237 for Superpowers+ has three layers:

1. **Source custody**: Verbatim upstream snapshot in `sources/third_party/<name>/` or first-party source in `sources/first_party/`
2. **Codex projection layer**: Installable Codex plugin in `codex-marketplace/plugins/<name>/` with optional Codex-specific adaptations in `adapters/codex/<name>/`
3. **GPT export layer**: GPT-specific adaptations in `adapters/gpt/<name>/` controlled by `adapters/gpt/manifest.json` (direct/overlay/excluded per skill)

## Plugin Classification (Final State After MARK-239)

### Fully Compliant (MARK-237 standard with overlays)
- **superpowers-plus**: Has SOURCE.md, PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries, source custody

### Compliant with PROJECTION.md and GPT manifest (no overlays needed)
- **superpowers-ecc**: Has SOURCE.md, PROJECTION.md, GPT manifest entries, source custody. No Codex/GPT overlays needed (direct export appropriate)
- **everything-codex-code**: Has SOURCE.md, PROJECTION.md, source custody. Uses default GPT export mode (direct export appropriate)
- **codex-cortex**: Has SOURCE.md, PROJECTION.md, source custody, first-party ledgers. Uses default GPT export mode (direct export appropriate)
- **repo-worker-base**: Has SOURCE.md, PROJECTION.md, source custody. Uses default GPT export mode (direct export appropriate)
- **dotnet-kit**: Has SOURCE.md, PROJECTION.md, source custody, first-party ledgers. Uses default GPT export mode (direct export appropriate)
- **api-contracts-pack**: Has SOURCE.md, PROJECTION.md, source custody. Uses default GPT export mode (direct export appropriate)
- **architecture-pack**: Has SOURCE.md, PROJECTION.md, source custody. Uses default GPT export mode (direct export appropriate)
- **language-patterns-pack**: Has SOURCE.md, PROJECTION.md, source custody. Uses default GPT export mode (direct export appropriate)
- **security-pack**: Has SOURCE.md, PROJECTION.md, source custody. Uses default GPT export mode (direct export appropriate)
- **frontend-pack**: Has SOURCE.md, PROJECTION.md, source custody. Uses default GPT export mode (direct export appropriate)

### Compliant with PROJECTION.md (no overlays needed)
- **wild-bunch-project-pack**: Has SOURCE.md, PROJECTION.md, source custody. Uses default GPT export mode (direct export appropriate)

### First-party projections (different pattern, no overlays needed)
- **house-skills**: Has SOURCE.md, source custody, GPT manifest entries. Uses default GPT export mode (direct export appropriate)
- **adventures-pack**: Has SOURCE.md, first-party source custody. Uses default GPT export mode (direct export appropriate)
- **unslop**: Has SOURCE.md, adapted third-party custody. Uses default GPT export mode (direct export appropriate)
- **game-studio**: Has SOURCE.md, imported third-party custody. Uses default GPT export mode (direct export appropriate)

## Overlay Requirement Analysis

Based on first-pass analysis of platform-specific content and Skill tool dependencies:

### Plugins requiring overlays (already compliant)
- **superpowers-plus**: Has Skill tool dependencies and platform-specific routing, requires both Codex and GPT overlays (already implemented)

### Plugins suitable for direct export (first-pass classification)
- **house-skills**: First-party skills with descriptive Codex references, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **adventures-pack**: First-party skills with descriptive Codex references, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **unslop**: Adapted third-party skills with descriptive Codex references, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **wild-bunch-project-pack**: Mixed custody with descriptive Codex references, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **game-studio**: Imported third-party skills, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **superpowers-ecc**: Third-party ECC skills with descriptive Codex references, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **everything-codex-code**: Mirrored ECC skills with descriptive Codex references, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **codex-cortex**: Third-party Claude-Cortex skills, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **repo-worker-base**: First-party core skills with descriptive Codex references, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **dotnet-kit**: Third-party dotnet skills, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **api-contracts-pack**: Mirrored Claude-Cortex skills, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **architecture-pack**: Mirrored Claude-Cortex skills, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **language-patterns-pack**: Third-party Claude-Cortex skills, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **security-pack**: Third-party Claude-Cortex and ECC skills, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.
- **frontend-pack**: Third-party Claude-Cortex skills, no Skill tool dependencies found. First-pass classification: direct export appropriate pending full GPT QA.

**Note**: The "no Skill tool dependencies" analysis is a first-pass signal based on grep searches. Full per-skill GPT QA would be needed to confirm that these skills are truly GPT-safe for direct export without platform-specific adaptations.

## Follow-up Work Required

1. ✅ Add PROJECTION.md to plugins that have complex custody or adaptation stories (for documentation clarity) - COMPLETED
2. ✅ Add GPT manifest entries with direct export mode for all plugins that don't have them - COMPLETED
3. Update validation to enforce the standard for new plugins (future work)

## Validation Results

Marketplace validation passed successfully after normalization. All plugin roots, manifests, skill paths, and source custody surfaces validated correctly.
