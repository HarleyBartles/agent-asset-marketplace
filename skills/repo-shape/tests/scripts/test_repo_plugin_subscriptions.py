from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tomllib
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
    config.write_text(
        '[plugins."architecture-pack@wild-bunch-marketplace"]\nenabled = true\n'
        '[marketplaces.wild-bunch-marketplace]\nsource_type = "git"\n'
        'source = "https://github.com/example/wild-bunch.git"\nref = "main"\n',
        encoding="utf-8",
    )
    local_skill = root / ".agents/skills/repo-local-skill/SKILL.md"
    local_skill.parent.mkdir(parents=True)
    local_skill.write_text("---\nname: repo-local-skill\ndescription: local\n---\n", encoding="utf-8")


def test_accepts_codex_floating_ref_and_preserves_local_skills(tmp_path: Path) -> None:
    _consumer(tmp_path)

    assert subscriptions.validate(tmp_path) == []
    assert (tmp_path / ".agents/skills/repo-local-skill/SKILL.md").is_file()


@pytest.mark.parametrize(
    "registration",
    [
        "",
        '[marketplaces.other]\nsource_type = "git"\nsource = "https://github.com/example/wild-bunch.git"\n',
        '[marketplaces.wild-bunch-marketplace]\nsource_type = "local"\nsource = ".agents/plugins/marketplace.json"\n',
        '[marketplaces.wild-bunch-marketplace]\nsource_type = "git"\n',
        '[marketplaces.wild-bunch-marketplace]\nsource_type = "git"\nsource = "C:/catalog"\n',
        '[marketplaces.wild-bunch-marketplace]\nsource_type = "git"\nsource = "https:///repo.git"\n',
    ],
)
def test_rejects_missing_or_non_git_marketplace_registration(tmp_path: Path, registration: str) -> None:
    _consumer(tmp_path)
    config = tmp_path / ".codex/config.toml"
    config.write_text(
        '[plugins."architecture-pack@wild-bunch-marketplace"]\nenabled = true\n' + registration,
        encoding="utf-8",
    )

    assert any("marketplaces" in finding for finding in subscriptions.validate(tmp_path))


@pytest.mark.parametrize(
    "path",
    [
        "/plugins/game-studio",
        "C:/plugins/game-studio",
        ".//plugins/game-studio",
        "./C:/plugins/game-studio",
        "./C:plugins/game-studio",
        "./\\plugins/game-studio",
        "./\\\\server\\share\\plugins",
        "./plugins\\..\\escape",
    ],
)
def test_rejects_rooted_or_escaping_paths_in_both_path_syntaxes(tmp_path: Path, path: str) -> None:
    _consumer(tmp_path)
    catalog = tmp_path / ".agents/plugins/marketplace.json"
    data = json.loads(catalog.read_text(encoding="utf-8"))
    data["plugins"][0]["source"]["path"] = path
    catalog.write_text(json.dumps(data), encoding="utf-8")

    assert any("plugin-relative path" in finding for finding in subscriptions.validate(tmp_path))


@pytest.mark.parametrize("path", ["./plugins/game-studio", "./dist/plugins/architecture-pack"])
def test_accepts_relative_plugin_paths_with_git_registration(tmp_path: Path, path: str) -> None:
    _consumer(tmp_path)
    catalog = tmp_path / ".agents/plugins/marketplace.json"
    data = json.loads(catalog.read_text(encoding="utf-8"))
    data["plugins"][0]["source"]["path"] = path
    catalog.write_text(json.dumps(data), encoding="utf-8")

    assert subscriptions.validate(tmp_path) == []


@pytest.mark.parametrize(
    "mutate, message",
    [
        (lambda source: source.update(path="../escape"), "plugin-relative path"),
        (lambda source: source.update(ref="main", sha="a" * 40), "exactly one"),
        (lambda source: (source.pop("ref"), source.update(sha="not-a-commit")), "full hexadecimal Git commit"),
        (lambda source: source.update(url="https://example.com/archive.zip"), "Git repository URL"),
        (lambda source: source.update(url="https:///repo.git"), "Git repository URL"),
        (lambda source: source.update(url="https:// /repo.git"), "Git repository URL"),
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
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "remote", "add", "origin", "https://github.com/example/consumer.git"],
        check=True,
        capture_output=True,
    )
    (tmp_path / ".agents/plugins").mkdir(parents=True)
    existing = tmp_path / ".agents/plugins/marketplace.json"
    existing.write_text('{"name":"consumer","plugins":[],"repo":{"local_skills":["mine"]}}\n', encoding="utf-8")

    created = subscriptions.scaffold(tmp_path)

    assert created == [".codex/config.toml", ".devin/config.json"]
    assert existing.read_text(encoding="utf-8").endswith('"mine"]}}\n')
    assert (tmp_path / ".codex/config.toml").is_file()
    assert (tmp_path / ".devin/config.json").is_file()
    config = tomllib.loads((tmp_path / ".codex/config.toml").read_text(encoding="utf-8"))
    assert config["marketplaces"]["consumer"] == {
        "source_type": "git",
        "source": "https://github.com/example/consumer.git",
        "ref": "main",
    }
    assert subscriptions.validate(tmp_path) == []


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


def test_scaffold_requires_origin_before_creating_files(tmp_path: Path) -> None:
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)

    with pytest.raises(ValueError, match="Git origin"):
        subscriptions.scaffold(tmp_path)

    assert not (tmp_path / ".agents/plugins/marketplace.json").exists()
    assert not (tmp_path / ".codex/config.toml").exists()


def test_scaffold_registers_a_new_catalog_from_git_origin(tmp_path: Path) -> None:
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "remote", "add", "origin", "git@example.com:consumer.git"],
        check=True,
        capture_output=True,
    )

    assert subscriptions.scaffold(tmp_path) == [
        ".agents/plugins/marketplace.json",
        ".codex/config.toml",
        ".devin/config.json",
    ]
    config = tomllib.loads((tmp_path / ".codex/config.toml").read_text(encoding="utf-8"))
    assert config["marketplaces"]["consumer-repo"]["source"] == "git@example.com:consumer.git"
    assert subscriptions.validate(tmp_path) == []


def test_scaffold_preserves_existing_codex_configuration(tmp_path: Path) -> None:
    _consumer(tmp_path)
    config = tmp_path / ".codex/config.toml"
    before = config.read_bytes()

    assert subscriptions.scaffold(tmp_path) == [".devin/config.json"]
    assert config.read_bytes() == before
    assert subscriptions.validate(tmp_path) == []
