# AGENTS.md

Scope: `.agents/`

This scope covers the tracked agent-facing home for repo doctrine, local plugin
posture, work surfaces, and output/evidence conventions.

Defer to the repository root `AGENTS.md` for global repo doctrine and to
`docs/mesh-policy.md` for mesh-specific law.

Keep this scope short. It owns local agent-facing law, not directory navigation.
Navigation stays in generated `INDEX.md` files.

## Routing pointers

- `docs/mesh-policy.md` for the canonical mesh contract
- `docs/INDEX.md` for tracked docs under `.agents/docs/`
- `docs/guides/AGENTS.md` for stage-aware docs guidance
- `../docs/AGENTS.md` for docs-owned guidance when the work moves into `docs/`

## Review guidelines

- Flag any `.agents/` file that turns into product/source custody instead of
  agent-facing infrastructure.
- Flag any hand-maintained navigation inside `.agents/`; the tree should stay
  self-describing through generated indexes and scoped law.
- Flag mesh-law drift when a `.agents/` file starts repeating root doctrine
  instead of stating the local delta.
- Treat `.agents/playbooks/` and `.agents/runbooks/` as the canonical home for
  reusable workflow guidance. Use playbooks for scenario routing and runbooks
  for deterministic procedures.
- Treat `sources/first_party/**` as mutable source custody: edit the source
  directly when the skill or asset changes, then regenerate projections.
- Treat `sources/third_party/**` as immutable custody: do not edit it directly;
  express behavior changes through `adapters/**` and regenerate the projection.
