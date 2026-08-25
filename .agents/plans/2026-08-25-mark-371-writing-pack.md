# MARK-371 Writing Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/subagent-driven-development` (recommended) or `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a first-party `writing-pack` whose clarity, author-voice, and evidence-backed anti-fatigue controls compose cleanly; retain `unslop-plus` as the generic engine/profile home; and remove duplicate writing custody from `repo-worker-pack` without breaking this repository's installed skill set.

**Architecture:** Add four self-contained skills under one plugin: `writing` routes the workflow, `writing-with-clarity` remains the clarity authority, `writing-style` owns writing-specific profiles and evidence, and `writing-profile-engine` discovers, validates, and evaluates those profiles. Keep generic `unslop-engine` and `unslop-profiles` in `unslop-plus`. Treat profiles as versioned data below lawful `references/` roots, and make the writing engine return typed findings instead of authorship judgments or detector scores.

**Tech Stack:** Markdown and YAML skill assets, JSON Schema and JSON profile fixtures, Python 3.11+ standard-library scripts, pytest, repository marketplace/index generators.

**Execution Strategy:** `subagent-driven-development` — the plan is long but well sliced. Use one fresh implementer per task and fresh review context between tasks; preserve task order because later tasks consume the plugin and contracts established earlier.

## Global Constraints

- The approved design at `.agents/specs/2026-08-25-mark-371-writing-pack-design.md` is authoritative. Do not re-open settled plugin boundaries during implementation.
- `writing-with-clarity` is the clarity authority and final gate. Anti-fatigue edits must not make prose less clear.
- `writing-style` preserves declared author voice unless clarity, factual accuracy, safety, or an explicit house rule requires a change.
- The workflow order is: intent and facts -> clarity -> author voice -> fatigue review -> final clarity gate.
- This is not detector evasion. Do not add detector scores, "humanizer" language, authorship claims, or instructions to bypass AI detection.
- A single token, phrase, rhetorical device, or formatting choice is never enough to prove a problem. Findings require contextual evidence and profile-defined thresholds.
- Profiles may live only below skill-standard roots. Use `references/profiles/**`; never create a top-level `profiles/` directory inside a skill.
- Use public or publishable fixtures only. Do not commit private author corpora, unpublished client copy, or personal messages.
- `unslop-plus` remains the generic home for `unslop-engine` and `unslop-profiles`; do not move either into `writing-pack`.
- Move the existing `writing-with-clarity` tree with `git mv` so its history and public-domain authority assets remain intact.
- Edit canonical plugin sources under `codex-marketplace/plugins/`. Do not hand-edit `.agents/skills/`; regenerate it from the installed-default configuration.
- New and materially changed skills must keep `SKILL.md` below 500 words excluding frontmatter, include `agents/openai.yaml`, and pass source-custody and skill-script validation.
- Every mutating script must expose `--help`, default to `--check`, and require explicit `--apply`. The evaluation scripts in this plan are read-only and must not mutate their inputs.
- Research claims must be traceable to primary sources. Label each claim `measured`, `inferred`, or `hypothesis`, include domain and limitations, and record `retrieved_at` and a refresh date.
- Use TDD for Python and structural behavior. Record the focused RED failure before implementation and the focused GREEN result after it.
- Each task ends with focused validation, a diff review, plan checkbox updates, and its own commit. Do not batch unchecked tasks into one commit.
- Before any commit that depends on generated indexes, stage all intended source files first and run `py -3 tools/run.py mesh --apply` so the generated mesh sees the staged tree.
- The full completion gate is `py -3 tools/run.py ci --check`, a clean worktree, an open draft PR with branch and full SHA, completed iterative review, and honest Linear/PR reporting.

---

### Task 1: Establish the research ledger and RED pressure baseline

**Files:**
- Create: `research/ai-prose-fatigue/README.md`
- Create: `research/ai-prose-fatigue/evidence-ledger.md`
- Create: `research/ai-prose-fatigue/source-register.json`
- Create: `tests/pressure/writing/prompts/clarity-versus-unslop.md`
- Create: `tests/pressure/writing/prompts/preserve-deliberate-device.md`
- Create: `tests/pressure/writing/prompts/voice-without-private-corpus.md`
- Create: `tests/pressure/writing/prompts/no-detector-evasion.md`
- Create: `tests/pressure/writing/prompts/INDEX.md`
- Create: `tests/pressure/writing/README.md`
- Create: `tests/pressure/writing/red.md`

