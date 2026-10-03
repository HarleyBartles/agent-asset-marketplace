"""Temporarily trust one exact Codex project path while an audit is active."""

import json
import hashlib
import os
import re
import stat
import tempfile
import tomllib
import uuid
from pathlib import Path
from typing import Callable, Optional, Tuple

from store import AuditStoreError, registration_lock


def _config_path(explicit: Optional[Path] = None) -> Path:
    if explicit is not None:
        return Path(explicit).expanduser().resolve()
    codex_home = os.environ.get("CODEX_HOME")
    base = Path(codex_home).expanduser() if codex_home else Path.home() / ".codex"
    return (base / "config.toml").resolve()


def _snapshot(path: Path) -> Optional[Tuple[bytes, tuple]]:
    try:
        before = path.stat()
        raw = path.read_bytes()
        after = path.stat()
    except FileNotFoundError:
        return None
    except Exception:
        raise AuditStoreError("codex-config-invalid") from None
    before_identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    after_identity = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    if before_identity != after_identity:
        raise AuditStoreError("codex-config-changed")
    return raw, after_identity


def _read(path: Path) -> tuple[str, dict, Optional[Tuple[bytes, tuple]]]:
    snapshot = _snapshot(path)
    try:
        text = snapshot[0].decode("utf-8") if snapshot else ""
        data = tomllib.loads(text)
    except Exception:
        raise AuditStoreError("codex-config-invalid") from None
    projects = data.get("projects", {})
    if not isinstance(projects, dict):
        raise AuditStoreError("codex-config-invalid")
    return text, projects, snapshot


def _path_key(projects: dict, project: Path) -> str | None:
    wanted = os.path.normcase(os.path.normpath(str(project)))
    for key in projects:
        if isinstance(key, str) and os.path.normcase(os.path.normpath(key)) == wanted:
            return key
    return None


def _level(projects: dict, key: str | None) -> str | None:
    if key is None:
        return None
    section = projects[key]
    if not isinstance(section, dict):
        raise AuditStoreError("codex-config-invalid")
    level = section.get("trust_level")
    if level not in {None, "trusted", "untrusted"}:
        raise AuditStoreError("codex-config-invalid")
    return level


def _section_bounds(text: str, project_key: str) -> tuple[int, int] | None:
    lines = text.splitlines(keepends=True)
    start = None
    for index, line in enumerate(lines):
        header = line.strip()
        if not header.startswith("[") or header.startswith("[["):
            continue
        try:
            parsed = tomllib.loads(header)
        except tomllib.TOMLDecodeError:
            continue
        projects = parsed.get("projects")
        if isinstance(projects, dict) and set(projects) == {project_key} and projects[project_key] == {}:
            start = index
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        header = lines[index].strip()
        if header.startswith("[") and not header.startswith("#"):
            end = index
            break
    return start, end


def _assert_unchanged(path: Path, expected: Optional[Tuple[bytes, tuple]]) -> None:
    if _snapshot(path) != expected:
        raise AuditStoreError("codex-config-changed")


