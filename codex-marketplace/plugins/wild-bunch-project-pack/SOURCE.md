# Source

This bundle packages first-party Wild Bunch project guidance plus bundled
copies of the marketplace skills the project pack needs as a market-facing
Codex plugin.

## Canonical basis

- Issue: `MARK-73`
- Project target: `HarleyBartles/wild-bunch`
- License posture: first-party Harley-owned source plus copied marketplace
  skills preserved under their source plugin licenses

## Source roots inspected

- `codex-marketplace/plugins/game-studio/skills/game-studio/SKILL.md`
- `codex-marketplace/plugins/game-studio/skills/web-game-foundations/SKILL.md`
- `codex-marketplace/plugins/game-studio/skills/phaser-2d-game/SKILL.md`
- `codex-marketplace/plugins/game-studio/skills/game-ui-frontend/SKILL.md`
- `codex-marketplace/plugins/game-studio/skills/game-playtest/SKILL.md`
- `codex-marketplace/plugins/game-studio/skills/sprite-pipeline/SKILL.md`
- `codex-marketplace/plugins/game-studio/references/*.md`
- `codex-marketplace/plugins/vercel/skills/agent-browser/SKILL.md`
- `codex-marketplace/plugins/aspnet-core/skills/aspnet-core/SKILL.md`
- `codex-marketplace/plugins/linear-pack/skills/linear-reference-architecture/SKILL.md`
- `gpt-skills/house-skills/connector-safety/SKILL.md`

## Market discovery result

The repository already contains installable reference surfaces for the
browser-game, browser-QA, .NET, and CQRS/architecture patterns needed for this
pack. Those source assets were copied into the Wild Bunch pack so installation
does not depend on another plugin being present:

- `game-studio` and its browser-game specialist skills are installable local
  marketplace assets and are now copied into this bundle.
- `agent-browser` under the Vercel plugin is an installable local skill for
  browser verification and is now copied into this bundle.
- `aspnet-core` is an installable local plugin for .NET application guidance
  and is now copied into this bundle.
- `linear-pack` is an installable local plugin that includes a CQRS-oriented
  reference-architecture skill and is now copied into this bundle.
- `connector-safety` is a first-party House skill and is now copied into this
  bundle as the shared connector/tool safety component.

No third-party DDD/CQRS/.NET skill pack was vendored for v1 because the issue
only requires a project-scoped pack and the current marketplace already exposes
the needed installable patterns as references. The current version bundled the
selected marketplace skills directly instead of depending on those packs at
runtime.

## Outcome

- First-party skills: `6`
- Copied marketplace skills: `9`
- Skipped as out of scope: `0`
- Blocked: `0`

## Notes

The bundle keeps the project guidance in its own skill directories and records
the copied-vs-first-party split in `references/provenance-map.md` so workers
can inspect the same surface before they touch `HarleyBartles/wild-bunch`.
