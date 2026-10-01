from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "tools" / "check_agent_standards.py"
SOURCE_REPOSITORY = "https://github.com/HarleyBartles/agent-asset-marketplace.git"
SOURCE_COMMIT = "3d59506dbd7a02266dedc9251b396dd60e5cc37d"
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
                    "commit": SOURCE_COMMIT,
                    "definition": definition,
                },
                "certification": f".agents/contracts/standards-certification.md#{standard_id}",
            }
            for standard_id, definition in SELECTED_DEFINITIONS.items()
        ],
    }
    (contract_dir / "operating-standards.json").write_text(json.dumps(subscriptions), encoding="utf-8")
    (contract_dir / "repo-standards-commands.json").write_text(
        json.dumps(
            {
                "apply": [["@python", "tools/run.py", "ci", "--apply"]],
                "check": [["@python", "tools/run.py", "ci", "--check", "--diagnostics"]],
                "generated_paths": [],
            }
        ),
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


def test_checker_requires_hook_apply_and_check_to_use_the_same_ci_target(
    adopting_repo: Path,
) -> None:
    path = adopting_repo / ".agents/contracts/repo-standards-commands.json"
    declaration = json.loads(path.read_text(encoding="utf-8"))
    declaration["check"] = [["@python", "tools/run.py", "validate", "--check"]]
    path.write_text(json.dumps(declaration), encoding="utf-8")

    result = run_checker(adopting_repo)

    assert result.returncode != 0
    assert "command contract check must invoke tools/run.py ci --check" in result.stderr


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

    result = run_checker(adopting_repo)

    assert result.returncode != 0
    assert diagnostic in result.stderr
