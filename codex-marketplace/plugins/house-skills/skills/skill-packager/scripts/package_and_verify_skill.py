#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import hashlib
import json
import signal
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from editor_stability_lint import lint as editor_lint
from frontmatter_lint import lint as frontmatter_lint
from inspect_skill_zip import inspect as inspect_skill_zip
from quick_validate import validate_skill
from safe_skill_tree import iter_skill_files, skipped_output_paths
from script_architecture_lint import lint as script_architecture_lint

DEFAULT_TIMEOUT_SECONDS = 25
DEFAULT_WRAPPER_BUDGET_SECONDS = 120


class StepTimeout(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write_receipt(path: Path, receipt: dict) -> None:
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def timeout_handler(_signum, _frame):
    raise StepTimeout('step timed out')


def run_timed_callable(func, timeout: int):
    previous = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        return func()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def result_ok(name: str, elapsed: float, stdout: str = '') -> dict:
    return {
        'step': name,
        'ok': True,
        'returncode': 0,
        'elapsed_seconds': round(elapsed, 3),
        'stdout_tail': stdout[-4000:],
        'stderr_tail': '',
        'timed_out': False,
    }


def result_fail(name: str, elapsed: float, stdout: str = '', stderr: str = '', timed_out: bool = False, timeout: int | None = None) -> dict:
    result = {
        'step': name,
        'ok': False,
        'returncode': None if timed_out else 1,
        'elapsed_seconds': round(elapsed, 3),
        'stdout_tail': stdout[-4000:],
        'stderr_tail': stderr[-4000:],
        'timed_out': timed_out,
    }
    if timed_out and timeout is not None:
        result['timeout_seconds'] = timeout
    return result


def run_step(name: str, func, timeout: int, receipt: dict, receipt_path: Path, wrapper_started: float, wrapper_budget: int) -> dict:
    now_elapsed = time.monotonic() - wrapper_started
    if now_elapsed >= wrapper_budget:
        result = result_fail(name, now_elapsed, stderr='wrapper budget exceeded before step started', timed_out=True, timeout=wrapper_budget)
        result['wrapper_budget_exceeded'] = True
        return result

    receipt['current_step'] = name
    receipt['current_step_started_at_utc'] = utc_now()
    receipt['current_step_timeout_seconds'] = timeout
    write_receipt(receipt_path, receipt)

    started = time.monotonic()
    try:
        value = run_timed_callable(func, timeout)
        elapsed = time.monotonic() - started
        if isinstance(value, tuple):
            ok = bool(value[0])
            stdout = str(value[1]) if len(value) > 1 else ''
            stderr = str(value[2]) if len(value) > 2 else ''
        else:
            ok = bool(value)
            stdout = ''
            stderr = ''
        if ok:
            result = result_ok(name, elapsed, stdout)
        else:
            result = result_fail(name, elapsed, stdout, stderr)
    except StepTimeout:
        elapsed = time.monotonic() - started
        result = result_fail(name, elapsed, stderr=f'{name} timed out after {timeout} seconds', timed_out=True, timeout=timeout)
    except Exception as exc:
        elapsed = time.monotonic() - started
        result = result_fail(name, elapsed, stderr=f'{type(exc).__name__}: {exc}')

    receipt['steps'].append(result)
    receipt['current_step'] = None
    receipt['current_step_started_at_utc'] = None
    receipt['current_step_timeout_seconds'] = None
    write_receipt(receipt_path, receipt)
    return result


def step_frontmatter(skill_dir: Path):
    errors, warnings = frontmatter_lint(skill_dir)
    out = '\n'.join(['WARNING: ' + w for w in warnings] + ['ERROR: ' + e for e in errors])
    if not errors:
        out = (out + '\n' if out else '') + 'Frontmatter lint passed'
    return not errors, out, ''


def step_editor_stability(skill_dir: Path):
    errors, warnings = editor_lint(skill_dir)
    out = '\n'.join(['WARNING: ' + w for w in warnings] + ['ERROR: ' + e for e in errors])
    if not errors:
        out = (out + '\n' if out else '') + 'Editor-stability lint passed'
    return not errors, out, ''


def step_quick_validate(skill_dir: Path):
    ok, msg = validate_skill(skill_dir)
    return ok, msg, ''


def step_script_architecture(skill_dir: Path):
    errors, warnings = script_architecture_lint(skill_dir)
    out = '\n'.join(['WARNING: ' + w for w in warnings] + ['ERROR: ' + e for e in errors])
    if not errors:
        out = (out + '\n' if out else '') + 'Script architecture lint passed'
    return not errors, out, ''


def inspect_archive_shape(zip_path: Path):
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
        parts = text.split('---', 2)
        if len(parts) < 3:
            raise RuntimeError('SKILL.md frontmatter missing')
        fm_name = None
        for line in parts[1].splitlines():
            if line.startswith('name:'):
                fm_name = line.split(':', 1)[1].strip().strip('"\'')
                break
        return root, fm_name == root


def step_package(skill_dir: Path, package_path: Path, evidence_path: Path):
    forbidden = skipped_output_paths(skill_dir)
    if forbidden:
        return False, '', 'ERROR forbidden: ' + ', '.join(forbidden)
    if package_path.exists():
        package_path.unlink()
    try:
        files = sorted(iter_skill_files(skill_dir), key=lambda p: str(p.relative_to(skill_dir)))
    except ValueError as exc:
        return False, '', f'ERROR: {exc}'
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for fp in files:
            zipf.write(fp, fp.relative_to(skill_dir.parent))
    root, match = inspect_archive_shape(package_path)
    size = package_path.stat().st_size
    evidence = {
        'evidence_schema': 'skill-packager.package-evidence.v3',
        'target_skill': root,
        'staged_source_path': str(skill_dir),
        'package_path': str(package_path),
        'package_size_bytes': size,
        'package_sha256': sha256_file(package_path),
        'frontmatter_lint': 'pass',
        'editor_stability_lint': 'pass',
        'quick_validate': 'pass',
        'script_architecture_lint': 'pass',
        'unzip_test': 'pass',
        'archive_inspection': 'pass',
        'exact_file_exists': package_path.is_file(),
        'exact_file_nonzero': size > 0,
        'top_level_folder_matches_skill': match,
        'created_at_utc': utc_now(),
        'packager_wrapper': 'integrated-single-process',
        'next_required_step': 'skill-buster',
    }
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return True, f'OK: Successfully packaged skill to: {package_path}', ''


def step_zip_integrity(package_path: Path):
    with zipfile.ZipFile(package_path) as zf:
        bad = zf.testzip()
    if bad:
        return False, '', f'zip integrity failure at {bad}'
    return True, 'Zip integrity test passed', ''


def step_inspect_skill_zip(package_path: Path):
    errors, root = inspect_skill_zip(package_path)
    if errors:
        return False, '', '\n'.join(errors)
    return True, f'Archive inspection passed: folder={root}, size={package_path.stat().st_size} bytes', ''


def main(argv: list[str]) -> int:
    if len(argv) not in {3, 4, 5}:
        print('Usage: package_and_verify_skill.py <skill-folder> <external-dist-dir> [timeout-seconds] [wrapper-budget-seconds]')
        return 2
    skill_dir = Path(argv[1]).resolve()
    dist_dir = Path(argv[2]).resolve()
    timeout = int(argv[3]) if len(argv) >= 4 else DEFAULT_TIMEOUT_SECONDS
    wrapper_budget = int(argv[4]) if len(argv) == 5 else DEFAULT_WRAPPER_BUDGET_SECONDS
    dist_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = dist_dir / 'package-run-receipt.json'
    package_path = dist_dir / 'skill.zip'
    evidence_path = dist_dir / 'package-evidence.json'

    for stale in (package_path, evidence_path, receipt_path):
        if stale.exists():
            stale.unlink()

    receipt = {
        'receipt_schema': 'skill-packager.package-run-receipt.v2',
        'skill_dir': str(skill_dir),
        'dist_dir': str(dist_dir),
        'created_at_utc': utc_now(),
        'timeout_seconds_per_step': timeout,
        'wrapper_budget_seconds': wrapper_budget,
        'wrapper_mode': 'integrated-single-process',
        'steps': [],
        'current_step': None,
        'current_step_started_at_utc': None,
        'current_step_timeout_seconds': None,
        'ok': False,
    }
    write_receipt(receipt_path, receipt)
    wrapper_started = time.monotonic()

    steps = [
        ('frontmatter_lint', lambda: step_frontmatter(skill_dir)),
        ('editor_stability_lint', lambda: step_editor_stability(skill_dir)),
        ('quick_validate', lambda: step_quick_validate(skill_dir)),
        ('script_architecture_lint', lambda: step_script_architecture(skill_dir)),
        ('package_skill', lambda: step_package(skill_dir, package_path, evidence_path)),
        ('zip_integrity_test', lambda: step_zip_integrity(package_path)),
        ('inspect_skill_zip', lambda: step_inspect_skill_zip(package_path)),
    ]

    for name, func in steps:
        result = run_step(name, func, timeout, receipt, receipt_path, wrapper_started, wrapper_budget)
        print(f"{name}: {'pass' if result['ok'] else 'fail'} ({result['elapsed_seconds']}s)")
        if result.get('timed_out'):
            print(f"ERROR: {name} timed out after {result.get('timeout_seconds')} seconds")
            return 1
        if not result['ok']:
            if result.get('stdout_tail'):
                print(result['stdout_tail'])
            if result.get('stderr_tail'):
                print(result['stderr_tail'])
            return 1

    if not package_path.is_file() or package_path.stat().st_size <= 0:
        print('ERROR: expected skill.zip is missing or empty')
        return 1
    if not evidence_path.is_file():
        print('ERROR: package-evidence.json missing')
        return 1
    evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
    actual_sha = sha256_file(package_path)
    evidence_sha = evidence.get('package_sha256')
    if evidence.get('package_path') != str(package_path):
        print('ERROR: evidence package_path does not match exact archive path')
        return 1
    if evidence_sha != actual_sha:
        print('ERROR: evidence package_sha256 does not match exact archive sha')
        return 1
    with zipfile.ZipFile(package_path) as zf:
        names = [n for n in zf.namelist() if n and not n.endswith('/')]
        roots = sorted({n.split('/')[0] for n in names})
    receipt.update({
        'ok': True,
        'package_path': str(package_path),
        'package_size_bytes': package_path.stat().st_size,
        'package_sha256': actual_sha,
        'top_level_folders': roots,
        'package_evidence_path': str(evidence_path),
        'total_elapsed_seconds': round(time.monotonic() - wrapper_started, 3),
        'next_required_step': 'skill-buster',
    })
    write_receipt(receipt_path, receipt)
    print(f'OK: package verified at {package_path}')
    print(f'OK: receipt written to {receipt_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
