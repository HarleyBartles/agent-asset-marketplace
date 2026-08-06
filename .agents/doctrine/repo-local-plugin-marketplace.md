# Repo-Local Plugin Marketplace

## Base posture

- Repo-local plugin marketplaces declare install posture for the repo.
- This repo uses `.agents/plugins/marketplace.json` as the repo-local Codex
  plugin marketplace surface.
- The manifest is generated from repo plugin inventory plus a small
  hand-maintained policy file.

## Policy rules

- Do not hand-maintain copied `.agents/skills/` folders for plugin-supplied
  skills.
- Default-install the repo worker posture plugins:
  - `repo-worker-pack`
  - `superpowers-plus`
- Do not make `house-skills` a repo-local marketplace dependency or
  default-install.
- Use exclusions and overrides only for intentional local policy choices.
