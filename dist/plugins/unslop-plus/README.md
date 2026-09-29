# Unslop+

Ambient profile application and consumer-reviewed profile lifecycle support for software workflows.

## What's Included

## Usage

Use `$unslop-profiles` to find, read, and apply a matching consumer-owned or bundled generic profile during work and review. Consumer profiles are exposed through explicit adoption of the optional Unslop standard; Unslop+ can also apply bundled profiles without that standard. Use `$unslop-engine` to turn recurring evidence into a consumer-reviewable profile proposal, revision, or retirement. It does not score whether agents followed profiles. When `writing-pack` is available, route sustained prose through `$writing`; Unslop+ remains independently useful for profile application without it.

## Provenance

- Engine: Adapted from `mshumer/unslop` (MIT license, Copyright (c) 2026 Matt Shumer). The upstream script is a Claude Code CLI tool; the bundled `unslop-engine` skill is adapted for Codex/GPT skill use with Python standard library text analysis. See `SOURCE.md` for the adaptation rationale.
- Profiles: First-party portable starter profiles by Asset Marketplace (MIT license); consumers own their local operational profiles.
- Upstream source custody: `SOURCE.md` (contains the adaptation rationale and provenance record).
- Profile source: `skills/unslop-profiles/references/profiles/`; built copy: `dist/plugins/unslop-plus/skills/unslop-profiles/references/profiles/`.
- Upstream MIT notice: `skills/unslop-engine/LICENSE.upstream`.
