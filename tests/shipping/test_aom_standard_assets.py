from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[2]
PLUGIN_SOURCE = ROOT / "dist/plugins/agent-operating-model"
CHECKERS = {
    "runbook-composition": "scripts/check_runbooks.py",
    "playbook-composition": "scripts/check_playbooks.py",
    "agents-routing": "assets/check_agents_md.py",
    "agent-doctrine-contracts": "assets/check_agent_docs.py",
    "repo-agent-assets": "assets/check_plugin_subscriptions.py",
}
SKILLS = (
    "runbook-composition",
    "playbook-composition",
    "agents-routing",
    "agent-doctrine-contracts",
    "repo-agent-assets",
    "repo-standards",
    "command-bus",
    "review-entrypoint",
    "contribution-entrypoint",
)


def _links(markdown: Path) -> list[str]:
    return re.findall(r"\]\(([^)]+)\)", markdown.read_text(encoding="utf-8"))


def _copy_checker(plugin: Path, consumer: Path, skill: str) -> Path:
    source = plugin / "skills" / skill / CHECKERS[skill]
    destination = consumer / "tools" / f"{skill}.py"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    return destination


def _run(script: Path, consumer: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    return subprocess.run(
        [sys.executable, str(script), "--repo-root", str(consumer), *args, "--check"],
        cwd=consumer,
        env=env,
        capture_output=True,
        check=False,
    )


def _prepare_consumer(consumer: Path, plugin: Path) -> dict[str, Path]:
    consumer.mkdir()
    tools = {skill: _copy_checker(plugin, consumer, skill) for skill in CHECKERS}
    (consumer / "AGENTS.md").write_text(
        "For lifecycle design work, read [the stage guide](.agents/runbooks/design.md). "
        "For testing concerns, read [.agents/playbooks/testing.md](.agents/playbooks/testing.md). "
        "Read [.agents/doctrine/rule.md](.agents/doctrine/rule.md) and "
        "[.agents/contracts/contract.json](.agents/contracts/contract.json) when applicable.\n",
        encoding="utf-8",
    )
    runbooks = consumer / ".agents/runbooks"
    playbooks = consumer / ".agents/playbooks"
    doctrine = consumer / ".agents/doctrine"
    contracts = consumer / ".agents/contracts"
    for directory in (runbooks, playbooks, doctrine, contracts):
        directory.mkdir(parents=True)
    shutil.copyfile(
        plugin / "skills/runbook-composition/assets/runbooks/design.md",
        runbooks / "design.md",
    )
    shutil.copyfile(
        plugin / "skills/playbook-composition/assets/playbooks/testing.md",
        playbooks / "testing.md",
    )
    (doctrine / "rule.md").write_text("Preserve the repository's source-of-truth boundary.\n", encoding="utf-8")
    (contracts / "contract.json").write_text('{"local": "repository shape"}\n', encoding="utf-8")
    for name in ("marketplace.json.example", "codex-config.toml.example", "devin-config.json.example"):
        source = plugin / "skills/repo-agent-assets/assets/examples" / name
        target = {
            "marketplace.json.example": consumer / ".agents/plugins/marketplace.json",
            "codex-config.toml.example": consumer / ".codex/config.toml",
            "devin-config.json.example": consumer / ".devin/config.json",
        }[name]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return tools


def test_optional_aom_assets_are_closed_inside_the_generated_package() -> None:
    assert PLUGIN_SOURCE.is_dir()
    manifest = json.loads((PLUGIN_SOURCE / "references/bundle-manifest.json").read_text(encoding="utf-8"))
    manifest_text = json.dumps(manifest)
    for skill in SKILLS:
        root = PLUGIN_SOURCE / "skills" / skill
        assert (root / "SKILL.md").is_file(), skill
        assert skill in manifest_text
        for source in (root / "SKILL.md", *root.glob("references/*.md")):
            for target in _links(source):
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith(("#", "mailto:")):
                    continue
                relative = parsed.path.split("#", maxsplit=1)[0]
                if not relative or relative.startswith((".agents/", ".devin/")):
                    continue
                resolved = (source.parent / relative).resolve()
                assert resolved.is_relative_to(PLUGIN_SOURCE.resolve()), f"link escapes package: {source} -> {target}"
                assert resolved.is_file(), f"unresolved package link: {source} -> {target}"
    for skill, relative in CHECKERS.items():
        checker = PLUGIN_SOURCE / "skills" / skill / relative
        tree = ast.parse(checker.read_text(encoding="utf-8"))
        imports = [
            alias.name.split(".", maxsplit=1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        ]
        imports.extend(
            node.module.split(".", maxsplit=1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        missing_siblings = [
            module
            for module in imports
            if module not in sys.stdlib_module_names
            and not (checker.parent / f"{module}.py").is_file()
            and not (checker.parent / module / "__init__.py").is_file()
        ]
        assert not missing_siblings, f"non-stdlib import missing from package for {checker}: {missing_siblings}"
    for skill, relative in CHECKERS.items():
        checker = PLUGIN_SOURCE / "skills" / skill / relative
        assert checker.is_file(), skill
        assert not checker.with_suffix(".sh").exists()
        assert not checker.with_suffix(".ps1").exists()
    for skill in SKILLS:
        assert not (PLUGIN_SOURCE / "skills" / skill / "tests/evaluator-only").exists(), skill


def test_copied_checkers_run_as_consumer_owned_files_without_marketplace_runtime(tmp_path: Path) -> None:
    plugin = tmp_path / "installed/agent-operating-model"
    shutil.copytree(PLUGIN_SOURCE, plugin)
    consumer = tmp_path / "consumer"
    tools = _prepare_consumer(consumer, plugin)
    before = {
        path.relative_to(consumer).as_posix(): path.read_bytes() for path in consumer.rglob("*") if path.is_file()
    }

    checks = (
        ("runbook-composition", ("--document", ".agents/runbooks/design.md", "--route-source", "AGENTS.md")),
        ("playbook-composition", ("--document", ".agents/playbooks/testing.md", "--route-source", "AGENTS.md")),
        ("agents-routing", ("--warn-lines", "55", "--error-lines", "100")),
        ("agent-doctrine-contracts", ()),
        ("repo-agent-assets", ()),
    )
    for skill, args in checks:
        result = _run(tools[skill], consumer, *args)
        assert result.returncode == 0, result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace")
    after = {path.relative_to(consumer).as_posix(): path.read_bytes() for path in consumer.rglob("*") if path.is_file()}
    assert before == after


def test_checker_failures_report_mechanical_facts_and_remain_read_only(tmp_path: Path) -> None:
    plugin = tmp_path / "installed/agent-operating-model"
    shutil.copytree(PLUGIN_SOURCE, plugin)
    consumer = tmp_path / "consumer"
    tools = _prepare_consumer(consumer, plugin)
    (consumer / ".agents/runbooks/design.md").write_text("Read [missing](absent.md).\n", encoding="utf-8")
    (consumer / "AGENTS.md").write_text("oversized\n" * 101, encoding="utf-8")
    (consumer / ".agents/contracts/contract.json").write_text('{"local": }\n', encoding="utf-8")
    (consumer / ".agents/plugins/marketplace.json").write_text('{"plugins": [}', encoding="utf-8")
    before = {
        path.relative_to(consumer).as_posix(): path.read_bytes() for path in consumer.rglob("*") if path.is_file()
    }

    results = {
        skill: _run(tools[skill], consumer, *args)
        for skill, args in (
            ("runbook-composition", ("--document", ".agents/runbooks/design.md", "--route-source", "AGENTS.md")),
            ("agents-routing", ()),
            ("agent-doctrine-contracts", ()),
            ("repo-agent-assets", ()),
        )
    }
    after = {path.relative_to(consumer).as_posix(): path.read_bytes() for path in consumer.rglob("*") if path.is_file()}

    assert all(result.returncode == 1 for result in results.values())
    output = "\n".join(result.stdout.decode(errors="replace") for result in results.values()).lower()
    assert "broken local link" in output
    assert "error above 100" in output
    assert "invalid json syntax" in output
    assert "invalid catalog json" in output
    assert "does not certify compliance" in output
    assert "does not fetch remote repositories" in output
    assert before == after
