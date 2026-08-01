# Repo doctrine and user instructions

User instructions (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, direct requests),
repo-local doctrine (`.agents/doctrine/`, scoped `AGENTS.md`), and the active
skill all shape routing. If they explicitly conflict, follow this priority:

1. Explicit human instruction.
2. Repo-local doctrine and `AGENTS.md`.
3. This skill and the skill it routes to.
4. Default behavior.

Only skip a skill workflow when your human partner has explicitly told you to.
