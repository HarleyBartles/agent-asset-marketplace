import json
import os
import stat
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from marketplace.build import BuildError, build_marketplace


def _write(root: Path, relative: str, value: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def _source(root: Path) -> None:
    _write(root, "skills/shared-skill/SKILL.md", "# Shared skill\nSee [reference](references/guide.md).\n")
    _write(root, "skills/shared-skill/tests/pressure/case.md", "# Pressure case\n")
    _write(root, "skills/shared-skill/tests/evaluator-only/rubric.md", "# Hidden rubric\n")
    _write(root, "shared/references/guide.md", "# Guide\nExact source bytes.\n")
    for name in ("alpha", "beta"):
        definition = root / "src/plugin-definitions" / name
        _write(
            definition,
            "plugin.json",
            json.dumps(
                {
                    "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
                    "name": name,
                    "version": "1.0.0",
                    "license": "MIT",
                    "extensions": {"com.openai": {"interface": {"displayName": name}}},
                }
            ),
        )
        _write(definition, "bundle.json", json.dumps({"bundle_name": name, "source_families": ["first_party"]}))
        _write(definition, "files/LICENSE", "MIT notice\n")
        _write(
            definition,
            "contents.json",
            json.dumps(
                {
                    "skills": [
                        {
                            "name": "shared-skill",
                            "provenance": {"source_category": "first_party", "source_license": "MIT"},
                            "resources": [{"source": "guide", "destination": "references/guide.md"}],
                        }
                    ]
                }
            ),
        )
    _write(root, "resources.json", json.dumps({"guide": "references/guide.md"}))


def _tree(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)).replace("\\", "/"): path.read_bytes() for path in root.rglob("*") if path.is_file()
    }


def test_build_packages_complete_copies_and_check_mode_is_read_only(tmp_path: Path) -> None:
    _source(tmp_path)

    assert build_marketplace(tmp_path, apply=True)
    output = tmp_path / "dist/plugins"
    for name in ("alpha", "beta"):
        package = output / name
        manifest = json.loads((package / "plugin.json").read_text(encoding="utf-8"))
        assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
        assert manifest["name"] == name
        assert "skills" not in manifest and "interface" not in manifest
        assert manifest["extensions"]["com.openai"]["interface"]
        compatibility = json.loads((package / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        assert compatibility["skills"] == "./skills/"
        assert compatibility["interface"] == manifest["extensions"]["com.openai"]["interface"]
        assert not (package / ".claude-plugin").exists()
        assert (package / "LICENSE").read_bytes() == (
            tmp_path / "src/plugin-definitions" / name / "files/LICENSE"
        ).read_bytes()
        assert (package / "skills/shared-skill/SKILL.md").read_bytes() == (
            tmp_path / "skills/shared-skill/SKILL.md"
        ).read_bytes()
        assert (package / "skills/shared-skill/references/guide.md").read_bytes() == (
            tmp_path / "shared/references/guide.md"
        ).read_bytes()
        assert (package / "skills/shared-skill/tests/pressure/case.md").read_bytes() == (
            tmp_path / "skills/shared-skill/tests/pressure/case.md"
        ).read_bytes()
        assert not (package / "skills/shared-skill/tests/evaluator-only").exists()
        assert not any("shared/" in part or "src/plugin-definitions" in part for part in _tree(package))
        bundle = json.loads((package / "references/bundle-manifest.json").read_text(encoding="utf-8"))
        assert bundle["entries"][0]["canonical_source_path"] == "skills/shared-skill"
        assert bundle["entries"][0]["source_path"] == "skills/shared-skill/SKILL.md"
        assert bundle["entries"][0]["local_path"] == "skills/shared-skill"
        assert bundle["entries"][0]["source_category"] == "first_party"

    first = _tree(tmp_path / "dist")
    assert build_marketplace(tmp_path, apply=True)
    assert _tree(tmp_path / "dist") == first
    assert build_marketplace(tmp_path, apply=False)


def test_check_mode_reports_stale_output_without_mutating_it(tmp_path: Path) -> None:
    _source(tmp_path)
    output = tmp_path / "dist/plugins/alpha/stale.txt"
    output.parent.mkdir(parents=True)
    output.write_text("stale", encoding="utf-8")

    with pytest.raises(BuildError, match="stale"):
        build_marketplace(tmp_path, apply=False)
    assert output.read_text(encoding="utf-8") == "stale"


def test_empty_plugin_is_built_without_skills(tmp_path: Path) -> None:
    _source(tmp_path)
    definition = tmp_path / "src/plugin-definitions/empty"
    _write(
        definition,
        "plugin.json",
        json.dumps(
            {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
                "name": "empty",
                "version": "1.0.0",
            }
        ),
    )
    _write(definition, "contents.json", json.dumps({"skills": []}))

    build_marketplace(tmp_path, apply=True)

    package = tmp_path / "dist/plugins/empty"
    assert json.loads((package / "plugin.json").read_text(encoding="utf-8"))["name"] == "empty"
    assert (package / ".codex-plugin/plugin.json").is_file()
    assert not (package / ".claude-plugin").exists()


def test_build_preserves_executable_bits_for_shipped_hook_assets(tmp_path: Path) -> None:
    if os.name == "nt":
        pytest.skip("Windows does not expose POSIX executable bits through filesystem metadata")

    _source(tmp_path)
    source = tmp_path / "skills/shared-skill/assets/pre-commit"
    source.parent.mkdir(parents=True)
    source.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
    source.chmod(source.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    build_marketplace(tmp_path, apply=True)

    packaged = tmp_path / "dist/plugins/alpha/skills/shared-skill/assets/pre-commit"
    assert stat.S_IMODE(packaged.stat().st_mode) & stat.S_IXUSR
