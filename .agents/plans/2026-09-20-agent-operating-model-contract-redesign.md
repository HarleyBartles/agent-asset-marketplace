# Agent Operating Model Contract Redesign Implementation Plan

> Status: completed-awaiting-retirement. The implementation and verification evidence remain in this completing PR; retire this plan in the first commit of the next substantive slice.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the operating model's implicit template and presence semantics with explicit consumer-surface contracts, semantic validation, safe convergent apply, confirmed force template deployment, plugin prerequisite diagnostics, and dead skill-link checks.

**Architecture:** A versioned surface manifest declares presence, ownership, seed, validator, apply, and force behavior without implicit defaults. Focused validator modules feed one coordinator that reports failures and warnings, ordinary apply performs only registered preservation-first actions and rechecks convergence, and targeted `--force <surface-id>` deployment requires an additional destructive acknowledgement. Consumer plugin subscriptions remain in `.agents/plugins/marketplace.json`; consumer conformance exceptions live in `.agents/contracts/agent-operating-model.json`; command vectors and generated-output ownership live in `.agents/contracts/repo-standards-commands.json`.

**Tech Stack:** Python 3.12, JSON contracts, Markdown runbooks/playbooks/doctrine, Bash tracked hook, pytest, repository marketplace/index/mesh generators.

**Spec:** `.agents/specs/2026-09-20-agent-operating-model-contract-audit-design.md`

**Execution Strategy:** `subagent-driven-development` — the tasks have explicit producer/consumer interfaces and independent red-green review gates, while final regeneration and the staged-snapshot hook provide whole-branch integration proof.

## Global Constraints

- `agent-operating-model` remains an ordinary plugin whose plugin/bundle manifests own its bundled skill inventory.
- Consumer validation checks required plugin subscriptions and dead runbook/playbook skill links; it never enumerates or repairs a plugin's skills individually.
- Hard prerequisite subscriptions are `agent-operating-model`, `superpowers-plus`, and `repo-worker-pack`.
- Missing `writing-pack` is a visible warning and never blocks commit or hosted CI by itself.
- Governed unslop profiles require an `unslop-plus` subscription.
- Seeds create missing consumer-owned surfaces; they never imply continuing byte identity.
- Ordinary apply preserves consumer customisation, runs only registered safe migrations, and succeeds only after a complete recheck has no failures.
- `--force <surface-id>` deploys the current seed only for explicit targets and requires `--confirm-local-customisations-will-be-overwritten` or equivalent interactive confirmation.
- Hook and hosted CI exercise the same contract on the exact staged candidate tree.
- Consumer-generated indexes belong to consumer generators; never compare them with this marketplace repository's generated indexes.
- Edit canonical plugin sources under `codex-marketplace/plugins/agent-operating-model/`; regenerate plugin and installed projections instead of hand-editing `.agents/skills/`.
- Preserve the existing `.agents/plugins/marketplace.json` subscription representation; redesigning the marketplace catalogue or cross-plugin skill authorship is out of scope.

## Review Focus

- A customized seeded surface gains a new mandatory invariant: safe apply must preserve its prose while either making the registered localized migration or failing with manual guidance. Covered in Task 5 convergence fixtures.
- A repository has only the non-blocking `writing-pack` warning: hook and hosted-parity commands must exit zero while retaining the warning. Covered in Task 3 and Task 7 warning-path tests.
- A skill is referenced conditionally in a playbook and exists through any installed plugin or a declared repo-local skill: the link passes without provider/version reasoning. Covered in Task 6 resolver fixtures.
- A force command names one valid seeded surface and one invalid/unseeded surface: validation must reject the entire request before replacing either file. Covered in Task 5 atomic preflight tests.
- A consumer hook is reorganized but preserves staged-snapshot behavior: semantic hook tests must accept it while rejecting marker-bearing no-op hooks. Covered in Task 7 behavioral fixtures.

---

### Task 1: Freeze the surface audit and explicit manifest schema

