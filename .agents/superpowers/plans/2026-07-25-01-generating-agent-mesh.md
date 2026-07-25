# Generating Agent Mesh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the first-party skill `generating-index-mesh` to `generating-agent-mesh` and ship a generic `validate-agent-mesh` command that the `repo-standards` preflight can call.

**Architecture:** Keep the existing `generate-index-mesh` behavior intact, add `validate-agent-mesh` as a new core + wrapper pair under the renamed skill, and update the `repo-standards` preflight templates to call `validate-agent-mesh` after index generation and before skill refresh. Update the marketplace registry and all source references to the new skill name, then regenerate all derived marketplace surfaces with the canonical tooling.

**Tech Stack:** Python 3.13, bash, PowerShell, git, `py -3` launcher.

## Global Constraints

- Work in the isolated worktree at `Z:\_agent-worktrees\agent-asset-marketplace\repo-standards-design`.
- All text files must be written with LF line endings (`newline="\n"`).
- Any source-custody or skill change requires `py -3 tools/rebuild_marketplace.py` then `py -3 tools/check_marketplace.py` before the plan may be called green.
- Projection surfaces (plugin roots, bundle manifests, installed skills, `generated/skill-zips/`) are generated, not hand-edited.
- Use `git mv` for the skill directory rename so git tracks the move.
- The final commit message is `feat: rename generating-index-mesh to generating-agent-mesh and ship validate-agent-mesh`.

---

### Task 1: Rename the source root and refresh skill identity

**Files:**
- Rename: `sources/first_party/skills/generating-index-mesh` → `sources/first_party/skills/generating-agent-mesh`
- Modify: `sources/first_party/skills/generating-agent-mesh/SKILL.md`
- Modify: `sources/first_party/skills/generating-agent-mesh/agents/openai.yaml`
- Modify: `sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py:183`

- [ ] **Step 1: Rename the source directory with git mv**

```bash
cd Z:\_agent-worktrees\agent-asset-marketplace\repo-standards-design
git mv sources/first_party/skills/generating-index-mesh sources/first_party/skills/generating-agent-mesh
```

Expected: `git status` shows the directory rename.

- [ ] **Step 2: Write the new `SKILL.md`**

```markdown
---
name: generating-agent-mesh
description: Use when the repo-wide INDEX.md mesh or agent-mesh validation is stale, or as a CI/pre-commit gate.
metadata:
  source-id: generating-agent-mesh
  source-path: sources/first_party/skills/generating-agent-mesh/SKILL.md
  provenance-name: Generating Agent Mesh first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Run the repository's generate_index_mesh.py and validate_agent_mesh.py commands.
  use_when:
  - Use when INDEX.md files are stale after skill, plugin, or source changes.
  - Use when verifying the navigation mesh, local markdown links, and doctrine routing in CI or as a pre-commit gate.
  do_not_use_when:
  - Do not use when installing or refreshing skills from the plugin source.
  related_skills:
  - repo-standards
  - refreshing-installed-skills
license: MIT
---

# Generating Agent Mesh

Run the repository's index mesh generator and agent mesh validator.

## When to Use

- After changing skill, plugin, or source files that affect generated `INDEX.md` navigation.
- In CI or as a pre-commit hook to verify the mesh and local markdown links are current.

## Usage

```bash
# Generate or check the INDEX.md mesh
py -3 .agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py
py -3 .agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py --check

# Validate the agent mesh (local links + doctrine routing)
py -3 .agents/skills/generating-agent-mesh/scripts/validate_agent_mesh.py --check
py -3 .agents/skills/generating-agent-mesh/scripts/validate_agent_mesh.py --check --changed-from HEAD
```

The wrapper commands `generate-index-mesh` and `validate-agent-mesh` in the same directory call these Python cores and are the form used by `repo-standards` preflight.

This skill discovers the repo's `tools/generate_index_mesh.py` (source repo) or `scripts/generate_index_mesh.py` (consumer repo) for `generate-index-mesh`, and runs the bundled `validate_agent_mesh.py` for `validate-agent-mesh`. It does not commit; the caller decides whether to commit regenerated or validated state.

## Repo-specific validation extensions

`validate-agent-mesh` runs an optional extra hook if one exists:
- `scripts/validate_agent_mesh_extra.sh` — bash script; receives `--check` and optional `--changed-from <ref>`.
- `scripts/validate_agent_mesh_extra.ps1` — PowerShell script; must declare `param([switch]$Check, [string]$ChangedFrom)`.

The hook should print findings as `DRIFT: <message>` and exit non-zero on failure. Any stdout/stderr not prefixed with `DRIFT:` is reported as an extra-hook error.
```

