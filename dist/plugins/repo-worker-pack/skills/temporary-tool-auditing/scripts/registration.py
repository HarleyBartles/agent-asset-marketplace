"""Install and remove only the project-local hook entries owned by one run."""

import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import sys
import time
from pathlib import Path

from runtime import render_handlers
from codex_trust import (
    add_project_trust,
    project_trust_absent,
    project_trust_level,
    recover_pending_trust_write,
    remove_project_trust,
)
from store import AuditStoreError, registration_lock, load_manifest, save_manifest


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


def _validate_registration_root(project: Path, root: Path) -> None:
    try:
        resolved_project = project.resolve(strict=False)
        resolved_root = root.resolve(strict=False)
        resolved_root.relative_to(resolved_project)
    except (OSError, ValueError):
        raise AuditStoreError("registration-root-outside-project") from None


def _is_run_recorder_entry(runtime: str, event: str, entry: dict, run: Path) -> bool:
    if runtime != "codex" or event not in {
        "PreToolUse",
        "PostToolUse",
        "SubagentStart",
        "SubagentStop",
        "SessionStart",
        "SessionEnd",
    }:
        return False
    if set(entry) != {"matcher", "hooks"} or entry.get("matcher") != "":
        return False
    if not isinstance(entry.get("hooks"), list) or len(entry["hooks"]) != 1:
        return False
    handler = entry["hooks"][0]
    if not isinstance(handler, dict) or handler.get("type") != "command":
        return False
    expected_keys = {"type", "command", "commandWindows"}
    if event == "SessionEnd":
        expected_keys.add("timeout")
    if set(handler) != expected_keys or (event == "SessionEnd" and handler.get("timeout") != 3):
        return False
    recorder = Path(run) / "scripts" / "record.py"
    run_dir = str(Path(run))
    for bytecode_flag in (True, False):
        args = (["-B"] if bytecode_flag else []) + [str(recorder), "--run-dir", run_dir]
        command = handler.get("command")
        command_windows = handler.get("commandWindows")
        if not isinstance(command, str) or not isinstance(command_windows, str):
            continue
        try:
            parsed = shlex.split(command, posix=True)
        except ValueError:
            continue
        if not parsed:
            continue
        interpreter = parsed[0]
        executable = interpreter.replace("\\", "/").rsplit("/", 1)[-1].lower()
        if not re.fullmatch(r"python(?:3(?:\.\d+)?)?(?:\.exe)?", executable):
            continue
        full_argv = [interpreter, *args]
        if parsed == full_argv and command == shlex.join(full_argv):
            if command_windows != subprocess.list2cmdline(full_argv):
                continue
            return True
    return False


def _matching_run_entries(data: dict, runtime: str, run: Path) -> list[dict]:
    matches = []
    for event, entries in data.get("hooks", {}).items():
        if isinstance(entries, list):
            matches.extend(
                {"event": event, "entry": entry}
                for entry in entries
                if isinstance(entry, dict) and _is_run_recorder_entry(runtime, event, entry, run)
            )
    return matches


