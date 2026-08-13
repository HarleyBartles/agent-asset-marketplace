#!/usr/bin/env python3
"""Bootstrap an iterative review for a draft PR.

This script performs the `setup` and `normalize-inputs` nodes of the
iterative-review graph in one step. It creates the off-repo scratch
workspace, materializes the diff and PR context, and then hands control
back to the graph so the orchestrator can run `preflight` next.

(mixed: default is --check; --apply writes the scratch workspace.)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


REVIEW_NAME_PREFIX = "iterative-review"


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())


def _short_sha(ref: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short=7", ref],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def _resolve_base_commit(base_ref: str, head_ref: str, cwd: Path) -> str:
    """Return the merge-base commit between base and head.

    For a rebased PR the review diff is head relative to this commit.
    """
    base = base_ref if "/" in base_ref or base_ref == "HEAD" else f"origin/{base_ref}"
    result = subprocess.run(
        ["git", "merge-base", base, head_ref],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def _resolve_scratch_dir(repo_root: Path, pr_number: int) -> Path:
    """Return the off-repo scratch directory for this review."""
    common = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    main_checkout = Path(common).resolve().parent
    scratch_parent = main_checkout.parent
    repo_name = main_checkout.name

    branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    branch = re.sub(r'[\\/:*?"<>|]', "-", branch)

    workspace = scratch_parent / "_agent-scratch" / repo_name / branch
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace / f"{REVIEW_NAME_PREFIX}-{pr_number}"


def _pr_data(pr_number: int) -> dict:
    fields = [
        "number",
        "title",
        "body",
        "baseRefName",
        "headRefName",
        "headRefOid",
        "url",
    ]
    result = subprocess.run(
        ["gh", "pr", "view", str(pr_number), "--json", ",".join(fields)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def _generate_diff(
    repo_root: Path,
    base_commit: str,
    head_commit: str,
    out_path: Path,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as f:
        subprocess.run(
            [
                "git",
                "diff",
                "--no-color",
                "-U200",
                f"{base_commit}...{head_commit}",
            ],
            cwd=repo_root,
            stdout=f,
            check=True,
        )


def _bootstrap_review(pr_number: int, apply: bool) -> tuple[Path, dict, str, str]:
    repo_root = _repo_root()
    scratch_dir = _resolve_scratch_dir(repo_root, pr_number)

    pr = _pr_data(pr_number)
    base_ref = pr.get("baseRefName", "main")
    head_ref = pr.get("headRefName", "HEAD")
    head_sha = _short_sha(head_ref, repo_root)
    base_commit = _resolve_base_commit(base_ref, head_ref, repo_root)
    base_sha = _short_sha(base_commit, repo_root)

    if not apply:
        return scratch_dir, pr, base_sha, head_sha

    scratch_dir.mkdir(parents=True, exist_ok=True)

    (scratch_dir / "pr_description.txt").write_text(
        f"{pr.get('title', '')}\n\n{pr.get('body', '')}\n", encoding="utf-8"
    )

    diff_path = scratch_dir / f"review-{base_sha}..{head_sha}.diff"
    _generate_diff(repo_root, base_commit, head_ref, diff_path)

    state = {
        "current_node": "setup",
        "previous_node": "",
        "round": 1,
        "max_fix_rounds": 4,
        "pr": {
            "pr_number": pr_number,
            "base": base_ref,
            "branch": head_ref,
            "head_sha": head_sha,
            "url": pr.get("url", ""),
        },
        "scratch_dir": str(scratch_dir),
    }
    (scratch_dir / "review-state.json").write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return scratch_dir, pr, base_sha, head_sha


def _next_node_script() -> Path:
    return Path(__file__).with_name("next_node.py")


def _normalize_script() -> Path:
    return Path(__file__).with_name("normalize_review_inputs.py")


def _advance_to_node(node: str, state_path: Path) -> int:
    return subprocess.run(
        [sys.executable, str(_next_node_script()), "--propose", node, "--state", str(state_path)]
    ).returncode


def _discover_next_node(state_path: Path) -> tuple[str, str]:
    result = subprocess.run(
        [sys.executable, str(_next_node_script()), "--state", str(state_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = result.stdout.splitlines()
    node = lines[0].strip()
    return node, result.stdout


def _normalize_inputs(scratch_dir: Path) -> int:
    return subprocess.run(
        [
            sys.executable,
            str(_normalize_script()),
            "--source",
            str(scratch_dir),
            "--apply",
        ]
    ).returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap an iterative review for a draft PR.",
        epilog="(mixed: default is --check; --apply writes the scratch workspace.)",
    )
    parser.add_argument("--pr", type=int, help="PR number to review")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="create the scratch workspace, run normalize-inputs, and print the next allowed node",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report what start_review.py would do without writing files",
    )
    args = parser.parse_args(argv)

    if args.apply and args.check:
        print("error: --apply and --check are mutually exclusive", file=sys.stderr)
        return 2

    if not args.apply and not args.check:
        args.check = True

    if args.check:
        print("start_review.py is ready")
        return 0

    if args.pr is None:
        print("error: --pr is required when not using --check", file=sys.stderr)
        return 2

    try:
        scratch_dir, pr, base_sha, head_sha = _bootstrap_review(args.pr, apply=args.apply)
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    state_path = scratch_dir / "review-state.json"
    if _advance_to_node("normalize-inputs", state_path) != 0:
        return 1

    if _normalize_inputs(scratch_dir) != 0:
        return 1

    next_node, full_output = _discover_next_node(state_path)
    print(f"Started review for PR #{args.pr} at {scratch_dir}")
    print(f"Next allowed node:\n{full_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
