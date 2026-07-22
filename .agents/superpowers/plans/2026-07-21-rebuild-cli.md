# rebuild_marketplace.py CLI refactor implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a flag-based CLI to `tools/rebuild_marketplace.py` (`--check`, `--phase`, `--skip-*`, `--verbose`), split `tools/validate_marketplace.py` into invocable phase-scoped functions with a `--phase` CLI, and turn `tools/check_marketplace.py` into a thin wrapper over `rebuild_marketplace.py --check`.

**Architecture:** `rebuild_marketplace.py` selects a phase runner from an argparse `--phase` flag. Each phase runner invokes the existing writer/checker scripts and then calls `validate_marketplace.py --phase <phase> --skip-freshness-checks` so every phase is self-validating. `validate_marketplace.py` refactors `main` into `validate_inventory`, `validate_project`, `validate_index`, and `validate_all` functions exposed through its own `--phase` CLI.

**Tech Stack:** Python 3.13, `argparse`, `subprocess`, `pathlib`; existing generator/validator scripts under `tools/`.

## Global Constraints

- All text files must be written with LF line endings (`newline="\n"`).
- No hand-editing of derived marketplace surfaces (plugin trees, manifests, zips, index mesh).
- `check_marketplace.py` must remain a valid CI entry point; its only job becomes delegating to `rebuild_marketplace.py --check`.
- Default `rebuild_marketplace.py` (no flags) must continue to do a full rebuild.
- `validate_marketplace.py` default (no flags) must continue to do full marketplace validation.

---

## Task 1: Add failing CLI tests

**Files:**
- Create: `tests/test_rebuild_marketplace_cli.py`

**Interfaces:**
- Consumes: `tools/rebuild_marketplace.py` and `tools/validate_marketplace.py` as subprocess targets.
- Produces: Test cases that `--help` exposes the new flags and that `--phase project` runs on a clean tree.

- [ ] **Step 1: Write the failing test**

```python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REBUILD = [sys.executable, str(ROOT / "tools" / "rebuild_marketplace.py")]
VALIDATE = [sys.executable, str(ROOT / "tools" / "validate_marketplace.py")]


def test_rebuild_cli_help_exposes_new_flags():
    result = subprocess.run(
        [*REBUILD, "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    text = result.stdout
    assert "--phase" in text, "expected --phase in help"
    assert "--check" in text, "expected --check in help"
    assert "--skip-install" in text, "expected --skip-install in help"
    assert "--verbose" in text, "expected --verbose in help"


def test_validate_marketplace_phase_cli_exists():
    result = subprocess.run(
        [*VALIDATE, "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "--phase" in result.stdout, "expected --phase in validate_marketplace.py help"
```

- [ ] **Step 2: Run the tests and confirm they fail**

Run: `py -3 -m pytest tests/test_rebuild_marketplace_cli.py -v`

Expected: two FAILs because neither `--help` mentions the new flags.

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/test_rebuild_marketplace_cli.py
git commit -m "test: add failing rebuild/validate marketplace CLI flag tests"
```

---

## Task 2: Refactor `validate_marketplace.py` into phase functions

**Files:**
- Modify: `tools/validate_marketplace.py`

**Interfaces:**
- Consumes: existing `check_json`, `check_text`, `check_path_exists`, `_bootstrap_marketplace_dependencies`, `_run_tool_check`, `MARKETPLACE_PLUGIN_SPECS`, `MARKETPLACE_PATH`, etc.
- Produces: public functions `validate_inventory`, `validate_project`, `validate_index`, `validate_all` and a `--phase` CLI.

- [ ] **Step 1: Update `_parse_args` with `--phase`**

Replace the existing `_parse_args` function in `tools/validate_marketplace.py`:

```python
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the local marketplace registry and bundle surfaces")
    parser.add_argument(
        "--phase",
        choices=("inventory", "project", "index", "all"),
        default="all",
        help="Validate only one phase. Default: all",
    )
    parser.add_argument(
        "--skip-freshness-checks",
        action="store_true",
        help=(
            "Skip freshness checks already covered by an upstream step "
            "(generate_plugin_root_inventory --check, project_skills.py --check, "
            "and pack manifests). Metadata validation (validate_repo_index) still runs."
        ),
    )
    return parser.parse_args()
