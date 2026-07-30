# Refreshing Installed Skills — Provenance Rewrite Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `refresh_installed_skills.py` record repo-local skills in `.agents/skills/.provenance.json` and rewrite the file whenever the plugin list, local skill inventory, or manifest SHA changes, even if no marketplace skill files are copied.

**Architecture:** Add `_discover_local_skills`, `_provenance_state`, and `_provenance_needs_update` helpers. Use a non-temporal provenance state comparison to decide when to rewrite, and include the new `localSkills` field in the written provenance. Keep the existing skill-copy and orphan-cleanup logic unchanged.

**Tech stack:** Python 3.12, pytest, `tools/run`.

## Global Constraints

- Source of truth for the skill is `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`.
- Projected copies under `codex-marketplace/plugins/*/skills/refreshing-installed-skills/` and `.agents/skills/refreshing-installed-skills/` are regenerated outputs.
- No third-party dependencies.
- LF line endings; use `newline="\n"` on file writes.
- Every code-changing task ends with a commit.
- Final green-path proof is `tools/run ci --check` and `tools/run marketplace --apply`.

---

### Task 1: Write failing tests

**Files:**
- Modify: `tests/test_refresh_installed_skills.py`

**Interfaces:**
- Consumes: existing `refresh_installed_skills` module-level fixtures (`AGENTS_SKILLS_PATH`, `PROVENANCE_PATH`, `_get_plugin_skills_path`, etc.).
- Produces: new test functions that fail before the implementation changes.

- [ ] **Step 1: Add a failing test for local skill discovery**

Append to `tests/test_refresh_installed_skills.py`:

```python
def test_discover_local_skills_sorted_and_validated(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    valid = skills_path / "mark-valid"
    valid.mkdir(parents=True)
    (valid / "SKILL.md").write_text(
        "---\nname: mark-valid\n---\n\n# Valid\n",
        encoding="utf-8",
    )
    invalid = skills_path / "mark-invalid"
    invalid.mkdir(parents=True)
    (invalid / "SKILL.md").write_text(
        "---\nname: not-the-directory-name\n---\n\n",
        encoding="utf-8",
    )
    (skills_path / "marketplace-skill").mkdir()

    with patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path):
        result = refresh_installed_skills._discover_local_skills(["mark-"])

    assert result == ["mark-valid"]
```

- [ ] **Step 2: Add a failing test for provenance rewrite on plugin-list-only change**

Append to `tests/test_refresh_installed_skills.py`:

```python
def test_provenance_rewritten_on_plugin_list_only_change(tmp_path: Path) -> None:
    skills_path = tmp_path / "installed"
    skills_path.mkdir()
    (skills_path / "marketplace-example").mkdir()
    (skills_path / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )
    provenance_path = skills_path / ".provenance.json"
    provenance_path.write_text(
        json.dumps(
            {
                "manifestSha": "current",
                "syncedAt": "2026-07-20T00:00:00",
                "syncedPlugins": ["repo-worker-pack"],
                "syncedSkills": 1,
                "localSkills": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    source_skills = tmp_path / "source" / "skills"
    source_skills.mkdir(parents=True)
    (source_skills / "marketplace-example").mkdir()
    (source_skills / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )

    plugins = [
        {"name": "repo-worker-pack"},
        {"name": "superpowers-plus"},
    ]

    with (
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": plugins}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=plugins),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(refresh_installed_skills.shared_checkout, "approve_mutation", return_value=True),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply", "--allow-shared-checkout"]),
    ):
        assert refresh_installed_skills.main() == 0

    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    assert provenance["syncedPlugins"] == ["repo-worker-pack", "superpowers-plus"]
    assert provenance["syncedSkills"] == 1
    assert provenance["localSkills"] == []
```

- [ ] **Step 3: Add a failing test for `localSkills` in provenance**

Append to `tests/test_refresh_installed_skills.py`:

```python
def test_provenance_records_local_skills(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    skills_path.mkdir()
    local_skill = skills_path / "mark-local"
    local_skill.mkdir()
    (local_skill / "SKILL.md").write_text(
        "---\nname: mark-local\n---\n\n# Local\n",
        encoding="utf-8",
    )
    provenance_path = skills_path / ".provenance.json"
    source_skills = tmp_path / "source" / "skills"
    source_skills.mkdir(parents=True)
    (source_skills / "marketplace-example").mkdir()
    (source_skills / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )
    (skills_path / "marketplace-example").mkdir()
    (skills_path / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )
    plugin = {"name": "example"}

    with (
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": [plugin]}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=[plugin]),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(refresh_installed_skills.shared_checkout, "approve_mutation", return_value=True),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply", "--allow-shared-checkout"]),
    ):
        assert refresh_installed_skills.main() == 0

    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    assert provenance["localSkills"] == ["mark-local"]
```

