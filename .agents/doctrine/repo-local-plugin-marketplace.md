# Repo-Local Plugin Marketplace

## Base posture

- Repo-local plugin marketplaces declare install posture for the repo.
- This repo uses `.agents/plugins/marketplace.json` as the repo-local Codex plugin marketplace surface.
- The manifest is generated from repo plugin inventory plus a small hand-maintained policy file.

## Policy rules

- Keep `src/plugin-definitions/marketplace-policy.json` `install_defaults` empty. The Marketplace registry does not declare a local-skill inventory. Repository-authored skills, if any, belong under `.agents/skills/`; plugin skills remain in their installed plugin locations.
- Ambient plugins remain available to agents through the runtime and remain catalog products; availability does not make them repository dependencies.
- The generated `.agents/plugins/marketplace.json` must keep marketplace products available without marking any `INSTALLED_BY_DEFAULT`.
- `.agents/skills/` is absent because this repository currently has no repository-authored skills. Consumer plugin payloads are fetched by the harness and are never projected there.
