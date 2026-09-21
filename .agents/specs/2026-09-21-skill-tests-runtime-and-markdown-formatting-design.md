# Skill Tests, Helper Runtime, and Markdown Formatting Design

> **Status:** Approved for planning on 2026-09-21. Repository-local foundations are implemented in draft PR #328; the portable Markdown capability will complete that PR.

## Problem

Three operating-model concerns had accumulated inconsistent or fragile local treatment.

First, skill-owned tests lacked a defined custody lane. Some maintainer verification sat under `assets/` or directly at a skill root, which made tests look like behavioural inputs to ordinary skill invocation. Second, Bash workflow helpers assumed a single Python launcher spelling and did not prove that a resolved Bash belonged to the same environment as the agent. Third, Markdown prose used inconsistent wrapping and had no cheap repository-wide normalization path. The local formatter implementation now solves the immediate inconsistency, but its reusable behaviour still lives in this repository's command runner rather than in the `agent-operating-model` capability consumers inherit.

## Goal

Make the completed maintenance work explicit and durable, then turn the Markdown formatter into a portable, explicitly adopted operating-model capability. Consumer repositories should share implementation and formatter versions while retaining authority over dependency integration, exclusions, command composition, adoption, and the later decision to enforce the policy through a repository-wide normalization migration.

## Current PR boundary

Draft PR #328 owns the following repository changes:

- Define skill-root `tests/` as the marketplace's maintainer-verification lane.
- State the governing principle that skills are code and code ships with tests, while neither code nor skills ship test results.
- Move existing misplaced skill test material into `tests/` without reclassifying behavioural references or runtime assets.
- Make the executing-plan helpers resolve Python through a portable fallback ladder rather than assuming one launcher spelling.
- Require helpers to use a Bash from the same working environment as the agent instead of silently crossing into WSL or another filesystem/runtime environment.
- Remove the stale implication that local skill names require a prefix.
- Add pinned `mdformat`, GFM, and YAML-frontmatter support; normalize eligible tracked Markdown without arbitrary-width prose wrapping; and integrate check/apply behaviour into the local lint command.
- Preserve byte-governed authority evidence and the unrendered skill scaffold as explicit local exclusions.
- Make generated index Markdown formatter-stable so generation and formatting converge.

The receiving-code-review deeper-smell behaviour and its blinded RED/GREEN fixture are expressly excluded from this PR and remain specified in `2026-09-21-receiving-code-review-deeper-smell-and-skill-tests-design.md` for a fresh follow-up PR.

## Skill-test custody design

`.agents/doctrine/skill-standards-policy.md` defines `tests/` at a skill root as an optional maintainer-facing lane for automated tests, evaluation scenarios, complete lightweight fixtures, materialization helpers, rubrics, stable prompts, and expected results. It ships with canonical and installed skill directories but is not part of the skill's behavioural interface. Ordinary invocation must not require or direct an agent to load it.

Transient transcripts, generated repositories, score folders, caches, and other run results remain off-repo. `assets/` remains for resources used during ordinary skill execution, `references/` for on-demand behavioural knowledge, and `scripts/` for runtime capability code. Repository-root `tests/pressure/` continues to own shared campaign orchestration; a particular skill's portable test inputs belong to that skill.

Existing test material moves by meaning, not filename. Runtime decision guidance, worked examples, golden questions, and operational scenarios remain behavioural resources when they are used by an invoked skill.

## Helper-runtime design

Bash helpers resolve a concrete Python executable through a tested preference ladder and invoke that executable explicitly. They do not depend on `py` being bound inside Bash and do not stop after one brittle launcher attempt.

The caller remains responsible for knowing that the invoked Bash is in the same environment as the agent's working repository. A bare `bash` that resolves into WSL from a Windows checkout is not equivalent merely because it can execute shell syntax: drive paths, installed tools, credentials, environment variables, and filesystem state may differ. The helper guard must therefore fail with a useful diagnosis when the repository path cannot be represented in the resolved Bash environment.

## Repository-local Markdown foundation

The repository uses pinned `mdformat`, `mdformat-gfm`, and `mdformat-frontmatter` dependencies. `.mdformat.toml` disables prose wrapping, selects LF output, enables validation, and activates the GFM and frontmatter extensions.

The lint command enumerates eligible tracked Markdown through Git and invokes the formatter in bounded command batches. Check mode rejects formatting drift; apply mode normalizes it. Frontmatter tests compare the parsed YAML mapping before and after formatting rather than checking delimiters alone. Local exclusions protect byte-governed authority evidence and the invalid-until-materialized skill scaffold template.

