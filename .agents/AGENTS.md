# AGENTS.md

Scope: `.agents/`

This scope covers the tracked agent-facing home for repo doctrine, local plugin posture, work surfaces, and output/evidence conventions.

Defer to the repository root `AGENTS.md` for global repo doctrine and scoped `AGENTS.md` files for local routes.

Keep this scope short. It owns local agent-facing law and routing pointers.

## Routing pointers

- `.agents/doctrine/AGENTS.md` for doctrine routing
- `.agents/docs/AGENTS.md` for docs routing
- `runbooks/AGENTS.md` for stage-aware repository guidance
- `../.devin/rules/docs.md` for docs-owned guidance when the work moves into `.agents/docs/`

## Review guidelines

- Flag any `.agents/` file that turns into product/source custody instead of agent-facing infrastructure.
- Flag hand-maintained duplicate policy; scoped `AGENTS.md` files own local routes.
- Treat `dist/plugins/**` as the canonical product custody for plugins and skills; edit the source directly when the skill or asset changes.
