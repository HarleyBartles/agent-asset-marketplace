#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from editor_stability_lint import lint as editor_lint
from quick_validate import validate_skill
from safe_skill_tree import iter_skill_files, skipped_output_paths, write_canonical_skill_zip


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def find_forbidden(skill_path):
    return skipped_output_paths(Path(skill_path))


def inspect_archive_shape(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f'zip integrity failure at {bad}')
        names = [n for n in zf.namelist() if n and not n.endswith('/')]
        roots = sorted({n.split('/')[0] for n in names})
        if len(roots) != 1:
            raise RuntimeError('archive must contain exactly one top-level folder')
        root = roots[0]
        if f'{root}/SKILL.md' not in names:
            raise RuntimeError('SKILL.md not found at archive root')
        text = zf.read(f'{root}/SKILL.md').decode('utf-8')
        fm = text.split('---', 2)[1]
        fm_name = None
        for line in fm.splitlines():
            if line.startswith('name:'):
                fm_name = line.split(':', 1)[1].strip().strip('"\'')
                break
        return root, fm_name == root


def package_skill(skill_path, output_dir):
    skill_path = Path(skill_path).resolve()
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    forbidden = find_forbidden(skill_path)
    if forbidden:
        print('ERROR forbidden: ' + ', '.join(forbidden))
        return None
    ok, msg = validate_skill(skill_path)
    print(msg)
    if not ok:
        return None
    errs, warns = editor_lint(skill_path)
    for w in warns:
        print('WARNING: ' + w)
    if errs:
        for e in errs:
            print('ERROR: ' + e)
        return None
    zpath = output_path / 'skill.zip'
    if zpath.exists():
        zpath.unlink()
    try:
        files = sorted(iter_skill_files(skill_path), key=lambda p: str(p.relative_to(skill_path)))
    except ValueError as exc:
        print(f'ERROR: {exc}')
        return None
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        write_canonical_skill_zip(zipf, files, root=skill_path.parent)
    root, match = inspect_archive_shape(zpath)
    size = zpath.stat().st_size
    evidence = {
        'evidence_schema': 'skill-packager.package-evidence.v2',
        'target_skill': root,
        'staged_source_path': str(skill_path),
        'package_path': str(zpath),
        'package_size_bytes': size,
        'package_sha256': sha256_file(zpath),
        'frontmatter_lint': 'pass',
        'editor_stability_lint': 'pass',
        'quick_validate': 'pass',
        'unzip_test': 'pass',
        'archive_inspection': 'pass',
        'exact_file_exists': zpath.is_file(),
        'exact_file_nonzero': size > 0,
        'top_level_folder_matches_skill': match,
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'next_required_step': 'skill-handoff',
    }
    (output_path / 'package-evidence.json').write_text(json.dumps(evidence, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(f'OK: Successfully packaged skill to: {zpath}')
    return zpath


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: package_skill.py <skill-folder> <external-dist-dir>')
        sys.exit(2)
    res = package_skill(sys.argv[1], sys.argv[2])
    sys.exit(0 if res else 1)
