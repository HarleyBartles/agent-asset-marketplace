from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "codex-marketplace" / "plugins" / "writing-pack"
APPROVED_SKILLS = {
    "writing",
    "writing-with-clarity",
    "writing-style",
    "writing-profile-engine",
}
INSTALLED_DEFAULTS = [
    "mcp-usage-pack",
    "repo-worker-pack",
    "superpowers-plus",
    "unslop-plus",
    "writing-pack",
]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_writing_pack_is_an_enabled_marketplace_root() -> None:
    inventory = _load_json(ROOT / "codex-marketplace" / "plugin-roots.json")
    writing_pack = next(root for root in inventory["roots"] if root["name"] == "writing-pack")

    assert writing_pack["enabled"] is True


def test_writing_pack_manifests_expose_the_approved_boundary() -> None:
    plugin_manifest = _load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    package_manifest = _load_json(PLUGIN_ROOT / "package.json")

    assert plugin_manifest["name"] == "writing-pack"
    assert package_manifest["name"] == "@harleybartles/writing-pack"
    assert APPROVED_SKILLS <= set(plugin_manifest["keywords"])
    assert APPROVED_SKILLS <= set(package_manifest["keywords"])


def test_clarity_skill_has_one_writing_pack_custody_path() -> None:
    clarity_skill = PLUGIN_ROOT / "skills" / "writing-with-clarity"

    assert clarity_skill.is_dir()
    old_clarity_skill = ROOT / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills" / "writing-with-clarity"

    assert not old_clarity_skill.exists()


def test_clarity_authority_assets_and_report_hygiene_survive_the_move() -> None:
    clarity_skill = PLUGIN_ROOT / "skills" / "writing-with-clarity"
    authority = clarity_skill / "assets" / "authority"

    assert authority.is_dir()
    assert (authority / "authority.yaml").is_file()
    assert (authority / "source-map.yaml").is_file()
    assert (authority / "CITATIONS.md").is_file()
    assert (authority / "reference-source" / "elements-of-style-1918").is_dir()
    assert (clarity_skill / "references" / "report-hygiene-checklist.md").is_file()


def test_writing_router_declares_its_specialist_interfaces_and_order() -> None:
    writing_skill = PLUGIN_ROOT / "skills" / "writing"
    skill_text = (writing_skill / "SKILL.md").read_text(encoding="utf-8")
    workflow = (writing_skill / "references" / "workflow.md").read_text(encoding="utf-8")

    assert "related_skills:" in skill_text
    assert "writing-with-clarity" in skill_text
    assert "writing-style" in skill_text

    stages = [
        "1. Establish audience, purpose, facts, and hard constraints.",
        "2. Draft or revise through $writing-with-clarity.",
        "3. Apply a declared voice card through $writing-style when one is available.",
        "4. Run $writing-style fatigue review only when evidence supports a material finding.",
        "5. Re-run $writing-with-clarity as the final gate.",
    ]
    positions = [workflow.index(stage) for stage in stages]

    assert positions == sorted(positions)


def test_writing_router_authority_order_protects_facts_and_clarity() -> None:
    authority_order = (PLUGIN_ROOT / "skills" / "writing" / "references" / "authority-order.md").read_text(
        encoding="utf-8"
    )

    ranks = [
        "1. Factual accuracy, safety, legal requirements, and accessibility",
        "2. Explicit user intent",
        "3. Clarity and preservation of meaning",
        "4. Declared voice and authorised style guidance",
        "5. Reader-fatigue heuristics",
    ]
    positions = [authority_order.index(rank) for rank in ranks]

    assert positions == sorted(positions)


def test_writing_pack_skills_do_not_own_top_level_profiles_directories() -> None:
    skills_root = PLUGIN_ROOT / "skills"

    assert all(not (skill / "profiles").exists() for skill in skills_root.iterdir() if skill.is_dir())


def test_installed_defaults_include_the_writing_and_generic_unslop_owners() -> None:
    policy = _load_json(ROOT / "codex-marketplace" / "repo-local-marketplace-policy.json")
    old_unslop_profiles = ROOT / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills" / "unslop-profiles"

    assert policy["install_defaults"] == INSTALLED_DEFAULTS
    assert not old_unslop_profiles.exists()
    assert (ROOT / "codex-marketplace" / "plugins" / "unslop-plus" / "skills" / "unslop-profiles").is_dir()


def test_installed_projection_retains_clarity_and_generic_unslop_provenance() -> None:
    provenance = _load_json(ROOT / ".agents" / "skills" / ".provenance.json")
    installed_clarity = ROOT / ".agents" / "skills" / "writing-with-clarity" / "SKILL.md"
    installed_unslop_profiles = ROOT / ".agents" / "skills" / "unslop-profiles" / "SKILL.md"

    assert provenance["syncedPlugins"] == INSTALLED_DEFAULTS
    assert installed_clarity.is_file()
    assert "plugins/writing-pack/skills/writing-with-clarity/SKILL.md" in installed_clarity.read_text(encoding="utf-8")
    assert "plugins/unslop-plus/skills/unslop-profiles/SKILL.md" in installed_unslop_profiles.read_text(
        encoding="utf-8"
    )


def test_installed_unslop_engine_scripts_support_the_repository_check_contract() -> None:
    scripts_root = ROOT / "codex-marketplace" / "plugins" / "unslop-plus" / "skills" / "unslop-engine" / "scripts"

    for script_name in ("unslop.py", "validate_package.py", "validate_unslop_output.py"):
        result = subprocess.run(
            [sys.executable, str(scripts_root / script_name), "--check"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, result.stderr


def _run_unslop_engine(*arguments: str) -> subprocess.CompletedProcess[str]:
    script = (
        ROOT / "codex-marketplace" / "plugins" / "unslop-plus" / "skills" / "unslop-engine" / "scripts" / "unslop.py"
    )

    return subprocess.run(
        [sys.executable, str(script), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


def test_unslop_engine_defaults_to_a_non_mutating_check_mode(tmp_path: Path) -> None:
    output = tmp_path / "unslop-output"
    help_result = _run_unslop_engine("--help")
    explicit_check = _run_unslop_engine("--check")
    default_check = _run_unslop_engine(
        "--domain",
        "fixture-domain",
        "--fixture-samples",
        "--output",
        str(output),
    )

    assert help_result.returncode == 0, help_result.stderr
    assert explicit_check.returncode == 0, explicit_check.stderr
    assert default_check.returncode == 0, default_check.stderr
    assert not output.exists()
    assert "mixed" in help_result.stdout.lower()


def test_unslop_engine_requires_apply_before_creating_output(tmp_path: Path) -> None:
    output = tmp_path / "unslop-output"
    result = _run_unslop_engine(
        "--apply",
        "--domain",
        "fixture-domain",
        "--fixture-samples",
        "--output",
        str(output),
    )

    assert result.returncode == 0, result.stderr
    assert (output / "manifest.json").is_file()


def test_installed_unslop_engine_matches_its_canonical_source() -> None:
    canonical_script = (
        ROOT / "codex-marketplace" / "plugins" / "unslop-plus" / "skills" / "unslop-engine" / "scripts" / "unslop.py"
    )
    installed_script = ROOT / ".agents" / "skills" / "unslop-engine" / "scripts" / "unslop.py"

    assert installed_script.read_bytes() == canonical_script.read_bytes()
