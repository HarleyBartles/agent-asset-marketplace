# Standard Authority Packages Implementation Plan

**Status:** completed-awaiting-retirement

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Ship the agreed selectable standard definitions and an immutable subscription-record interface without migrating existing consumer implementations.

**Architecture:** Each standard has one focused skill and a definition reference. The repo-standards coordinator owns a small discovery catalog, record schema, read-only record checker, and local pinned-source reader. Current repo-shape deployment/runtime remains an explicitly legacy compatibility path until the roadmap's Marketplace migration.

**Tech Stack:** Markdown skill/reference files, JSON catalogs/schema, standard-library Python, pytest, existing deterministic Marketplace builder.

**Spec:** [Approved AOM design](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md).

**Roadmap:** [AOM adoption and shipping](roadmap.md), Plan 1. Planning baseline is commit `c380a60e8`; source baseline is the approved spec's investigated commit. Re-read live source before execution.

**Execution Strategy:** `executing-plans`, because the catalog, schema, coordinator, and generated package closure share one evolving authority model; inline continuity avoids repeatedly reconstructing that model. Obtain a fresh whole-change review at handoff. Do not begin execution before this plan is reviewed.

## Global Constraints

- The repo owns implementation and compliance. This plan supplies capabilities and definitions; it does not certify or migrate this Marketplace or any other repo.
- Subscription authority is standard ID, source repository, immutable Git commit, definition path, and certification reference. Ambient refresh is not an adoption upgrade.
- Root AGENTS is mandatory for adoption; no full AGENTS-standard subscription is implied. A checker can report missing routes but cannot certify useful routing by file existence.
- Ship no historical definition bundle, source submodule requirement, copied one-time scaffolders, fixed book inventory, automatic target installer, or latest-version alarm.
- Keep one portable Python implementation for Python work. Avoid new runtime dependencies for the authority helpers.
- Edit canonical source and `src/plugin-definitions/`; regenerate `dist/` through the existing bus.
- This plan does not remove old runtime files, change live `.agents/contracts/operating-standards.json`, remove this repo's formatter, alter the pre-commit hook, or rewrite other repos.
- Tests below are implementation acceptance work, not tests to run during plan authoring. Extend genuine behavior coverage rather than freeze wording or count headings.

## Review Focus

- Current plugin refresh must not invalidate an older or repository-owned subscription: Task 2 accepts valid IDs independently of the current catalog; Task 3 reads the pinned commit after the local branch advances.
- Missing or mutable authority must not turn into a latest-definition fallback: Tasks 2 and 3 reject floating commit values and missing pinned content without mutation.
- Consumer-controlled command fields must not become executable validation instructions: Task 2 rejects legacy command fields in v2 and never invokes declared commands.
- A package that works only in the source checkout is broken: Task 5 runs the installed helper with an isolated consumer and checks definition routes resolve inside the copied plugin.
- Definitions are semantic pledges, not headings or templates: Tasks 1 and 4 use bounded adoption scenarios and review the actual decisions, not text-presence tests.

## File and interface map

Paths below are relative to the canonical worktree. New names are implementation choices within the approved spec, fixed here so executors do not rediscover them.

| Standard ID                  | Owning skill                 | Definition path                                            |
| ---------------------------- | ---------------------------- | ---------------------------------------------------------- |
| `repo-plugin-subscriptions`  | `repo-agent-assets`          | `skills/repo-agent-assets/references/standard.md`          |
| `root-agent-router`          | `agents-routing`             | `skills/agents-routing/references/standard.md`             |
| `runbook-composition`        | `runbook-composition`        | `skills/runbook-composition/references/standard.md`        |
| `playbook-composition`       | `playbook-composition`       | `skills/playbook-composition/references/standard.md`       |
| `agent-doctrine-contracts`   | `agent-doctrine-contracts`   | `skills/agent-doctrine-contracts/references/standard.md`   |
| `tracked-validation-hook`    | `tracked-repo-hooks`         | `skills/tracked-repo-hooks/references/standard.md`         |
| `command-bus`                | `command-bus`                | `skills/command-bus/references/standard.md`                |
| `review-entrypoint`          | `review-entrypoint`          | `skills/review-entrypoint/references/standard.md`          |
| `contribution-entrypoint`    | `contribution-entrypoint`    | `skills/contribution-entrypoint/references/standard.md`    |
| `completed-artifact-custody` | `completed-artifact-custody` | `skills/completed-artifact-custody/references/standard.md` |
| `unslop`                     | `unslop`                     | `skills/unslop/references/standard.md`                     |

