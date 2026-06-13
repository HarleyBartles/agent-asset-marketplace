# Skill Quality Gate

Use this checklist to review a skill before package handoff. The goal is not a score. The goal is to decide whether the
skill should pass, be repaired by GPT, be blocked for Harley input, or be rejected before handoff.

## Binding source

`skill-creator` is the binding source for skill structure and authorship quality. Apply its guidance first:

- frontmatter has only `name` and `description`;
- `description` carries activation information: what the skill does, when to use it, and likely trigger keywords;
- `SKILL.md` is a compact control plane, not a knowledge dump;
- references hold optional detail and have explicit load triggers;
- scripts exist only when deterministic execution materially improves reliability;
- assets are output materials, not reasoning text;
- example scaffold files from init templates are removed unless genuinely needed;
- existing-skill updates preserve full skill structure and return a complete package.

## Decision lenses

### 1. Trigger quality

Fail or repair when the description is vague, missing likely user terms, missing mandatory triggers, or relies on a
body section called `when to use` to activate the skill. The agent sees descriptions before bodies.

### 1a. Semantic discovery gate

Treat the frontmatter description as a fit-for-purpose contract, not a style field. The description must be good
enough that, if it were pasted in isolation, a reviewer would not need to say `not bad, but I would make it better`.
It must name the skill's actual ownership boundary, highest-risk trigger contexts, and decisive action.

Return `repair_required` when the description:

- is directionally true but too broad, such as claiming the skill owns QA when it only gates mutation authority;
- lists adjacent workflow contexts without saying the decision the skill owns inside those contexts;
- omits the failure mode that motivated the skill or the decisive rule that prevents it;
- cannot explain when the skill should be discovered before reading the body;
- would pass only because the body later repairs or clarifies the discovery contract.

The semantic test is: `Could another agent choose this skill at the right time from this description alone, and avoid
choosing it for the wrong adjacent task?` If not, repair the description before handoff.

Description length is not governed by an arbitrary character-count ceiling. `skill-creator` is the binding source: it
says the description is the initial discovery surface and to aim for about 100 words. Treat that as cognitive-load
guidance, not a hard limit. A description should be as short as possible while still carrying the skill's ownership,
highest-signal triggers, and adjacent-skill boundary. Return `repair_required` for descriptions that are vague,
overloaded, procedural, body-like, repetitive, or hard to scan. Do not repair merely because the description exceeds
120 characters, 350 characters, or another local style threshold when the extra text is discovery-critical and still
cognitively manageable.

Examples:

- Weak: `gate image mutation; use for visual plans, prompts, qa, critique, and image-call authorization.`
- Better: `gate image generation and editing; use before visual planning, prompt drafting, qa, critique, or any image
  tool call to decide whether the latest user turn authorizes visible mutation.`

The better form includes the contexts, but also states the owned decision: latest-turn mutation authorization. It does
not imply the skill owns visual planning, prompt drafting, or QA quality itself.


### 1b. Mutation-tool authorization gate

For any skill that controls a visible mutation tool, file write, repo mutation,
email send, calendar change, image generation, or other costly/irreversible
operation, validate that the skill uses a positive proof gate rather than implicit
workflow authority.

Return `repair_required` when such a skill:

- lets readiness, next-step sequence, prior approval, active workflow state, QA
  output, repair packets, or likely intent substitute for current-turn authority;
- relies mainly on watchword blacklists rather than requiring positive proof;
- does not require exact current-message evidence before the tool call;
- cannot answer `what proof did you use?` with the quoted words that authorized
  the mutation;
- allows ambiguous instructions to mutate instead of stopping or asking for
  confirmation.

For image-generation skills, require the quote-or-no-call pattern: before any
image tool call, the skill must require a proof object containing non-empty exact
`quoted_authorizing_words` from the latest user message, a requested mutation type,
a concrete target, and a non-empty prompt or edit contract. If the quote is empty
or only planning/correction/QA language, the decision must be `not_authorized`.