- [ ] **Step 3: Write the new `agents/openai.yaml`**

```yaml
version: 1
metadata:
  skill_name: generating-agent-mesh
  source_category: first_party
interface:
  display_name: Generating Agent Mesh
  short_description: Use when the repo-wide INDEX.md mesh is stale or agent-mesh validation is needed.
  default_prompt: Use generating-agent-mesh when the repo-wide INDEX.md mesh is stale or when validating the agent mesh.
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 4: Update the generated INDEX.md footer line**

In `sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py` around line 183, replace:

```python
lines.append("This index is generated by the `generating-index-mesh` skill (`.agents/skills/generating-index-mesh/scripts/generate-index-mesh`).")
```

with:

```python
lines.append("This index is generated by the `generating-agent-mesh` skill (`.agents/skills/generating-agent-mesh/scripts/generate-index-mesh`).")
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "refactor: rename generating-index-mesh source root to generating-agent-mesh"
```

---

### Task 2: Add the `validate-agent-mesh` core and wrappers

**Files:**
- Create: `sources/first_party/skills/generating-agent-mesh/scripts/validate_agent_mesh.py`
- Create: `sources/first_party/skills/generating-agent-mesh/scripts/validate-agent-mesh.sh`
- Create: `sources/first_party/skills/generating-agent-mesh/scripts/validate-agent-mesh.ps1`

- [ ] **Step 1: Write `validate_agent_mesh.py`**

```python
#!/usr/bin/env python3
"""Validate the repo-wide agent mesh.

Checks that local markdown links in mesh surfaces resolve inside the repo, that
active doctrine files are reachable from an INDEX.md or AGENTS.md link in an
ancestor directory, and runs a repo-specific extra hook if present.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

EXCLUDED_DIR_NAMES = {
    ".git",
    ".worktrees",
    "__pycache__",
    ".pytest_cache",
    ".superpowers",
    "superpowers",  # covers .agents/superpowers/plans session-artifacts
    "marketplace-source",
    "third_party",  # retained upstream snapshots are not repo-owned mesh
}

NON_SOURCE_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".zip", ".tar", ".gz",
    ".tgz", ".bz2", ".xz", ".7z", ".rar", ".exe", ".dll", ".so", ".dylib",
    ".pyc", ".pyo", ".pyd", ".pdf", ".docx", ".xlsx", ".pptx", ".otf", ".ttf",
    ".woff", ".woff2", ".eot", ".mp3", ".mp4", ".mov", ".avi", ".webm",
    ".ogg", ".wav", ".flac", ".DS_Store", ".db", ".sqlite", ".sqlite3",
    ".lockb",
}

MESH_LINK_FILE_NAMES = {"INDEX.md", "AGENTS.md", "SKILL.md"}


def _stripped_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip())


def _load_tracked(repo_root: Path) -> tuple[set[Path], set[Path]]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    tracked_dirs: set[Path] = set()
    tracked_files: set[Path] = set()
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = repo_root / line
        tracked_files.add(path)
        tracked_dirs.add(path.parent)
        for parent in path.parents:
            if parent == repo_root:
                break
            tracked_dirs.add(parent)
    return tracked_dirs, tracked_files


def _changed_files(ref: str, repo_root: Path) -> list[Path]:
    for args in (
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{ref}..."],
        ["git", "diff", "--name-only", ref],
    ):
        result = subprocess.run(
            args,
            cwd=repo_root,
            capture_output=True,
            text=True,
            env=_stripped_env(),
        )
        if result.returncode == 0:
            return [repo_root / line for line in result.stdout.splitlines() if line.strip()]
    raise RuntimeError(f"Could not determine changed files for ref {ref!r}")


def _is_under(path: Path, ancestor: Path) -> bool:
    return path == ancestor or ancestor in path.parents


def _should_examine(path: Path, repo_root: Path) -> bool:
    if not path.exists():
        return False
    try:
        rel = path.relative_to(repo_root)
    except ValueError:
        return False
    for part in rel.parts:
        if part in EXCLUDED_DIR_NAMES:
            return False
    if path.is_dir():
        return False
    if path.suffix.lower() in NON_SOURCE_SUFFIXES:
        return False
    return True


def _link_candidates(current_file: Path, raw_target: str, repo_root: Path) -> list[Path]:
    if raw_target.startswith(("http://", "https://", "mailto:")):
        return []
    clean = raw_target.split("#", 1)[0]
    if not clean:
        return []
    clean = clean.lstrip("/")
    candidates: list[Path] = []
    seen: set[Path] = set()
    for base in (current_file.parent, repo_root):
        try:
            resolved = (base / clean).resolve()
        except (OSError, ValueError):
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if _is_under(resolved, repo_root):
            candidates.append(resolved)
    return candidates


def _is_mesh_link_file(path: Path, repo_root: Path) -> bool:
    if path.suffix.lower() not in {".md", ".markdown"}:
        return False
    if path.name in MESH_LINK_FILE_NAMES:
        return True
    try:
        rel = path.relative_to(repo_root)
    except ValueError:
        return False
    # Any markdown under a docs/ tree is part of the mesh we link-check.
    if len(rel.parts) > 1 and any(part == "docs" for part in rel.parts[:-1]):
        return True
    return False


def _collect_link_findings(repo_root: Path, files: list[Path]) -> list[str]:
    findings: list[str] = []
    for path in files:
        if not _should_examine(path, repo_root) or not _is_mesh_link_file(path, repo_root):
            continue
        rel = path.relative_to(repo_root)
        try:
            content = path.read_text(encoding="utf-8", newline="\n")
        except (OSError, UnicodeDecodeError):
            continue
        for _label, raw_target in LINK_PATTERN.findall(content):
            candidates = _link_candidates(path, raw_target, repo_root)
            if not candidates:
                continue
            if raw_target.endswith("/"):
                if not any(c.is_dir() for c in candidates):
                    findings.append(f"broken link: {rel.as_posix()} -> {raw_target}")
                continue
            if not any(c.exists() for c in candidates):
                findings.append(f"broken link: {rel.as_posix()} -> {raw_target}")
    return findings


def _is_active_doctrine(path: Path) -> bool:
    if path.suffix.lower() not in {".md", ".markdown"}:
        return False
    try:
        content = path.read_text(encoding="utf-8", newline="\n")
    except (OSError, UnicodeDecodeError):
        return False
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return False
    return re.search(r"^\s*status:\s*active\s*$", match.group(1), re.MULTILINE | re.IGNORECASE) is not None


def _links_from(index_file: Path, repo_root: Path) -> set[Path]:
    try:
        content = index_file.read_text(encoding="utf-8", newline="\n")
    except (OSError, UnicodeDecodeError):
        return set()
    targets: set[Path] = set()
    for _label, raw_target in LINK_PATTERN.findall(content):
        candidates = _link_candidates(index_file, raw_target, repo_root)
        for resolved in candidates:
            if resolved.exists():
                targets.add(resolved)
                if resolved.is_dir():
                    targets.add(resolved)
                break
    return targets


def _collect_doctrine_route_findings(repo_root: Path, files: list[Path]) -> list[str]:
    doctrine_files = [p for p in files if _is_active_doctrine(p)]
    if not doctrine_files:
        return []
    findings: list[str] = []
    index_links: dict[Path, set[Path]] = {}
    for doctrine in doctrine_files:
        rel = doctrine.relative_to(repo_root)
        routed = False
        for ancestor in doctrine.parents:
            if not _is_under(ancestor, repo_root):
                break
            for idx_name in ("INDEX.md", "AGENTS.md"):
                idx = ancestor / idx_name
                if not idx.is_file():
                    continue
                if idx not in index_links:
                    index_links[idx] = _links_from(idx, repo_root)
                if doctrine in index_links[idx] or doctrine.parent in index_links[idx]:
                    routed = True
                    break
            if routed:
                break
        if not routed:
            findings.append(f"active doctrine not routed: {rel.as_posix()}")
    return findings


def _collect_retired_token_findings(
    repo_root: Path, files: list[Path], retired_tokens: tuple[str, ...] = ()
) -> list[str]:
    findings: list[str] = []
    for token in retired_tokens:
        for path in files:
            if not _should_examine(path, repo_root):
                continue
            try:
                content = path.read_text(encoding="utf-8", newline="\n")
            except (OSError, UnicodeDecodeError):
                continue
            if token in content:
                findings.append(f"retired token {token!r} in {path.relative_to(repo_root).as_posix()}")
    return findings


def _powershell_cmd() -> list[str]:
    for name in ("pwsh", "powershell"):
        if shutil.which(name):
            return [name, "-NoProfile", "-File"]
    return ["powershell", "-NoProfile", "-File"]


def _run_extra_hook(repo_root: Path, changed_from: str | None, check: bool) -> list[str]:
    findings: list[str] = []
    hook_sh = repo_root / "scripts" / "validate_agent_mesh_extra.sh"
    hook_ps1 = repo_root / "scripts" / "validate_agent_mesh_extra.ps1"

    # Prefer .ps1 on Windows and .sh elsewhere, but allow fallback.
    if sys.platform == "win32" and hook_ps1.is_file():
        cmd = _powershell_cmd() + [str(hook_ps1)]
        if check:
            cmd.append("-Check")
        if changed_from:
            cmd.extend(["-ChangedFrom", changed_from])
    elif hook_sh.is_file():
        cmd = ["bash", str(hook_sh)]
        if check:
            cmd.append("--check")
        if changed_from:
            cmd.extend(["--changed-from", changed_from])
    elif hook_ps1.is_file():
        cmd = _powershell_cmd() + [str(hook_ps1)]
        if check:
            cmd.append("-Check")
        if changed_from:
            cmd.extend(["-ChangedFrom", changed_from])
    else:
        return findings

    result = subprocess.run(
        cmd,
        cwd=repo_root,
        capture_output=True,
        text=True,
        env=_stripped_env(),
    )
    for line in result.stdout.splitlines():
        if line.startswith("DRIFT:") or line.startswith("drift:"):
            findings.append(line[6:].strip())
    if result.returncode != 0:
        for line in result.stdout.splitlines() + result.stderr.splitlines():
            line = line.strip()
            if line and not line.startswith("DRIFT:") and not line.startswith("drift:"):
                findings.append(f"extra hook: {line}")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the repo-wide agent mesh")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report drift without writing (validation is always read-only)",
    )
    parser.add_argument(
        "--changed-from",
        type=str,
        default=None,
        help="Only examine files changed since this git ref",
    )
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    _tracked_dirs, tracked_files = _load_tracked(repo_root)

    if args.changed_from:
        files = _changed_files(args.changed_from, repo_root)
    else:
        files = list(tracked_files)

    files = [p for p in files if _should_examine(p, repo_root)]

    findings: list[str] = []
    findings.extend(_collect_link_findings(repo_root, files))
    findings.extend(_collect_doctrine_route_findings(repo_root, files))
    findings.extend(_collect_retired_token_findings(repo_root, files))
    findings.extend(_run_extra_hook(repo_root, args.changed_from, args.check))

    if findings:
        for finding in findings:
            print(f"DRIFT: {finding}", file=sys.stderr)
        return 1

    print("OK agent mesh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Write the bash wrapper `validate-agent-mesh.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for python in python3 python; do
    if command -v "$python" >/dev/null 2>&1; then
        exec "$python" "${SCRIPT_DIR}/validate_agent_mesh.py" "$@"
    fi
done
echo "No Python interpreter found" >&2
exit 1
```

- [ ] **Step 3: Write the PowerShell wrapper `validate-agent-mesh.ps1`**

```powershell
<#
.SYNOPSIS
  Validate the repo-wide agent mesh.
#>
[CmdletBinding()]
param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Remaining)
$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$python = $null
foreach ($l in @('py', 'python', 'python3')) {
    if (Get-Command $l -ErrorAction SilentlyContinue) {
        $python = $l
        break
    }
}
if (-not $python) {
    throw "No Python interpreter found"
}

if ($python -eq 'py') {
    & py -3 "$scriptDir\validate_agent_mesh.py" @Remaining
} else {
    & $python "$scriptDir\validate_agent_mesh.py" @Remaining
}
exit $LASTEXITCODE
```

- [ ] **Step 4: Smoke test the new core**

Run:

```bash
py -3 sources/first_party/skills/generating-agent-mesh/scripts/validate_agent_mesh.py --help
```

Expected: argparse help output with `--check` and `--changed-from` options.

- [ ] **Step 5: Commit**

```bash
git add sources/first_party/skills/generating-agent-mesh/scripts/validate_agent_mesh.py \
        sources/first_party/skills/generating-agent-mesh/scripts/validate-agent-mesh.sh \
        sources/first_party/skills/generating-agent-mesh/scripts/validate-agent-mesh.ps1
git commit -m "feat: add validate-agent-mesh core and wrappers"
```

---

### Task 3: Update dependents and the marketplace registry

**Files:**
- Modify: `codex-marketplace/custody-pack-registry.json`
- Modify: `sources/first_party/skills/refreshing-installed-skills/SKILL.md`
- Modify: `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
- Modify: `sources/first_party/skills/repo-standards/templates/ci-preflight.sh`
- Modify: `sources/first_party/skills/repo-standards/templates/ci-preflight.ps1`
- Modify: `tools/rebuild_marketplace.py`
- Modify: `tools/AGENTS.md`
- Modify: `tests/test_generate_index_mesh.py`
- Modify: `tests/test_refresh_installed_skills.py`
- Modify: `tests/test_worktree_scripts.py`

- [ ] **Step 1: Update `codex-marketplace/custody-pack-registry.json`**

Run this Python one-liner in the repo root:

```bash
py -3 - <<'PY'
import pathlib
p = pathlib.Path('codex-marketplace/custody-pack-registry.json')
t = p.read_text(encoding='utf-8', newline='\n')
t = t.replace('sources/first_party/skills/generating-index-mesh', 'sources/first_party/skills/generating-agent-mesh')
t = t.replace('skills/generating-index-mesh', 'skills/generating-agent-mesh')
t = t.replace('generating-index-mesh', 'generating-agent-mesh')
p.write_text(t, encoding='utf-8', newline='\n')
PY
```

Expected: no output; `grep generating-index-mesh codex-marketplace/custody-pack-registry.json` returns nothing.

- [ ] **Step 2: Update `refreshing-installed-skills/SKILL.md`**

Write the full file:

```markdown
---
name: refreshing-installed-skills
description: Use when a worktree is initialized or .agents/skills/ is stale from the plugin source.
metadata:
  source-id: refreshing-installed-skills
  source-path: sources/first_party/skills/refreshing-installed-skills/SKILL.md
  provenance-name: Refreshing Installed Skills first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Install or refresh .agents/skills/ from the plugin source and regenerate the agent mesh.
  use_when:
  - Use when creating a new worktree.
  - Use after updating the marketplace-source submodule.
  - Use when .agents/skills/ appears stale.
  do_not_use_when:
  - Do not use when only the INDEX.md mesh is stale without any skill changes; use generating-agent-mesh instead.
  related_skills:
  - generating-agent-mesh
  - using-git-worktrees
license: MIT
---

# Refreshing Installed Skills

Install or refresh `.agents/skills/` from the plugin source, then regenerate the agent mesh.

## When to Use

- After creating a new worktree.
- After updating the `marketplace-source` submodule in a consumer repo.
- When `.agents/skills/` appears stale.

## Usage

```bash
py -3 .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py
py -3 .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --check
```

This skill discovers the repo's `tools/install_agent_skills.py` (source repo) or `scripts/install_agent_skills.py` (consumer repo), runs it, then runs `generating-agent-mesh`. If changes were made, it commits them with the message `chore: refresh installed skills and regenerate agent mesh`.
```

- [ ] **Step 3: Update `refreshing-installed-skills/scripts/refresh_installed_skills.py`**

Replace the mesh script candidates in `_regenerate_index_mesh` (around lines 389-391):

```python
    candidates = [
        repo_root / ".agents" / "skills" / "generating-agent-mesh" / "scripts" / "generate_index_mesh.py",
        repo_root / ".agents" / "plugins" / "marketplace-source" / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills" / "generating-agent-mesh" / "scripts" / "generate_index_mesh.py",
    ]
```

- [ ] **Step 4: Write the new `repo-standards/templates/ci-preflight.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

find_skill_script() {
    local skill="$1" core="$2"
    local installed="$REPO_ROOT/.agents/skills/$skill/scripts/$core.sh"
    if [ -f "$installed" ]; then echo "$installed"; return; fi

    local mp_source="$REPO_ROOT/.agents/plugins/marketplace-source/codex-marketplace/plugins"
    if [ -d "$mp_source" ]; then
        local found
        found=$(find "$mp_source" -path "*/skills/$skill/scripts/$core.sh" -maxdepth 4 -print -quit 2>/dev/null)
        if [ -n "$found" ]; then echo "$found"; return; fi
    fi
    echo "$skill $core wrapper not found" >&2; exit 1
}

CHECK=""
FULL=""
CHANGED_FROM=""
while [ $# -gt 0 ]; do
    case "$1" in
        --check) CHECK="--check" ;;
        --full) FULL="1" ;;
        --changed-from)
            shift
            CHANGED_FROM="$1"
            ;;
        *) echo "unknown arg: $1" >&2; exit 1 ;;
    esac
    shift
done

STANDARDS=$(find_skill_script repo-standards repo-standards)
SCAFFOLD=$(find_skill_script repo-standards scaffold-all)
MESH=$(find_skill_script generating-agent-mesh generate-index-mesh)
VALIDATE=$(find_skill_script generating-agent-mesh validate-agent-mesh)
REFRESH=$(find_skill_script refreshing-installed-skills refresh-installed-skills)

STANDARDS_ARGS=()
[ -n "$CHECK" ] && STANDARDS_ARGS+=("--check")
"$STANDARDS" "${STANDARDS_ARGS[@]}"

SCAFFOLD_ARGS=()
[ -n "$CHECK" ] && SCAFFOLD_ARGS+=("--check")
"$SCAFFOLD" "${SCAFFOLD_ARGS[@]}"

MESH_ARGS=()
[ -n "$CHECK" ] && MESH_ARGS+=("--check")
# generate-index-mesh reconciles the whole tracked mesh; scoped diff is
# handled by validate-agent-mesh and the optional ci-preflight-extra hook.
"$MESH" "${MESH_ARGS[@]}"

VALIDATE_ARGS=()
[ -n "$CHECK" ] && VALIDATE_ARGS+=("--check")
[ -n "$CHANGED_FROM" ] && VALIDATE_ARGS+=("--changed-from" "$CHANGED_FROM")
"$VALIDATE" "${VALIDATE_ARGS[@]}"

REFRESH_ARGS=()
[ -n "$CHECK" ] && REFRESH_ARGS+=("--check")
"$REFRESH" "${REFRESH_ARGS[@]}"

EXTRA="$SCRIPT_DIR/ci-preflight-extra.sh"
if [ -f "$EXTRA" ]; then
    EXTRA_ARGS=()
    [ -n "$CHECK" ] && EXTRA_ARGS+=("--check")
    [ -n "$CHANGED_FROM" ] && EXTRA_ARGS+=("--changed-from" "$CHANGED_FROM")
    "$EXTRA" "${EXTRA_ARGS[@]}"
fi
```

- [ ] **Step 5: Write the new `repo-standards/templates/ci-preflight.ps1`**

```powershell
<#
.SYNOPSIS
  Run the repository preflight checks for local and CI use.
#>
[CmdletBinding()]
param(
    [switch]$Check,
    [switch]$Full,
    [string]$ChangedFrom
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ScriptDir = (Resolve-Path $PSScriptRoot).Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir '..')).Path

function Find-SkillScript($skill, $core) {
    $installed = Join-Path $RepoRoot ".agents/skills/$skill/scripts/$core.ps1"
    if (Test-Path $installed) { return $installed }

    $marketplaceSource = Join-Path $RepoRoot ".agents/plugins/marketplace-source/codex-marketplace/plugins"
    if (Test-Path $marketplaceSource) {
        $glob = Join-Path $marketplaceSource "*/skills/$skill/scripts/$core.ps1"
        $found = @(Get-Item $glob -ErrorAction SilentlyContinue)
        if ($found.Count -gt 0) { return $found[0].FullName }
    }
    throw "$skill $core wrapper not found"
}

$standards = Find-SkillScript 'repo-standards' 'repo-standards'
$scaffold = Find-SkillScript 'repo-standards' 'scaffold-all'
$mesh = Find-SkillScript 'generating-agent-mesh' 'generate-index-mesh'
$validate = Find-SkillScript 'generating-agent-mesh' 'validate-agent-mesh'
$refresh = Find-SkillScript 'refreshing-installed-skills' 'refresh-installed-skills'

& $standards -Check:$Check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $scaffold -Check:$Check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# generate-index-mesh reconciles the whole tracked mesh; scoped diff is
# handled by validate-agent-mesh and the optional ci-preflight-extra hook.
& $mesh -Check:$Check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$validateArgs = @()
if ($Check) { $validateArgs += '--check' }
if ($ChangedFrom) { $validateArgs += '--changed-from'; $validateArgs += $ChangedFrom }
& $validate @validateArgs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $refresh -Check:$Check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$extra = Join-Path $ScriptDir 'ci-preflight-extra.ps1'
if (Test-Path $extra) {
    & $extra -Check:$Check -ChangedFrom:$ChangedFrom
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

exit 0
```

- [ ] **Step 6: Update `tools/rebuild_marketplace.py`**

Replace all occurrences of `generating-index-mesh` with `generating-agent-mesh` in `tools/rebuild_marketplace.py` (lines 145-148):

```bash
py -3 - <<'PY'
import pathlib
p = pathlib.Path('tools/rebuild_marketplace.py')
t = p.read_text(encoding='utf-8', newline='\n')
t = t.replace('generating-index-mesh', 'generating-agent-mesh')
p.write_text(t, encoding='utf-8', newline='\n')
PY
```

- [ ] **Step 7: Update `tools/AGENTS.md`**

Replace the mesh command reference:

```diff
- itself. The repo-wide `INDEX.md` mesh is proven by `py -3 sources/first_party/skills/generating-index-mesh/scripts/generate_index_mesh.py
+ itself. The repo-wide `INDEX.md` mesh is proven by `py -3 sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py
 --check`, and mesh law lives in `../.agents/docs/mesh-policy.md`.
```

- [ ] **Step 8: Update test files for the new source path**

Update `tests/test_generate_index_mesh.py`:

```bash
py -3 - <<'PY'
import pathlib
p = pathlib.Path('tests/test_generate_index_mesh.py')
t = p.read_text(encoding='utf-8', newline='\n')
t = t.replace('generating-index-mesh', 'generating-agent-mesh')
p.write_text(t, encoding='utf-8', newline='\n')
PY
```

Update `tests/test_refresh_installed_skills.py`:

```bash
py -3 - <<'PY'
import pathlib
p = pathlib.Path('tests/test_refresh_installed_skills.py')
t = p.read_text(encoding='utf-8', newline='\n')
t = t.replace('generating-index-mesh', 'generating-agent-mesh')
p.write_text(t, encoding='utf-8', newline='\n')
PY
```

Update `tests/test_worktree_scripts.py`:

```bash
py -3 - <<'PY'
import pathlib
p = pathlib.Path('tests/test_worktree_scripts.py')
t = p.read_text(encoding='utf-8', newline='\n')
t = t.replace('generating-index-mesh', 'generating-agent-mesh')
p.write_text(t, encoding='utf-8', newline='\n')
PY
```

Expected: `grep generating-index-mesh tests/test_generate_index_mesh.py tests/test_refresh_installed_skills.py tests/test_worktree_scripts.py` returns nothing.

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "chore: align generating-index-mesh references to generating-agent-mesh"
```

---

### Task 4: Add `tests/test_validate_agent_mesh.py`

**Files:**
- Create: `tests/test_validate_agent_mesh.py`

- [ ] **Step 1: Write the test file**

```python
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CORE = (
    REPO_ROOT
    / "sources"
    / "first_party"
    / "skills"
    / "generating-agent-mesh"
    / "scripts"
    / "validate_agent_mesh.py"
)


def _stripped_env():
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def test_source_repo_agent_mesh_passes() -> None:
    """The current checkout's agent mesh is valid."""
    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=REPO_ROOT,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "OK agent mesh" in result.stdout