The index generator emits formatter-normal Markdown directly. Generators and formatters must converge in one pass; a generated file that is immediately changed by the formatter is a producer defect, not a reason to exempt generated Markdown wholesale.

## Portable Markdown capability

### Source custody

The reusable behaviour should live in canonical `agent-operating-model` source, not remain embedded in each consumer's `tools/run.py`. The proposed shape is a focused `markdown-formatting` skill containing a small Python command and its own tests. Marketplace generation projects that complete skill into consumer-visible installed skills.

### Behavioural interface

The portable command should:

- expose explicit `--check` and `--apply` modes;
- enumerate tracked Markdown through Git rather than walking arbitrary untracked content;
- invoke the active Python interpreter's `mdformat` module in command-length-safe batches;
- preserve YAML frontmatter through the configured extension and fail clearly when required formatter modules are unavailable;
- read consumer-owned exclusions from a stable repository contract;
- expose a bounded producer-validation interface for a generator to check the Markdown outputs it owns with the same formatter configuration and pinned toolchain;
- produce deterministic, concise diagnostics; and
- remain safe in staged-snapshot hook execution.

The command owns mechanics, not consumer policy. It must not embed this marketplace repository's authority paths, scaffold exceptions, or command-bus layout. Formatter pins belong to the skill-owned requirements file rather than command code or consumer policy.

### Consumer-owned contract

Each consumer owns whether the capability is adopted or enforced, how the skill-owned dependency pins enter its environment, which tracked Markdown is excluded, and how check/apply are composed into its canonical repository commands after enforcement. Its policy lives at `.agents/contracts/markdown-formatting.json`, alongside the repository's other operating-model contracts. That contract records the surface state and exclusions as structured file or tree entries. Every exclusion must identify one explicit repository-relative file or directory tree and give a non-empty reason explaining the exceptional custody that prevents normal formatting. Arbitrary globs are not supported. The portable implementation owns validation and interpretation of that contract; consumer-specific Python filtering code is not required.

`.mdformat.toml` remains the formatter's native configuration surface for rendering behaviour such as wrapping, extensions, validation, and line endings. It does not carry repository custody policy or explain exclusions. Standards validation treats the native configuration and the consumer contract as separate required parts of the enabled surface.

The named surface enforces one core formatter policy: prose is not hard-wrapped, output uses LF line endings, formatter validation remains enabled, and the GFM and YAML-frontmatter extensions are active. Consumers may add supported settings only when they do not weaken or contradict those invariants. A repository that requires different core Markdown semantics must not claim conformance to this named surface.

Exclusions are exceptional custody claims, not formatting preferences. Before adding one, the preferred remedy is to make the file or producer formatter-compliant so normal formatting can include it. An exclusion is justified only when the identified file or tree has an independently established reason that its Markdown bytes must not change, such as externally governed source evidence or a deliberately invalid-until-materialized template.

The contract must distinguish that custody from convenient formatter avoidance. Missing or blank reasons, unsupported entry kinds, paths outside the repository, file entries that are not tracked Markdown, and tree entries containing no tracked Markdown are hard contract failures in both check and apply modes. Exclusions describe files that presently exist under exceptional custody; they cannot reserve hypothetical future territory or remain after their final tracked Markdown match disappears. Diagnostics must identify the invalid or unmatched entry and the contract that owns it.

### Dependency boundary

The portable `markdown-formatting` skill owns and ships a requirements file with exact pins for `mdformat`, its GFM extension, and its YAML-frontmatter extension. Those pins are part of the capability version: consumers do not select alternative formatter versions for the same named surface.

The operating model does not silently install packages or assume every consumer uses this repository's dependency-file layout. Adoption integrates the skill-owned requirements into the consumer's chosen environment or installation workflow and then proves the command with that interpreter. Runtime validation checks the installed package set and versions and fails clearly when they are missing or differ from the skill-owned pins. Network-backed ephemeral execution is not the normal hook path.

### Repo-shape adoption

`repo-shape` should offer an explicit adoption path that can scaffold the formatter configuration, the consumer exclusion contract, code-style guidance, and the command wiring appropriate to that repository. Refreshing or upgrading `agent-operating-model` must not silently enable formatting or rewrite a consumer repository.

Rollout has two explicit states and two separate human decisions:

