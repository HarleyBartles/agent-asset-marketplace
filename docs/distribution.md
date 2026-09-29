# Distributed assets

This repository authors skills under `skills/`, reusable assets under `shared/`, plugin composition under `src/plugin-definitions/`, and Python package source under `src/packages/`. The builder in `src/marketplace/` assembles each installable plugin from these sources.

`dist/` is the committed output that this repository distributes. `dist/plugins/<plugin>/` contains self-contained Codex plugins, including copies of their selected skills and ship-ready tests. `dist/wheels/` contains the built Python wheel used by the Markdown formatting skill. The generated `dist/plugin-roots.json` and `dist/manifest.json` describe the built inventory. Edit `src/plugin-definitions/catalog.json` to change the active catalog and `src/plugin-definitions/marketplace-policy.json` for the local marketplace policy.

Codex discovers the marketplace through `.agents/plugins/marketplace.json` at the repository root. Plugin source paths in that catalog lead into `dist/plugins/`. The repository's `.agents/skills/` tree is its installed skill projection, refreshed from built plugins.

Run `py -3 tools/run.py marketplace --apply` to build the plugins and catalog, or `py -3 tools/run.py marketplace --check` to check tracked output. Build the Markdown wheel with `py -3 src/packages/mdformat-safe-link-labels/build_wheel.py`.

## Consumer source revisions

Consumers identify a published marketplace source by its immutable Git commit SHA. Use that exact SHA for the `marketplace-source` submodule gitlink and for marketplace standard `revision` entries. Plugin metadata `version` fields describe the plugin package and are not the source revision used to deploy hosted checkers. This repository does not currently publish semantic-version tags or GitHub Releases; the release handoff records the merged source SHA consumers should pin.

For migration from copied ambient plugins, installed-skill runner paths, or the retired index mesh, follow the [consumer runner migration guide](../skills/repo-shape/references/consumer-runner-migration.md). Keep the consumer's outer runner interface and remove ambient subscriptions only after the updated runner and hosted validation pass.