The two existing plugin-management catalog entries consolidate under `repo-plugin-subscriptions`. IDs preserved from the old catalog continue identifying their concern; their new definitions are separately pinned. Old records do not acquire these new requirements automatically.

Create `skills/repo-standards/references/standards-catalog.json` as the new capability discovery catalog:

```json
{
  "version": 2,
  "standards": [
    {
      "id": "command-bus",
      "title": "Command bus",
      "skill": "command-bus",
      "definition": "skills/command-bus/references/standard.md"
    }
  ]
}
```

The complete catalog contains all eleven mapped rows. Paths are canonical source paths, not installed-plugin paths. Within SKILL.md, use actual relative links that resolve in both source and installed skill layouts. No automatic dependencies, executable command fields, universal resource deployment list, or semantic compliance booleans.

The subscription format is version 2:

```json
{
  "version": 2,
  "standards": [
    {
      "id": "command-bus",
      "source": {
        "repository": "https://github.com/HarleyBartles/agent-asset-marketplace.git",
        "commit": "0123456789abcdef0123456789abcdef01234567",
        "definition": "skills/command-bus/references/standard.md"
      },
      "certification": ".agents/contracts/standards-certification.md#command-bus"
    }
  ]
}
```

The example commit is a syntax fixture, not claimed published authority. Actual adoption uses an existing retrievable commit. Empty standards lists remain valid for explicit non-adoption. Repository-owned standard IDs are valid without appearing in the current AOM catalog; source authority belongs to their own repo. Standard IDs use lowercase kebab-case (`^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`). Duplicate IDs and unknown fields are rejected. `commit` accepts full 40- or 64-character lowercase hexadecimal IDs, not branches or abbreviations. Definition and certification file paths are relative, normalized POSIX paths without traversal, absolute/drive/UNC forms, or colons; certification may have a nonempty fragment. Repository identifiers are nonempty strings; fetching and authentication are outside this read-only checker.

## Task 1: Publish focused definitions and discovery catalog

**Files:** Create the eight new skill homes from the table, their `SKILL.md` and `references/standard.md`; create the three definition references in existing `repo-agent-assets`, `tracked-repo-hooks`, and `command-bus`; create `skills/repo-standards/references/standards-catalog.json`. Add `skills/repo-standards/tests/behavior/standard-selection.md` and evaluator-only assessment notes under `skills/repo-standards/tests/evaluator-only/standard-selection.md`. Modify `src/plugin-definitions/agent-operating-model/contents.json` to include the new owners immediately and its `plugin.json`, `files/package.json`, and `files/README.md` to explain the additive compatibility bridge.

**Consumes:** Approved spec sections 2-6, including all shared adoption requirements.

**Produces:** Eleven independently readable definitions and the exact catalog rows above. Definitions name their stable ID, pledge, standalone obligations, conditional obligations, self-certification criteria, and optional asset policy. They do not require a universal document heading scheme from consumer books.

- [x] Write the selection behavior fixture with these bounded prompts before authoring guidance:

```text
Case A: A tiny repo wants a release-stage runbook only. It has no playbooks,
doctrine store, or ambient workflow plugin. Explain adoption requirements.
Case B: Installed AOM changed today. This repo's certification pins an older
commit. Assess whether an upgrade is mandatory or produces a warning.
Case C: A repo has a root REVIEW.md with its review guide inline. Assess whether
it must create review books or another guidance store.
```

