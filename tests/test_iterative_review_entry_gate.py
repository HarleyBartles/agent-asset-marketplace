from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = (
    ROOT
    / "codex-marketplace"
    / "plugins"
    / "superpowers-plus"
    / "skills"
    / "iterative-review"
)


def test_legacy_iterative_review_is_not_implicitly_invoked() -> None:
    config = yaml.safe_load((SKILL_ROOT / "agents" / "openai.yaml").read_text())

    assert config["policy"]["allow_implicit_invocation"] is False