- [ ] **Step 4: Add a failing test for `--check` when provenance is stale**

Append to `tests/test_refresh_installed_skills.py`:

```python
def test_check_fails_when_provenance_plugin_list_stale(tmp_path: Path, capsys) -> None:
    skills_path = tmp_path / "installed"
    skills_path.mkdir()
    (skills_path / "marketplace-example").mkdir()
    (skills_path / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )
    provenance_path = skills_path / ".provenance.json"
    provenance_path.write_text(
        json.dumps(
            {
                "manifestSha": "current",
                "syncedAt": "2026-07-20T00:00:00",
                "syncedPlugins": ["repo-worker-pack"],
                "syncedSkills": 1,
                "localSkills": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    source_skills = tmp_path / "source" / "skills"
    source_skills.mkdir(parents=True)
    (source_skills / "marketplace-example").mkdir()
    (source_skills / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )

    plugins = [
        {"name": "repo-worker-pack"},
        {"name": "superpowers-plus"},
    ]

    with (
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": plugins}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=plugins),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--check"]),
    ):
        result = refresh_installed_skills.main()

    assert result == 1
    assert "CHECK: Changes would be made" in capsys.readouterr().out
```

- [ ] **Step 5: Update the no-diff test to use identical provenance state**

In `test_force_refresh_with_no_skill_changes_is_a_no_diff_operation`, change the `original` dict and the manifest SHA so the state is truly unchanged:

```python
    original = {
        "manifestSha": "current",
        "syncedAt": "2026-07-20T00:00:00",
        "syncedPlugins": ["repo-worker-pack", "superpowers-plus"],
        "syncedSkills": 0,
        "localSkills": [],
    }
```

And change the `_get_marketplace_manifest_sha` patch to return `"current"`:

```python
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="current"),
```

- [ ] **Step 6: Run the tests and confirm they fail for the right reasons**

Run:

```powershell
py -3 -m pytest tests/test_refresh_installed_skills.py -v
```

Expected: new tests fail because `_discover_local_skills`, `_provenance_state`, `_provenance_needs_update` are undefined or `localSkills` is not written.

---

### Task 2: Implement `_discover_local_skills`

**Files:**
- Modify: `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`

**Interfaces:**
- Produces: `def _discover_local_skills(prefixes: list[str]) -> list[str]`.

- [ ] **Step 1: Add the helper after `_validate_local_skill_dirs`**

```python
def _discover_local_skills(prefixes: list[str]) -> list[str]:
    """Return sorted, valid repo-local skill directory names."""
    if not AGENTS_SKILLS_PATH.is_dir():
        return []

    local_skills: list[str] = []
    for skill_dir in sorted(AGENTS_SKILLS_PATH.iterdir()):
        if not _is_local_skill_dir(skill_dir, prefixes):
            continue
        try:
            if _frontmatter_name(skill_dir) != skill_dir.name:
                continue
        except (
            FileNotFoundError,
            UnicodeDecodeError,
            ValueError,
            AttributeError,
            TypeError,
            yaml.YAMLError,
        ):
            continue
        local_skills.append(skill_dir.name)

    return sorted(local_skills)
```

- [ ] **Step 2: Run the `test_discover_local_skills_sorted_and_validated` test**

```powershell
py -3 -m pytest tests/test_refresh_installed_skills.py::test_discover_local_skills_sorted_and_validated -v
```

Expected: PASS.

- [ ] **Step 3: Commit**

```powershell
git add sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py tests/test_refresh_installed_skills.py
git commit -m "test(refresh): failing tests for provenance plugin-list and local-skill drift"
```

---

### Task 3: Implement provenance state and drift detection

**Files:**
- Modify: `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`

**Interfaces:**
- Produces:
  - `def _provenance_state(...) -> dict[str, Any]`
  - `def _provenance_needs_update(existing, new_state) -> bool`

- [ ] **Step 1: Add `_provenance_state` before `_write_provenance`**