**Files:**
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/consumer-surface-audit.md`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/repository-shape-manifest.schema.json`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/surface_contracts.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/repo_standards.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/repository-shape-manifest.json`
- Create: `tests/test_operating_model_surface_contracts.py`
- Modify: `tests/test_workflow_contracts.py`

**Interfaces:**
- Consumes: approved design spec and current version-2 manifest.
- Produces: `SurfaceContract`, `ManifestContract`, `load_manifest(path: Path) -> ManifestContract`, and an explicit version-3 manifest consumed by every later task.

- [ ] **Step 1: Write failing manifest-schema tests**

Add parameterized tests that reject omitted `presence`, `ownership`, `validator`, `apply`, or `force_reset`; a seeded consumer surface using `identity`; a consumer surface using `overwrite`; an unregistered validator; and a forbidden surface without remediation.

```python
@pytest.mark.parametrize("missing", ["presence", "ownership", "validator", "apply", "force_reset"])
def test_surface_contract_rejects_implicit_behavior(tmp_path: Path, missing: str) -> None:
    surface = valid_surface()
    del surface[missing]
    manifest = write_manifest(tmp_path, [surface])
    with pytest.raises(ValueError, match=missing):
        surface_contracts.load_manifest(manifest)


def test_seed_never_implies_identity_validation(tmp_path: Path) -> None:
    surface = valid_surface(seed="templates/example.md", validator="identity")
    with pytest.raises(ValueError, match="consumer-authored.*identity"):
        surface_contracts.load_manifest(write_manifest(tmp_path, [surface]))
```

- [ ] **Step 2: Run the schema tests and witness RED**

Run: `py -3 -m pytest tests/test_operating_model_surface_contracts.py -q`

Expected: FAIL because `surface_contracts.py` and the version-3 schema do not exist.

- [ ] **Step 3: Write the complete current-state audit ledger**

Inventory every current surface named by the spec. For each row record current deployer/checker, practical and desired ownership, mandatory invariants, ordinary apply, force availability, and the identified defect. Include installed projections and consumer indexes only to mark their ownership boundaries; do not pull marketplace generation behavior into consumer conformance.

- [ ] **Step 4: Implement strict manifest loading**

Use frozen dataclasses and finite literal sets. Reject unknown keys so misspellings cannot silently create defaults.

```python
@dataclass(frozen=True)
class SurfaceContract:
    id: str
    path: str
    presence: Literal["required", "optional", "forbidden"]
    ownership: Literal["consumer-authored", "consumer-generated"]
    validator: str
    apply: Literal["create", "create-or-migrate", "manual-remediation", "delegate-generator"]
    force_reset: Literal["confirmed-template-restore", "unavailable"]
    seed: str | None = None
    scaffold: str | None = None
    required_with: str | None = None
```

Register validator and migrator names centrally but bind their callables in later tasks to avoid import cycles.

- [ ] **Step 5: Convert every manifest row explicitly**

Set manifest `version` to `3`. Classify each existing surface using the audit ledger. `completed-artifacts-doctrine` becomes consumer-authored with a seed and semantic validator. The hook becomes consumer-authored with a seed and hook-contract validator. Forbidden completed directories use manual remediation until an authorized safe migration exists. Remove `kind`, `source`, `optional`, and `check_content` only after their behavior is represented explicitly.

- [ ] **Step 6: Bridge the current coordinator to manifest version 3**

Load `ManifestContract` in `repo_standards.py` and adapt each explicit version-3 field to the current check/apply functions without changing their observable behavior yet. This bridge keeps the repository gate green after the schema commit; Tasks 3-5 then replace string findings, identity checks, and unsafe mutation paths behind the same typed contracts.

- [ ] **Step 7: Add architectural anti-regression assertions**

Require the spec's core sentences, the audit reference, manifest schema, and absence of `surface.get("check_content", True)` from canonical coordinator source.

- [ ] **Step 8: Run Task 1 tests GREEN**

Run: `py -3 -m pytest tests/test_operating_model_surface_contracts.py tests/test_workflow_contracts.py -q`

Expected: PASS.

- [ ] **Step 9: Commit the explicit surface model**

```bash
git add codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references \
  codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/surface_contracts.py \
  codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/repo_standards.py \
  tests/test_operating_model_surface_contracts.py tests/test_workflow_contracts.py
