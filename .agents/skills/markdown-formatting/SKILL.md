---
name: markdown-formatting
description: Use when a repository adopts, enforces, or diagnoses the portable Markdown formatting standard or a Markdown generator must validate its output.
metadata:
  source-id: markdown-formatting
  source-path: codex-marketplace/plugins/agent-operating-model/skills/markdown-formatting/SKILL.md
  provenance-name: Markdown Formatting first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Portable Markdown normalization mechanics and consumer-contract validation.
  use_when:
    - a repository adopts or enforces the named Markdown formatting surface.
    - Markdown formatting drift or exclusions need diagnosis.
    - a generator that emits Markdown must validate its owned output.
  do_not_use_when:
    - the repository has not explicitly adopted the named surface.
    - formatting non-Markdown files.
license: MIT
---

# Markdown Formatting

Use `scripts/format_markdown.py` as the single implementation of the named Markdown formatting surface. It owns tracked-file selection, contract validation, pinned-toolchain validation, bounded formatter invocation, rollback on apply failure, and producer-scoped checks.

The consumer owns `.agents/contracts/markdown-formatting.json`, `.mdformat.toml`, dependency integration, exclusions, adoption, enforcement, and canonical command composition. Installing or refreshing this skill does not adopt the policy, install packages, reformat files, or enable a gate.

## Commands

```text
python scripts/format_markdown.py --check
python scripts/format_markdown.py --apply
python scripts/format_markdown.py --check-files path/to/generated.md [...]
```

No mode defaults to repository-wide check. `--check-files` is non-mutating and is the producer boundary for generators that emit tracked Markdown.

## Contract

Read [the contract schema](references/markdown-formatting-contract.schema.json) when authoring consumer policy. Exclusions are explicit `file` or `tree` custody claims with independent reasons. They are not globs, prospective reservations, generated-file shortcuts, or formatting preferences. Prefer making the file or producer compliant.

The native formatter configuration must keep prose unwrapped, use LF, validate output, write visible consecutive numbers for ordered lists, and enable GFM plus YAML frontmatter. The active interpreter must provide the exact versions in `requirements.txt`; hooks never install them dynamically.

`adopted` means the complete callable surface exists without binding formatting into repository gates. `enforced` is a separate decision that normalizes all eligible tracked Markdown before adding apply/check to canonical local and hosted validation.
