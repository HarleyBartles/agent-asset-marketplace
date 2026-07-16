# Source

This plugin replaces the vendored `unslop` plugin as a combined third/first-party projection. It composes the upstream `mshumer/unslop` workflow engine (adapted for Codex/GPT skill use) with thirteen first-party portable profiles (projected verbatim from first-party source custody).

## Upstream Basis

- Repo: `mshumer/unslop`
- URL: <https://github.com/mshumer/unslop.git>
- Pinned commit: `edcb62386d129c65e4395f0cfcc9168eb1ba2148`
- License: `MIT` (Copyright (c) 2026 Matt Shumer)
- Source custody: `sources/third_party/unslop/upstream/`
- Projection: engine script adapted into `skills/unslop-plus/scripts/unslop.py`

### Why the upstream engine is adapted, not shipped verbatim

The upstream `unslop.py` is a Claude Code CLI tool. It cannot ship verbatim as a Codex/GPT skill package because:

1. **Claude Code CLI dependency**: The upstream script requires the `claude` CLI binary (`shutil.which("claude")` check at line 996, exits with error if missing). It spawns `claude -p` as a subprocess (line 407) for sample generation and pattern analysis. This runtime assumption is inappropriate for a Codex/GPT skill package that must run in arbitrary Python environments.
2. **Interactive TerminalUI**: The upstream script includes a full interactive terminal UI with spinners, progress bars, TTY detection, ANSI color codes, and live-updating display (lines 30-170). These are not appropriate for a non-interactive skill package.
3. **Process signal handling**: The upstream uses `signal`, `os`, and `time` modules for subprocess management and timeout handling tied to the Claude Code CLI process model.
4. **Claude Code permission denial handling**: The upstream includes Claude Code-specific permission denial detection and error messages (lines 533-540).

The projected script adapts the upstream idea (sample collection, pattern detection, profile generation) to use Python standard library text analysis, local sample files, and optional Playwright for visual dependencies. The upstream MIT license and copyright are preserved in `skills/unslop-plus/LICENSE.upstream`.

## First-Party Profile Source Custody

- Profile author: Harley Bartles (Asset Marketplace)
- Profile source: MARK-265 Linear issue requirements
- Profile license: MIT
- Canonical source custody: `sources/first_party/skills/unslop-plus/profiles/`
- Projection: profiles projected verbatim into `skills/unslop-plus/profiles/`

## Marketplace Composition

- Replaces the vendored `unslop` plugin root in `plugin-roots.json`
- Third-party Unslop engine script adapted from upstream custody (not byte-identical)
- Thirteen first-party portable profiles projected verbatim from first-party source custody
- Each profile is portable across repos with no Asset Marketplace-specific nouns
- Provenance distinguishes third-party engine adaptation from first-party profile authorship
- Upstream MIT license preserved at `skills/unslop-plus/LICENSE.upstream`
- Plugin-level MIT license at `LICENSE` covers first-party profile and adaptation work

## Install Shape

- GPT skill package: `codex-marketplace/plugins/unslop-plus/skills/unslop-plus/`
- Codex plugin route: `codex-marketplace/plugins/unslop-plus/.codex-plugin/plugin.json`
- Marketplace registry: `.agents/plugins/marketplace.json`