```python
def _provenance_state(
    manifest_sha: str,
    installed_plugins: list[dict[str, Any]],
    synced_skill_count: int,
    local_skills: list[str],
) -> dict[str, Any]:
    """Return the non-temporal provenance fields for comparison and writing."""
    synced_plugins = [
        plugin.get("name", "unknown") if isinstance(plugin.get("name"), str) else "unknown"
        for plugin in installed_plugins
    ]

    local_plugins: list[dict[str, Any]] = []
    for plugin in installed_plugins:
        source = plugin.get("source", {}) if isinstance(plugin.get("source"), dict) else {}
        if source.get("source") == "local":
            name = plugin.get("name", "unknown")
            if not isinstance(name, str):
                name = "unknown"
            local_plugins.append(
                {
                    "name": name,
                    "path": source.get("path"),
                    "source": "local",
                }
            )

    return {
        "manifestSha": manifest_sha,
        "syncedPlugins": synced_plugins,
        "syncedSkills": synced_skill_count,
        "localSkills": local_skills,
        "marketplace": {
            "source": "HarleyBartles/agent-asset-marketplace",
            "sourcePath": "codex-marketplace/plugins",
        },
        "localPlugins": local_plugins,
        "marketplaceFile": ".agents/plugins/marketplace.json",
    }
```

- [ ] **Step 2: Add `_provenance_needs_update` next to it**

```python
def _provenance_needs_update(
    existing: dict[str, Any] | None, new_state: dict[str, Any]
) -> bool:
    """Return True if any non-temporal provenance field has changed."""
    if not existing:
        return True
    for key, value in new_state.items():
        if existing.get(key) != value:
            return True
    return False
```

- [ ] **Step 3: Update `_write_provenance` to use `_provenance_state` and accept `local_skills`**

Replace `_write_provenance` with:

```python
def _write_provenance(
    manifest_sha: str,
    installed_plugins: list[dict[str, Any]],
    synced_skill_count: int,
    local_skills: list[str],
) -> None:
    """Write provenance data.

    Distinguishes marketplace-derived plugins from repo-local plugins so the
    provenance file does not falsely attribute local plugins to the marketplace,
    and records repo-local skills under localSkills.
    """
    provenance = _provenance_state(manifest_sha, installed_plugins, synced_skill_count, local_skills)
    provenance["syncedAt"] = datetime.now().isoformat()

    with PROVENANCE_PATH.open("w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(provenance, indent=2) + "\n")
```

- [ ] **Step 4: Run the tests for the new helpers**

```powershell
py -3 -m pytest tests/test_refresh_installed_skills.py -v
```

Expected: PASS for `test_discover_local_skills_sorted_and_validated` and `test_provenance_records_local_skills`; others may still fail until `main()` is wired.

- [ ] **Step 5: Commit**

```powershell
git add sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py
git commit -m "feat(refresh): add provenance state, drift detection, and localSkills field"
```

---

### Task 4: Wire drift detection into `main()`

**Files:**
- Modify: `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`

**Interfaces:**
- Consumes: `_discover_local_skills`, `_provenance_state`, `_provenance_needs_update`, `_expected_marketplace_skill_inventory`.
- Produces: updated `main()` that rewrites provenance on drift.

- [ ] **Step 1: Compute local skills and provenance state before the early-exit check**

After:

```python
    installed_plugins = _get_installed_plugins(config)
```

Add:

```python
    local_skills = _discover_local_skills(prefixes)
    expected_skills = _expected_marketplace_skill_inventory(installed_plugins, prefixes)
    synced_skill_count = len(expected_skills)
```

- [ ] **Step 2: Replace the early-exit block**

Find:

```python
    # Check if refresh is needed based on provenance
    if not args.force and existing_provenance:
        if existing_provenance.get("manifestSha") == current_manifest_sha:
            if _marketplace_skill_inventory_is_current(installed_plugins, prefixes):
                print(f"Skills already synced at manifest SHA {current_manifest_sha}. Use --force to re-copy.")
                print(f"Synced skills: {existing_provenance.get('syncedSkills')} from {existing_provenance.get('syncedPlugins')} plugins.")
                return 0
```

Replace with:

```python
    # Check if refresh is needed based on provenance
    new_state = _provenance_state(current_manifest_sha, installed_plugins, synced_skill_count, local_skills)
    provenance_needs_update = _provenance_needs_update(existing_provenance, new_state)

    if not args.force and existing_provenance and not provenance_needs_update:
        if _marketplace_skill_inventory_is_current(installed_plugins, prefixes):
            print(f"Skills already synced at manifest SHA {current_manifest_sha}. Use --force to re-copy.")
            print(f"Synced skills: {existing_provenance.get('syncedSkills')} from {existing_provenance.get('syncedPlugins')} plugins.")
            return 0
```

- [ ] **Step 3: Fold provenance drift into `changes_made` and update the write call**

After the orphan-skill cleanup block, add:

```python
    # Provenance metadata drift (plugin list, local skills, manifest SHA) is also
    # a change worth reporting and writing.
    changes_made = changes_made or provenance_needs_update
```

Find:

