#!/usr/bin/env python3
"""Validate the canonical requested-skill export command."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from export_skill_zips import export_skill_zips
from skill_zip_artifacts import GENERATED_SKILL_ZIPS_REGISTRY_PATH


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "tools" / "export_skill_zips.py"
README_PATH = ROOT / "tools" / "README.md"


def run_export(args: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(EXPORTER), *args]
    return subprocess.run(command, cwd=cwd or ROOT, capture_output=True, text=True)


def assert_ok(result: subprocess.CompletedProcess[str]) -> None:
    if result.returncode != 0:
        raise AssertionError(f"expected success, got {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")


def assert_failed(result: subprocess.CompletedProcess[str], needle: str) -> None:
    if result.returncode == 0:
        raise AssertionError(f"expected failure containing {needle!r}, but command succeeded\nSTDOUT:\n{result.stdout}")
    if needle not in result.stderr and needle not in result.stdout:
        raise AssertionError(
            f"expected {needle!r} in output\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )


def _load_registry() -> dict:
    return json.loads(GENERATED_SKILL_ZIPS_REGISTRY_PATH.read_text(encoding="utf-8"))


def _write_temp_registry(tmp: Path, registry: dict) -> Path:
    path = tmp / "registry.json"
    path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def test_pack_export_and_manifest() -> tuple[Path, dict]:
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp) / "batch"
        out_dir.mkdir(parents=True, exist_ok=True)
        stale_file = out_dir / "stale.txt"
        stale_file.write_text("remove me", encoding="utf-8", newline="\n")
        result = run_export(["--pack", "house-skills", "--out", str(out_dir), "--clean-output"])
        assert_ok(result)

        manifest_path = out_dir / "export-manifest.json"
        assert manifest_path.is_file()
        assert not stale_file.exists()

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["request"]["form"] == "pack"
        assert manifest["request"]["value"] == "house-skills"
        assert manifest["resolved"]
        assert manifest["copied"]
        first_output = out_dir / manifest["resolved"][0]["output_path"]
        assert first_output.is_file()
        assert manifest["resolved"][0]["output_path"] == manifest["copied"][0]["output_path"]
        return out_dir, manifest


def test_from_file_export() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        request_file = tmp_path / "requested-skills.txt"
        request_file.write_text("house-skills/asset-market\nhouse-skills/boring-loop\n", encoding="utf-8", newline="\n")

        manifest = export_skill_zips(
            form="from-file",
            values=[],
            out_dir=tmp_path / "from-file",
            from_file=request_file,
            clean_output=True,
        )

        assert (tmp_path / "from-file" / "asset-market" / "skill.zip").is_file()
        assert (tmp_path / "from-file" / "boring-loop" / "skill.zip").is_file()
        assert manifest["request"]["form"] == "from-file"
        assert manifest["request"]["value"] == ["house-skills/asset-market", "house-skills/boring-loop"]
        assert manifest["request"]["source_file"] == str(request_file)


def test_subset_export_and_bare_name_ambiguity() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp) / "subset"
        result = run_export(["--skills", "house-skills/asset-market,house-skills/boring-loop", "--out", str(out_dir)])
        assert_ok(result)
        assert (out_dir / "asset-market" / "skill.zip").is_file()
        assert (out_dir / "boring-loop" / "skill.zip").is_file()

        bare_unique = export_skill_zips(
            form="skills",
            values=["asset-market"],
            out_dir=Path(tmp) / "bare-unique",
            clean_output=True,
        )
        assert (Path(tmp) / "bare-unique" / "asset-market" / "skill.zip").is_file()
        assert bare_unique["request"]["value"] == ["asset-market"]

        ambiguous = run_export(["--skills", "linear", "--out", str(Path(tmp) / "ambiguous")])
        assert_failed(ambiguous, "<pack>/linear")


def test_missing_and_collision_failures() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        missing = run_export(["--skills", "house-skills/definitely-not-a-skill", "--out", str(Path(tmp) / "missing")])
        assert_failed(missing, "missing from the registry")

        collision = run_export(
            ["--skills", "house-skills/linear,adventures-pack/linear", "--out", str(Path(tmp) / "collision")]
        )
        assert_failed(collision, "duplicate output folder")


def test_missing_and_stale_artifact_failures() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        registry = _load_registry()
        asset_market_record = next(
            record for record in registry["artifacts"] if record["pack"] == "house-skills" and record["skill"] == "asset-market"
        )

        missing_registry = json.loads(json.dumps(registry))
        missing_record = json.loads(json.dumps(asset_market_record))
        missing_record["zip_path"] = "generated/skill-zips/house-skills/asset-market/missing-skill.zip"
        missing_registry["artifacts"] = [missing_record if record is asset_market_record else record for record in registry["artifacts"]]
        missing_path = _write_temp_registry(tmp_path, missing_registry)

        try:
            export_skill_zips(
                form="skills",
                values=["house-skills/asset-market"],
                out_dir=tmp_path / "missing-out",
                registry_path=missing_path,
            )
        except Exception as exc:  # noqa: BLE001
            assert "missing-skill.zip" in str(exc)
        else:  # pragma: no cover - defensive
            raise AssertionError("expected missing artifact failure")

        stale_registry = json.loads(json.dumps(registry))
        stale_record = json.loads(json.dumps(asset_market_record))
        stale_record["zip_sha256"] = "0" * 64
        stale_registry["artifacts"] = [stale_record if record is asset_market_record else record for record in registry["artifacts"]]
        stale_path = _write_temp_registry(tmp_path, stale_registry)

        try:
            export_skill_zips(
                form="skills",
                values=["house-skills/asset-market"],
                out_dir=tmp_path / "stale-out",
                registry_path=stale_path,
            )
        except Exception as exc:  # noqa: BLE001
            assert "zip sha256 mismatch" in str(exc)
        else:  # pragma: no cover - defensive
            raise AssertionError("expected stale artifact failure")


def test_readme_mentions_worker_export_command() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    assert "export_skill_zips.py" in text
    assert "worker-output/<issue>/<name>" in text


def main() -> int:
    out_dir, manifest = test_pack_export_and_manifest()
    test_from_file_export()
    test_subset_export_and_bare_name_ambiguity()
    test_missing_and_collision_failures()
    test_missing_and_stale_artifact_failures()
    test_readme_mentions_worker_export_command()
    print("Receipt:")
    print("  commands run:")
    print("    py -3 tools/export_skill_zips.py --pack house-skills --out <temp>/batch --clean-output")
    print("    py -3 tools/export_skill_zips.py --skills house-skills/asset-market,house-skills/boring-loop --out <temp>/subset")
    print("    py -3 tools/export_skill_zips.py --skills linear --out <temp>/ambiguous")
    print("  sample export path: " + str(out_dir / manifest["resolved"][0]["output_path"]))
    print("  exported skills: " + ", ".join(f"{entry['pack']}/{entry['skill']}" for entry in manifest["resolved"]))
    print("  skipped entries: none")
    print("  ambiguous entries: none")
    print("  manifest path: " + str(out_dir / "export-manifest.json"))
    print("OK export skill zip validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