**Interfaces:**
- Produces: a publishable evidence ledger separating empirical findings, bounded inference, and working hypotheses.
- Produces: a source register with stable URL, publication date, retrieval date, study domain, evidence class, limitations, and next-review date.
- Produces: four reusable behavioral scenarios and a recorded pre-skill RED baseline.
- Does not produce: profile rules, word bans, detector claims, or private author samples.

- [x] **Step 1: Verify and record primary research**

Use web research and original papers or publisher records. At minimum, assess these live candidates and replace any that cannot support the claimed point:

- Sourati et al., "The shrinking landscape of linguistic diversity in the age of large language models," *Nature Human Behaviour* (2026): `https://www.nature.com/articles/s41562-026-02550-0`.
- Acerbi et al., "What Are LLMs Doing to Scientific Communication? Measuring Changes in Writing Practices and Reading Experience," LREC 2026: `https://aclanthology.org/2026.lrec-1.142/`.
- Agarwal et al., "AI Suggestions Homogenize Writing Toward Western Styles and Diminish Cultural Nuances," CHI 2025: `https://doi.org/10.1145/3706598.3713564`.
- Kobak et al., the published or latest primary record for post-ChatGPT excess vocabulary in biomedical writing; verify the final bibliographic record rather than relying on a search snippet or news article.
- Weber-Wulff et al. or a stronger primary audit on machine-generated-text detection limitations; use it only to support abstention and non-detection boundaries.

For each source, record what was measured, what population/domain was studied, what it does not establish, and whether it supports an operational rule. Do not generalize academic-writing word-frequency results to all prose.

- [x] **Step 2: Write the evidence ledger**

Organize `evidence-ledger.md` by pattern family rather than by disliked phrase:

1. lexical concentration and repeated stock transitions;
2. structural regularity and paragraph-shape repetition;
3. evaluative inflation and unsupported importance claims;
4. excessive signposting, summary repetition, and conclusion restatement;
5. voice flattening and loss of culturally or personally meaningful variation;
6. legitimate-device preservation and false-positive risk.

Every entry must include `Evidence class`, `Observed domain`, `Operational implication`, `Preserve when`, `Limitations`, and `Source IDs`.

- [x] **Step 3: Write pressure scenarios before the new skills exist**

Each prompt must include concrete input prose and an objective rubric. Collectively require the future workflow to:

- reject an "unslop" edit that makes a clear sentence obscure;
- preserve an intentional repeated phrase, em dash, or three-part structure when it pays rhetorical rent;
- derive a bounded voice card from user-provided text without storing a corpus;
- refuse detector-evasion framing while still offering a legitimate clarity/style revision.

- [x] **Step 4: Run and record the RED baseline**

Dispatch one fresh pressure-test subagent per prompt with no access to the approved design or future skills. Record the model/profile, exact prompt path, response, rubric judgment, and failure mode in `tests/pressure/writing/red.md`. RED is successful when the baseline exposes at least one material routing, preservation, or detector-boundary failure; do not manufacture a failure if all scenarios pass.

- [x] **Step 5: Validate and commit Task 1**

```powershell
py -3 -m json.tool research/ai-prose-fatigue/source-register.json > $null
py -3 tools/run.py mesh --apply
git diff --check
git add research/ai-prose-fatigue tests/pressure/writing .agents/plans/2026-08-25-mark-371-writing-pack.md .agents/plans/INDEX.md .agents/plans/INDEX.json
git commit -m "research: establish AI prose fatigue evidence baseline"
```

---

### Task 2: Scaffold `writing-pack` and migrate the clarity authority

**Files:**
- Create: `codex-marketplace/plugins/writing-pack/**` via `tools/new_plugin.py`
- Move: `codex-marketplace/plugins/repo-worker-pack/skills/writing-with-clarity/` -> `codex-marketplace/plugins/writing-pack/skills/writing-with-clarity/`
- Modify: `codex-marketplace/plugins/writing-pack/.codex-plugin/plugin.json`
- Modify: `codex-marketplace/plugins/writing-pack/package.json`
- Modify: `codex-marketplace/plugins/writing-pack/README.md`
- Modify: `codex-marketplace/plugins/writing-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/writing-pack/skills/writing-with-clarity/SKILL.md`
- Modify: `codex-marketplace/plugins/writing-pack/skills/writing-with-clarity/agents/openai.yaml`
- Create: `tests/test_writing_pack.py`