git commit -m "feat(operating-model): define explicit consumer surface contracts"
```

### Task 2: Add the consumer conformance and command-output contracts

**Files:**
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/templates/agent-operating-model.json`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/scaffold_operating_model_contract.py`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/scaffold-operating-model-contract.sh`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/scaffold-operating-model-contract.ps1`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/repository-shape-manifest.json`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/repository-shape-standard.md`
- Modify: `.agents/contracts/repo-standards-commands.json`
- Create: `.agents/contracts/agent-operating-model.json`
- Modify: `tests/test_operating_model_surface_contracts.py`
- Modify: `tests/test_repo_standards.py`

**Interfaces:**
- Consumes: `SurfaceContract` and manifest version 3 from Task 1.
- Produces: `.agents/contracts/agent-operating-model.json` schema version 1 and `generated_paths: list[str]` in the command declaration for Task 7.

- [ ] **Step 1: Write failing contract-scaffold tests**

Cover missing-file creation, customized valid content, invalid exception IDs, schema-version rejection, and preservation of an existing contract without force.

```python
def test_operating_model_contract_customized_valid_passes(tmp_path: Path) -> None:
    write_json(tmp_path / ".agents/contracts/agent-operating-model.json", {
        "version": 1,
        "surface_exceptions": [{"id": "marketplace-source-submodule", "reason": "source repository"}],
        "unslop_profile_roots": [".agents/contracts/unslop"],
    })
    assert run_scaffold_check(tmp_path).returncode == 0
```

Add command-declaration tests requiring a list of repository-relative generated pathspecs and rejecting absolute paths, `..`, empty strings, and repository-wide `**`.

- [ ] **Step 2: Run focused tests RED**

Run: `py -3 -m pytest tests/test_operating_model_surface_contracts.py tests/test_repo_standards.py -q`

Expected: FAIL on missing scaffold and generated-output validation.

- [ ] **Step 3: Implement the focused conformance contract scaffold**

The seed contains only version, explicit exception objects, and the canonical unslop profile root. `--check` validates structure and known surface IDs. Normal execution creates a missing file and preserves an existing valid file. Do not implement destructive force behavior in this scaffold; Task 5 centralizes force deployment.

- [ ] **Step 4: Extend command declaration validation**

Change `_check_declared_commands()` to return a typed declaration containing `apply`, `check`, and `generated_paths`. Treat generated path ownership as part of the command boundary used by the hook.

- [ ] **Step 5: Add this repository's two contracts**

Declare its marketplace exception in `.agents/contracts/agent-operating-model.json`. Populate `generated_paths` with the paths currently hard-coded by this repository's hook: `.agents/skills/**`, `**/INDEX.md`, `**/INDEX.json`, `**/.provenance.json`, `.agents/plugins/marketplace.json`, `codex-marketplace/plugin-roots.json`, and `codex-marketplace/manifest.json`.

- [ ] **Step 6: Update standards prose and wrappers**

Document the separation among subscription state, conformance exceptions, runbook mapping, command vectors, and generated-output ownership. Add the new scaffold to `scaffold-all` after marketplace JSON and before hook deployment.

- [ ] **Step 7: Run Task 2 tests GREEN**

Run: `py -3 -m pytest tests/test_operating_model_surface_contracts.py tests/test_repo_standards.py -q`

Expected: PASS.

- [ ] **Step 8: Commit the consumer contracts**

```bash
git add codex-marketplace/plugins/agent-operating-model/skills/repo-shape \
  .agents/contracts/agent-operating-model.json .agents/contracts/repo-standards-commands.json \
  tests/test_operating_model_surface_contracts.py tests/test_repo_standards.py
git commit -m "feat(operating-model): declare consumer conformance and generated outputs"
```

### Task 3: Validate prerequisite plugin subscriptions and severity-aware findings

**Files:**
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/plugin_contracts.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/surface_contracts.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/repo_standards.py`
- Create: `tests/test_operating_model_plugin_contracts.py`
- Modify: `tests/test_repo_standards.py`

