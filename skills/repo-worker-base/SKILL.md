---
name: repo-worker-base
description: Use when beginning or reviewing repo-backed work that needs portable worktree, source-custody, validation, or publication guidance, especially when a portable suggestion conflicts with repository policy.
metadata:
  source-id: repo-worker-base
  source-path: skills/repo-worker-base/SKILL.md
  provenance-name: Repo Worker Base first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Portable repo-worker routing, hygiene, and publication boundaries.
  use_when:
    - repo work needs worktree, branch, scratch, source, layout, validation, evidence, review, closeout, or publication guidance.
  do_not_use_when:
    - work is not repo-backed or a repository-specific policy alone owns the decision.
  use_with:
    - using-superpowers-plus
    - brainstorming
    - writing-plans
    - executing-plans
    - subagent-driven-development
    - requesting-code-review
license: MIT
---

# Repo Worker Base

This is the thin portable control plane for repo-backed work. It supplies repeatable hygiene and publication boundaries; the consuming repository owns its paths, commands, exclusions, CI, and exceptions through its local hygiene/layout policy and stage runbooks. Superpowers lane composition is owned by `using-superpowers-plus`; each stage skill owns its own baseline.

At the start of a new substantive slice, follow the repository's planning-artifact policy. If the repository explicitly adopts `completed-artifact-custody`, resolve the immutable subscription revision and read its definition and local certification before applying its obligations. If a human requests the lifecycle without a subscription, use the current capability only for the requested scope. Route to `completing-planning-artifacts` for the applicable process; the standard ID alone does not upgrade an older subscription. Retire eligible artifacts in that slice's first substantive commit only when the applicable requirements allow it. If the lifecycle is neither adopted nor requested, installed capability does not impose it; follow local policy.

## Read when

| Need                                                                           | Read                                                                              |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Repo work, worktree, branch, scratch, PR, or publication                       | [worktree-and-branch-policy.md](references/worktree-and-branch-policy.md)         |
| Running or changing a mutation script                                          | [mutation-script-safety.md](references/mutation-script-safety.md)                 |
| Creating an agent-facing script                                                | [script-entrypoint-contract.md](references/script-entrypoint-contract.md)         |
| Focused validation, hooked commit proof, Draft/Ready publication, or CI parity | [repository-validation-contract.md](references/repository-validation-contract.md) |
| Changing README, AGENTS.md, doctrine, docs, plans, or specifications           | [repository-layout.md](references/repository-layout.md)                           |
| Finding or creating a repository-local stage guide                             | [stage-guide-contract.md](references/stage-guide-contract.md)                     |

Read the consuming repository's local hygiene/layout policy whenever it exists. That local policy is the authority for repository-specific paths, commands, exclusions, CI, and exceptions; this skill does not replace it.

When workflow-composition guidance is available in the current agent runtime, use it for lane selection and stage routing. This worker capability does not require a consumer to subscribe to or install that guidance. Each invoked workflow skill owns its own baseline references.

## Supporting owners

- using-superpowers-plus owns session bootstrap and request classification.
- linear-issue-shaping owns the Linear control plane.
- verification-before-completion owns evidence-before-assertions.
- connector-safety owns sensitive or blocked connector writes.
- using-github-mcp owns GitHub proof.
- base-doctrine owns cross-project source-truth and doctrine routing.

Do not treat an installed skill, generated bundle, local cache, or worker report as authored source custody. Use the first-party source and the repository's declared local policy, then regenerate or install through their respective owners.
