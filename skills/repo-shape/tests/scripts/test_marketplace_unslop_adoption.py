from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "skills/repo-shape/scripts"))

import unslop_standard  # noqa: E402


def test_marketplace_explicitly_adopts_unslop_without_plugin_subscription() -> None:
    standards = json.loads((ROOT / ".agents/contracts/operating-standards.json").read_text(encoding="utf-8"))
    adoption = next(item for item in standards["standards"] if item["id"] == "unslop")
    assert re.fullmatch(r"[0-9a-f]{40}", adoption["revision"])

    contract_path = ROOT / ".agents/contracts/unslop.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    assert contract == {"version": 1, "profile_roots": [".agents/unslop"]}
    assert (ROOT / ".agents/unslop/repository.md").is_file()
    assert unslop_standard.validate(ROOT) == []

    assert adoption["requires"] == []


def test_marketplace_profile_routes_only_its_declared_workflows() -> None:
    profile = ROOT / ".agents/unslop/repository.md"
    text = profile.read_text(encoding="utf-8")
    assert text.startswith("# Unslop Profile: repository\n")
    for path in (
        ".agents/runbooks/planning.md",
        ".agents/runbooks/implementing.md",
        ".agents/runbooks/code-review.md",
        ".agents/runbooks/pr.md",
    ):
        workflow = ROOT / path
        assert f"](../runbooks/{workflow.name})" in text
        content = workflow.read_text(encoding="utf-8")
        section = content.split("## Unslop profile routing", 1)[1].split("\n## ", 1)[0]
        assert "$unslop-profiles" in section
