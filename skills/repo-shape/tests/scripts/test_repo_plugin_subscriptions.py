from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "skills/repo-shape/scripts"))
SCRIPT = ROOT / "skills/repo-shape/scripts/repo_plugin_subscriptions.py"
spec = importlib.util.spec_from_file_location("repo_plugin_subscriptions", SCRIPT)
assert spec and spec.loader
subscriptions = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = subscriptions
spec.loader.exec_module(subscriptions)

scaffold_spec = importlib.util.spec_from_file_location(
    "scaffold_operating_standards", ROOT / "skills/repo-shape/scripts/scaffold_operating_standards.py"
)
assert scaffold_spec and scaffold_spec.loader
scaffold = importlib.util.module_from_spec(scaffold_spec)
sys.modules[scaffold_spec.name] = scaffold
scaffold_spec.loader.exec_module(scaffold)


def _consumer(root: Path) -> None:
    marketplace = root / ".agents/plugins/marketplace.json"
    marketplace.parent.mkdir(parents=True)
    marketplace.write_text(
        json.dumps(
            {
                "name": "wild-bunch-marketplace",
                "plugins": [
                    {
                        "name": "architecture-pack",
                        "source": {
                            "source": "git-subdir",
                            "url": "https://github.com/example/agent-asset-marketplace.git",
                            "path": "./dist/plugins/architecture-pack",
                            "ref": "main",
                        },
                    }
                ],
                "repo": {"local_skills": ["repo-local-skill"]},
            }
        ),
        encoding="utf-8",
    )
    config = root / ".codex/config.toml"
    config.parent.mkdir(parents=True)
    config.write_text('[plugins."architecture-pack@wild-bunch-marketplace"]\nenabled = true\n', encoding="utf-8")
    local_skill = root / ".agents/skills/repo-local-skill/SKILL.md"
    local_skill.parent.mkdir(parents=True)
    local_skill.write_text("---\nname: repo-local-skill\ndescription: local\n---\n", encoding="utf-8")


def test_accepts_codex_floating_ref_and_preserves_local_skills(tmp_path: Path) -> None:
    _consumer(tmp_path)

    assert subscriptions.validate(tmp_path) == []
    assert (tmp_path / ".agents/skills/repo-local-skill/SKILL.md").is_file()


@pytest.mark.parametrize(
    "mutate, message",
    [
        (lambda source: source.update(path="../escape"), "plugin-relative path"),
        (lambda source: source.update(ref="main", sha="a" * 40), "exactly one"),
        (lambda source: (source.pop("ref"), source.update(sha="not-a-commit")), "full hexadecimal Git commit"),
        (lambda source: source.update(url="https://example.com/archive.zip"), "Git repository URL"),
        (lambda source: source.update(url="https:///repo.git"), "Git repository URL"),
    ],
)
def test_rejects_invalid_plugin_source(tmp_path: Path, mutate, message: str) -> None:
    _consumer(tmp_path)
    path = tmp_path / ".agents/plugins/marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    mutate(data["plugins"][0]["source"])
    path.write_text(json.dumps(data), encoding="utf-8")

    assert any(message in finding for finding in subscriptions.validate(tmp_path))


def test_rejects_duplicate_plugin_identity_and_unmatched_activation(tmp_path: Path) -> None:
    _consumer(tmp_path)
    path = tmp_path / ".agents/plugins/marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["plugins"].append(data["plugins"][0])
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("duplicates plugin identity" in finding for finding in subscriptions.validate(tmp_path))

    data["plugins"] = data["plugins"][:1]
    path.write_text(json.dumps(data), encoding="utf-8")
    config = tmp_path / ".codex/config.toml"
    config.write_text('[plugins."missing@wild-bunch-marketplace"]\nenabled = true\n', encoding="utf-8")
    assert any("has no matching marketplace plugin" in finding for finding in subscriptions.validate(tmp_path))


def test_scaffold_creates_missing_native_files_without_overwriting_local_configs(tmp_path: Path) -> None:
    (tmp_path / ".agents/plugins").mkdir(parents=True)
    existing = tmp_path / ".agents/plugins/marketplace.json"
    existing.write_text('{"name":"consumer","plugins":[],"repo":{"local_skills":["mine"]}}\n', encoding="utf-8")

    created = subscriptions.scaffold(tmp_path)

    assert created == [".codex/config.toml", ".devin/config.json"]
    assert existing.read_text(encoding="utf-8").endswith('"mine"]}}\n')
    assert (tmp_path / ".codex/config.toml").is_file()
    assert (tmp_path / ".devin/config.json").is_file()


def test_operating_standard_catalog_resolves_from_installed_plugin_without_submodule(
    tmp_path: Path, monkeypatch
) -> None:
    plugin_root = tmp_path / "cache/agent-operating-model"
    skill_root = plugin_root / "skills/repo-shape"
    references = skill_root / "references"
    references.mkdir(parents=True)
    catalog_path = references / "operating-standards-catalog.json"
    manifest_path = references / "repository-shape-manifest.json"
    catalog_path.write_text("{}", encoding="utf-8")
    manifest_path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(scaffold, "_SKILL_ROOT", skill_root)
    monkeypatch.setattr(scaffold, "_CATALOG_PATH", catalog_path)
    monkeypatch.setattr(scaffold, "_MANIFEST_PATH", manifest_path)

    assert scaffold._source_root(tmp_path / "consumer") == plugin_root
