# Worktree helpers, refreshing installed skills, and generating the index mesh

## Goal

Ship a consistent, skill-driven way for agents to create and remove Git worktrees and to refresh the agent-facing surfaces that depend on the marketplace plugin source. The result is three related assets in the `agent-asset-marketplace` repo:

1. A `refreshing-installed-skills` skill that installs/updates `.agents/skills/` from the plugin source and then regenerates the index mesh.
2. A `generating-index-mesh` skill that regenerates the repo-wide `INDEX.md` mesh on demand or as a CI gate.
3. An updated `using-git-worktrees` skill overlay that ships bundled `new-worktree` and `remove-worktree` scripts. `new-worktree` automatically invokes `refreshing-installed-skills` after creating the worktree.

This design supersedes the earlier per-repo `scripts/new-worktree.*` / `scripts/remove-worktree.*` plan. The stale plan file `2026-07-24-add-worktree-scripts-and-overlay.md` and the failing test `tests/test_worktree_scripts.py` will be removed or rewritten during implementation.

## Scope

- Create two first-party skills (`refreshing-installed-skills`, `generating-index-mesh`) in `sources/first_party/skills/`.
- Add a portable Python core plus Bash and PowerShell wrappers for each skill.
- Add bundled `new-worktree` / `remove-worktree` scripts to the `using-git-worktrees` skill via the Codex overlay adapter.
- Update the `using-git-worktrees` overlay text to point agents at the bundled scripts and the new refresh skills.
- Register the new skills in `repo-worker-pack` and `house-skills` via `codex-marketplace/custody-pack-registry.json`.
- Add tests for the new scripts and update generated marketplace surfaces.
- Remove/replace the stale per-repo-script plan and failing test that were committed under the old design.

## Non-goals

- Does not rewrite the third-party `using-git-worktrees` source. Changes are applied through the existing overlay adapter.
- Does not modify the per-repo `install_agent_skills.py` or `generate_index_mesh.py` commands. The new skills discover and invoke the existing repo-level commands.
- Does not change the `marketplace-source` submodule layout in consumer repos.
- Does not add repo-level `scripts/` wrappers in the source repo beyond the skill-provided entrypoints.

## Architecture

```
using-git-worktrees (third-party skill + overlay)
├── scripts/new_worktree.py  -> creates worktree, then auto-runs refreshing-installed-skills
├── scripts/new-worktree.sh / .ps1 -> wrappers
├── scripts/remove_worktree.py -> removes worktree
├── scripts/remove-worktree.sh / .ps1 -> wrappers
└── SKILL.md (overlay) -> tells agents to use bundled scripts and skills

refreshing-installed-skills (first-party skill)
├── scripts/refresh_installed_skills.py
│   ├── find plugin source (local or marketplace-source submodule)
│   ├── run install_agent_skills.py
│   ├── find generating-index-mesh skill and run it
│   └── commit if changed
├── scripts/refresh-installed-skills.sh / .ps1
└── SKILL.md

generating-index-mesh (first-party skill)
├── scripts/generate_index_mesh.py
│   └── find and run the repo's generate_index_mesh.py
├── scripts/generate-index-mesh.sh / .ps1
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
3. Look for a repo-level override in this order and run the first one found:
   - `scripts/refresh-installed-skills.*`
   - `tools/refresh-installed-skills.*`
   If found, run it and exit.
4. Detect repo layout:
   - **Marketplace source repo** — `codex-marketplace/plugins` exists and `tools/install_agent_skills.py` exists.
   - **Consumer repo** — `.agents/plugins/marketplace-source` exists as a directory or git submodule. If it is a submodule, run `git submodule update --init --recursive .agents/plugins/marketplace-source`.
5. Run the discovered install command:
   - source repo: `tools/install_agent_skills.py`
   - consumer: `scripts/install_agent_skills.py`
   If the consumer wrapper is missing, fail with a clear message; the generic skill does not copy files manually from the submodule.
6. After install succeeds, find the `generating-index-mesh` skill core and run it:
   - Search order:
     1. `.agents/skills/generating-index-mesh/scripts/generate_index_mesh.py`
     2. For each active plugin root from `.agents/plugins/marketplace.json`, `<plugin-root>/skills/generating-index-mesh/scripts/generate_index_mesh.py`
   - Run the first one found.
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
2. Look for a repo-level override in this order and run the first one found:
   - `scripts/generate-index-mesh.*`
   - `tools/generate-index-mesh.*`
   If found, run it and exit.
3. Detect repo layout:
   - source repo: `tools/generate_index_mesh.py`
   - consumer: `scripts/generate_index_mesh.py`
   If the consumer wrapper is missing, fail with a clear message.
4. Run the discovered command. Pass `--check` through when invoked in check mode.
5. Does **not** auto-commit; the caller (`refreshing-installed-skills`, CI, or pre-commit) decides whether to commit.

### `adapters/codex/superpowers-plus/using-git-worktrees/`

- `scripts/new_worktree.py` — core creation logic.
- `scripts/new-worktree.sh` / `scripts/new-worktree.ps1` — wrappers.
- `scripts/remove_worktree.py` — core removal logic.
- `scripts/remove-worktree.sh` / `scripts/remove-worktree.ps1` — wrappers.
- `overlay.yaml` — extended with `generated_files` entries for the above scripts and with line edits that teach agents to use them.

The `overlay.yaml` `generated_files` block becomes:

```yaml
generated_files:
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/new_worktree.py
    path: scripts/new_worktree.py
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/new-worktree.sh
    path: scripts/new-worktree.sh
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/new-worktree.ps1
    path: scripts/new-worktree.ps1
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/remove_worktree.py
    path: scripts/remove_worktree.py
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/remove-worktree.sh
    path: scripts/remove-worktree.sh
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/remove-worktree.ps1
    path: scripts/remove-worktree.ps1
