# MARK-137 Codex-Plugin-First GPT Export Audit

## Scope

This audit records the current posture for the agent asset marketplace after
reviewing the live repo surfaces for Codex plugin custody and GPT export
derivation.

## Inspected Surfaces

- `codex-marketplace/plugin-roots.json`
- `codex-marketplace/manifest.json`
- `.agents/plugins/marketplace.json`
- `gpt-overlays/manifest.json`
- `generated/skill-zips/registry.json`
- `provenance/house-skills.md`

## Current Posture

The repo is operating as `Codex plugin first; generated GPT-safe skill zips
second.`.

The canonical marketplace source custody remains the protected plugin roots
under `codex-marketplace/plugins/`:

- `house-skills`
- `adventures-pack`
- `unslop`
- `game-studio`
- `wild-bunch-project-pack`
- `superpowers`

The marketplace manifest, plugin-roots inventory, and runtime plugin export
surface are aligned to that six-root set.

The generated GPT export surface is derived from those plugin roots plus any
repo-owned overlay declared in `gpt-overlays/manifest.json`.

## GPT Export Classification

The current `superpowers` export posture is:

- `brainstorming` - `overlay`
- `executing-plans` - `overlay`
- `finishing-a-development-branch` - `overlay`
- `linear-superpowers` - `direct`
- `receiving-code-review` - `direct`
- `requesting-code-review` - `overlay`
- `subagent-driven-development` - `excluded`
- `systematic-debugging` - `direct`
- `test-driven-development` - `direct`
- `using-git-worktrees` - `excluded`
- `using-superpowers` - `overlay`
- `verification-before-completion` - `direct`
- `writing-plans` - `overlay`
- `writing-skills` - `overlay`

The generated registry currently records 102 artifacts and 3 exclusions, and
the overlay/exclusion split for `superpowers` matches the overlay manifest.

## Findings

- No mismatch was found between the active plugin inventory, the marketplace
  manifest surfaces, the overlay manifest, and the generated registry in the
  inspected posture slice.
- No source tree was treated as canonical GPT export source.
- No plugin-only surface was observed leaking into the GPT export model in the
  audited classification data.

## Repair Posture

No repair was required in this slice. If a future audit finds drift in a
specific plugin, skill, overlay, or generated export entry, that repair should
be split into the smallest follow-up issue that owns the affected surface.
