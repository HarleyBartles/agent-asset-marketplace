#!/usr/bin/env python3
"""Export canonical skill.zip artifacts into a GPT-upload-ready output tree."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from marketplace_utils import load_json
from skill_zip_artifacts import (
    GENERATED_SKILL_ZIPS_REGISTRY_PATH,
    GENERATED_SKILL_ZIPS_ROOT,
    ROOT,
    SkillArtifact,
    SkillTarget,
    discover_skill_targets,
    record_to_artifact,
    sha256_file,
    validate_package_matches_source,
    validate_skill_zip_registry,
)


@dataclass(frozen=True)
class RequestToken:
    form: str
    raw: str
    pack: str | None
    skill: str | None


@dataclass(frozen=True)
class ResolvedExport:
    request: RequestToken
    target: SkillTarget
    artifact: SkillArtifact

    @property
    def output_path(self) -> Path:
        return Path(self.artifact.skill) / "skill.zip"


def _split_tokens(raw_values: list[str]) -> list[str]:
    tokens: list[str] = []
    for raw_value in raw_values:
        for chunk in raw_value.replace("\n", ",").split(","):
            token = chunk.strip()
            if token:
                tokens.append(token)
    return tokens


def _load_file_tokens(path: Path) -> list[str]:
    tokens: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.split("#", 1)[0].strip()
        if not stripped:
            continue
        tokens.extend(_split_tokens([stripped]))
    return tokens


def _build_target_indexes() -> tuple[dict[tuple[str, str], SkillTarget], dict[str, list[SkillTarget]]]:
    by_key: dict[tuple[str, str], SkillTarget] = {}
    by_skill: dict[str, list[SkillTarget]] = {}
    for target in discover_skill_targets():
        key = (target.pack, target.skill)
        by_key[key] = target
        by_skill.setdefault(target.skill, []).append(target)
    for entries in by_skill.values():
        entries.sort(key=lambda item: (item.pack, item.skill))
    return by_key, by_skill


def _build_artifact_indexes(registry: dict[str, Any]) -> tuple[dict[tuple[str, str], SkillArtifact], dict[str, list[SkillArtifact]]]:
    by_key: dict[tuple[str, str], SkillArtifact] = {}
    by_skill: dict[str, list[SkillArtifact]] = {}
    for record in registry.get("artifacts", []):
        artifact = record_to_artifact(record)
        key = (artifact.pack, artifact.skill)
        if key in by_key:
            raise ValueError(f"duplicate registry entry for {artifact.pack}/{artifact.skill}")
        by_key[key] = artifact
        by_skill.setdefault(artifact.skill, []).append(artifact)
    for entries in by_skill.values():
        entries.sort(key=lambda item: (item.pack, item.skill))
    return by_key, by_skill


def _build_exclusion_indexes(registry: dict[str, Any]) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    by_key: dict[tuple[str, str], dict[str, Any]] = {}
    by_skill: dict[str, list[dict[str, Any]]] = {}
    for record in registry.get("excluded", []):
        if not isinstance(record, dict):
            raise ValueError("registry contains a malformed exclusion entry")
        pack = str(record.get("pack"))
        skill = str(record.get("skill"))
        key = (pack, skill)
        if key in by_key:
            raise ValueError(f"duplicate registry exclusion entry for {pack}/{skill}")
        by_key[key] = record
        by_skill.setdefault(skill, []).append(record)
    for entries in by_skill.values():
        entries.sort(key=lambda item: (str(item.get("pack")), str(item.get("skill"))))
    return by_key, by_skill


def _resolve_token(
    token: RequestToken,
    *,
    targets_by_key: dict[tuple[str, str], SkillTarget],
    targets_by_skill: dict[str, list[SkillTarget]],
    artifacts_by_key: dict[tuple[str, str], SkillArtifact],
    artifacts_by_skill: dict[str, list[SkillArtifact]],
    exclusions_by_key: dict[tuple[str, str], dict[str, Any]],
    exclusions_by_skill: dict[str, list[dict[str, Any]]],
) -> ResolvedExport:
    if token.pack and token.skill:
        key = (token.pack, token.skill)
        target = targets_by_key.get(key)
        artifact = artifacts_by_key.get(key)
        if target is None or artifact is None:
            exclusion = exclusions_by_key.get(key)
            if exclusion is not None:
                raise ValueError(
                    f"requested skill {token.pack}/{token.skill} is excluded from GPT exports: "
                    f"{exclusion.get('reason')}"
                )
            raise ValueError(f"requested skill missing from the registry: {token.pack}/{token.skill}")
        return ResolvedExport(request=token, target=target, artifact=artifact)

    if not token.skill:
        raise ValueError("internal request token is missing a skill name")

    target_matches = targets_by_skill.get(token.skill, [])
    artifact_matches = artifacts_by_skill.get(token.skill, [])
    exclusion_matches = exclusions_by_skill.get(token.skill, [])
    if not target_matches or not artifact_matches:
        if exclusion_matches:
            if len(exclusion_matches) > 1:
                matches = ", ".join(f"{entry.get('pack')}/{entry.get('skill')}" for entry in exclusion_matches)
                raise ValueError(
                    f"ambiguous excluded skill name {token.skill}; use <pack>/{token.skill} ({matches})"
                )
            exclusion = exclusion_matches[0]
            raise ValueError(
                f"requested skill {token.skill} is excluded from GPT exports: {exclusion.get('reason')}"
            )
        raise ValueError(f"requested skill missing from the registry: {token.skill}")
    if len(target_matches) > 1:
        matches = ", ".join(f"{target.pack}/{target.skill}" for target in target_matches)
        raise ValueError(f"ambiguous skill name {token.skill}; use <pack>/{token.skill} ({matches})")
    return ResolvedExport(request=token, target=target_matches[0], artifact=artifact_matches[0])


def _make_request_tokens(
    *,
    form: str,
    values: list[str],
) -> list[RequestToken]:
    if form == "pack":
        if len(values) != 1:
            raise ValueError("pack export requires exactly one pack name")
        return [RequestToken(form=form, raw=values[0], pack=values[0], skill=None)]

    request_tokens: list[RequestToken] = []
    for raw in values:
        if "/" in raw:
            pack, skill = raw.split("/", 1)
            if not pack or not skill:
                raise ValueError(f"invalid requested skill token: {raw}")
            request_tokens.append(RequestToken(form=form, raw=raw, pack=pack, skill=skill))
        else:
            request_tokens.append(RequestToken(form=form, raw=raw, pack=None, skill=raw))
    return request_tokens


def _ensure_clean_output(out_dir: Path, clean_output: bool) -> None:
    if out_dir == ROOT:
        raise ValueError("refusing to export directly into the repository root")
    if out_dir.exists():
        if clean_output:
            shutil.rmtree(out_dir)
        elif any(out_dir.iterdir()):
            raise ValueError(f"output directory is not clean: {out_dir}")


def _manifest_request_section(
    *,
    form: str,
    values: list[str],
    from_file: Path | None,
    out_dir: Path,
    clean_output: bool,
) -> dict[str, Any]:
    request: dict[str, Any] = {
        "form": form,
        "out": out_dir.relative_to(ROOT).as_posix() if out_dir.is_absolute() and out_dir.is_relative_to(ROOT) else str(out_dir),
        "clean_output": clean_output,
    }
    if form == "pack":
        request["value"] = values[0]
    elif form == "skills":
        request["value"] = values
    elif form == "from-file":
        request["value"] = values
        request["source_file"] = from_file.relative_to(ROOT).as_posix() if from_file and from_file.is_absolute() and from_file.is_relative_to(ROOT) else (str(from_file) if from_file else None)
    return request


def export_skill_zips(
    *,
    form: str,
    values: list[str],
    out_dir: Path,
    clean_output: bool = False,
    from_file: Path | None = None,
    registry_path: Path = GENERATED_SKILL_ZIPS_REGISTRY_PATH,
    generated_root: Path = GENERATED_SKILL_ZIPS_ROOT,
) -> dict[str, Any]:
    if form not in {"pack", "skills", "from-file"}:
        raise ValueError(f"unsupported request form: {form}")

    out_dir = out_dir.resolve()
    from_file = from_file.resolve() if from_file is not None else None
    requested_values = list(values)

    if form == "from-file" and from_file is None:
        raise ValueError("from-file export requires a file path")
    if form == "from-file" and not requested_values:
        requested_values = _load_file_tokens(from_file)

    _ensure_clean_output(out_dir, clean_output)

    registry = load_json(registry_path)
    targets_by_key, targets_by_skill = _build_target_indexes()
    artifacts_by_key, artifacts_by_skill = _build_artifact_indexes(registry)
    exclusions_by_key, exclusions_by_skill = _build_exclusion_indexes(registry)

    if form == "pack":
        pack = values[0]
        request_tokens = [RequestToken(form=form, raw=pack, pack=pack, skill=None)]
        selected_targets = [target for target in discover_skill_targets() if target.pack == pack]
        if not selected_targets:
            raise ValueError(f"no installable skills found for pack {pack}")
        selected = []
        for target in selected_targets:
            key = (target.pack, target.skill)
            artifact = artifacts_by_key.get(key)
            if artifact is None:
                exclusion = exclusions_by_key.get(key)
                if exclusion is not None:
                    raise ValueError(
                        f"requested skill {target.pack}/{target.skill} is excluded from GPT exports: "
                        f"{exclusion.get('reason')}"
                    )
                raise ValueError(f"requested skill missing from the registry: {target.pack}/{target.skill}")
            selected.append(ResolvedExport(request=request_tokens[0], target=target, artifact=artifact))
    else:
        request_tokens = _make_request_tokens(form=form, values=requested_values)
        selected = [
            _resolve_token(
                token,
                targets_by_key=targets_by_key,
                targets_by_skill=targets_by_skill,
                artifacts_by_key=artifacts_by_key,
                artifacts_by_skill=artifacts_by_skill,
                exclusions_by_key=exclusions_by_key,
                exclusions_by_skill=exclusions_by_skill,
            )
            for token in request_tokens
        ]

    output_names: dict[str, ResolvedExport] = {}
    for resolved in selected:
        output_name = resolved.artifact.skill
        if output_name in output_names:
            other = output_names[output_name]
            raise ValueError(
                f"duplicate output folder {output_name} requested by {other.artifact.pack}/{other.artifact.skill} "
                f"and {resolved.artifact.pack}/{resolved.artifact.skill}"
            )
        output_names[output_name] = resolved

    resolved_entries: list[dict[str, Any]] = []
    copied_entries: list[dict[str, Any]] = []
    for resolved in selected:
        validate_package_matches_source(resolved.target, resolved.artifact)

        source_zip = ROOT / resolved.artifact.zip_path
        output_zip = out_dir / resolved.output_path
        output_zip.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_zip, output_zip)

        copied_sha256 = sha256_file(output_zip)
        entry = {
            "pack": resolved.artifact.pack,
            "skill": resolved.artifact.skill,
            "source_path": resolved.artifact.source_path,
            "canonical_zip_path": resolved.artifact.zip_path,
            "zip_sha256": resolved.artifact.zip_sha256,
            "output_path": output_zip.relative_to(out_dir).as_posix(),
            "output_zip_sha256": copied_sha256,
            "request": {
                "form": resolved.request.form,
                "raw": resolved.request.raw,
                "pack": resolved.request.pack,
                "skill": resolved.request.skill,
            },
        }
        resolved_entries.append(entry)
        copied_entries.append(entry)

    manifest = {
        "schema_version": "skill-zip-export.v1",
        "request": _manifest_request_section(
            form=form,
            values=requested_values,
            from_file=from_file,
            out_dir=out_dir,
            clean_output=clean_output,
        ),
        "registry_path": registry_path.relative_to(ROOT).as_posix() if registry_path.is_absolute() and registry_path.is_relative_to(ROOT) else str(registry_path),
        "generated_root": generated_root.relative_to(ROOT).as_posix() if generated_root.is_absolute() and generated_root.is_relative_to(ROOT) else str(generated_root),
        "resolved": resolved_entries,
        "copied": copied_entries,
        "skipped": [],
        "missing": [],
        "stale": [],
        "ambiguous": [],
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "export-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export canonical skill.zip artifacts for manual GPT upload")
    parser.add_argument("--check", action="store_true", help="validate the canonical registry without exporting")
    parser.add_argument("--clean-output", action="store_true", help="remove the output directory before exporting")
    parser.add_argument("--out", help="output directory for GPT upload batches")
    parser.add_argument("--pack", help="export every skill in a pack")
    parser.add_argument("--skills", help="export a comma-separated list of skills or <pack>/<skill> entries")
    parser.add_argument("--from-file", dest="from_file", help="read requested skills from a newline-delimited file")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    selected_forms = sum(1 for value in (args.pack, args.skills, args.from_file) if value is not None)
    if args.check:
        if selected_forms:
            raise SystemExit("--check cannot be combined with export request flags")
        validate_skill_zip_registry()
        print("OK skill zip registry is current")
        return 0

    if selected_forms != 1:
        raise SystemExit("choose exactly one of --pack, --skills, or --from-file")
    if not args.out:
        raise SystemExit("--out is required for export operations")

    if args.pack is not None:
        form = "pack"
        values = [args.pack]
        from_file = None
    elif args.skills is not None:
        form = "skills"
        values = _split_tokens([args.skills])
        from_file = None
    else:
        form = "from-file"
        values = []
        from_file = Path(args.from_file)

    manifest = export_skill_zips(
        form=form,
        values=values,
        out_dir=Path(args.out),
        clean_output=args.clean_output,
        from_file=from_file,
    )

    exported = ", ".join(f"{entry['pack']}/{entry['skill']}" for entry in manifest["resolved"])
    print(f"OK exported {len(manifest['resolved'])} skill zip(s)")
    print(f"OK exported skills: {exported}")
    print(f"OK export manifest: {Path(args.out) / 'export-manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
