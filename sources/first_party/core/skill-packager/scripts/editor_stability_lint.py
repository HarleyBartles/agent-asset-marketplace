#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import ast
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml
from safe_skill_tree import is_hidden_path, is_text_file, iter_skill_files, read_bounded_text, skipped_output_paths

ALLOWED_CONTROLS = {9, 10, 13}


def lint(skill_dir):
    skill_dir = Path(skill_dir).resolve()
    errors = []
    warnings = []

    for rel in skipped_output_paths(skill_dir):
        if any(part.startswith('.') for part in Path(rel).parts):
            errors.append(f'{rel}: hidden dotfile/directory is not allowed')
        elif '__pycache__' in Path(rel).parts:
            errors.append(f'{rel}: __pycache__ is not allowed')
        elif Path(rel).suffix.lower() in {'.pyc', '.pyo'}:
            errors.append(f'{rel}: generated Python bytecode is not allowed')
        elif Path(rel).name in {'skill.zip', 'package-evidence.json'} or any(part in {'dist','build','.pytest_cache','.mypy_cache','.ruff_cache','.cache','node_modules'} for part in Path(rel).parts):
            errors.append(f'{rel}: package/build/cache output is not allowed inside a staged skill root')

    try:
        paths = list(iter_skill_files(skill_dir))
    except ValueError as exc:
        errors.append(str(exc))
        return errors, warnings

    for path in paths:
        rel = path.relative_to(skill_dir)
        if is_hidden_path(rel):
            errors.append(f'{rel}: hidden dotfile/directory is not allowed')
            continue
        if path.suffix.lower() in {'.pyc', '.pyo'}:
            errors.append(f'{rel}: generated Python bytecode is not allowed')
            continue
        if not is_text_file(path):
            continue
        raw, text, error = read_bounded_text(path)
        if error:
            errors.append(f'{rel}: {error}')
            continue
        assert raw is not None and text is not None
        if b'\r' in raw:
            errors.append(f'{rel}: use LF line endings only; CR/CRLF found')
        if any(ord(c) > 127 for c in text):
            errors.append(f'{rel}: non-ASCII character found')
        for i, c in enumerate(text):
            if ord(c) < 32 and ord(c) not in ALLOWED_CONTROLS:
                errors.append(f'{rel}: control character U+{ord(c):04X} at offset {i}')
                break
        if path.suffix.lower() in {'.yaml', '.yml'} or path.name == 'openai.yaml':
            try:
                yaml.safe_load(text)
            except Exception as exc:
                errors.append(f'{rel}: YAML parse failed: {exc}')
        if path.suffix.lower() == '.py':
            try:
                ast.parse(text)
            except SyntaxError as exc:
                errors.append(f'{rel}: Python parse failed: {exc}')
        if path.suffix.lower() in {'.svg', '.xml'}:
            try:
                ET.fromstring(text)
            except Exception as exc:
                errors.append(f'{rel}: XML parse failed: {exc}')
    return errors, warnings


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: editor_stability_lint.py <skill-folder>')
        sys.exit(2)
    errs, warns = lint(Path(sys.argv[1]).resolve())
    for w in warns:
        print('WARNING: ' + w)
    for e in errs:
        print('ERROR: ' + e)
    if not errs:
        print('Editor-stability lint passed')
    sys.exit(1 if errs else 0)
