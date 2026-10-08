# AOM candidate-preserving hook and CI gates

Status: completed-awaiting-retirement.

## Purpose

An agent should be able to attempt a commit cheaply, receive an exact explanation of the first failing check, repair it with a focused command, and retry without paying for unrelated expensive checks. The tracked hook accepts or rejects the candidate supplied by Git. Hosted CI applies equivalent checks and failure criteria to its committed counterpart. Neither gate repairs or stages repository content.

The human confirmed that literal read-only execution is too restrictive for builds and tests. Disposable outputs are allowed; changes to maintained repository files or the intended index are not. This distinction governs the standards, skills, optional starter assets, and the Marketplace's own integration.

The standard defines the shared hook/CI contract, not every repository-specific infrastructure requirement. It does not require submodule support. Repositories that use submodules include their treatment in their own gate and self-certification; the optional starter does not prescribe that behavior. This Marketplace repository does not use submodules, so this implementation adds no submodule-specific handling or tests.

## Existing behavior and ownership

Canonical source is `skills/tracked-repo-hooks/` and `skills/command-bus/`. The hook standard currently permits normalization and generation inside the candidate. Its optional Bash starter runs an apply callback locally, stages its results, then runs the check callback; hosted mode runs only the check callback. The command-bus standard already distinguishes check from apply and permits disposable test/build outputs during checks.

The Marketplace's `githooks/pre-commit` separately runs declared apply commands, stages mechanical changes, and runs declared checks. `.agents/contracts/repo-standards-commands.json` currently chooses `ci --check --diagnostics`, which collects independent failures. `tools/run.py` already supports fail-fast `ci --check`, but places some cheap validators after test suites and emits repair hints whose executability and scope need inspection.

Consumers own their copied implementations and immutable standard subscriptions. Installed plugin caches and generated packages are not source authority. Changes to the current canonical definition do not silently upgrade consumers pinned to older commits.

## Gate contract

The hook and hosted CI execute the same complete set of required checks, in a dependency-safe order that prioritizes cheap checks before expensive ones. The repository owns the order and documents any dependency requiring an expensive step before a cheaper check. Failure stops the gate before later checks or their expensive setup starts. Aggregate diagnostics may remain an explicit developer command, but are not the canonical hook/CI gate.

The gate validates the original candidate. It never invokes repair/apply commands, corrects authored or committed generated files, stages paths, or leaves a changed intended index. Normalization, format fixes, lint fixes, and maintained generation are explicit preparation operations outside the gate. Their check counterparts report drift and fail. A command named build or lint is classified by its side effects, not by its name.

The gate may create disposable test reports, caches, temporary generation comparisons, and build outputs derived from the candidate. Such outputs must be isolated or declared disposable and must not overwrite maintained files, provide stale evidence, or become staged content. Git ignore rules alone do not establish that a file is disposable. A maintained ignored file remains protected. A generated file committed to the repository remains maintained and is checked for freshness without being corrected.

Local execution sees exactly the staged candidate, including the temporary index Git supplies for path-limited commits. Hosted execution sees the proposed commit. Configuration, adapters, and checked inputs come from that candidate. Unstaged and untracked authored work cannot supply a repair that conceals staged failure. Ignored derived inputs must be rebuilt in disposable locations from candidate inputs or excluded from gate decisions. Both platforms fail clearly on missing required prerequisites.

Temporary candidate materialization and restoration are allowed implementation mechanics. They must preserve the original staged, unstaged, untracked, and protected ignored state on both success and failure. They are not permission to transform the candidate. A gate implementation that changes maintained content or the index is rejected even when its checks otherwise pass. Mutation detection must run on failing child exits as well as successful exits; restoration errors also reject the commit and provide recovery information.

## Failure and repair contract

Each failure identifies the named check, its underlying command or prerequisite, the diagnostic explaining the rejection, and an exact focused recheck invocation. Preserve meaningful child output and nonzero status; do not replace a specific cause with an opaque full-gate failure.

When a mechanical repair exists, report an exact executable invocation for the owning repair target. It must use the repository's actual entrypoint, supported mode, and relevant scope arguments. Do not default to a full `ci --apply` sweep when a format, lint, or generation target can repair the specific failure. When human or authored code changes are required, say so and provide the focused diagnostic/reproduction command; do not invent an automatic fix.

