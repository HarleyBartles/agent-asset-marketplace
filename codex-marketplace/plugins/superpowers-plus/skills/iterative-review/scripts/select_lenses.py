#!/usr/bin/env python3
"""select_lenses.py - discover and select reviewer lens profiles for a PR. (read-only)"""

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path


def _reviewer_paths() -> list[Path]:
    """Return candidate reviewer-*.md paths in precedence order."""
    if sys.platform != "win32":
        user_root = Path.home() / ".config" / "devin" / "agents"
    else:
        user_root = Path.home() / "AppData" / "Roaming" / "devin" / "agents"
    roots = [
        user_root,
        Path(".devin/agents"),
        Path(".agents/agents"),
        Path(__file__).parents[3] / "skills" / "selecting-a-subagent" / "assets",
    ]
    seen = set()
    results = []
    for root in roots:
        if not root.exists():
            continue
        for p in sorted(root.glob("reviewer-*.md")):
            if p.name in seen:
                continue
            seen.add(p.name)
            results.append(p)
    return results


def _applies_to(text: str) -> dict:
    """Parse the ## Applies to section from a reviewer profile."""
    section_match = re.search(r"## Applies to(.*?)\n(?:## |\Z)", text, re.S)
    if not section_match:
        return {}
    section = section_match.group(1)

    def _list_items(name: str) -> list[str]:
        pattern = re.compile(rf"- {re.escape(name)}:\s*\n((?:[ \t]+- [^\n]*(?:\n|\Z))+)", re.S)
        m = pattern.search(section)
        if not m:
            return []
        lines = m.group(1).strip().splitlines()
        return [line.strip("- ").strip().strip("`") for line in lines if line.strip().startswith("-")]

    return {
        "globs": _list_items("globs"),
        "keywords": _list_items("keywords"),
        "inputs": _list_items("inputs"),
    }


def _changed_files(diff_path: Path | None) -> list[str]:
    if not diff_path or not diff_path.exists():
        return []
    text = diff_path.read_text(encoding="utf-8")
    pairs = re.findall(r"^diff --git a/(.+) b/(.+)$", text, re.M)
    return list(dict.fromkeys(f for pair in pairs for f in pair))


def _matches(rule: dict, changed: list[str], diff_text: str, pr_text: str, provided_inputs: list[str]) -> bool:
    for inp in rule.get("inputs", []):
        if inp in provided_inputs:
            return True
    for pattern in rule.get("globs", []):
        if any(fnmatch.fnmatch(f, pattern) for f in changed):
            return True
    for keyword in rule.get("keywords", []):
        if keyword.lower() in diff_text.lower() or keyword.lower() in pr_text.lower():
            return True
    return False


def _lenses_path(state: dict) -> Path:
    return Path(state["scratch_dir"]) / "lenses.jsonl"


def _load_state(state_path: Path) -> dict:
    with state_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _find_diff_path(scratch: Path) -> Path | None:
    candidates = list(scratch.glob("review-*..*.diff"))
    return candidates[0] if candidates else None


def _select(state: dict) -> list[dict]:
    scratch = Path(state["scratch_dir"])
    diff_path = _find_diff_path(scratch)
    pr_path = scratch / "pr_description"
    diff_text = diff_path.read_text(encoding="utf-8") if diff_path and diff_path.exists() else ""
    pr_text = pr_path.read_text(encoding="utf-8") if pr_path.exists() else ""
    changed = _changed_files(diff_path)
    provided = []
    if diff_path and diff_path.exists():
        provided.append("<diff_path>")
    if pr_path.exists():
        provided.append("<pr_description>")
    if (scratch / "scan_findings").exists():
        provided.append("<scan_findings>")
    if (scratch / "review-log-orchestrator-self-review.md").exists():
        provided.append("<review-log-orchestrator-self-review>")

    selected = []
    for profile in _reviewer_paths():
        text = profile.read_text(encoding="utf-8")
        rule = _applies_to(text)
        lens = profile.stem
        if _matches(rule, changed, diff_text, pr_text, provided) and lens not in {"reviewer-strong", "reviewer-fixes"}:
            selected.append(
                {
                    "lens": lens,
                    "profile_path": str(profile.resolve()),
                    "output_path": str((scratch / f"review-log-{lens}.md").resolve()),
                }
            )
    return selected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Select reviewer lenses for a PR. (read-only)")
    parser.add_argument("--state", help="Path to review-state.json")
    parser.add_argument("--apply", action="store_true", help="Write lenses.jsonl to the scratch dir")
    parser.add_argument("--check", action="store_true", help="Validate CLI contract only")
    args = parser.parse_args(argv)

    if args.check:
        print("select_lenses.py: --check ok")
        return 0

    if not args.state:
        parser.error("--state is required unless --check is used")

    state = _load_state(Path(args.state))
    selected = _select(state)

    out_path = _lenses_path(state)
    if args.apply:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            for entry in selected:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"Wrote {out_path} with {len(selected)} lens(es)")
    else:
        for entry in selected:
            print(entry["lens"], "->", entry["output_path"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
