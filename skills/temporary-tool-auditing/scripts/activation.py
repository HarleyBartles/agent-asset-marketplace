"""Session and worktree gate for the stable user-wide Codex dispatcher."""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from store import AuditStoreError, load_manifest, registration_lock

ACTIVATION_ENV = "CODEX_TOOL_AUDIT_ACTIVATION_FILE"


def current_registry_path(environ=None, platform=None):
    """Read the current user setting on Windows instead of inherited process state."""
    platform = sys.platform if platform is None else platform
    environ = os.environ if environ is None else environ
    value = None
    if platform == "win32":
        try:
            import winreg

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                try:
                    value, _ = winreg.QueryValueEx(key, ACTIVATION_ENV)
                except FileNotFoundError:
                    pass
        except (OSError, ImportError):
            return None
        return Path(value).expanduser() if value else None
    if value is None:
        value = environ.get(ACTIVATION_ENV)
    if value is None:
        value = str(Path(environ.get("CODEX_HOME") or (Path.home() / ".codex")) / "tool-auditing" / "activations.json")
    return Path(value).expanduser() if value else None


def _project_matches(cwd, project):
    try:
        Path(cwd).resolve(strict=False).relative_to(Path(project).resolve(strict=False))
        return True
    except (OSError, TypeError, ValueError):
        return False


def _read_registry(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {"version": 1, "entries": []}
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("entries"), list):
        return {"version": 1, "entries": []}
    return data


def _write_registry(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}-", suffix=".tmp", dir=path.parent)
    try:
        if os.name != "nt":
            os.chmod(temporary, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, ensure_ascii=False, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def set_user_activation(path, enable):
    """Flip the current-user switch; dispatch reads it fresh for every event."""
    if sys.platform != "win32":
        return
    try:
        import winreg

        access = winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, access)
        try:
            if enable:
                try:
                    existing, _ = winreg.QueryValueEx(key, ACTIVATION_ENV)
                except FileNotFoundError:
                    existing = None
                if existing not in (None, str(path)):
                    raise AuditStoreError("activation-setting-conflict")
                winreg.SetValueEx(key, ACTIVATION_ENV, 0, winreg.REG_EXPAND_SZ, str(path))
            else:
                try:
                    existing, _ = winreg.QueryValueEx(key, ACTIVATION_ENV)
                except FileNotFoundError:
                    existing = None
                if existing == str(path):
                    winreg.DeleteValue(key, ACTIVATION_ENV)
        finally:
            winreg.CloseKey(key)
    except AuditStoreError:
        raise
    except (OSError, ImportError):
        raise AuditStoreError("activation-setting-failed") from None


def enable(registry, run, session_id, *, manage_switch=True):
    if not isinstance(session_id, str) or not session_id:
        raise AuditStoreError("session-id-required")
    run = Path(run).resolve()
    manifest = load_manifest(run)
    project = manifest.get("project_root")
    if not isinstance(project, str) or manifest.get("runtime") != "codex" or not manifest.get("global_dispatcher"):
        raise AuditStoreError("codex-project-required")
    if manifest.get("capture_session_id") not in (None, session_id):
        raise AuditStoreError("session-id-mismatch")
    entry = {
        "session_id": session_id,
        "project_root": str(Path(project).resolve()),
        "run_dir": str(run),
        "run_id": manifest.get("run_id"),
        "detail": manifest.get("detail", "status"),
        "expires_at": manifest.get("expires_at"),
    }
    registry = Path(registry)
    with registration_lock(registry.parent):
        data = _read_registry(registry)
        existing = next(
            (
                item
                for item in data["entries"]
                if item.get("session_id") == session_id
                and item.get("project_root") == entry["project_root"]
                and item.get("run_id") != entry["run_id"]
            ),
            None,
        )
        if existing is not None:
            raise AuditStoreError("activation-conflict")
        entries = [
            item
            for item in data["entries"]
            if not (item.get("session_id") == session_id and item.get("project_root") == entry["project_root"])
        ]
        entries.append(entry)
        if manage_switch:
            set_user_activation(registry, True)
        _write_registry(registry, {"version": 1, "entries": entries})
    return {"enabled": True, "run_id": entry["run_id"], "session_id": session_id}


def disable(registry, run, *, manage_switch=True):
    run = Path(run).resolve()
    manifest = load_manifest(run)
    with registration_lock(Path(registry).parent):
        data = _read_registry(registry)
        entries = [
            item
            for item in data["entries"]
            if not (item.get("run_id") == manifest.get("run_id") and Path(item.get("run_dir", "")).resolve() == run)
        ]
        _write_registry(registry, {"version": 1, "entries": entries})
        if manage_switch and not entries:
            set_user_activation(registry, False)
    return {"disabled": True, "run_id": manifest.get("run_id")}


def dispatch(registry, payload, now):
    if registry is None:
        return False
    if not isinstance(payload, dict):
        return False
    session_id = payload.get("session_id")
    cwd = payload.get("cwd")
    if not isinstance(session_id, str) or not isinstance(cwd, str):
        return False
    entry = next(
        (
            item
            for item in _read_registry(registry)["entries"]
            if item.get("session_id") == session_id
            and _project_matches(cwd, item.get("project_root"))
            and isinstance(item.get("expires_at"), (int, float))
            and now < item["expires_at"]
        ),
        None,
    )
    if entry is None:
        return False
    run = Path(entry.get("run_dir", ""))
    try:
        manifest = load_manifest(run)
        if manifest.get("run_id") != entry.get("run_id") or manifest.get("project_root") != entry.get("project_root"):
            return False
        if not manifest.get("armed") or manifest.get("registration_state") != "installed":
            return False
        if not isinstance(manifest.get("expires_at"), (int, float)) or now >= manifest["expires_at"]:
            return False
        global_root = Path(registry).resolve().parent
        owner = json.loads((global_root / "owner.json").read_text(encoding="utf-8"))
        recorder = global_root / "record.py"
        expected_hashes = owner.get("file_hashes", {})
        owned_helpers = ("activation.py", "dispatch.py", "record.py", "runtime.py", "store.py", "sanitize.py")
        if owner.get("state") != "installed":
            return False
        for helper_name in owned_helpers:
            expected_hash = expected_hashes.get(helper_name)
            helper_path = global_root / helper_name
            if (
                not isinstance(expected_hash, str)
                or hashlib.sha256(helper_path.read_bytes()).hexdigest() != expected_hash
            ):
                return False
        interpreter = manifest.get("hook_interpreter") or sys.executable
        result = subprocess.run(
            [interpreter, "-B", str(recorder), "--run-dir", str(run)],
            input=json.dumps(payload, ensure_ascii=False),
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        return result.returncode == 0
    except (AuditStoreError, OSError, ValueError, TypeError, subprocess.SubprocessError):
        return False


def main(argv=None):
    parser = argparse.ArgumentParser(description="Global session-scoped tool audit dispatcher. (read-only)")
    parser.add_argument("--check", action="store_true", help="validate the dispatcher command without reading stdin")
    args = parser.parse_args(argv)
    if args.check:
        return 0
    try:
        payload = json.load(sys.stdin)
        dispatch(current_registry_path(), payload, time.time())
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