def _atomic_write(
    path: Path,
    text: str,
    expected: Optional[Tuple[bytes, tuple]],
    temporary_path: Optional[Path] = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    old_mode = None
    try:
        old_mode = stat.S_IMODE(path.stat().st_mode)
    except FileNotFoundError:
        pass
    if temporary_path is None:
        descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}-", suffix=".tmp", dir=path.parent)
    else:
        temporary = os.fspath(temporary_path)
        try:
            descriptor = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            raise AuditStoreError("codex-config-recovery-pending", {"recovery_file": temporary}) from None
    keep_temporary = False
    try:
        if old_mode is not None:
            os.chmod(temporary, old_mode)
            if os.name == "nt":
                _copy_windows_dacl(path, Path(temporary))
        elif os.name != "nt":
            os.chmod(temporary, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        _assert_unchanged(path, expected)
        if old_mode is None:
            os.replace(temporary, path)
        elif os.name == "nt":
            try:
                _replace_windows_file(path, Path(temporary))
            except AuditStoreError as error:
                if error.code != "codex-replace-incomplete":
                    raise
                if not path.exists() and Path(temporary).exists() and error.details.get("winerror") == 1177:
                    displaced = _find_file_by_identity(path.parent, expected[1], Path(temporary)) if expected else []
                    if len(displaced) == 1:
                        try:
                            os.replace(displaced[0], path)
                        except OSError:
                            keep_temporary = True
                            raise AuditStoreError(
                                "codex-config-recovery-failed",
                                {
                                    "recovery_file": str(displaced[0]),
                                    "replacement_file": temporary,
                                    "restore_to": str(path),
                                },
                            ) from None
                        raise AuditStoreError("codex-config-recovered") from None
                    keep_temporary = True
                    raise AuditStoreError(
                        "codex-config-recovery-failed",
                        {
                            "recovery_file": temporary,
                            "recovery_files": [str(candidate) for candidate in displaced],
                            "restore_to": str(path),
                        },
                    ) from None
                if not path.exists() and Path(temporary).exists():
                    try:
                        os.replace(temporary, path)
                    except OSError:
                        keep_temporary = True
                        raise AuditStoreError(
                            "codex-config-recovery-failed",
                            {"recovery_file": temporary, "restore_to": str(path)},
                        ) from None
                    raise AuditStoreError("codex-config-recovered") from None
                if path.exists() and Path(temporary).exists():
                    raise
                keep_temporary = Path(temporary).exists()
                raise AuditStoreError(
                    "codex-config-recovery-failed",
                    {"recovery_file": temporary, "restore_to": str(path)},
                ) from None
        else:
            _copy_extended_attributes(path, Path(temporary))
            os.replace(temporary, path)
    finally:
        if os.path.exists(temporary) and not keep_temporary:
            os.unlink(temporary)


def _find_file_by_identity(directory: Path, identity: tuple, replacement: Path) -> list[Path]:
    if len(identity) < 3 or not identity[1]:
        return []
    matches = []
    wanted = identity[:3]
    try:
        entries = list(directory.iterdir())
    except OSError:
        return matches
    for candidate in entries:
        if candidate == replacement or candidate.is_symlink():
            continue
        try:
            info = candidate.stat()
        except OSError:
            continue
        if stat.S_ISREG(info.st_mode) and (info.st_dev, info.st_ino, info.st_size) == wanted:
            matches.append(candidate)
    return matches


def _restore_displaced_config(config: Path, ownership: dict) -> None:
    identity = ownership.get("config_identity")
    if config.exists() or not identity:
        return
    if len(identity) != 3 or not identity[1]:
        raise AuditStoreError("codex-config-recovery-ambiguous", {"restore_to": str(config)})
    displaced = _find_file_by_identity(config.parent, tuple(identity), Path())
    if not displaced:
        if ownership.get("config_created"):
            return
        raise AuditStoreError("codex-config-recovery-missing", {"restore_to": str(config)})
    if len(displaced) != 1:
        raise AuditStoreError(
            "codex-config-recovery-ambiguous",
            {"recovery_files": [str(item) for item in displaced], "restore_to": str(config)},
        )
    try:
        os.replace(displaced[0], config)
    except OSError:
        raise AuditStoreError(
            "codex-config-recovery-failed",
            {"recovery_files": [str(item) for item in displaced], "restore_to": str(config)},
        ) from None


def _staging_path(config: Path, run_id: str) -> Path:
    if not isinstance(run_id, str) or not run_id:
        raise AuditStoreError("trust-ownership-invalid") from None
    run_key = hashlib.sha256(run_id.encode("utf-8")).hexdigest()[:32]
    return config.parent / f".{config.name}-audit-{run_key}.tmp"


def recover_pending_trust_write(ownership: dict, persist_intent: Optional[Callable[[dict], None]] = None) -> None:
    pending = ownership.get("pending_config_write")
    if not pending:
        config = Path(ownership["config_path"])
        _restore_displaced_config(config, ownership)
        committed = _snapshot(config)
        if committed and not ownership.get("config_identity"):
            ownership["config_identity"] = list(committed[1][:3])
            if persist_intent:
                persist_intent(ownership)
        return
    config = Path(ownership["config_path"])
    stage = _staging_path(config, ownership.get("run_id"))
    if os.path.normcase(os.path.abspath(pending)) != os.path.normcase(os.path.abspath(stage)):
        raise AuditStoreError("trust-ownership-invalid")
    if config.exists():
        stage.unlink(missing_ok=True)
    elif stage.exists():
        identity = ownership.get("config_identity")
        if identity:
            if len(identity) != 3 or not identity[1]:
                raise AuditStoreError(
                    "codex-config-recovery-ambiguous",
                    {"recovery_file": str(stage), "restore_to": str(config)},
                )
            displaced = _find_file_by_identity(config.parent, tuple(identity), stage)
            if displaced:
                if len(displaced) != 1:
                    raise AuditStoreError(
                        "codex-config-recovery-ambiguous",
                        {
                            "recovery_file": str(stage),
                            "recovery_files": [str(item) for item in displaced],
                            "restore_to": str(config),
                        },
                    )
                os.replace(displaced[0], config)
                stage.unlink(missing_ok=True)
            else:
                expected_digest = ownership.get("pending_config_write_sha256")
                try:
                    actual_digest = hashlib.sha256(stage.read_bytes()).hexdigest()
                except OSError:
                    actual_digest = None
                if not expected_digest or actual_digest != expected_digest:
                    raise AuditStoreError(
                        "codex-config-recovery-invalid",
                        {"recovery_file": str(stage), "restore_to": str(config)},
                    )
                os.replace(stage, config)
        else:
            expected_digest = ownership.get("pending_config_write_sha256")
            try:
                actual_digest = hashlib.sha256(stage.read_bytes()).hexdigest()
            except OSError:
                actual_digest = None
            if not expected_digest or actual_digest != expected_digest:
                raise AuditStoreError(
                    "codex-config-recovery-invalid",
                    {"recovery_file": str(stage), "restore_to": str(config)},
                )
            os.replace(stage, config)
    else:
        _restore_displaced_config(config, ownership)
    ownership.pop("pending_config_write", None)
    ownership.pop("pending_config_write_sha256", None)
    committed = _snapshot(config)
    ownership["config_identity"] = list(committed[1][:3]) if committed else None
    if persist_intent:
        persist_intent(ownership)


def _replace_windows_file(original: Path, replacement: Path) -> None:
    # ReplaceFileW merges the replaced file's ACLs and attributes onto the new file.
    import ctypes

    replace_file = ctypes.WinDLL("kernel32", use_last_error=True).ReplaceFileW
    replace_file.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_uint32,
        ctypes.c_void_p,
        ctypes.c_void_p,
    ]
    replace_file.restype = ctypes.c_int
    if not replace_file(str(original), str(replacement), None, 0, None, None):
        error = ctypes.get_last_error()
        if error in {1176, 1177}:
            raise AuditStoreError("codex-replace-incomplete", {"winerror": error})
        raise OSError(error, "config-replace-failed")