def test_broken_markdown_link_fails(tmp_path: Path) -> None:
    """A repo with a broken local link in an INDEX.md fails validation."""
    repo = tmp_path / "broken-link-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)

    (repo / "INDEX.md").write_text(
        "# Test\n[broken](./missing.md)\n",
        encoding="utf-8",
        newline="\n",
    )
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)

    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "broken link" in result.stderr.lower()
```

- [ ] **Step 2: Run the failing-case test only (the source-repo test needs regenerated indexes first)**

```bash
py -3 -m pytest tests/test_validate_agent_mesh.py::test_broken_markdown_link_fails -v
```

Expected: `test_broken_markdown_link_fails` PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/test_validate_agent_mesh.py
git commit -m "test: add validate-agent-mesh coverage"
```

---

### Task 5: Regenerate marketplace, scaffold root preflight, final validation

**Files:**
- Generated: all marketplace surfaces via `py -3 tools/rebuild_marketplace.py`
- Generated: `scripts/ci-preflight.sh` and `scripts/ci-preflight.ps1` via `scaffold_ci_preflight.py --force`

- [ ] **Step 1: Scaffold the root `scripts/ci-preflight.*` from the updated templates**

```bash
py -3 sources/first_party/skills/repo-standards/scripts/scaffold_ci_preflight.py --force
```

