from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "tools" / "check_agent_standards.py"
SOURCE_REPOSITORY = "https://github.com/HarleyBartles/agent-asset-marketplace.git"
SOURCE_COMMIT = "3d59506dbd7a02266dedc9251b396dd60e5cc37d"
CURRENT_SUBSCRIPTION = json.loads(
    (REPO_ROOT / ".agents" / "contracts" / "operating-standards.json").read_text(encoding="utf-8")
)
HOOK_SOURCE_COMMIT = next(
    entry["source"]["commit"] for entry in CURRENT_SUBSCRIPTION["standards"] if entry["id"] == "tracked-validation-hook"
)
SELECTED_DEFINITIONS = {
    "root-agent-router": "skills/agents-routing/references/standard.md",
    "runbook-composition": "skills/runbook-composition/references/standard.md",
    "playbook-composition": "skills/playbook-composition/references/standard.md",
    "tracked-validation-hook": "skills/tracked-repo-hooks/references/standard.md",
    "review-entrypoint": "skills/review-entrypoint/references/standard.md",
    "contribution-entrypoint": "skills/contribution-entrypoint/references/standard.md",
    "completed-artifact-custody": "skills/completed-artifact-custody/references/standard.md",
    "unslop": "skills/unslop/references/standard.md",
}


@pytest.fixture
def adopting_repo(tmp_path: Path) -> Path:
    contract_dir = tmp_path / ".agents" / "contracts"
    contract_dir.mkdir(parents=True)
    subscriptions = {
        "version": 2,
        "standards": [
            {
                "id": standard_id,
                "source": {
                    "repository": SOURCE_REPOSITORY,
                    "commit": HOOK_SOURCE_COMMIT if standard_id == "tracked-validation-hook" else SOURCE_COMMIT,
                    "definition": definition,
                },
                "certification": f".agents/contracts/standards-certification.md#{standard_id}",
            }
            for standard_id, definition in SELECTED_DEFINITIONS.items()
        ],
    }
    (contract_dir / "operating-standards.json").write_text(json.dumps(subscriptions), encoding="utf-8")
    (contract_dir / "repo-standards-commands.json").write_text(
        json.dumps({"check": [["@python", "tools/run.py", "ci", "--check"]]}),
        encoding="utf-8",
    )
    certifications = ["# Standards certification", "", "Status: not yet certified.", ""]
    certifications.extend(
        f"## {standard_id}\n\nEvidence is still being assessed.\n" for standard_id in SELECTED_DEFINITIONS
    )
    (contract_dir / "standards-certification.md").write_text("\n".join(certifications), encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text(
        "Read `.agents/contracts/operating-standards.json` and `.agents/contracts/standards-certification.md`.\n",
        encoding="utf-8",
    )
    required_files = {
        "REVIEW.md": "Review guidance.\n",
        "CONTRIBUTING.md": "Contribution guidance.\n",
        "tools/validate_agents_md.py": "# repository-owned router checker\n",
        "tools/run.py": "tools/check_agent_standards.py tools/validate_agents_md.py\n",
        "githooks/pre-commit": "#!/usr/bin/env bash\n",
        ".github/workflows/marketplace-validation.yml": "run: githooks/pre-commit\n",
        ".agents/runbooks/example.md": "Lifecycle-stage guide.\n",
        ".agents/playbooks/example.md": "Cross-stage concern guide.\n",
        ".agents/unslop/repo.md": "No profiles yet.\n",
        ".agents/runbooks/planning.md": "See [repository profile](../unslop/repository.md).\n",
        ".agents/runbooks/implementing.md": "See [repository profile](../unslop/repository.md).\n",
        ".agents/runbooks/code-review.md": "See [repository profile](../unslop/repository.md).\n",
        ".agents/runbooks/pr.md": "See [repository profile](../unslop/repository.md).\n",
    }
    for relative, content in required_files.items():
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return tmp_path


def run_checker(repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--check", "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )


def load_subscriptions(repo: Path) -> dict[str, object]:
    path = repo / ".agents" / "contracts" / "operating-standards.json"
    return json.loads(path.read_text(encoding="utf-8"))


def save_subscriptions(repo: Path, value: dict[str, object]) -> None:
    path = repo / ".agents" / "contracts" / "operating-standards.json"
    path.write_text(json.dumps(value), encoding="utf-8")


def test_valid_pins_and_incomplete_certification_are_structurally_accepted(
    adopting_repo: Path,
) -> None:
    result = run_checker(adopting_repo)

    assert result.returncode == 0, result.stderr
    assert "semantic certification is not assessed" in result.stdout
    assert "certified" not in result.stdout.lower()
    pins = {entry["id"]: entry["source"]["commit"] for entry in load_subscriptions(adopting_repo)["standards"]}
    assert pins["tracked-validation-hook"] == HOOK_SOURCE_COMMIT
    assert {pin for standard_id, pin in pins.items() if standard_id != "tracked-validation-hook"} == {SOURCE_COMMIT}
    assert HOOK_SOURCE_COMMIT != SOURCE_COMMIT


def test_checked_in_tracked_hook_pin_resolves_its_definition() -> None:
    hook = next(entry for entry in CURRENT_SUBSCRIPTION["standards"] if entry["id"] == "tracked-validation-hook")
    source = hook["source"]
    source_git_dir = os.environ.get("REPO_STANDARDS_SOURCE_GIT_DIR")
    git_command = ["git"]
    if source_git_dir:
        git_command.extend(["--git-dir", source_git_dir])
    result = subprocess.run(
        [*git_command, "show", f"{source['commit']}:{source['definition']}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "disposable checkout" in result.stdout


@pytest.mark.parametrize("unexpected_id", ["command-bus", "repo-plugin-subscriptions", "marketplace-registry"])
def test_checker_rejects_a_standard_not_selected_for_this_repository(adopting_repo: Path, unexpected_id: str) -> None:
    record = load_subscriptions(adopting_repo)
    standards = record["standards"]
    assert isinstance(standards, list)
    standards.append(
        {
            "id": unexpected_id,
            "source": {
                "repository": SOURCE_REPOSITORY,
                "commit": SOURCE_COMMIT,
                "definition": f"skills/{unexpected_id}/references/standard.md",
            },
            "certification": f".agents/contracts/standards-certification.md#{unexpected_id}",
        }
    )
    save_subscriptions(adopting_repo, record)

    result = run_checker(adopting_repo)

    assert result.returncode != 0
    assert f"unexpected selected standard: {unexpected_id}" in result.stderr


def test_checker_rejects_an_unknown_definition_source(adopting_repo: Path) -> None:
    record = load_subscriptions(adopting_repo)
    standards = record["standards"]
    assert isinstance(standards, list)
    first = standards[0]
    source = dict(first["source"])
    source["repository"] = "https://example.invalid/another-source.git"
    first["source"] = source
    save_subscriptions(adopting_repo, record)

    result = run_checker(adopting_repo)

    assert result.returncode != 0
    assert "unexpected source repository" in result.stderr


def test_checker_rejects_execution_commands_in_the_subscription_record(
    adopting_repo: Path,
) -> None:
    record = load_subscriptions(adopting_repo)
    record["check"] = ["python tools/do_not_run.py"]
    save_subscriptions(adopting_repo, record)

    result = run_checker(adopting_repo)

    assert result.returncode != 0
    assert "unknown field(s): check" in result.stderr


def test_checker_rejects_unreadable_subscription_json(adopting_repo: Path) -> None:
    path = adopting_repo / ".agents/contracts/operating-standards.json"
    path.write_text("{not json", encoding="utf-8")

    result = run_checker(adopting_repo)

    assert result.returncode != 0
    assert "is not readable JSON" in result.stderr


def test_checker_accepts_the_check_only_hook_command_contract(adopting_repo: Path) -> None:
    result = run_checker(adopting_repo)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    ("mutation", "diagnostic"),
    [
        ({"apply": [["@python", "tools/run.py", "ci", "--apply"]]}, "unknown field(s): apply"),
        ({"generated_paths": []}, "unknown field(s): generated_paths"),
        ({"check": []}, "check must be a non-empty array"),
        ({"check": [["python", "tools/run.py", "ci", "--check"]]}, "must be exactly"),
        ({"check": [["@python", "tools/run.py", "ci", "--check", "--diagnostics"]]}, "must be exactly"),
        ({"check": [["@python", "tools/run.py", "ci", "--apply"]]}, "must be exactly"),
    ],
)
def test_checker_rejects_mutative_or_malformed_hook_command_contract(
    adopting_repo: Path, mutation: dict[str, object], diagnostic: str
) -> None:
    path = adopting_repo / ".agents/contracts/repo-standards-commands.json"
    path.write_text(json.dumps(mutation), encoding="utf-8")

    result = run_checker(adopting_repo)

    assert result.returncode != 0
    assert diagnostic in result.stderr


def test_checker_rejects_a_forged_tracked_hook_pin(adopting_repo: Path) -> None:
    record = load_subscriptions(adopting_repo)
    hook = next(entry for entry in record["standards"] if entry["id"] == "tracked-validation-hook")
    source = dict(hook["source"])
    source["commit"] = "0" * 40
    hook["source"] = source
    save_subscriptions(adopting_repo, record)

    result = run_checker(adopting_repo)

    assert result.returncode != 0
    assert "does not match the repository's certified pin" in result.stderr


def test_checker_rejects_legacy_subscription_versions(adopting_repo: Path) -> None:
    record = load_subscriptions(adopting_repo)
    record["version"] = 1
    save_subscriptions(adopting_repo, record)

    result = run_checker(adopting_repo)

    assert result.returncode != 0
    assert "record version must be numeric 2" in result.stderr


@pytest.mark.parametrize(
    ("mutation", "diagnostic"),
    [
        ("duplicate_id", "duplicates 'root-agent-router'"),
        ("short_commit", "full lowercase"),
        ("wrong_commit", "does not match the repository's certified pin"),
        ("wrong_definition", "definition path does not match the selected standard"),
        ("unsafe_path", "normalized, repository-relative POSIX"),
        ("missing_certification", "certification file is missing"),
        ("missing_cert_section", "certification section is missing"),
        ("missing_root_router", "root AGENTS.md"),
        ("missing_route", "root AGENTS.md must route"),
        ("missing_review", "required by review-entrypoint: REVIEW.md is missing"),
        ("missing_unslop_route", "Unslop profile route is missing from .agents/runbooks/planning.md"),
    ],
)
def test_checker_reports_subscription_and_route_drift(adopting_repo: Path, mutation: str, diagnostic: str) -> None:
    record = load_subscriptions(adopting_repo)
    standards = record["standards"]
    assert isinstance(standards, list)
    first = standards[0]

    if mutation == "duplicate_id":
        duplicate = dict(first)
        standards.append(duplicate)
        save_subscriptions(adopting_repo, record)
    elif mutation == "short_commit":
        source = dict(first["source"])
        source["commit"] = "3d59506"
        first["source"] = source
        save_subscriptions(adopting_repo, record)
    elif mutation == "wrong_commit":
        source = dict(first["source"])
        source["commit"] = "0" * 40
        first["source"] = source
        save_subscriptions(adopting_repo, record)
    elif mutation == "wrong_definition":
        source = dict(first["source"])
        source["definition"] = "skills/command-bus/references/standard.md"
        first["source"] = source
        save_subscriptions(adopting_repo, record)
    elif mutation == "unsafe_path":
        source = dict(first["source"])
        source["definition"] = "../outside.md"
        first["source"] = source
        save_subscriptions(adopting_repo, record)
    elif mutation == "missing_certification":
        (adopting_repo / ".agents/contracts/standards-certification.md").unlink()
    elif mutation == "missing_cert_section":
        cert_path = adopting_repo / ".agents/contracts/standards-certification.md"
        cert_path.write_text("# Standards certification\n", encoding="utf-8")
    elif mutation == "missing_root_router":
        (adopting_repo / "AGENTS.md").unlink()
    elif mutation == "missing_route":
        (adopting_repo / "AGENTS.md").write_text("No subscription route here.\n", encoding="utf-8")
    elif mutation == "missing_review":
        (adopting_repo / "REVIEW.md").unlink()
    elif mutation == "missing_unslop_route":
        path = adopting_repo / ".agents/runbooks/planning.md"
        path.write_text("No profile link here.\n", encoding="utf-8")

    result = run_checker(adopting_repo)

    assert result.returncode != 0
    assert diagnostic in result.stderr
