from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "assets" / "check_plugin_subscriptions.py"
SHA = "0123456789abcdef0123456789abcdef01234567"


def _write_codex(root: Path, *, path: str = "./plugins/review-tools", selectors: str = '"ref": "main"') -> None:
    catalog = {
        "name": "sample-repo-plugins",
        "plugins": [
            {
                "name": "review-tools",
                "source": {
                    "source": "git-subdir",
                    "url": "https://github.com/example-org/agent-plugins.git",
                    "path": path,
                    **json.loads("{" + selectors + "}"),
                },
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Coding",
            }
        ],
    }
    catalog_path = root / ".agents/plugins/marketplace.json"
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
    codex = root / ".codex/config.toml"
    codex.parent.mkdir(parents=True, exist_ok=True)
    codex.write_text(
        '[marketplaces.sample-repo-plugins]\nsource_type = "git"\n'
        'source = "https://github.com/example-org/sample-repo.git"\nref = "main"\n\n'
        '[plugins."review-tools@sample-repo-plugins"]\nenabled = true\n',
        encoding="utf-8",
    )


def _check(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(root), "--check"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def test_accepts_codex_and_devin_native_git_subdirectory_declarations(tmp_path: Path) -> None:
    _write_codex(tmp_path)
    devin = tmp_path / ".devin/config.json"
    devin.parent.mkdir(parents=True)
    devin.write_text(
        json.dumps(
            {
                "requiredPlugins": [
                    {
                        "source": "git-subdir",
                        "url": "https://github.com/example-org/agent-plugins.git",
                        "path": "plugins/review-tools",
                        "ref": "main",
                    },
                    {
                        "source": "git-subdir",
                        "url": "https://github.com/example-org/agent-plugins.git",
                        "path": "plugins/test-tools",
                        "sha": SHA,
                    },
                ],
                "optionalPlugins": [],
                "forbiddenPlugins": [],
            }
        ),
        encoding="utf-8",
    )

    result = _check(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "codex: checked" in result.stdout.lower()
    assert "devin: checked" in result.stdout.lower()
    assert "does not fetch" in result.stdout.lower()
    assert "authentication" in result.stdout.lower()


def test_catalog_can_offer_inactive_plugin_without_making_it_a_dependency(tmp_path: Path) -> None:
    _write_codex(tmp_path)
    catalog_path = tmp_path / ".agents/plugins/marketplace.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog["plugins"].append(
        {
            "name": "optional-linter",
            "source": {
                "source": "git-subdir",
                "url": "https://github.com/example-org/agent-plugins.git",
                "path": "./plugins/optional-linter",
                "ref": "main",
            },
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        }
    )
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")

    result = _check(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "local declarations are syntactically consistent" in result.stdout.lower()


def test_shipped_codex_and_devin_examples_are_consistent(tmp_path: Path) -> None:
    assets = SCRIPT.parents[1] / "assets/examples"
    targets = {
        "marketplace.json.example": tmp_path / ".agents/plugins/marketplace.json",
        "codex-config.toml.example": tmp_path / ".codex/config.toml",
        "devin-config.json.example": tmp_path / ".devin/config.json",
    }
    for source_name, target in targets.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(assets / source_name, target)

    result = _check(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr


def test_accepts_sha_or_ref_but_rejects_both_selectors(tmp_path: Path) -> None:
    _write_codex(tmp_path, selectors=f'"sha": "{SHA}"')
    accepted = _check(tmp_path)
    _write_codex(tmp_path, selectors=f'"ref": "main", "sha": "{SHA}"')
    rejected = _check(tmp_path)

    assert accepted.returncode == 0, accepted.stdout + accepted.stderr
    assert rejected.returncode == 1
    assert "exactly one" in rejected.stdout.lower()


def test_rejects_malformed_catalog_toml_and_conflicting_activation(tmp_path: Path) -> None:
    _write_codex(tmp_path)
    config = tmp_path / ".codex/config.toml"
    config.write_text("[marketplaces.sample-repo-plugins\n", encoding="utf-8")
    malformed = _check(tmp_path)
    assert malformed.returncode == 1 and "toml" in malformed.stdout.lower()

    _write_codex(tmp_path)
    config.write_text(
        '[marketplaces.sample-repo-plugins]\nsource_type = "git"\n'
        'source = "https://github.com/example-org/sample-repo.git"\nref = "main"\n\n'
        '[plugins."missing@sample-repo-plugins"]\nenabled = true\n',
        encoding="utf-8",
    )
    conflict = _check(tmp_path)

    assert conflict.returncode == 1
    assert "no matching catalog entry" in conflict.stdout.lower()


def test_rejects_malformed_catalog_and_devin_json(tmp_path: Path) -> None:
    catalog = tmp_path / ".agents/plugins/marketplace.json"
    catalog.parent.mkdir(parents=True)
    catalog.write_text('{"name":', encoding="utf-8")
    catalog_result = _check(tmp_path)
    assert catalog_result.returncode == 1 and "catalog json" in catalog_result.stdout.lower()

    config = tmp_path / ".devin/config.json"
    config.parent.mkdir(parents=True)
    config.write_text('{"requiredPlugins": [}', encoding="utf-8")
    devin_result = _check(tmp_path)
    assert devin_result.returncode == 1 and "invalid json" in devin_result.stdout.lower()


def test_rejects_escaping_catalog_path_and_malformed_devin_declaration(tmp_path: Path) -> None:
    _write_codex(tmp_path, path="./plugins/../outside")
    path_error = _check(tmp_path)
    assert path_error.returncode == 1 and "path" in path_error.stdout.lower()

    _write_codex(tmp_path)
    devin = tmp_path / ".devin/config.json"
    devin.parent.mkdir(parents=True, exist_ok=True)
    devin.write_text(
        json.dumps(
            {
                "requiredPlugins": [
                    {
                        "source": "git-subdir",
                        "url": "https://example.com/x.git",
                        "path": "plugins/x",
                        "ref": "main",
                        "sha": SHA,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    selectors = _check(tmp_path)

    assert selectors.returncode == 1
    assert "devin" in selectors.stdout.lower() and "exactly one" in selectors.stdout.lower()


def test_checks_only_present_harness_surfaces_and_does_not_modify_repository(tmp_path: Path) -> None:
    before = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*") if path.is_file())

    result = _check(tmp_path)

    after = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*") if path.is_file())
    assert result.returncode == 0, result.stdout + result.stderr
    assert "codex: not present" in result.stdout.lower()
    assert "devin: not present" in result.stdout.lower()
    assert before == after
