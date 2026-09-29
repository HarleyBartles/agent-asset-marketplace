# Codex Plugin Products

## Scope

`src/plugin-definitions/` owns product metadata and composition. `dist/plugins/` is the generated Codex install surface. Active products and catalog order are declared in `dist/plugin-roots.json` and validated against both marketplace manifests.

Skill source lives under `skills/<skill-id>/`; shared resources live under `shared/`. A plugin may include a skill without owning its source, and one canonical skill may be selected by multiple products. `contents.json` names skill sources and shared resource destinations. `references/bundle-manifest.json` in built plugin folders is generated compatibility metadata.

All marketplace source is first-party maintained, including open-source adaptations. Preserve upstream attribution, revisions, adaptations, and license requirements in provenance records and in every affected shipped product. Do not use origin to divide canonical source roots.

## Build and review

- Run `py -3 tools/run.py marketplace --apply` to assemble complete plugin packages and regenerate marketplace metadata.
- Run `py -3 tools/run.py marketplace --check` to verify package and manifest freshness without writing.
- Do not hand-edit generated plugin contents, bundle manifests, or indexes.
- Verify `.codex-plugin/plugin.json`, all referenced assets, skill closure, copied resources, and required license notices in each built package.
- Confirm `dist/plugins/` remains consumable from a Git checkout; Portfolio pins this path through the marketplace-source submodule.

Keep this doctrine aligned with `dist/plugin-roots.json` and [marketplace source doctrine](dist.md).
