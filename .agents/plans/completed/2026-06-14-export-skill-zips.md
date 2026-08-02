# Export Skill Zips Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add a copy-only export command that turns canonical `generated/skill-zips/` artifacts into a GPT-upload-ready worker output directory with a manifest.

**Architecture:** Keep packaging and export separate. Reuse the canonical registry/artifact helpers in `tools/skill_zip_artifacts.py` for discovery, validation, and registry lookups, then add a standalone `tools/export_skill_zips.py` that copies already-built `skill.zip` files into `<out>/<skill-name>/skill.zip` and writes `export-manifest.json`.

**Tech Stack:** Python 3, `argparse`, `json`, `pathlib`, `shutil`, `tempfile`, `hashlib`.

---

### Task 1: Lock the export contract in a validation script

**Files:**
- Create: `tools/validate_export_skill_zips.py`

- [x] **Step 1: Write the failing test**

```python
def test_export_happy_path_and_error_cases(tmp_path):
    from export_skill_zips import main

    out_dir = tmp_path / "worker-output"
    sample_manifest = run_export(main, ["--pack", "house-skills", "--out", str(out_dir)])

    assert (out_dir / "skill-installer" / "skill.zip").is_file()
    assert sample_manifest["request"]["form"] == "pack"
    assert sample_manifest["copied"][0]["output_path"].endswith("skill.zip")
```

- [x] **Step 2: Run test to verify it fails**

Run: `py -3 tools/validate_export_skill_zips.py`
Expected: fail because `export_skill_zips.py` does not exist yet.

- [x] **Step 3: Write minimal implementation**

No production code yet. Keep this script as the first consumer of the new exporter and its manifest.

- [x] **Step 4: Run test to verify it passes**

Run: `py -3 tools/validate_export_skill_zips.py`
Expected: PASS after the exporter exists.

- [x] **Step 5: Commit**

```bash
git add tools/validate_export_skill_zips.py
git commit -m "test: add export skill zip validation coverage"
```

### Task 2: Add the standalone exporter with copy-only behavior

**Files:**
- Create: `tools/export_skill_zips.py`
- Modify: `tools/skill_zip_artifacts.py`

- [x] **Step 1: Write the failing test**

```python
def test_export_requires_pack_scoped_resolution_for_duplicate_skill_names(tmp_path):
    result = run_export_cli([
        "--skills",
        "linear",
        "--out",
        str(tmp_path / "out"),
    ])

    assert result.returncode != 0
    assert "<pack>/linear" in result.stderr
```

- [x] **Step 2: Run test to verify it fails**

Run: `py -3 tools/validate_export_skill_zips.py`
Expected: fail until the exporter resolves pack-scoped and bare-name requests correctly.

- [x] **Step 3: Write minimal implementation**

Implement:

```python
def main() -> int:
    parser = argparse.ArgumentParser(...)
    # --pack, --skills, --from-file, --out, --clean-output, --check, --refresh
    ...

def resolve_export_requests(...):
    ...

def export_skill_zips(...):
    # copy existing skill.zip files only
    # fail on ambiguous bare names for --skills
    # fail on duplicate output folders for colliding explicit requests
    # write export-manifest.json
```

In `tools/skill_zip_artifacts.py`, add only the smallest helper surface needed for registry lookup and validation reuse, such as:

```python
def load_skill_zip_registry() -> dict[str, Any]:
    return load_registry()

def registry_artifacts_by_pack_and_skill(registry: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    ...

def registry_artifacts_by_skill(registry: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    ...
```

- [x] **Step 4: Run test to verify it passes**

Run: `py -3 tools/validate_export_skill_zips.py`
Expected: PASS with copied `skill.zip` files and a written manifest.

- [x] **Step 5: Commit**

```bash
git add tools/export_skill_zips.py tools/skill_zip_artifacts.py
git commit -m "feat: add skill zip export command"
```

### Task 3: Document worker usage and validate the repo

**Files:**
- Modify: `tools/README.md`
- Modify: `tools/validate_marketplace.py` if needed to keep tool docs aligned with the new exporter

- [x] **Step 1: Write the failing test**

```python
def test_tools_readme_mentions_export_batch_command():
    text = Path("tools/README.md").read_text(encoding="utf-8")
    assert "export_skill_zips.py" in text
    assert "worker-output/<issue>/<name>" in text
```

- [x] **Step 2: Run test to verify it fails**

Run: `py -3 tools/validate_export_skill_zips.py`
Expected: fail until the README mentions the worker command.

- [x] **Step 3: Write minimal implementation**

Add a short usage snippet to `tools/README.md` showing the common worker flow:

```text
python tools/export_skill_zips.py --skills <pack>/<skill>,<pack>/<skill> --out worker-output/<issue>/<name> --clean-output
```

- [x] **Step 4: Run test to verify it passes**

Run:

```bash
py -3 tools/validate_export_skill_zips.py
py -3 tools/validate_marketplace.py
git diff --check HEAD~1 HEAD
```

Expected: all pass; export tooling remains copy-only and the repo validation still sees a consistent marketplace surface.

- [x] **Step 5: Commit**

```bash
git add tools/README.md tools/validate_marketplace.py
git commit -m "docs: document skill zip export usage"
```