def _copy_windows_dacl(original: Path, replacement: Path) -> None:
    import ctypes

    advapi = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    get_security = advapi.GetNamedSecurityInfoW
    get_security.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_int,
        ctypes.c_uint32,
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_void_p),
    ]
    get_security.restype = ctypes.c_uint32
    set_security = advapi.SetNamedSecurityInfoW
    set_security.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_int,
        ctypes.c_uint32,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
    ]
    set_security.restype = ctypes.c_uint32
    owner, group, dacl, sacl, descriptor = (ctypes.c_void_p() for _ in range(5))
    result = get_security(
        str(original),
        1,
        0x00000004,
        ctypes.byref(owner),
        ctypes.byref(group),
        ctypes.byref(dacl),
        ctypes.byref(sacl),
        ctypes.byref(descriptor),
    )
    if result:
        raise AuditStoreError("codex-config-acl-read-failed")
    try:
        get_control = advapi.GetSecurityDescriptorControl
        get_control.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort), ctypes.POINTER(ctypes.c_uint32)]
        get_control.restype = ctypes.c_int
        control, revision = ctypes.c_ushort(), ctypes.c_uint32()
        if not get_control(descriptor, ctypes.byref(control), ctypes.byref(revision)):
            raise AuditStoreError("codex-config-acl-read-failed")
        inheritance_flag = 0x80000000 if control.value & 0x1000 else 0x20000000
        result = set_security(str(replacement), 1, 0x00000004 | inheritance_flag, None, None, dacl, None)
        if result:
            raise AuditStoreError("codex-config-acl-write-failed")
    finally:
        kernel.LocalFree.argtypes = [ctypes.c_void_p]
        kernel.LocalFree.restype = ctypes.c_void_p
        kernel.LocalFree(descriptor)


