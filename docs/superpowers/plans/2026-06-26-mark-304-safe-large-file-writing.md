# MARK-304 safe-large-file-writing pre-composition context-pressure implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a pre-composition context-pressure rule to the first-party `safe-large-file-writing` skill so agents stop before they inline-compose a large document in a low-context session and instead route to a clean-context worker/subagent or bounded append path.

**Architecture:** Keep the canonical skill source in `sources/first_party/skills/safe-large-file-writing/`. Make a small additive edit to the skill body so the new rule appears before the existing large-write decision gate, then refresh the projected `house-skills` surface and skill zip through the repo tooling. The update stays additive: preserve the existing chunked/temp-file write mechanics, but move the decision to avoid inline composition earlier so the main session never spends its remaining context building the full document string.

**Tech Stack:** Markdown skill source, YAML agent metadata, projected Codex marketplace skill trees, generated skill zips, Python regeneration/check scripts, PowerShell.

## Global Constraints

- Use the fresh `origin/main` base and keep the isolated `.worktrees/` checkout as the only edit surface.
- Do not patch Devin Desktop installed state at `C:\Users\hbart\AppData\Roaming\devin\skills\safe-large-file-writing\SKILL.md`; it is field evidence only.
- The repository does not have a `.agents/skills` tree in this checkout, so do not invent one; the relevant source custody is under `sources/first_party/skills/safe-large-file-writing/`.
- Keep the change additive and small. Do not rewrite the whole skill or touch unrelated skills.
- Preserve the existing chunked-temp-file write path and atomic replace guidance.
- The current repository already projects `safe-large-file-writing` into `codex-marketplace/plugins/house-skills/skills/safe-large-file-writing` and `generated/skill-zips/house-skills/safe-large-file-writing/skill.zip`; use the generators to keep those downstream surfaces in sync.
- Use repo generators for downstream outputs. Do not hand-edit generated projection or zip surfaces.

---

### Task 1: Update the canonical first-party skill source

**Files:**
- Modify: `sources/first_party/skills/safe-large-file-writing/SKILL.md`
- Modify: `sources/first_party/skills/safe-large-file-writing/agents/openai.yaml`

**Interfaces:**
- Consumes: the current `safe-large-file-writing` source body and agent prompt.
- Produces: a skill that names pre-composition context pressure before the large-write branch and tells the agent to route away from inline composition when context is tight.

- [ ] **Step 1: Insert the new pre-composition rule before the existing large-write branch**

Add this section between the current opening rule and the `## Large-write threshold` section:

```markdown
## Pre-composition context pressure

Before composing a large document, decide whether the composition itself will exceed the session's remaining context budget.

Treat a write as context-risky when either is true:

- the output is likely to exceed about 300 lines;
- the session has already accumulated significant subagent output, research, or file reads in context.

When context-risky:

1. Do not compose the whole document as one inline string in the main session.
2. Prefer a clean-context worker/subagent write with only the required inputs.
3. Or generate the document in bounded sections with sequential append calls, keeping each section below the existing large-write threshold.
4. Still apply the existing chunked/temp-file write mechanics inside the chosen path.
```

- [ ] **Step 2: Keep the existing write-safety sequence intact**

Retain the current `## Core rule`, `## Large-write threshold`, `## Safe sequence`, Python example, Windows notes, and `## Decision test` structure. The new section should add a pre-flight guard, not replace the existing temp-file/chunked write safety net.

- [ ] **Step 3: Update the decision test to stop before inline composition starts**

Replace the current decision test with:

```markdown
## Decision test

If you would be tempted to compose a large document inline in the main session context, stop and route to a clean-context worker/subagent or section-by-section append path before composition starts.
```

- [ ] **Step 4: Extend the agent prompt so the trigger also reflects context pressure**

Update `default_prompt` in `agents/openai.yaml` so the trigger line says the agent should choose a non-inline route when the write is large *or* when composing it inline would risk exhausting the remaining context. Keep the prompt short and operational:

```yaml
default_prompt: Use /safe-large-file-writing when a text write may exceed the safe threshold or when inline composition itself would risk consuming the remaining context. Estimate line count and byte size before writing, avoid composing the full document inline, use a clean-context worker/subagent or bounded append path for risky writes, validate the completed temp file, and atomically replace the target only after validation.
```

### Task 2: Regenerate and validate the projected marketplace outputs

**Files:**
- Regenerated: `codex-marketplace/plugins/house-skills/skills/safe-large-file-writing/SKILL.md`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/safe-large-file-writing/agents/openai.yaml`
- Regenerated: `generated/skill-zips/house-skills/safe-large-file-writing/skill.zip`
- Regenerated: `generated/skill-zips/registry.json`

**Interfaces:**
- Consumes: the updated canonical source skill from Task 1.
- Produces: refreshed marketplace projection files and the corresponding generated skill-zip registry entry.

- [ ] **Step 1: Rebuild the targeted skill artifacts**

Run:

```bash
py -3 tools/update_skill_artifacts.py --skill house-skills/safe-large-file-writing
```

Expected result: the `house-skills` projection surface and `generated/skill-zips/house-skills/safe-large-file-writing/skill.zip` are refreshed from the updated source, not hand-copied.

- [ ] **Step 2: Check the deterministic generation and validation ladder**

Run:

```bash
py -3 tools/materialize_projection.py --check
py -3 tools/update_skill_artifacts.py --check
py -3 tools/validate_skill_zips.py
py -3 tools/generate_marketplace.py --check
py -3 tools/generate_repo_index.py --check
py -3 tools/validate_marketplace.py
git diff --check
```

Expected result: the projected skill tree, generated zip registry, marketplace manifest, repo index, and whitespace/pattern checks all pass. If `validate_marketplace.py` still reports the known unrelated `adventures-pack` asset gap from earlier `safe-large-file-writing` work, record it as a baseline blocker instead of widening the scope.

### Coverage Check

- Pre-composition guard and decision test: Task 1
- Canonical source skill and agent prompt: Task 1
- Projected marketplace surfaces and generated zip registry: Task 2
- Validation and drift checks: Task 2
