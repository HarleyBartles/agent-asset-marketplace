---
name: repo-standards
description: Use when reading, creating, updating, or aligning repo standards; when determining repo shape, guide layout, workflow order, and handoff requirements.
metadata:
  source-id: repo-standards
  source-path: sources/first_party/skills/repo-standards/SKILL.md
  provenance-name: Repo Standards first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Cross-repo guide layout, invocation, workflow order, and handoff requirements.
  use_when:
  - Use when reading, creating, updating, or aligning any repo-local guide.
  - Use when determining the workflow order for repo-backed design, planning, implementation, or review.
  - Use when a repo's guide set is missing or misaligned with the standard.
  do_not_use_when:
  - Do not use for generic repo hygiene such as worktree, branch, source custody, or publication boundaries — defer to repo-worker-base for those.
  use_with:
  - repo-worker-base
  - inspecting-the-environment
  - work-mode-router
  - brainstorming
  - writing-plans
  - executing-plans
  - subagent-driven-development
  - requesting-code-review
license: MIT
---

# Repo Standards

This skill is the portable baseline for repo-local guides. It defines the cross-repo layout of root `AGENTS.md` headings, root pointer files, the `.agents/guides/` set, and the workflow order and Superpowers routing for each stage.

Each repo supplies a thin overlay at `.agents/docs/repo-guide-policy.md` that maps the standard to local files and records any exceptions. Local guides in `.agents/guides/` contain only repo-specific paths, commands, exclusions, CI, and exceptions.

## Read when

| Need | Read |
| --- | --- |
| How a repo's guides should be laid out | [references/repository-guide-standard.md](references/repository-guide-standard.md) |
| How a repo's shape should be checked/applied | [references/repository-shape-manifest.json](references/repository-shape-manifest.json) |
| The repo's local guide mappings | `.agents/docs/repo-guide-policy.md` in the consuming repo |
| Repo hygiene (worktree, branch, validation, publication) | `/repo-worker-base` |

## Composition contract

For any guide work, use:

```text
repo-standards -> repo-worker-base -> local guide -> selected Superpowers lane
```

`repo-standards` supplies the universal guide standard and workflow order. `repo-worker-base` supplies worktree, branch, validation, and publication boundaries. The local guide supplies repo-specific details. The Superpowers lane supplies stage technique.

## Required root surfaces

- Root `AGENTS.md` is a router with five core sections and a `## Routing pointers` table that resolves to tracked files.
- Root `REVIEW.md` is the review entry point. It contains first-class review concerns and routes to `.agents/guides/code-review-guide.md` for detailed review methodology and to `/requesting-code-review` for execution.
- Root `CONTRIBUTING.md` is the contributor entry point. It routes to the design, planning, implementation, and review guides and to the relevant repo-worker-pack and Superpowers skills. It may be a thin pointer to `.agents/guides/contributing-guide.md` when a repo keeps detailed guidance there.

## Router AGENTS.md model

Root `AGENTS.md` is a router, not an encyclopedia. It must contain exactly five core sections:

1. `## Repository purpose`
2. `## Source-of-truth split`
3. `## Build and test commands`
4. `## Routing pointers`
5. `## Maintenance responsibility`

The `## Routing pointers` section must contain resolvable markdown links to the scoped surfaces that own each canonical topic. Canonical topics are: Repository purpose, Source-of-truth split, Publication proof, Build and test commands, Testing instructions, Code style guidelines, Review guidelines, PR instructions, Contributing, Security considerations, Routing pointers, and Maintenance responsibility.

`repo-standards --check` validates that the five core sections exist, that every routing pointer resolves to a tracked file, and that the 12 canonical topics are covered by the union of root sections and routed targets.

## Marketplace.json schema

`.agents/plugins/marketplace.json` must contain a top-level `repo` object with a non-empty `repo.local_skill_prefixes` list. The `scaffold-marketplace-json` helper writes a minimal scaffold and migrates legacy top-level `local_skill_prefixes` and `local_skills` keys into `repo.local_skill_prefixes` while preserving `plugins`, `name`, and `interface` blocks.

## Core guide set

`.agents/guides/` must contain these stage guides:

- `design-guide.md`
- `planning-guide.md`
- `implementing-guide.md`
- `code-review-guide.md`

## Allowed additional guides

A repo may declare additional `<topic>-guide.md` files in `.agents/guides/`. Each must be a repo-specific overlay, not a repeat of portable doctrine. Examples:

- `security-guide.md`
- `testing-guide.md`
- `contributing-guide.md`
- `pr-guide.md`
- `code-style-guide.md`
- `marketplace-generation-guide.md`
- `skill-authoring-guide.md`

## Scaffold helpers

The `repo-standards` skill ships `scaffold-*` scripts for user-content surfaces that an agent must fill in. Run `scaffold-all` to create all missing scaffolds, or use the individual scripts:

- `scaffold-repo-guide-policy` for `.agents/docs/repo-guide-policy.md`
- `scaffold-guides` for `.agents/guides/*.md`
- `scaffold-review` for `REVIEW.md`
- `scaffold-contributing` for `CONTRIBUTING.md`
- `scaffold-ci-preflight` for `scripts/ci-preflight.sh` and `scripts/ci-preflight.ps1`
- `scaffold-gitignore` for the `.gitignore` sdd rule
- `scaffold-agents-md` for root `AGENTS.md` as a router
- `scaffold-marketplace-json` for `.agents/plugins/marketplace.json`

`ci-preflight` supports an optional extra hook: if `scripts/ci-preflight-extra.sh` or `scripts/ci-preflight-extra.ps1` exists, the preflight bundle invokes it with the same `--check` and `--changed-from` contract as the core preflight.

Repos may declare surface exceptions in the `## Exceptions` section of `.agents/docs/repo-guide-policy.md`.

## Workflow order

The canonical repo-backed workflow is:

```text
design -> planning -> implementing -> review
```

For each stage:

1. Invoke `/repo-standards` and read `references/repository-guide-standard.md`.
2. Invoke `/repo-worker-base` for worktree, branch, validation, and publication boundaries.
3. Read the repo's `.agents/docs/repo-guide-policy.md` to find the local guide path.
4. Read the repo-local guide for that stage.
5. Route to the correct Superpowers skill:
   - design -> `/brainstorming`
   - planning -> `/writing-plans`
   - implementation -> `/executing-plans` or `/subagent-driven-development`
   - review -> `/requesting-code-review`