### 1c. Image-credit stewardship gate

For visual-production skills, validate the Adventures #55 resource-discipline invariant when the skill can influence
image generation, image editing, prompt boards, storyboards, QA, repair planning, contact sheets, asset-sheet
compilation, template assembly, package review, or visual preproduction.

The invariant is: image-generation credits are scarce production capacity; deterministic workflows exist to reduce
failed image calls and conserve those credits; calling image generation during deterministic work defeats the purpose of
those workflows and can block visual preproduction, preprod-ready work, deck-ready work, and production until credits
refresh.

Return `repair_required` when a visual-production skill:

- collapses deterministic/no-credit work into image generation or generative editing;
- treats prompt boards, storyboards, QA, repair packets, contact sheets, asset-sheet compilation, template work,
  package validation, repo comments, policy discussion, or skill work as image-generation contexts;
- implies that an accepted prompt board, QA failure, repair plan, active workflow, prior authorization, or `continue`
  is enough to spend an image credit;
- lacks operation-class separation such as `deterministic_no_credit`, `non_credit_pixel_work`, and
  `credit_spending_mutation` when the skill sits near the image-call boundary;
- omits the credit-scarcity/resource-stewardship reason for its image-generation constraints;
- uses a phrase blacklist as the primary mechanism instead of functional classification and positive proof;
- says or implies that contact sheets, prompt boards, deterministic compiles, or QA should call image generation;
- lacks a deterministic route or adjacent-skill route for no-credit work that it mentions;
- does not stop after QA/repair planning and wait for a separate current-turn generation/edit request;
- weakens legitimate image generation at the proper visual-mutation stage instead of preserving it with readiness and
  credit-spend justification.

A passable visual-production skill should make the operation class clear before tool choice. It should protect
image-generation credits while preserving legitimate generation, regeneration, or generative editing when the current
user turn explicitly requests new or changed pixels, deterministic preparation is complete or waived, no deterministic
route satisfies the request, and the spend advances the production boundary.

Specific regression pattern to catch: a skill that lists `make the contact sheet`, asset-sheet compilation, QA, prompt
board creation, or package review as generation-mode work must be repaired before handoff.

### 2. Knowledge delta

Keep specific workflow knowledge, route cues, tradeoffs, edge cases, and anti-patterns. Remove generic tutorials,
basic definitions, broad best practices, and explanations ChatGPT already knows unless they are very short activation
reminders.

### 3. Top-level structure

A spec-compliant `SKILL.md` should make purpose, use/non-use, composition, and quick workflow easy to find near the
top. Do not bury governing routing rules after long detail.

### 4. Progressive disclosure

References must have explicit load triggers in the workflow. If a fragile branch needs a reference, say when it must be
read. Do not list references passively and hope the assistant chooses them.

### 4.1 Bounded skill-read and wrong-wrapper gate

Validate that the skill cannot send GPT into broad skill-reading loops after the controlling skill for the task has already been read. A skill that composes with other skills or references project wrappers must include a concrete stop rule and project-compatibility gate.

Return `repair_required` when a skill:

- says to read `relevant`, `related`, `adjacent`, or `project` skills without naming the unresolved decision that justifies each read;
- lacks a rule to stop reading skills once the current task route is classified and the controlling skill surfaces have been read;
- treats safety, caution, prior workflow memory, connector presence, or broad project context as enough reason to load more skills;
- permits loading project-specific wrapper skills whose project does not match the active task;
- lets a generic report, GitHub verification, or validation task drift into continuity-ingress, dispatch, artifact, image, or wrong-project skills without a current-task trigger;
- does not require a concrete internal classification before additional skill reads, such as `missing_decision`, `already_read_owner`, `candidate_owner`, and `project_compatibility`;
- omits a hard stop for user corrections such as `stop reading skills` or `that skill is unrelated`.

A passable routing or reporting skill should teach: read the smallest set of controlling surfaces, act from them, and load another skill only when a named unresolved decision is outside the already-read owner and the candidate skill directly owns it. Wrong-project wrapper skills are not fallbacks; they are noise.