```

**`new_worktree.py` behavior:**
1. Determine repo root via `git rev-parse --show-toplevel` and reject submodules.
2. Strip `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` from the environment for all subprocess calls.
3. Compute canonical sibling worktree root: `<repo-root>/../_agent-worktrees/<repo-name>/<branch>`.
4. Run `git worktree add <path> -b <branch> [<base-ref>]`.
5. **Auto-run `refreshing-installed-skills` in the new worktree** (default; skip with `--no-skill-refresh`).
   - Search order for the core script:
     1. `<new-worktree>/.agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
     2. For each active plugin root from `.agents/plugins/marketplace.json` in the new worktree:
        `<plugin-root>/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
   - Run the first one found. If none is found, print a clear warning telling the agent to run `refreshing-installed-skills` manually.
6. Print `Worktree ready at <path>`.
7. Support `--no-skill-refresh` and `--base-ref` options.

**`remove_worktree.py` behavior:**
1. Resolve the worktree by branch name or path using `git worktree list --porcelain`.
2. Reject removal if the resolved path is the main repo root.
3. Run `git -C <path> submodule deinit --all -f` and ignore failures.
4. Run `git worktree remove <path> [--force]`.
5. Print `Removed worktree <path>`.

### `codex-marketplace/custody-pack-registry.json`

Add the source directories to the `repo-worker-pack` `source_ledger` and add first-party entries for `refreshing-installed-skills` and `generating-index-mesh` to the `repo-worker-pack` bundle (both are also auto-included in the `house-skills` mega-pack because it scans `sources/first_party/skills/`).

Example entry shape for `repo-worker-pack`:

```json
{
  "canonical_name": "refreshing-installed-skills",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/refreshing-installed-skills",
  "local_path": "skills/refreshing-installed-skills",
  "lane": "Worker",
  "source_path": "sources/first_party/skills/refreshing-installed-skills/SKILL.md",
  "source_author": "Harley Bartles",
  "source_license": "MIT",
  "source_repo": "https://github.com/HarleyBartles/agent-asset-marketplace",
  "copy_expectation": "byte_identical",
  "provenance_note": "First-party skill projected verbatim into the repo-worker-pack. Refreshes installed skills from the plugin source and regenerates the index mesh."
}
```

Repeat the same shape for `generating-index-mesh`.

## Data flow

```
Agent invokes new-worktree
        |
        v
new_worktree.py creates worktree at canonical path
        |
        v
auto-runs refreshing-installed-skills in the new worktree
        |
        +--> refresh_installed_skills.py
             |    run install_agent_skills.py
             |    find and run generating-index-mesh
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
        +--> run repo's generate_index_mesh.py
        v
Mesh regenerated (caller decides whether to commit)
```

## Error handling

- If `git rev-parse --show-superproject-working-tree` returns a path, stop; do not run from a submodule.
- If the worktree path already exists, `new_worktree.py` reports the conflict and stops.
- If the install or mesh command fails, the wrapper exits non-zero and leaves the worktree for inspection.
- If `new_worktree.py` cannot find `refreshing-installed-skills` and `--no-skill-refresh` was not given, it warns and continues so the worktree is still usable.
- `remove_worktree.py` refuses to remove the main checkout.

## Testing

- `tests/test_worktree_scripts.py` — rewritten to test `new_worktree.py` and `remove_worktree.py` help/usage and a minimal temp-repo create/remove cycle.
- `tests/test_refresh_installed_skills.py` — tests override precedence, source-vs-consumer layout detection, `--check` mode, and failure when expected commands are missing.
- `tests/test_generate_index_mesh.py` — tests override precedence, source-vs-consumer layout detection, and `--check` mode.
- All tests use temporary Git repositories so they do not mutate the source repo.
- Full marketplace validation: `py -3 tools/rebuild_marketplace.py` and `py -3 tools/check_marketplace.py`.

## Skill text / overlay changes

- `refreshing-installed-skills/SKILL.md` describes triggering: new worktree, plugin source update, or stale `.agents/skills`.
- `generating-index-mesh/SKILL.md` describes triggering: mesh staleness, CI gate, or pre-commit.
- `using-git-worktrees` overlay adds:
  - A pointer after Step 1a to use bundled `new-worktree` / `remove-worktree` scripts when present.
  - A "Remove a worktree" section near the end.
  - Quick Reference rows for the bundled scripts and `refreshing-installed-skills`.
  - Instructions to invoke `refreshing-installed-skills` after creating a worktree (or rely on `new-worktree` to do it automatically).

## Marketplace packaging

- First-party skills live in `sources/first_party/skills/refreshing-installed-skills` and `sources/first_party/skills/generating-index-mesh`.
- Add entries to `repo-worker-pack` in `codex-marketplace/custody-pack-registry.json`.
- The `house-skills` mega-pack will auto-include both skills from `sources/first_party/skills/` during `rebuild_marketplace.py`.
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
