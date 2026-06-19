# MARK-258 Implementation Record

**Goal:** validate the current projection contract and licensing provenance checks for marketplace skills and bundles without broadening the marketplace layout.

## Scope

- Hardened `agents/openai.yaml` validation so projected skills must carry structured provenance, interface, policy, and dependency metadata in the repo's current Codex pattern.
- Tightened skill frontmatter validation so structured `metadata` is enforced for projected skills instead of relying on loose top-level YAML keys.
- Added bundle-manifest `repo_index` validation to ensure provenance references and registry alignment are explicit.
- Updated the current ECC Superpowers source and projection metadata so the repo's validated shape remains consistent end-to-end.
- Regenerated the derived skill-zips and repository index artifacts through the normal tooling path.

## Files Changed

- `adaptation-overlays/superpowers-plus/verification-before-completion/SKILL.md`
- `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- `codex-marketplace/plugins/superpowers-plus/references/provenance-map.json`
- `codex-marketplace/plugins/superpowers-plus/skills/architecture-superpowers/SKILL.md`
- `codex-marketplace/plugins/superpowers-plus/skills/ecc-superpowers/agents/openai.yaml`
- `codex-marketplace/plugins/superpowers-plus/skills/verification-before-completion/SKILL.md`
- `docs/contracts/openai-agent-yaml.md`
- `docs/contracts/skill-frontmatter.md`
- `docs/superpowers/plans/2026-06-19-mark-258-validate-projection-contracts-and-licensing-provenance.md`
- `docs/superpowers/records/2026-06-19-mark-258-validate-projection-contracts-and-licensing-provenance.md`
- `generated/skill-zips/registry.json`
- `generated/skill-zips/superpowers-plus/architecture-superpowers/skill.zip`
- `generated/skill-zips/superpowers-plus/ecc-superpowers/skill.zip`
- `generated/skill-zips/superpowers-plus/verification-before-completion/skill.zip`
- `sources/first_party/skills/architecture-superpowers/SKILL.md`
- `sources/first_party/skills/ecc-superpowers/agents/openai.yaml`
- `tests/test_skill_overlay_materializer.py`
- `tests/test_validate_marketplace.py`
- `tools/skill_overlay_materializer.py`
- `tools/skill_zip_artifacts.py`
- `tools/validate_marketplace.py`

## Validation

- `py -3 -m pytest tests/test_skill_overlay_materializer.py tests/test_validate_marketplace.py`
- `py -3 tools/update_skill_artifacts.py --all`
- `py -3 tools/generate_marketplace.py`
- `py -3 tools/generate_repo_index.py`
- `py -3 tools/validate_marketplace.py`
- `py -3 tools/validate_repo_index.py`
- `py -3 tools/validate_skill_zips.py`
- `git diff --check`

## Generated Artifacts

The generated `skill.zip` and registry were refreshed through the standard tooling path after the metadata validation changes. They are derived projection outputs, not hand-authored source.

## Notes

- The repo currently does not contain a live `everything-codex-code` projection surface, so the implementation records that omission rather than inventing a new mirror target.

## Publication

- Branch: `harleydbartles/mark-258-validate-projection-contracts-and-licensing-provenance`
- Commit: `227b4658`
- Draft PR: [#133](https://github.com/HarleyBartles/agent-asset-marketplace/pull/133)