```

- [ ] **Step 2: Add `validate_inventory`**

Insert after `_parse_args`:

```python
def validate_inventory(*, skip_freshness: bool = False) -> None:
    _bootstrap_marketplace_dependencies()
    if not skip_freshness:
        _run_tool_check(
            [sys.executable, "tools/generate_plugin_root_inventory.py", "--check"],
            "plugin root inventory check",
        )
    for spec in MARKETPLACE_PLUGIN_SPECS:
        plugin_manifest = check_json(spec["manifest_path"])
        validate_plugin_manifest(plugin_manifest, spec)
    validate_active_plugin_tree()
    check_json(PLUGIN_ROOT_INVENTORY_PATH)
    print("OK validate_marketplace: inventory")
```

- [ ] **Step 3: Add `validate_project`**

Insert after `validate_inventory`:

```python
def validate_project(*, skip_freshness: bool = False) -> None:
    _bootstrap_marketplace_dependencies()
    intake = check_json(SOURCE_INTAKE_JSON_PATH)
    plugin_manifests: list[dict] = []
    for spec in MARKETPLACE_PLUGIN_SPECS:
        plugin_manifest = check_json(spec["manifest_path"])
        validate_plugin_manifest(plugin_manifest, spec)
        plugin_manifests.append(plugin_manifest)
    registry = check_json(MARKETPLACE_PATH)
    bundle_manifest = check_json(BUNDLE_MANIFEST_PATH)

    validate_marketplace_registry(registry, plugin_manifests)
    if not skip_freshness:
        validate_projection_materializer()
        validate_pack_manifests()
    codex_manifest = check_json(CODEX_MARKETPLACE_MANIFEST_PATH)
    if codex_manifest != registry:
        raise ValueError("codex-marketplace/manifest.json does not match .agents/plugins/marketplace.json")
    validate_bundle_manifest(bundle_manifest, intake)
    for spec in MARKETPLACE_PLUGIN_SPECS:
        if spec["name"] == "house-skills":
            continue
        plugin_root = ROOT / spec["plugin_root"]
        if spec["name"] == "superpowers-plus":
            for required in ("SOURCE.md", "PROJECTION.md", "LICENSE"):
                check_text(plugin_root / required)
            check_json(plugin_root / ".codex-plugin" / "plugin.json")
            check_path_exists(plugin_root / "assets" / "app-icon.png")
            check_path_exists(plugin_root / "assets" / "superpowers-small.svg")
        else:
            for required in ("README.md", "SOURCE.md", "LICENSE"):
                check_text(plugin_root / required)
            if (plugin_root / "package.json").exists():
                check_json(plugin_root / "package.json")
            check_path_exists(plugin_root / "assets/icon.svg")

        bundle_path = plugin_root / "references/bundle-manifest.json"
        if bundle_path.exists():
            bundle_manifest_json = check_json(bundle_path)
            if spec["name"] == "superpowers-plus":
                validate_superpowers_bundle_manifest(bundle_manifest_json, spec["plugin_root"])
            elif bundle_manifest_json.get("bundle_type") == "projection-lane":
                if "entries" in bundle_manifest_json:
                    validate_projection_pack_manifest(
                        bundle_manifest_json,
                        bundle_name=spec["name"],
                        plugin_root=spec["plugin_root"],
                    )
                else:
                    raise ValueError(f"{spec['name']} projection-lane bundle manifest has no recognized payload shape")
            else:
                validate_skill_bundle_manifest(
                    bundle_manifest_json,
                    bundle_name=spec["name"],
                    plugin_root=spec["plugin_root"],
                )

    source_map = check_text(SOURCE_MAP_PATH)
    validate_source_map(source_map)
    check_text(ROOT / "codex-marketplace/README.md")
    check_text(ROOT / "codex-marketplace/plugins/README.md")
    check_text(PLUGIN_README_PATH)
    check_text(PLUGIN_SKILL_PATH)
    check_text(PLUGIN_BUNDLE_AGENTS_PATH)
    check_text(PROVENANCE_PATH)
    check_text(ROOT / "provenance/MARK-99-unslop.md")
    validate_no_legacy_manifest_shapes()
    orphans = detect_first_party_orphans()
    if orphans:
        raise ValueError(
            f"first-party orphan skills detected (have SKILL.md in custody but no projection entry): {orphans}\n"
            f"Fix: add manifest entries for these skills and regenerate, or remove retired source custody that should not stay in the active first-party tree."
        )
    print(f"OK first-party orphan check: 0 orphans")
    validate_mega_pack_inclusion()
    validate_skill_zip_assertions()
    print("OK validate_marketplace: project")
