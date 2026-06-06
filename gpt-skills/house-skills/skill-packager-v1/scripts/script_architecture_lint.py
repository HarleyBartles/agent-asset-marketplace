#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import ast
from pathlib import Path

from safe_skill_tree import is_text_file, iter_skill_files, read_bounded_text

SCRIPT_SUFFIXES = {'.py', '.sh'}
RECIPE_FILES = {'SKILL.md', '.md', '.yaml', '.yml', '.json'}


def _doc_text(skill_dir: Path) -> str:
    chunks = []
    for path in iter_skill_files(skill_dir):
        rel = path.relative_to(skill_dir)
        if 'scripts' in rel.parts:
            continue
        if path.name == 'SKILL.md' or path.suffix.lower() in {'.md', '.yaml', '.yml', '.json'}:
            _raw, text, error = read_bounded_text(path)
            if not error and text:
                chunks.append(text)
    return '\n'.join(chunks)


def _script_files(skill_dir: Path) -> list[Path]:
    scripts = skill_dir / 'scripts'
    if not scripts.exists():
        return []
    return [p for p in iter_skill_files(scripts) if p.is_file() and p.suffix.lower() in SCRIPT_SUFFIXES]


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _call_name(node.value)
        return f'{base}.{node.attr}' if base else node.attr
    return ''


def _has_keyword(call: ast.Call, name: str) -> bool:
    return any(kw.arg == name for kw in call.keywords)


def lint(skill_dir):
    skill_dir = Path(skill_dir).resolve()
    errors = []
    warnings = []
    scripts = _script_files(skill_dir)
    if not scripts:
        return errors, warnings

    docs = _doc_text(skill_dir)
    if not docs.strip():
        errors.append('scripts present but no non-script documentation was available for normal-use recipes')

    for script in scripts:
        rel = script.relative_to(skill_dir)
        rel_text = str(rel).replace('\\', '/')
        if script.name not in docs and rel_text not in docs:
            errors.append(f'{rel_text}: script is not named from SKILL.md or references; normal-use/discovery recipe is missing')

        if script.suffix.lower() == '.py':
            _raw, text, error = read_bounded_text(script)
            if error:
                errors.append(f'{rel_text}: {error}')
                continue
            assert text is not None
            if 'dont_write_bytecode' not in text:
                errors.append(f'{rel_text}: Python script should set sys.dont_write_bytecode = True to avoid __pycache__ output')
            try:
                tree = ast.parse(text)
            except SyntaxError as exc:
                errors.append(f'{rel_text}: Python parse failed: {exc}')
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    name = _call_name(node.func)
                    if name in {'subprocess.run', 'subprocess.call', 'subprocess.check_call', 'subprocess.check_output'}:
                        if not _has_keyword(node, 'timeout'):
                            errors.append(f'{rel_text}: {name} call without explicit timeout')
                    if name == 'subprocess.Popen':
                        warnings.append(f'{rel_text}: subprocess.Popen requires explicit process-tree cleanup and timeout documentation')
                    if name.endswith('.rglob') or name in {'glob.glob'}:
                        if script.name != 'safe_skill_tree.py':
                            errors.append(f'{rel_text}: recursive walk should use safe_skill_tree bounded helpers instead of {name}')
                    if name.endswith('.read_text') or name.endswith('.read_bytes'):
                        if script.name != 'safe_skill_tree.py':
                            warnings.append(f'{rel_text}: whole-file read should be bounded or limited to known small control files')
            if len(scripts) > 1 and 'scripts/' not in docs:
                warnings.append('multiple scripts exist; documentation should map script lane ownership and normal execution recipes')

    return sorted(set(errors)), sorted(set(warnings))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: script_architecture_lint.py <skill-folder>')
        sys.exit(2)
    errs, warns = lint(Path(sys.argv[1]).resolve())
    for w in warns:
        print('WARNING: ' + w)
    for e in errs:
        print('ERROR: ' + e)
    if not errs:
        print('Script architecture lint passed')
    sys.exit(1 if errs else 0)