def install(run: Path, project: Path, runtime: str) -> dict:
    run, project = Path(run).resolve(), Path(project).resolve()
    if runtime not in {"codex", "devin-desktop"}:
        raise AuditStoreError("unsupported-runtime")
    root, config_path, owner_path = _paths(project, run, runtime)
    _validate_registration_root(project, root)
    manifest = load_manifest(run)
    if manifest.get("runtime") != runtime:
        raise AuditStoreError("runtime-mismatch")
    # Keep the portable recorder dependencies beside the run so it remains usable
    # after the installed skill or source checkout changes.
    scripts = run / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    source_scripts = Path(__file__).resolve().parent
    for name in ("record.py", "runtime.py", "store.py", "sanitize.py", "codex_trust.py"):
        shutil.copyfile(source_scripts / name, scripts / name)
    rendered = render_handlers(runtime, scripts / "record.py")
    rendered_events = rendered.get("hooks", rendered)
    owned = []
    root_created = not root.exists()
    prior_intent = manifest.get("owned_entries", [])
    prior_pairs = {
        (item.get("event"), json.dumps(item.get("entry"), sort_keys=True))
        for item in prior_intent
        if isinstance(item, dict)
    }
    with registration_lock(root):
        _validate_registration_root(project, root)
        manifest = load_manifest(run)
        if manifest.get("runtime") != runtime:
            raise AuditStoreError("runtime-mismatch")
        if manifest.get("registration_state") in {"removing", "removed", "teardown-verified"}:
            raise AuditStoreError("registration-not-installable")
        prior_intent = manifest.get("owned_entries", [])
        prior_pairs = {
            (item.get("event"), json.dumps(item.get("entry"), sort_keys=True))
            for item in prior_intent
            if isinstance(item, dict)
        }
        config_created = not config_path.exists()
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
        for event, entries in rendered_events.items():
            current = hooks.setdefault(event, [])
            if not isinstance(current, list):
                raise AuditStoreError("hook-entry-conflict")
            for entry in entries:
                if entry not in current:
                    current.append(entry)
                    owned.append({"event": event, "entry": entry})
                elif (event, json.dumps(entry, sort_keys=True)) in prior_pairs:
                    owned.append({"event": event, "entry": entry})
                else:
                    raise AuditStoreError("registration-conflict")

        manifest.update(
            {
                "registration_root": str(root),
                "registration_state": "installing",
                "cleanup_required": True,
                "owned_entries": owned,
                "registration_root_created": bool(manifest.get("registration_root_created") or root_created),
                "registration_config_created": bool(manifest.get("registration_config_created") or config_created),
                "hook_interpreter": str(Path(sys.executable).resolve()),
                "lifecycle_cli_path": str((Path(__file__).with_name("auditctl.py")).resolve()),
            }
        )
        save_manifest(run, manifest)  # durable intent precedes config mutation
        if runtime == "codex":

            def persist_trust_intent(ownership):
                current_manifest = load_manifest(run)
                current_manifest["codex_trust"] = ownership
                save_manifest(run, current_manifest)

            prior_trust = manifest.get("codex_trust")
            trust_config_path = Path(prior_trust["config_path"]) if prior_trust else None
            if prior_trust and prior_trust.get("state") == "added":
                prior_trust.setdefault("run_id", manifest.get("run_id"))
                recover_pending_trust_write(prior_trust, persist_trust_intent)
            if not prior_trust or project_trust_level(project, trust_config_path) != "trusted":
                manifest["codex_trust"] = add_project_trust(
                    project,
                    trust_config_path,
                    persist_intent=persist_trust_intent,
                    run_id=manifest.get("run_id"),
                )
            else:
                manifest["codex_trust"] = prior_trust
        if not owner_path.exists():
            _write(owner_path, owner)
        _write(config_path, data)
        manifest["registration_state"] = "installed"
        save_manifest(run, manifest)
    return {
        "registration_state": "installed",
        "registration_root": str(root),
        "config_path": str(config_path),
        "trust": manifest.get("codex_trust", {}).get("state") if runtime == "codex" else None,
        "restart_required": runtime == "codex",
    }


