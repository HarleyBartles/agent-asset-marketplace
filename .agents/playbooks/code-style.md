# Code Style Playbook

## When

Use when Python, Markdown, or agent-facing prose changes.

## Required skills

- `writing-with-clarity` for human-facing prose.
- `writing-skills` for skill authoring conventions.

## Composition

Apply the named capability skills under the binding doctrine and local evidence requirements. This playbook does not own a lifecycle stage.

## Doctrine and contracts

- [Skill standards policy](../doctrine/skill-standards-policy.md)

Durable coding and architecture invariants belong in doctrine. Reusable language and framework technique belongs in capability skills; this playbook binds those owners to repository conventions.

## Local commands and paths

Use LF line endings. Use code formatting for literal commands, paths, identifiers, and values rather than emphasis. Skill names are kebab-case. First-party skill source lives under `codex-marketplace/plugins/<plugin>/skills/<name>/`. Prefer `Optional[X]` to `X | None` for Python compatibility; avoid the Python 3.13-only `Path.read_text(newline=...)` in Python 3.12-compatible scripts. Edit canonical plugin source before regeneration.

## Evidence contract

Changed prose and code follow repository conventions without duplicating portable technique.

## Prohibited combinations

Do not use this playbook as a bucket for durable architecture law or framework tutorials.

## Invoked by

- [Implementation](../runbooks/implementing.md)
- [Code review](../runbooks/code-review.md)
