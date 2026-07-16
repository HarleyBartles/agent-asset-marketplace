# Superpowers Provenance

## Source anchor

- Upstream repository: `https://github.com/obra/superpowers`
- Release tag: `v6.1.0`
- Release commit: `f268f7c953744036f0fa7e9d4b73535c04e57cb8`
- Tag object: `61fd6f0ebbb6c6ff58d8cc61ada4073a8df8c35e`
- License: MIT

## Custody

The upstream release snapshot is retained in third-party source custody at
`sources/third_party/superpowers/obra-superpowers/v6.1.0/`.

## Marketplace projection

The Codex-facing marketplace projection lives at
`codex-marketplace/plugins/superpowers-plus/`.

It copies the upstream skill trees and Codex assets into the active plugin
surface and keeps the non-Codex harness metadata and hooks in third-party
source custody.

Projection contract:

- `superpowers-plus` is the third-party plugin projection with the upstream
  Superpowers core plus the first-party `inspecting-the-environment` helper.
- The first-party helper is compositional and complementary. It keeps
  Superpowers workflow guidance narrow by adding environment inspection only.
- Do not place first-party expert or domain skills directly in the Superpowers
  plugin.
- Do not use this plugin as a dumping ground for House Skills, project doctrine,
  verification experts, GitHub/Linear mechanics, or other first-party expert
  surfaces.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or
  reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection
  wording.
- Any future first-party skill proposed for projection into `superpowers-plus`
  must be justified as a compositional wrapper over Superpowers, not as an
  expert skill being relocated into the third-party plugin.

The bundle projects the first-party `inspecting-the-environment` skill from
`sources/first_party/skills/inspecting-the-environment/`
into `codex-marketplace/plugins/superpowers-plus/skills/inspecting-the-environment/`
so the Superpowers plugin surface retains the environment-inspection helper
without introducing second editable source roots.

## Excluded from the active projection

- `.claude-plugin/`
- `.cursor-plugin/`
- `.opencode/`
- `gemini-extension.json`
- `CLAUDE.md`
- `GEMINI.md`
- `hooks/`

Those surfaces remain source evidence for the upstream package boundary and are
not part of the Codex install surface on this pass.
