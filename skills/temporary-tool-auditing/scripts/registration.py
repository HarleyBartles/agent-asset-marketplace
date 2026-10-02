"""Install and remove only the project-local hook entries owned by one run."""

import json
import os
import shutil
import tempfile
import time
from pathlib import Path

from runtime import render_handlers
from store import AuditStoreError, _locked, load_manifest, save_manifest


def _read(path: Path) -> dict:
    if not path.exists():
        return {"hooks": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("hooks", {}), dict):
            data.setdefault("hooks", {})
            return data
        if isinstance(data, dict) and "hooks" not in data:
            data["hooks"] = {}
            return data
    except Exception:
        pass
    raise AuditStoreError("hook-config-invalid")


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}-", suffix=".tmp", dir=path.parent)
    try:
        if os.name != "nt":
            os.chmod(temporary, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _paths(project: Path, run: Path, runtime: str) -> tuple[Path, Path, Path]:
    root = project / (".codex" if runtime == "codex" else ".devin")
    config = root / ("hooks.json" if runtime == "codex" else "hooks.v1.json")
    owner = root / ".temporary-tool-auditing-owner.json"
    return root, config, owner


def install(run: Path, project: Path, runtime: str) -> dict:
    run, project = Path(run).resolve(), Path(project).resolve()
    if runtime not in {"codex", "devin"}:
        raise AuditStoreError("unsupported-runtime")
    root, config_path, owner_path = _paths(project, run, runtime)
    manifest = load_manifest(run)
    if manifest.get("runtime") != runtime:
        raise AuditStoreError("runtime-mismatch")
    # Keep the portable recorder dependencies beside the run so it remains usable
    # after the installed skill or source checkout changes.
    scripts = run / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    source_scripts = Path(__file__).resolve().parent
    for name in ("record.py", "runtime.py", "store.py", "sanitize.py"):
        shutil.copyfile(source_scripts / name, scripts / name)
    rendered = render_handlers(runtime, scripts / "record.py")
    owned = []
    with _locked(root):
        data = _read(config_path)
        if owner_path.exists():
            try:
                owner = json.loads(owner_path.read_text(encoding="utf-8"))
            except Exception:
                raise AuditStoreError("registration-owner-invalid") from None
            if owner.get("run_id") != manifest.get("run_id"):
                raise AuditStoreError("registration-conflict")
        else:
            owner = {"run_id": manifest.get("run_id"), "run_dir": str(run)}
        hooks = data["hooks"]
        for event, entries in rendered.items():
            if runtime == "codex":
                current = hooks.setdefault(event, [])
                for entry in entries:
                    if entry not in current:
                        current.append(entry)
                    owned.append({"event": event, "entry": entry})
            else:
                previous = hooks.get(event)
                if previous is not None and previous != entries:
                    raise AuditStoreError("hook-entry-conflict")
                hooks[event] = entries
                owned.append({"event": event, "entry": entries})

        manifest.update(
            {
                "registration_root": str(root),
                "registration_state": "installing",
                "cleanup_required": True,
                "owned_entries": owned,
            }
        )
        save_manifest(run, manifest)  # durable intent precedes config mutation
        if not owner_path.exists():
            _write(owner_path, owner)
        _write(config_path, data)
        manifest["registration_state"] = "installed"
        save_manifest(run, manifest)
    return {"registration_state": "installed", "registration_root": str(root), "config_path": str(config_path)}


def remove(run: Path) -> dict:
    run = Path(run).resolve()
    manifest = load_manifest(run)
    runtime = manifest.get("runtime")
    project = Path(manifest.get("project_root", manifest.get("registration_root", "")))
    if manifest.get("registration_root"):
        root = Path(manifest["registration_root"])
        config = root / ("hooks.json" if runtime == "codex" else "hooks.v1.json")
        owner = root / ".temporary-tool-auditing-owner.json"
    elif project:
        root, config, owner = _paths(project, run, runtime)
    else:
        raise AuditStoreError("registration-location-unknown")
    conflicts = []
    manifest["teardown_probe_started_at"] = time.time()
    with _locked(root):
        data = _read(config) if config.exists() else {"hooks": {}}
        hooks = data["hooks"]
        for owned in manifest.get("owned_entries", []):
            event, entry = owned["event"], owned["entry"]
            current = hooks.get(event)
            if runtime == "codex":
                if isinstance(current, list) and entry in current:
                    current.remove(entry)
                    if not current:
                        hooks.pop(event, None)
                elif current is not None and any(
                    isinstance(candidate, dict)
                    and candidate.get("hooks", [{}])[0].get("command") == entry.get("hooks", [{}])[0].get("command")
                    for candidate in current
                ):
                    conflicts.append(event)
            elif current == entry:
                hooks.pop(event, None)
            elif current is not None:
                conflicts.append(event)
        if config.exists():
            if hooks or len(data) > 1:
                _write(config, data)
            else:
                config.unlink()
        if owner.exists() and not conflicts:
            try:
                current_owner = json.loads(owner.read_text(encoding="utf-8"))
            except Exception:
                current_owner = {}
            if current_owner.get("run_id") == manifest.get("run_id"):
                owner.unlink()
            else:
                conflicts.append("owner-marker")
    manifest["registration_state"] = "removed" if not conflicts else "conflict"
    manifest["cleanup_required"] = True
    save_manifest(run, manifest)
    return {
        "registration_state": manifest["registration_state"],
        "config_absent": not _has_owned_config(config, manifest),
        "conflicts": sorted(set(conflicts)),
    }


def _has_owned_config(config: Path, manifest: dict) -> bool:
    if not config.exists():
        return False
    try:
        data = _read(config)["hooks"]
        for owned in manifest.get("owned_entries", []):
            values = data.get(owned["event"])
            if isinstance(values, list) and owned["entry"] in values:
                return True
            if values == owned["entry"]:
                return True
    except AuditStoreError:
        return True
    return False
