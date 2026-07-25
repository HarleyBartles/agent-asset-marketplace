---
date: 2026-07-25
topic: repo-standards-skill-execution
---

# Repo Standards, Skill Execution, and CI Preflight Design

## Goal

Make `repo-standards` (renamed from `repo-guide-standard`) the portable authority for what a participating repo should look like, and give it a deterministic `check`/`apply` script that can converge a repo to that shape. Move the canonical implementations of `generate_index_mesh` and `install_agent_skills` into the `generating-index-mesh` and `refreshing-installed-skills` skills, with `.sh`/`.ps1` wrappers and Python launcher auto-detection. Give every repo a single `scripts/ci-preflight` entrypoint wired to the skills and a pre-commit hook that runs the same check cheaply before CI.

## Scope

1. Rename `repo-guide-standard` → `repo-standards`.
2. Add `repo-standards/references/repository-shape-manifest.json` (machine-readable target shape) and `repo-standards/references/repository-shape-standard.md` (prose companion).
3. Add `repo-standards/scripts/repo_standards.py`, `repo-standards.sh`, and `repo-standards.ps1` with `check` and `apply` modes.
4. Move `tools/generate_index_mesh.py` logic into `sources/first_party/skills/generating-index-mesh/scripts/generate_index_mesh.py` and make it importable for repo validators.
5. Move `tools/install_agent_skills.py` logic into `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`, add `marketplace-source` freshness roll-to-`origin/main`, and support per-repo local skill prefixes.
6. Add `repo.local_skill_prefixes` to `marketplace.json`, sourced from `codex-marketplace/repo-local-marketplace-policy.json`.
7. Remove `tools/generate_index_mesh.py` and `tools/install_agent_skills.py` from `agent-asset-marketplace`; update `tools/rebuild_marketplace.py` and `tools/AGENTS.md` to call the skill scripts.
8. Add `scripts/ci-preflight.ps1` and `scripts/ci-preflight.sh` templates for consumer repos; `repo-standards` installs them and a `.git/hooks/pre-commit` that calls `scripts/ci-preflight.sh -Check`.
9. Pilot the changes in `agent-asset-marketplace` and `wild-bunch`.

## Non-goals

- Do not unify repo-specific `validate_agent_mesh` logic. Each repo keeps its own validator that wraps/imports from the `generating-index-mesh` skill.
- Do not eliminate the rest of `tools/`; only `generate_index_mesh.py` and `install_agent_skills.py` are being retired in the source repo.
- Do not change the `work-mode-router` `preflight_needed` planning route state. CI preflight is a separate, explicitly named surface.
- Do not support multiple `marketplace-source` submodule paths; only `.agents/plugins/marketplace-source` is in scope.
- Do not add the `mesh_post_processor` extension in this spec; it is deferred for repo-specific extras like ADR freshness tables.

## Contract

### `repo-standards` skill

- Rename source directory `sources/first_party/skills/repo-guide-standard/` to `sources/first_party/skills/repo-standards/`.
- Rename skill frontmatter `name` to `repo-standards`; update `description`, `scope`, and `use_with` to include `inspecting-the-environment`.
- Keep `references/repository-guide-standard.md` as the prose standard and add `references/repository-shape-manifest.json` as the checked source of truth.
- Update `.agents/docs/repo-guide-policy.md` to reference `repo-standards` and list the shape manifest mapping (file may be renamed in a later pass if desired).
- The core script `repo_standards.py` lives at `repo-standards/scripts/repo_standards.py`; wrappers are `repo-standards.sh` and `repo-standards.ps1`.
- Modes:
  - `repo-standards check` — compare the current repo against `repository-shape-manifest.json`; report missing/extra/drift; exit non-zero when non-compliant.
  - `repo-standards apply` — interactive, or `--yes` for automation, fixing missing surfaces by copying templates. It must follow `repo-worker-base/references/mutation-script-safety.md`: refuse a shared checkout by default, support `--allow-shared-checkout` with a prominent warning, and reject submodules.

### `repository-shape-manifest.json`

- Top-level object with `version` and a `surfaces` array.
- Each surface entry has:
  - `id` — stable identifier, e.g. `ci-preflight-ps1`.
  - `path` — repo-relative path, e.g. `scripts/ci-preflight.ps1`.
  - `kind` — `file`, `hook`, `directory`, `skill-installed`, `submodule`, or `marketplace-json-key`.
  - `source` — path inside `repo-standards/templates/` for generated files, or `null` for surfaced/checked-only entries.
  - `optional` — boolean; defaults to `false`.
- Initial surfaces:
  - `scripts/ci-preflight.ps1`
  - `scripts/ci-preflight.sh`
  - `.git/hooks/pre-commit`
  - `.agents/plugins/marketplace-source` (submodule)
  - `.agents/plugins/marketplace.json`
  - `.agents/skills/` (installed from plugins)
  - `marketplace.json` `repo.local_skill_prefixes` key
  - `REVIEW.md` and `CONTRIBUTING.md` (already in `repo-standards`)
  - `.agents/guides/*` guides (already in `repo-standards`)

### `generating-index-mesh` skill

