# Marketplace Source and Build

## Scope

Marketplace inputs are canonical skills under `skills/`, reusable resources under `shared/`, and product definitions under `plugin-definitions/`. Build implementation belongs in `src/marketplace/`; `tools/` exposes repository commands. `codex-marketplace/` is the committed generated catalog and plugin output because the Portfolio marketplace-source submodule consumes `codex-marketplace/plugins/`.

Every plugin is a self-contained installable package. Build copies selected skill source, ship-ready skill tests, and explicitly declared shared resources into each product. Runtime files resolve within their installed plugin. Repository and build tests are not shipped.

## Composition and build

Skill-to-plugin membership lives in `plugin-definitions/<plugin>/contents.json`; one skill may be selected by several plugins. Resource names resolve through the root resource catalog and each destination is relative to its packaged skill. Provenance and license notices follow the source into every package that includes it.

Run `py -3 tools/run.py marketplace --apply` to build and regenerate the marketplace. Run `py -3 tools/run.py marketplace --check` for a non-mutating freshness check. `py -3 tools/run.py ci --check` is the full repository gate; normal commits use the tracked hook.

`codex-marketplace/plugins/*/references/bundle-manifest.json`, product summaries, marketplace manifests, inventories, and indexes are generated or compatibility surfaces. They do not define source custody or membership.

## Review

- Confirm package metadata and local catalog paths resolve.
- Confirm all declared skills and resources are included and no source-tree path is needed at runtime.
- Confirm shared resources are copied to their declared package-relative destinations.
- Confirm required attribution, license text, and adaptation notes are present in every affected plugin.
- Confirm the build is deterministic and leaves `codex-marketplace/packages/` untouched.
