# AGENTS.md

## Repository purpose

This repository is the source of truth for agent-facing assets. It is an agent asset marketplace, not just a research ledger.

The primary durable output is market-consumable assets; support surfaces exist to help them, not substitute for them. Codex plugin first; generated GPT-safe skill zips second. The tracked agent mesh lives under `.agents/`. Root `AGENTS.md` is the local law node; `.agents/doctrine/mesh-policy.md` is the canonical mesh statement.
## Source-of-truth split

GitHub and the repository tree prove file state, landed assets, manifests, source snapshots, provenance notes, validation scripts, and playbooks.

Linear remains the control plane for issue state, worker state, review posture, and closeout decisions. Do not treat a Linear note, worker report, or chat summary as repo truth until the repository state or an explicit follow-up issue preserves the consequence.

Generated artifacts are downstream outputs unless the repo explicitly says otherwise.

## Cross-repo standards alignment
This repo ships portable skills and runbooks to consumer repos under `.agents/skills/`. Ask: *Is this change a repo-local fix or a standard consumer repos will inherit?* If the latter, update the source skill or reference, not only the installed copy.
## Vendored asset source and inspection

The canonical vendored marketplace assets live under `codex-marketplace/plugins/`. The active inventory is in `codex-marketplace/plugin-roots.json`, the aggregate Codex manifest is `codex-marketplace/manifest.json`, and the bundled skills for each plugin are declared in that plugin's `references/bundle-manifest.json` with their canonical source trees under that plugin's `skills/` directory.

Do not treat `.agents/skills/` as additional or duplicate vendored assets. Those are installed copies from the plugins this repo consumes for its own operation (currently `repo-worker-pack`, `superpowers-plus`, and `mcp-usage-pack`). They are downstream of the canonical plugin source. To see what this repo actually offers, inspect the bundle manifests or read the marketplace inventory in `codex-marketplace/README.md`.
## Publication proof for repo work

Local file changes are not repo completion. A worker must not return GREEN, claim repo work is done, or ask for issue closure from local paths, local commit hashes, local validation output, or an unpublished branch alone.

If repo files changed, the worker must publish the changes to GitHub before claiming completion. A valid repo-work return must include one of:

1. an open PR URL with branch name and full head SHA;
2. a verified direct-main commit SHA when direct-main work was explicitly authorized;
3. a concrete publication blocker explaining why the local changes could not be pushed or turned into a PR.

For ordinary worker execution, prefer a PR into `main`.
## Draft PR policy
Open pull requests as **draft**; keep them in draft while iterating and validating. Flip to ready for review only after self-review is complete and the latest committed tree has passed the pre-commit hook. Use `py -3 tools/run.py ci --check` only for an uncommitted verification, pipeline diagnosis, or explicit CI-parity work. See `.agents/runbooks/pr.md` and `.devin/rules/pr.md`.
## Build and test commands

Canonical: `py -3 tools/run.py ci --check`, `py -3 tools/run.py ci --apply`, and `py -3 tools/run.py marketplace --apply`. For a normal commit, stage the intended tree and let the tracked pre-commit hook materialize the staged snapshot, run `py -3 tools/run.py ci --apply`, and then run `py -3 tools/run.py ci --check --diagnostics` as the single complete local gate. Do not run `py -3 tools/run.py ci --check` immediately before a normal commit or immediately after a successful hooked commit; run it only for an uncommitted verification, when diagnosing the pipeline, or when explicitly proving CI parity. Use `py -3 .agents/skills/selecting-a-subagent/scripts/install_profiles.py --apply` to install portable subagent profiles to the user-global agents directory; use `py -3 tools/run.py runtime-agents --apply --allow-shared-checkout` only for repo-local `.agents/agents/` profiles when working in a worktree; see `.agents/doctrine/non-repo-locations-policy.md`.
## Security considerations

Apply the `security-review` profile from `/unslop-profiles` to relevant work and review the security lenses in `.agents/runbooks/security.md`.
## Routing pointers

- [Mesh policy](.agents/doctrine/mesh-policy.md)
- Scoped law lives in `.devin/rules/*.md` (including [PR workflow](.devin/rules/pr.md))
- [Worker guidance](.agents/runbooks/repo-doctrine.md)
- [Implementing workflow](.agents/runbooks/implementing.md)
- [Runbook stage routing](.agents/runbooks/AGENTS.md), [repo runbook policy](.agents/doctrine/repo-runbook-policy.md), and [completing plans](.agents/runbooks/completing-plans.md)
- [Completed plans doctrine](.agents/doctrine/completed-plans.md) and [completed plans rule](.devin/rules/completed-plans.md) for the in-flight vs completed boundary
- [Worktree and scratch policy](.agents/doctrine/non-repo-locations-policy.md)

## Maintenance responsibility

This file is the repository's primary worker doctrine. When repo conventions, marketplace structure, or publication rules change, this file must be updated to reflect the new expectations.