### 4a. Deterministic execution, evidence receipts, and read-loop gate

For skills with scripts, CLIs, templates, schemas, or deterministic builders, validate that normal execution does not
require inspecting implementation files. A script-backed skill must expose a compact execution recipe in `SKILL.md` or a
directly linked reference. The recipe must name the minimum resources to read, the exact command shape, the expected
input artifact shape, the expected output artifact, and the post-run verification step.

Return `repair_required` when a skill:

- tells the assistant to use a script but does not provide a short command recipe outside the script source;
- makes script source files feel like planning doctrine rather than executable implementation;
- requires reading long scripts to discover ordinary input JSON, CLI arguments, or output paths;
- spreads the same operating contract across `SKILL.md`, references, and scripts without saying which surface is
  authoritative for normal use;
- lacks a hard stop that forbids repeated script/resource rereads after the contract has been read once;
- lacks a debug-only rule for script inspection, such as `read scripts only after execution fails or when editing the
  script itself`;
- has multiple adjacent references that can be reread in circles without advancing to execution;
- gives enough detail to know that a deterministic run is needed but not enough detail to run it confidently.

A passable deterministic skill should let the assistant proceed like this: read `SKILL.md`, read at most one named contract/reference if required, write the declared input artifact, run the declared command, inspect the exact output, write or consume any required machine evidence receipt, and stop. If uncertainty remains, the next action should be to run the smallest valid input and debug any real failure,
not to reread scripts or resources.

### 4a.1 Script architecture and efficiency gate

For any skill that creates or changes files under `scripts/`, validate that the scripts are architected for normal agent use rather than for agent improvisation. The authored skill must expose script purpose, lane ownership, normal command shape, expected inputs, expected outputs or receipts, and debug-only source-inspection rules outside script source.

Return `repair_required` when a script-backed skill:

- adds scripts but does not document the normal execution route in `SKILL.md` or a directly linked reference;
- requires agents to read implementation source to discover CLI arguments, input schema, output paths, or validation rules;
- carries multiple scripts without a lane map or wrapper/substep ownership explanation;
- performs recursive tree scanning without bounded skip rules for output, cache, package, hidden, and dependency directories;
- reads arbitrary files without size bounds or text/binary classification;
- shells out or runs subprocesses without explicit timeout and failure receipt behavior;
- duplicates expensive validation or packaging steps without explaining why;
- creates generated bytecode, cache, dist, or package output inside the staged skill root during normal execution;
- produces artifacts without machine-readable evidence when those artifacts will later be handed off or trusted.

A passable script-backed skill should be executable from documented contracts alone. Packaging-time script architecture lint may catch mechanical defects, but semantic validation must still decide whether the script surface makes efficient, non-improvised agent execution likely.

Add or require explicit anti-loop language when the skill has executable resources. Use wording close to:

```text
For normal execution, do not read script files. Scripts are executable implementation, not planning doctrine. After
reading the execution contract once, create the input artifact and run the command. Read or inspect scripts only when
the script failed, when validating package contents, or when explicitly editing the script.
```

### 4a2. Batch preparation efficiency gate

For skills that package, queue, or hand off multiple skill archives, validate that batch preparation and batch handoff are separated. Batch handoff may present several prepared `skill.zip` archives, but packaging remains a bounded series of single-target preparation units.

Return `repair_required` when a skill workflow:

- implies that batch mode requires packaging multiple skill roots in one wrapper invocation;
- encourages a large preparation window after recent timeouts or slow wrapper runs;
- treats a packaging timeout before handoff cursor start as `poisoned_batch` rather than `preparation_efficiency_failure`;
- treats timeout recovery as permission to manually zip, reuse stale packages, skip creator/validator evidence, or bypass the canonical wrapper;
- lacks a clear rule to reduce the preparation window to one, retry the same item in isolation, and continue serially after success;
- conflates packaging timeout with semantic validation failure when the wrapper receipt only shows slow execution.

