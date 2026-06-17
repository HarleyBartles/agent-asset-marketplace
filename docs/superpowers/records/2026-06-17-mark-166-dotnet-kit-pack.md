# MARK-166 dotnet-kit pack Implementation Record

**Issue:** MARK-166
**Branch:** `codex/mark-166-dotnet-kit-pack`
**Starting main SHA:** `dc51454384bf947c4d2a11974c1fb40fe9c52872`
**Implementation commit SHA:** `2a378b87a40192f7524de39fdfcaa2a4f94adba9`
**PR URL:** [https://github.com/HarleyBartles/agent-asset-marketplace/pull/103](https://github.com/HarleyBartles/agent-asset-marketplace/pull/103)
**Publication state:** Published on branch `codex/mark-166-dotnet-kit-pack` and tracked by PR #103 against `main`. The implementation commit is the feature-bearing commit that added the pack; this record documents the published marketplace state and the canonical regeneration that kept repo-resident zip artifacts aligned.

## Files changed

- `docs/superpowers/plans/2026-06-17-mark-166-dotnet-kit-pack.md`
- `docs/superpowers/records/2026-06-17-mark-166-dotnet-kit-pack.md`
- `tools/generate_repo_index.py`
- `tools/validate_marketplace.py`
- `repo-index/repo-index.json`
- `codex-marketplace/plugin-roots.json`
- `codex-marketplace/manifest.json`
- `.agents/plugins/marketplace.json`
- `codex-marketplace/plugins/dotnet-kit/.codex-plugin/plugin.json`
- `codex-marketplace/plugins/dotnet-kit/LICENSE`
- `codex-marketplace/plugins/dotnet-kit/README.md`
- `codex-marketplace/plugins/dotnet-kit/SOURCE.md`
- `codex-marketplace/plugins/dotnet-kit/assets/icon.svg`
- `codex-marketplace/plugins/dotnet-kit/references/bundle-manifest.json`
- `codex-marketplace/plugins/dotnet-kit/references/source-map.md`
- `codex-marketplace/plugins/dotnet-kit/skills/clean-architecture/SKILL.md`
- `codex-marketplace/plugins/dotnet-kit/skills/ddd/SKILL.md`
- `codex-marketplace/plugins/dotnet-kit/skills/ef-core/SKILL.md`
- `codex-marketplace/plugins/dotnet-kit/skills/modern-csharp/SKILL.md`
- `codex-marketplace/plugins/dotnet-kit/skills/testing/SKILL.md`
- `codex-marketplace/plugins/dotnet-kit/skills/vertical-slice/SKILL.md`
- `sources/first_party/skills/dotnet-kit/decisions.json`
- `sources/first_party/skills/dotnet-kit/decisions.md`
- `sources/first_party/skills/dotnet-kit/intake.json`
- `sources/third_party/dotnet-claude-kit/upstream/README.md`
- `sources/third_party/dotnet-claude-kit/upstream/LICENSE`
- `sources/third_party/dotnet-claude-kit/upstream/CLAUDE.md`
- `sources/third_party/dotnet-claude-kit/upstream/.mcp.json`
- `sources/third_party/dotnet-claude-kit/upstream/.claude-plugin/plugin.json`
- `sources/third_party/dotnet-claude-kit/upstream/.claude-plugin/marketplace.json`
- `sources/third_party/dotnet-claude-kit/upstream/skills/clean-architecture/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/ddd/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/ef-core/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/modern-csharp/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/testing/SKILL.md`
- `sources/third_party/dotnet-claude-kit/upstream/skills/vertical-slice/SKILL.md`
- `generated/skill-zips/dotnet-kit/clean-architecture/skill.zip`
- `generated/skill-zips/dotnet-kit/ddd/skill.zip`
- `generated/skill-zips/dotnet-kit/ef-core/skill.zip`
- `generated/skill-zips/dotnet-kit/modern-csharp/skill.zip`
- `generated/skill-zips/dotnet-kit/testing/skill.zip`
- `generated/skill-zips/dotnet-kit/vertical-slice/skill.zip`
- `generated/skill-zips/house-skills/codex-receipts-superpowers/skill.zip`
- `generated/skill-zips/house-skills/codex-repo-receipts/skill.zip`
- `generated/skill-zips/house-skills/house-skills/skill.zip`
- `generated/skill-zips/superpowers/codex-receipts-superpowers/skill.zip`
- `generated/skill-zips/registry.json`

## Scope and boundary

- Included: `modern-csharp`, `vertical-slice`, `clean-architecture`, `ddd`, `ef-core`, `testing`
- Excluded from this child: `tdd`, `verify`
- The pack uses a selective retained upstream snapshot. It does not import the full upstream repository.

## Authorship, license, and provenance

- The upstream technical guidance remains attributed to `codewithmukesh/dotnet-claude-kit` and is retained in `sources/third_party/dotnet-claude-kit/upstream/` under the upstream MIT license.
- The first-party contribution here is the selection boundary, the repackaging/adaptation work, the marketplace projection, and the repository-specific documentation around that transformation.
- `provenance/dotnet-claude-kit.md` carries the upstream intake and subset-selection record.
- `codex-marketplace/plugins/dotnet-kit/references/source-map.md` ties each adapted skill back to its retained source path and pack path.
- The adapted skill text is not presented as original first-party authorship of the upstream guidance. It is a Codex/GPT-compatible repack of third-party source with explicit provenance preserved.

## Generated-artifact alignment

The non-dotnet zip changes in this PR are kept because the authorized canonical regeneration lane was used to resolve stale generated artifacts that blocked the pack-scoped update path. These are repository-resident generated artifacts, not new MARK-166 semantic scope.

Changed zip paths from the canonical regeneration:

- `generated/skill-zips/house-skills/codex-receipts-superpowers/skill.zip`
- `generated/skill-zips/house-skills/codex-repo-receipts/skill.zip`
- `generated/skill-zips/house-skills/house-skills/skill.zip`
- `generated/skill-zips/superpowers/codex-receipts-superpowers/skill.zip`

## Validation

- `py -3 tools/update_skill_artifacts.py --pack dotnet-kit`
  - Result: failed because stale unselected generated artifacts for `house-skills/codex-receipts-superpowers` blocked the pack-scoped path.
- `py -3 tools/update_skill_artifacts.py --all`
  - Result: passed; regenerated the canonical zip corpus and registry, including the `dotnet-kit` pack and the unrelated stale artifacts above.
- `py -3 tools/validate_marketplace.py`
  - Result: passed.
- `py -3 tools/validate_repo_index.py`
  - Result: passed.
- `git diff --check`
  - Result: passed, with standard line-ending warnings only.

## Skipped checks

- `py -3 tools/update_skill_artifacts.py --check`
  - Skipped because the full canonical regeneration lane was used after the pack-scoped lane was blocked by stale unrelated artifacts.

## Deviations

- The pack-scoped regeneration attempt was blocked by unrelated stale generated artifacts already present in the repository.
- The resulting non-dotnet zip changes were retained as canonical artifact alignment from the full regeneration lane, not as a MARK-166 scope expansion.