**Interfaces:**
- Consumes: the approved boundary and existing `writing-with-clarity` tree.
- Produces: an enabled marketplace plugin root with `writing-with-clarity` under its sole canonical plugin path.
- Preserves: the existing clarity guidance, source map, citations, licence, bounded public-domain reference chapters, and report-hygiene reference.

- [x] **Step 1: Add failing plugin-boundary tests**

In `tests/test_writing_pack.py`, add focused tests asserting:

- `writing-pack` is enabled in `codex-marketplace/plugin-roots.json`;
- its plugin and package manifests expose the name `writing-pack` and the four approved skill names;
- `writing-with-clarity` exists under `writing-pack` and not under `repo-worker-pack`;
- its authority asset tree and report-hygiene reference still exist;
- no skill inside `writing-pack` owns a top-level directory named `profiles`.

Run and record RED:

```powershell
py -3 -m pytest tests/test_writing_pack.py -q
```

- [x] **Step 2: Scaffold and enable the plugin**

```powershell
py -3 tools/new_plugin.py --check writing-pack
py -3 tools/new_plugin.py --apply writing-pack
```

Change the new `writing-pack` entry in `codex-marketplace/plugin-roots.json` from scaffold default `enabled: false` to `enabled: true`. Replace scaffold prose and manifest metadata with the approved four-skill boundary, writing-specific keywords, MIT rights statement, and a default prompt that routes ordinary writing work through `$writing`.

- [x] **Step 3: Move `writing-with-clarity` with history**

Use `git mv` for the whole skill directory. Update only path metadata and cross-skill routing needed by the new custody location; do not rewrite the clarity doctrine. Set `metadata.source-path` to `codex-marketplace/plugins/writing-pack/skills/writing-with-clarity/SKILL.md` and keep the existing `skills-with-source` authority lane byte-valid.

- [x] **Step 4: Sync the bundle and pass focused GREEN**

```powershell
py -3 tools/new_plugin.py --sync writing-pack
py -3 tools/validate_authority_assets.py
py -3 -m pytest tests/test_writing_pack.py -q
git diff --check
```

- [x] **Step 5: Commit Task 2**

```powershell
git add codex-marketplace/plugin-roots.json codex-marketplace/plugins/writing-pack codex-marketplace/plugins/repo-worker-pack/skills/writing-with-clarity tests/test_writing_pack.py .agents/plans/2026-08-25-mark-371-writing-pack.md
git commit -m "feat: scaffold writing pack and migrate clarity skill"
```

---

### Task 3: Build and pressure-test the compositional `writing` router