1. **Adopted:** the named surface, skill-owned dependencies, formatter configuration, exclusion contract, code-style guidance, and callable formatter command are present and valid. Adoption does not add formatter apply/check to the repository gate, reformat Markdown, or make formatting drift binding.
2. **Enforced:** a separate authorized transition runs apply mode across every eligible tracked Markdown file, exposes that repository-wide migration as a reviewable diff, and enables check mode in the canonical local hook and hosted validation path.

The enforcement transition must not claim success unless normalization completes and the resulting tree passes formatter check mode. The migration baseline is committed with the enabling change; enforcement cannot point at an unformatted repository and defer cleanup. Later plugin refreshes update the portable implementation without re-authorizing adoption, enforcement, or new consumer policy.

The consumer contract records the state as `adopted` or `enforced`. Standards validation requires the configuration, exclusions, pinned toolchain, and callable formatter command in both states. In `enforced`, it additionally requires formatter apply/check composition in the consumer's canonical repository command declaration and hosted-equivalent validation path. Moving back from `enforced` to `adopted` is a policy change, not an automatic recovery action.

### Named repo-standard surface

Markdown formatting is an optional named repo-standard surface. A consumer enables it explicitly through the repository's standards declaration; `repo-shape` can then scaffold its formatter configuration, exclusion contract, code-style guidance, dependency instructions, and command composition. Standards validation verifies that the enabled surface is complete and internally consistent.

The surface remains opt-in. Installing or refreshing `agent-operating-model` makes the capability available but does not adopt it, integrate its dependency pins, rewrite Markdown, or change the consumer's command declaration. In both states, missing configuration, invalid exclusions, an unavailable or mismatched formatter dependency, or a non-callable formatter command are contract failures. Missing canonical apply/check composition is an additional failure only in `enforced` state.

### Generated Markdown and no-churn

Every tracked Markdown file is eligible by default, including generated Markdown. Being generated is not exceptional custody and cannot justify an exclusion. During the initial enforcement migration, apply mode may normalize existing generated files along with the rest of the repository; after that baseline, their producers own continued compliance.

A generator that emits Markdown is bound by the same core formatter policy and pinned toolchain as authored Markdown. Before reporting success, it must explicitly run the shared formatter in check mode against the Markdown outputs it owns. If that check would change an output, the generator fails and the producer is repaired. The repository-wide formatter gate must not serve as a routine cleanup stage for generator output.

Generator validation must not mutate output silently. Focused tests prove that generation followed immediately by formatter check is clean, and that a second generator run produces no formatting diff. Repository-wide check mode remains the final backstop for a missed or incorrectly declared producer output.

## Source and generated surfaces

Authored portable changes belong under `codex-marketplace/plugins/agent-operating-model/skills/` and the owning repo-shape contracts or templates. Repository-local doctrine, dependency integration, exclusions, surface state, and command wiring remain consumer-authored inputs. Installed `.agents/skills/` trees, manifests, indexes, and mesh files remain generated outputs and are never edited as authority.

## Validation

The completed repository-local work is covered by contract tests for test custody, projection preservation, helper runtime resolution, tracked Markdown selection, check/apply invocation, frontmatter semantic round-tripping, explicit exclusions, generator convergence, authority preservation, and the repository's hooked apply/check gate.

The portable capability will additionally require tests against neutral consumer fixtures covering tracked versus untracked files, authored and generated Markdown, frontmatter, GFM, exclusion validation, missing or mismatched dependencies, batching, staged-snapshot execution, adopted/enforced state transitions, initial migration, idempotence, producer-scoped validation, generator no-churn, and installation/projection from canonical `agent-operating-model` source.

## Failure handling

- Fail without mutation when formatter dependencies or configuration are invalid.
- Fail closed when a contract path escapes the repository.
- Preserve original files when formatter validation fails.
- Treat a generator/formatter oscillation as a producer-contract failure.
- Reject generator success when its owned Markdown outputs fail the shared formatter check.
- Keep a consumer's existing command and policy surfaces unchanged unless adoption was explicitly requested.

## Non-goals

- Enabling Markdown formatting automatically when a plugin is refreshed.
- Imposing this marketplace repository's exclusions on consumers.
- Choosing a consumer's dependency manager.
- Installing formatter dependencies dynamically during a commit hook.
- Reformatting byte-governed source evidence without explicit custody authority.
- Combining the receiving-code-review deeper-smell behaviour into this PR.

## Planning handoff

Planning should separate canonical skill implementation, the optional named repo-standard surface and its `repo-shape` adoption support, neutral consumer-fixture proof, this repository's migration from local runner code to the portable command, generated refresh, and final hooked validation.
