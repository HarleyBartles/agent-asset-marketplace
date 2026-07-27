from __future__ import annotations

import sys
import subprocess
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
REBUILD = [sys.executable, str(ROOT / "tools" / "rebuild_marketplace.py")]
VALIDATE = [sys.executable, str(ROOT / "tools" / "validate_marketplace.py")]

sys.path.insert(0, str(ROOT / "tools"))

import rebuild_marketplace


def test_rebuild_cli_help_exposes_new_flags():
    result = subprocess.run(
        [*REBUILD, "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    text = result.stdout
    assert "--phase" in text, "expected --phase in help"
    assert "--check" in text, "expected --check in help"
    assert "--apply" in text, "expected --apply in help"
    assert "--allow-shared-checkout" in text, "expected --allow-shared-checkout in help"
    assert "--skip-install" in text, "expected --skip-install in help"
    assert "--verbose" in text, "expected --verbose in help"


def test_validate_marketplace_phase_cli_exists():
    result = subprocess.run(
        [*VALIDATE, "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "--phase" in result.stdout, "expected --phase in validate_marketplace.py help"


def test_rebuild_cli_rejects_allow_shared_checkout_without_apply():
    result = subprocess.run(
        [*REBUILD, "--allow-shared-checkout", "--phase", "inventory"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "--allow-shared-checkout requires --apply" in result.stderr


def test_rebuild_cli_rejects_apply_and_check():
    result = subprocess.run(
        [*REBUILD, "--apply", "--check", "--phase", "inventory"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "mutually exclusive" in result.stderr


def test_rebuild_refuses_apply_in_shared_checkout_without_flag(monkeypatch, capsys) -> None:
    """In a shared checkout, --apply must be paired with --allow-shared-checkout."""
    monkeypatch.setattr(rebuild_marketplace.shared_checkout, "is_shared_checkout", lambda _root: True)
    monkeypatch.setattr(rebuild_marketplace.shared_checkout, "prompt_for_approval", lambda _name: False)
    monkeypatch.setattr(sys, "argv", ["rebuild_marketplace.py", "--apply", "--phase", "inventory"])

    exit_code = rebuild_marketplace.main()
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Pass --allow-shared-checkout" in captured.err


def test_rebuild_interactive_approval_forwards_allow_shared_checkout(monkeypatch) -> None:
    """If the user interactively approves a shared checkout, child skill scripts receive --allow-shared-checkout."""
    calls: list[tuple[str, ...]] = []
    monkeypatch.setattr(rebuild_marketplace.shared_checkout, "is_shared_checkout", lambda _root: True)
    monkeypatch.setattr(rebuild_marketplace.shared_checkout, "prompt_for_approval", lambda _name: True)
    monkeypatch.setattr(sys, "argv", ["rebuild_marketplace.py", "--apply", "--phase", "project"])

    def fake_run_skill_script(skill_name: str, core_name: str, *args: str, verbose: bool = False) -> None:
        calls.append((skill_name, core_name, *args))

    def fake_run_tool(script_name: str, *args: str, verbose: bool = False) -> None:
        calls.append((script_name, *args))

    monkeypatch.setattr(rebuild_marketplace, "_run_skill_script", fake_run_skill_script)
    monkeypatch.setattr(rebuild_marketplace, "_run_tool", fake_run_tool)

    exit_code = rebuild_marketplace.main()
    assert exit_code == 0
    refresh_call = next((c for c in calls if len(c) > 1 and c[1] == "refresh_installed_skills.py"), None)
    assert refresh_call == ("refreshing-installed-skills", "refresh_installed_skills.py", "--apply", "--allow-shared-checkout")


def test_rebuild_forwards_allow_shared_checkout_to_skill_scripts(monkeypatch) -> None:
    """The project and index phases must forward --allow-shared-checkout in apply mode."""
    calls: list[tuple[str, ...]] = []

    def fake_run_skill_script(skill_name: str, core_name: str, *args: str, verbose: bool = False) -> None:
        calls.append((skill_name, core_name, *args))

    def fake_run_tool(script_name: str, *args: str, verbose: bool = False) -> None:
        calls.append((script_name, *args))

    monkeypatch.setattr(rebuild_marketplace, "_run_skill_script", fake_run_skill_script)
    monkeypatch.setattr(rebuild_marketplace, "_run_tool", fake_run_tool)

    rebuild_marketplace._run_project(
        check=False,
        verbose=False,
        skip_install=False,
        allow_shared_checkout=True,
    )
    refresh_call = next((c for c in calls if len(c) > 1 and c[1] == "refresh_installed_skills.py"), None)
    assert refresh_call == ("refreshing-installed-skills", "refresh_installed_skills.py", "--apply", "--allow-shared-checkout")

    calls.clear()
    rebuild_marketplace._run_index(
        check=False,
        verbose=False,
        skip_index=False,
        allow_shared_checkout=True,
    )
    mesh_calls = [c for c in calls if len(c) > 1 and c[1] == "generate_index_mesh.py"]
    assert any(c == ("generating-agent-mesh", "generate_index_mesh.py", "--apply", "--allow-shared-checkout") for c in mesh_calls)


def test_rebuild_does_not_forward_allow_shared_checkout_in_check_mode(monkeypatch) -> None:
    """In check mode, skill scripts should not receive --allow-shared-checkout."""
    calls: list[tuple[str, ...]] = []

    def fake_run_skill_script(skill_name: str, core_name: str, *args: str, verbose: bool = False) -> None:
        calls.append((skill_name, core_name, *args))

    def fake_run_tool(script_name: str, *args: str, verbose: bool = False) -> None:
        calls.append((script_name, *args))

    monkeypatch.setattr(rebuild_marketplace, "_run_skill_script", fake_run_skill_script)
    monkeypatch.setattr(rebuild_marketplace, "_run_tool", fake_run_tool)

    rebuild_marketplace._run_project(
        check=True,
        verbose=False,
        skip_install=False,
        allow_shared_checkout=True,
    )
    refresh_call = next((c for c in calls if len(c) > 1 and c[1] == "refresh_installed_skills.py"), None)
    assert refresh_call == ("refreshing-installed-skills", "refresh_installed_skills.py", "--check")
    assert "--allow-shared-checkout" not in refresh_call
