# Marketplace Worker Doctrine

This is the durable repo-local worker doctrine for `agent-asset-marketplace`.
Read it with the root [AGENTS.md](../AGENTS.md), the local mesh policy in
[mesh-policy.md](mesh-policy.md), and the repo-local marketplace registry in
[../plugins/marketplace.json](../plugins/marketplace.json).

## Execution model

- Edit first-party source files directly when first-party behavior changes.
- Treat third-party source custody as immutable; do not edit `sources/third_party/**` to change behavior. Use the relevant adapter under `adapters/**` and regenerate the projection instead.
- Edit third-party adapters, and plugin or manifest source surfaces, as the source of truth for projected behavior.
- Reproject the marketplace and generated outputs with the checked-in deterministic tooling.
- Reproject the repo-wide `INDEX.md` mesh with the checked-in deterministic
  tooling.
- Run the repo validators after regeneration and treat their results as the proof surface.
- Generated zips and projections are output surfaces, not hand-edit surfaces.
- If deterministic tooling is missing, unavailable, or broken, fix or create the tooling so source edits plus full regeneration can pass validation.
- Do not hand-edit generated outputs just to make the diff pass unless the task explicitly targets generated-output mechanics and preserves the source/tooling relationship.
- When source and projection diverge, repair the source or tooling first, then regenerate from durable source.
- Treat the index mesh as generated output unless a task explicitly calls for a
  handwritten exception.

## Durable proof

- Publication proof still matters: a pushed branch and PR are the normal repo completion surface.
- A clean diff is not enough if the generated projection or validator disagrees with the source.
- If a worker changes source custody, the matching projection and registry surfaces must be refreshed in the same execution path.
