# MARK-318 incomplete tool-surface discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a compact invariant to `inspecting-the-environment` that prevents agents from treating truncated or partial tool/capability listings as proof that a capability is unavailable.

**Architecture:** Keep the fix inside the first-party `inspecting-the-environment` skill source, then regenerate the projected Superpowers bundle artifacts from that source so the marketplace copy and generated zip stay aligned. The wording should stay general-purpose and behavior-shaping: incomplete listings are not negative evidence, focused discovery must continue, and uncertainty must remain open until the relevant surface is actually proven complete.

**Tech Stack:** Markdown skill source, Codex marketplace projection, generated skill zips, Python regeneration scripts, Linear issue tracking, GitHub draft PRs.

## Global Constraints

- Keep the change narrow and inside `inspecting-the-environment` unless source inspection proves another location is more correct.
- Do not add a new MCP-specific skill or a Linear/GitHub-specific tool table.
- Do not turn the skill into a long troubleshooting manual.
- Preserve the skill's core-quality tone: compact, direct, and behavior-shaping.
- Regenerate downstream artifacts with repo tooling instead of hand-editing generated output.
- Document the three adversarial eval scenarios required by the issue.

---

### Task 1: Inspect the current skill and choose the smallest insertion point

**Files:**
- Read: `sources/first_party/skills/inspecting-the-environment/SKILL.md`
- Read: `codex-marketplace/plugins/superpowers-plus/skills/inspecting-the-environment/SKILL.md`
- Read: `codex-marketplace/plugins/superpowers-plus/references/source-map.md`

**Interfaces:**
- Consumes: current skill wording, existing environment-inspection guidance, projection mapping.
- Produces: a concrete insertion point for the invariant and a decision on whether it belongs in a new subsection or an integrated paragraph.

- [ ] Read the current source and projected copy side by side.
- [ ] Identify the smallest place where incomplete-surface guidance fits without broadening the skill.
- [ ] Confirm the change stays generic and does not introduce Linear/GitHub/MCP-only doctrine.

### Task 2: Add the incomplete-surface invariant to the source skill

**Files:**
- Modify: `sources/first_party/skills/inspecting-the-environment/SKILL.md`

**Interfaces:**
- Consumes: the existing `Environment dimensions`, `Inspection rules`, and `Authority split` sections.
- Produces: one concise rule that tells agents to keep searching when a surface may be truncated, paginated, filtered, or scoped.

- [ ] Add a compact paragraph or subsection that says incomplete tool and connector listings are not negative evidence.
- [ ] Require continuation/readback or focused rediscovery before declaring a capability unavailable.
- [ ] Require search by action families rather than one guessed name.
- [ ] Preserve uncertainty when the full relevant surface has not been proven complete.

Proposed wording shape:

```markdown
Tool and connector listings may be truncated, paginated, filtered, or scoped. Absence from the visible portion is not proof that a capability is unavailable. If the needed tool is not visible, inspect any continuation or readback surface, retry discovery with a narrower server, namespace, connector, or query, and search likely action families before concluding the capability is unavailable. Only report a capability as unavailable after focused discovery; otherwise preserve uncertainty.
```

### Task 3: Regenerate the marketplace projection and generated zip artifacts

**Files:**
- Regenerated: `codex-marketplace/plugins/superpowers-plus/skills/inspecting-the-environment/SKILL.md`
- Regenerated: `generated/skill-zips/superpowers-plus/inspecting-the-environment/skill.zip`
- Regenerated: `generated/skill-zips/registry.json`

**Interfaces:**
- Consumes: the updated first-party source skill.
- Produces: the projected marketplace copy and generated skill zip that match the source update.

- [ ] Run `py -3 tools/update_skill_artifacts.py --skill superpowers-plus/inspecting-the-environment`.
- [ ] Verify the generated outputs only reflect the intended skill change.
- [ ] Confirm the registry entry updates cleanly if the skill zip hash changes.

### Task 4: Document and verify the adversarial eval scenarios

**Files:**
- Modify: `.agents/docs/superpowers/plans/2026-06-28-mark-318-incomplete-tool-surface-discovery.md`

**Interfaces:**
- Consumes: the updated skill wording.
- Produces: documented before/after eval cases that prove the invariant covers truncation, focused discovery, and unexpected naming.

- [ ] Record the truncated-list case where mutation tools are hidden until continuation or focused search is used.
- [ ] Record the focused-discovery case where only read/query tools exist after the narrower search.
- [ ] Record the unexpected-naming case where the needed action is found by family search rather than the first guessed name.

Eval cases to keep in the implementation record:

1. **Truncated list hides mutation tools**
   - Bad behavior: the agent says no update or save tools exist after reading only the visible truncated portion.
   - Expected behavior: the agent notices truncation, continues discovery, and keeps searching for mutation tools before concluding anything.

2. **Focused discovery proves only read tools exist**
   - Bad behavior: the agent jumps from a partial list to "no mutation tool exists."
   - Expected behavior: the agent reports "no mutation tool found after focused discovery" and preserves uncertainty if the surface is still not proven complete.

3. **Unexpected tool naming**
   - Bad behavior: the agent stops after the first guessed name does not match.
   - Expected behavior: the agent searches action families such as read/query and mutation names until the capability is found or bounded uncertainty remains.

## Validation

- `py -3 tools/update_skill_artifacts.py --skill superpowers-plus/inspecting-the-environment`
- `py -3 tools/update_skill_artifacts.py --check`
- `py -3 tools/validate_marketplace.py`
- `git diff --check`

## Return Contract

When this plan is executed, return:

- the exact files changed;
- the final wording summary;
- whether the guidance stayed inside `inspecting-the-environment`;
- the three adversarial eval results;
- the validation output;
- any remaining uncertainty that still needs follow-up.
