# AGENTS.md

Scope: `gpt-overlays/`

This scope covers source-owned GPT export overlays for generated skill zips.

Codex plugin first; generated GPT-safe skill zips second.

## Overlay Type Distinction

This directory contains **GPT overlays**, which are distinct from **adaptation overlays**:

### GPT Overlays (`gpt-overlays/`)
- **Purpose**: Final GPT export adaptations for generated skill zips
- **Target**: GPT-safe skill exports in `generated/skill-zips/`
- **Content**: Platform-neutral guidance, removed Codex-specific assumptions
- **Usage**: Applied during skill.zip generation to create GPT-compatible exports
- **Examples**: Removing subagent dependencies, platform-neutral design, GPT-safe workflows

### Adaptation Overlays (`adaptation-overlays/`)
- **Purpose**: Intermediate Codex-specific adaptation layers
- **Target**: Codex plugin projections that need platform-specific adjustments
- **Content**: Codex-specific behavior, tool assumptions, runtime dependencies
- **Usage**: Applied during Codex plugin projection to adapt skills for Codex runtime
- **Examples**: Removing GPT-only assumptions, adding Codex tool references, adapting workflow orchestration

## Workflow

1. **Source custody** → Original skill in `sources/first_party/` or `sources/third_party/`
2. **Codex projection** → Skill projected to `codex-marketplace/plugins/<pack>/skills/`
3. **Adaptation overlay** → Codex-specific adjustments applied (if needed)
4. **GPT overlay** → Final GPT export adjustments applied (if needed)
5. **Generated export** → Final skill.zip in `generated/skill-zips/`

Overlay files in this tree are not the Codex plugin projection and not the
generated artifact surface. They are the source input for GPT-ready exports.

Keep overlay paths aligned with `gpt-overlays/manifest.json`, and keep the
manifest aligned with the generated registry fields that prove source plus
overlay derivation.

Do not hand-edit files under `generated/skill-zips/`. Do not copy Codex plugin
projection assumptions into GPT overlays unless the overlay itself is the
intentional adaptation.

Overlays may adapt wording or guidance for GPT safety, but they must not weaken
Codex-native plugin behavior or imply that generated exports are the canonical
source.