A passable workflow should teach: timeout recovery should minimize wasted wall-clock time while preserving the canonical stack. Before the handoff cursor starts, slow package preparation is queue efficiency state. After the handoff cursor starts, wrong-surface links or substantive state-changing interruptions remain lifecycle failures.

### 4b. Fake-ledger resistance gate

For packaging, archive handoff, or other artifact handoff workflows, reject any design that lets assistant-authored ledger prose satisfy an evidence gate. A ledger is only a summary; the evidence must come from a machine-written receipt, tool response, or fresh file/hash check.

Return `repair_required` when a skill:

- treats `packaged_by_skill_packager` prose, package-size text, a pasted checklist, or `archive checks passed` as sufficient evidence;
- allows a package link without reading `package-evidence.json` or an equivalent machine-written receipt;
- does not require a fresh stat and SHA-256 check immediately before handoff;
- says a handoff is ready from expected paths, prior logs, or memory;
- lacks the fake-ledger regression test: `could this ledger have been typed without the artifact existing?`;
- fails to distinguish `hard_red_stack_incomplete` from `hard_red_invalid_handoff` when evidence or linked files are missing.

A passable package handoff workflow should make prose-only ledgers impossible to use as proof. The package path should come from a receipt produced by the packaging operation, and the final link should be generated only after the receipt and file hash match.


### 4b. Skill package handoff UI and control-system gate

For skills that create, validate, package, queue, or hand off installable Skill archives, validate the handoff path as a user-facing install surface, not as bookkeeping.

A `sandbox:/.../skill.zip` link can render as an installable Skill preview card in ChatGPT. If the archive is missing, malformed, stale, wrongly named, or only claimed in prose, Harley may see an Install UI that fails with `We could not load this skill`. That wastes the install attempt, creates false progress, causes skill-buster churn, and defeats the purpose of the validator/packager/buster control system built specifically to prevent invalid handoffs.

Return `repair_required` when a skill handoff workflow:

- accepts assistant-written ledger text, package-size claims, SHA claims, or receipt-shaped prose as archive evidence;
- allows a `skill.zip` link when no machine-written package evidence and final exact-path check are required;
- does not require the linked archive basename to be exactly `skill.zip`;
- allows renamed, versioned, guessed, stale, or planned zip paths as install handoffs;
- treats a local package plan, expected output, validation narrative, or prior log as enough to emit a link;
- lacks an explicit hard stop for fake or broken Skill preview cards;
- does not explain that this failure is severe because the control system failed at the job it exists to perform.

A passable handoff workflow should teach the model why the gate matters: if a broken `skill.zip` can still reach Harley, the stack failed at its core purpose. The correct behavior is to report `package not handoff-ready` instead of emitting any package link.


### 4c. Handoff surface and cursor-driver gate

For skills that create, validate, package, queue, or hand off installable Skill archives, validate the distinction between the handoff surface and the cursor driver.

The handoff surface is where the package link appears. A valid package handoff is a normal assistant chat message containing exactly one installable link whose basename is `skill.zip`.

The cursor driver is how the runtime advances from one assistant handoff message to the next. An inert cursor-advance pulse may be allowed between handoffs only when it contains no package link or package path, creates no evidence, inspects no source, has no external side effect, and leaves the manifest unchanged.

Return `repair_required` when a skill handoff workflow:

- permits `python_user_visible`, code output, canvas, widgets, GitHub comments, logs, notebook output, or any other tool/output channel to print or carry the installable package link;
- treats a file upload event, generated stdout, or hidden tool artifact as equivalent to a UI-surfaced install card;
- rejects all inert cursor-advance pulses so aggressively that the prepared batch cursor cannot complete in a runtime that needs an intervening event;
- allows an intervening pulse to inspect sources, post comments, mutate state, create evidence, alter the manifest, or carry package paths;
- does not require the pre-send check to include `handoff_surface: assistant_message`, `intervening_events_are_inert_pulses_only: true`, and `manifest_unchanged_since_preparation: true`.