**Interfaces:**
- Consumes: consumer marketplace JSON, conformance contract, and `Finding` severity model.
- Produces: `check_plugin_contract(repo_root: Path, config: ConsumerContract) -> list[Finding]` and coordinator exit semantics used by hook/CI tasks.

- [ ] **Step 1: Write failing plugin-contract tests**

Cover hard prerequisites, the writing warning, governed unslop roots, arbitrary additional subscriptions, and no per-skill inventory checks.

```python
def test_missing_writing_pack_warns_without_failure(tmp_path: Path) -> None:
    write_marketplace(tmp_path, installed=["agent-operating-model", "superpowers-plus", "repo-worker-pack"])
    findings = plugin_contracts.check_plugin_contract(tmp_path, default_contract())
    assert [(item.severity, item.code) for item in findings] == [("warning", "missing-writing-pack")]


def test_unslop_profiles_require_unslop_plus(tmp_path: Path) -> None:
    write_marketplace(tmp_path, installed=HARD_PLUGINS)
    write(tmp_path / ".agents/contracts/unslop/repository.md", "# Repository profile\n")
    assert any(item.code == "missing-unslop-plus" and item.severity == "failure" for item in check(tmp_path))
```

- [ ] **Step 2: Run focused tests RED**

Run: `py -3 -m pytest tests/test_operating_model_plugin_contracts.py -q`

Expected: FAIL because the plugin contract and severity model do not exist.

- [ ] **Step 3: Add structured findings**

Define `Finding(severity: Literal["warning", "failure"], code: str, surface: str, message: str, repair: str)`. Replace string-only coordinator findings without changing message order. Check mode exits nonzero only if at least one failure exists.

- [ ] **Step 4: Implement subscription checks**

Read current `policy.installation == "INSTALLED_BY_DEFAULT"` entries from the consumer marketplace file. Fail for missing hard plugins. Warn for missing `writing-pack`. Resolve configured unslop roots and fail when any governed profile exists without `unslop-plus`. Do not enumerate plugin skill contents.

- [ ] **Step 5: Prove warnings are non-blocking end-to-end**

Add a coordinator subprocess fixture containing only the writing warning. Require exit 0, a `WARN:` line, and no `DRIFT:`/failure line.

- [ ] **Step 6: Run Task 3 tests GREEN**

Run: `py -3 -m pytest tests/test_operating_model_plugin_contracts.py tests/test_repo_standards.py -q`

Expected: PASS.

- [ ] **Step 7: Commit plugin prerequisite validation**

```bash
git add codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts \
  tests/test_operating_model_plugin_contracts.py tests/test_repo_standards.py
git commit -m "feat(operating-model): validate prerequisite plugin subscriptions"
```

### Task 4: Replace identity and presence checks with semantic consumer-surface validators

**Files:**
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/document_contracts.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/_agents_md.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/repo_standards.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/scaffold_runbooks.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/scaffold_playbooks.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/scaffold_review.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/scaffold_contributing.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/scaffold_repo_runbook_policy.py`
- Create: `tests/test_operating_model_document_contracts.py`
- Modify: `tests/test_repo_standards.py`

**Interfaces:**
- Consumes: manifest validator IDs and structured findings from Tasks 1 and 3.
- Produces: validator registry `DOCUMENT_VALIDATORS: dict[str, Callable[[Path, Path], list[Finding]]]` and preservation-first create/migrate results consumed by Task 5.

- [ ] **Step 1: Write customized valid and hollow invalid fixtures**

For runbooks, playbooks, root/scoped routers, policy, review, and contribution entrypoints, prove that repository-specific sections and prose pass while missing, empty, comment-only, or fenced mandatory content fails.

```python
def test_customized_runbook_passes_without_matching_seed(tmp_path: Path) -> None:
    path = write_runbook(tmp_path, extra="## Repository-specific release train\n\nBlue/green only.\n")
    assert document_contracts.check_runbook(path, tmp_path) == []


def test_placeholder_required_skills_does_not_pass(tmp_path: Path) -> None:
    path = write_runbook(tmp_path, required_skills="<!-- choose later -->")
    assert any(item.code == "empty-required-skills" for item in check_runbook(path, tmp_path))
