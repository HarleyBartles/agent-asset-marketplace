# MARK-163 Wild Bunch DDD Aggregate Guidance Implementation Record

**Issue:** MARK-163
**Branch:** `codex/mark-163-update-wild-bunch-ddd-aggregate-guidance`
**Starting main SHA:** `4ae23edc1cab98f4a7dd00ae1ba4c8a0cf497eaf`
**Implementation SHA:** `beb32379c071fdc5c4e7fca2d0da4d9bc9b120d3`
**Final head SHA:** `0da48e8eee429da4e822bcd0dff06318b66a7752`
**PR URL:** [https://github.com/HarleyBartles/agent-asset-marketplace/pull/104](https://github.com/HarleyBartles/agent-asset-marketplace/pull/104)
**Plan:** [docs/superpowers/plans/2026-06-17-mark-163-wild-bunch-ddd-aggregate-guidance.md](/C:/WORK/codex-lanes/codex-b/agent-asset-marketplace/docs/superpowers/plans/2026-06-17-mark-163-wild-bunch-ddd-aggregate-guidance.md)
**Publication state:** Published on branch `codex/mark-163-update-wild-bunch-ddd-aggregate-guidance` and tracked by PR #104 against `main`. The execution record is a follow-up documentation commit that captures the feature commit and the receipt commit without rewriting the feature commit.

## Changed files

- `codex-marketplace/plugins/house-skills/skills/wild-bunch-domain-modeling/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/wild-bunch-domain-modeling/references/domain-model.md`
- `codex-marketplace/plugins/house-skills/skills/wild-bunch-dotnet-architecture/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/wild-bunch-dotnet-architecture/references/dotnet-architecture.md`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-domain-modeling/SKILL.md`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-domain-modeling/references/domain-model.md`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-dotnet-architecture/SKILL.md`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-dotnet-architecture/references/dotnet-architecture.md`
- `docs/superpowers/plans/2026-06-17-mark-163-wild-bunch-ddd-aggregate-guidance.md`
- `generated/skill-zips/dotnet-kit/clean-architecture/skill.zip`
- `generated/skill-zips/dotnet-kit/ddd/skill.zip`
- `generated/skill-zips/dotnet-kit/ef-core/skill.zip`
- `generated/skill-zips/dotnet-kit/modern-csharp/skill.zip`
- `generated/skill-zips/dotnet-kit/testing/skill.zip`
- `generated/skill-zips/dotnet-kit/vertical-slice/skill.zip`
- `generated/skill-zips/house-skills/wild-bunch-domain-modeling/skill.zip`
- `generated/skill-zips/house-skills/wild-bunch-dotnet-architecture/skill.zip`
- `generated/skill-zips/registry.json`
- `generated/skill-zips/wild-bunch-project-pack/wild-bunch-domain-modeling/skill.zip`
- `generated/skill-zips/wild-bunch-project-pack/wild-bunch-dotnet-architecture/skill.zip`

## What changed

- Updated the Wild Bunch domain-modeling and .NET architecture guidance in both the canonical House Skills source and the projected Wild Bunch project-pack copies.
- Replaced `aggregate route` language with DDD Aggregate Root terminology.
- Made `GameSession` the explicit live-play Aggregate Root.
- Required external live-play commands to mutate through `GameSession`.
- Allowed owned aggregate/component files under the root to own cohesive state, behavior, invariants, and lifecycle transitions.
- Explicitly rejected policy/coordinator/resolver-only extraction as aggregate-track completion.
- Regenerated the affected skill zip artifacts and the registry.

## Validation

- `py -3 tools/update_skill_artifacts.py --all`
- `py -3 tools/validate_marketplace.py`
- `rg -n "aggregate route" codex-marketplace/plugins/house-skills/skills/wild-bunch-domain-modeling codex-marketplace/plugins/house-skills/skills/wild-bunch-dotnet-architecture codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-domain-modeling codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-dotnet-architecture`
- `git diff --check`

## Notes

- The first targeted artifact regeneration attempt failed because `dotnet-kit/clean-architecture` was stale, so the full `--all` regeneration was used.
- The marketplace validator confirmed the project-pack copies had to match the canonical House Skills bytes exactly, so the mirrored Wild Bunch skill files were aligned directly from the canonical source.
- The PR is draft PR #104 against `main`.
- The follow-up documentation commit is `0da48e8eee429da4e822bcd0dff06318b66a7752`.