**Files:**
- Create: `codex-marketplace/plugins/writing-pack/skills/writing/SKILL.md`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing/agents/openai.yaml`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing/references/workflow.md`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing/references/authority-order.md`
- Modify: `tests/pressure/writing/red.md`
- Create: `tests/pressure/writing/green-writing.md`
- Modify: `tests/test_writing_pack.py`

**Interfaces:**
- Consumes: user intent, facts, audience, constraints, optional voice guidance, and draft text.
- Routes to: `$writing-with-clarity`, `$writing-style`, and a final `$writing-with-clarity` check.
- Produces: revised prose plus concise disclosure of material voice/style choices when useful.
- Never delegates: factual authority to a style profile or clarity authority to an anti-fatigue finding.

- [x] **Step 1: Extend tests for the routing contract**

Assert that the skill metadata names related skills, that `workflow.md` contains the five-stage order, and that `authority-order.md` ranks factual accuracy/safety, explicit user intent, clarity, declared voice, and fatigue heuristics in that order. Run the focused test and record RED.

- [x] **Step 2: Write the lean router and references**

Keep `SKILL.md` procedural and below 500 words. It must:

1. establish audience, purpose, facts, and hard constraints;
2. draft/revise for clarity;
3. apply a declared voice card if present;
4. invoke the writing-specific profile review only where evidence supports a finding;
5. re-run the clarity gate and restore anything whose removal damaged meaning.

Make abstention normal: if no material fatigue pattern is present, return the clear draft unchanged.

- [x] **Step 3: Run fresh-context GREEN pressure tests**

Re-run `clarity-versus-unslop.md` and `no-detector-evasion.md` with the new `writing` skill available. Record exact responses and rubric judgments in `green-writing.md`. Fix the skill, not the rubric, until both pass.

- [x] **Step 4: Validate and commit Task 3**

```powershell
py -3 -m pytest tests/test_writing_pack.py -q
py -3 codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/validate_skill_scripts.py
py -3 tools/new_plugin.py --sync writing-pack
git diff --check
git add codex-marketplace/plugins/writing-pack tests/pressure/writing tests/test_writing_pack.py .agents/plans/2026-08-25-mark-371-writing-pack.md
git commit -m "feat(writing-pack): add compositional writing router"
```

---

### Task 4: Build `writing-style` with evidence-backed fatigue and voice profiles

**Files:**
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/SKILL.md`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/agents/openai.yaml`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/assets/authority/authority.yaml`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/assets/authority/source-map.yaml`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/assets/authority/CITATIONS.md`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/references/profile-contract.md`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/references/voice-card.md`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/references/profiles/fatigue/ai-prose-fatigue/profile.md`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/references/profiles/fatigue/ai-prose-fatigue/patterns.json`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/references/profiles/fatigue/ai-prose-fatigue/goldens.json`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/references/profiles/fatigue/ai-prose-fatigue/sources.md`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/references/profiles/voice/voice-card.schema.json`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-style/references/profiles/voice/default-voice-card.json`
- Create: `tests/test_writing_profiles.py`
- Create: `tests/pressure/writing/green-style.md`
- Create: `tests/pressure/writing/blinded/README.md`
- Create: `tests/pressure/writing/blinded/stimulus.md`
- Create: `tests/pressure/writing/blinded/hidden-rubric.md`
- Create: `tests/pressure/writing/blinded/campaign.json`

**Interfaces:**
- Consumes: the Task 1 evidence ledger, a draft, optional voice card, and context/audience.
- Produces: `observed`, `candidate`, `preserve`, `repair`, or `abstain` guidance with evidence and scope.
- Owns: writing-specific profile data under `references/profiles/**`.
- Does not own: generic cross-domain unslop profiles or automated authorship classification.

- [x] **Step 1: Write failing contract and golden-fixture tests**

`tests/test_writing_profiles.py` must initially fail and then enforce:

- all JSON parses and every profile ID is unique and stable;
- every pattern declares family, rationale, evidence class, contextual threshold, preserve conditions, repair guidance, source IDs, limitations, version, `reviewed_at`, and `review_after`;
- exact-token bans and detector-score fields are rejected;
- each `goldens.json` case names expected finding types and IDs;
- positive cases cover pattern clusters, negative cases preserve legitimate devices, and counterexamples protect clarity and author voice;
- the voice-card schema stores bounded tendencies and explicit avoid/prefer choices, not source prose or identity claims.

Run and record RED:

```powershell
py -3 -m pytest tests/test_writing_profiles.py -q
```

- [x] **Step 2: Create the `skills-with-citation` authority record**

Synthesize from Task 1's primary sources without vendoring paywalled or copyrighted papers. `authority.yaml`, `source-map.yaml`, and `CITATIONS.md` must follow the repository citation-lane contract and hash the local citation evidence exactly. Map each derived reference/profile file to the source sections that support it. Keep issue-specific empirical notes in `research/`; put only durable, bounded operational guidance in the skill.

- [x] **Step 3: Author profile contract, fatigue profile, and goldens**

Use contextual pattern families, not a banned-word list. Each finding must answer:

- what repeated or mismatched behavior was observed;
- why it may tire or flatten this audience in this context;
- what evidence class supports the concern;
- when the same device should be preserved;
- the smallest repair that retains meaning and voice.

Set a dated refresh horizon. Expired evidence may still be displayed but must downgrade automated recommendations to `candidate` or `abstain` until reviewed.

- [x] **Step 4: Author the voice-card contract**

The voice card may capture tendencies such as sentence range, directness, preferred vocabulary register, tolerated fragments, rhetorical devices, formatting norms, and explicit do/don't choices. It must be generated only from text the user supplies for the current task or from explicit preferences, and it must not retain the original corpus.

- [x] **Step 5: Run GREEN tests and pressure tests**

