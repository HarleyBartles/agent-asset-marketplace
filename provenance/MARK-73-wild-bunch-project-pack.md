# MARK-73 Wild Bunch Project Pack

This note records the discovery and provenance context for the
`wild-bunch-project-pack` plugin.

## Summary

- The pack is first-party Harley-authored Wild Bunch project guidance.
- It does not mutate `HarleyBartles/wild-bunch`.
- The pack references existing installable marketplace assets in this repo as
  patterns and guardrails:
  - `codex-marketplace/plugins/game-studio/`
  - `codex-marketplace/plugins/vercel/skills/agent-browser/SKILL.md`
  - `codex-marketplace/plugins/aspnet-core/`
  - `codex-marketplace/plugins/linear-pack/`
  - `gpt-skills/house-skills/connector-safety/SKILL.md`

## Installability status

- `game-studio`: installable local marketplace asset
- `agent-browser`: installable local skill
- `aspnet-core`: installable local marketplace asset
- `linear-pack`: installable local marketplace asset
- `connector-safety`: first-party House skill copied into the pack

## Not vendored

No third-party DDD/CQRS/.NET skill pack was vendored into v1. The project pack
was kept first-party because the repository already exposes the needed pattern
assets and the issue did not authorize redistributing an external skill pack.