Keep expected judgments evaluator-only: A requires useful stage guidance, certification and root routing but no starter inventory; B remains governed by its pin without alarms; C permits inline review guidance. Assess decisions, not exact phrasing. Run a fresh skill behavior probe only during authorized implementation using available capabilities; record results in task scratch, never alongside shipped prompts.

- [x] Author each definition from its corresponding approved spec subsection, including shared records/routing and relevant cross-standard obligations. The unslop definition includes the standalone management method now, even though optional observation starters land in Plan 5. Do not claim a checker, hook starter, or template exists before its later delivery.
- [x] Write each owning SKILL.md with installed-skill frontmatter, a concise trigger description, an on-demand definition link, and instructions to inspect the repo's declared authority before assessment. An explicit upgrade resolves the requested source; ordinary use must not substitute current guidance for older pinned requirements.
- [x] Write the discovery catalog using the eleven table rows. Retain the old `skills/repo-shape/references/operating-standards-catalog.json` unchanged for current runtime compatibility.
- [x] Add the new skill membership using the existing first-party provenance shape in contents.json. Update metadata without claiming future starters exist. Retain legacy capabilities needed for v1 consumers. Run `py -3 tools/run.py marketplace --apply`, review the prompts against the source skills, stage canonical additions and owned generated output, and commit through the normal hook. This makes Task 1 independently deliverable with no temporary membership failure.

**Exit:** A reader can determine one standard's actual pledge independently; optional assets and other standards do not turn into hidden obligations. No current consumer runtime changes.

## Task 2: Structural subscription validation

**Files:** Create `skills/repo-standards/references/subscriptions.schema.json`, `skills/repo-standards/scripts/subscriptions.py`, and `skills/repo-standards/tests/scripts/test_subscriptions.py`. Do not change live repo subscription records.

**Interfaces:**

```python
def validate_record(raw: object) -> list[str]:
    """Return structural diagnostics; empty means structurally valid only."""

def check_repository(repo_root: Path) -> list[str]:
    """Read v2 record and referenced files; never execute, scaffold, or fetch."""

def main(argv: list[str] | None = None) -> int:
    """--repo-root PATH --check; errors nonzero; --help does no work."""
```

`check_repository` checks root AGENTS and certification-file existence for selected subscriptions, not semantic routing or claim truth. It uses `.agents/contracts/operating-standards.json`; missing records report missing input, not implicit adoption. Version 1 reports an explicit legacy-format diagnostic and leaves bytes alone. Empty v2 subscriptions do not initialize AGENTS or require certification files. The JSON schema and Python checker must accept/reject the same structural cases without needing a runtime schema library.

Expose `validate_commit(value: object) -> list[str]` and `validate_relative_path(value: object, *, allow_fragment: bool = False) -> list[str]` for Task 3 reuse. CLI `--repo-root` defaults to the current directory; bare `--check` must respond with a clear result and exit 0 or 1 rather than an argparse missing-option exit. This fits the existing skill-script CLI validator.

- [x] Add independent behavior tests with this minimal fixture and the assertions below:

```python
def record(standard_id="repo-private", commit="a" * 40):
    return {"version": 2, "standards": [{
        "id": standard_id,
        "source": {"repository": "https://example.com/private.git",
                   "commit": commit, "definition": "rules/standard.md"},
        "certification": ".agents/contracts/certification.md#private",
    }]}

def test_pinned_repo_owned_standard_does_not_need_current_catalog():
    assert validate_record(record()) == []

def test_floating_authority_is_rejected():
    assert validate_record(record(commit="main"))

def test_legacy_commands_are_not_v2_authority():
    raw = record()
    raw["standards"][0]["check"] = ["python", "sentinel.py"]
    assert validate_record(raw)
```

