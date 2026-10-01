import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN_SOURCE = ROOT / "dist/plugins/agent-operating-model"
FOCUSED_SKILLS = (
    "agents-routing",
    "agent-doctrine-contracts",
    "completed-artifact-custody",
    "contribution-entrypoint",
    "command-bus",
    "playbook-composition",
    "review-entrypoint",
    "runbook-composition",
    "unslop",
    "repo-agent-assets",
    "repo-composition",
    "repo-shape",
    "repo-standards",
    "repository-validation",
    "tracked-repo-hooks",
)


def _run(args: list[str], *, cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True, check=False)


def _git(authority: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(authority), *args],
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    return result.stdout.strip()


def _tree_bytes(root: Path) -> dict[str, bytes]:
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}


def _links(markdown: Path) -> list[str]:
    return re.findall(r"\]\(([^)]+)\)", markdown.read_text(encoding="utf-8"))


def test_aom_authority_helpers_work_from_isolated_package(tmp_path: Path) -> None:
    plugin = tmp_path / "installed/agent-operating-model"
    shutil.copytree(PLUGIN_SOURCE, plugin)
    assert (plugin / "plugin.json").is_file()
    for skill in FOCUSED_SKILLS:
        assert (plugin / "skills" / skill / "SKILL.md").is_file(), skill

    catalog = json.loads(
        (plugin / "skills/repo-standards/references/standards-catalog.json").read_text(encoding="utf-8")
    )
    for entry in catalog["standards"]:
        assert (plugin / entry["definition"]).is_file(), entry["definition"]

    for skill in FOCUSED_SKILLS:
        skill_root = plugin / "skills" / skill
        for markdown in skill_root.rglob("*.md"):
            if "templates" in markdown.relative_to(skill_root).parts:
                continue
            for target in _links(markdown):
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                path = target.split("#", maxsplit=1)[0]
                if not path or path.startswith((".agents/", ".devin/")):
                    continue
                resolved = (markdown.parent / path).resolve()
                assert resolved.is_relative_to(plugin.resolve()), f"link escapes package: {markdown} -> {target}"
                assert resolved.is_file(), f"unresolved installed reference: {markdown} -> {target}"

    consumer = tmp_path / "consumer"
    (consumer / ".agents/contracts").mkdir(parents=True)
    (consumer / "AGENTS.md").write_text("# Routes\n", encoding="utf-8")
    certification = consumer / ".agents/contracts/standards-certification.md"
    certification.write_text("# Certification\n", encoding="utf-8")
    (consumer / ".agents/contracts/operating-standards.json").write_text(
        json.dumps(
            {
                "version": 2,
                "standards": [
                    {
                        "id": "runbook-composition",
                        "source": {
                            "repository": "https://example.test/aom.git",
                            "commit": "0123456789abcdef0123456789abcdef01234567",
                            "definition": "skills/runbook-composition/references/standard.md",
                        },
                        "certification": ".agents/contracts/standards-certification.md#runbook-composition",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    checker = plugin / "skills/repo-standards/scripts/subscriptions.py"
    before = _tree_bytes(consumer)
    result = _run([sys.executable, str(checker), "--repo-root", str(consumer), "--check"], cwd=consumer, env=env)
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert b"semantic certification is not assessed" in result.stdout
    assert _tree_bytes(consumer) == before

    certification.unlink()
    missing_result = _run(
        [sys.executable, str(checker), "--repo-root", str(consumer), "--check"], cwd=consumer, env=env
    )
    assert missing_result.returncode != 0
    assert b"certification file is missing" in missing_result.stderr

    authority = tmp_path / "authority"
    authority.mkdir()
    _git(authority, "init", "--quiet")
    _git(authority, "config", "user.name", "Fixture Author")
    _git(authority, "config", "user.email", "fixture@example.test")
    _git(authority, "config", "core.hooksPath", str(tmp_path / "empty-hooks"))
    definition = authority / "standards/removed-policy.md"
    definition.parent.mkdir()
    definition.write_bytes(b"Pinned historical policy\n")
    _git(authority, "add", "standards/removed-policy.md")
    _git(authority, "commit", "--quiet", "-m", "add pinned definition")
    commit = _git(authority, "rev-parse", "HEAD").decode("ascii")

    reader = plugin / "skills/repo-standards/scripts/pinned_definition.py"
    read = _run(
        [
            sys.executable,
            str(reader),
            "--source-root",
            str(authority),
            "--commit",
            commit,
            "--definition",
            "standards/removed-policy.md",
            "--check",
        ],
        cwd=consumer,
        env=env,
    )
    assert read.returncode == 0, read.stderr.decode("utf-8", errors="replace")
    assert read.stdout == b"Pinned historical policy\n"
