---
name: playbook-composition
description: Use when adopting, authoring, routing, assessing, or updating repository concern-based playbooks.
metadata:
  source-id: playbook-composition
  source-path: skills/playbook-composition/SKILL.md
  provenance-name: Playbook Composition first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
license: MIT
---

# Playbook Composition

Use the [playbook composition standard](references/standard.md) when a repository explicitly adopts or asks to assess `playbook-composition`. Inspect its pinned subscription and certification. A playbook can stand alone; runbooks and doctrine/contracts are optional standards.

AOM offers optional editable [testing](assets/playbooks/testing.md), [security](assets/playbooks/security.md), and [code-review concern](assets/playbooks/code-review.md) guides, plus a [checker starter](scripts/check_playbooks.py). A repository may select any subset, author its own playbooks, adapt or replace these examples, or omit them all. Adoption is an agent-led repository change; the repository owns selected files and its compliance chain. The checker accepts selected document and route-source paths, then checks file/link integrity only. It does not determine whether a guide is a cross-stage concern, useful, or effectively routed through non-Markdown mechanisms.
