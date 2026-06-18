# Superpowers Provenance

## Source anchor

- Upstream repository: `https://github.com/obra/superpowers`
- Release tag: `v5.1.0`
- Release commit: `f2cbfbefebbfef77321e4c9abc9e949826bea9d7`
- Tag object: `ecbd610fce16d5faabcea997f17031129589b572`
- License: MIT

## Custody

The upstream release snapshot is retained in third-party source custody at
`sources/third_party/superpowers/obra-superpowers/v5.1.0/`.

## Marketplace projection

The Codex-facing marketplace projection lives at
`codex-marketplace/plugins/superpowers/`.

It copies the upstream skill trees and Codex assets into the active plugin
surface and keeps the non-Codex harness metadata and hooks in third-party
source custody.

Projection contract:

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

The bundle also projects the first-party `linear-superpowers` skill from
`sources/first_party/skills/linear-superpowers/`
into `codex-marketplace/plugins/superpowers/skills/linear-superpowers/`
and the first-party `github-superpowers` skill from
`sources/first_party/skills/github-superpowers/`
into `codex-marketplace/plugins/superpowers/skills/github-superpowers/`
and the first-party `unslop-superpowers` skill from
`sources/first_party/skills/unslop-superpowers/`
into `codex-marketplace/plugins/superpowers/skills/unslop-superpowers/`
and the first-party `codex-receipts-superpowers` skill from
`sources/first_party/skills/codex-receipts-superpowers/`
into `codex-marketplace/plugins/superpowers/skills/codex-receipts-superpowers/`
and the first-party `architecture-superpowers` skill from
`sources/first_party/skills/architecture-superpowers/`
into `codex-marketplace/plugins/superpowers/skills/architecture-superpowers/`
so the Superpowers plugin surface shows Harley's compositional Linear,
GitHub, anti-slop, receipt, and architecture workflow skills without creating
second editable source roots.

These first-party projections are directory-level skill specs with
`SKILL.md` and `agents/openai.yaml` under the same source/projection contract.

`linear-superpowers`, `github-superpowers`, `codex-receipts-superpowers`, and
`architecture-superpowers` invoke `unslop-superpowers` when repo-specific
anti-slop controls, profile-aware non-goals, or evidence requirements matter.

This is the final allowed pre-fork Superpowers wrapper projection. Any further
first-party wrapper projection into `superpowers` requires the Superpowers
fork/overlay custody model to exist first, plus a migration plan for the
existing wrapper set:
`linear-superpowers`, `github-superpowers`, `unslop-superpowers`,
`codex-receipts-superpowers`, and `architecture-superpowers`.

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
