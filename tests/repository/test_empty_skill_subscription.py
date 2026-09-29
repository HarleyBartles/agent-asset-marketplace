from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import validate_marketplace  # noqa: E402


def _policy() -> dict:
    return {"install_defaults": [], "local_skills": []}


def _registry() -> dict:
    return {
        "plugins": [{"name": "writing-pack", "policy": {"installation": "AVAILABLE"}}],
        "repo": {"local_skills": []},
    }


def test_empty_skill_subscription_accepts_absent_projection(tmp_path: Path) -> None:
    validate_marketplace.validate_empty_skill_subscription(_policy(), _registry(), tmp_path / ".agents" / "skills")


@pytest.mark.parametrize(
    ("policy", "registry", "projection", "message"),
    [
        ({"install_defaults": ["writing-pack"], "local_skills": []}, _registry(), False, "install_defaults"),
        ({"install_defaults": [], "local_skills": ["local-skill"]}, _registry(), False, "local_skills"),
        (
            _policy(),
            {
                "plugins": [{"name": "writing-pack", "policy": {"installation": "INSTALLED_BY_DEFAULT"}}],
                "repo": {"local_skills": []},
            },
            False,
            "INSTALLED_BY_DEFAULT",
        ),
        (_policy(), _registry(), True, ".agents/skills"),
    ],
)
def test_empty_skill_subscription_rejects_repo_owned_skill_state(
    tmp_path: Path, policy: dict, registry: dict, projection: bool, message: str
) -> None:
    skills = tmp_path / ".agents" / "skills"
    if projection:
        skills.mkdir(parents=True)
    with pytest.raises(ValueError, match=message):
        validate_marketplace.validate_empty_skill_subscription(policy, registry, skills)
