# Task 2 Fix Report — repo-standards.py Important Issues

## What was implemented

1. **Shared-checkout override warning**  
   In `main()`, before any apply path runs, `repo_standards.py` now prints a warning to `sys.stderr` whenever `--allow-shared-checkout` is used:
   > `warning: --allow-shared-checkout is an override and requires human approval before applying changes`

2. **Conditional `marketplace-source` submodule check**  
   `_check_surface()` now only reports a `submodule not initialized` finding when `.gitmodules` exists and actually declares the path `.agents/plugins/marketplace-source`. If the path is not declared (as in the source marketplace repo), the surface is treated as not applicable and is not flagged.

## Test commands and results

```powershell
py -3 "Z:\_agent-worktrees\agent-asset-marketplace\repo-standards-design\sources\first_party\skills\repo-standards\scripts\repo_standards.py" --check
```

Output:

```text
DRIFT: missing: scripts/ci-preflight.ps1
DRIFT: missing: scripts/ci-preflight.sh
DRIFT: missing hook: .git/hooks/pre-commit
```

Exit code: `1`

The `marketplace-source` submodule drift is no longer reported after the `.gitmodules` conditional change. The remaining three surfaces are generated/consumer-repo surfaces that are not present in this source worktree (a git worktree with no `.git/hooks` directory).

Additional verification:

```powershell
py -m py_compile "Z:\_agent-worktrees\agent-asset-marketplace\repo-standards-design\sources\first_party\skills\repo-standards\scripts\repo_standards.py"
```

Exit code: `0`

```powershell
git -C "Z:\_agent-worktrees\agent-asset-marketplace\repo-standards-design" diff --check
```

Exit code: `0`

## Publication

```text
commit a235c3ec fix(repo-standards): warn on shared-checkout override and conditional submodule check
```

Pushed to `origin repo-standards-design`:

```text
To https://github.com/HarleyBartles/agent-asset-marketplace.git
   780fdffd..a235c3ec  repo-standards-design -> repo-standards-design
```

## Files changed

- `sources/first_party/skills/repo-standards/scripts/repo_standards.py`

## Concerns

The two requested fixes are implemented and verified. However, the `--check` command in this source worktree still reports drift for `scripts/ci-preflight.ps1`, `scripts/ci-preflight.sh`, and `.git/hooks/pre-commit`. These are consumer-generated or git-worktree-specific surfaces and were not in scope of the requested fixes, so the worktree does not yet produce the `OK repo-standards: all surfaces present` result.

## Status

**DONE_WITH_CONCERNS**
