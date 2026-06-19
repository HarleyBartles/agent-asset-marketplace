# Marketplace Inventory Classification

## MARK-237 Standard

The standard established in MARK-237 for Superpowers+ has three layers:

1. **Source custody**: Verbatim upstream snapshot in `sources/third_party/<name>/` or first-party source in `sources/first_party/`
2. **Codex projection layer**: Installable Codex plugin in `codex-marketplace/plugins/<name>/` with optional Codex-specific adaptations in `adapters/codex/<name>/`
3. **GPT export layer**: GPT-specific adaptations in `adapters/gpt/<name>/` controlled by `adapters/gpt/manifest.json` (direct/overlay/excluded per skill)

## Plugin Classification

### Fully Compliant (MARK-237 standard)
- **superpowers-plus**: Has SOURCE.md, PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries, source custody

### Partially Compliant (has PROJECTION.md but lacks overlays)
- **wild-bunch-project-pack**: Has SOURCE.md, PROJECTION.md, source custody. Lacks Codex overlays, GPT overlays, GPT manifest entries

### Partially Compliant (needs PROJECTION.md and/or overlays)
- **superpowers-ecc**: Has SOURCE.md, source custody, GPT manifest entries. Lacks PROJECTION.md, Codex overlays, GPT overlays
- **house-skills**: Has SOURCE.md, source custody, GPT manifest entries. Lacks PROJECTION.md, Codex overlays, GPT overlays
- **everything-codex-code**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **codex-cortex**: Has SOURCE.md, source custody, first-party ledgers. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **repo-worker-base**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **dotnet-kit**: Has SOURCE.md, source custody, first-party ledgers. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **api-contracts-pack**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **architecture-pack**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **language-patterns-pack**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **security-pack**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **frontend-pack**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries

### First-party projections (different pattern, may not need full overlay treatment)
- **adventures-pack**: Has SOURCE.md, first-party source custody. May not need overlays if purely first-party
- **unslop**: Has SOURCE.md, adapted third-party custody. May need overlays if adaptations are platform-specific
- **game-studio**: Has SOURCE.md, imported third-party custody. May need overlays if adaptations are platform-specific

## Overlay Requirement Analysis

Based on analysis of platform-specific content and Skill tool dependencies:

### Plugins requiring overlays (already compliant)
- **superpowers-plus**: Has Skill tool dependencies and platform-specific routing, requires both Codex and GPT overlays (already implemented)

### Plugins suitable for direct export (no overlays needed)
- **house-skills**: First-party skills with descriptive Codex references, no Skill tool dependencies, direct export appropriate
- **adventures-pack**: First-party skills with descriptive Codex references, no Skill tool dependencies, direct export appropriate
- **unslop**: Adapted third-party skills with descriptive Codex references, no Skill tool dependencies, direct export appropriate
- **wild-bunch-project-pack**: Mixed custody with descriptive Codex references, no Skill tool dependencies, direct export appropriate
- **game-studio**: Imported third-party skills, no Skill tool dependencies, direct export appropriate
- **superpowers-ecc**: Third-party ECC skills with descriptive Codex references, no Skill tool dependencies, direct export appropriate
- **everything-codex-code**: Mirrored ECC skills with descriptive Codex references, no Skill tool dependencies, direct export appropriate
- **codex-cortex**: Third-party Claude-Cortex skills, no Skill tool dependencies, direct export appropriate
- **repo-worker-base**: First-party core skills with descriptive Codex references, no Skill tool dependencies, direct export appropriate
- **dotnet-kit**: Third-party dotnet skills, no Skill tool dependencies, direct export appropriate
- **api-contracts-pack**: Mirrored Claude-Cortex skills, no Skill tool dependencies, direct export appropriate
- **architecture-pack**: Mirrored Claude-Cortex skills, no Skill tool dependencies, direct export appropriate
- **language-patterns-pack**: Third-party Claude-Cortex skills, no Skill tool dependencies, direct export appropriate
- **security-pack**: Third-party Claude-Cortex and ECC skills, no Skill tool dependencies, direct export appropriate
- **frontend-pack**: Third-party Claude-Cortex skills, no Skill tool dependencies, direct export appropriate

## Follow-up Work Required

1. Add PROJECTION.md to plugins that have complex custody or adaptation stories (for documentation clarity)
2. Add GPT manifest entries with direct export mode for all plugins that don't have them
3. Update validation to enforce the standard for new plugins