```

- [ ] **Step 2: Run focused tests RED**

Run: `py -3 -m pytest tests/test_operating_model_document_contracts.py -q`

Expected: FAIL because focused document validators do not exist.

- [ ] **Step 3: Extract Markdown parsing primitives**

Move live-heading, live-section, link, and placeholder detection into `document_contracts.py`. Preserve fenced-code/comment exclusion. Return focused codes and repairs rather than generic `drift`.

- [ ] **Step 4: Bind validators to manifest IDs**

Replace `_check_surface_content()` and scaffold early-return behavior with the registry. A seed is read only when creating a missing surface or Task 5 force deployment requests it.

- [ ] **Step 5: Make scaffold checks semantic and apply preservation-first**

`--check` invokes the same focused validators as the coordinator. Normal scaffold execution creates missing files and leaves existing files intact unless a registered localized migrator exists. Remove help text that presents ordinary `--force` overwrite as routine scaffold behavior.

- [ ] **Step 6: Prove optional means absent-or-valid**

Add scoped `AGENTS.md` fixtures showing absence passes, valid customized content passes, and present invalid content fails.

- [ ] **Step 7: Run Task 4 tests GREEN**

Run: `py -3 -m pytest tests/test_operating_model_document_contracts.py tests/test_repo_standards.py -q`

Expected: PASS.

- [ ] **Step 8: Commit semantic document contracts**

```bash
git add codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts \
  tests/test_operating_model_document_contracts.py tests/test_repo_standards.py
git commit -m "feat(operating-model): validate consumer documents by contract"
```

### Task 5: Add completed-artifact semantics, convergence, and confirmed force deployment

**Files:**
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/completed_artifact_contract.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/repo_standards.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/templates/completed-artifacts.md`
- Create: `tests/fixtures/operating-model/portfolio-completed-artifacts.md`
- Create: `tests/test_completed_artifact_contract.py`
- Modify: `tests/test_repo_standards.py`

**Interfaces:**
- Consumes: registry and structured findings from Tasks 3-4.
- Produces: `check_completed_artifact_doctrine(path: Path) -> list[Finding]`, convergent apply orchestration, and targeted force deployment CLI.

- [ ] **Step 1: Write failing completed-artifact contract tests**

Use a reduced Portfolio fixture containing plans, specs, roadmaps, checkpoints, and `.agents/image-briefs/`. Require explicit completion or abandonment, reject scratch/rejected-candidate completion, require completion marking before successor retirement, and permit repository-specific paths and evidence.

```python
def test_portfolio_image_brief_extension_passes() -> None:
    findings = check_completed_artifact_doctrine(FIXTURES / "portfolio-completed-artifacts.md")
    assert findings == []


def test_rejected_candidate_does_not_complete_brief(tmp_path: Path) -> None:
    path = write_doctrine(tmp_path, "A rejected candidate completes its brief.")
    assert any(item.code == "invalid-completion-trigger" for item in check(path))
```

- [ ] **Step 2: Write failing apply and force tests**

Cover apply recheck, idempotent second apply, unresolved forbidden paths, customized-file preservation, bare `--force`, mixed valid/invalid force targets, missing acknowledgement, and confirmed replacement of only selected seeded surfaces.

- [ ] **Step 3: Run focused tests RED**

Run: `py -3 -m pytest tests/test_completed_artifact_contract.py tests/test_repo_standards.py -q`

Expected: FAIL on identity checking, false apply success, and absent force preflight.

- [ ] **Step 4: Implement semantic doctrine validation**

Use heading/statement invariants with explicit accepted formulations in tests. Do not require the seed's sentences or artifact list. Diagnostics must identify the missing or contradicted lifecycle invariant.

- [ ] **Step 5: Make apply transactional at the contract level**

Preflight all selected actions, apply registered actions, reload configuration, and rerun the complete check. If any failure remains, exit nonzero and print the remaining findings. A second apply against the converged tree writes nothing.

- [ ] **Step 6: Implement targeted `--force` template deployment**

Parse `--force SURFACE_ID` as a repeatable destructive mode mutually exclusive with `--apply` and `--check`. Resolve every target and seed before writing any file. Require `--confirm-local-customisations-will-be-overwritten` in non-interactive mode; otherwise prompt once with the exact approved warning for the full target list.

