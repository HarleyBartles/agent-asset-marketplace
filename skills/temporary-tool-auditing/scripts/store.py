"""Locked, sanitising persistence primitives for temporary tool audits."""

import json
import os
import hashlib
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator

from sanitize import sanitize

MAX_EVENT_LOG_BYTES = 25 * 1024 * 1024
MAX_HEALTH_LOG_BYTES = 256 * 1024
MAX_CONTROL_LOG_BYTES = 1024 * 1024
CONTROL_LOG_CLEANUP_RESERVE_BYTES = 64 * 1024
MAX_MANIFEST_BYTES = 2 * 1024 * 1024
MANIFEST_CLEANUP_RESERVE_BYTES = 64 * 1024


class AuditStoreError(Exception):
    """Safe storage failure identified by a non-sensitive error code."""

    def __init__(self, code: str, details: dict | None = None):
        self.code = code
        self.details = details or {}
        super().__init__(code)


@contextmanager
def _locked(run: Path) -> Iterator[None]:
    run.mkdir(parents=True, exist_ok=True, mode=0o700)
    if os.name != "nt":
        os.chmod(run, 0o700)
    lock_path = run / ".audit.lock"
    handle = open(lock_path, "a+b")
    try:
        if os.name == "nt":
            import msvcrt

            if lock_path.stat().st_size == 0:
                handle.write(b"\0")
                handle.flush()
            handle.seek(0)
            deadline = time.monotonic() + 10
            while True:
                try:
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    if time.monotonic() >= deadline:
                        raise AuditStoreError("lock-timeout") from None
                    time.sleep(0.025)
        else:
            import fcntl

            deadline = time.monotonic() + 10
            while True:
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise AuditStoreError("lock-timeout") from None
                    time.sleep(0.025)
        yield
    finally:
        try:
            if os.name == "nt":
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        except (OSError, ImportError):
            pass
        handle.close()


