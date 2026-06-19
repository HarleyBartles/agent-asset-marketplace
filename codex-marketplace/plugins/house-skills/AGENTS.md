# AGENTS.md

Scope: `codex-marketplace/plugins/house-skills/`

This scope covers the current first-party House Skills plugin root.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

## Review guidelines

- Flag mismatches between `.codex-plugin/plugin.json`, `README.md`, the bundle
  manifest, and the current skill-root inventory that would make the plugin
  non-installable or misleading.
- Flag missing or broken `skills/`, `assets/`, or bundle-reference files before
  minor copy edits.
- Flag any claim that this bundle is still a projection or mirror. The live
  projection/install surface is `codex-marketplace/plugins/house-skills/skills/`.
- Flag license or rights drift, especially if the bundle metadata or README
  starts implying broader rights than the repo evidence supports.

## Current-root workflow

- House Skills updates follow the unversioned current projection roots in `codex-marketplace/plugins/house-skills/skills/`.
- Historical package folders are folded into the current root and recorded in changelog and version-history notes.
- Update the live skill root and inventory surfaces first, then regenerate the bundle manifest and marketplace export.
- Keep `house-skills` valid while adding project-scoped bundles beside it.
- Project-scoped bundles, such as an Adventures pack, should point at explicit canonical source paths when they are meant to be projections.

## Maintenance responsibility

This file must stay aligned with the House Skills plugin structure and the repo's
first-party skill conventions. When House Skills workflow changes or new
project-scoped bundles are added, review and update this file to reflect current
expectations. The current-root workflow guidance must stay accurate—when that
workflow evolves, this file should be updated to prevent drift.