```powershell
py -3 -m pytest tests/test_writing_profiles.py tests/test_writing_pack.py -q
py -3 tools/validate_authority_assets.py
```

Run `preserve-deliberate-device.md` and `voice-without-private-corpus.md` in fresh contexts with `writing-style` available. Record responses and judgments in `green-style.md`; both must pass without changing the scenario rubric.

Treat those two runs as acceptance/regression evidence only because their Task
1 baseline already passed. Separately use a fresh test designer to freeze one
adversarial worker stimulus, a hidden judge rubric, and a machine-readable A/B
manifest under `tests/pressure/writing/blinded/`. Do not run either A/B arm in
Task 4 and never expose the hidden rubric to workers.

- [x] **Step 6: Commit Task 4**

```powershell
git add codex-marketplace/plugins/writing-pack/skills/writing-style tests/test_writing_profiles.py tests/pressure/writing .agents/plans/2026-08-25-mark-371-writing-pack.md
git commit -m "feat(writing-pack): add evidence-backed style profiles"
```

---

### Task 5: Implement the writing-specific profile engine with TDD

**Files:**
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/SKILL.md`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/agents/openai.yaml`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/assets/schemas/writing-profile.schema.json`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/references/result-contract.md`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/scripts/discover_profiles.py`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/scripts/validate_profiles.py`
- Create: `codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/scripts/evaluate_profile.py`
- Create: `tests/test_writing_profile_engine.py`
- Modify: `tests/test_writing_profiles.py`
- Create: `tests/pressure/writing/blinded/results.md`
- Create: six frozen-arm worker outputs and six anonymized judge inputs under `tests/pressure/writing/blinded/outputs/`

**Interfaces:**
- `discover_profiles.py [--root PATH] [--json]`: returns profiles found only below `references/profiles/`, with stable ID, version, kind, and path.
- `validate_profiles.py [--root PATH] [--json]`: defaults to non-mutating validation and returns non-zero for schema, reference, golden, expiry-policy, or unsafe-field errors.
- `evaluate_profile.py --profile PATH --input PATH [--voice-card PATH] [--json]`: evaluates one UTF-8 text file and emits typed findings without editing the source.
- JSON result: `{schema_version, profile_id, profile_version, input_sha256, status, findings, warnings}`.
- Finding: `{type, pattern_id, evidence, span, rationale, preserve_when, repair, confidence}` where `type` is one of `observed`, `candidate`, `preserve`, `repair`, `abstain`.

- [x] **Step 1: Write failing CLI and evaluator tests**

Cover:

- `--help` for every script;
- default check/read-only behavior and stable JSON output;
- lawful recursive discovery below `references/profiles/` only;
- schema and cross-reference failures with actionable paths;
- cluster thresholds, preserve rules, overlapping findings, UTF-8, empty input, and deterministic ordering;
- expired-profile downgrade behavior;
- no detector score, authorship conclusion, or source mutation;
- every fatigue golden fixture's expected finding IDs and types.
- evaluator behavior is fixed solely from profile goldens before any blinded
  campaign output is generated or revealed.

Run and record RED:

```powershell
py -3 -m pytest tests/test_writing_profile_engine.py -q
```

- [x] **Step 2: Implement schema and discovery**

Use Python's standard library. Resolve paths with `Path.resolve()`, verify the discovered file remains under the requested root, reject symlink/path escapes, ignore unrelated files, and sort by normalized relative path. The JSON Schema is the machine-readable contract; the validator may implement the supported subset explicitly rather than adding a runtime dependency.

- [x] **Step 3: Implement profile validation**

Validate JSON shape, required metadata, unique pattern IDs, allowed enums, source ID references, golden expected IDs, and dates. Treat a past `review_after` as a warning plus recommendation downgrade, not silent invalidation. Reject fields whose semantics imply detection/evasion or a universal word ban.

- [x] **Step 4: Implement deterministic evaluation**

Support only transparent rules declared in `patterns.json`: normalized phrase occurrence, paragraph/sentence repetition, local structure clusters, and explicitly declared co-occurrence thresholds. Return evidence spans and counts. Do not infer authorship, fabricate confidence, or use opaque model calls. If the profile cannot support a judgment, emit `abstain`.

- [x] **Step 5: Pass focused GREEN and script-contract validation**