This is a control-system distinction. A package can exist on disk while still being unpresented if it was surfaced through the wrong channel. Conversely, an inert pulse with no package link is not a handoff and should not poison the batch by itself.

### 4c2. Handoff telemetry and user confirmation gate

For skills that create, queue, or hand off installable Skill archives, validate that assistant-side upload telemetry is treated as a confidence signal, not as authoritative negative evidence of the user-visible install surface.

Return `repair_required` when a handoff workflow:

- treats missing, delayed, hidden, or unavailable assistant upload telemetry as proof that a valid assistant-message package link failed to surface;
- poisons a batch solely because upload telemetry is absent, when the package evidence was valid and the link appeared in a normal assistant message;
- ignores Harley's confirmation that a package surfaced or landed;
- lacks a `surface_unconfirmed` state for cases where pre-send evidence and the assistant-message link are valid but the assistant cannot observe the install card;
- fails to distinguish user-reported install failure from assistant-observed telemetry absence.

A passable workflow should teach: assistant-side upload telemetry can confirm surfacing, but it cannot disprove surfacing when the package link was validly emitted and Harley confirms the user-visible UI. Real poison conditions remain wrong-surface links, missing or mismatched archive evidence, user-reported install-card failure, or substantive cursor-breaking actions.


### 4d. Intended-update and no-op package prevention gate

For skill update, repair, packaging, or batch handoff work, validate that the staged source actually contains the intended update. A real `skill.zip` can still be false green if it repackages an existing skill without the requested change.

Return `repair_required` when a workflow or staged source:

- packages a skill without naming the intended update being reviewed;
- validates only generic package shape while ignoring whether the requested edit exists;
- lets a fresh package receipt substitute for source-change conformance;
- presents a rebuilt archive from an unmodified installed skill as if the update landed;
- cannot identify which files changed and how those changes satisfy the request;
- has validator evidence for a different staged path, a stale source tree, or a pre-edit copy.

A passable update review should prove:

```yaml
intended_update_present:
  intended_update_named: true
  modified_surfaces_match_intended_update: true
  validator_reviewed_modified_source: true
  package_must_be_built_from_that_source: true
```

This gate is distinct from fake-ledger and broken-link prevention. Fake-ledger prevention proves evidence is real. No-op prevention proves the real evidence is for the actual requested update.

### 5. Anti-pattern quality

Warnings must be concrete and reasoned. Repair vague warnings like `be careful`, `avoid errors`, or `consider edge
cases`. Prefer named failure modes and exact forbidden moves that prevent observed mistakes.

### 6. Freedom calibration

Match instruction strictness to task fragility. File packaging, source-control gates, and handoff cadence need precise
steps. Creative or judgment-heavy work needs principles, boundaries, and examples rather than fake determinism.

### 7. Composition boundaries

A skill should state what it owns and what adjacent skills own. Repair drift where a packager writes doctrine, a queue
skill edits content, a validator packages archives, or a project wrapper replaces its source-of-truth skill.

### 8. Practical usability

The skill must be usable in a real turn. It needs decision rules, fallbacks, exact blockers, and return expectations.
If the assistant would need to invent missing steps every time, repair before package handoff.

### 9. Immutable and protected targets

Reject attempts to edit immutable system skills, especially `skill-creator`. Use them as spec or source guidance only.
If the desired behavior change belongs near an immutable skill, update adjacent mutable enforcement skills instead.

## Handoff lifecycle, reference, and laundering regression checks

For skill-stack and project-wrapper updates, reject designs that treat packaging, validation, reporting, or continuity artifacts as stronger evidence than they are.

Return `repair_required` when a skill:

