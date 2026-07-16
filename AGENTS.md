# AGENTS.md

## Repository purpose

This repository is the source of truth for agent-facing assets. It is an agent asset marketplace, not just a research ledger.

The primary durable output is market-consumable assets. Support surfaces such as provenance, catalogs, ledgers, reports, doctrine notes, indexes, and discovery records exist to support those assets. They do not substitute for them.

Codex plugin first; generated GPT-safe skill zips second.

The tracked agent mesh lives under `.agents/`. Root `AGENTS.md` is the local law node; `.agents/AGENTS.md` and `.agents/docs/mesh-policy.md` carry the repo-local mesh doctrine; docs-owned guidance lives under `docs/`; and generated `INDEX.md` files carry navigation only.

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

For ordinary worker execution, prefer a PR into `main`. The PR or direct-main commit is the publication surface that lets GPT verify changed files, diffs, and final main state. Local validation supports the return, but it does not substitute for GitHub-visible publication.

## Routing pointers

- `.agents/AGENTS.md` for tracked agent doctrine and local agent-facing deltas
- `.agents/docs/mesh-policy.md` for mesh-specific law
- `docs/AGENTS.md` for docs-owned guidance
- `tools/AGENTS.md` for generators and validators
- `codex-marketplace/AGENTS.md` for marketplace source/projection law
- `sources/AGENTS.md` for source custody
- `adapters/AGENTS.md` for adapter and overlay work
- `provenance/AGENTS.md` for provenance and trust evidence

## Maintenance responsibility

This file is the repository's primary worker doctrine. When repo conventions, marketplace structure, or publication rules change, this file must be updated to reflect the new expectations. Do not let this file become stale if agents are following patterns that contradict this document, either update the document or update the repo conventions to match.
