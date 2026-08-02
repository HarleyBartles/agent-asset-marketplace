# Cross-repo extension hooks for skill refresh and index mesh

## Goal

Add optional repo-supplied extension hooks to `refreshing-installed-skills` and `generating-agent-mesh` so consumer repos can enforce extra local-skill policy and post-process the repo-wide `INDEX.md` mesh while still benefiting from the built-in validation and link checking.

## Plan

- [x] Inspect `refreshing-installed-skills` and `generating-agent-mesh` source, tests, and SKILL metadata.
- [x] Update `refreshing-installed-skills` to track the `marketplace-source` submodule HEAD in provenance `manifestSha`.
- [x] Update `refreshing-installed-skills` to record every `INSTALLED_BY_DEFAULT` plugin name in `syncedPlugins` in order.
- [x] Add `scripts/validate_local_skills_extra` hook invocation to `refreshing-installed-skills` after built-in local skill validation.
- [x] Add `scripts/generate_index_mesh_extra` hook invocation to `generating-agent-mesh` after writing `INDEX.md` files and before link validation.
- [x] Treat the generated `INDEX.md` content as the required prefix so repo-specific appended content is preserved.
- [x] Update `SKILL.md` and `agents/openai.yaml` for both skills.
- [x] Add/update tests for provenance, submodule SHA, hook invocation, hook failures, and post-processing behavior.
- [x] Run `py -3 -m pytest`, `py -3 tools/rebuild_marketplace.py`, and `py -3 tools/check_marketplace.py`.
- [x] Commit, push, open a draft PR, self-review, mark ready for review, and verify CI passes.