- [ ] **Step 7: Remove unsafe scaffold force paths**

Route all template restoration through the coordinator so individual scaffold scripts cannot bypass target validation or confirmation.

- [ ] **Step 8: Run Task 5 tests GREEN**

Run: `py -3 -m pytest tests/test_completed_artifact_contract.py tests/test_repo_standards.py -q`

Expected: PASS.

- [ ] **Step 9: Commit lifecycle and mutation safety**

```bash
git add codex-marketplace/plugins/agent-operating-model/skills/repo-shape \
  tests/fixtures/operating-model tests/test_completed_artifact_contract.py tests/test_repo_standards.py
git commit -m "feat(operating-model): enforce lifecycle and safe template deployment"
```

### Task 6: Validate runbook and playbook skill links without plugin-provider inference

**Files:**
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/skill_link_contract.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/document_contracts.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/repo_standards.py`
- Create: `tests/test_operating_model_skill_links.py`
- Modify: `tests/test_repo_standards.py`

**Interfaces:**
- Consumes: active runbook/playbook documents, `.agents/skills/`, and exact `repo.local_skills` declarations.
- Produces: `check_skill_links(repo_root: Path) -> list[Finding]` with no plugin provenance/version reasoning.

- [ ] **Step 1: Write failing resolution fixtures**

Cover installed skill, declared repo-local skill, dead link, conditional bullet, operational composition mention missing from `Required skills`, placeholder-only section, and multiple-plugin deduplicated installation represented by one installed directory.

```python
def test_installed_skill_reference_resolves_from_visible_namespace(tmp_path: Path) -> None:
    write_skill(tmp_path / ".agents/skills/test-driven-development", "test-driven-development")
    write_playbook(tmp_path, required="- `test-driven-development` — when behavior changes.")
    assert check_skill_links(tmp_path) == []


def test_dead_skill_link_names_document_and_skill(tmp_path: Path) -> None:
    playbook = write_playbook(tmp_path, required="- `missing-skill` — required.")
    finding = only_failure(check_skill_links(tmp_path))
    assert finding.surface == playbook.relative_to(tmp_path).as_posix()
    assert "missing-skill" in finding.message
