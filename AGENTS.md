# AGENTS.md

## Repository purpose

This repository is the source of truth for agent-facing assets. It is an agent asset marketplace, not just a research ledger.

The primary durable output is market-consumable assets. Support surfaces such as provenance, catalogs, ledgers, reports, doctrine notes, indexes, and discovery records exist to support those assets. They do not substitute for them.

Codex plugin first; generated GPT-safe skill zips second.

The tracked agent mesh lives under `.agents/`. Root `AGENTS.md` is the local law node; `.agents/docs/mesh-policy.md` is the canonical mesh statement.

## Source-of-truth split

GitHub and the repository tree prove file state, landed assets, manifests, source snapshots, provenance notes, validation scripts, and playbooks.

Linear remains the control plane for issue state, worker state, review posture, and closeout decisions. Do not treat a Linear note, worker report, or chat summary as repo truth until the repository state or an explicit follow-up issue preserves the consequence.

Generated artifacts are downstream outputs unless the repo explicitly says otherwise.

## Publication proof for repo work

Local file changes are not repo completion. A worker must not return GREEN, claim repo work is done, or ask for issue closure from local paths, local commit hashes, local validation output, or an unpublished branch alone.

If repo files changed, the worker must publish the changes to GitHub before claiming completion. A valid repo-work return must include one of:

1. an open PR URL with branch name and full head SHA;
2. a verified direct-main commit SHA when direct-main work was explicitly authorized;
3. a concrete publication blocker explaining why the local changes could not be pushed or turned into a PR.

For ordinary worker execution, prefer a PR into `main`.

## Build and test commands

Canonical: `py -3 tools/run.py ci --check` and `py -3 tools/run.py marketplace --apply`.

For the full command matrix, see `.devin/rules/tools.md` after migration. For the implementation workflow, see `.agents/guides/implementing-guide.md`.

## Security considerations

Apply the `security-review` profile from `/unslop-profiles` to relevant work and review the security lenses in `.agents/guides/security-guide.md`.

## Routing pointers

- [Mesh policy](.agents/docs/mesh-policy.md)
- Scoped rule triggers live in `.devin/rules/*.md`; canonical repo-local doctrine lives in `.agents/doctrine/*.md`
- [Worker guidance](.agents/guides/repo-doctrine-guide.md)
- [Implementing workflow](.agents/guides/implementing-guide.md)
- [Worktree and scratch policy](docs/non-repo-locations-policy.md)

## Maintenance responsibility

This file is the repository's primary worker doctrine. When repo conventions, marketplace structure, or publication rules change, this file must be updated to reflect the new expectations.