With command-bus adoption, every gate check and available mechanical repair is discoverable through the repository-owned bus. Target help declares its purpose, prerequisites, meaningful modes, side effects, and accepted scope arguments. Mutation requires an explicit supported apply mode. Check mode may create disposable outputs under the gate's candidate-preservation rules. Focused targets remain independently callable without running unrelated expensive dependencies. The gate invokes checks only.

The standards remain independently selectable. Hook adoption does not silently adopt command-bus or require an AOM-specific registry, ABI, command JSON, Python runtime, or starter inventory. A repository without an adopted bus still provides exact check and repair commands through its existing tooling. A repository adopting both standards routes those operations through its bus.

Repair occurs after rejection, outside the hook. The agent runs the reported preparation command, inspects and stages the intended changes, optionally runs the focused recheck, then retries the commit. A successful focused recheck does not replace the final complete hook or hosted gate.

## Source and implementation scope

Update the tracked-hook and command-bus definitions and skill guidance together so mutation ownership, disposable output handling, failure order, and diagnostics agree. Update adoption scenarios to assess the changed choices without exact wording assertions. The text normalizer remains an optional preparation utility with check/apply modes; its presence does not authorize hook-side correction.

Adapt the optional Bash hook to a check-only repository adapter seam in both local and hosted modes. Remove the apply callback and automatic staging path. Preserve candidate-safe loading, temporary-index support, fail-closed missing adapters, hosted checkout validation, executable mode, and restoration protections. The adapter owns the ordered complete gate and check-specific diagnostic/repair guidance; the starter need not add a universal check registry or scheduling engine.

The optional bus target and hosted workflow examples must describe the same candidate-preserving contract and disposable-output allowance. Their sample interfaces remain optional and independently replaceable. The normalizer, hook, workflow, and bus target do not become a mandatory bundle.

Migrate the Marketplace's own hook and declared check command to this contract. Remove hook-side apply/staging, select fail-fast checks, put cheap independent checks before test suites, and expose truthful focused repair/recheck commands through its existing bus. Preserve the complete required Windows/Linux gate, staged input semantics, and hosted CI parity. Do not change unrelated bus targets or make formerly mandatory checks optional to improve speed.

Regenerate shipped packages through `tools/run.py marketplace --apply` after canonical source edits. Maintain the affected repository certification with honest current evidence and source-pin handling. A new subscription pin must reference an existing immutable source commit containing the revised definition; never fabricate a future commit or imply that an old pin incorporates new requirements. Updating other consumer repositories or installed user plugins is outside this slice.

## Verification design

Behavior tests witness rejection of maintained-file or index mutation, preservation of original state on success and failure, staged adapter selection, and Git's temporary-index candidate for path-limited commits. A local rejection must not leave normalized or generated candidate changes behind. Hosted failures must detect mutation as well as report the check failure.

Use observable execution markers to prove that a cheap failed check prevents expensive build/test checks and their setup from executing. Exercise a failing check with meaningful output and status, its exact focused repair invocation where available, and its focused recheck. Do not assert implementation text or add tests that merely mirror target tables.

Positive tests allow disposable build/test outputs while preserving maintained files and the index. Negative cases cover stale ignored derived inputs concealing candidate failure, undeclared/protected files treated as disposable, and missing prerequisites. Local and hosted runs of equivalent candidate content must have equivalent check coverage and failure criteria.

Focused tests belong beside their owning skill assets; Marketplace integration tests belong in the existing repository suite. Reuse meaningful behavior coverage and replace assumptions about apply-before-check rather than preserving obsolete tests. Retain portable Windows/Linux execution and meaningful platform differences only. Run focused behavior proofs, deterministic package checks, and the normal complete tracked hook; use hosted CI for the Linux counterpart. No committed run results or development receipts are added.

## Exclusions and handoff

This change does not reduce complete gate coverage, add automatic hook fixes, add a mandatory AOM runtime/scaffold, migrate other consumers, or change agent no-skip policy. It does not promise that every defect has an automatic repair. It provides the smallest truthful repair or diagnosis lever supported by the repository.

After human review of this specification, the implementation plan resolves the concrete restoration mechanism, existing test owners, exact target ordering, diagnostic plumbing, and publication/pin sequence using live source. Those are implementation choices within the candidate-preservation, fail-fast, and repair contracts above. The completing slice promotes durable rules into canonical skills and standards and follows repository planning-artifact custody.