def _safe_json(value: object, code: str, safe_session_paths: set[str] | None = None) -> tuple[bytes, list[str]]:
    try:
        cleaned, redactions = sanitize(value, safe_session_paths=safe_session_paths)
        encoded = json.dumps(cleaned, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8")
        return encoded, redactions
    except Exception:
        raise AuditStoreError(code) from None


def load_manifest(run: Path) -> dict:
    run = Path(run)
    path = run / "manifest.json"
    try:
        if not path.is_file():
            raise AuditStoreError("manifest-read-failed")
        if not (run / ".audit.lock").exists():
            # Atomic replacement makes an unlocked read safe when no writer has
            # created the lock yet, and keeps read-only status checks read-only.
            data = json.loads(path.read_text(encoding="utf-8"))
        else:
            with _locked(run):
                data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError
        return data
    except AuditStoreError:
        raise
    except Exception:
        raise AuditStoreError("manifest-read-failed") from None


def _write_manifest_locked(run: Path, path: Path, value: dict) -> None:
    safe_session_paths = set()
    if isinstance(value, dict) and isinstance(value.get("capture_session_id"), str):
        safe_session_paths.add("$.capture_session_id")
    subject = value.get("subject") if isinstance(value, dict) else None
    if isinstance(subject, dict) and "session_id" in subject:
        safe_session_paths.add("$.subject.session_id")
    controls = value.get("controls") if isinstance(value, dict) else None
    if isinstance(controls, list):
        safe_session_paths.update(
            f"$.controls[{index}].session_id"
            for index, control in enumerate(controls)
            if isinstance(control, dict) and "session_id" in control
        )
    encoded, _ = _safe_json(value, "manifest-encode-failed", safe_session_paths)
    state = value.get("registration_state") if isinstance(value, dict) else None
    if state in {"teardown-verified", "cleaned"}:
        maximum = MAX_MANIFEST_BYTES
    elif state in {"removed", "removing"}:
        maximum = MAX_MANIFEST_BYTES - MANIFEST_CLEANUP_RESERVE_BYTES
    else:
        maximum = MAX_MANIFEST_BYTES - 2 * MANIFEST_CLEANUP_RESERVE_BYTES
    if len(encoded) > maximum:
        raise AuditStoreError("manifest-size-limit-reached")
    descriptor, temporary = tempfile.mkstemp(prefix=".manifest-", suffix=".tmp", dir=run)
    try:
        if os.name != "nt":
            os.chmod(temporary, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save_manifest(run: Path, value: dict) -> None:
    run = Path(run)
    path = run / "manifest.json"
    try:
        with _locked(run):
            _write_manifest_locked(run, path, value)
    except AuditStoreError:
        raise
    except Exception:
        raise AuditStoreError("manifest-write-failed") from None


def create_manifest(run: Path, value: dict) -> None:
    run = Path(run)
    path = run / "manifest.json"
    try:
        existed = run.exists()
        with _locked(run):
            if existed or path.exists():
                raise AuditStoreError("run-directory-exists")
            _write_manifest_locked(run, path, value)
    except AuditStoreError:
        raise
    except Exception:
        raise AuditStoreError("manifest-write-failed") from None


def update_manifest(run: Path, updater: Callable[[dict], Any]) -> tuple[dict, Any]:
    """Atomically apply one lifecycle read-modify-write under the run lock."""
    run = Path(run)
    path = run / "manifest.json"
    try:
        with _locked(run):
            manifest = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(manifest, dict):
                raise AuditStoreError("manifest-read-failed")
            original = json.loads(json.dumps(manifest))
            result = updater(manifest)
            if manifest != original:
                _write_manifest_locked(run, path, manifest)
            return manifest, result
    except AuditStoreError:
        raise
    except Exception:
        raise AuditStoreError("manifest-write-failed") from None


def registration_lock(root: Path):
    """Return a cross-run lock outside the project registration directory."""
    canonical = str(Path(root).resolve()).casefold().encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    lock_root = Path(tempfile.gettempdir()) / "temporary-tool-auditing-locks"
    lock_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name != "nt":
        os.chmod(lock_root, 0o700)
    return _locked(lock_root / digest)


def append_record(run: Path, name: str, value: dict) -> dict:
    result = append_record_if(run, name, value, None)
    if result is None:
        raise AuditStoreError("record-write-failed")
    return result


def append_record_if(
    run: Path,
    name: str,
    value: dict,
    eligible: Callable[[dict, dict], bool] | None,
) -> dict | None:
    if not isinstance(name, str) or name not in {"events", "health", "controls"}:
        raise AuditStoreError("invalid-record-name")
    safe_session_paths = {"$.session_id"} if name in {"events", "controls"} and "session_id" in value else set()
    cleaned, redactions = sanitize(value, safe_session_paths=safe_session_paths)
    if not isinstance(cleaned, dict):
        raise AuditStoreError("record-encode-failed")
    cleaned["redactions"] = sorted(set(cleaned.get("redactions", [])) | set(redactions))
    run = Path(run)
    try:
        with _locked(run):
            if eligible is not None:
                try:
                    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
                except Exception:
                    raise AuditStoreError("manifest-read-failed") from None
                if not eligible(manifest, cleaned):
                    return None
            encoded, _ = _safe_json(cleaned, "record-encode-failed", safe_session_paths)
            path = run / f"{name}.jsonl"
            current_size = path.stat().st_size if path.exists() else 0
            if name == "events":
                maximum = MAX_EVENT_LOG_BYTES
                code = "event-log-limit-reached"
            elif name == "controls":
                cleanup_codes = {"recorder-health-control", "recorder-direct-control"}
                reserve_record = cleaned.get("code") in cleanup_codes
                maximum = (
                    MAX_CONTROL_LOG_BYTES
                    if reserve_record
                    else MAX_CONTROL_LOG_BYTES - CONTROL_LOG_CLEANUP_RESERVE_BYTES
                )
                code = "control-log-limit-reached"
            else:
                maximum = MAX_HEALTH_LOG_BYTES
                code = "health-log-limit-reached" if name == "health" else "auxiliary-log-limit-reached"
            if current_size + len(encoded) + 1 > maximum:
                raise AuditStoreError(code)
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
            try:
                if os.name != "nt":
                    os.fchmod(fd, 0o600)
                os.write(fd, encoded + b"\n")
                os.fsync(fd)
            finally:
                os.close(fd)
    except AuditStoreError:
        raise
    except Exception:
        raise AuditStoreError("record-write-failed") from None
    return cleaned
