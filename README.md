# agent-asset-marketplace

A source-first marketplace of first-party maintained agent skills and Codex plugins, written by Harley Bartles to solve specific problems and workflows.

## What this is

This repository is the source of truth for agent skills and plugins. Skills are organized as a marketplace so agents can use them across projects and tools. This checkout itself uses ambient plugins and does not install marketplace skill copies.

You are welcome to browse or use anything here, but these skills were built for my purposes, not as a general-purpose product or a guaranteed fit for anyone else.

## What's inside

- `skills/` — canonical skill source, independent of plugin membership.
- `shared/` — reusable references and assets copied into built skills.
- `src/plugin-definitions/` — plugin metadata and declared skill/resource composition.
- `src/marketplace/` — definition validation and deterministic plugin build implementation.
- `src/packages/` — source for separately built Python packages.
- `dist/plugins/` — generated, self-contained installable Codex plugins.
- `dist/wheels/` — built Python wheels distributed by this repository.
- `.agents/plugins/marketplace.json` — the available plugin catalog; this repo declares no skill subscriptions, so `.agents/skills/` is absent.
- `docs/decisions/` — architecture decision records.
- `tests/` — named repository, build, shipping, and evaluation-harness suites; skill tests stay with their source.

## How to use

Plugins are the installable units. Their packages contain complete copies of selected skills and shared resources; they do not own canonical skill source. Adapted open-source work remains first-party maintained source with honest attribution and license notices. Use `py -3 tools/run.py marketplace --apply` to build packages and `py -3 tools/run.py marketplace --check` to verify the generated output.

Skill tests live under each canonical `skills/<skill-id>/tests/` tree. The build copies ship-ready tests into every plugin that carries that skill. Run a changed skill's tests directly; the commit and PR gate runs the named `tests/build/`, `tests/repository/`, and `tests/shipping/` suites. See [test suite ownership](tests/README.md).

## License

This repository is released under the MIT License. See [LICENSE](LICENSE) for the full text. I am sharing the code in case it is useful, but there is no warranty, support, or guarantee that any skill here will work for your situation.
