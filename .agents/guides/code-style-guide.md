# Code Style Guide

Use this guide for Python and Markdown conventions in `agent-asset-marketplace`.

## Before you begin

- Read [`docs/skill-standards-policy.md`](../../docs/skill-standards-policy.md) for skill shape standards.
- Read [`tools/AGENTS.md`](../../tools/AGENTS.md) for tooling conventions.

## When to use

- Writing new Python scripts or Markdown docs.
- Reviewing style in a PR.

## Repo-specific guidance

- Write all text files with LF line endings. Use `with path.open("w", encoding="utf-8", newline="\n") as f: f.write(content)` instead of `Path.write_text(..., newline="\n")` for Python 3.12 compatibility.
- Follow `docs/skill-standards-policy.md` for skill frontmatter and metadata fields.
- Keep Markdown headings descriptive of the reader's task.
- Use code formatting for literal commands, paths, identifiers, and values; do not use code formatting for emphasis.
- Prefer active voice and concise sentences in human-facing prose.
- Skill names are kebab-case. First-party source skills live under `sources/first_party/skills/<name>/`.
- Generated surfaces (`codex-marketplace/`, `generated/`, `.agents/skills/` from marketplace) are downstream outputs. Edit canonical source, then regenerate.

## Routing to skills

- `/writing-with-clarity` for human-facing prose.
- `/repo-worker-base` for repo hygiene and publication boundaries.
