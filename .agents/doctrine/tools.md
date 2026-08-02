
## Scope

`tools/`

This scope covers repository validation and generation scripts.

Defer to the repository root `AGENTS.md` for global doctrine, publication rules, and upstream-drain policy.

The canonical task runner is `tools/run`. It composes the individual generator and validator scripts into a dependency-aware task graph.

- `./tools/run ci --check` (or `.\tools\run.ps1 ci --check` on Windows PowerShell) is the full non-mutating CI gate (lint, repo-standards, marketplace).
- `./tools/run marketplace --apply` (or `.\tools\run.ps1 marketplace --apply` on Windows PowerShell) is the canonical local full regeneration and validation entrypoint.
- `tools/run <target> --apply` / `tools/run.ps1 <target> --apply` regenerates only the named target and its prerequisites.
- `tools/run <target> --check` / `tools/run.ps1 <target> --check` validates only the named target and its prerequisites without writing.
- `tools/run --help` / `tools/run.ps1 --help` lists all targets and flags.
- `py -3 tools/run.py` or `python tools/run.py` works on any platform as a fallback.

Targets are: `inventory`, `installed-skills`, `repo-index`, `mesh`, `validate`, `marketplace`, `lint`, `repo-standards`, `ci`, `all`.

Codex plugin first.

Use `--check` to validate the current generated surface without rewriting it. `--allow-shared-checkout` is approved once by `tools/run` and forwarded to child scripts that require explicit approval to write in the main shared checkout. It is not needed in a linked worktree. `--allow-shared-checkout` alone is rejected by those scripts.

`py -3 tools/validate_marketplace.py` verifies the plugin manifest, bundle manifest, and referenced surfaces for each plugin.

## Policy for agent work

- Any change to canonical plugin skills, bundle manifests, adapter files, or plugin manifests requires a full market regeneration followed by validation before a PR may be called green.
- The canonical completion path is the full regeneration stack, not a partial refresh.
- Partial regeneration paths are fallback-only repair tools and should not be advertised as a normal completion route.
- The expected local green-path proof is `tools/run marketplace --apply`.
- The expected CI green-path proof is `tools/run ci --check`.
- After editing source, run the appropriate `tools/run <target> --apply` command to regenerate derived surfaces. Stage all changes. Then run the preflight (`tools/run ci --check`) on the staged tree before committing. The pre-commit hook also runs `ci --check` on the staged tree; if it is available, commit normally and it will re-run the same checks.
- Run `tools/run ci --check` on the staged tree before committing. If the pre-commit hook is installed, commit normally and it will re-run the same checks. Do not use `--no-verify` to bypass the hook.
- Both commands must be aligned so check mode fails if regeneration would be needed and write mode still performs the actual regeneration locally.
- If a worker cannot run the full stack, it must say so explicitly instead of assuming CI will catch the missing regeneration.

Deterministic pack rule: if a plugin pack lacks a manifest-driven generator/validator path, add one to `tools/` and wire it into the standard `tools/run` update/check entrypoints. Do not paper over missing pipeline support with a pack-specific one-off script or a hand-edited output surface. The editable source custody for marketplace generation is the canonical plugin skill trees, adapter overlays, provenance records, and bundle manifests. Treat generated marketplace manifests, bundle manifests, repo index, index mesh, and installed skill surfaces as derived outputs only. If a convention can be expressed in the plugin metadata and generator, do that instead of hand-rolling per-pack output conventions in the generated surfaces.

## Line-ending policy for generated files

This repo normalizes to LF. `core.autocrlf` is `false` so git does not translate line endings. Generators and agents that write text files must write LF explicitly, not the platform default (CRLF on Windows).

When writing text files, prefer `open("w")` with `newline="\n"`:
```python
with path.open("w", encoding="utf-8", newline="\n") as f:
    f.write(content)
```

Do not pass `newline=` to `Path.read_text()` in scripts that must run under Python 3.12; the `newline` keyword for `Path.read_text()` was added in Python 3.13. For consistent LF-only reads and writes across `Path.read_text()` and `Path.write_text()`, prefer `Path.open(..., newline="\n")` or the built-in `open(..., newline="\n")` (or `newline=""` if the text already contains explicit `\n` and you want no translation) instead.

Without the explicit `newline` parameter, Python translates `\n` to `os.linesep` (CRLF on Windows), which `git diff --check` flags as trailing whitespace and which churns every generated file on every rebuild.

Do not add CRLF detection or preservation logic to generators. Always write LF.

## Review guidelines

- Flag validators that can pass while indexed paths, plugin manifests, or registry entries have already drifted.
- Flag generator changes that are not paired with matching validation updates.
- Flag JSON or path parsing that could silently skip missing files, stale references, or unsupported plugin entries.
- Flag tooling changes that do not keep the marketplace export, repo index, and validation command documentation aligned.
- Flag targeted skill-update helpers that rewrite unrelated generated state or that hide full-regeneration behavior behind an ordinary update path.

## Maintenance responsibility

This file must stay aligned with the repo's validation and generation tooling. When tooling paths change, new validation scripts are added, or worker-facing commands evolve, review and update this file to reflect current expectations. The skill-update path, marketplace inventory source, and drift validation references must stay accurate—when those change, this file should be updated to prevent drift.
