# Source

This bundle packages first-party Wild Bunch project guidance as a market-facing
Codex plugin.

## Canonical basis

- Issue: `MARK-73`
- Project target: `HarleyBartles/wild-bunch`
- License posture: first-party Harley-owned source

## Source roots inspected

- `codex-marketplace/plugins/game-studio/skills/game-studio/SKILL.md`
- `codex-marketplace/plugins/game-studio/skills/web-game-foundations/SKILL.md`
- `codex-marketplace/plugins/game-studio/skills/phaser-2d-game/SKILL.md`
- `codex-marketplace/plugins/game-studio/skills/game-ui-frontend/SKILL.md`
- `codex-marketplace/plugins/game-studio/skills/game-playtest/SKILL.md`
- `codex-marketplace/plugins/vercel/skills/agent-browser/SKILL.md`
- `codex-marketplace/plugins/aspnet-core/skills/aspnet-core/SKILL.md`
- `codex-marketplace/plugins/linear-pack/skills/linear-reference-architecture/SKILL.md`

## Market discovery result

The repository already contains installable reference surfaces for the
browser-game, browser-QA, .NET, and CQRS/architecture patterns needed for this
pack:

- `game-studio` and its browser-game specialist skills are installable local
  marketplace assets.
- `agent-browser` under the Vercel plugin is an installable local skill for
  browser verification.
- `aspnet-core` is an installable local plugin for .NET application guidance.
- `linear-pack` is an installable local plugin that includes a CQRS-oriented
  reference-architecture skill.

No third-party DDD/CQRS/.NET skill pack was vendored for v1 because the issue
only requires a project-scoped pack and the current marketplace already exposes
the needed installable patterns as references.

## Outcome

- Imported into this pack: `5`
- Skipped as out of scope: `0`
- Blocked: `0`

## Notes

The bundle keeps the project guidance in its own skill directories and records
the discovery result here so workers can inspect the same surface before they
touch `HarleyBartles/wild-bunch`.
