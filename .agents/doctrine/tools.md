## Scope

`tools/`

This scope covers repository validation and generation scripts.

Defer to the repository root `AGENTS.md` for global doctrine, publication rules, and upstream-drain policy.

The canonical task runner is `tools/run`. It composes the individual generator and validator scripts into a dependency-aware task graph.

- `./tools/run ci --check` (or `.\tools\run.ps1 ci --check` on Windows PowerShell) is the fail-fast CI gate. Use `ci --check --diagnostics` for a complete multi-failure report.
- `./tools/run marketplace --apply` (or `.\tools\run.ps1 marketplace --apply` on Windows PowerShell) is the canonical local full regeneration and validation entrypoint.
- `tools/run <target> --apply` / `tools/run.ps1 <target> --apply` regenerates only the named target and its prerequisites.
- `tools/run <target> --check` / `tools/run.ps1 <target> --check` validates only the named target and its prerequisites without writing.
- `tools/run --help` / `tools/run.ps1 --help` lists all targets and flags.
- `py -3 tools/run.py` or `python tools/run.py` works on any platform as a fallback.

Targets are: `normalize`, `lint`, `format`, `validate`, `repo-standards`, `tests-build`, `tests-repository`, `tests-shipping`, `inventory`, `marketplace`, `review-preflight`, `runtime-agents`, `ci`, and `all`.

Codex plugin first.

Use `--check` to validate without changing maintained files; builds and tests may create disposable ignored outputs. Use explicit `--apply` targets for formatting, normalization, generation, and other maintained-file repairs, then inspect and stage the result. The tracked hook checks the staged candidate in isolation and either rejects it with a focused repair/recheck command or passes it. It never repairs or stages repository content.

`py -3 tools/validate_marketplace.py` verifies the plugin manifest, bundle manifest, and referenced surfaces for each plugin.

## Policy for agent work

- Any change to canonical plugin skills, bundle manifests, adapter files, or plugin manifests requires a full market regeneration followed by validation before a PR may be called green.
- The canonical completion path is the full Marketplace regeneration stack.
- Partial regeneration paths are fallback-only repair tools and should not be advertised as a normal completion route.
- The expected source-publication preparation is `tools/run.py marketplace --apply` followed by inspection and staging of the intended tree.
- The expected CI green-path proof is `tools/run ci --check`.
- After editing source, run the appropriate explicit `tools/run <target> --apply` command to repair or regenerate derived surfaces. Stage the intended tree and commit normally; the pre-commit hook checks that staged snapshot in a disposable checkout and does not mutate it. Do not use `--no-verify` to bypass the hook.
- Do not run `tools/run ci --check` immediately before a normal commit or immediately after a successful hooked commit. Run `ci --check` only for an uncommitted verification, pipeline diagnosis, or explicit CI-parity work.
- Apply mode performs maintained-file changes; check mode validates the staged candidate and may create disposable build/test outputs. Keep both interfaces aligned so hosted CI and the local hook run the same complete checks.
- If a worker cannot run the full stack, it must say so explicitly instead of assuming CI will catch the missing regeneration.

Deterministic pack rule: if a plugin pack lacks a manifest-driven generator/validator path, add one to `tools/` and wire it into the standard `tools/run` update/check entrypoints. Do not paper over missing pipeline support with a pack-specific one-off script or a hand-edited output surface. The editable source custody for Marketplace generation is the canonical plugin skill trees, adapter overlays, provenance records, and bundle manifests. Treat generated Marketplace manifests and bundle manifests as derived outputs. Consumer plugin payloads are fetched and cached by the harness, not copied into `.agents/skills/`.

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

This file must stay aligned with the repo's validation and generation tooling. When tooling paths change, new validation scripts are added, or worker-facing commands evolve, review and update this file to reflect current expectations.
