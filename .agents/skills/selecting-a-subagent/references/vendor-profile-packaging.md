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
- Marketplace regeneration already copies `assets/` into the projected plugin
  tree; extending `refreshing-installed-skills` to copy `assets/profiles/*.md` is
  a narrow addition rather than a new projection lane.

## Consumer search paths

A consumer worktree uses the same precedence documented in
`devin-desktop-profile.md`:

1. Repo-local override: `.devin/agents/`
2. Plugin-local (from installed packs): `.agents/agents/`
3. User-global: `~/.config/devin/agents/` (or `%APPDATA%\devin\agents\` on Windows)

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
