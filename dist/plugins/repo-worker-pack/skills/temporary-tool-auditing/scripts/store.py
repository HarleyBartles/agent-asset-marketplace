"""Locked, sanitising persistence primitives for temporary tool audits."""

import json
import os
import re
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from sanitize import sanitize


class AuditStoreError(Exception):
    """Safe storage failure identified by a non-sensitive error code."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@contextmanager
def _locked(run: Path) -> Iterator[None]:
    run.mkdir(parents=True, exist_ok=True)
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


def _safe_json(value: object, code: str) -> tuple[bytes, list[str]]:
    try:
        cleaned, redactions = sanitize(value)
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


def save_manifest(run: Path, value: dict) -> None:
    run = Path(run)
    path = run / "manifest.json"
    encoded, _ = _safe_json(value, "manifest-encode-failed")
    try:
        with _locked(run):
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
    except AuditStoreError:
        raise
    except Exception:
        raise AuditStoreError("manifest-write-failed") from None


def append_record(run: Path, name: str, value: dict) -> dict:
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", name):
        raise AuditStoreError("invalid-record-name")
    cleaned, redactions = sanitize(value)
    if not isinstance(cleaned, dict):
        raise AuditStoreError("record-encode-failed")
    cleaned["redactions"] = sorted(set(cleaned.get("redactions", [])) | set(redactions))
    encoded, _ = _safe_json(cleaned, "record-encode-failed")
    run = Path(run)
    try:
        with _locked(run):
            path = run / f"{name}.jsonl"
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
