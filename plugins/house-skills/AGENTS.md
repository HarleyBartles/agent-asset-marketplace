# AGENTS.md

Scope: `plugins/house-skills/`

This scope covers the repo-local marketplace projection of the reviewed House
Skills bundle.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

## Review guidelines

- Flag mismatches between `.codex-plugin/plugin.json`, `README.md`, the bundle
  manifest, and the source ledger that would make the projection non-installable
  or misleading.
- Flag missing or broken `skills/`, `assets/`, or bundle-reference files before
  minor copy edits.
- Flag any claim that this bundle is the authoritative House Skills source;
  the source ledger under `sources/house-skills/` remains the source-of-truth
  record.
- Flag license or rights drift, especially if the bundle metadata or README
  starts implying broader rights than the repo evidence supports.

## Unversioned active-root bundle workflow

- House Skills bundle updates follow the unversioned active roots in `gpt-skills/house-skills/`, with current version recorded in each skill's frontmatter and version-history note.
- A new skill version line is historical until the bundle projection, registry, and source map point at the unversioned active root.
- Update the designated source and inventory surfaces first, then regenerate the bundle manifest and marketplace export.
- Keep `house-skills` valid while adding project-scoped bundles beside it.
- Bundles and plugins are projections over canonical House Skills sources, not new source-of-truth forks.
- Project-scoped bundles, such as an Adventures pack, should point at explicit canonical source paths and version metadata.