- allows a partially presented batch to resume from unpresented prebuilt archives instead of requiring rebuild after poison;
- permits multiple installable `skill.zip` links in one message, which can prevent later links from materializing as reliable install cards;
- uses direct skill directory names for ordinary handoffs where descriptive capability routing would be more robust, except for hard-coupled composition skills and locked safety gates;
- creates a duplicate specialist surface without a durable use-case justification;
- uses actor-prefixed GPT-native names that can imply GPT is impersonating an on-disk/project actor;
- lets validation selection, report text, worker claims, session-buster continuity, or package receipts launder into proof, truth, or closure state;
- omits a regression check for the current dispatch gate's three consecutive introspective GREENs when dispatch-gate behavior is in scope;
- places generic law in a project wrapper or project-specific law in a generic skill without an explicit composition reason.

A passable skill should teach the failure model behind each hard gate. The model is not `be careful`; it is that stale handoff state, brittle names, actor leakage, or evidence laundering can create false green progress that later users cannot safely distinguish from real completion.

## Common failure patterns

- `tutorial`: explains basics instead of adding expert workflow knowledge.
- `dump`: puts large optional detail in `SKILL.md` instead of references.
- `orphan references`: reference files exist but no workflow step requires them.
- `script read loop`: normal execution requires rereading scripts or resources to learn the command, schema, or
  stopping point.
- `implementation-as-doctrine`: script source is treated as the operating manual for ordinary use instead of a concise
  execution recipe.
- `checkbox procedure`: generic steps with no decision logic or domain-specific reason.
- `vague warning`: warnings lack concrete failure modes or reasons.
- `invisible skill`: frontmatter lacks trigger scenarios and keywords.
- `wrong location`: activation guidance appears only in the body.
- `over-engineered`: includes README, changelog, installation docs, or repo ceremony that the agent does not need.
- `boundary drift`: performs another skill's job or weakens adjacent-skill ownership.
- `image-credit churn`: treats deterministic visual work as image generation, omits credit-scarcity rationale, or lets
  QA/repair/prompt-board/workflow momentum spend scarce image credits.
- `immutable-target`: tries to modify a system or protected skill instead of routing through a mutable wrapper.
- `broken-install-card`: emits or permits a fake, stale, wrongly named, malformed, or unverified `skill.zip` link that can render as a broken Skill preview card and defeat the handoff-control stack.
- `fake-ledger`: assistant-authored ledger text claims packaging, validation, file existence, or upload readiness without machine evidence and a matching artifact hash.


## Stack-order fitness

For skill create, update, repair, packaging, or handoff work, the skill is not fit for handoff unless the approved stack
order is observable: `skill-creator, then skill-validator, then skill-packager, then skill-buster`.

Fail validation or block the process when:

- a package or handoff is attempted without an explicit `authored_by_skill_creator` token;
- the validator pass is only claimed in prose rather than returned as a decision for the same source path;
- `skill-packager` or `skill-buster` is being used as a substitute for validation;
- a later step tries to infer an earlier step from workflow readiness, memory, or expected sequence;
- a handoff workflow accepts assistant-authored package ledgers instead of a machine-written evidence receipt and fresh exact-file/hash verification.

Use `repair_required` for target-skill content defects. Use `blocked_requires_harley` with
`hard_red_stack_incomplete` when the update process itself has skipped the locked stack and must restart from the
missing step.

## Decision rules

Return `pass` only when the skill is handoff-ready after ordinary package validation.

Return `repair_required` for quality defects GPT can fix: vague or semantically weak descriptions, duplicate prose,
misplaced triggers, missing reference triggers, bloated control plane, weak composition, orphan scaffold files,
script-read-loop risk, implementation-as-doctrine drift, missing deterministic execution recipes, missing image-credit
stewardship in visual-production skills, deterministic visual work routed to image generation, broken Skill install-card
risk in package handoff workflows, prose-only package evidence, non-`skill.zip` handoff filenames, or generic filler.

Return `blocked_requires_harley` only for missing external input, missing authority, unavailable connectors, or real
product choices that cannot be inferred safely.

Return `reject_before_handoff` when the skill target is immutable, unsafe, redundant beyond repair, or incompatible
with the local skill stack.
