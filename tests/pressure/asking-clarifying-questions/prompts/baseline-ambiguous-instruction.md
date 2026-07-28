# Baseline ambiguous instruction

You are an agent operating in the repo root `Z:\_agent-worktrees\agent-asset-marketplace\feature\asking-clarifying-questions`.

Read the skill at `sources/first_party/skills/asking-clarifying-questions/SKILL.md` and the related skills at `sources/first_party/skills/brainstorming/SKILL.md` and `sources/first_party/skills/risk-gates/SKILL.md`.

Scenario: The user instruction is 'rename the temp file'. The workspace has two files: `temp.txt` and `temp.log`. The new name is not given. This is reversible; no scope, authority, canon, safety, or irreversible mutation is at stake. There is a single missing fact (which file) and a single missing output shape (the new name).

Use the `asking-clarifying-questions` skill. Respond with the compact queue: next action, ambiguity, risk of guessing, recommendation/options, and exactly one concrete question. Do not use `brainstorming` or `risk-gates`, and do not proceed to rename.
