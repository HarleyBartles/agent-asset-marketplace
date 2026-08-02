# Vendor and third-party profile packaging

## Canonical location

Third-party subagent `.md` profile assets live under `assets/profiles/` inside
an installable pack. For example:

```
codex-marketplace/plugins/<pack-name>/
  assets/
    profiles/
      reviewer.md
      implementer-strong.md
```

This reuses the existing pack-level `assets/` surface. Do not create a
dedicated top-level `vendor-profiles/` directory or split profile assets into a
parallel tree.

## Why `assets/profiles/`

- The Codex plugin pack already exposes pack-level assets (`assets/icon.svg`,
  `assets/app-icon.png`, etc.). Profiles are pack-level assets, not skill bodies.
- The Devin Desktop search paths already expect `.md` profile assets under
  `assets/` (see `devin-desktop-profile.md`).
- Marketplace regeneration already copies `assets/` into the bundled plugin
  tree; extending `refreshing-installed-skills` to copy `assets/profiles/*.md` is
  a narrow addition rather than a new marketplace bundle lane.

## Consumer search paths

A consumer worktree uses the same precedence documented in
`devin-desktop-profile.md`:

1. User/repo-local override: `.devin/agents/` (user-managed; never created by skills)
2. Plugin-local (from installed packs): `.agents/agents/` (the canonical marketplace surface)
3. User-global: `~/.config/devin/agents/` (or `%APPDATA%\devin\agents\` on Windows)

No skill should create or pressure a consumer to create `.devin/agents/`.
That directory is reserved for repo-local user-managed overrides.

## Installation behavior

A vendor profile is copied to `.agents/agents/` only when no file of the same
name already exists. If the consumer repo already has `reviewer.md`, the pack's
`reviewer.md` is not installed. This preserves repo-owned profiles while still
enabling fresh consumer worktrees to receive a pack's default set. Marketplace
profiles live in `.agents/agents/`; repo-local overrides live in `.devin/agents/`.

## Provenance

`refresh_installed_skills` records installed vendor profiles in
`.agents/skills/.provenance.json` under a `vendorProfiles` array. Each entry:

```json
{
  "plugin": "<pack-name>",
  "sourcePath": "codex-marketplace/plugins/<pack-name>/assets/profiles",
  "profiles": ["reviewer.md", "implementer-strong.md"]
}
```

This keeps the record of which plugin installed which profiles next to the
marketplace skill manifest, on the same surface as `syncedPlugins` and
`localSkills`.
