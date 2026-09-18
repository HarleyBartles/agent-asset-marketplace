# Completing Plans Playbook

## When

Use after a plan is fully implemented and its durable decisions have current custody.

## Required skills

- `cleanup-custody`
- `verification-before-completion`

## Composition

Classify each artifact with `cleanup-custody`; keep it live while it governs implementation or review. Promote enduring architecture decisions to `adr/` and operating rules to doctrine, runbooks, or playbooks. Remove the exact tracked artifact, optionally retain a disposable non-evidentiary scratch copy, regenerate the mesh, and commit the resulting tree in the completing PR.

## Doctrine and contracts

- [Completed artifacts doctrine](../doctrine/completed-artifacts.md)

## Local commands and paths

Remove completed artifacts from `.agents/plans/`, `.agents/specs/`, or `.agents/roadmaps/` and run `py -3 tools/run.py mesh --apply` only after durable decisions are promoted. Disposable copies may live under `_agent-scratch/<repo-name>/completed/<artifact-type>/`.

## Evidence contract

No active guidance depends on the removed artifact, generated indexes are current, and Git history remains the immutable record.

## Prohibited combinations

Do not remove an in-flight plan or delete the only copy of a durable decision.

## Runbook routing

- [Pull request](../runbooks/pr.md)
