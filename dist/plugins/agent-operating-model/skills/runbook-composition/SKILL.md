---
name: runbook-composition
description: Use when adopting, authoring, routing, assessing, or updating repository lifecycle-stage runbooks.
metadata:
  source-id: runbook-composition
  source-path: skills/runbook-composition/SKILL.md
  provenance-name: Runbook Composition first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
license: MIT
---

# Runbook Composition

Use the [runbook composition standard](references/standard.md) when a repository explicitly adopts or asks to assess `runbook-composition`. Inspect the pinned subscription and certification first. Do not require playbooks, doctrine stores, or a fixed starter inventory unless the repository separately adopts those obligations.

AOM offers optional editable [design](assets/runbooks/design.md), [planning](assets/runbooks/planning.md), [implementation](assets/runbooks/implementing.md), [code-review stage](assets/runbooks/code-review.md), and [pull-request](assets/runbooks/pr.md) guides, plus a [checker starter](scripts/check_runbooks.py). A repository may take any subset, author its own guides, adapt or replace these examples, or omit them all. Adoption is an agent-led repository change; the repository owns selected files and its compliance chain. The checker accepts selected document and route-source paths, then checks file/link integrity only. It does not determine whether a guide is a lifecycle stage, useful, or effectively routed through non-Markdown mechanisms.