Also cover duplicate IDs, malformed entry/source types, 64-character IDs, empty selections, unknown fields, missing root AGENTS/certification, empty certificate fragments, POSIX traversal, Windows drive-relative paths, UNC paths, and malformed JSON. These protect actual cross-platform structural behavior, not document wording.

- [x] Run `py -3 -m pytest -q skills/repo-standards/tests/scripts/test_subscriptions.py` and observe the specific unsupported behavior before implementation.
- [x] Implement schema and standard-library validation using explicit field sets, `PurePosixPath`/`PureWindowsPath` checks, and read-only JSON loading. Use no shell evaluation. Never interpret `check`, `apply`, or paths from a v1 record as executable instructions. CLI output states that structural validity is not certification.
- [x] Add a subprocess fixture that snapshots consumer bytes, invokes the checker, and asserts no file additions or changes for valid, missing, and legacy records. Put an executable sentinel in the fixture and assert it is never invoked.
- [x] Run the focused suite and `py -3 tools/run.py marketplace --apply`; stage only owning source/tests and regenerated outputs; commit with the normal hook. No duplicate complete CI command before/after the commit.

**Exit:** Valid pinned records and malformed/legacy input have clear structural results, and the checker cannot silently adopt, fetch, execute declared commands, or assert semantic compliance.

## Task 3: Read immutable definitions from local Git authority

**Files:** Create `skills/repo-standards/scripts/pinned_definition.py`, `skills/repo-standards/tests/scripts/test_pinned_definition.py`, and `skills/repo-standards/references/source-resolution.md`.

**Consumes:** Task 2 path/commit constraints; call its validation utilities rather than duplicate incompatible rules.

**Produces:**

```python
def read_pinned_definition(source_root: Path, commit: str, definition: str) -> bytes:
    """Read exactly commit:path using local Git; raise ValueError on bad input
    and a clear retrieval error when the object or path is unavailable."""
```

CLI: `python pinned_definition.py --source-root PATH --commit FULL_ID --definition RELATIVE_PATH --check` prints the exact definition bytes or reports retrieval failure. `--help` does no source reading. The caller supplies a checkout matching the declared source repository; the adoption guide requires verifying its origin/identity before calling. This helper does not authenticate, clone, fetch, write a reference copy, validate semantics, or fall back to HEAD. Online retrieval is an explicit agent action outside it.

Bare `--check` reports missing retrieval inputs with exit 1, without fetching or inspecting an inferred repository. `--help` exits 0. This is helper validation, not a command-bus mutation preview.

- [x] Write this real temporary-Git fixture. It uses explicit fixture-local identity and stripped repository-local environment, not the user's global settings:

```python
@pytest.fixture
def git_authority(tmp_path):
    root = tmp_path / "authority"
    root.mkdir()
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        env.pop(key, None)
    def git(*args):
        return subprocess.run(
            ["git", "-C", str(root), *args], env=env,
            check=True, capture_output=True, text=True,
        ).stdout.strip()
    git("init")
    git("config", "user.name", "Fixture")
    git("config", "user.email", "fixture@example.invalid")
    path = root / "rules/standard.md"
    path.parent.mkdir()
    path.write_bytes(b"old requirements\n")
    git("add", "rules/standard.md")
    git("-c", "core.hooksPath=", "commit", "-m", "old definition")
    old_commit = git("rev-parse", "HEAD")
    path.write_bytes(b"new requirements\n")
    git("add", "rules/standard.md")
    git("-c", "core.hooksPath=", "commit", "-m", "new definition")
    return root, old_commit
```

The temporary fixture has no project hooks; this local override isolates it from user-global hook configuration and must never be used for Marketplace commits.

- [x] Add these behavioral assertions:

```python
def test_older_commit_is_read_after_branch_advances(git_authority):
    root, old_commit = git_authority
    assert read_pinned_definition(root, old_commit, "rules/standard.md") == b"old requirements\n"

def test_missing_path_has_no_head_fallback(git_authority):
    root, old_commit = git_authority
    with pytest.raises((ValueError, RuntimeError)):
        read_pinned_definition(root, old_commit, "rules/missing.md")
```

