from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import validate_marketplace  # noqa: E402


def _policy() -> dict:
    return {"install_defaults": []}


def _registry() -> dict:
    return {"plugins": [{"name": "writing-pack", "policy": {"installation": "AVAILABLE"}}]}


def test_repo_authored_skills_need_no_marketplace_subscription(tmp_path: Path) -> None:
    local_skill = tmp_path / ".agents" / "skills" / "local-skill"
    local_skill.mkdir(parents=True)
    (local_skill / "SKILL.md").write_text("---\nname: local-skill\n---\n", encoding="utf-8")

    validate_marketplace.validate_installation_policy(_policy(), _registry())


def test_generated_marketplace_has_no_repo_local_skill_registry() -> None:
    manifests = [{"name": spec["name"]} for spec in validate_marketplace.MARKETPLACE_PLUGIN_SPECS]

    assert "repo" not in validate_marketplace.build_marketplace_manifest(manifests)


@pytest.mark.parametrize(
    ("policy", "registry", "message"),
    [
        ({"install_defaults": ["writing-pack"]}, _registry(), "install_defaults"),
        ({"install_defaults": [], "local_skills": []}, _registry(), "must not declare local_skills"),
        (_policy(), {**_registry(), "repo": {"local_skills": []}}, "must not declare repo.local_skills"),
        (
            _policy(),
            {"plugins": [{"name": "writing-pack", "policy": {"installation": "INSTALLED_BY_DEFAULT"}}]},
            "INSTALLED_BY_DEFAULT",
        ),
    ],
)
def test_marketplace_installation_policy_rejects_legacy_skill_or_default_fields(
    policy: dict, registry: dict, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        validate_marketplace.validate_installation_policy(policy, registry)