Expected output includes:

```
wrote scripts/ci-preflight.sh
wrote scripts/ci-preflight.ps1
```

- [ ] **Step 2: Regenerate the marketplace**

```bash
py -3 tools/rebuild_marketplace.py
```

Expected: completes without error; emits "Wrote index mesh", "OK marketplace", and similar success lines. There will be many file writes and prunes as the skill rename is projected.

- [ ] **Step 3: Run the marketplace check**

```bash
py -3 tools/check_marketplace.py
```

Expected: exit code 0.

- [ ] **Step 4: Run `validate-agent-mesh` on the source repo**

```bash
py -3 sources/first_party/skills/generating-agent-mesh/scripts/validate_agent_mesh.py --check
```

Expected: `OK agent mesh`.

- [ ] **Step 5: Run the new test file**

```bash
py -3 -m pytest tests/test_validate_agent_mesh.py -v
```

Expected: both tests PASS.

- [ ] **Step 6: Stage and commit the full change**

```bash
git add -A
git commit -m "feat: rename generating-index-mesh to generating-agent-mesh and ship validate-agent-mesh"
```

---

## Execution Confidence Rating

**8/10.**

The exact file paths, skill names, registry occurrences, and tooling references were verified against the current repo tree. The `validate-agent-mesh` algorithm is specified concretely (link candidates from both file-relative and repo-root-relative bases, doctrine routing via ancestor `INDEX.md`/`AGENTS.md` links, and a repo-specific extension hook). Prototype scans showed zero broken links and zero unrouted active doctrine files when the validator is scoped to mesh surfaces (`INDEX.md`, `AGENTS.md`, `SKILL.md`, and `docs`/`.agents/docs` markdown) and excludes retained upstream (`third_party`) and session-artifact (`superpowers` plans) directories.

Known caveats that lower the rating from 9/10:

- `tests/test_generate_index_mesh.py`, `tests/test_refresh_installed_skills.py`, and one test in `tests/test_worktree_scripts.py` are pre-existing failures unrelated to this rename; only their source-path references are updated here.
- `rebuild_marketplace.py` projects many derived surfaces; if any unreferenced hard-coded `generating-index-mesh` strings remain outside the scoped files, the check phase will surface them and need a quick follow-up replacement.
- `generate-index-mesh` does not accept `--changed-from`; the preflight template deliberately runs a full mesh reconciliation and lets `validate-agent-mesh` and `ci-preflight-extra` handle scoped diff work. A future plan can add `--changed-from` to `generate_index_mesh.py` if scoped regeneration becomes required.
- Any `ci-preflight-extra.ps1` / `validate_agent_mesh_extra.ps1` hook must accept the same parameter contract as `ci-preflight.ps1`: `param([switch]$Check, [string]$ChangedFrom)`. The plan documents this contract in the `SKILL.md` and script comments.

The plan is self-contained: after execution, `generating-agent-mesh` exists, `validate-agent-mesh` runs green on the source repo, and the marketplace is regenerated and passes `check_marketplace.py`.
