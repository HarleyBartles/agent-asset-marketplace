# Unslop+

Anti-slop engine and profile router for software development workflows.

## What's Included

## Usage

Use `$unslop-engine` to generate a new domain-specific anti-slop profile from samples, or `$unslop-profiles` to apply the right existing generic profile for your current task. When `writing-pack` is installed, route sustained prose through `$writing`; `unslop-plus` remains independently usable without it.

## Provenance

- Engine: Adapted from `mshumer/unslop` (MIT license, Copyright (c) 2026 Matt Shumer). The upstream script is a Claude Code CLI tool; the bundled `unslop-engine` skill is adapted for Codex/GPT skill use with Python standard library text analysis. See `SOURCE.md` for the adaptation rationale.
- Profiles: First-party portable profiles by Asset Marketplace (MIT license).
- Upstream source custody: `SOURCE.md` (contains the adaptation rationale and provenance record).
- First-party profile custody: `codex-marketplace/plugins/unslop-plus/skills/unslop-profiles/references/profiles/`.
- Upstream MIT notice: `skills/unslop-engine/LICENSE.upstream`.
