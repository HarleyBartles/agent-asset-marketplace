# Code Style Runbook

Use this runbook for Python and Markdown conventions in `agent-asset-marketplace`.

## Before you begin

- Read [`.agents/doctrine/skill-standards-policy.md`](../../.agents/doctrine/skill-standards-policy.md) for skill shape standards.
- Read [`.devin/rules/tools.md`](../../.devin/rules/tools.md) for tooling conventions.

## When to use

- Writing new Python scripts or Markdown docs.
- Reviewing style in a PR.

## Repo-specific guidance

- Write all text files with LF line endings. Use `with path.open("w", encoding="utf-8", newline="\n") as f: f.write(content)` for new code; `Path.read_text(newline=...)` requires Python 3.13, so do not use it in scripts that must run under Python 3.12.
- Follow `.agents/doctrine/skill-standards-policy.md` for skill frontmatter and metadata fields.
- Keep Markdown headings descriptive of the reader's task.
- Use code formatting for literal commands, paths, identifiers, and values; do not use code formatting for emphasis.
- Prefer active voice and concise sentences in human-facing prose.
- Skill names are kebab-case. First-party source skills live under `codex-marketplace/plugins/<plugin>/skills/<name>/`.
- Generated surfaces (`codex-marketplace/` and `.agents/skills/` from marketplace) are downstream outputs. Edit canonical source, then regenerate.

## Routing to skills

- `/writing-with-clarity` for human-facing prose.
- `/repo-worker-base` for repo hygiene and publication boundaries.