```powershell
py -3 -m pytest tests/test_writing_profile_engine.py tests/test_writing_profiles.py -q
py -3 codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/scripts/discover_profiles.py --help
py -3 codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/scripts/validate_profiles.py --help
py -3 codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/scripts/evaluate_profile.py --help
py -3 codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/scripts/validate_profiles.py
py -3 codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/validate_skill_scripts.py
```

- [x] **Step 6: Run the frozen blinded A/B campaign (retained as protocol-invalid diagnostic evidence)**

Only after the engine passes GREEN, run the unchanged campaign declared in
`tests/pressure/writing/blinded/campaign.json`: three fresh no-skill workers and
three fresh workers with `writing-style` explicitly available and invoked. Use
the identical declared model, reasoning, and `fork_turns` settings. Workers may
read only the stimulus plus their arm's declared skill files; they must never
read the hidden rubric or another output.

Evaluate active pattern-family counts and density plus typed findings. Anonymize
the six outputs and send only those outputs and the hidden rubric to a fresh
independent judge for clarity, factuality, and authorised-voice decisions. Do
not edit the skill, profile, engine, evaluator, stimulus, rubric, manifest, or
thresholds after outputs are revealed to make the campaign pass.

Baseline RED requires the manifest's majority-failure threshold. GREEN requires
its majority treatment-pass and primary-improvement thresholds without
degrading secondary metrics. Otherwise report the result as inconclusive or
non-discriminating; do not claim causality.

- [x] **Step 7: Commit Task 5**

```powershell
git add codex-marketplace/plugins/writing-pack/skills/writing-profile-engine tests/test_writing_profile_engine.py tests/test_writing_profiles.py tests/pressure/writing/blinded .agents/plans/2026-08-25-mark-371-writing-pack.md
git commit -m "feat(writing-pack): add writing profile engine"
```

---

### Task 6: Complete routing, remove duplicate custody, and preserve generic `unslop-plus`

**Files:**
- Remove: `codex-marketplace/plugins/repo-worker-pack/skills/unslop-profiles/`
- Modify: `codex-marketplace/plugins/repo-worker-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/unslop-plus/README.md`
- Modify: `codex-marketplace/plugins/unslop-plus/SOURCE.md`
- Modify: `codex-marketplace/plugins/unslop-plus/skills/unslop-engine/SKILL.md`
- Modify: `codex-marketplace/plugins/unslop-plus/skills/unslop-profiles/SKILL.md`
- Move: `codex-marketplace/plugins/unslop-plus/skills/unslop-profiles/profiles/` -> `codex-marketplace/plugins/unslop-plus/skills/unslop-profiles/references/profiles/`
- Modify: `codex-marketplace/plugins/unslop-plus/skills/unslop-profiles/references/profiles/writing.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/references/doctrine-index.md`
- Modify: `codex-marketplace/plugins/planning-pack/skills/estimation/SKILL.md`
- Modify: `codex-marketplace/plugins/planning-pack/skills/mermaid-diagramming/SKILL.md`
- Modify: `codex-marketplace/plugins/planning-pack/skills/requirements-elicitation/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/references/bootstrap-routing.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/SKILL.md`
- Modify: `AGENTS.md`
- Modify: `tests/test_writing_pack.py`

**Interfaces:**
- Produces: one canonical `unslop-profiles` tree under `unslop-plus` and one canonical `writing-with-clarity` tree under `writing-pack`.
- Preserves: `/unslop-profiles` as the generic cross-domain router and `/unslop-engine` as the generic profile-generation concept.
- Routes: prose creation/revision to `/writing`; direct clarity-only work may still invoke `/writing-with-clarity`.

- [ ] **Step 1: Add failing uniqueness and reference tests**

Extend `tests/test_writing_pack.py` to assert exactly one canonical directory exists for each of `writing-with-clarity` and `unslop-profiles`, that no marketplace skill owns a top-level `profiles/` directory, and that live non-generated references point to their current owning plugin where a physical path is named. Run RED.

- [ ] **Step 2: Remove the duplicate generic profile tree**

Delete only `codex-marketplace/plugins/repo-worker-pack/skills/unslop-profiles/`; its byte-identical canonical replacement remains in `unslop-plus`. Do not delete or relocate `unslop-plus/skills/unslop-engine` or `unslop-plus/skills/unslop-profiles`.

