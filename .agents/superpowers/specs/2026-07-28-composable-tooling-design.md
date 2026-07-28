---
date: 2026-07-28
topic: composable-tooling
---

# Composable tooling design

## Goal

Give the repository a single, dependency-aware command surface.
Agents should be able to regenerate only the surfaces that changed, run the same
checks locally that CI runs, and get a concrete repair command on failure.
This design replaces the current flat list of generator/validator scripts and
the separate `scripts/ci-preflight.sh` abstraction.

## Background

- `2026-07-21-rebuild-cli-design.md` added `--phase` to `tools/rebuild_marketplace.py`
  so a single script could run one logical phase of the marketplace pipeline.
- `2026-07-27-ci-preflight-pipeline-design.md` made `scripts/ci-preflight.sh`
  the repo-owned CI mirror and wired it to `.git/hooks/pre-commit`.

Both improved the surface, but an agent still has to know the right script and
mode for each job:

- `tools/rebuild_marketplace.py --phase <inventory|heal|project|index|catalog|validate> --check`
- `tools/rebuild_marketplace.py --phase <x> --apply`
- `python .agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py --apply`
- `python .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --apply`
- `bash scripts/ci-preflight.sh --check`

There is no clean way to compose "refresh installed skills and regenerate the
mesh" without running the whole marketplace. Pre-commit and CI are also still
framed as separate surfaces even though they run the same checks.

## Scope

1. Create `tools/run` as the canonical agent-facing command.
2. Define a task graph of named targets that can be composed.
3. `tools/run` resolves dependencies and runs the requested target plus its
   prerequisites in the right order.
4. `--check` runs non-mutating validation; `--apply` regenerates outputs.
5. On failure, print the exact `--apply` command (or target-specific repair
   command) to stderr.
6. Replace `scripts/ci-preflight.sh` with `.git/hooks/pre-commit` calling
   `tools/run ci --check`.
7. Replace `tools/rebuild_marketplace.py` as the public entrypoint; move its
   phase logic into the `tools/run` task graph or remove the script.
8. Update `.github/workflows/marketplace-validation.yml` to call
   `tools/run ci --check` or the same target sequence.
9. Update `tools/AGENTS.md`, `tools/README.md`, and the relevant guides to
   document `tools/run`.
10. Add `tests/test_run_cli.py` covering target resolution, dependency order,
    failure messages, and the `ci` meta-target.

## Non-goals

- Do not add an external task runner such as `just`, `make`, or `invoke`.
  The runner is a small Python script in `tools/`.
- Do not implement incremental/dirty detection in the first version.
  The runner composes existing `--check`/`--apply` scripts in dependency order.
  Skipping already-valid phases can be added later.
- Do not change the underlying generator/validator algorithms.
  Only how they are exposed and composed changes.
- Do not rewrite historical specs. Reference them and explain how this design
  supersedes their public surface.

## Principles

- One public entrypoint: `tools/run`.
- Pre-commit and CI are peers that consume the same target set (`ci`).
- Every failure prints a fix command.
- Targets are small and composable; meta-targets group them.
- Existing generator/validator scripts become implementation details invoked by
  the runner.

## Task graph

### Leaf targets

| Target | `--apply` action | `--check` action | Fix command |
|---|---|---|---|
| `lint` | `python -m ruff check --fix <changed-files> && python -m ruff format <changed-files>` | `tools/ruff_diff.py --changed-from <base>` | same ruff command |
| `repo-standards` | `python .agents/skills/repo-standards/scripts/repo_standards.py --apply --yes` | `bash .agents/skills/repo-standards/scripts/repo-standards.sh --check` | `tools/run repo-standards --apply` |
| `inventory` | `tools/generate_plugin_root_inventory.py` | `tools/generate_plugin_root_inventory.py --check` | `tools/run inventory --apply` |
| `heal` | `tools/heal_overlays.py` | `tools/heal_overlays.py --check` | `tools/run heal --apply` |
| `project` | `tools/update_skill_artifacts.py --all`, `tools/normalize_first_party_skill_sources.py`, `tools/project_skills.py` (write) | `tools/update_skill_artifacts.py --check`, `tools/normalize_first_party_skill_sources.py --check`, `tools/project_skills.py` (write=False) | `tools/run project --apply` |
| `installed-skills` | `python .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --apply` | same script in `--check` mode | `tools/run installed-skills --apply` |
| `repo-index` | `tools/generate_repo_index.py` | `tools/generate_repo_index.py --check` | `tools/run repo-index --apply` |
| `mesh` | `python .agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py --apply`, then `bash .agents/skills/generating-agent-mesh/scripts/validate-agent-mesh.sh --check` | `python .agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py --check`, then `bash .agents/skills/generating-agent-mesh/scripts/validate-agent-mesh.sh --check` | `tools/run mesh --apply` |
| `catalog` | `tools/generate_first_party_skill_catalog.py` | `tools/generate_first_party_skill_catalog.py --check` | `tools/run catalog --apply` |
| `validate` | `tools/validate_authority_assets.py` and `git diff --check` on changed paths | same non-mutating checks | `tools/run marketplace --apply` (or repair the failure reported by the sub-check) |

The exact commands in `project` will be verified against `tools/rebuild_marketplace.py`
during implementation; they may be split into smaller, more focused targets if the
existing scripts already expose finer-grained flags.

### Meta-targets

