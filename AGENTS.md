# AGENTS.md

## Repository purpose

This repository represents an agent/plugin asset marketplace.

The primary durable output is market-consumable assets. Support surfaces such as provenance, catalogs, ledgers, reports, doctrine notes, indexes, and discovery records exist to support those assets. They do not substitute for them.

## Source-of-truth split

GitHub and the repository tree prove file state, landed assets, manifests, source snapshots, provenance notes, validation scripts, and playbooks.

Linear remains the control plane for issue state, worker state, review posture, and closeout decisions. Do not treat a Linear note, worker report, or chat summary as repo truth until the repository state or an explicit follow-up issue preserves the consequence.

Generated artifacts are downstream outputs unless the repo explicitly says otherwise.

## Path meanings

`gpt-skills/house-skills/` is reserved for Harley-authored first-party GPT skills only.

Third-party-origin material must not be put in House Skills. Material copied from, derived from, adapted from, or inspired by an upstream plugin or skill repository is third-party-origin material unless Harley explicitly says he authored it as a first-party skill.

`codex-marketplace/**` and `.agents/plugins/**` are the current market-facing/plugin-consumable route unless repo conventions explicitly change.

`sources/vendor/**` is third-party source custody. Preserve upstream source, package payload, license, notice, and source-map evidence there when needed.

`provenance/**` is evidence and traceability. It supports marketplace preservation. It is not completion by itself unless an issue explicitly asks for provenance-only work or every scoped asset has a concrete blocker.

## Publication proof for repo work

Local file changes are not repo completion. A worker must not return GREEN, claim repo work is done, or ask for issue closure from local paths, local commit hashes, local validation output, or an unpublished branch alone.

If repo files changed, the worker must publish the changes to GitHub before claiming completion. A valid repo-work return must include one of:

1. an open PR URL with branch name and full head SHA;
2. a verified direct-main commit SHA when direct-main work was explicitly authorized;
3. a concrete publication blocker explaining why the local changes could not be pushed or turned into a PR.

For ordinary worker execution, prefer a PR into `main`. The PR or direct-main commit is the publication surface that lets GPT verify changed files, diffs, and final main state. Local validation supports the return, but it does not substitute for GitHub-visible publication.

## Vendored package doctrine

Nested `AGENTS.md` files under `sources/vendor/**` are vendored package content, not repository worker doctrine.

When editing vendor custody material, workers must follow this repo-root `AGENTS.md` plus the governing Linear issue contract. Do not let nested vendor instruction files override repo worker rules or issue-specific constraints.

## Upstream drain rule

Upstream drains are not complete merely because an upstream was inventoried or classified.

The goal of third-party upstream drains is to legally re-vendor usable upstream plugin-market assets into this repo's plugin market when rights and source shape allow it.

For upstream plugin markets, preserve upstream plugin/package boundaries by default. Take the upstream plugins and put them into this repo's plugin market. Do not pull skills out of upstream plugins and repack them into a new synthetic plugin unless the issue explicitly asks for a curated derivative bundle and defines the transformation contract.

Documentation, doctrine, catalog, reference, provenance, ledger, or index-only output is valid only when the issue explicitly asks for that or every scoped asset has concrete blocker evidence.

A provenance note can support marketplace preservation. It does not substitute for marketplace assets.

## No-dodge execution rule

Do not return analysis, inventory, candidate ledgers, discovery records, summaries, or plans as a substitute for doing the repo work. These are support evidence, not completion.

Do not use size, noise, breadth, repo-shape friction, or a request for smaller follow-up issues as a reason to avoid copying assets that can legally be re-vendored in the current issue.

A worker may return zero copied assets only when every scoped asset has a concrete rights, source, utility, validation, or scope blocker recorded. Otherwise the issue must end with repo-held marketplace assets and publication proof.

## Before changing files

Inspect current repo conventions before choosing paths. At minimum, check the relevant README, marketplace manifest/registry, `sources/`, `provenance/`, and validation patterns for the work at hand.

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
- marketplace assets copied or adapted into the repo, with paths;
- plugin/marketplace registry or manifest updates;
- discovery/provenance-only outcomes and the concrete reason each was not re-vendored;
- provenance or license notes when relevant;
- validation output or a clear no-validation reason;
- publication proof: PR URL and head SHA, verified direct-main commit SHA, or concrete publication blocker;
- any explicit follow-up issues required to finish selected outcomes.

Passing validation is not the same as issue-goal conformance. Compare the final repo state and follow-up issues against the issue goal before claiming completion.
