# Worktree helpers, refreshing installed skills, and generating the index mesh

## Goal

Ship a consistent, skill-driven way for agents to create and remove Git worktrees and to refresh the agent-facing surfaces that depend on the marketplace plugin source. The result is three related assets in the `agent-asset-marketplace` repo:

1. A `refreshing-installed-skills` skill that installs/updates `.agents/skills/` from the plugin source and then regenerates the index mesh.
2. A `generating-index-mesh` skill that regenerates the repo-wide `INDEX.md` mesh on demand or as a CI gate.
3. An updated `using-git-worktrees` skill overlay that ships bundled `new-worktree` and `remove-worktree` scripts and automatically invokes `refreshing-installed-skills` when a worktree is created.

## Scope

- Create two first-party skills (`refreshing-installed-skills`, `generating-index-mesh`) in `sources/first_party/skills/`.
- Add a portable Python core plus Bash and PowerShell wrappers for each skill.
- Add bundled `new-worktree` / `remove-worktree` scripts to the `using-git-worktrees` skill via the Codex overlay adapter.
- Update the `using-git-worktrees` overlay text to point agents at the bundled scripts and the new refresh skills.
- Register the new skills in `repo-worker-pack` and `house-skills` via `codex-marketplace/custody-pack-registry.json`.
- Add tests for the new scripts and update generated marketplace surfaces.
- Supersedes the earlier per-repo `scripts/new-worktree.*` / `scripts/remove-worktree.*` plan committed in `add-worktree-helpers`.

## Non-goals

- Does not rewrite the third-party `using-git-worktrees` source. Changes are applied through the existing overlay adapter.
- Does not modify the per-repo `install_agent_skills.py` or `generate_index_mesh.py` commands. The new skills discover and invoke the existing repo-level commands.
- Does not change the `marketplace-source` submodule layout in consumer repos.
- Does not add repo-level `scripts/` wrappers in the source repo beyond the skill-provided entrypoints.

## Architecture

```
using-git-worktrees (third-party skill + overlay)
├── new-worktree.*  -> creates worktree, then runs refreshing-installed-skills
├── remove-worktree.* -> removes worktree
└── SKILL.md (overlay) -> tells agents to use bundled scripts and skills

refreshing-installed-skills (first-party skill)
├── refresh_installed_skills.py
│   ├── find plugin source (local or marketplace-source submodule)
│   ├── run install_agent_skills.py
│   └── run generating-index-mesh
├── wrappers (.sh, .ps1)
└── SKILL.md

generating-index-mesh (first-party skill)
├── generate_index_mesh.py
│   └── find and run the repo's generate_index_mesh.py
├── wrappers (.sh, .ps1)
└── SKILL.md
```

Both refresh skills and the worktree helpers are portable wrappers: they discover the repo-specific command and run it. The actual install/index logic stays in the repo-level `install_agent_skills.py` and `generate_index_mesh.py` files that already exist in each repo.

## Components

### `sources/first_party/skills/refreshing-installed-skills/`

- `SKILL.md` — trigger conditions, usage, and contract.
- `agents/openai.yaml` — Codex metadata.
- `scripts/refresh_installed_skills.py` — core script.
- `scripts/refresh-installed-skills.sh` — Bash wrapper.
- `scripts/refresh-installed-skills.ps1` — PowerShell wrapper.

**Behavior of `refresh_installed_skills.py`:**
1. Determine repo root via `git rev-parse --show-toplevel` and reject submodules.
2. Strip `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` from the environment for all subprocess calls.
3. Look for a repo-level override:
   - `scripts/refresh-installed-skills.*` (consumer or source)
   - `tools/refresh-installed-skills.*` (source repo only, transitional)
   If found, run it and exit.
4. Detect layout:
   - If `codex-marketplace/plugins` exists and `tools/install_agent_skills.py` exists, this is the marketplace source repo.
   - Else if `.agents/plugins/marketplace-source` exists (submodule or directory), treat as consumer repo; run `git submodule update --init --recursive .agents/plugins/marketplace-source`.
5. Run the discovered install command:
   - source repo: `tools/install_agent_skills.py`
   - consumer: `scripts/install_agent_skills.py` (falls back to `marketplace-source/tools/install_agent_skills.py` only if the consumer wrapper is missing, and copies the result from the source's `.agents/skills` to the repo's `.agents/skills` if necessary).
6. After install succeeds, invoke the `generating-index-mesh` skill's core script to regenerate the mesh.
7. If working-tree changes exist after both steps, `git add -A` and commit with message `chore: refresh installed skills and regenerate index mesh`.
8. Support `--check` mode that validates without writing.

