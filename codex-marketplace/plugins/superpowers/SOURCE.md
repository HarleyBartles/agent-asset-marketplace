# Source

This bundle projects the upstream `obra/superpowers` `v5.1.0` release into the
Codex marketplace and adds the first-party `linear-superpowers`,
`github-superpowers`, `unslop-superpowers`, `codex-receipts-superpowers`, and
`architecture-superpowers` skills from House Skills as source-backed
projections.

## Projection contract

- `superpowers` is a third-party plugin projection with selected first-party
  compositional skills projected into the vendored marketplace plugin.
- The active plugin may contain upstream Superpowers skills plus the selected
  first-party wrapper skills `linear-superpowers`, `github-superpowers`,
  `unslop-superpowers`, `codex-receipts-superpowers`, and
  `architecture-superpowers`.
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
- Any future first-party skill proposed for projection into `superpowers` must
  be justified as a compositional wrapper over Superpowers, not as an expert
  skill being relocated into the third-party plugin.

## Canonical basis

- Upstream repository: `https://github.com/obra/superpowers`
- Release tag: `v5.1.0`
- Resolved release commit: `f2cbfbefebbfef77321e4c9abc9e949826bea9d7`
- Tag object: `ecbd610fce16d5faabcea997f17031129589b572`
- License: MIT
- Retained source custody:
  `sources/third_party/superpowers/obra-superpowers/v5.1.0/`
- House Skills source custody:
  `sources/first_party/skills/linear-superpowers/`
  `sources/first_party/skills/github-superpowers/`
  `sources/first_party/skills/unslop-superpowers/`
  `sources/first_party/skills/codex-receipts-superpowers/`

## Projected surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/app-icon.png`
- `assets/superpowers-small.svg`
- `LICENSE`
- `skills/linear-superpowers/`
- `skills/github-superpowers/`
- `skills/unslop-superpowers/`
- `skills/codex-receipts-superpowers/`
- `references/codex-marketplace-compatibility.md`

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

`linear-superpowers`, `github-superpowers`, `unslop-superpowers`,
`codex-receipts-superpowers`, and `architecture-superpowers` stay editable in
House Skills and are projected here as readable directory copies for the
Superpowers bundle rather than as second source roots. Each first-party
projection is a directory-level skill spec that carries both `SKILL.md` and
`agents/openai.yaml` under the same custody contract.
