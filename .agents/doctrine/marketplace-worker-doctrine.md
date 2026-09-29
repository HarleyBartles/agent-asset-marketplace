# Marketplace Worker Doctrine

This is the durable repo-local worker doctrine for `agent-asset-marketplace`. Read it with the root [AGENTS.md](../AGENTS.md) and the repo-local marketplace registry in [../plugins/marketplace.json](../plugins/marketplace.json).

## Execution model

- Edit first-party source files directly when first-party behavior changes.
- Treat provenance records as evidence; edit canonical skill source under `skills/` and product composition under `src/plugin-definitions/` when behavior or membership changes.
- Record upstream attribution and license obligations honestly for every adapted open-source source.
- Reproject the marketplace and generated outputs with the checked-in deterministic tooling.
- Run the repo validators after regeneration and treat their results as the proof surface.
- Generated zips and marketplace bundles are output surfaces, not hand-edit surfaces.
- If deterministic tooling is missing, unavailable, or broken, fix or create the tooling so source edits plus full regeneration can pass validation.
- Do not hand-edit generated outputs just to make the diff pass unless the task explicitly targets generated-output mechanics and preserves the source/tooling relationship.
- When source and marketplace bundle diverge, repair the source or tooling first, then regenerate from durable source.

## Source-of-truth split

- GitHub and the repository tree prove file state, landed assets, manifests, provenance records, validators, and playbooks.
- Linear owns issue state, worker state, review posture, and closeout decisions. Treat comments and worker reports as context until repository state or a follow-up issue preserves their consequence.
- Generated artifacts are downstream outputs unless the repository explicitly declares otherwise.

## Publication proof

- Publication proof still matters: a pushed branch and PR are the normal repo completion surface.
- A clean diff is not enough if the generated bundle or validator disagrees with the source.
- If a worker changes source custody, the matching marketplace bundle and registry surfaces must be refreshed in the same execution path.
