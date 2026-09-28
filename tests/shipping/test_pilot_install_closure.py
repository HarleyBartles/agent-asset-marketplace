import json
import re
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PLUGIN_NAMES = ("feature-sliced-design", "frontend-pack")


def _local_links(skill: Path) -> list[Path]:
    targets: list[Path] = []
    for markdown in skill.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", markdown.read_text(encoding="utf-8")):
            if "://" not in target and not target.startswith(("#", "mailto:")):
                targets.append((markdown.parent / target.split("#", maxsplit=1)[0]).resolve())
    return targets


def test_shared_skill_and_reference_resolve_after_each_plugin_isolated(tmp_path: Path) -> None:
    installed = tmp_path / "installed"
    installed.mkdir()
    for name in PLUGIN_NAMES:
        source = ROOT / "dist/plugins" / name
        package = installed / name
        shutil.copytree(source, package)

        assert (package / ".codex-plugin/plugin.json").is_file()
        assert (package / "LICENSE").is_file()
        skill = package / "skills/feature-sliced-design"
        frontmatter = yaml.safe_load((skill / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1])
        entries = json.loads((package / "references/bundle-manifest.json").read_text(encoding="utf-8"))["entries"]
        entry = next(item for item in entries if item["canonical_name"] == "feature-sliced-design")
        for field in ("source_author", "source_license", "source_repo"):
            assert frontmatter["metadata"][field] == entry[field]
        assert (skill / "references/migration-guide.md").is_file()
        for link in _local_links(skill):
            assert link.is_file(), f"unresolved installed skill reference: {link}"
        assert not any(path.is_symlink() for path in package.rglob("*"))

    copies = [
        (installed / name / "skills/feature-sliced-design/references/migration-guide.md").read_bytes()
        for name in PLUGIN_NAMES
    ]
    assert copies[0] == copies[1]
