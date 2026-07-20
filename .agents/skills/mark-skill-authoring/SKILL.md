---
name: mark-skill-authoring
description: Use when creating, reviewing, or refreshing a repository-local or marketplace skill and its authority record.
---

# Mark Skill Authoring

**REQUIRED SUB-SKILL:** Use `superpowers-plus:writing-skills` for skill authoring and review.

For creating a new skill, first read [local and marketplace custody](references/local-and-marketplace-custody.md). When applicable, read [source-grounded authoring](references/source-grounded-authoring.md). Choose custody and lane, then run `scripts/new-skill.sh` or `scripts/new-skill.ps1` before authoring files. When reviewing or refreshing an existing skill, inspect its existing custody and lane; do not run the scaffolder against an existing destination.

`references/` is operational guidance. `assets/authority/` is cold authority custody. Operational skill text has no inline citations by default.

Authority freshness is manual: a human reviews and records each authority refresh before operational guidance changes.
