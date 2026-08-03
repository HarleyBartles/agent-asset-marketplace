---
name: subagent-workspace
description: Use when resolving the off-repo scratch workspace for subagent tasks and placing short-lived subagent inputs and outputs.
metadata:
  source-id: subagent-workspace
  source-path: codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/SKILL.md
  provenance-name: Subagent Workspace first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when resolving the off-repo scratch workspace for subagent tasks and placing short-lived subagent inputs and outputs.
  use_when:
  - Use when a subagent task needs an off-repo scratch directory.
  - Use when materializing inputs (diffs, PR descriptions, issues) for subagents to read.
  - Use when routing subagent briefs, reports, review packages, or review logs to a disposable location.
  do_not_use_when:
  - Do not use for durable custody, canonical source, provenance, or publication proof.
  - Do not use when the artifact must survive beyond the current task.
  related_skills:
  - subagent-driven-development
  - iterative-review
  - selecting-a-subagent
  license: MIT
---

## Provenance

This skill is a first-party skill authored for this repository. It is not derived from an upstream snapshot.

# Subagent Workspace

Resolve the canonical off-repo scratch workspace and place short-lived subagent artifacts there.

## Workspace location

The workspace lives at `<main-checkout>/../_agent-scratch/<branch>/<plan-basename>/`, or on Windows `Z:\_agent-scratch\<branch>\<plan-basename>\`. It is outside the repo tree, never committed, and survives `git clean`.

## Scripts

- `scripts/sdd-workspace [PLAN_FILE]` — bash workspace resolver.
- `scripts/sdd-workspace.ps1 [PLAN_FILE]` — PowerShell workspace resolver.

Both print the absolute workspace directory and create it if it does not exist.

## Usage

For subagent-driven plans:

1. Run `scripts/sdd-workspace PLAN_FILE` and capture the printed path.
2. Write the task brief, subagent prompt, and report under that path.
3. When the task is done, the scratch directory can be discarded.

For iterative review:

1. Run `scripts/sdd-workspace` with no plan file.
2. Create an `iterative-review-<pr_number>` subdirectory.
3. Write `diff.txt`, `pr.json`, `review-log.md`, and fix diffs there.

## Rules

- Do not commit scratch files into the repo.
- Do not place canonical source or durable custody in scratch.
- If a scratch artifact ends up in the repo tree, remove it before committing.