def remove(run: Path) -> dict:
    run = Path(run).resolve()
    manifest = load_manifest(run)
    runtime = manifest.get("runtime")
    project_value = manifest.get("project_root")
    if not project_value and manifest.get("registration_root"):
        project_value = str(Path(manifest["registration_root"]).parent)
    project = Path(project_value or "")
    if manifest.get("registration_root"):
        root = Path(manifest["registration_root"])
        config = root / ("hooks.json" if runtime == "codex" else "hooks.v1.json")
        owner = root / ".temporary-tool-auditing-owner.json"
    elif project:
        root, config, owner = _paths(project, run, runtime)
    else:
        raise AuditStoreError("registration-location-unknown")
    _validate_registration_root(project, root)
    conflicts = []
    with registration_lock(root):
        manifest = load_manifest(run)
        current_root = Path(manifest.get("registration_root") or _paths(project, run, runtime)[0])
        if current_root.resolve() != root.resolve():
            raise AuditStoreError("registration-location-changed")
        _validate_registration_root(project, current_root)
        config = current_root / ("hooks.json" if runtime == "codex" else "hooks.v1.json")
        owner = current_root / ".temporary-tool-auditing-owner.json"
        manifest["teardown_probe_started_at"] = time.time()
        manifest["late_outcomes_allowed"] = False
        save_manifest(run, manifest)
        if owner.exists():
            try:
                current_owner = json.loads(owner.read_text(encoding="utf-8"))
            except Exception:
                raise AuditStoreError("registration-owner-invalid") from None
            if current_owner.get("run_id") != manifest.get("run_id"):
                raise AuditStoreError("registration-conflict")
        elif manifest.get("registration_state") != "removed":
            current_data = _read(config) if config.exists() else {"hooks": {}}
            if _has_owned_config(config, manifest) or _matching_run_entries(current_data, runtime, run):
                raise AuditStoreError("registration-owner-missing")
        data = _read(config) if config.exists() else {"hooks": {}}
        existing_owned = {
            (item.get("event"), json.dumps(item.get("entry"), sort_keys=True))
            for item in manifest.get("owned_entries", [])
            if isinstance(item, dict)
        }
        discovered = [
            item
            for item in _matching_run_entries(data, runtime, run)
            if (item["event"], json.dumps(item["entry"], sort_keys=True)) not in existing_owned
        ]
        if discovered:
            if not owner.exists():
                raise AuditStoreError("registration-owner-missing")
            manifest.setdefault("owned_entries", []).extend(discovered)
            save_manifest(run, manifest)
        hooks = data["hooks"]
        for owned in manifest.get("owned_entries", []):
            event, entry = owned["event"], owned["entry"]
            current = hooks.get(event)
            if isinstance(current, list) and entry in current:
                current.remove(entry)
                if not current:
                    hooks.pop(event, None)
            elif current is not None and isinstance(current, list) and current:
                conflicts.append(event)
            elif current is not None and not isinstance(current, list):
                conflicts.append(event)
        if config.exists() and not conflicts:
            if hooks or len(data) > 1 or not manifest.get("registration_config_created"):
                _write(config, data)
            else:
                config.unlink()
        if owner.exists() and not conflicts:
            owner.unlink()
        if manifest.get("registration_root_created"):
            try:
                root.rmdir()
            except OSError:
                pass
        if runtime == "codex" and manifest.get("codex_trust"):

            def persist_trust_intent(ownership):
                current_manifest = load_manifest(run)
                current_manifest["codex_trust"] = ownership
                save_manifest(run, current_manifest)

            trust_result = remove_project_trust(manifest["codex_trust"], persist_trust_intent)
            if trust_result.get("state") == "conflict":
                conflicts.append("codex-trust")
    manifest["registration_state"] = "removed" if not conflicts else "conflict"
    manifest["cleanup_required"] = True
    save_manifest(run, manifest)
    return {
        "registration_state": manifest["registration_state"],
        "config_absent": not _has_owned_config(config, manifest),
        "owned_trust_absent": project_trust_absent(manifest.get("codex_trust")),
        "restart_required": runtime == "codex",
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
    except AuditStoreError:
        return True
    return False


def registration_absent(run: Path, manifest: dict | None = None) -> bool:
    run = Path(run).resolve()
    manifest = manifest or load_manifest(run)
    root_value = manifest.get("registration_root")
    if not root_value:
        return manifest.get("registration_state") in {"not-installed", "removed", "teardown-verified"}
    root = Path(root_value)
    try:
        _validate_registration_root(Path(manifest.get("project_root", "")), root)
    except AuditStoreError:
        return False
    runtime = manifest.get("runtime")
    config = root / ("hooks.json" if runtime == "codex" else "hooks.v1.json")
    owner = root / ".temporary-tool-auditing-owner.json"
    if owner.exists():
        return False
    if _has_owned_config(config, manifest):
        return False
    if runtime == "codex" and config.exists():
        try:
            if _matching_run_entries(_read(config), runtime, run):
                return False
        except AuditStoreError:
            return False
    return project_trust_absent(manifest.get("codex_trust"))
