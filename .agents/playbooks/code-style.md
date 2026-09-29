# Code Style Playbook

## When

Use when Python, Markdown, or agent-facing prose changes.

## Required capabilities

- Write clear human-facing repository guidance.
- Create or update reusable skills with appropriate scope and supporting resources.

## Optional capabilities

None.

## Required repository-owned skills

None.

## Optional repository-owned skills

None.

## Composition

Resolve the stated capabilities against skills available at runtime, under the binding doctrine and local evidence requirements. Stop and report if a required capability has no suitable provider. This playbook does not own a lifecycle stage.

## Doctrine and contracts

- [Skill standards policy](../doctrine/skill-standards-policy.md)

Durable coding and architecture invariants belong in doctrine. Reusable language and framework technique belongs in capability skills; this playbook binds those owners to repository conventions.

## Local commands and paths

Use LF line endings. Markdown prose uses semantic paragraphs without hard wrapping; `py -3 .agents/standards/markdown-formatting/markdown-formatting/scripts/format_markdown.py --apply` normalizes eligible tracked Markdown with the pinned portable toolchain, and `--check` rejects drift. Authority evidence under `assets/authority/` remains byte-preserved, and the unrendered writing-skills scaffold template is excluded because its `{metadata}` insertion token is not valid YAML until materialization. Use code formatting for literal commands, paths, identifiers, and values rather than emphasis. Skill names are kebab-case. First-party maintained skill source lives under `skills/<skill-id>/`; edit that source before rebuilding plugin packages. Prefer `Optional[X]` to `X | None` for Python compatibility; avoid the Python 3.13-only `Path.read_text(newline=...)` in Python 3.12-compatible scripts.

## Markdown formatting

Use the repository's declared formatter command for repository-wide check/apply and producer-scoped checks. Generated Markdown must be formatter-clean at its producer.

## Evidence contract

Changed prose and code follow repository conventions without duplicating portable technique.

## Prohibited combinations

Do not use this playbook as a bucket for durable architecture law or framework tutorials.

## Runbook routing

- [Implementation](../runbooks/implementing.md)
- [Code review](../runbooks/code-review.md)