```

- [ ] **Step 2: Run focused tests RED**

Run: `py -3 -m pytest tests/test_operating_model_skill_links.py -q`

Expected: FAIL because the skill-link validator does not exist.

- [ ] **Step 3: Implement the consumer-visible namespace**

Index installed `.agents/skills/*/SKILL.md` frontmatter names and validate exact repo-local declarations against their directories/frontmatter. Treat one visible installed skill as resolved regardless of how many plugins supplied it. Do not read bundle manifests or compare plugin versions.

- [ ] **Step 4: Parse authoritative required-skill entries**

Accept bullet entries with exact backticked skill names and non-placeholder role/condition text. Scan the Composition section for backticked skill invocations and require them to appear in Required skills; avoid treating paths, states, or commands outside Composition as skills.

- [ ] **Step 5: Run Task 6 tests GREEN**

Run: `py -3 -m pytest tests/test_operating_model_skill_links.py tests/test_operating_model_document_contracts.py tests/test_repo_standards.py -q`

Expected: PASS.

- [ ] **Step 6: Commit dead-link validation**

```bash
git add codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts \
  tests/test_operating_model_skill_links.py tests/test_operating_model_document_contracts.py \
  tests/test_repo_standards.py
git commit -m "feat(operating-model): reject dead workflow skill links"
```

### Task 7: Make the tracked hook behaviorally conformant and consumer-configured

**Files:**
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/templates/pre-commit`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/repo_standards.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/ci-validation-pipeline.md`
- Create: `tests/fixtures/operating-model/custom-pre-commit`
- Modify: `tests/test_repo_standards.py`

**Interfaces:**
- Consumes: typed command declaration and `generated_paths` from Task 2, severity exits from Task 3, and force/apply coordinator semantics from Task 5.
- Produces: a hook template with data-driven generated staging and `_check_hook_contract()` that validates behavior without `actual == template`.

- [ ] **Step 1: Replace exact-identity tests with behavioral fixtures RED**

Add a reorganized customized hook that preserves all required operations and must pass. Retain marker-bearing no-op, reordered apply/check, unsafe shell, branch-hosted, dirty-submodule, wrong-gitlink, unstaged-restoration, and hosted-tree mutation failures.

- [ ] **Step 2: Add generated-path staging tests RED**

Give a consumer declaration one generated output and one unowned apply output. Require the declared output to stage and the unowned output to fail. Add the Review Focus warning-only hook fixture and require a successful commit with visible `WARN:` output.

- [ ] **Step 3: Run hook tests and witness RED**

Run: `py -3 -m pytest tests/test_repo_standards.py -k "hook or generated_paths or writing_pack" -q`

Expected: FAIL because the hook hard-codes marketplace paths and the validator requires exact template identity.

- [ ] **Step 4: Stage declared generated paths safely**

Pass validated pathspec strings from the command JSON to `git add -A -- <pathspec>`. Reject invalid pathspecs in Python before the hook runs. Preserve original-staged-path restaging and unexpected authored-change detection.

- [ ] **Step 5: Implement semantic hook validation**

Remove `_retains_canonical_hook_contract(actual == required)`. Validate required guards, declaration loading, staged-snapshot materialization, submodule checks, apply-before-stage-before-check ordering, restore trap, hosted reconstruction, and final hosted tree comparison using normalized executable statements and integration fixtures.

- [ ] **Step 6: Update hook/CI doctrine**

State that the template is a seed, list mandatory behavior, and describe consumer customization boundaries and generated-output declaration.

- [ ] **Step 7: Run Task 7 tests GREEN**

Run: `py -3 -m pytest tests/test_repo_standards.py -k "hook or generated_paths or writing_pack" -q`

Expected: PASS.

- [ ] **Step 8: Commit behaviorally validated parity**

```bash
git add codex-marketplace/plugins/agent-operating-model/skills/repo-shape/templates/pre-commit \
  codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/repo_standards.py \
  codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/ci-validation-pipeline.md \
  tests/fixtures/operating-model/custom-pre-commit tests/test_repo_standards.py
git commit -m "feat(operating-model): validate hook behavior and generated ownership"
```

### Task 8: Align plugin skills, documentation, wrappers, and migration diagnostics

**Files:**
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/SKILL.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-standards/SKILL.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-composition/SKILL.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/tracked-repo-hooks/SKILL.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-agent-assets/SKILL.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/README.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/repository-runbook-standard.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/repository-shape-standard.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-standards/scripts/repo_standards.py`
- Modify: `tests/test_workflow_contracts.py`
- Modify: `tests/test_operating_model_surface_contracts.py`

**Interfaces:**
- Consumes: final CLI, surface, subscription, skill-link, and hook contracts from Tasks 1-7.
- Produces: one consistent human-facing operating model and a read-only migration audit route for existing consumers.

- [ ] **Step 1: Write failing documentation and legacy-route assertions**

Require every owning skill to distinguish seeds from contracts, plugin prerequisites from per-skill installation, warnings from failures, and apply from force deployment. Reject instructions that say existing scaffolded files must match templates or that plugin-bundled skills must be separately installed.

- [ ] **Step 2: Run workflow contracts RED**

Run: `py -3 -m pytest tests/test_workflow_contracts.py tests/test_operating_model_surface_contracts.py -q`

Expected: FAIL on obsolete force, identity, and installation wording.

- [ ] **Step 3: Update canonical capability guidance**

Make `repo-shape` the implementation owner; keep `repo-standards` as a thin routing/compatibility entrypoint with an explicit eventual retirement note rather than duplicate behavior. Update composition, hook, and agent-asset skills to point at their focused contracts.

- [ ] **Step 4: Add read-only migration audit output**

Document and test `repo-standards --check` as the migration audit: it reports schema upgrades, missing contracts, deprecated fields, unsafe customizations, and force-reset availability without mutating. Do not add a second audit command unless a distinct behavior is required.

- [ ] **Step 5: Remove stale vocabulary and duplicated inventories**

Search canonical operating-model source for `check_content`, byte-identical consumer prose, generic `drift` where a contract code exists, per-skill plugin installation lists, and ordinary scaffold overwrite guidance. Retain identity language only for marketplace/package projections outside consumer surface conformance.

- [ ] **Step 6: Run Task 8 tests GREEN**

Run: `py -3 -m pytest tests/test_workflow_contracts.py tests/test_operating_model_surface_contracts.py -q`

Expected: PASS.

- [ ] **Step 7: Commit the durable operating-model explanation**

```bash
git add codex-marketplace/plugins/agent-operating-model tests/test_workflow_contracts.py \
  tests/test_operating_model_surface_contracts.py
git commit -m "docs(operating-model): codify consumer ownership and conformance"
```

### Task 9: Regenerate projections, run the complete gate, review, and publish

**Files:**
- Regenerate: `codex-marketplace/plugins/agent-operating-model/references/bundle-manifest.json`
- Regenerate: `codex-marketplace/manifest.json`
- Regenerate: `.agents/skills/`
- Regenerate: repository indexes and mesh
- Modify: `.agents/plans/2026-09-20-agent-operating-model-contract-redesign.md`
- Publish: Draft PR from `codex/operating-model-contract-audit` to `main`

**Interfaces:**
- Consumes: all implementation commits from Tasks 1-8.
- Produces: converged canonical/generated state, full validation evidence, completed planning lifecycle, and GitHub-visible Draft PR proof.

- [ ] **Step 1: Regenerate canonical marketplace projections**

Run: `py -3 tools/run.py marketplace --apply`

Run: `py -3 tools/run.py installed-skills --apply`

Run: `py -3 tools/run.py mesh --apply`

Expected: canonical plugin source, bundle manifests, installed projections, repo indexes, and mesh converge.

- [ ] **Step 2: Run the complete focused regression set**

Run:

```powershell
py -3 -m pytest `
  tests/test_operating_model_surface_contracts.py `
  tests/test_operating_model_plugin_contracts.py `
  tests/test_operating_model_document_contracts.py `
  tests/test_completed_artifact_contract.py `
  tests/test_operating_model_skill_links.py `
  tests/test_repo_standards.py `
  tests/test_workflow_contracts.py -q
```

Expected: PASS.

- [ ] **Step 3: Run the approved anti-regression residue scan**

Run:

```powershell
rg -n 'check_content|actual == required|use --force to overwrite|byte comparison|byte-identical' `
  codex-marketplace/plugins/agent-operating-model tests
```

Expected: no active consumer-surface identity or unsafe ordinary-force guidance; only deliberate negative assertions or marketplace-package identity language.

- [ ] **Step 4: Review the whole branch against the spec and audit ledger**

Verify every audit row has a final validator/apply/reset disposition; every acceptance criterion maps to passing evidence; no consumer fixture depends on this marketplace's generated indexes; warnings do not block; and no plugin skill inventory is duplicated as consumer installation policy.

- [ ] **Step 5: Complete the planning-artifact lifecycle**

Promote any enduring implementation detail missing from canonical doctrine or references, mark this plan `completed-awaiting-retirement`, retain the approved design spec and plan in the completing PR, and regenerate the mesh.

- [ ] **Step 6: Commit through the tracked hook**

```bash
git add --all
git commit -m "chore(operating-model): finalize contract-first redesign"
```

Expected: the tracked hook materializes the staged tree, runs `ci --apply`, stages declared generated outputs, runs `ci --check --diagnostics`, preserves warning severity, and reports `0 FAIL`.

- [ ] **Step 7: Push and open a Draft PR**

Push `codex/operating-model-contract-audit`, open a Draft PR into `main`, and include the consumer-surface audit, migration impact, focused evidence, complete hook evidence, and explicit note that Portfolio remains blocked until it advances its marketplace pin after this PR lands.

- [ ] **Step 8: Verify publication proof**

Verify the PR URL, base `main`, exact head SHA, Draft state, and hosted checks for that SHA. Attach the PR to the Codex task. Do not mark Ready or merge without the human-owned action.