```

- [ ] **Step 4: Add `validate_index`**

Insert after `validate_project`:

```python
def validate_index(*, skip_freshness: bool = False) -> None:
    _ = skip_freshness
    _bootstrap_marketplace_dependencies()
    check_text(REPO_INDEX_README_PATH)
    check_json(REPO_INDEX_PATH)
    validate_repo_index()
    print("OK validate_marketplace: index")
```

- [ ] **Step 5: Add `validate_all`**

Insert after `validate_index`:

```python
def validate_all(*, skip_freshness: bool = False) -> None:
    validate_inventory(skip_freshness=skip_freshness)
    validate_project(skip_freshness=skip_freshness)
    validate_index(skip_freshness=skip_freshness)
```

- [ ] **Step 6: Replace `main` with phase dispatch**

Replace the entire `main` function:

```python
def main() -> int:
    args = _parse_args()
    phase_runners = {
        "inventory": lambda: validate_inventory(skip_freshness=args.skip_freshness_checks),
        "project": lambda: validate_project(skip_freshness=args.skip_freshness_checks),
        "index": lambda: validate_index(skip_freshness=args.skip_freshness_checks),
        "all": lambda: validate_all(skip_freshness=args.skip_freshness_checks),
    }
    phase_runners[args.phase]()
    print("Marketplace validation passed.")
    return 0
```

- [ ] **Step 7: Run the tests**

Run: `py -3 -m pytest tests/test_rebuild_marketplace_cli.py -v`

Expected: `test_validate_marketplace_phase_cli_exists` passes; `test_rebuild_cli_help_exposes_new_flags` still fails.

- [ ] **Step 8: Verify full validation still works**

Run: `py -3 tools/validate_marketplace.py --skip-freshness-checks`

Expected: `Marketplace validation passed.`

- [ ] **Step 9: Verify phase validation works**

Run:

```bash
py -3 tools/validate_marketplace.py --phase inventory --skip-freshness-checks
py -3 tools/validate_marketplace.py --phase project --skip-freshness-checks
py -3 tools/validate_marketplace.py --phase index --skip-freshness-checks
```

Expected: each prints its own OK and finally `Marketplace validation passed.`

- [ ] **Step 10: Commit**

```bash
git add tools/validate_marketplace.py
git commit -m "refactor(validate): split main into phase-scoped functions and add --phase CLI"
```

---

## Task 3: Add `rebuild_marketplace.py` argument parser

**Files:**
- Modify: `tools/rebuild_marketplace.py`

**Interfaces:**
- Consumes: existing `_run_tool`, `_run_git`, `_git_output` helpers.
- Produces: `args` namespace with `check`, `phase`, `skip_install`, `skip_index`, `skip_validate`, `skip_whitespace_check`, `verbose`.

- [ ] **Step 1: Update `_run_tool` to support verbose printing**

Replace the existing `_run_tool` function in `tools/rebuild_marketplace.py`:

```python
def _run_tool(script_name: str, *args: str, verbose: bool = False) -> None:
    script_path = Path(__file__).resolve().with_name(script_name)
    cmd = [sys.executable, str(script_path), *args]
    if verbose:
        print("+ " + " ".join(cmd))
    subprocess.run(cmd, check=True)
