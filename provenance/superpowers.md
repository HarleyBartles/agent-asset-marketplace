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

The bundle also projects the first-party `linear-superpowers` skill from
`codex-marketplace/plugins/house-skills/skills/linear-superpowers/SKILL.md`
into `codex-marketplace/plugins/superpowers/skills/linear-superpowers/SKILL.md`
so the Superpowers plugin surface shows Harley's compositional Linear workflow
skill without creating a second editable source root.

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