```python
    # Write provenance only when the installed skill tree changed. A forced
    # byte-identical refresh must remain a no-diff operation.
    if not args.check and changes_made:
        _write_provenance(current_manifest_sha, installed_plugins, len(synced_skill_names))
        print(f"\nProvenance: {current_manifest_sha} -> {PROVENANCE_PATH}")
```

Replace with:

```python
    # Write provenance when the skill tree or provenance state changed. A forced
    # byte-identical refresh must remain a no-diff operation.
    if not args.check and changes_made:
        _write_provenance(current_manifest_sha, installed_plugins, synced_skill_count, local_skills)
        print(f"\nProvenance: {current_manifest_sha} -> {PROVENANCE_PATH}")
```

The final `if args.check:` and `else:` blocks already use `changes_made`, so no further edits are needed.

- [ ] **Step 4: Run the targeted tests**

```powershell
py -3 -m pytest tests/test_refresh_installed_skills.py -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```powershell
git add sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py
git commit -m "feat(refresh): rewrite provenance on plugin-list and local-skill drift"
```

---

### Task 5: Update the skill documentation

**Files:**
- Modify: `sources/first_party/skills/refreshing-installed-skills/SKILL.md`

**Interfaces:**
- Produces: updated Provenance section.

- [ ] **Step 1: Update the Provenance section**

Replace the current Provenance paragraph with:

```markdown
## Provenance

`.agents/skills/.provenance.json` records the marketplace-source version that was installed and the repo's local skill inventory. When the `marketplace-source` submodule is present, `manifestSha` tracks the submodule HEAD; otherwise it falls back to the consumer repo HEAD. `syncedPlugins` lists every plugin configured as `INSTALLED_BY_DEFAULT`, in order, regardless of whether its skills needed copying on this run. `syncedSkills` is the count of marketplace-derived skills. `localSkills` lists valid repo-local skill directories (matching `local_skill_prefixes`) sorted by name. The file is rewritten whenever any of those durable fields change, including a plugin-list-only change with no skill file updates.
```

- [ ] **Step 2: Commit**

```powershell
git add sources/first_party/skills/refreshing-installed-skills/SKILL.md
git commit -m "docs(refresh): document localSkills and provenance drift rewrite"
```

---

### Task 6: Regenerate marketplace surfaces

**Files:**
- Generated: `codex-marketplace/plugins/*/skills/refreshing-installed-skills/`, `.agents/skills/refreshing-installed-skills/`, `generated/skill-zips/refreshing-installed-skills.zip`, etc.

**Interfaces:**
- Consumes: `tools/run marketplace --apply`.

- [ ] **Step 1: Run the full marketplace regeneration**

```powershell
.\tools\run.ps1 marketplace --apply
```

- [ ] **Step 2: Inspect the diff to confirm only intended surfaces changed**

```powershell
git diff --stat
```

Expected changes:
- `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
- `sources/first_party/skills/refreshing-installed-skills/SKILL.md`
- `tests/test_refresh_installed_skills.py`
- Projected `refreshing-installed-skills` trees under `codex-marketplace/plugins/` and `.agents/skills/`
- `generated/skill-zips/refreshing-installed-skills.zip`
- `.agents/skills/.provenance.json` (now includes `localSkills`)

- [ ] **Step 3: Commit the regenerated surfaces**

```powershell
git add -A
git commit -m "chore(refresh): regenerate marketplace surfaces for provenance rewrite"
```

---

### Task 7: Run CI gate

**Files:**
- All repo surfaces.

**Interfaces:**
- Consumes: `tools/run ci --check`.

- [ ] **Step 1: Run the CI gate**

```powershell
.\tools\run.ps1 ci --check
```

- [ ] **Step 2: Run the focused test suite**

```powershell
py -3 -m pytest tests/test_refresh_installed_skills.py -v
```

- [ ] **Step 3: If any step fails, fix and re-run**

Do not claim completion until both commands pass cleanly.

---

### Task 8: Handoff-gate / plan-readiness

Before claiming the implementation is complete, rate the plan for execution confidence using the `handoff-gates` `plan-readiness` lane.

- [ ] **Step 1: Re-read the completed plan and spec**
- [ ] **Step 2: Score against the `plan-readiness` question: can an implementer execute this without improvising?**
- [ ] **Step 3: If below 8/10, strengthen gaps and re-rate; target 9/10**
- [ ] **Step 4: Record the final rating in the implementation report**

---

## Execution Handoff

After the plan is approved and the handoff-gate is satisfied, the implementer should:

1. Continue on the same worktree branch `fix/refreshing-installed-skills-provenance`.
2. Work through the tasks in order, checking each box.
3. Run `tools/run ci --check` and `tools/run marketplace --apply` before finishing.
4. Push the branch and open a PR with publication proof.