```

- [ ] **Step 2: Update `_run_git` to support verbose printing**

Replace the existing `_run_git` function:

```python
def _run_git(*args: str, verbose: bool = False) -> None:
    cmd = ["git", *args]
    if verbose:
        print("+ " + " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)
```

- [ ] **Step 3: Add `_check_arg` helper and `_PHASE_ORDER`**

Insert after `_parse_args` (or where `_parse_args` will be):

```python
def _check_arg(check: bool) -> tuple[str, ...]:
    return ("--check",) if check else ()


_PHASE_ORDER = ("inventory", "heal", "project", "index", "catalog", "validate")
```

- [ ] **Step 4: Replace `_parse_args` with the new CLI parser**

Replace the existing `_parse_args` function:

```python
def _parse_args() -> argparse.Namespace:
    epilog = (
        "This is the canonical 'refresh marketplace' command. It regenerates all derived\n"
        "marketplace surfaces and then validates them.\n\n"
        "Use --phase to run only one logical phase. Each phase is self-checking; earlier\n"
        "phases are not automatically regenerated unless you run --phase all (the default).\n\n"
        "Editable inputs (do not hand-edit derived outputs):\n"
        "  - codex-marketplace/custody-pack-registry.json\n"
        "  - sources/first_party/skills/<skill>/\n"
        "  - sources/third_party/<upstream>/\n"
        "  - adapters/codex/<pack>/<skill>/\n\n"
        "Key outputs:\n"
        "  - .agents/plugins/marketplace.json, codex-marketplace/manifest.json\n"
        "  - codex-marketplace/plugins/<pack>/skills/<skill>/\n"
        "  - codex-marketplace/plugins/<pack>/references/{bundle-manifest,source-map,provenance-map}.*\n"
        "  - generated/skill-zips/<skill>.zip\n"
        "  - provenance/first-party-skills.md\n"
        "  - repo-index/repo-index.json and repo-wide INDEX.md mesh\n"
        "  - .agents/skills/<skill>/ (installed skills)\n\n"
        "For the full step-by-step flow see .agents/guides/marketplace-generation-guide.md."
    )
    parser = argparse.ArgumentParser(
        description="Run the full marketplace rebuild and validation stack",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Non-mutating check mode. Forwards --check to every writer script that supports it.",
    )
    parser.add_argument(
        "--phase",
        choices=("inventory", "heal", "project", "index", "catalog", "validate", "all"),
        default="all",
        help="Run only the named phase. Default: all",
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip installing skills into .agents/skills/",
    )
    parser.add_argument(
        "--skip-index",
        action="store_true",
        help="Skip repo-index and index-mesh generation",
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Skip validator scripts in the final validate phase",
    )
    parser.add_argument(
        "--skip-whitespace-check",
        action="store_true",
        help="Skip git diff --check (whitespace lint). Does not skip --exit-code in --check mode.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print each command before running it",
    )
    return parser.parse_args()
```

- [ ] **Step 5: Run the failing test**

Run: `py -3 -m pytest tests/test_rebuild_marketplace_cli.py::test_rebuild_cli_help_exposes_new_flags -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add tools/rebuild_marketplace.py
git commit -m "feat(rebuild): add --phase, --check, --skip-*, and --verbose argument parser"
```

---

## Task 4: Implement `rebuild_marketplace.py` phase runners

**Files:**
- Modify: `tools/rebuild_marketplace.py`

**Interfaces:**
- Consumes: `_run_tool`, `_run_git`, `_git_output`, `_prune_stale_projected_plugin_roots`, `_retained_verbatim_paths`, `_check_arg`.
- Produces: `_run_inventory`, `_run_heal`, `_run_project`, `_run_index`, `_run_catalog`, `_run_validate`, `_run_whitespace_check`.

- [ ] **Step 1: Add `_run_inventory` and `_run_heal`**

Insert after `_check_arg`:

```python
def _run_inventory(*, check: bool, verbose: bool) -> None:
    _run_tool("generate_plugin_root_inventory.py", *_check_arg(check), verbose=verbose)
    if not check:
        _prune_stale_projected_plugin_roots()
    _run_tool("validate_marketplace.py", "--phase", "inventory", "--skip-freshness-checks", verbose=verbose)


def _run_heal(*, check: bool, verbose: bool) -> None:
    _run_tool("heal_overlays.py", *_check_arg(check), verbose=verbose)
```

- [ ] **Step 2: Add `_run_project`**

Insert after `_run_heal`:

```python
def _run_project(*, check: bool, verbose: bool, skip_install: bool) -> None:
    if check:
        _run_tool("update_skill_artifacts.py", "--check", verbose=verbose)
    else:
        _run_tool("update_skill_artifacts.py", "--all", verbose=verbose)
    _run_tool("normalize_first_party_skill_sources.py", *_check_arg(check), verbose=verbose)
    if not skip_install:
        _run_tool("install_agent_skills.py", *_check_arg(check), verbose=verbose)
    _run_tool("validate_marketplace.py", "--phase", "project", "--skip-freshness-checks", verbose=verbose)
```

- [ ] **Step 3: Add `_run_index` and `_run_catalog`**

Insert after `_run_project`:

```python
def _run_index(*, check: bool, verbose: bool, skip_index: bool) -> None:
    if skip_index:
        return
    _run_tool("generate_repo_index.py", *_check_arg(check), verbose=verbose)
    if check:
        _run_tool("generate_index_mesh.py", "--check", verbose=verbose)
    else:
        _run_tool("generate_index_mesh.py", verbose=verbose)
        _run_tool("generate_index_mesh.py", "--check", verbose=verbose)
    _run_tool("validate_marketplace.py", "--phase", "index", "--skip-freshness-checks", verbose=verbose)


def _run_catalog(*, check: bool, verbose: bool) -> None:
    if check:
        _run_tool("generate_first_party_skill_catalog.py", "--check", verbose=verbose)
    else:
        _run_tool("generate_first_party_skill_catalog.py", verbose=verbose)
        _run_tool("generate_first_party_skill_catalog.py", "--check", verbose=verbose)
```

- [ ] **Step 4: Add `_run_whitespace_check` helper**

Insert before `_run_validate`:

```python
def _run_whitespace_check(*, verbose: bool, skip: bool) -> None:
    if skip:
        return
    changed_paths = [
        path
        for path in _git_output("diff", "--name-only", "HEAD").splitlines()
        if path and path not in _retained_verbatim_paths()
    ]
    if not changed_paths:
        return
    _MAX_CMD_CHARS = 28000
    batch: list[str] = []
    batch_len = 0
    for path in changed_paths:
        path_len = len(path) + 4  # path + space + 2 quotes + separator
        if batch and batch_len + path_len > _MAX_CMD_CHARS:
            _run_git("diff", "--check", "HEAD", "--", *batch, verbose=verbose)
            batch = []
            batch_len = 0
        batch.append(path)
        batch_len += path_len
    if batch:
        _run_git("diff", "--check", "HEAD", "--", *batch, verbose=verbose)
```

- [ ] **Step 5: Add `_run_validate`**

Insert after `_run_whitespace_check`:

```python
def _run_validate(
    *,
    check: bool,
    verbose: bool,
    skip_validate: bool,
    skip_whitespace_check: bool,
) -> None:
    if not skip_validate:
        _run_tool("validate_authority_assets.py", verbose=verbose)
    _run_whitespace_check(verbose=verbose, skip=skip_whitespace_check)
    if check:
        _run_git("diff", "--exit-code", verbose=verbose)
```

- [ ] **Step 6: Run the CLI tests**

Run: `py -3 -m pytest tests/test_rebuild_marketplace_cli.py -v`

Expected: PASS (the tests only inspect `--help`).

- [ ] **Step 7: Commit**

```bash
git add tools/rebuild_marketplace.py
git commit -m "feat(rebuild): implement phase runner functions with per-phase validation"
```

---

## Task 5: Wire phase dispatch into `main`

**Files:**
- Modify: `tools/rebuild_marketplace.py`

**Interfaces:**
- Consumes: `_parse_args`, all `_run_*` functions, `_PHASE_ORDER`.
- Produces: `main()` dispatches to the selected phase(s).

- [ ] **Step 1: Replace `main` with phase dispatch**

Replace the entire `main` function:

```python
def main() -> int:
    args = _parse_args()

    phase_runners = {
        "inventory": lambda: _run_inventory(check=args.check, verbose=args.verbose),
        "heal": lambda: _run_heal(check=args.check, verbose=args.verbose),
        "project": lambda: _run_project(
            check=args.check,
            verbose=args.verbose,
            skip_install=args.skip_install,
        ),
        "index": lambda: _run_index(
            check=args.check,
            verbose=args.verbose,
            skip_index=args.skip_index,
        ),
        "catalog": lambda: _run_catalog(check=args.check, verbose=args.verbose),
        "validate": lambda: _run_validate(
            check=args.check,
            verbose=args.verbose,
            skip_validate=args.skip_validate,
            skip_whitespace_check=args.skip_whitespace_check,
        ),
    }

    phases = _PHASE_ORDER if args.phase == "all" else (args.phase,)
    for phase in phases:
        phase_runners[phase]()
    return 0
```

- [ ] **Step 2: Run the full CLI test suite**

Run: `py -3 -m pytest tests/test_rebuild_marketplace_cli.py -v`

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add tools/rebuild_marketplace.py
git commit -m "feat(rebuild): wire --phase dispatch into main"
```

---

## Task 6: Rewrite `check_marketplace.py` as a thin wrapper

**Files:**
- Modify: `tools/check_marketplace.py`

**Interfaces:**
- Consumes: `rebuild_marketplace.py --check`.
- Produces: `check_marketplace.py` delegates to `rebuild_marketplace.py --check`.

- [ ] **Step 1: Replace `check_marketplace.py` content**

```python
#!/usr/bin/env python3
"""Canonical non-mutating marketplace validation entrypoint.

This is a thin wrapper around `tools/rebuild_marketplace.py --check`.
The wrapper preserves the canonical CI command and help surface while the
full orchestration lives in the rebuild entry point.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REBUILD = ROOT / "tools" / "rebuild_marketplace.py"


def _parse_args() -> argparse.Namespace:
    epilog = (
        "This is the canonical non-mutating CI gate. It checks whether the committed\n"
        "marketplace surfaces are current and valid without writing any files.\n\n"
        "The check is implemented as `py -3 tools/rebuild_marketplace.py --check`.\n\n"
        "For the full rebuild flow see .agents/guides/marketplace-generation-guide.md."
    )
    parser = argparse.ArgumentParser(
        description="Run the non-mutating marketplace check stack",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    return parser.parse_args()


def main() -> int:
    _parse_args()
    return subprocess.run(
        [sys.executable, str(REBUILD), "--check"],
        cwd=ROOT,
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run the wrapper**

Run: `py -3 tools/check_marketplace.py`

Expected: exits 0 on a clean tree.

- [ ] **Step 3: Commit**

```bash
git add tools/check_marketplace.py
git commit -m "refactor(check): make check_marketplace.py a thin wrapper over rebuild --check"
```

---

## Task 7: Update tooling documentation

**Files:**
- Modify: `tools/AGENTS.md`

**Interfaces:**
- Consumes: current `tools/AGENTS.md` text.
- Produces: documented `--check`, `--phase`, and `validate_marketplace.py --phase` capabilities.

- [ ] **Step 1: Locate the `rebuild_marketplace.py` description**

Read `tools/AGENTS.md` and find:

> The canonical full rebuild and validation entrypoint is
> `py -3 tools/rebuild_marketplace.py`.
> The canonical non-mutating CI gate is `py -3 tools/check_marketplace.py`.

- [ ] **Step 2: Update the description**

Replace those sentences with:

```markdown
The canonical full rebuild and validation entrypoint is
`py -3 tools/rebuild_marketplace.py`.
Use `py -3 tools/rebuild_marketplace.py --check` for a non-mutating check,
or `py -3 tools/check_marketplace.py` as the CI convenience wrapper.
Use `--phase <inventory|heal|project|index|catalog|validate|all>` to run a
single logical phase; `--skip-install`, `--skip-index`, `--skip-validate`,
and `--skip-whitespace-check` omit steps from a full run.
Partial validation is available with `py -3 tools/validate_marketplace.py --phase <inventory|project|index>`.
```

- [ ] **Step 3: Commit**

```bash
git add tools/AGENTS.md
git commit -m "docs(tools): document rebuild --phase and validate_marketplace --phase flags"
```

---

## Task 8: Validate end-to-end

**Files:**
- No file changes.

**Interfaces:**
- Consumes: the modified `rebuild_marketplace.py`, `validate_marketplace.py`, `check_marketplace.py`, and tests.

- [ ] **Step 1: Run the CLI tests**

Run: `py -3 -m pytest tests/test_rebuild_marketplace_cli.py -v`

Expected: PASS.

- [ ] **Step 2: Run the full test suite**

Run: `py -3 -m pytest tests -q`

Expected: all existing tests still pass.

- [ ] **Step 3: Run a full rebuild**

Run: `py -3 tools/rebuild_marketplace.py`

Expected: completes with no errors and no whitespace diff failures.

- [ ] **Step 4: Run a non-mutating check**

Run: `py -3 tools/check_marketplace.py`

Expected: exits 0 on the clean tree.

- [ ] **Step 5: Run each phase in check mode**

Run:

```bash
py -3 tools/rebuild_marketplace.py --check --phase inventory
py -3 tools/rebuild_marketplace.py --check --phase heal
py -3 tools/rebuild_marketplace.py --check --phase project
py -3 tools/rebuild_marketplace.py --check --phase index
py -3 tools/rebuild_marketplace.py --check --phase catalog
py -3 tools/rebuild_marketplace.py --check --phase validate
```

Expected: each exits 0.

- [ ] **Step 6: Run `validate_marketplace.py` phase CLI**

Run:

```bash
py -3 tools/validate_marketplace.py --phase inventory --skip-freshness-checks
py -3 tools/validate_marketplace.py --phase project --skip-freshness-checks
py -3 tools/validate_marketplace.py --phase index --skip-freshness-checks
```

Expected: each exits 0.

- [ ] **Step 7: Commit final validation state**

If any generated artifacts changed during the rebuild:

```bash
git add -A
git commit -m "chore: regenerate marketplace surfaces after CLI refactor"
```

---

## Self-review checklist

- [ ] **Spec coverage:** Every CLI flag and phase from `.agents/superpowers/specs/2026-07-21-rebuild-cli-design.md` maps to a task:
  - `rebuild_marketplace.py --check` → Task 3 parser + Task 4 runners forwarding `--check`
  - `rebuild_marketplace.py --phase` → Task 3 parser + Task 5 dispatch
  - `rebuild_marketplace.py --skip-*` → Task 3 parser + Task 4 runner functions
  - `rebuild_marketplace.py --verbose` → Task 3 parser + Task 3 `_run_tool`/`_run_git` update
  - `validate_marketplace.py --phase` → Task 2 parser + Task 2 phase functions
  - `check_marketplace.py` wrapper → Task 6
- [ ] **Placeholder scan:** No `TBD`, `TODO`, or vague steps in the plan.
- [ ] **Type consistency:** All `_run_*` signatures use `check: bool` and `verbose: bool`; `validate_*` functions use `skip_freshness: bool`; `main` reads `args.*` correctly.
- [ ] **File path sanity:** `tools/rebuild_marketplace.py`, `tools/validate_marketplace.py`, `tools/check_marketplace.py`, `tools/AGENTS.md`, `tests/test_rebuild_marketplace_cli.py` are the only touched files.

## Execution handoff

Plan complete and saved to `.agents/superpowers/plans/2026-07-21-rebuild-cli.md`. Two execution options:

1. **Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks.
2. **Inline Execution** — execute tasks in this session using `executing-plans` or direct edits.

Which approach do you want to use?
