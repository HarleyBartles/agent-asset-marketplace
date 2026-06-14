# Source

This bundle projects the upstream `obra/superpowers` `v5.1.0` release into the
Codex marketplace.

## Canonical basis

- Upstream repository: `https://github.com/obra/superpowers`
- Release tag: `v5.1.0`
- Resolved release commit: `f2cbfbefebbfef77321e4c9abc9e949826bea9d7`
- Tag object: `ecbd610fce16d5faabcea997f17031129589b572`
- License: MIT
- Retained source custody:
  `sources/third_party/superpowers/obra-superpowers/v5.1.0/`

## Projected surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/app-icon.png`
- `assets/superpowers-small.svg`
- `LICENSE`
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