| Target | Dependencies |
|---|---|
| `marketplace` | `inventory → heal → project → installed-skills → repo-index → mesh → catalog → validate` |
| `ci` | `lint → repo-standards → marketplace` |
| `all` | alias for `ci` |

The exact edge list will be verified against `tools/rebuild_marketplace.py` and
`scripts/ci-preflight.sh` during implementation so no ordering or freshness bug
is introduced.

## CLI contract

### Usage

```bash
tools/run <target> [<target>...] [--check | --apply] [--base-ref <ref>] [--allow-shared-checkout] [--verbose]
```

- If neither `--check` nor `--apply` is passed, default to `--check`.
- Multiple targets are resolved and deduplicated; dependencies run once.
- `--base-ref` sets the comparison ref for the `lint` target. Defaults to
  `origin/main` if available; otherwise all tracked `.py` files are linted with
  a warning.
- `--allow-shared-checkout` is forwarded to child scripts that require explicit
  approval to write in the main shared checkout (`generate_index_mesh.py`,
  `refresh_installed_skills.py`, etc.). It is not needed in a linked worktree.
- `--verbose` prints each sub-command before executing it.

### Examples

```bash
# Run the full CI gate (what pre-commit and CI both run)
tools/run ci --check

# Regenerate only the repo-wide INDEX.md mesh
tools/run mesh --apply

# Refresh installed skills and regenerate the mesh
tools/run installed-skills mesh --apply

# Regenerate the full marketplace
tools/run marketplace --apply

# Apply in the main shared checkout
tools/run marketplace --apply --allow-shared-checkout
```

### Failure output

When a target fails, the runner prints one loud line:

```
[tools/run] target '<name>' failed.
Fix: <command>
```

For most targets the `<command>` is `tools/run <name> --apply`.
For `lint` it is the concrete ruff command.
For `validate` it is `tools/run marketplace --apply` because `validate` is a
final check-only gate; the underlying sub-check output shows the precise failure.

## Pre-commit and CI unification

- `.git/hooks/pre-commit` becomes `exec tools/run ci --check`.
- `.github/workflows/marketplace-validation.yml` calls `tools/run ci --check`
  as a single step, or decomposes it into named workflow steps that each call
  `tools/run <target> --check` if we want per-target visibility.
- `scripts/ci-preflight.sh` and `scripts/ci-preflight.ps1` are removed.

## Replacing existing public entrypoints

- `tools/rebuild_marketplace.py` is removed as a public entrypoint.
  Its phase logic is moved into the `tools/run` task graph or deleted once the
  runner can invoke the same underlying scripts.
- `tools/update_skill_artifacts.py` remains as an implementation detail invoked by
  the `project` target. The `--skill` and `--pack` flags, already deprecated,
  are removed.
- `tools/check_marketplace.py` is already gone per `2026-07-27-ci-preflight-pipeline-design.md`.

## Implementation sketch

`tools/run` is a Python script with a small in-memory registry:

```python
TASKS: dict[str, Task] = {
    "inventory": Task(
        apply=["tools/generate_plugin_root_inventory.py"],
        check=["tools/generate_plugin_root_inventory.py", "--check"],
        deps=(),
    ),
    ...
}
```

- The registry maps each target to its `--apply` and `--check` command lists and
  to its dependency names.
- A resolver expands requested targets topologically and fails on cycles.
- A runner executes each task in order, aborting on the first failure.
- Failure handling looks up the target's `fix` message and prints it.
- In `--apply` mode the runner also calls `shared_checkout.approve_mutation`
  with the `--allow-shared-checkout` value before executing any writer, so the
  same gating behavior as `tools/rebuild_marketplace.py` is preserved.

The registry stays in `tools/run` itself so the command, the dependency graph,
and the failure messages live in one file that is easy to review and diff.

## Testing and verification

- Run `tools/run ci --check` locally and confirm each target reports OK.
- Run `tools/run ci --apply` and confirm generated surfaces update.
- Run `tools/run installed-skills mesh --apply` and confirm only those targets
  and their dependencies execute.
- Run `py -3 -m pytest tests/test_run_cli.py` to confirm target resolution,
  dependency order, and failure-message behavior.
- Regenerate the marketplace with `tools/run marketplace --apply` and confirm
  `tools/run ci --check` passes.

## Risks and open questions

1. **Ordering bugs.** The task graph must exactly match the current
   `rebuild_marketplace.py` phase order or generated surfaces can become stale.
2. **Windows/PowerShell compatibility.** The runner must invoke sub-commands in
   a way that works on Windows (PowerShell) and Linux/macOS (bash). Concrete
   shell scripts are replaced with Python `subprocess` calls.
3. **First version is not incremental.** It composes better but still runs the
   full dependency chain for a target. `--since` or dirty-detection can be a
   follow-up.
4. **Docs churn.** Many guides mention `rebuild_marketplace.py` and
   `ci-preflight.sh`; they must be updated in the same PR.
5. **Lint target base ref.** `ruff_diff.py` needs a base ref. The `lint`
   target defaults to `origin/main` if available, else warns and lints all
   tracked `.py` files. This matches the current `ci-preflight.sh` behavior.
6. **`project` target still heavy.** `tools/update_skill_artifacts.py --all` is a
   coarse wrapper. Composing `installed-skills` and `mesh` still drags in
   `project` because of real dependencies. Finer-grained targets can be split
   out in a follow-up if the underlying scripts expose smaller commands.
