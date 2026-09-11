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
- Use code formatting for literal commands, paths, identifiers, and values; do not use code formatting for emphasis.
- Skill names are kebab-case. First-party source skills live under `codex-marketplace/plugins/<plugin>/skills/<name>/`.
- Use `Optional[X]` rather than `X | None` for nullable type annotations.
- Generated surfaces (`codex-marketplace/` and `.agents/skills/` from marketplace) are downstream outputs. Edit canonical source, then regenerate.

## Workflow routing

Invoke `using-superpowers-plus` once and follow its handoff. The routed writing
and authoring skills own general prose and document method; this runbook owns
only repository-specific Python and Markdown conventions.