- `sources/first_party/skills/generating-index-mesh/scripts/generate_index_mesh.py` becomes the implementation.
- It accepts `--repo-root` or reads `REPO_ROOT` from the environment; defaults to `git rev-parse --show-toplevel`.
- It is importable as a module: expose `ROOT`, `INDEX_NAME`, `collect_generated_indexes`, `collect_scoped_generated_indexes`, `build_index_scoped`, `discover_existing_indexes`, `render_index`, `is_submodule_root`, `is_submodule_descendant`, `mesh_state_is_current`, and `should_skip_path`.
- It respects `.gitignore`, uses `git ls-files` for tracked paths, and supports `--check` and `--changed-from` (where the repo already uses the fast path).
- It must not run inside a submodule and must follow `mutation-script-safety.md` for writes.
- Wrappers `generate-index-mesh.sh` and `generate-index-mesh.ps1` locate `generate_index_mesh.py` and run it with `python3`/`py`/`python` fallback detection.

### `refreshing-installed-skills` skill

- `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py` becomes the implementation.
- It reads `.agents/plugins/marketplace.json` and the `repo.local_skill_prefixes` list to identify repo-local skills that must not be pruned.
- In write mode, before installing skills, it rolls `.agents/plugins/marketplace-source` to `origin/main`:
  - `git -C .agents/plugins/marketplace-source fetch origin`
  - `git -C .agents/plugins/marketplace-source reset --hard origin/main`
  - Stage the submodule path in the superproject (so the commit captures the bump).
- In `--check` mode, it reports whether the submodule is behind `origin/main` and whether any skills or mesh would change, but does not write.
- It refuses shared checkouts by default and supports `--allow-shared-checkout` with a warning.
- It rejects submodules.
- After installing, it invokes `generating-index-mesh`.
- Wrappers `refresh-installed-skills.sh` and `refresh-installed-skills.ps1` use the same Python launcher detection.

### `marketplace.json` prefix

- Add a top-level `repo` object or a `repo.local_skill_prefixes` key to `marketplace.json`.
- The authoritative source value lives in `codex-marketplace/repo-local-marketplace-policy.json` under `local_skill_prefixes`.
- `tools/generate_marketplace.py` copies it into `marketplace.json`.
- `install_agent_skills.py` uses the key to preserve any directory under `.agents/skills/` whose name starts with one of the prefixes.

### `tools/` cleanup

- Delete `tools/generate_index_mesh.py` and `tools/install_agent_skills.py` from `agent-asset-marketplace`.
- Update `tools/rebuild_marketplace.py` to call `sources/first_party/skills/generating-index-mesh/scripts/generate_index_mesh.py` and `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py` for the source repo.
- Update `tools/AGENTS.md` to point at the skill entrypoints.

### CI preflight templates

- `repo-standards/templates/ci-preflight.ps1` and `ci-preflight.sh` are copied into a consumer repo as `scripts/ci-preflight.ps1` and `scripts/ci-preflight.sh`.
- The PowerShell template calls `.agents/skills/generating-index-mesh/scripts/generate-index-mesh.ps1 -Check`, `.agents/skills/refreshing-installed-skills/scripts/refresh-installed-skills.ps1 -Check`, and a repo-specific `scripts/validate_agent_mesh.ps1` if it exists.
- The Bash template is equivalent.
- `.git/hooks/pre-commit` is installed as a Bash hook that calls `scripts/ci-preflight.sh -Check` and exits with the same code.

### Pilot repos

- `agent-asset-marketplace`: implement source changes, remove `tools/*.py`, regenerate marketplace projections.
- `wild-bunch`: run `repo-standards apply` to install `ci-preflight` and pre-commit hook; remove `scripts/generate_index_mesh.py`, `scripts/install_agent_skills.py`, and their wrappers; keep `scripts/validate_agent_mesh.py` or add an empty template.

## Validation

- `repo-standards check` passes in `agent-asset-marketplace` and `wild-bunch`.
- `py -3 .agents/skills/generating-index-mesh/scripts/generate_index_mesh.py --check` passes in both pilot repos.
- `py -3 .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --check` passes in both pilot repos.
- `py -3 tools/rebuild_marketplace.py --check` passes in `agent-asset-marketplace`.
- `scripts/ci-preflight.ps1 -Check` passes in `wild-bunch`.
- `git diff --check` is clean in both pilots.

## Tradeoffs and intentionally deferred decisions

- **Rename churn.** Renaming `repo-guide-standard` to `repo-standards` touches source paths, plugin manifests, `repo-guide-policy.md`, and generated `INDEX.md` links. We accept the churn to match the expanded scope.
- **Pre-commit hook on Windows.** The initial hook is a Bash script. A native Windows `.ps1` pre-commit hook is deferred; `core.hooksPath` or a `.githooks` directory can be introduced later.
- **Mesh post-processing.** Repo-specific extras (e.g., `wild-bunch` ADR freshness) are out of scope. A follow-up spec will add a `mesh_post_processor` hook to `repo-standards`/`marketplace.json`.
- **`marketplace.json` schema.** The `repo.local_skill_prefixes` key is added to the generated file. A later pass may promote it to `repo-local-marketplace-policy.json` if the source file already carries enough repo-local policy.
- **Scope of `repo-standards apply`.** The first version only generates files and installs hooks. It does not create a `marketplace-source` submodule from scratch; it assumes the submodule is already declared in `.gitmodules`.

## Handoff confidence

This spec is concrete enough for planning: exact skill names, file targets, contract rules, and validation commands are defined. Confidence is **9/10**; the only user-owned gap is the exact `repo.local_skill_prefixes` values for `wild-bunch` and `rooms-mostly`, which can be set when `repo-standards apply` runs.