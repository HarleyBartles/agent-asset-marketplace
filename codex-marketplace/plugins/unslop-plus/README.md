# Unslop+

Anti-slop profiles for software development workflows.

## What's Included

This plugin bundles an adapted Unslop analysis engine with thirteen first-party portable profiles:

- **writing** - Generic AI prose patterns
- **technical-writing** - Documentation and technical content
- **implementation-plans** - Executable coding plans
- **code-review** - Evidence-based code review
- **worker-returns** - Completion report validation
- **debugging** - Systematic bug diagnosis
- **frontend-react** - React implementation defaults
- **frontend-ui** - Generic UI patterns
- **api-design** - API contract design
- **architecture** - Pattern-based architecture reasoning
- **testing** - Behavior-focused testing
- **security-review** - Concrete security analysis
- **cleanup-custody** - Repository hygiene decisions

## Usage

Use the appropriate profile for your workflow before drafting or reviewing content.

## Provenance

- Engine: Adapted from `mshumer/unslop` (MIT license, Copyright (c) 2026 Matt Shumer). The upstream script is a Claude Code CLI tool; the projected script is adapted for Codex/GPT skill use with Python standard library text analysis. See `SOURCE.md` for the adaptation rationale.
- Profiles: First-party portable profiles by Asset Marketplace (MIT license)
- Upstream source custody: `sources/third_party/unslop/upstream/` (retained verbatim)
- First-party profile custody: `sources/first_party/skills/unslop-plus/profiles/`
- Upstream MIT notice: `skills/unslop-plus/LICENSE.upstream`