Move the retained generic library with `git mv` from
`unslop-plus/skills/unslop-profiles/profiles/` to
`unslop-plus/skills/unslop-profiles/references/profiles/`, then update its
router paths. This is a layout correction, not a transfer of ownership to the
writing plugin.

- [ ] **Step 3: Make the generic/writing boundary explicit**

Update `unslop-plus` prose so its generic writing profile routes sustained prose work to `$writing` when installed, while remaining usable by itself. Correct the stale `unslop-engine` output-contract reference: either add the referenced contract under its lawful `references/` root or remove the false claim, based on the live generic engine behavior. Do not expand MARK-371 into a generic-engine rewrite.

- [ ] **Step 4: Update live cross-references**

Audit the file list above plus a fresh repository-wide `rg`. Replace ownership/path statements, not historical completed specs. Update general prose routing to `$writing`; retain `$writing-with-clarity` where the call genuinely requests only clarity or final-edit review. Keep `/unslop-profiles` references for security, testing, code review, and other generic profiles.

- [ ] **Step 5: Sync manifests and pass focused GREEN**

```powershell
py -3 tools/new_plugin.py --sync writing-pack
py -3 tools/new_plugin.py --sync repo-worker-pack
py -3 tools/new_plugin.py --sync unslop-plus
py -3 -m pytest tests/test_writing_pack.py -q
rg -n "repo-worker-pack/skills/(writing-with-clarity|unslop-profiles)" AGENTS.md codex-marketplace tools tests
git diff --check
```

The final `rg` must return no live ownership references; historical completed specs may remain untouched and should be excluded if needed.

- [ ] **Step 6: Commit Task 6**

```powershell
git add AGENTS.md codex-marketplace/plugins tests/test_writing_pack.py .agents/plans/2026-08-25-mark-371-writing-pack.md
git commit -m "refactor: separate writing and generic unslop custody"
```

---

### Task 7: Install defaults, regenerate consumer surfaces, and prove package integrity

**Files:**
- Modify: `codex-marketplace/repo-local-marketplace-policy.json`
- Modify: generated `.agents/plugins/marketplace.json`
- Modify: generated `codex-marketplace/manifest.json`
- Modify: generated `codex-marketplace/README.md`
- Modify: generated `codex-marketplace/INDEX.md`
- Modify: generated `codex-marketplace/INDEX.json`
- Modify: generated `repo-index/**`
- Modify: generated `.agents/skills/**`
- Modify: generated `.agents/skills/.provenance.json`
- Modify: generated index mesh files
- Modify: `tests/test_refresh_installed_skills.py`
- Modify: `tests/test_worktree_scripts.py` if their minimal fixture assumptions require the expanded default set
- Modify: `tests/test_writing_pack.py`

**Interfaces:**
- Consumes: canonical plugin sources and `install_defaults` policy.
- Produces: this repository's installed skills from `repo-worker-pack`, `superpowers-plus`, `mcp-usage-pack`, `writing-pack`, and `unslop-plus`.
- Guarantees: `.agents/skills/writing`, `writing-with-clarity`, `writing-style`, `writing-profile-engine`, `unslop-engine`, and `unslop-profiles` are present and provenance points to the correct plugin owners.

- [ ] **Step 1: Add failing installed-default tests**

Update focused tests to expect `writing-pack` and `unslop-plus` in `install_defaults` and `syncedPlugins`, and to reject stale provenance pointing `writing-with-clarity` or `unslop-profiles` at `repo-worker-pack`. Keep fixture order deterministic. Run RED:

```powershell
py -3 -m pytest tests/test_refresh_installed_skills.py tests/test_worktree_scripts.py tests/test_writing_pack.py -q
```

- [ ] **Step 2: Update the editable default policy**

Add `writing-pack` and `unslop-plus` to `codex-marketplace/repo-local-marketplace-policy.json` `install_defaults` in marketplace order. Do not hand-edit generated policy results to disguise a generator mismatch.

- [ ] **Step 3: Regenerate in dependency order**

Stage all canonical source additions, moves, removals, policy changes, tests, research, and plan updates before applying generators. Then run:

```powershell
git add AGENTS.md research tests codex-marketplace/plugins codex-marketplace/repo-local-marketplace-policy.json codex-marketplace/plugin-roots.json .agents/specs .agents/plans
py -3 tools/run.py marketplace --apply
py -3 tools/run.py installed-skills --apply
py -3 tools/run.py index-mesh --apply
```

