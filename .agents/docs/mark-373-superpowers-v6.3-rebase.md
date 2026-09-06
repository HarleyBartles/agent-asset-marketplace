# Superpowers+ v6.3 Rebase Record

## Source evidence

- Upstream repository: `https://github.com/obra/superpowers.git`
- Retrieval: one temporary blob-filtered clone at
  `C:\Users\hbart\AppData\Local\Temp\mark-373-superpowers-upstream`
- Comparison: `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9` (v6.2.0) ->
  `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` (v6.3.0)
- Both commits were verified as commit objects in the temporary clone.
- No upstream remote or upstream history is added to this repository.

The temporary clone is reference-only. The editable destination remains the
canonical `codex-marketplace/plugins/superpowers-plus/` tree.

## Disposition table

| upstream path | upstream change | existing first-party delta | disposition | canonical destination | validation |
|---|---|---|---|---|---|
| `.claude-plugin/marketplace.json` | Claude marketplace metadata | Not a marketplace skill surface | `not-applicable` | none | path absent from bundle |
| `.claude-plugin/plugin.json` | Claude plugin metadata | Not a Codex plugin surface | `not-applicable` | none | path absent from bundle |
| `.codex-plugin/plugin.json` | upstream plugin metadata | Marketplace has its own manifest/plugin metadata | `not-applicable` | existing marketplace metadata | marketplace checks |
| `.cursor-plugin/plugin.json` | Cursor plugin metadata | Not a Codex plugin surface | `not-applicable` | none | path absent from bundle |
| `.devin-plugin/plugin.json` | Devin plugin metadata | Not a Codex plugin surface | `not-applicable` | none | path absent from bundle |
| `.gitignore` | upstream repository ignores | Repository has its own generated/source policy | `not-applicable` | repository `.gitignore` | repository checks |
| `.hermes-plugin/__init__.py` | Hermes plugin support | No Hermes marketplace entry | `not-applicable` | none | path absent from bundle |
| `.hermes-plugin/plugin.yaml` | Hermes plugin metadata | No Hermes marketplace entry | `not-applicable` | none | path absent from bundle |
| `.kimi-plugin/plugin.json` | Kimi plugin metadata | Not a Codex plugin surface | `not-applicable` | none | path absent from bundle |
| `.version-bump.json` | upstream release automation metadata | Marketplace versioning is repo-local | `not-applicable` | repository version metadata | marketplace checks |
| `README.md` | upstream product documentation | Marketplace has first-party README surfaces | `not-applicable` | existing marketplace docs | documentation review |
| `RELEASE-NOTES.md` | upstream release notes | Upstream release retained by commit/provenance only | `not-applicable` | this record | source review |
| `docs/superpowers/plans/2026-07-30-codex-efficiency-fixes.md` | upstream design record | No upstream design-doc custody in active plugin | `not-applicable` | this record | source review |
| `docs/superpowers/plans/2026-08-06-hermes-version-bump-wiring.md` | upstream Hermes plan | Hermes is outside the Codex bundle | `not-applicable` | none | path absent from bundle |
| `docs/superpowers/specs/2026-07-30-codex-efficiency-fixes-design.md` | upstream design record | No upstream spec import | `not-applicable` | this record | source review |
| `docs/superpowers/specs/2026-08-05-hermes-version-bump-wiring-design.md` | upstream Hermes design | Hermes is outside the Codex bundle | `not-applicable` | none | path absent from bundle |
| `gemini-extension.json` | Gemini extension metadata | Not a Codex plugin surface | `not-applicable` | none | path absent from bundle |
| `package.json` | upstream package/version metadata | Marketplace package metadata is independent | `not-applicable` | existing marketplace metadata | marketplace checks |
| `scripts/bump-version.sh` | upstream release script | No shared release-script contract | `not-applicable` | none | path absent from bundle |
| `scripts/sync-to-codex-plugin.sh` | upstream sync script | Marketplace generator owns distribution | `not-applicable` | `tools/run.py` | marketplace checks |
| `skills/brainstorming/SKILL.md` | three-path classification and scaled ceremony | Rich first-party metadata/provenance | `manual-merge` | `skills/brainstorming/SKILL.md` | Task 3 structural tests |
| `skills/brainstorming/visual-companion.md` | portable Windows-safe launcher guidance | Marketplace does not carry the upstream visual-companion runtime or guide | `not-applicable` | none | path absent from bundle |
| `skills/finishing-a-development-branch/SKILL.md` | refusal-safe cleanup guidance | First-party custody/publication rules | `manual-merge` | `skills/finishing-a-development-branch/SKILL.md` | Task 4 structural tests |
| `skills/requesting-code-review/code-reviewer.md` | no nested reviewer dispatch | First-party prompt metadata | `manual-merge` | `skills/requesting-code-review/code-reviewer.md` | Task 5 structural tests |
| `skills/subagent-driven-development/SKILL.md` | rulings, conflict scan, batching, no stalls | First-party execution-lane contract | `manual-merge` | `skills/subagent-driven-development/SKILL.md` | Task 5 structural tests |
| `skills/subagent-driven-development/implementer-prompt.md` | no nested subagents/reviewers | First-party prompt template | `manual-merge` | `skills/subagent-driven-development/implementer-prompt.md` | Task 5 structural tests |
| `skills/subagent-driven-development/re-review-prompt.md` | no nested reviewers | First-party prompt template | `manual-merge` | `skills/subagent-driven-development/re-review-prompt.md` | Task 5 structural tests |
| `skills/subagent-driven-development/task-reviewer-prompt.md` | evidence readability and batched-file checks | First-party prompt template | `manual-merge` | `skills/subagent-driven-development/task-reviewer-prompt.md` | Task 5 structural tests |
| `skills/using-superpowers/SKILL.md` | adds non-Codex Hermes routing | Canonical entrypoint is `using-superpowers-plus` | `not-applicable` | `skills/using-superpowers-plus/SKILL.md` only where relevant | Task 3 structural tests |
| `skills/using-superpowers/references/codex-tools.md` | current Codex multi-agent/event guidance | First-party Codex adapter/reference | `manual-merge` | `skills/using-superpowers-plus/references/codex-tools.md` | Task 3/5 structural tests |
| `skills/using-superpowers/references/hermes-tools.md` | Hermes tool reference | Hermes is outside this Codex bundle | `not-applicable` | none | path absent from bundle |
| `skills/writing-plans/SKILL.md` | plan carries its governing spec | First-party recipient-relative planning metadata | `manual-merge` | `skills/writing-plans/SKILL.md` | Task 5 structural tests |
| `skills/writing-skills/render-graphs.js` | ESM and direct executable invocation | First-party skill tooling | `manual-merge` | `skills/writing-skills/render-graphs.js` | tooling/source checks |
| `tests/devin/test-devin-plugin.sh` | Devin plugin tests | No Devin marketplace entry | `not-applicable` | none | path absent from bundle |
| `tests/hermes/__init__.py` | Hermes test package | Hermes is outside this Codex bundle | `not-applicable` | none | path absent from bundle |
| `tests/hermes/conftest.py` | Hermes test configuration | Hermes is outside this Codex bundle | `not-applicable` | none | path absent from bundle |
| `tests/hermes/test_bootstrap.py` | Hermes bootstrap tests | Hermes is outside this Codex bundle | `not-applicable` | none | path absent from bundle |
| `tests/hermes/test_plugin.py` | Hermes plugin tests | Hermes is outside this Codex bundle | `not-applicable` | none | path absent from bundle |
| `tests/version-bump/test-bump-version.sh` | upstream release tests | Marketplace versioning is repo-local | `not-applicable` | none | path absent from bundle |
| `tests/writing-skills/test-render-graphs.sh` | upstream renderer test | Renderer source is retained; upstream test harness is not | `not-applicable` | existing repo checks | tooling/source checks |

Only the Codex-relevant skill changes above are candidates for deliberate
manual merge. Upstream release packaging, non-Codex integrations, and
upstream test/release infrastructure are not imported into the marketplace.

## Active provenance after application

The active Superpowers+ source will record upstream basis `obra/superpowers`
at v6.3.0 commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`, while preserving
the first-party ownership and adaptation metadata of the marketplace bundle.
