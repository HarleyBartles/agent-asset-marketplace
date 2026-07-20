"""Create custody-aware skill scaffolds without overwriting authored files."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
from typing import Final


LANES: Final = {"first_party", "skills-with-source", "skills-with-citation"}
CUSTODIES: Final = {"local", "marketplace"}
LOCAL_PREFIX: Final = "mark-"
NAME_PATTERN: Final = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SCRIPT_ROOT = Path(__file__).resolve().parent
TEMPLATE_ROOT = SCRIPT_ROOT.parent / "templates"


def validate_request(name: str, custody: str, lane: str) -> None:
    if custody not in CUSTODIES:
        raise ValueError(f"unsupported custody: {custody}")
    if lane not in LANES:
        raise ValueError(f"unsupported lane: {lane}")
    if len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        raise ValueError("skill name must use lowercase letters, numbers, and single hyphens (64 characters maximum)")
    if custody == "local" and not name.startswith(LOCAL_PREFIX):
        raise ValueError("local custody requires the mark- prefix")
    if custody == "local" and lane != "first_party":
        raise ValueError("local custody requires the first_party lane")
    if custody == "marketplace" and name.startswith(LOCAL_PREFIX):
        raise ValueError("marketplace custody cannot use the mark- prefix")


def destination_for(repo_root: Path, name: str, custody: str) -> Path:
    if custody == "local":
        return repo_root / ".agents" / "skills" / name
    return repo_root / "sources" / "first_party" / "skills" / name


def _template(path: str, **values: str) -> str:
    return (TEMPLATE_ROOT / path).read_text(encoding="utf-8").format(**values).replace("\r\n", "\n").rstrip("\n") + "\n"


def render_scaffold(name: str, custody: str, lane: str) -> dict[str, str]:
    validate_request(name, custody, lane)
    files = {"SKILL.md": _template("skill/SKILL.md", name=name, custody=custody, lane=lane)}
    if custody == "local":
        return files
    files.update(
        {
            "references/.gitkeep": "\n",
            "assets/authority/authority.yaml": _template("authority/authority.yaml", name=name, custody=custody, lane=lane),
            "assets/authority/source-map.yaml": _template("authority/source-map.yaml", name=name, custody=custody, lane=lane),
            "assets/authority/CITATIONS.md": _template("authority/CITATIONS.md", name=name, custody=custody, lane=lane),
        }
    )
    if lane == "skills-with-source":
        files["assets/authority/reference-source/.gitkeep"] = "\n"
    return files


def _git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo_root, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def _guard_write_checkout(repo_root: Path, allow_shared_checkout: bool) -> Path:
    superproject = _git(repo_root, "rev-parse", "--show-superproject-working-tree")
    if superproject:
        raise ValueError("refusing to scaffold from a submodule checkout")
    checkout_root = Path(_git(repo_root, "rev-parse", "--show-toplevel")).resolve()
    git_dir = Path(_git(checkout_root, "rev-parse", "--path-format=absolute", "--git-dir")).resolve()
    common_dir = Path(_git(checkout_root, "rev-parse", "--path-format=absolute", "--git-common-dir")).resolve()
    if git_dir == common_dir:
        if not allow_shared_checkout:
            raise ValueError("refusing to scaffold from a shared main checkout; use --allow-shared-checkout with current human approval")
        print("WARNING: --allow-shared-checkout is active; current human approval is required.")
    return checkout_root


def scaffold(
    repo_root: Path, name: str, custody: str, lane: str, check: bool, *, allow_shared_checkout: bool = False
) -> int:
    validate_request(name, custody, lane)
    if not check:
        repo_root = _guard_write_checkout(repo_root, allow_shared_checkout)
    destination = destination_for(repo_root, name, custody)
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    files = render_scaffold(name, custody, lane)
    if check:
        for relative_path in files:
            print(destination / relative_path)
        return 0
    for relative_path, content in files.items():
        output_path = destination / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True)
    parser.add_argument("--custody", required=True, choices=sorted(CUSTODIES))
    parser.add_argument("--lane", required=True, choices=sorted(LANES))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--allow-shared-checkout", action="store_true")
    args = parser.parse_args()
    try:
        repo_root = Path.cwd().resolve()
        return scaffold(repo_root, args.name, args.custody, args.lane, args.check, allow_shared_checkout=args.allow_shared_checkout)
    except (OSError, subprocess.CalledProcessError, ValueError, FileExistsError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
