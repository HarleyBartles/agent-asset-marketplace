import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from marketplace.definitions import DefinitionError, load_marketplace


def _write(root: Path, relative: str, value: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def _fixture(root: Path) -> None:
    _write(root, "skills/shared-skill/SKILL.md", "# Shared skill\n")
    _write(root, "shared/references/reusable.md", "# Reference\n")
    for plugin in ("alpha", "beta"):
        _write(
            root,
            f"src/plugin-definitions/{plugin}/plugin.json",
            json.dumps({"name": plugin, "version": "1.0.0", "license": "MIT"}),
        )
        _write(
            root,
            f"src/plugin-definitions/{plugin}/contents.json",
            json.dumps(
                {
                    "skills": [
                        {
                            "name": "shared-skill",
                            "resources": [
                                {
                                    "source": "reusable-reference",
                                    "destination": "references/reusable.md",
                                }
                            ],
                        }
                    ]
                }
            ),
        )
    _write(
        root,
        "resources.json",
        json.dumps({"reusable-reference": "references/reusable.md"}),
    )


def test_one_skill_can_be_in_two_plugins_and_share_a_resource(tmp_path: Path) -> None:
    _fixture(tmp_path)

    marketplace = load_marketplace(tmp_path)

    assert set(marketplace.plugins) == {"alpha", "beta"}
    for plugin in marketplace.plugins.values():
        skill = plugin.skills[0]
        assert skill.source == (tmp_path / "skills/shared-skill").resolve()
        assert skill.resources[0].source == (tmp_path / "shared/references/reusable.md").resolve()
        assert skill.resources[0].destination == Path("references/reusable.md")


@pytest.mark.parametrize(
    ("contents", "resource_map", "message"),
    [
        (
            [{"name": "shared-skill", "resources": [{"source": "reusable-reference", "destination": "SKILL.md"}]}],
            {"reusable-reference": "references/reusable.md"},
            "destination collision",
        ),
        ([{"name": "missing-skill", "resources": []}], {}, "unknown skill"),
        (
            [{"name": "shared-skill", "resources": [{"source": "missing", "destination": "references/m.md"}]}],
            {},
            "unknown resource",
        ),
        ([{"name": "../shared-skill", "resources": []}], {}, "must be a declared skill"),
    ],
)
def test_invalid_compositions_report_actionable_errors(
    tmp_path: Path, contents: list[dict], resource_map: dict, message: str
) -> None:
    _fixture(tmp_path)
    definition = tmp_path / "src/plugin-definitions/alpha/contents.json"
    definition.write_text(json.dumps({"skills": contents}), encoding="utf-8")
    (tmp_path / "src/plugin-definitions/beta/contents.json").write_text(json.dumps({"skills": []}), encoding="utf-8")
    (tmp_path / "resources.json").write_text(json.dumps(resource_map), encoding="utf-8")

    with pytest.raises(DefinitionError, match=message):
        load_marketplace(tmp_path)


def test_source_paths_cannot_escape_their_declared_roots(tmp_path: Path) -> None:
    _fixture(tmp_path)
    (tmp_path / "resources.json").write_text(json.dumps({"reusable-reference": "../outside.md"}), encoding="utf-8")

    with pytest.raises(DefinitionError, match="escapes shared root"):
        load_marketplace(tmp_path)
