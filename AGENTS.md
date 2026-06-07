# AGENTS.md

## Repository purpose

This repository is the source of truth for agent-facing assets. It is an agent asset marketplace, not just a research ledger.

Durable assets in this repo may include:

- GPT-native skill sources under `gpt-skills/`;
- Codex marketplace metadata and plugin source shape under `codex-marketplace/`;
- repo-specific overlays under `repo-overlays/`;
- upstream source snapshots and references under `sources/`;
- provenance, license, attribution, and trust records under `provenance/`;
- worker playbooks, validation scripts, and other enablement assets where the repo conventions support them.

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

## Upstream drain rule

Upstream drains are not complete merely because an upstream was inventoried or classified.

The goal of third-party upstream drains is to legally re-vendor usable assets into this repository when rights and source shape allow it. A discovery surface or provenance note is allowed only when full re-vendoring is blocked, not useful, or explicitly deferred for a concrete reason.

If a drain identifies selected outcomes such as direct install/default or optional assets, first-party adaptation candidates, reference/catalog surfaces, overlap anchors, or high-signal source patterns, the worker must preserve the consequence in one of these ways:

1. copy the legally re-vendorable asset into the appropriate repo asset/source surface with provenance and license evidence;
2. update the appropriate marketplace, source, provenance, catalog, playbook, or adaptation surface in the repo;
3. create or link explicit Linear follow-up issues only for work that is genuinely out of scope or blocked for the current issue; or
4. revise the outcome to a true final pass or final park with evidence.

A provenance note can support marketplace preservation. It does not substitute for marketplace assets unless the selected outcome is truly reference-only or final-parked with evidence.

## No-dodge execution rule

Do not return analysis, inventory, candidate ledgers, discovery records, or plans as a substitute for doing the repo work. These are support evidence, not completion.

Do not use size, noise, breadth, repo-shape friction, or a request for smaller follow-up issues as a reason to avoid copying assets that can legally be re-vendored in the current issue.

A worker may return zero copied assets only when every scoped asset has a concrete rights, source, utility, validation, or scope blocker recorded. Otherwise the issue must end with repo-held assets and publication proof.

## Before changing files

Inspect current repo conventions before choosing paths. At minimum, check the relevant README, manifest, `sources/`, `provenance/`, and validation patterns for the work at hand.

Do not invent broad new structure when a small existing surface can carry the asset. Do not relabel upstream material as first-party. Preserve license, attribution, and source-map evidence for anything mirrored, adapted, or referenced.

## Validation

After repo changes, run the repo's current validation where available. The usual baseline is:

```bash
python3 tools/validate_marketplace.py || py -3 tools/validate_marketplace.py || python tools/validate_marketplace.py
git diff --check HEAD~1 HEAD
```

If a command is unavailable or the repo conventions have changed, record the actual command, output, and reason.

## Closeout

A valid return should report:

- files changed;
- assets copied or adapted into the repo, with paths;
- discovery/provenance-only outcomes and the concrete reason each was not re-vendored;
- the durable asset consequence preserved;
- provenance or license notes when relevant;
- validation output or a clear no-validation reason;
- publication proof: PR URL and head SHA, verified direct-main commit SHA, or concrete publication blocker;
- any explicit follow-up issues required to finish selected outcomes.

Passing validation is not the same as issue-goal conformance. Compare the final repo state and follow-up issues against the issue goal before claiming completion.
