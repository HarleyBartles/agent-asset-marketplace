---
name: using-superpowers-plus
description: Use when starting any conversation - establishes how to find and use skills,
  requiring skill invocation before ANY response including clarifying questions
metadata:
  source-id: using-superpowers-plus
  source-path: sources/first_party/skills/using-superpowers-plus/SKILL.md
  provenance-name: Using Superpowers Plus first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when starting any conversation - establishes how to find and use skills,
    requiring skill invocation before ANY response including clarifying questions
  use_when:
  - Use when starting any conversation to find and invoke the right skill.
  - Use when unsure whether a skill applies to the current task.
  - Use before any response or action when a workflow skill might be relevant.
  do_not_use_when:
  - Do not use when dispatched as a subagent with a specific task.
  - Do not use when user instructions explicitly override skill selection.
  - Do not use as a substitute for reading the chosen skill.
  use_before:
  - brainstorming
  - systematic-debugging
  - writing-plans
  - executing-plans
  - subagent-driven-development
  - using-git-worktrees
  - test-driven-development
  - verification-before-completion
  - finishing-a-development-branch
  - requesting-code-review
  - working-with-epics
  related_skills:
  - brainstorming
  - systematic-debugging
  - writing-plans
  - executing-plans
  - subagent-driven-development
  - using-git-worktrees
  - test-driven-development
  - verification-before-completion
  - finishing-a-development-branch
  - requesting-code-review
  - receiving-code-review
  - writing-skills
  - working-with-epics
  - repo-worker-base
  - base-doctrine
  - inspecting-the-environment
license: MIT
---

## Provenance

This skill is a first-party authored derivation of `obra/superpowers` v6.2.0, released under the MIT License. The original upstream snapshot is retained in `sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/using-superpowers/` for reference.

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — including clarifying questions, exploring the codebase, or checking files. If it turns out wrong for the situation, you don't have to use it.

**Before entering plan mode:** if you haven't already brainstormed, invoke the brainstorming skill first.

Then announce "Using [skill] to [purpose]" and follow the skill exactly. If it has a checklist, create a todo per item.

## Skill Priority

When multiple skills apply, process skills come first — they set the approach, then implementation skills (frontend-design, etc.) carry it out. Brainstorming and systematic-debugging are Superpowers' most common process skills, but the rule holds for any of them.

- "Let's build X" → superpowers:brainstorming first, then implementation skills.
- "Fix this bug" → superpowers:systematic-debugging first, then domain skills.

## Red Flags

These thoughts mean STOP—you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Bootstrap order

This skill is the generic workflow router for any repo that installs the
superpowers-plus skill pack. At session start, resume, or when the next action
is unclear, run these steps in order and then hand off.

1. **The invocation rule.** If a skill applies to the request, invoke it before
   any response or action. You do not have a choice if a skill matches.
2. **Inspect the environment.** Invoke `/inspecting-the-environment` if the
   current environment is unknown or may have changed. Record the shell, repo,
   branch, worktree, and available connectors. Do not route until the
   environment is known.
3. **Load doctrine.** Invoke `/base-doctrine` for cross-runtime invariants.
   For how local doctrine and user instructions shape routing, see
   [`references/repo-doctrine.md`](references/repo-doctrine.md).
4. **Classify the request.** Pick the smallest sufficient mode from
   [`references/bootstrap-routing.md`](references/bootstrap-routing.md).
5. **Route and stop.** Hand off to the owning skill. Do not load additional
   skills unless the current skill leaves a decision unresolved and the
   candidate skill directly owns it.

## Platform Adaptation

If your harness appears here, read its reference file for special instructions:

- Codex: `references/codex-tools.md`
- Pi: `references/pi-tools.md`
- Antigravity: `references/antigravity-tools.md`
- Gemini: `references/gemini-tools.md`

For the local-doctrine and user-instruction priority rules, see
[`references/repo-doctrine.md`](references/repo-doctrine.md).
