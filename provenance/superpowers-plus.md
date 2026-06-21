# Superpowers Provenance

## Source anchor

- Upstream repository: `https://github.com/obra/superpowers`
- Release tag: `v6.0.3`
- Release commit: `896224c4b1879920ab573417e68fd51d2ccc9072`
- Tag object: `45c3cc5b66cfc5f147a7ddcfb86f7650e47a8ae0`
- License: MIT

## Custody

The upstream release snapshot is retained in third-party source custody at
`sources/third_party/superpowers/obra-superpowers/v6.0.3/`.

## Marketplace projection

The Codex-facing marketplace projection lives at
`codex-marketplace/plugins/superpowers-plus/`.

It copies the upstream skill trees and Codex assets into the active plugin
surface and keeps the non-Codex harness metadata and hooks in third-party
source custody.

Projection contract:

- `superpowers-plus` is the third-party plugin projection with selected
  first-party compositional skills projected into the vendored marketplace
  plugin.
- The active plugin may contain upstream Superpowers skills plus the selected
  first-party wrapper skills `linear-superpowers`, `github-superpowers`,
  `unslop-superpowers`, `architecture-superpowers`, `ecc-superpowers`, and
  `inspecting-the-environment`.
- Those first-party skills are compositional and complementary. They compose
  Superpowers workflow guidance with first-party expert skills that live
  outside the Superpowers plugin.
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

The bundle also projects the first-party `linear-superpowers` skill from
`sources/first_party/skills/linear-superpowers/`
into `codex-marketplace/plugins/superpowers-plus/skills/linear-superpowers/`
and the first-party `github-superpowers` skill from
`sources/first_party/skills/github-superpowers/`
into `codex-marketplace/plugins/superpowers-plus/skills/github-superpowers/`
and the first-party `unslop-superpowers` skill from
`sources/first_party/skills/unslop-superpowers/`
into `codex-marketplace/plugins/superpowers-plus/skills/unslop-superpowers/`
and the first-party `architecture-superpowers` skill from
`sources/first_party/skills/architecture-superpowers/`
into `codex-marketplace/plugins/superpowers-plus/skills/architecture-superpowers/`
and the first-party `ecc-superpowers` skill from
`sources/first_party/skills/ecc-superpowers/`
into `codex-marketplace/plugins/superpowers-plus/skills/ecc-superpowers/`
and the first-party `inspecting-the-environment` skill from
`sources/first_party/skills/inspecting-the-environment/`
into `codex-marketplace/plugins/superpowers-plus/skills/inspecting-the-environment/`
so the Superpowers plugin surface shows Harley's compositional Linear,
GitHub, anti-slop, architecture, ECC routing, and environment-inspection
workflow skills without creating second editable source roots.

These first-party projections are directory-level skill specs with
`SKILL.md` and `agents/openai.yaml` under the same source/projection contract.

`linear-superpowers`, `github-superpowers`, `architecture-superpowers`, and
`ecc-superpowers` invoke `unslop-superpowers` when repo-specific anti-slop
controls, profile-aware non-goals, or evidence requirements matter.

`ecc-superpowers` is a verbatim first-party router wrapper that points to the
dedicated `superpowers-ecc` pack. It is compositional, not a fork cue, and it
keeps ECC workflow doctrine out of the upstream Superpowers snapshot.

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