Review generated diffs. Confirm `.agents/skills/` contains installed copies, not a second editable source tree.

- [ ] **Step 4: Pass package and installed-surface GREEN**

```powershell
py -3 -m pytest tests/test_refresh_installed_skills.py tests/test_worktree_scripts.py tests/test_writing_pack.py -q
py -3 tools/run.py marketplace --check
py -3 tools/run.py installed-skills --check
py -3 tools/run.py index-mesh --check
py -3 tools/validate_authority_assets.py
git diff --check
```

- [ ] **Step 5: Commit Task 7**

```powershell
git add -A
git commit -m "build: publish writing pack to marketplace surfaces"
```

---

### Task 8: Run end-to-end review, publish the draft PR, and return proof

**Files:**
- Modify: `tests/pressure/writing/README.md`
- Modify: `tests/pressure/writing/INDEX.md`
- Modify: `tests/pressure/writing/red.md`
- Modify: `tests/pressure/writing/green-writing.md`
- Modify: `tests/pressure/writing/green-style.md`
- Modify: `.agents/plans/2026-08-25-mark-371-writing-pack.md`
- Modify: generated mesh/index files if the final documentation update changes them

**Interfaces:**
- Produces: proof that the compositional workflow passes behavioral, structural, source-custody, generation, and repository-wide checks.
- Produces: a draft PR URL, branch name, full head SHA, CI posture, review findings, and remaining risks.
- Does not produce: a GREEN completion claim from local-only evidence.

- [ ] **Step 1: Close the pressure campaign honestly**

Summarize RED versus GREEN behavior without claiming statistical validity. Record model/profile and context mode for every run. State that the campaign tests instruction-following and boundary behavior, not whether prose is human-authored or universally pleasant.

- [ ] **Step 2: Run focused and full verification**

```powershell
py -3 -m pytest tests/test_writing_pack.py tests/test_writing_profiles.py tests/test_writing_profile_engine.py -q
py -3 tools/run.py ci --check
py -3 tools/run.py ci --check
git diff --check
```

The second full gate is a determinism check. If either run fails, invoke `/systematic-debugging`, fix the root cause, and rerun both gates from fresh output.

- [ ] **Step 3: Self-review with the required lenses**

Mechanically review the branch diff against the current `reviewer-skills`, `reviewer-marketplace`, and `reviewer-security` profile checklists. Pay particular attention to:

- vague triggers or overlong skill bodies;
- source-lane hashes and unsupported research claims;
- illegal folder roots or path traversal in discovery;
- accidental detector/evasion semantics;
- generated/source custody confusion;
- lost installed-default coverage;
- stale plugin paths and duplicate canonical skill names.

Fix all actionable findings before external review.

- [ ] **Step 4: Run iterative review**

Invoke `/iterative-review` against the complete branch diff. Use the required independent lens and strong-review passes. Resolve every valid finding, rerun affected focused tests, then rerun `py -3 tools/run.py ci --check`. Record reviewer identity/profile, branch SHA reviewed, findings, repairs, and final verdict.

- [ ] **Step 5: Complete the plan and publish**

Mark each genuinely delivered checkbox complete, regenerate the mesh, run the final CI gate, and commit the closeout update:

```powershell
py -3 tools/run.py index-mesh --apply
py -3 tools/run.py ci --check
git add -A
git commit -m "docs: complete MARK-371 writing pack plan"
git status --short
git rev-parse HEAD
```

Push `codex/mark-371-writing-pack-design` and open a **draft** PR into `main`. The PR body must name MARK-371, summarize the settled plugin boundary, list RED/GREEN and full-CI evidence, disclose the research limitations, and state that the feature is anti-fatigue/style guidance rather than detector evasion.

- [ ] **Step 6: Return proof and update Linear**

Verify the remote PR head equals local `HEAD`. Report:

- draft PR URL;
- branch and full SHA;
- exact validation commands and results;
- pressure-test scope and limitations;
- iterative-review profiles and verdicts;
- any residual evidence-refresh risk;
- confirmation that `writing-pack` and `unslop-plus` are installed by default here while remaining distinct plugins.

Add the same evidence-backed summary to MARK-371. Do not close the Linear issue unless the user explicitly requests closure or the issue workflow independently authorizes it.
