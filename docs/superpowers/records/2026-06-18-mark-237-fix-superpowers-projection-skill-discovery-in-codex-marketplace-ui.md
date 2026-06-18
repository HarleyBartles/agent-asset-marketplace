# MARK-237 Superpowers Projection Skill Discovery Record

**Issue:** MARK-237
**Branch:** `harleydbartles/mark-237-fix-superpowers-projection-skill-discovery-in-codex-marketplace-ui`
**Starting main SHA:** `7c1b9f2e93dcaa6a464dd81290414960a02b65a4`
**Implementation SHA:** `cdf490b0d61980109bea7f52aca5c46d924f4e79`
**Publication state:** Draft branch work in progress. This record captures the implementation commit separately from the later publication commit and PR evidence.

## Changed files

- `codex-marketplace/plugins/superpowers/.codex-plugin/plugin.json`
- `codex-marketplace/plugins/superpowers/PROJECTION.md`
- `codex-marketplace/plugins/superpowers/SOURCE.md`
- `codex-marketplace/plugins/superpowers/references/bundle-manifest.json`
- `codex-marketplace/plugins/superpowers/references/codex-marketplace-compatibility.md`
- `codex-marketplace/plugins/superpowers/references/provenance-map.json`
- `codex-marketplace/plugins/superpowers/skills/architecture-superpowers/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/codex-receipts-superpowers/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/codex-receipts-superpowers/agents/openai.yaml`
- `codex-marketplace/plugins/superpowers/skills/finishing-a-development-branch/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/github-superpowers/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/unslop-superpowers/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/using-superpowers/SKILL.md`
- `generated/skill-zips/registry.json`
- `generated/skill-zips/superpowers/architecture-superpowers/skill.zip`
- `generated/skill-zips/superpowers/codex-receipts-superpowers/skill.zip`
- `generated/skill-zips/superpowers/github-superpowers/skill.zip`
- `generated/skill-zips/superpowers/unslop-superpowers/skill.zip`
- `sources/first_party/skills/architecture-superpowers/SKILL.md`
- `sources/first_party/skills/github-superpowers/SKILL.md`
- `sources/first_party/skills/unslop-superpowers/SKILL.md`
- `tools/skill_zip_artifacts.py`
- `tools/validate_marketplace.py`

## What changed

- Normalized the surviving projected Superpowers skill files so the marketplace-facing `SKILL.md` files begin with standalone YAML frontmatter, have required `name` and `description` fields, and are BOM-free where the issue called out corruption.
- Removed `codex-receipts-superpowers` from the active Superpowers projection and deleted the projected directory so the install surface matches the intended surviving skill set.
- Updated the Superpowers bundle manifest, projection docs, provenance map, and marketplace compatibility note to reflect the reduced active projection.
- Added frontmatter validation helpers that reject BOM-prefixed or malformed `SKILL.md` headers for the Superpowers marketplace surface.
- Regenerated the skill zip corpus and `generated/skill-zips/registry.json`.
- Narrowed the mirror validation to compare canonical text bytes rather than flagging line-ending noise as projection drift.

## Validation

- `py -3 tools/update_skill_artifacts.py --all`
- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_repo_index.py`
- `py -3 tools/validate_generated_drift.py --base origin/main`
- `git diff --check`

## Results

- Marketplace validation passed after the projection cleanup and validation updates.
- Repo-index validation passed.
- Generated drift validation passed against `origin/main`.
- Diff whitespace checks passed.
- UI install proof was not run in this workspace; the remaining verification is for Harley to confirm the Codex marketplace UI lists the surviving Superpowers skills after install.

## Coordination note

- This branch coordinated the MARK-236 receipt-skill removal by dropping `codex-receipts-superpowers` from the active Superpowers projection.
- The canonical source snapshot for the removed skill remains in `sources/first_party/skills/codex-receipts-superpowers/` as historical custody, but it is no longer part of the installable Superpowers projection.