### `sources/first_party/skills/generating-index-mesh/`

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/generate_index_mesh.py` — core script.
- `scripts/generate-index-mesh.sh`
- `scripts/generate-index-mesh.ps1`

**Behavior of `generate_index_mesh.py`:**
1. Determine repo root and strip `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`.
2. Look for a repo-level override `scripts/generate-index-mesh.*` or `tools/generate-index-mesh.*` and run it if present.
3. Detect layout:
   - source repo: `tools/generate_index_mesh.py`
   - consumer: `scripts/generate_index_mesh.py` (falls back to `marketplace-source/tools/generate_index_mesh.py`)
4. Run the discovered command.
5. Support `--check` mode.
6. Does **not** auto-commit; the caller (CI, pre-commit, or `refreshing-installed-skills`) decides whether to commit.

### `adapters/codex/superpowers-plus/using-git-worktrees/`

- `scripts/new_worktree.py` — core creation logic.
- `scripts/new-worktree.sh` / `scripts/new-worktree.ps1` — wrappers.
- `scripts/remove_worktree.py` — core removal logic.
- `scripts/remove-worktree.sh` / `scripts/remove-worktree.ps1` — wrappers.
- `overlay.yaml` — extended with `generated_files` entries for the above scripts and with line edits that teach agents to use them.

**`new_worktree.py` behavior:**
1. Determine repo root and strip `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`.
2. Compute canonical sibling worktree root: `<repo-root>/../_agent-worktrees/<repo-name>/<branch>`.
3. Run `git worktree add <path> -b <branch> [<base-ref>]`.
4. In the new worktree, run `refreshing-installed-skills`.
   - Try `.agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py` first.
   - If not present, run it from the plugin source (`codex-marketplace/plugins/repo-worker-pack/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py` or `marketplace-source/.../repo-worker-pack/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`).
   - If still not found, print a clear warning telling the agent to run `refreshing-installed-skills` manually.
5. Print `Worktree ready at <path>`.
6. Support `--no-skill-refresh` and `--base-ref` options.

**`remove_worktree.py` behavior:**
1. Resolve the worktree by branch name or path using `git worktree list --porcelain`.
2. Reject removal if the resolved path is the main repo root.
3. Run `git -C <path> submodule deinit --all -f` and ignore failures.
4. Run `git worktree remove <path> [--force]`.
5. Print `Removed worktree <path>`.

### `codex-marketplace/custody-pack-registry.json`

Add first-party entries for `refreshing-installed-skills` and `generating-index-mesh`:
- In `house-skills` bundle (mega-pack requirement).
- In `repo-worker-pack` bundle (worker-facing route).
- `content_mode`: `verbatim`.
- `canonical_source_path`: `sources/first_party/skills/<skill-name>`.
- `provenance_note`: first-party skill.

## Data flow

```
Agent invokes new-worktree
        |
        v
new_worktree.py creates worktree at canonical path
        |
        v
runs refreshing-installed-skills in the new worktree
        |
        +--> refresh_installed_skills.py
             |    install_agent_skills.py
             |    generate_index_mesh.py
             +--> commit if changed
        v
Worktree ready
```

For ongoing mesh maintenance:

```
CI / pre-commit / agent invokes generating-index-mesh
        |
        v
generate_index_mesh.py
        |
        +--> repo's generate_index_mesh.py
```

## Error handling

- If `git rev-parse --show-superproject-working-tree` returns a path, stop; do not run from a submodule.
- If the worktree path already exists, `new_worktree.py` reports the conflict and stops.
- If the install or mesh command fails, the wrapper exits non-zero and leaves the worktree for inspection.
- If `refreshing-installed-skills` cannot be found and `--no-skill-refresh` was not given, `new_worktree.py` warns and continues so the worktree is still usable.
- `remove_worktree.py` refuses to remove the main checkout.

## Testing

- `tests/test_worktree_scripts.py` — tests `new_worktree.py` and `remove_worktree.py` help/usage and a minimal temp-repo create/remove cycle.
- `tests/test_refresh_installed_skills.py` — tests discovery of source-vs-consumer layout, override behavior, and `--check` mode.
- `tests/test_generate_index_mesh.py` — tests discovery and override behavior.
- All tests use temporary Git repositories so they do not mutate the source repo.
- Full marketplace validation: `py -3 tools/rebuild_marketplace.py` and `py -3 tools/check_marketplace.py`.

## Skill text / overlay changes

- `refreshing-installed-skills/SKILL.md` describes triggering: new worktree, plugin source update, or stale `.agents/skills`.
- `generating-index-mesh/SKILL.md` describes triggering: mesh staleness, CI gate, or pre-commit.
- `using-git-worktrees` overlay adds:
  - A pointer after Step 1a to use bundled `new-worktree` / `remove-worktree` scripts when present.
  - A "Remove a worktree" section near the end.
  - Quick Reference rows for the bundled scripts and `refreshing-installed-skills`.
  - Instructions to invoke `refreshing-installed-skills` after creating a worktree (or rely on `new-worktree` to do it).

## Marketplace packaging

- First-party skills live in `sources/first_party/skills/refreshing-installed-skills` and `sources/first_party/skills/generating-index-mesh`.
- Register both in `house-skills` and `repo-worker-pack` entries in `codex-marketplace/custody-pack-registry.json`.
- Regenerate projections with `py -3 tools/rebuild_marketplace.py`.
- Validate with `py -3 tools/check_marketplace.py`.

## Validation

- `py -3 -m pytest tests/test_worktree_scripts.py tests/test_refresh_installed_skills.py tests/test_generate_index_mesh.py -v`
- `py -3 tools/rebuild_marketplace.py`
- `py -3 tools/check_marketplace.py`
- `git diff --check`

## Rollout and deferred work

- The new skills will be picked up by consumer repos when they refresh from `marketplace-source`.
- Consumer repos can later delete their `refresh_agent_surfaces.py` variants because `new-worktree` and `refreshing-installed-skills` replace that behavior.
- `scripts/install_agent_skills.py` and `scripts/generate_index_mesh.py` in consumer repos remain in place; they are the commands the new skills invoke.
