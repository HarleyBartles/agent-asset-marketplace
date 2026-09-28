from __future__ import annotations
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SKILLS = ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "skills"

REPO_SKILLS = ROOT / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills"

OPERATING_SKILLS = ROOT / "codex-marketplace" / "plugins" / "agent-operating-model" / "skills"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestAuthorityBootstrapPortability:
    def test_superpowers_plus_version_matches_pinned_upstream_release(self):
        plugin = json.loads(_read(SKILLS.parent / ".codex-plugin" / "plugin.json"))
        bundle = json.loads(_read(SKILLS.parent / "references" / "bundle-manifest.json"))
        source = _read(SKILLS.parent / "SOURCE.md")
        assert plugin["version"] == "6.4.1"
        assert bundle["bundle_version"] == "6.4.1"
        assert "5bf4e78011075bcfc0dc295f0724994cd123ee71" in source

    def test_superpowers_plus_retains_first_party_helper_inventory(self):
        bundle = json.loads(_read(SKILLS.parent / "references" / "bundle-manifest.json"))
        names = {entry["canonical_name"] for entry in bundle["entries"]}
        assert {
            "asking-clarifying-questions",
            "handoff-gates",
            "inspecting-the-environment",
            "iterative-review",
            "publishing-source",
            "selecting-a-subagent",
            "subagent-workspace",
            "writing-roadmaps",
        } <= names

    def test_superpowers_plus_bundles_session_diagnostics(self):
        bundle = json.loads(_read(SKILLS.parent / "references" / "bundle-manifest.json"))
        names = {entry["canonical_name"] for entry in bundle["entries"]}
        assert "diagnosing-superpowers" in names
        assert (SKILLS / "diagnosing-superpowers" / "SKILL.md").is_file()

    def test_operating_contract_declares_shared_authority(self):
        path = REPO_SKILLS / "base-doctrine" / "references" / "operating-contract.md"
        text = _read(path)
        lowered = text.lower()
        assert "explicit human instruction" in lowered
        assert "owning skill" in lowered
        assert "reversible" in lowered

    def test_bootstrap_classifies_before_loading_broad_doctrine(self):
        text = _read(SKILLS / "using-superpowers-plus" / "SKILL.md")
        lowered = text.lower()
        assert lowered.index("classify the request") < lowered.index("load only selected doctrine")
        assert "stop reading" in text.lower()

    def test_portable_roots_do_not_encode_machine_or_repo_commands(self):
        for path in (REPO_SKILLS / "base-doctrine" / "SKILL.md", REPO_SKILLS / "repo-worker-base" / "SKILL.md"):
            text = _read(path)
            assert "Z:\\" not in text
            assert "tools/run.py" not in text

    def test_owner_applicability_is_not_overridden_by_callers(self):
        text = _read(REPO_SKILLS / "base-doctrine" / "references" / "operating-contract.md")
        assert "cannot bypass" in text
        assert "applicability" in text

    def test_operating_contract_requires_authority_for_new_workflow_semantics(self):
        text = " ".join(_read(REPO_SKILLS / "base-doctrine" / "references" / "operating-contract.md").lower().split())
        for phrase in (
            "only authority can change what the workflow means",
            "implementation detail",
            "environment marker",
            "reproduced failure",
            "preserve the existing workflow semantics",
        ):
            assert phrase in text

    def test_bootstrap_stops_expansion_without_a_route_changing_question(self):
        text = _read(SKILLS / "using-superpowers-plus" / "SKILL.md").lower()
        assert "concrete unresolved question" in text
        assert "might be useful" in text

    def test_sdd_stops_for_human_owned_requirements_but_rules_technical_findings(self):
        text = _read(SKILLS / "subagent-driven-development" / "SKILL.md").lower()
        assert "human-owned requirements" in text
        assert "product/canon" in text
        assert "already authorized" in text
        assert "only reasons to stop are the four named below" not in text
        assert "unauthorized irreversible or destructive" in text

    def test_portable_skill_tree_has_no_absolute_machine_paths(self):
        machine_path = re.compile(r"(?<!\w)[A-Za-z]:[\\/]+[A-Za-z0-9_.-]")
        text_suffixes = {"", ".md", ".py", ".json", ".ps1", ".js", ".ts", ".yml", ".yaml", ".txt"}
        offenders = []
        for root in (SKILLS, REPO_SKILLS, OPERATING_SKILLS):
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in text_suffixes or "__pycache__" in path.parts:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                if machine_path.search(text):
                    offenders.append(path.relative_to(ROOT).as_posix())
        assert offenders == []
