# MARK-160 Repo Receipt Skill Implementation Record

**Issue:** MARK-160
**Branch:** `codex/mark-160-repo-receipt-skill`
**Starting main SHA:** `6cbec0a6ae1b8d1bd51b7388575974b455f7d245`
**Final head SHA:** `6cbec0a6ae1b8d1bd51b7388575974b455f7d245` (working tree only; no commit or PR published yet)
**PR URL:** not created

## Changed files

- `codex-marketplace/plugins/house-skills/skills/codex-repo-receipts/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/codex-repo-receipts/agents/openai.yaml`
- `codex-marketplace/plugins/repo-worker-base/skills/codex-repo-receipts/SKILL.md`
- `codex-marketplace/plugins/repo-worker-base/skills/codex-repo-receipts/agents/openai.yaml`
- `codex-marketplace/plugins/repo-worker-base/README.md`
- `codex-marketplace/plugins/repo-worker-base/SOURCE.md`
- `codex-marketplace/plugins/repo-worker-base/.codex-plugin/plugin.json`
- `codex-marketplace/plugins/repo-worker-base/LICENSE`
- `codex-marketplace/plugins/repo-worker-base/package.json`
- `codex-marketplace/plugins/repo-worker-base/assets/icon.svg`
- `codex-marketplace/plugins/repo-worker-base/skills/repo-worker-base/SKILL.md`
- `codex-marketplace/plugins/repo-worker-base/skills/repo-worker-base/agents/openai.yaml`
- `codex-marketplace/plugin-roots.json`
- `codex-marketplace/README.md`
- `codex-marketplace/manifest.json`
- `.agents/plugins/marketplace.json`
- `codex-marketplace/plugins/house-skills/README.md`
- `codex-marketplace/plugins/house-skills/skills/house-skills/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json`
- `codex-marketplace/plugins/house-skills/skills/house-skills/references/source-map.md`
- `provenance/house-skills.md`
- `provenance/repo-worker-base.md`
- `sources/first_party/skills/house-skills/decisions.md`
- `sources/first_party/skills/house-skills/decisions.json`
- `sources/first_party/skills/house-skills/intake.json`
- `codex-marketplace/plugins/superpowers/PROJECTION.md`
- `codex-marketplace/plugins/superpowers/SOURCE.md`
- `codex-marketplace/plugins/superpowers/references/bundle-manifest.json`
- `codex-marketplace/plugins/superpowers/references/provenance-map.json`
- `gpt-overlays/manifest.json`
- `generated/skill-zips/registry.json`
- `generated/skill-zips/house-skills/codex-repo-receipts/skill.zip`
- `generated/skill-zips/repo-worker-base/repo-worker-base/skill.zip`
- `generated/skill-zips/repo-worker-base/codex-repo-receipts/skill.zip`
- `generated/skill-zips/superpowers/codex-repo-receipts/skill.zip`
- `generated/skill-zips/house-skills/house-skills/skill.zip`
- `generated/skill-zips/house-skills/linear-superpowers/skill.zip`
- `generated/skill-zips/house-skills/connector-safety/skill.zip`
- `generated/skill-zips/superpowers/linear-superpowers/skill.zip`
- `generated/skill-zips/adventures-pack/connector-safety/skill.zip`
- `repo-index/README.md`
- `repo-index/repo-index.json`
- `tools/generate_repo_index.py`
- `tools/validate_marketplace.py`
- `tools/validate_repo_index.py`
- `tools/update_skill_artifacts.py` was not edited; it was used for regeneration

## What changed

- Canonical first-party source for `codex-repo-receipts` now lives in House Skills.
- The `repo-worker-base` plugin was brought into the working branch from the existing remote vendored surface.
- `codex-repo-receipts` was projected into `repo-worker-base` as the required delivery target.
- The optional `superpowers` projection kept the same House Skills source custody.
- The marketplace root inventory was updated to include `repo-worker-base`.
- A deterministic `repo-index` generator was added so the navigation mirror can be regenerated instead of hand-edited.

## Validation

- `py -3 tools/update_skill_artifacts.py --all`
- `py -3 tools/update_skill_artifacts.py --check`
- `py -3 tools/generate_repo_index.py`
- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_repo_index.py`
- `py -3 tools/validate_generated_drift.py --base origin/main`
- `git diff --check`

## Generator command

- `py -3 tools/generate_repo_index.py`

## Notes

- No repo index mirror was hand-edited after the generator was added.
- No Linear "Open in Codex Desktop" prompt template was edited.
- No commit, push, or PR was created in this turn.
