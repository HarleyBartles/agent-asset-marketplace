#!/usr/bin/env python3
"""Canonical non-mutating marketplace validation entrypoint."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _run_tool(script_name: str, *args: str) -> None:
    script_path = Path(__file__).resolve().with_name(script_name)
    subprocess.run([sys.executable, str(script_path), *args], check=True)


def _run_git(*args: str) -> None:
    subprocess.run(["git", *args], cwd=ROOT, check=True)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the non-mutating marketplace check stack")
    parser.add_argument("--base", default="origin/main", help="git revision used for generated drift validation")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    _run_tool("generate_plugin_root_inventory.py", "--check")
    # Verify overlay.yaml line edits are healthy — stale overlays (where
    # source normalization shifted line numbers or whitespace) must be
    # healed via rebuild_marketplace.py before CI can pass.
    _run_tool("heal_overlays.py", "--check")
    _run_tool("update_skill_artifacts.py", "--check", "--full-regeneration", "--base", args.base, "--skip-zip-content-validation")
    _run_tool("normalize_first_party_skill_sources.py", "--check")
    _run_tool("install_agent_skills.py", "--check")
    _run_tool("validate_marketplace.py", "--skip-freshness-checks")
    _run_tool("generate_index_mesh.py", "--check")
    _run_tool("validate_authority_assets.py")
    _run_git("diff", "--check")
    _run_git("diff", "--exit-code")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