Add absent-object, invalid commit, unsafe path, and working-tree-dirty cases. The latter must still read committed authority, without resetting or modifying the checkout.

- [x] Run `py -3 -m pytest -q skills/repo-standards/tests/scripts/test_pinned_definition.py` and establish the missing behavior.
- [x] Implement this retrieval shape, importing Task 2 validators from the neighboring helper. Raise `ValueError` for input errors and `RuntimeError` for unavailable authority; never fall back to HEAD:

```python
def read_pinned_definition(source_root, commit, definition):
    issues = validate_commit(commit) + validate_relative_path(definition)
    if issues:
        raise ValueError("; ".join(issues))
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        env.pop(key, None)
    result = subprocess.run(
        ["git", "-C", str(source_root), "show", f"{commit}:{definition}"],
        env=env, shell=False, capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout
```

- [x] Write source-resolution guidance: verify source identity, retrieve the declared commit explicitly when absent, read the exact definition, and report unavailable authority without assessing latest requirements instead. An offline retained snapshot must identify its pin; do not treat an unverified downloaded file as source proof.
- [x] Run both authority suites, regenerate with `py -3 tools/run.py marketplace --apply`, and commit the source helper, tests, and owned projections through the normal hook.

**Exit:** Advancing current source or refreshing ambient AOM does not change what bytes the pinned authority reader returns.

## Task 4: Coordinator and compatibility routing

**Files:** Modify `skills/repo-standards/SKILL.md`, `skills/repo-shape/SKILL.md`, `skills/repo-composition/SKILL.md`, and the existing owner skills `repo-agent-assets`, `tracked-repo-hooks`, and `command-bus`. Add `skills/repo-standards/references/adoption-and-certification.md` and `skills/repo-standards/tests/behavior/authority-routing.md`.

**Consumes:** Task 1 catalog and focused definitions, Tasks 2-3 helpers.

**Produces:** Explicit new-model adoption/assessment/upgrade routes and bounded legacy guidance; no second semantic authority in broad legacy skills.

- [x] Add scenarios before changing instructions: v1 consumer asks for assessment, v2 repo pins a removed/non-current standard, new adopter requests only runbooks, and existing authored certification disagrees with observed implementation. Expected actions respectively preserve existing pinned legacy authority without auto-migration; retrieve declared historical source; adopt only requested obligations; report real drift without altering the pin to pass.
- [x] Update repo-standards to inspect the record format and requested task. V1 means use the existing pinned deployment or retrieve its historical definition, not run current scaffolders to upgrade it. V2 means follow immutable source and certification. Missing record is non-adoption until explicitly requested adoption. The coordinator advertises the new catalog as choices, not mandatory surfaces.
- [x] Add the adoption guide with root entrypoint routing, honest semantic certification, optional starter selection, and explicit upgrade reconciliation. Use the default paths from the spec. Do not provide a command that records certified success based solely on the structural checker.
- [x] Convert repo-composition to route stage and concern work to the focused owners. Mark repo-shape as legacy structural/deployment compatibility rather than the definition of every new standard. Preserve old executable resources for existing v1 consumer runtime; removal belongs in Plan 6.
- [x] Reconcile the three reused owner skills with their new definitions. Keep current ancillary reference material where useful, but route semantic requirements to the owning definition. Remove instructions that make Marketplace submodules, Markdown standard adoption, shared-checkout flags, or fixed book inventories requirements of the new model. Do not edit current runtime scripts in this task.
- [x] Probe the bounded scenarios in fresh implementation-time contexts and review decisions against the spec. Regenerate with `py -3 tools/run.py marketplace --apply`, then commit instructions and owned projections, preserving attribution and source metadata.

