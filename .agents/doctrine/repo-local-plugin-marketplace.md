# Repo-Local Plugin Marketplace

## Base posture

- Repo-local plugin marketplaces declare install posture for the repo.
- This repo uses `.agents/plugins/marketplace.json` as the repo-local Codex plugin marketplace surface.
- The manifest is generated from repo plugin inventory plus a small hand-maintained policy file.

## Policy rules

- Keep `repo.local_skills` and `src/plugin-definitions/marketplace-policy.json` `install_defaults` empty. This repository owns no repo-local skill copies and does not project Marketplace plugin skills.
- Ambient plugins remain available to agents through the runtime and remain catalog products; availability does not make them repository dependencies.
- The generated `.agents/plugins/marketplace.json` must keep marketplace products available without marking any `INSTALLED_BY_DEFAULT`.
- `.agents/skills/` is absent because this repository has no repo-local skills. Consumer plugin payloads are fetched by the harness and are never projected there.
