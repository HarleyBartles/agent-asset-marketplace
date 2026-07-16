# AGENTS.md

Scope: `adapters/gpt/`

This scope covers source-owned GPT export overlays for generated skill zips.

Codex plugin first; generated GPT-safe skill zips second.

Overlay roots are projections, not source custody, and they do not get manual
`INDEX.md` insertion inside skill or overlay roots.

Overlay files in this tree are not the Codex plugin projection and not the
generated artifact surface. They are the source input for GPT-ready exports.

Keep overlay paths aligned with `adapters/gpt/manifest.json`, and keep the
manifest aligned with the generated registry fields that prove source plus
overlay derivation.

Do not hand-edit files under `generated/skill-zips/`. Do not copy Codex plugin
projection assumptions into GPT overlays unless the overlay itself is the
intentional adaptation.

Overlays may adapt wording or guidance for GPT safety, but they must not weaken
Codex-native plugin behavior or imply that generated exports are the canonical
source.

## Maintenance responsibility

This file must stay aligned with `adapters/gpt/manifest.json`. When adding or
removing overlays, update the manifest first and ensure this AGENTS.md reflects
the current overlay strategy. Review this file when GPT export behavior changes
or when new overlay patterns are introduced.

