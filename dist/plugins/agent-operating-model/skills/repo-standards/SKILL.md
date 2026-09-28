---
name: repo-standards
description: Use when aligning several repository operating-model concerns or deciding which focused repository standard owns a requested change.
metadata:
  source-id: repo-standards
  source-path: skills/repo-standards/SKILL.md
  provenance-name: Repo Standards router first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
license: MIT
---

# Repo Standards

Agent Operating Model is an ambient catalog. Its presence does not mean the consumer adopts any of its standards. Help the repository choose only the standards it wants, including none; keep repository-owned standards in the repository's own composition. Run checks and scaffolds only for the explicitly declared composition.

The catalog is packaged with `repo-shape` at `references/operating-standards-catalog.json`. Treat its entries as available choices; a repository adopts a standard only through its own explicit composition declaration.

Route the request to the smallest owning capability:

| Concern                                                       | Skill                   |
| ------------------------------------------------------------- | ----------------------- |
| Required repository surfaces and structural checks            | `repo-shape`            |
| Runbooks, playbooks, and their composition graph              | `repo-composition`      |
| Named command targets and dispatch semantics                  | `command-bus`           |
| Focused checks, complete gates, and evidence                  | `repository-validation` |
| Tracked pre-commit and hosted-CI parity                       | `tracked-repo-hooks`    |
| Markdown formatting adoption and enforcement                  | `markdown-formatting`   |
| Plugin subscriptions, local skills, and installed projections | `repo-agent-assets`     |
| Python implementation patterns                                | `python`                |

Read the consumer repository's local policy after selecting the owner. Compose multiple skills only for a migration that genuinely crosses their boundaries. Generic worker hygiene, worktrees, risk, publication, and closeout remain owned by `repo-worker-base` and are not part of this router.
