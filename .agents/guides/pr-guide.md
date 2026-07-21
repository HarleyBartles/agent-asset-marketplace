# PR Guide

Use this guide for pull-request workflow and publication proof in `agent-asset-marketplace`.

## Before you begin

- Read root [`AGENTS.md`](../../AGENTS.md) `## Publication proof for repo work`.
- Read [`tools/AGENTS.md`](../../tools/AGENTS.md) for validation commands.
- Invoke `/repo-worker-base`.

## When to use

- Preparing a branch for review.
- Creating or updating a PR.
- Providing publication proof for repo work.

## Repo-specific guidance

- Work in an isolated worktree on a task branch.
- Run the relevant validation before pushing:
  - Marketplace changes: `py -3 tools/rebuild_marketplace.py` then `py -3 tools/check_marketplace.py`.
  - Structural changes: `py -3 tools/generate_index_mesh.py`.
- Commit focused changes. Do not commit generated artifacts unless the generator produced them.
- Push the branch and open a PR into `main` unless direct-main work is explicitly authorized.
- A valid repo-work return must include one of:
  1. an open PR URL with branch name and full head SHA;
  2. a verified direct-main commit SHA;
  3. a concrete publication blocker.

## Routing to skills

- `/repo-worker-base` for worktree, branch, and publication boundaries.
- `/github-operations` for PR evidence and GitHub proof.
- `/verification-before-completion` before claiming the PR is green.
