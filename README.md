# agent-asset-marketplace

The canonical source of truth for agent-facing marketplace assets, starting with Codex plugins and portable skills.

## What this is

This repository publishes market-consumable assets for agents: plugins, skills, runbooks, and validation tooling. It is not a research ledger or a mirror of upstream docs. Every tracked file either ships to a marketplace or supports the traceability, provenance, and validation that lets a consumer trust what ships.

The primary outputs are:

- `codex-marketplace/plugins/` — Codex plugin source assets (the market-facing product).
- `.agents/skills/` — portable skills and runbooks that consumer repos can install.
- `provenance/` — source-custody, license, and attribution records for third-party assets.
- `tools/` — scripts that validate the marketplace inventory, plugin manifests, and repo mesh.

## How to use this repo

1. Clone the repository.
2. Make changes in the appropriate plugin or skill source tree.
3. Regenerate generated surfaces: `py -3 tools/run.py marketplace --apply`
4. Validate the tree: `py -3 tools/run.py ci --check`
5. Commit and push. Open a draft PR for ordinary work; direct-main pushes are only for authorized maintenance.

## How to navigate

- Start at [INDEX.md](INDEX.md) for the generated repo-wide navigation mesh.
- Read [AGENTS.md](AGENTS.md) for repository doctrine and worker expectations.
- Read [`.agents/doctrine/mesh-policy.md`](.agents/doctrine/mesh-policy.md) for the canonical mesh contract that governs how surfaces are organized and validated.

## Adding or updating assets

- Keep upstream plugin boundaries by default.
- Copy legally re-vendorable third-party assets into `codex-marketplace/plugins/<plugin>/` with provenance evidence.
- Update `codex-marketplace/plugin-roots.json` when the active plugin set changes.
- Run `py -3 tools/run.py marketplace --apply` to update `codex-marketplace/manifest.json`, `.agents/plugins/marketplace.json`, and bundle manifests.
- Run `py -3 tools/run.py ci --check` before claiming the tree is green.

## Trust and provenance

- Preserve license and attribution evidence for every imported asset.
- Do not store secrets or credentials in this repository.
- Treat provenance notes as supporting evidence, not as a substitute for shipping real marketplace assets.

## License

Assets in this repository are MIT licensed unless the individual file or provenance record states otherwise. See `provenance/` for third-party source-custody details and any per-asset exceptions.
