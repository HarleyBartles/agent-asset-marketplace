# Distributed assets

This repository authors skills under `skills/`, reusable assets under `shared/`, plugin composition under `src/plugin-definitions/`, and Python package source under `src/packages/`. The builder in `src/marketplace/` assembles each installable plugin from these sources.

`dist/` is the committed output that this repository distributes. `dist/plugins/<plugin>/` contains self-contained Codex plugins, including copies of their selected skills and ship-ready tests. `dist/wheels/` contains the built Python wheel used by the Markdown formatting skill. The generated `dist/plugin-roots.json` and `dist/manifest.json` describe the built inventory. Edit `src/plugin-definitions/catalog.json` to change the active catalog and `src/plugin-definitions/marketplace-policy.json` for the local marketplace policy.

Codex discovers the marketplace through `.agents/plugins/marketplace.json` at the repository root. Plugin source paths in that catalog lead into `dist/plugins/`. The repository's `.agents/skills/` tree is its installed operating mesh, refreshed from built plugins.

Run `py -3 tools/run.py marketplace --apply` to build the plugins and catalog, or `py -3 tools/run.py marketplace --check` to check tracked output. Build the Markdown wheel with `py -3 src/packages/mdformat-safe-link-labels/build_wheel.py`.
