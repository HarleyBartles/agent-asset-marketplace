# Marketplace Worker Doctrine

This is the durable repo-local worker doctrine for `agent-asset-marketplace`.
Read it with the root [AGENTS.md](../AGENTS.md), the local mesh policy in
[mesh-policy.md](mesh-policy.md), and the repo-local marketplace registry in
[../plugins/marketplace.json](../plugins/marketplace.json).

## Execution model

- Edit first-party source files directly when first-party behavior changes.
- Treat third-party source custody as immutable; do not edit the retained provenance record to change behavior. Update the canonical plugin source or bundle manifest and regenerate the plugin distribution instead.
- Edit canonical plugin or manifest source surfaces as the source of truth for bundled behavior.
- Reproject the marketplace and generated outputs with the checked-in deterministic tooling.
- Reproject the repo-wide `INDEX.md` mesh with the checked-in deterministic
  tooling.
- Run the repo validators after regeneration and treat their results as the proof surface.
- Generated zips and marketplace bundles are output surfaces, not hand-edit surfaces.
- If deterministic tooling is missing, unavailable, or broken, fix or create the tooling so source edits plus full regeneration can pass validation.
- Do not hand-edit generated outputs just to make the diff pass unless the task explicitly targets generated-output mechanics and preserves the source/tooling relationship.
- When source and marketplace bundle diverge, repair the source or tooling first, then regenerate from durable source.
- Treat the index mesh as generated output unless a task explicitly calls for a
  handwritten exception.

## Durable proof

- Publication proof still matters: a pushed branch and PR are the normal repo completion surface.
- A clean diff is not enough if the generated bundle or validator disagrees with the source.
- If a worker changes source custody, the matching marketplace bundle and registry surfaces must be refreshed in the same execution path.
