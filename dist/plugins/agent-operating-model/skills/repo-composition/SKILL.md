---
name: repo-composition
description: Use when creating, changing, or assessing repository runbooks and playbooks under their explicitly adopted standards.
metadata:
  source-id: repo-composition
  source-path: skills/repo-composition/SKILL.md
  provenance-name: Repo Composition first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
license: MIT
---

# Repo Composition

First inspect the repository's pinned subscription and certification through `repo-standards`. Follow only standards the repository adopted, using their pinned definitions.

Runbooks are lifecycle-stage guides for work that happens in the repository. Playbooks are concern guides that compose capabilities, doctrine, and contracts. Keep those purposes distinct. Either standard can be adopted and implemented on its own. If both are adopted, runbooks generally route to the applicable playbooks so the stage guide composes the relevant concerns.

Neither standard mandates a starter inventory, fixed headings, empty placeholder sections, or a doctrine/contract store. A repository may select optional starter books, adapt them, author its own, or use none. Do not create a book just to satisfy a template.

Capabilities can refer to repository-authored skills by name and path, plugin skills by installed plugin-qualified name from `.agents/plugins`, or ambient skills by capability description. Do not claim an ambient skill will exist for someone cloning the repository. If the repository has adopted `agent-doctrine-contracts`, use its locations for doctrine and contracts; otherwise playbooks can carry the operating knowledge needed for the selected concern.

Keep routing useful and proportional: connect each lifecycle stage to the concerns that apply, rather than making every runbook reference every playbook. The `Applicability` text in a book corroborates scope and can rule out a mismatch; it does not trigger discovery. Route the book from a place an agent reads at the relevant work point.

For historical v1 consumers, follow the exact pinned definition and deployed resources. Current composition definitions do not silently replace existing requirements. The old structural and scaffolding assets remain covered by `repo-shape` compatibility guidance.
