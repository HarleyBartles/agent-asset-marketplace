---
name: repo-shape
description: Use when maintaining a repository against its explicitly pinned v1 AOM structural or deployment coordinator.
metadata:
  source-id: repo-shape
  source-path: skills/repo-shape/SKILL.md
  provenance-name: Repo Shape first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Compatibility guidance for the legacy repository-shape coordinator and its deployed resources.
license: MIT
---

# Repo Shape

This skill documents the legacy v1 structural and deployment coordinator. It is not the authority for current AOM standard requirements. For adoption, assessment, and the pinned definition, start with `repo-standards`.

When a repository's v1 pin routes work here, read the exact historical definition and deployed resources named by that pin, then follow their compatibility contract. Do not infer new adoption from these resources, scaffolders, or files already present. Do not use a current scaffold to migrate a v1 consumer implicitly.

The following reference assets and scripts remain for existing v1 consumers. Their behavior is governed by the pinned v1 authority:

- [Repository shape standard](references/repository-shape-standard.md)
- [Repository shape manifest](references/repository-shape-manifest.json)
- [Runbook standard](references/repository-runbook-standard.md)
- [CI validation pipeline](references/ci-validation-pipeline.md)
- [Scratch workspace policy](references/scratch-workspace-policy.md)
- [Script contract validator](references/skill-script-contract-validator.md)
- [Vendor profile deployment](references/vendor-profile-deployment.md)

Current runbook and playbook semantics belong to `repo-composition` and the adopted pinned definitions. Current plugin subscription semantics belong to `repo-agent-assets`. A v1 repository continues to use its own recorded authority until it explicitly requests an upgrade.