def _copy_extended_attributes(original: Path, replacement: Path) -> None:
    if not hasattr(os, "listxattr"):
        return
    import errno

    try:
        names = os.listxattr(original, follow_symlinks=False)
    except OSError as error:
        if error.errno in {errno.ENOTSUP, errno.EOPNOTSUPP, errno.ENOSYS}:
            return
        raise
    for name in names:
        value = os.getxattr(original, name, follow_symlinks=False)
        os.setxattr(replacement, name, value, follow_symlinks=False)


def _append_table(text: str, project_key: str) -> str:
    prefix = text
    if prefix and not prefix.endswith(("\n", "\r")):
        prefix += "\n"
    if prefix and not prefix.endswith("\n\n"):
        prefix += "\n"
    section = f'[projects.{json.dumps(project_key, ensure_ascii=False)}]\ntrust_level = "trusted"\n'
    return prefix + section


def _commit_owned_write(
    config: Path,
    updated: str,
    expected: Optional[Tuple[bytes, tuple]],
    ownership: dict,
    persist_intent: Optional[Callable[[dict], None]],
) -> None:
    stage = _staging_path(config, ownership["run_id"])
    ownership["pending_config_write"] = str(stage)
    ownership["pending_config_write_sha256"] = hashlib.sha256(updated.encode("utf-8")).hexdigest()
    if persist_intent:
        persist_intent(ownership)
    _atomic_write(config, updated, expected, temporary_path=stage)
    ownership.pop("pending_config_write", None)
    ownership.pop("pending_config_write_sha256", None)
    committed = _snapshot(config)
    ownership["config_identity"] = list(committed[1][:3]) if committed else None
    if persist_intent:
        persist_intent(ownership)


def project_trust_level(project: Path, config_path: Optional[Path] = None) -> Optional[str]:
    project = Path(project).resolve()
    config = _config_path(config_path)
    with registration_lock(config.parent / config.name):
        _, projects, _ = _read(config)
        key = _path_key(projects, project)
        return _level(projects, key)


def preview_project_trust(project: Path, config_path: Optional[Path] = None) -> dict:
    project = Path(project).resolve()
    config = _config_path(config_path)
    level = project_trust_level(project, config)
    if level == "trusted":
        action = "already-trusted"
    elif level == "untrusted":
        action = "blocked-untrusted"
    else:
        action = "add-exact-project-path"
    return {"config_path": str(config), "project_path": str(project), "current_trust": level, "action": action}


def add_project_trust(
    project: Path,
    config_path: Optional[Path] = None,
    persist_intent: Optional[Callable[[dict], None]] = None,
    run_id: Optional[str] = None,
) -> dict:
    config = _config_path(config_path)
    run_id = run_id or str(uuid.uuid4())
    with registration_lock(config.parent / config.name):
        return _add_project_trust(project, config, persist_intent, run_id)


