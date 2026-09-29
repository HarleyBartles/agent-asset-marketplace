# AGENTS.md

## Repository purpose

This repository is the source of truth for agent-facing assets. It is an agent asset marketplace, not just a research ledger.

The primary durable output is market-consumable assets; support surfaces exist to help them, not substitute for them. Codex plugin first; generated GPT-safe skill zips second. Root `AGENTS.md` is the local law node; scoped `AGENTS.md` files route repository guidance.

## Source-of-truth split

GitHub and the repository tree prove file state, landed assets, manifests, source snapshots, provenance notes, validation scripts, and playbooks.

Linear remains the control plane for issue state, worker state, review posture, and closeout decisions. Do not treat a Linear note, worker report, or chat summary as repo truth until the repository state or an explicit follow-up issue preserves the consequence.

Generated artifacts are downstream outputs unless the repo explicitly says otherwise.

## Cross-repo standards alignment

This repo ships portable skills and standards resources to consumer repos. Ask: *Is this change a repo-local fix or a standard consumer repos will inherit?* If the latter, update the canonical source, not only a deployed or installed copy.

## Marketplace source and output

Canonical skill source lives under `skills/`; reusable authored material lives under `shared/`; and plugin metadata and skill/resource membership live under `src/plugin-definitions/`. All marketplace source is first-party maintained, including adapted open-source work. Keep upstream attribution and license obligations with that source and in every shipped plugin that needs them.

`src/marketplace/` implements definition validation and package assembly. `src/packages/` holds separately built Python package source. `dist/` is the committed distribution output: self-contained plugins under `dist/plugins/`, wheels under `dist/wheels/`, and generated product metadata in `dist/manifest.json` and `dist/plugin-roots.json`. Do not edit built plugin trees to change behavior.

Skill tests live with their source in each skill's `tests/` directory, including script tests and pressure cases. The build copies ship-ready test material with each installed skill; evaluator-only material and run results stay out of the package. Repository, build, shipped-plugin, and evaluation-harness suites have distinct homes under `tests/`. CI runs the first three suites as separate targets. `.agents/contracts/operating-standards.json` declares this repo's selected standards; `.agents/standards/` holds pinned checkers for hosted CI. `.agents/skills/` is the installed projection for the remaining Writing Pack subscription, not marketplace source. Inspect `src/plugin-definitions/` for product membership and the marketplace manifests for shipped products.

## Publication proof for repo work

If repo files changed, a valid repo-work return must include one of:

1. an open PR URL (GitHub supplies its branch and head identity);
2. a verified direct-main commit SHA when direct-main work was explicitly authorized;
3. a concrete publication blocker explaining why the local changes could not be pushed or turned into a PR.

For ordinary worker execution, prefer a PR into `main`. Resolve the needed publication and repository hygiene capabilities from the ambient skills available at runtime.

## Draft PR policy

Open pull requests as **draft**; keep them in draft while iterating and validating. Flip to ready for review only after self-review is complete and the latest committed tree has passed the pre-commit hook. Use `py -3 tools/run.py ci --check` only for an uncommitted verification, pipeline diagnosis, or explicit CI-parity work. See `.agents/runbooks/pr.md` and `.devin/rules/pr.md`.

## Build and test commands

Canonical: `py -3 tools/run.py ci --check`, `py -3 tools/run.py ci --apply`, and `py -3 tools/run.py marketplace --apply`. For a normal commit, stage the intended tree and let the tracked pre-commit hook materialize the staged snapshot, run `py -3 tools/run.py ci --apply`, and then run `py -3 tools/run.py ci --check --diagnostics` as the single complete local gate. Do not run `py -3 tools/run.py ci --check` immediately before a normal commit or immediately after a successful hooked commit; run it only for an uncommitted verification, when diagnosing the pipeline, or when explicitly proving CI parity. Install portable subagent profiles through the available ambient workflow capability; use `py -3 tools/run.py runtime-agents --apply --allow-shared-checkout` only for repo-local `.agents/agents/` profiles when working in a worktree; see `.agents/doctrine/non-repo-locations-policy.md`.

## Security considerations

Security review must apply the relevant profile and the repository lenses in `.agents/playbooks/security.md`; compose an available ambient workflow capability for the review.

## Routing pointers

- Scoped law lives in `.devin/rules/*.md` (including [PR workflow](.devin/rules/pr.md))
- [Worker guidance](.agents/playbooks/repo-doctrine.md) and [implementing workflow](.agents/runbooks/implementing.md)
- [Runbook stage routing](.agents/runbooks/AGENTS.md), [implementation runbook](.agents/runbooks/implementing.md), and [repo runbook policy](.agents/doctrine/repo-runbook-policy.md)
- [Playbook routing](.agents/playbooks/AGENTS.md), [testing playbook](.agents/playbooks/testing.md), and [security considerations](.agents/playbooks/security.md)
- [Testing instructions](.agents/playbooks/testing.md), [code style guidelines](.agents/playbooks/code-style.md), [review guidelines](.agents/runbooks/code-review.md), and [PR instructions](.agents/runbooks/pr.md)
- [Contributing](CONTRIBUTING.md) and [security considerations](.agents/playbooks/security.md)
- [Completed-artifact custody](.agents/doctrine/completed-artifacts.md) and the [ADR log](docs/decisions/README.md) for the in-flight, removal, and durable-decision boundary
- [Worktree and scratch policy](.agents/doctrine/non-repo-locations-policy.md)

## Maintenance responsibility

This file is the repository's primary worker doctrine. When repo conventions, marketplace structure, or publication rules change, this file must be updated to reflect the new expectations.
