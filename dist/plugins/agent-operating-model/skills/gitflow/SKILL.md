---
name: gitflow
description: Use when choosing or assessing feature, release, or hotfix branch routes, release promotion, or integration reconciliation in a repository that adopts Gitflow.
metadata:
  source-id: "gitflow"
  source-path: "skills/gitflow/SKILL.md"
  provenance-name: Gitflow Standard first-party skill
  source-category: first_party
  status: active
  owner: "Harley Bartles"
  scope: Gitflow branch routing, release promotion, and reconciliation decisions.
  use_when:
    - choosing a branch base, pull-request target, release route, or hotfix route in a repository that adopts Gitflow.
    - assessing or certifying an explicit Gitflow subscription.
  do_not_use_when:
    - the repository has not adopted Gitflow and the human has not requested its assessment or adoption.
    - a continuously delivered product has no need for parallel release lines and no explicit request to use Gitflow.
license: MIT
---

# Gitflow

Use this skill when a repository explicitly adopts or asks to assess the `gitflow` standard. First read its pinned subscription and certification. Then use the [standard](references/standard.md) for required invariants and the [workflow guide](references/adoption-and-workflow.md) for branch and release decisions. The standard is optional; branch names and a Marketplace catalog entry do not establish adoption.
