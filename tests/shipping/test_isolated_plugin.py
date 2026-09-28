import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from marketplace.build import build_marketplace


def _write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def assert_plugin_is_self_contained(plugin: Path) -> None:
    """Reject symlinks that depend on the source checkout after installation."""
    assert (plugin / ".codex-plugin/plugin.json").is_file()
    for path in plugin.rglob("*"):
        assert not path.is_symlink(), f"installed plugin contains a filesystem dependency: {path}"


def test_built_plugin_can_be_inspected_as_an_isolated_install(tmp_path: Path) -> None:
    _write(tmp_path, "skills/guide/SKILL.md", "# Guide\n")
    _write(tmp_path, "src/plugin-definitions/guide/plugin.json", json.dumps({"name": "guide", "version": "1.0.0"}))
    _write(tmp_path, "src/plugin-definitions/guide/contents.json", json.dumps({"skills": [{"name": "guide"}]}))
    _write(tmp_path, "resources.json", "{}")
    (tmp_path / "shared").mkdir()

    build_marketplace(tmp_path, apply=True)
    assert_plugin_is_self_contained(tmp_path / "dist/plugins/guide")
