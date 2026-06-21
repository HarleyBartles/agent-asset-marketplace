# Source

This bundle projects the upstream `obra/superpowers` `v6.0.3` release into the
Codex marketplace as `Superpowers+` and adds the first-party
`linear-superpowers`, `github-superpowers`, `unslop-superpowers`, and
`architecture-superpowers` skills from House Skills as source-backed
projections, plus the first-party `ecc-superpowers` routing wrapper that
points to the dedicated `superpowers-ecc` pack, plus the first-party
`inspecting-the-environment` skill.

## Projection contract

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

## Canonical basis

- Upstream repository: `https://github.com/obra/superpowers`
- Release tag: `v6.0.3`
- Resolved release commit: `896224c4b1879920ab573417e68fd51d2ccc9072`
- Tag object: `45c3cc5b66cfc5f147a7ddcfb86f7650e47a8ae0`
- License: MIT
- Retained source custody:
  `sources/third_party/superpowers/obra-superpowers/v6.0.3/`
- First-party source custody:
  `sources/first_party/skills/linear-superpowers/`
  `sources/first_party/skills/github-superpowers/`
  `sources/first_party/skills/unslop-superpowers/`
  `sources/first_party/skills/architecture-superpowers/`
  `sources/first_party/skills/ecc-superpowers/`
  `sources/first_party/skills/inspecting-the-environment/`

## Projected surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/app-icon.png`
- `assets/superpowers-small.svg`
- `LICENSE`
- `skills/linear-superpowers/`
- `skills/github-superpowers/`
- `skills/unslop-superpowers/`
- `skills/architecture-superpowers/`
- `skills/ecc-superpowers/`
- `skills/inspecting-the-environment/`
- `references/codex-marketplace-compatibility.md`
- `references/source-map.md`

## Source-only support provenance

These upstream harness surfaces stay in third-party source custody on the first
pass and are not projected into the Codex install surface:

- `.claude-plugin/`
- `.cursor-plugin/`
- `.opencode/`
- `gemini-extension.json`
- `CLAUDE.md`
- `GEMINI.md`
- `hooks/`

## Notes

The retained upstream snapshot also preserves the broader package boundary
(`docs/`, `scripts/`, `tests/`, `README.md`, `package.json`, `AGENTS.md`, and
the top-level license and release notes) in third-party custody.

`linear-superpowers`, `github-superpowers`, `unslop-superpowers`, and
`architecture-superpowers` stay editable in House Skills and are projected
here as readable directory copies for the Superpowers bundle rather than as
second source roots. `ecc-superpowers` is the first-party router wrapper
that points to the dedicated `superpowers-ecc` pack. `inspecting-the-environment`
is the first-party environment-inspection skill. Each first-party
projection is a directory-level skill spec that carries both `SKILL.md` and
`agents/openai.yaml` under the same custody contract.
