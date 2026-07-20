# AGENTS.md

Scope: `tools/`

This scope covers repository validation and generation scripts.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

The skill-update path is now worker-facing through
`py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>`. The root
inventory that drives marketplace plugin ownership is
`codex-marketplace/plugin-roots.json`, GPT overlay sources live under
`adapters/gpt/`, and drift validation lives in
`tools/validate_generated_drift.py`.
The marketplace freshness proof is `py -3 tools/generate_marketplace.py --check`
for `.agents/plugins/marketplace.json` and
`codex-marketplace/manifest.json`, plus `py -3 tools/generate_repo_index.py
--check` for `repo-index/repo-index.json`. Projection-lane freshness is
proven by `py -3 tools/materialize_projection.py --check`, and the selected
pack bundle-manifest surfaces are proven by `py -3 tools/generate_pack_manifests.py
--check`. `validate_repo_index.py` checks metadata alignment, not freshness by
itself. The repo-wide `INDEX.md` mesh is proven by `py -3 tools/generate_index_mesh.py
--check`, and mesh law lives in `../.agents/docs/mesh-policy.md`.
Agent skills installation is handled by `py -3 tools/install_agent_skills.py`,
which deterministically installs/refreshes skills in `.agents/skills` based on
plugins with `INSTALLED_BY_DEFAULT` policy in `.agents/plugins/marketplace.json`.
`py -3 tools/generate_pack_manifests.py --check` also verifies any
manifest-declared generated inventory blocks in pack `README.md`, `SOURCE.md`,
and `PROJECTION.md` surfaces.
The canonical full rebuild and validation entrypoint is
`py -3 tools/rebuild_marketplace.py`.
The canonical non-mutating CI gate is `py -3 tools/check_marketplace.py`.
Overlay self-healing is handled by `py -3 tools/heal_overlays.py`, which
adjusts `overlay.yaml` line-edit entries when source normalization (CRLF→LF,
trailing whitespace stripping) shifts line numbers or whitespace. It runs
automatically in write mode during `rebuild_marketplace.py` and in check mode
during `check_marketplace.py`. If `heal_overlays.py --check` fails, run
`py -3 tools/rebuild_marketplace.py` to auto-heal stale overlays.

## Routing pointers

- `../.agents/docs/mesh-policy.md` before changing generator or validator behavior
- `../.agents/guides/planning-guide.md` before planning tool changes
- `../.agents/guides/implementing-guide.md` before implementing tool changes
- `../.agents/guides/marketplace-generation-guide.md` before changing marketplace regeneration behavior
- `../.agents/guides/code-review-guide.md` before reviewing tooling changes

Policy for agent work:

- Any change to source custody, adapter files, projection plugin shapes, bundle manifests,
  source maps, provenance maps, or generated zips requires a full market regeneration
  followed by validation before a PR may be called green.
- The canonical completion path is the full regeneration stack, not a partial refresh.
- Partial regeneration paths are fallback-only repair tools and should not be
  advertised as a normal completion route.
- The expected local green-path proof is `py -3 tools/rebuild_marketplace.py`.
- The expected CI green-path proof is `py -3 tools/check_marketplace.py`.
- Both commands must be aligned so check mode fails if regeneration would be
  needed and write mode still performs the actual regeneration locally.
- If a worker cannot run the full stack, it must say so explicitly instead of
  assuming CI will catch the missing regeneration.

Deterministic pack rule: if a skillset pack or projection lane lacks a
manifest-driven generator/validator path, add one to `tools/` and wire it into
the standard update/check entrypoints. Do not paper over missing pipeline
support with a pack-specific one-off script or a hand-edited output surface.
The editable source custody for marketplace generation is the trio of source
trees, adapters/overlays, and `codex-marketplace/custody-pack-registry.json`.
Treat generated manifests, projection trees, source maps, provenance maps, and
zip artifacts as derived outputs only. If a convention can be expressed in the
registry and generator, do that instead of hand-rolling per-pack output
conventions in the generated surfaces.

## Line-ending policy for generated files

This repo normalizes to LF. `core.autocrlf` is `false` so git does not
translate line endings. Generators and agents that write text files must
write LF explicitly, not the platform default (CRLF on Windows).

When using `Path.write_text()`, always pass `newline="\n"`:
```python
path.write_text(content, encoding="utf-8", newline="\n")
```

When using `open("w")`, always pass `newline="\n"` (or `newline=""` if the
text already contains explicit `\n` and you want no translation):
```python
with path.open("w", encoding="utf-8", newline="\n") as f:
    f.write(content)
```

Without the explicit `newline` parameter, Python translates `\n` to
`os.linesep` (CRLF on Windows), which `git diff --check` flags as trailing
whitespace and which churns every generated file on every rebuild.

Do not add CRLF detection or preservation logic to generators. Always
write LF.

## Review guidelines

- Flag validators that can pass while indexed paths, plugin manifests, or
  registry entries have already drifted.
- Flag generator changes that are not paired with matching validation updates.
- Flag JSON or path parsing that could silently skip missing files, stale
  references, or unsupported plugin entries.
- Flag tooling changes that do not keep the marketplace export, repo index,
  and validation command documentation aligned.
- Flag targeted skill-update helpers that rewrite unrelated generated state or
  that hide full-regeneration behavior behind an ordinary update path.
- Flag GPT export manifests that allow raw Codex-specific assumptions to leak
  into generated skill zips instead of using an overlay or exclusion.

## Maintenance responsibility

This file must stay aligned with the repo's validation and generation tooling.
When tooling paths change, new validation scripts are added, or worker-facing
commands evolve, review and update this file to reflect current expectations.
The skill-update path, marketplace inventory source, and drift validation
references must stay accurate—when those change, this file should be updated to
prevent drift.
