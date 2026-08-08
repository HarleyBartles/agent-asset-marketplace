# Source

This plugin contains the first-party `unslop-engine` skill and the first-party `unslop-profiles` skill.

## Upstream Basis

- Repo: `mshumer/unslop`
- URL: <https://github.com/mshumer/unslop.git>
- Pinned commit: `edcb62386d129c65e4395f0cfcc9168eb1ba2148`
- License: `MIT` (Copyright (c) 2026 Matt Shumer)
- Source custody: this `SOURCE.md`
- Distribution: engine script adapted into `skills/unslop-engine/scripts/unslop.py`

### Why the upstream engine is adapted, not shipped verbatim

The upstream `unslop.py` is a Claude Code CLI tool. It cannot ship verbatim as a Codex/GPT skill package because:

1. **Claude Code CLI dependency**: The upstream script requires the `claude` binary and spawns `claude -p` as a subprocess for sample generation. This runtime assumption is inappropriate for a Codex/GPT skill package.
2. **Interactive TerminalUI**: The upstream script includes an interactive terminal UI with spinners, progress bars, TTY detection, ANSI color codes, and live-updating display. These are not appropriate for a non-interactive skill package.
3. **Process signal handling**: The upstream uses `signal`, `os`, and `time` modules for subprocess management and timeout handling tied to the Claude Code CLI process model.
4. **Claude Code permission denial handling**: The upstream includes Claude Code-specific permission denial detection and error messages.

The `unslop-engine` skill adapts the upstream idea (sample collection, pattern detection, profile generation) to use Python standard library text analysis, local sample files, and optional Playwright for visual evidence. The upstream MIT license and copyright are preserved in `skills/unslop-engine/LICENSE.upstream`.

## First-Party Source Custody

## Marketplace Composition

- The `unslop-plus` plugin root contains the `unslop-engine` and `unslop-profiles` first-party skills.
- The `unslop-engine` skill is an adaptation of the upstream `mshumer/unslop` idea; the `unslop-profiles` skill is a first-party read-when router.
- Each profile is portable across repos with no Asset Marketplace-specific nouns.
- Provenance distinguishes third-party engine adaptation from first-party profile authorship.
- Upstream MIT license preserved at `skills/unslop-engine/LICENSE.upstream`.
- Plugin-level MIT license at `LICENSE` covers first-party profile and adaptation work.

## Provenance

### Vendor record

- Upstream repo: `mshumer/unslop`
- Pinned commit: `edcb62386d129c65e4395f0cfcc9168eb1ba2148`
- License: MIT
- Retained source record: this `SOURCE.md`
- Marketplace package: `codex-marketplace/plugins/unslop-plus/`

### Adaptation Notes

- GPT skill install paths: `codex-marketplace/plugins/unslop-plus/skills/unslop-engine/` and `codex-marketplace/plugins/unslop-plus/skills/unslop-profiles/`
- Codex plugin install path: `codex-marketplace/plugins/unslop-plus/.codex-plugin/plugin.json`
- Text mode uses Python standard library analysis over inline samples, fixture samples, or a sample directory.
- Visual mode checks for Playwright and Chromium before attempting visual evidence; missing optional dependencies are recorded as skipped in the output manifest and validation report.
- Output contract is documented in `skills/unslop-engine/references/output-contract.md`.

### Validation Expectations

- Package validator checks required GPT skill files and rejects forbidden shipped runtime instructions.
- Output validator checks `unslop-output/` for manifest, prompts, samples, counted analysis, draft profile strength, and visual evidence status.
- Repo marketplace validation checks the plugin manifest, registry entry, and bundle manifest.
