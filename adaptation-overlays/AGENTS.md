# AGENTS.md

Scope: `adaptation-overlays/`

This scope covers intermediate Codex adaptation layers for skills that require platform-specific adjustments before final GPT export.

Codex plugin first; generated GPT-safe skill zips second.

## Overlay Type Distinction

This directory contains **adaptation overlays**, which are distinct from **GPT overlays**:

### Adaptation Overlays (`adaptation-overlays/`)
- **Purpose**: Intermediate Codex-specific adaptation layers
- **Target**: Codex plugin projections that need platform-specific adjustments
- **Content**: Codex-specific behavior, tool assumptions, runtime dependencies
- **Usage**: Applied during Codex plugin projection to adapt skills for Codex runtime
- **Examples**: Removing GPT-only assumptions, adding Codex tool references, adapting workflow orchestration

### GPT Overlays (`gpt-overlays/`)
- **Purpose**: Final GPT export adaptations for generated skill zips
- **Target**: GPT-safe skill exports in `generated/skill-zips/`
- **Content**: Platform-neutral guidance, removed Codex-specific assumptions
- **Usage**: Applied during skill.zip generation to create GPT-compatible exports
- **Examples**: Removing subagent dependencies, platform-neutral design, GPT-safe workflows

## Workflow

1. **Source custody** → Original skill in `sources/first_party/` or `sources/third_party/`
2. **Codex projection** → Skill projected to `codex-marketplace/plugins/<pack>/skills/`
3. **Adaptation overlay** → Codex-specific adjustments applied (if needed)
4. **GPT overlay** → Final GPT export adjustments applied (if needed)
5. **Generated export** → Final skill.zip in `generated/skill-zips/`

## Review Guidelines

- Adaptation overlays should only contain Codex-specific adjustments
- Do not weaken Codex-native plugin behavior through adaptation overlays
- Keep adaptation overlays focused on runtime compatibility, not content changes
- GPT overlays should handle platform-neutralization, not adaptation overlays
- Maintain clear separation between Codex runtime adaptations and GPT export adaptations