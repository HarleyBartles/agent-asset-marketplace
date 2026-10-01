---
name: repo-standards
description: Use when aligning repository operating-model standards, assessing adoption, or deciding which focused standard owns a requested change.
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

Agent Operating Model (AOM) publishes selectable standards. Availability is not adoption. A repository owns its implementation and self-certification after adopting a standard.

For assessment or adoption, read [adoption and certification](references/adoption-and-certification.md), then inspect `.agents/contracts/operating-standards.json` and the certification it names. The current choices are listed in [the standards catalog](references/standards-catalog.json). A missing subscription means non-adoption unless the user asks to adopt. Do not infer adoption from installed skills, existing files, or an ambient catalog.

For an explicit adoption task, follow the [agent-led adoption sequence](references/adoption-and-certification.md#adoption-workflow). Editable [subscription](assets/templates/operating-standards-v2.example.json), [root router](assets/templates/AGENTS.md.example), and [certification](assets/templates/standards-certification.md.example) examples are available. Treat example values as placeholders and replace them with repository facts before deployment.

Honor the source and immutable commit recorded by the repository. A v1 record identifies the historical deployed authority; inspect that pinned definition and deployed resources. Do not run current scaffolders as an upgrade. A v2 record identifies the source repository, full commit, definition path, and certification reference; retrieve that exact object, including when its standard is absent from today's catalog. The catalog presents current choices, not an update alarm. Upgrades are explicit reconciliation work.

After selecting the pinned authority, route to the smallest owner:

| Concern                                                  | Skill                      |
| -------------------------------------------------------- | -------------------------- |
| Subscription, certification, and broad routing           | `repo-standards`           |
| Runbook lifecycle stages and playbook concerns           | `repo-composition`         |
| Repository plugin dependencies and local authored skills | `repo-agent-assets`        |
| AGENTS.md routing                                        | `agents-routing`           |
| Agent doctrine and contracts                             | `agent-doctrine-contracts` |
| Tracked hook and hosted CI parity                        | `tracked-repo-hooks`       |
| Named command targets                                    | `command-bus`              |
| Focused checks and evidence                              | `repository-validation`    |

Use other focused standard skills named in the pinned definition or current catalog. Compose owners only when the requested change crosses their boundaries. `repo-shape` is a legacy v1 structural/deployment compatibility route; it does not define the obligations of every current standard.
