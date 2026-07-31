# Source

This plugin projects a first-party `unslop-engine` skill and a first-party `unslop-profiles` skill.

## Upstream Basis

- Repo: `mshumer/unslop`
- URL: <https://github.com/mshumer/unslop.git>
- Pinned commit: `edcb62386d129c65e4395f0cfcc9168eb1ba2148`
- License: `MIT` (Copyright (c) 2026 Matt Shumer)
- Source custody: `sources/third_party/unslop/upstream/`
- Projection: engine script adapted into `skills/unslop-engine/scripts/unslop.py`

### Why the upstream engine is adapted, not shipped verbatim

The upstream `unslop.py` is a Claude Code CLI tool. It cannot ship verbatim as a Codex/GPT skill package because:

1. **Claude Code CLI dependency**: The upstream script requires the `claude` binary and spawns `claude -p` as a subprocess for sample generation. This runtime assumption is inappropriate for a Codex/GPT skill package.
2. **Interactive TerminalUI**: The upstream script includes an interactive terminal UI with spinners, progress bars, TTY detection, ANSI color codes, and live-updating display. These are not appropriate for a non-interactive skill package.
3. **Process signal handling**: The upstream uses `signal`, `os`, and `time` modules for subprocess management and timeout handling tied to the Claude Code CLI process model.
4. **Claude Code permission denial handling**: The upstream includes Claude Code-specific permission denial detection and error messages.

The projected `unslop-engine` skill adapts the upstream idea (sample collection, pattern detection, profile generation) to use Python standard library text analysis, local sample files, and optional Playwright for visual evidence. The upstream MIT license and copyright are preserved in `skills/unslop-engine/LICENSE.upstream`.

## First-Party Source Custody
<!-- BEGIN GENERATED: pack-inventory -->
## Source custody
### First Party custody
- `sources/first_party/skills/unslop-engine/`
- `sources/first_party/skills/unslop-profiles/`

## Projection surfaces
- Codex plugin root: `codex-marketplace/plugins/unslop-plus/`
- Skill root: `codex-marketplace/plugins/unslop-plus/skills/`
- Skill roots:
  - `codex-marketplace/plugins/unslop-plus/skills/unslop-engine/`
  - `codex-marketplace/plugins/unslop-plus/skills/unslop-profiles/`
<!-- END GENERATED: pack-inventory -->

## Marketplace Composition

- The `unslop-plus` plugin root projects `unslop-engine` and `unslop-profiles` first-party skills.
- The `unslop-engine` skill is an adaptation of the upstream `mshumer/unslop` idea; the `unslop-profiles` skill is a first-party read-when router.
- Each profile is portable across repos with no Asset Marketplace-specific nouns.
- Provenance distinguishes third-party engine adaptation from first-party profile authorship.
- Upstream MIT license preserved at `skills/unslop-engine/LICENSE.upstream`.
- Plugin-level MIT license at `LICENSE` covers first-party profile and adaptation work.