def _add_project_trust(
    project: Path,
    config: Path,
    persist_intent: Optional[Callable[[dict], None]] = None,
    run_id: Optional[str] = None,
) -> dict:
    project = Path(project).resolve()
    text, projects, expected = _read(config)
    key = _path_key(projects, project)
    config_created = not config.exists()
    if key is not None:
        section = projects[key]
        if not isinstance(section, dict):
            raise AuditStoreError("codex-config-invalid")
        prior = _level(projects, key)
        if prior == "untrusted":
            raise AuditStoreError("trust-conflict")
        if prior == "trusted":
            ownership = {
                "state": "preexisting",
                "config_path": str(config),
                "project_path": str(project),
                "config_created": False,
                "section_created": False,
            }
            if persist_intent:
                persist_intent(ownership)
            return ownership
        bounds = _section_bounds(text, key)
        if bounds is None:
            raise AuditStoreError("trust-config-shape-conflict")
        lines = text.splitlines(keepends=True)
        start, end = bounds
        if end and not lines[end - 1].endswith(("\n", "\r")):
            lines[end - 1] += "\n"
        lines.insert(end, 'trust_level = "trusted"\n')
        updated = "".join(lines)
    else:
        if any(re.match(r"^\s*projects\s*=", line) for line in text.splitlines()):
            raise AuditStoreError("trust-config-shape-conflict")
        key = str(project)
        updated = _append_table(text, key)
    ownership = {
        "state": "added",
        "config_path": str(config),
        "project_path": str(project),
        "config_created": config_created,
        "section_created": key == str(project) and key not in projects,
        "config_identity": list(expected[1][:3]) if expected else None,
        "run_id": run_id or str(uuid.uuid4()),
    }
    if persist_intent:
        persist_intent(ownership)
    _commit_owned_write(config, updated, expected, ownership, persist_intent)
    return ownership


def remove_project_trust(
    ownership: dict,
    persist_intent: Optional[Callable[[dict], None]] = None,
) -> dict:
    if ownership.get("state") == "preexisting":
        return {"state": "preserved"}
    if ownership.get("state") != "added":
        raise AuditStoreError("trust-ownership-invalid")
    config = Path(ownership["config_path"])
    with registration_lock(config.parent / config.name):
        return _remove_project_trust(ownership, persist_intent)


def _remove_project_trust(ownership: dict, persist_intent: Optional[Callable[[dict], None]] = None) -> dict:
    config = Path(ownership["config_path"])
    project = Path(ownership["project_path"])
    recover_pending_trust_write(ownership, persist_intent)
    text, projects, expected = _read(config)
    key = _path_key(projects, project)
    if key is None:
        if ownership.get("config_created") and config.exists() and not text.strip():
            _assert_unchanged(config, expected)
            config.unlink(missing_ok=True)
            return {"state": "removed"}
        return {"state": "already-removed"}
    section = projects[key]
    if not isinstance(section, dict):
        raise AuditStoreError("codex-config-invalid")
    current = section.get("trust_level")
    if current is None:
        if ownership.get("section_created") and not section:
            bounds = _section_bounds(text, key)
            if bounds is not None:
                lines = text.splitlines(keepends=True)
                del lines[bounds[0]]
                updated = "".join(lines)
                if ownership.get("config_created") and not updated.strip():
                    config.unlink(missing_ok=True)
                else:
                    _commit_owned_write(config, updated, expected, ownership, persist_intent)
                return {"state": "removed"}
        return {"state": "already-removed"}
    if current != "trusted":
        return {"state": "conflict"}
    bounds = _section_bounds(text, key)
    if bounds is None:
        raise AuditStoreError("trust-config-shape-conflict")
    lines = text.splitlines(keepends=True)
    start, end = bounds
    trust_index = next(
        (index for index in range(start + 1, end) if lines[index].split("=", 1)[0].strip() == "trust_level"),
        None,
    )
    if trust_index is None:
        raise AuditStoreError("trust-config-shape-conflict")
    del lines[trust_index]
    if not section.keys() - {"trust_level"}:
        # Remove only the section header. Comments and unrelated file content survive.
        del lines[start]
    updated = "".join(lines)
    if ownership.get("config_created") and not updated.strip():
        _assert_unchanged(config, expected)
        config.unlink(missing_ok=True)
    else:
        _commit_owned_write(config, updated, expected, ownership, persist_intent)
    return {"state": "removed"}


def project_trust_absent(ownership: Optional[dict]) -> bool:
    if not ownership or ownership.get("state") == "preexisting":
        return True
    if ownership.get("state") != "added":
        return False
    config = Path(ownership["config_path"])
    if ownership.get("pending_config_write"):
        return False
    if not config.exists() and ownership.get("config_identity") and not ownership.get("config_created"):
        return False
    text, projects, _ = _read(config)
    key = _path_key(projects, Path(ownership["project_path"]))
    return key is None or _level(projects, key) is None
