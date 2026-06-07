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

## Upstream drain rule

Upstream drains are not complete merely because an upstream was inventoried or classified.

If a drain identifies selected outcomes such as direct install/default or optional assets, first-party adaptation candidates, reference/catalog surfaces, overlap anchors, or high-signal source patterns, the worker must preserve the consequence in one of these ways:

1. update the appropriate marketplace, source, provenance, catalog, playbook, or adaptation surface in the repo;
2. create or link explicit Linear follow-up issues for bounded work that cannot fit in the current issue; or
3. revise the outcome to a true final pass or final park with evidence.

A provenance note can support marketplace preservation. It does not substitute for marketplace assets unless the selected outcome is truly reference-only or final-parked with evidence.

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
- the durable asset consequence preserved;
- provenance or license notes when relevant;
- validation output or a clear no-validation reason;
- any explicit follow-up issues required to finish selected outcomes.

Passing validation is not the same as issue-goal conformance. Compare the final repo state and follow-up issues against the issue goal before claiming completion.
