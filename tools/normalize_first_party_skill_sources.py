#!/usr/bin/env python3
"""Normalize active first-party skill sources to the canonical repo format."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml

from marketplace_utils import ROOT

SOURCE_ROOT = ROOT / "sources/first_party/skills"

# Proper-noun overrides for skill display names so brand casing is preserved
# when generating provenance-name and agents/openai.yaml display_name.
_SKILL_NAME_OVERRIDES: dict[str, str] = {
    "github": "GitHub",
    "ux": "UX",
}


def _skill_display_name(skill_name: str) -> str:
    """Convert a kebab-case skill name to a title-case display name."""
    parts = skill_name.replace("-", " ").split()
    return " ".join(
        _SKILL_NAME_OVERRIDES.get(part.lower(), part.title()) for part in parts
    )


def _read_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("\ufeff"):
        raw = raw.lstrip("\ufeff")
    lines = raw.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path.relative_to(ROOT)} must start with YAML frontmatter")

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            end_index = index
            break
    if end_index is None:
        raise ValueError(f"{path.relative_to(ROOT)} is missing a closing YAML frontmatter delimiter")

    frontmatter_text = "\n".join(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :])
    if raw.endswith("\n"):
        body += "\n"

    try:
        frontmatter = _safe_load_yaml(frontmatter_text)
        if isinstance(frontmatter, dict):
            return frontmatter, body
    except Exception:
        pass

    return _parse_frontmatter_fallback(frontmatter_text, path), body


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def _sanitize_plain_scalar_lines(text: str) -> str:
    sanitized: list[str] = []
    for line in text.splitlines():
        stripped = line.lstrip(" ")
        if not stripped or stripped.startswith("#") or stripped.startswith("- "):
            sanitized.append(line)
            continue
        if ":" not in line:
            sanitized.append(line)
            continue
        prefix, value = line.split(":", 1)
        if value == "":
            sanitized.append(line)
            continue
        value_text = value.lstrip(" ")
        if not value_text or value_text[0] in "\"'[{|>":
            sanitized.append(line)
            continue
        if re.fullmatch(r"(?:true|false|null|~|-?\d+(?:\.\d+)?)", value_text, flags=re.IGNORECASE):
            sanitized.append(line)
            continue
        if ":" in value_text or "#" in value_text or "\t" in value_text:
            sanitized.append(f"{prefix}: {json.dumps(value_text)}")
            continue
        sanitized.append(line)
    return "\n".join(sanitized)


def _safe_load_yaml(text: str) -> Any:
    try:
        return yaml.safe_load(text)
    except Exception:
        return yaml.safe_load(_sanitize_plain_scalar_lines(text))


def _parse_block_text(lines: list[str]) -> str:
    if not lines:
        return ""
    indents = [len(line) - len(line.lstrip(" ")) for line in lines if line.strip()]
    strip_indent = min(indents) if indents else 0
    return "\n".join(line[strip_indent:] if len(line) >= strip_indent else line for line in lines)


def _parse_frontmatter_fallback(frontmatter_text: str, path: Path) -> dict[str, Any]:
    lines = frontmatter_text.splitlines()
    result: dict[str, Any] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith(" "):
            raise ValueError(f"{path.relative_to(ROOT)} frontmatter contains unexpected indentation")
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if match is None:
            raise ValueError(f"{path.relative_to(ROOT)} frontmatter line is not a simple key/value pair: {line!r}")
        key = match.group(1)
        value = match.group(2) or ""
        if value.strip():
            result[key] = _parse_scalar(value)
            index += 1
            continue

        block: list[str] = []
        index += 1
        while index < len(lines):
            candidate = lines[index]
            if not candidate.strip():
                block.append("")
                index += 1
                continue
            if candidate.startswith("  ") or candidate.startswith("\t"):
                block.append(candidate[2:] if candidate.startswith("  ") else candidate.lstrip("\t"))
                index += 1
                continue
            break

        block_text = _parse_block_text(block)
        if key == "metadata":
            metadata = _safe_load_yaml(block_text) if block_text.strip() else {}
            if metadata is None:
                metadata = {}
            if not isinstance(metadata, dict):
                raise ValueError(f"{path.relative_to(ROOT)} metadata block must be a mapping")
            result[key] = metadata
            continue

        result[key] = _safe_load_yaml(block_text) if block_text.strip() else ""

    if not isinstance(result, dict):
        raise ValueError(f"{path.relative_to(ROOT)} frontmatter must be a mapping")
    return result


def _write_frontmatter(path: Path, frontmatter: dict[str, Any], body: str) -> None:
    rendered = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).rstrip() + "\n"
    path.write_text(f"---\n{rendered}---\n{body}", encoding="utf-8", newline="\n")


def _ensure_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        items = value
    else:
        items = [value]
    result: list[str] = []
    for item in items:
        text = str(item).strip()
        if text:
            result.append(text)
    return result


_USE_WHEN_PREFIXES = ("use when ", "use for ")
_USE_BEFORE_PREFIXES = ("use before ",)
_USE_AFTER_PREFIXES = ("use after ",)
_USE_WITH_PREFIXES = ("use with ",)
_USE_INSTEAD_PREFIXES = ("use instead ",)
# Exclude bare "do not use " — it would strip the start of "Do not use to switch..."
# and cause the normalizer to prepend "when", producing "Do not use when to switch...".
_DO_NOT_USE_WHEN_PREFIXES = ("do not use when ", "don't use when ", "avoid when ")


def _strip_prefix(text: str, prefixes: tuple[str, ...]) -> str:
    lower = text.lower()
    for prefix in prefixes:
        if lower.startswith(prefix):
            return text[len(prefix):].lstrip()
    return text


def _capitalize_first(text: str) -> str:
    if not text:
        return text
    return text[0].upper() + text[1:]


def _normalize_use_when(description: str) -> str:
    text = description.strip()
    if not text:
        return text
    for prefixes, label in (
        (_USE_WHEN_PREFIXES, "Use when"),
        (_USE_BEFORE_PREFIXES, "Use before"),
        (_USE_AFTER_PREFIXES, "Use after"),
        (_USE_WITH_PREFIXES, "Use with"),
        (_USE_INSTEAD_PREFIXES, "Use instead"),
    ):
        bare = _strip_prefix(text, prefixes)
        if bare != text:
            return f"{label} {bare}"
    return "Use when " + text[0].lower() + text[1:]


def _normalize_condition(value: str, *, prefix: str) -> str:
    text = value.strip()
    if not text:
        return text
    if prefix == "do not use when":
        bare = _strip_prefix(text, _DO_NOT_USE_WHEN_PREFIXES)
        if not bare or bare == text:
            return text
        return f"{_capitalize_first(prefix)} {bare}"
    bare = _strip_prefix(text, (prefix,))
    if not bare or bare == text:
        return text
    return f"{_capitalize_first(prefix)} {bare}"


def _normalize_skill(skill_md: Path, *, write: bool) -> bool:
    frontmatter, body = _read_frontmatter(skill_md)

    name = str(frontmatter.get("name") or skill_md.parent.name).strip()
    if not name:
        raise ValueError(f"{skill_md.relative_to(ROOT)} frontmatter name is blank")

    description = str(frontmatter.get("description") or "").strip()
    if not description:
        raise ValueError(f"{skill_md.relative_to(ROOT)} is missing a description")
    normalized_description = _normalize_use_when(description)

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}

    scope = metadata.get("scope")
    if not isinstance(scope, str) or not scope.strip():
        scope = normalized_description

    use_when = _ensure_list(metadata.get("use_when"))
    if not use_when:
        use_when = [normalized_description]
    else:
        use_when = [_normalize_use_when(entry) for entry in use_when]

    do_not_use_when = _ensure_list(metadata.get("do_not_use_when"))
    if not do_not_use_when:
        do_not_use_when = ["Do not use when another more specific skill owns this task."]
    else:
        do_not_use_when = [_normalize_condition(entry, prefix="do not use when") for entry in do_not_use_when]

    normalized_metadata: dict[str, Any] = {
        "source-id": name,
        "source-path": skill_md.relative_to(ROOT).as_posix(),
        "provenance-name": f"{_skill_display_name(name)} first-party skill",
        "source-category": "first_party",
        "status": "active",
        "owner": str(metadata.get("owner") or "Harley Bartles").strip(),
        "scope": scope,
        "use_when": use_when,
        "do_not_use_when": do_not_use_when,
    }

    for key in ("related_skills", "notes", "use_before", "use_after", "use_with", "use_instead"):
        if key in metadata and metadata.get(key) is not None:
            normalized_metadata[key] = metadata[key]

    normalized_frontmatter: dict[str, Any] = {
        "name": name,
        "description": normalized_description,
        "metadata": normalized_metadata,
        "license": frontmatter.get("license", "MIT"),
    }

    changed = normalized_frontmatter != frontmatter
    if write and changed:
        _write_frontmatter(skill_md, normalized_frontmatter, body)
    return changed


def _normalize_openai_yaml(path: Path, *, skill_name: str, description: str, write: bool) -> bool:
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("\ufeff"):
        raw = raw.lstrip("\ufeff")
    data = _safe_load_yaml(raw)
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a mapping")

    interface = data.get("interface")
    if not isinstance(interface, dict):
        interface = {}
    policy = data.get("policy")
    if not isinstance(policy, dict):
        policy = {}

    title = _skill_display_name(skill_name)
    normalized = dict(data)
    normalized["interface"] = {
        "display_name": interface.get("display_name") or title,
        "short_description": interface.get("short_description") or description,
        "default_prompt": interface.get("default_prompt")
        or f"Use /{skill_name} when {description.lower().removeprefix('use when ')}",
    }
    normalized["policy"] = dict(policy)
    normalized["policy"]["allow_implicit_invocation"] = policy.get("allow_implicit_invocation", True)

    changed = normalized != data
    if write and changed:
        rendered = yaml.safe_dump(normalized, sort_keys=False, allow_unicode=True).rstrip() + "\n"
        path.write_text(rendered, encoding="utf-8", newline="\n")
    return changed


def run(*, write: bool) -> int:
    changed_files: list[str] = []
    for skill_dir in sorted((path for path in SOURCE_ROOT.iterdir() if path.is_dir()), key=lambda path: path.name):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        frontmatter, _ = _read_frontmatter(skill_md)
        description = str(frontmatter.get("description") or "")
        changed = _normalize_skill(skill_md, write=write)
        if changed:
            changed_files.append(skill_md.relative_to(ROOT).as_posix())

        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if openai_yaml.is_file():
            openai_changed = _normalize_openai_yaml(
                openai_yaml,
                skill_name=str(frontmatter.get("name") or skill_dir.name),
                description=str(frontmatter.get("description") or description),
                write=write,
            )
            if openai_changed:
                changed_files.append(openai_yaml.relative_to(ROOT).as_posix())

    if write:
        for file_path in changed_files:
            print(f"WROTE {file_path}")
        print(f"OK first-party skill sources: {len(changed_files)} file(s) normalized")
    else:
        if changed_files:
            raise ValueError(
                "first-party skill sources are stale; run py -3 tools/normalize_first_party_skill_sources.py"
            )
        print("OK first-party skill sources: current")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize active first-party skill sources")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args()
    return run(write=not args.check)


if __name__ == "__main__":
    raise SystemExit(main())
