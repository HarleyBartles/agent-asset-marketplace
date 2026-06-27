# Source

This bundle packages the Wild Bunch first-party bridge/native skills as a Codex plugin overlay. Dependency plugins stay separate install surfaces and are not duplicated into this pack.

## Canonical basis

- First-party Wild Bunch and control-plane source custody: `sources/first_party/skills/`
- License posture: first-party custody for the active pack surface

## Source roots copied

- `references/bundle-manifest.json`
- `references/source-map.md`
- `references/provenance-map.json`
- `hooks/`
- Dependency topology is declared in `references/bundle-manifest.json`; it keeps the bridge skills thin and the dependency plugins separate.

## Marketplace adaptation

- Status: `projected`
- Plugin name: `wild-bunch-project-pack`
- Display name: `Wild Bunch Project Pack`
- Marketplace category normalized to `Productivity`
- Icon paths normalized to `./assets/icon.svg`
- The pack installs as a bridge/overlay surface and keeps dependency plugins separate.
- Browser verification stays in the browser-game bridge skill and installed tooling.

## Notes

The active projection inventory lives in `references/bundle-manifest.json` and `references/source-map.md`.
Pack-local Codex hooks live under `hooks/` and are advisory only; they do not become part of GPT skill exports.
