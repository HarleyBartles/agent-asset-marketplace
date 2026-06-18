# MARK-237 Superpowers Projection Skill Discovery Record

**Issue:** MARK-237
**Branch:** `harleydbartles/mark-237-fix-superpowers-projection-skill-discovery-in-codex-marketplace-ui`
**Starting main SHA:** `81b82b579a3ede48a914e61da0edc8fd01237ca6`
**Implementation SHA:** `c15e0030b4376063ec1b63c6436ca01b0f788f5e`
**Publication state:** Implementation committed; branch has been pushed and the draft PR is open.

## Changed files

- `adaptation-overlays/superpowers/finishing-a-development-branch/SKILL.md`
- `adaptation-overlays/superpowers/finishing-a-development-branch/agents/openai.yaml`
- `adaptation-overlays/superpowers/finishing-a-development-branch/overlay.yaml`
- `adaptation-overlays/superpowers/using-superpowers/SKILL.md`
- `adaptation-overlays/superpowers/using-superpowers/agents/openai.yaml`
- `adaptation-overlays/superpowers/using-superpowers/overlay.yaml`
- `codex-marketplace/plugins/superpowers/PROJECTION.md`
- `codex-marketplace/plugins/superpowers/references/bundle-manifest.json`
- `codex-marketplace/plugins/superpowers/references/codex-marketplace-compatibility.md`
- `codex-marketplace/plugins/superpowers/references/provenance-map.json`
- `codex-marketplace/plugins/superpowers/skills/finishing-a-development-branch/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/finishing-a-development-branch/agents/openai.yaml`
- `codex-marketplace/plugins/superpowers/skills/using-superpowers/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/using-superpowers/agents/openai.yaml`
- `docs/contracts/openai-agent-yaml.md`
- `docs/contracts/skill-frontmatter.md`
- `generated/skill-zips/registry.json`
- `generated/skill-zips/superpowers/finishing-a-development-branch/skill.zip`
- `generated/skill-zips/superpowers/using-superpowers/skill.zip`
- `tests/test_skill_overlay_materializer.py`
- `tests/test_validate_marketplace.py`
- `tools/materialize_superpowers_projection.py`
- `tools/skill_gpt_exports.py`
- `tools/skill_overlay_materializer.py`
- `tools/skill_zip_artifacts.py`
- `tools/update_skill_artifacts.py`
- `tools/validate_generated_drift.py`
- `tools/validate_marketplace.py`

## What changed

- Added a source-controlled adaptation overlay layer for `using-superpowers` and `finishing-a-development-branch`.
- Preserved the full behavior-bearing skill bodies in the overlay copies and normalized the `SKILL.md` frontmatter for Codex parsing.
- Added explicit contracts for skill frontmatter and `agents/openai.yaml` under `docs/contracts/`.
- Added a canonical Superpowers projection materializer that rebuilds `codex-marketplace/plugins/superpowers/skills/...` from custody plus overlays.
- Updated bundle/provenance metadata so adapted third-party entries carry explicit `adaptation_overlay_path` values.
- Tightened validation to parse YAML frontmatter, enforce required metadata shape, verify overlay contracts, and reconstruct the Superpowers projection from source plus overlay.
- Regenerated the canonical Superpowers skill zips and registry through the update tooling.

## Validation

- `py -3 -m unittest tests.test_skill_overlay_materializer`
- `py -3 -m unittest tests.test_validate_marketplace`
- `py -3 tools/materialize_superpowers_projection.py --check`
- `py -3 tools/update_skill_artifacts.py --all`
- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_repo_index.py`
- `py -3 tools/validate_generated_drift.py --base origin/main`
- `git diff --check`

## Results

- Overlay materialization tests passed.
- Marketplace validation passed with adapted Superpowers entries reconstructed from source plus overlay.
- Projection check passed for the materialized Superpowers skill tree.
- Generated skill zips and registry were refreshed successfully.
- Repo index validation passed.
- Generated drift validation passed against `origin/main`.
- Diff whitespace checks passed.
- The branch is ready for publication once pushed and wrapped in a draft PR.
