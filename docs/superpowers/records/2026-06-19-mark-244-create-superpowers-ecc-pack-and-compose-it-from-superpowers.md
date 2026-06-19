# MARK-244 Implementation Record

**Goal:** create the dedicated `superpowers-ecc` pack and add the thin `ecc-superpowers` router wrapper to `superpowers-plus`.

## Scope

- Added a new marketplace pack at `codex-marketplace/plugins/superpowers-ecc/`.
- Added the repo-authored `ecc-superpowers` source and projection wrapper.
- Updated `superpowers-plus` docs, provenance, and validation metadata so the wrapper is discoverable without absorbing the ECC workflow slice into Superpowers+.
- Updated the marketplace registry, repo index, generated skill-zips registry, and GPT export manifest classification so the new pack is wired through the current toolchain.

## Files Changed

- `adaptation-overlays/superpowers-plus/using-superpowers/SKILL.md`
- `codex-marketplace/README.md`
- `codex-marketplace/manifest.json`
- `codex-marketplace/plugin-roots.json`
- `codex-marketplace/plugins/AGENTS.md`
- `codex-marketplace/plugins/README.md`
- `codex-marketplace/plugins/superpowers-ecc/.codex-plugin/plugin.json`
- `codex-marketplace/plugins/superpowers-ecc/LICENSE`
- `codex-marketplace/plugins/superpowers-ecc/README.md`
- `codex-marketplace/plugins/superpowers-ecc/SOURCE.md`
- `codex-marketplace/plugins/superpowers-ecc/assets/icon.svg`
- `codex-marketplace/plugins/superpowers-ecc/references/bundle-manifest.json`
- `codex-marketplace/plugins/superpowers-ecc/references/source-map.md`
- `codex-marketplace/plugins/superpowers-ecc/skills/**`
- `codex-marketplace/plugins/superpowers-plus/PROJECTION.md`
- `codex-marketplace/plugins/superpowers-plus/SOURCE.md`
- `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- `codex-marketplace/plugins/superpowers-plus/references/codex-marketplace-compatibility.md`
- `codex-marketplace/plugins/superpowers-plus/references/provenance-map.json`
- `codex-marketplace/plugins/superpowers-plus/references/source-map.md`
- `codex-marketplace/plugins/superpowers-plus/skills/ecc-superpowers/SKILL.md`
- `codex-marketplace/plugins/superpowers-plus/skills/ecc-superpowers/agents/openai.yaml`
- `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers/SKILL.md`
- `docs/superpowers/plans/2026-06-19-mark-244-create-superpowers-ecc-pack-and-compose-it-from-superpowers.md`
- `gpt-overlays/manifest.json`
- `generated/skill-zips/registry.json`
- `provenance/superpowers-ecc.md`
- `provenance/superpowers-plus.md`
- `repo-index/repo-index.json`
- `sources/first_party/skills/ecc-superpowers/SKILL.md`
- `sources/first_party/skills/ecc-superpowers/agents/openai.yaml`
- `sources/third_party/ecc/upstream/LICENSE`
- `sources/third_party/ecc/upstream/source-custody.md`
- `tools/generate_repo_index.py`
- `tools/validate_marketplace.py`

## Validation

- `py -3 tools/update_skill_artifacts.py --all`
- `py -3 tools/generate_marketplace.py`
- `py -3 tools/generate_repo_index.py`
- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_repo_index.py`
- `py -3 tools/validate_skill_zips.py`
- `git diff --check`

## Licensing Repair

- Recovered the upstream ECC MIT license into `sources/third_party/ecc/upstream/LICENSE`.
- Corrected the `superpowers-ecc` plugin shell license to Harley Bartles while
  keeping upstream skill authorship and license evidence in the projected
  bundle metadata.
- Added explicit upstream author, source path, and license fields to the
  projected ECC skill headers and the Superpowers+ wrapper provenance records.

## Generated Artifacts

The generated `skill.zip` registry now includes `superpowers-ecc` as a first-class included pack alongside `superpowers-plus`. The new pack is a derived artifact surface built from the retained ECC source custody plus the dedicated marketplace projection; it is not hand-authored.

## Publication

- Branch: `harleydbartles/mark-244-create-superpowers-ecc-pack-and-compose-it-from-superpowers`
  - Commit: `6eff4fba0084f279676295494e13c9f2a53eb031`
  - Push: published to `origin/harleydbartles/mark-244-create-superpowers-ecc-pack-and-compose-it-from-superpowers`
- Draft PR: [#131](https://github.com/HarleyBartles/agent-asset-marketplace/pull/131)

## Notes

The first validation pass surfaced two toolchain gaps:

- `gpt-overlays/manifest.json` was missing a classification for `superpowers-plus/ecc-superpowers`.
- `tools/validate_marketplace.py` did not recognize the ECC tree URL used by the new pack manifest.

Both gaps were fixed in-repo and the validators now pass.
