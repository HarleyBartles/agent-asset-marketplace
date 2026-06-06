#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import re
import tempfile
import zipfile
from pathlib import Path

import yaml
from editor_stability_lint import lint as editor_lint


def safe_extract(zf: zipfile.ZipFile, target: Path) -> None:
    base = target.resolve()
    for member in zf.infolist():
        dest = (base / member.filename).resolve()
        if not str(dest).startswith(str(base) + '/') and dest != base:
            raise RuntimeError(f'unsafe archive member path: {member.filename}')
    zf.extractall(base)


def inspect(zpath: Path) -> tuple[list[str], str | None]:
    errors: list[str] = []
    root: str | None = None
    if zpath.name != 'skill.zip':
        errors.append('archive filename must be skill.zip')
    try:
        with zipfile.ZipFile(zpath) as zf:
            bad = zf.testzip()
            if bad:
                errors.append(f'zip integrity failure at {bad}')
            names = [n for n in zf.namelist() if n and not n.endswith('/')]
            roots = sorted({n.split('/')[0] for n in names})
            root = roots[0] if len(roots) == 1 else None
            if len(roots) != 1:
                errors.append('archive must contain exactly one top-level folder')
            if root and f'{root}/SKILL.md' not in names:
                errors.append('SKILL.md missing')
            if root and f'{root}/agents/openai.yaml' not in names:
                errors.append('agents/openai.yaml missing')
            if root:
                text = zf.read(f'{root}/SKILL.md').decode('utf-8')
                m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
                data = yaml.safe_load(m.group(1)) if m else {}
                if data.get('name') != root:
                    errors.append('frontmatter name does not match archive folder')
            if not errors and root:
                with tempfile.TemporaryDirectory() as tmp:
                    safe_extract(zf, Path(tmp))
                    errs, _warns = editor_lint(Path(tmp) / root)
                    errors.extend(errs)
    except Exception as exc:
        errors.append(f'archive inspection failed: {exc}')
    return errors, root


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: inspect_skill_zip.py <skill.zip>')
        sys.exit(2)
    zpath = Path(sys.argv[1]).resolve()
    errors, root = inspect(zpath)
    for e in errors:
        print('ERROR: ' + e)
    if errors:
        sys.exit(1)
    print(f'Archive inspection passed: folder={root}, size={zpath.stat().st_size} bytes')
