"""Install one stable, inert-by-default Codex user hook dispatcher."""

import json
import hashlib
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from store import AuditStoreError, registration_lock

EVENTS = ("PreToolUse", "PostToolUse", "SubagentStart", "SubagentStop", "SessionStart", "SessionEnd")
HELPERS = ("activation.py", "record.py", "runtime.py", "store.py", "sanitize.py")


def _read(path):
    if not path.exists():
        return {"hooks": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise AuditStoreError("global-hook-config-invalid") from None
    if not isinstance(data, dict) or not isinstance(data.get("hooks", {}), dict):
        raise AuditStoreError("global-hook-config-invalid")
    data.setdefault("hooks", {})
    return data


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}-", suffix=".tmp", dir=path.parent)
    try:
        if os.name != "nt":
            os.chmod(temporary, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _owned_entry(event, dispatcher, interpreter):
    args = [str(interpreter), "-B", str(dispatcher)]
    command = shlex.join(args)
    windows = subprocess.list2cmdline(args)
    handler = {"type": "command", "command": command, "commandWindows": windows}
    if event == "SessionEnd":
        handler["timeout"] = 3
    return {"matcher": "", "hooks": [handler]}


def install_global(codex_home, source_dir, interpreter=None, *, refresh_helpers=False):
    """Idempotently register global hooks, preserving all unrelated entries."""
    home = Path(codex_home).resolve()
    source = Path(source_dir).resolve()
    root = home / "tool-auditing"
    config = home / "hooks.json"
    dispatcher = root / "dispatch.py"
    interpreter = Path(interpreter or sys.executable).resolve()
    proposed = {event: _owned_entry(event, dispatcher, interpreter) for event in EVENTS}
    with registration_lock(home):
        owner_path = root / "owner.json"
        if owner_path.exists():
            try:
                owner = json.loads(owner_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                raise AuditStoreError("global-install-conflict") from None
            if not _owned_files_match(root, owner):
                raise AuditStoreError("global-install-conflict")
            data = _read(config)
            if owner.get("state") == "installed":
                if owner.get("interpreter") != str(interpreter):
                    raise AuditStoreError("global-install-conflict")
                if not all(
                    item["entry"] in data["hooks"].get(item["event"], []) for item in owner.get("owned_entries", [])
                ):
                    raise AuditStoreError("global-hook-config-changed")
                proposed_hashes = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in HELPERS}
                proposed_hashes["dispatch.py"] = proposed_hashes["activation.py"]
                changed = proposed_hashes != owner.get("file_hashes")
                if changed and not refresh_helpers:
                    raise AuditStoreError("global-helper-refresh-requires-review")
                if changed:
                    for name in HELPERS:
                        shutil.copyfile(source / name, root / name)
                    shutil.copyfile(source / "activation.py", dispatcher)
                    owner["file_hashes"] = {
                        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in root.iterdir()
                        if path.is_file() and path.name != "owner.json"
                    }
                    _write(owner_path, owner)
                return {
                    "installed": True,
                    "already_installed": not changed,
                    "updated_helpers": changed,
                    "dispatcher": str(dispatcher),
                    "hooks": list(EVENTS),
                }
            if owner.get("state") != "prepared":
                raise AuditStoreError("global-install-conflict")
            for item in owner.get("owned_entries", []):
                entries = data["hooks"].setdefault(item["event"], [])
                if item["entry"] not in entries:
                    entries.append(item["entry"])
            _write(config, data)
            owner["state"] = "installed"
            _write(owner_path, owner)
            return {"installed": True, "recovered": True, "dispatcher": str(dispatcher), "hooks": list(EVENTS)}
        if root.exists():
            raise AuditStoreError("global-install-unowned-files")
        data = _read(config)
        config_before = config.read_bytes() if config.exists() else None
        root.mkdir(parents=True, exist_ok=False)
        for name in HELPERS:
            shutil.copyfile(source / name, root / name)
        shutil.copyfile(source / "activation.py", dispatcher)
        hooks = data["hooks"]
        owned = []
        for event, entry in proposed.items():
            entries = hooks.setdefault(event, [])
            if entry not in entries:
                entries.append(entry)
            owned.append({"event": event, "entry": entry})
        file_hashes = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.iterdir()
            if path.is_file() and path.name != "owner.json"
        }
        owner = {
            "version": 1,
            "config": str(config),
            "dispatcher": str(dispatcher),
            "interpreter": str(interpreter),
            "owned_entries": owned,
            "file_hashes": file_hashes,
            "state": "prepared",
            "activation_registry": str(root / "activations.json"),
        }
        _write(root / "owner.json", owner)
        current_config = config.read_bytes() if config.exists() else None
        if current_config != config_before:
            raise AuditStoreError("global-hook-config-changed")
        _write(config, data)
        owner["state"] = "installed"
        _write(root / "owner.json", owner)
    return {"installed": True, "dispatcher": str(dispatcher), "hooks": list(EVENTS)}


def global_install_present(codex_home):
    home = Path(codex_home).resolve()
    root = home / "tool-auditing"
    config = home / "hooks.json"
    if not (root / "owner.json").is_file():
        return False
    try:
        owner = json.loads((root / "owner.json").read_text(encoding="utf-8"))
        hooks = _read(config)["hooks"]
    except (OSError, ValueError, AuditStoreError):
        return False
    if owner.get("state") != "installed":
        return False
    if not all(item["entry"] in hooks.get(item["event"], []) for item in owner.get("owned_entries", [])):
        return False
    return _owned_files_match(root, owner)


def _owned_files_match(root, owner):
    expected_names = {*HELPERS, "dispatch.py"}
    hashes = owner.get("file_hashes")
    if not isinstance(hashes, dict) or set(hashes) != expected_names:
        return False
    for name, expected in hashes.items():
        try:
            if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
                return False
        except OSError:
            return False
    return True
