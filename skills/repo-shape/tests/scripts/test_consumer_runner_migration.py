from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "skills/repo-shape/scripts"
sys.path.insert(0, str(SCRIPTS))

import deploy_operating_standards  # noqa: E402
import operating_standards_catalog  # noqa: E402

CATALOG_PATH = ROOT / "skills/repo-shape/references/operating-standards-catalog.json"
MANIFEST_PATH = ROOT / "skills/repo-shape/references/repository-shape-manifest.json"
CATALOG = operating_standards_catalog.load_catalog(CATALOG_PATH, MANIFEST_PATH, ROOT)
STANDARD_ID = "root-gitignore-hygiene"


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def _consumer(root: Path) -> tuple[Path, Path]:
    _git(root, "init", "-b", "codex/migration-fixture")
    _git(root, "config", "user.name", "Migration Fixture")
    _git(root, "config", "user.email", "migration-fixture@example.invalid")
    source = root / ".agents/plugins/marketplace-source"
    resources = set(deploy_operating_standards.RUNTIME_RESOURCES)
    resources.update(deploy_operating_standards.RUNTIME_REFERENCES)
    standard = next(item for item in CATALOG.standards if item.id == STANDARD_ID)
    resources.update(standard.resources)
    resources.add("skills/refreshing-installed-skills/scripts/refresh_installed_skills.py")
    resources.add("tools/shared_checkout.py")
    for resource in resources:
        destination = source / resource
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / resource, destination)

    _git(source, "init")
    _git(source, "config", "user.name", "Pinned Marketplace")
    _git(source, "config", "user.email", "pinned-marketplace@example.invalid")
    _git(source, "add", ".")
    _git(source, "commit", "-m", "pinned marketplace source")
    revision = _git(source, "rev-parse", "HEAD")

    contract = root / ".agents/contracts/operating-standards.json"
    contract.parent.mkdir(parents=True)
    contract.write_text(
        json.dumps(
            {
                "version": 1,
                "standards": [
                    {
                        "id": STANDARD_ID,
                        "origin": "marketplace",
                        "revision": revision,
                        "implementation_root": f".agents/standards/{STANDARD_ID}",
                        "check": [
                            "@python",
                            ".agents/standards/_runtime/repo_standards.py",
                            "--run-standard",
                            STANDARD_ID,
                            "--check",
                        ],
                        "apply": [
                            "@python",
                            ".agents/standards/_runtime/repo_standards.py",
                            "--run-standard",
                            STANDARD_ID,
                            "--apply",
                            "--yes",
                            "@allow-shared-checkout",
                        ],
                        "generated_paths": [],
                        "requires": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (root / ".agents/plugins/marketplace.json").parent.mkdir(parents=True, exist_ok=True)
    (root / ".agents/plugins/marketplace.json").write_text('{"plugins": []}\n', encoding="utf-8")
    (root / ".gitignore").write_text("", encoding="utf-8")
    return source, contract


def _run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, capture_output=True, text=True, check=False)


def test_runner_migrates_refresh_and_selected_standard_off_ambient_projection(tmp_path: Path) -> None:
    guide = (ROOT / "skills/repo-shape/references/consumer-runner-migration.md").read_text(encoding="utf-8")
    contract_match = re.search(r"```json consumer-runner-contract\s+(.*?)```", guide, re.DOTALL)
    assert contract_match is not None
    runner_contract = json.loads(contract_match.group(1))

    source, _ = _consumer(tmp_path)
    old_refresh = tmp_path / ".agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py"
    new_refresh = tmp_path / runner_contract["refresh_script"]
    runtime = tmp_path / runner_contract["standards_dispatcher"]

    assert not old_refresh.exists()
    assert new_refresh.is_file()

    old_result = _run(tmp_path, sys.executable, str(old_refresh), "--check")
    assert old_result.returncode != 0

    deploy_operating_standards.deploy(tmp_path, source, CATALOG, apply=True)
    assert runtime.is_file()

    tools = tmp_path / "tools"
    tools.mkdir()
    runner = tools / "run.py"
    runner.write_text(
        """import subprocess
import sys

if len(sys.argv) != 3 or sys.argv[1] != "ci" or sys.argv[2] not in {"--apply", "--check"}:
    raise SystemExit("expected tools/run.py ci --apply|--check")
mode = sys.argv[2]
runtime = """
        + json.dumps(runner_contract["standards_dispatcher"])
        + """
refresh = """
        + json.dumps(runner_contract["refresh_script"])
        + """
standard = [sys.executable, runtime, "--run-standard", "root-gitignore-hygiene", mode]
sync = [sys.executable, refresh, "--no-roll-marketplace-source", mode]
if mode == "--apply":
    standard.extend(["--yes", "--allow-shared-checkout"])
    sync.append("--allow-shared-checkout")
for command in (standard, sync):
    result = subprocess.run(command, check=False)
    if result.returncode:
        raise SystemExit(result.returncode)
""",
        encoding="utf-8",
        newline="\n",
    )

    for mode, command in runner_contract["outer_commands"].items():
        result = _run(tmp_path, sys.executable, *command)
        assert result.returncode == 0, result.stdout + result.stderr

    assert not (tmp_path / ".agents/skills").exists()
    assert (tmp_path / ".agents/standards/provenance.json").is_file()
    assert (tmp_path / ".agents/contracts/operating-standards.json").is_file()