**Exit:** No ambient route implies adoption or changes historical requirements; generic capability guidance cannot silently revive retired obligations.

## Task 5: Package closure and plan completion

**Files:** Add `tests/shipping/test_aom_standard_authority.py`; reconcile Task 1's `src/plugin-definitions/agent-operating-model/contents.json`, `plugin.json`, `files/package.json`, and `files/README.md` against the completed capability. Generated files include `dist/plugins/agent-operating-model/**`, `dist/manifest.json`, and `.agents/plugins/marketplace.json` only as produced by the builder. Do not hand-edit them.

**Consumes:** Tasks 1-4 canonical skills and helpers; existing `src/marketplace/build.py` deterministic copy behavior.

**Produces:** Self-contained AOM package exposing all target owners and the coordinator, with isolated runtime proof. Existing nonstandard capability skills such as Python remain unless they conflict with this plan; broad removal is not authorized here.

- [x] Add a shipping test that copies generated `dist/plugins/agent-operating-model` to an isolated temp directory, creates a separate consumer with a v2 record, root AGENTS, and certificate file, then invokes its packaged `skills/repo-standards/scripts/subscriptions.py`. Expected exit is 0 with a structural-only result. Remove certificate and expect nonzero. Snapshot consumer bytes to prove no writes. The source checkout is not on PYTHONPATH and the subprocess cwd is the consumer, not Marketplace.
- [x] Add a definition-link closure assertion: use actual package-relative links from owning skill entries and resolve them within the isolated plugin. Verify no required path escapes into canonical source or another plugin. Execute packaged pinned-definition retrieval against Task 3's temporary Git authority; no source-checkout imports are allowed.
- [x] Confirm AOM contents include the eight new focused skills and existing three owner skills plus coordinator; reconcile membership only if Task 1 missed a required owner. Keep first-party source custody and explicit provenance. Update package descriptions to the selectable-standard model without claiming future starter implementations are already present. Do not advertise retired Markdown as a new selectable standard; preserve any still-needed legacy capability until Plan 6 removes or relocates it.
- [x] Run `py -3 tools/run.py marketplace --apply` after canonical edits, then the two focused script suites and `py -3 -m pytest -q tests/shipping/test_aom_standard_authority.py`. The normal commit hook performs the complete gate; do not repeat it immediately before or after a passing hooked commit.
- [x] Stage intended source, tests, metadata, and generated projections; commit. Confirm `git show --stat HEAD` contains only Plan 1 scope and `git status --short` is clean. If the builder needs modification, constrain it to a proven isolated closure defect; do not redesign deployment in this plan.
- [x] Obtain fresh whole-change review against this plan and the approved spec. Fix actual findings, regenerate affected output, and repeat focused evidence for changed behavior. Describe v1 bridge behavior and current absence of later starters honestly in the handoff.
- [x] Use completing-planning-artifacts to close only this completed plan after a verified fully reviewable implementation handoff. Retain it through its completing PR if publication is authorized. Keep the roadmap and full spec active for future deliveries. Record actual commits/PRs only after they exist; do not infer publication authorization from this planning request.

**Exit:** Packaged definitions and authority helpers work as an isolated install, existing gate/runtime remain usable, and a reviewer can trace all Plan 1 acceptance claims to current evidence.

## Handoff and later-plan boundaries

All source paths above are canonical worktree paths. The plan intentionally preserves current `.agents/standards/`, old catalog, command JSON, and runtime until later explicit migration. That coexistence is a compatibility bridge, not two interchangeable definitions: the consumer's declared pin decides authority.

Plans 2-7 implement optional deployment assets, checker details, full portable gate, semantic lifecycle, dynamic unslop, Marketplace certification/migration, and rollout closure. Do not mark the complete design implemented after Plan 1. Do not create consumer certifications from this illustrative schema or update a subscription to an uncommitted/self-referential revision.

Execution starts only after human review of this saved plan. No tests, behavior probes, or implementation commands in this document were run while authoring it.
