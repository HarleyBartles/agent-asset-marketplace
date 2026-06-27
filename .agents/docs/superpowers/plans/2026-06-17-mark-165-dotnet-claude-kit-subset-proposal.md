# dotnet-claude-kit Codex .NET subset proposal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Produce a provenance-safe subset proposal for a future Codex-native .NET skill/plugin pack, based on the live upstream `codewithmukesh/dotnet-claude-kit` release state, without repackaging any skills in this child.

**Architecture:** Treat upstream intake as source analysis only. Record the upstream ref, license basis, and provider-specific exclusions first, then choose a small technical subset that is already close to Codex/GPT compatibility. Keep Claude-only install, hook, slash-command, and MCP assumptions out of the first subset so MARK-166 can repack from a clean selection boundary.

**Tech Stack:** Markdown docs, provenance notes, Linear issue linkage, marketplace repo docs.

---

### Task 1: Record the upstream provenance basis

**Files:**
- Create: `provenance/dotnet-claude-kit.md`

- [x] **Step 1: Capture the live upstream anchor**

Record the inspected upstream repository, default branch, and commit:

```md
Upstream repository: `https://github.com/codewithmukesh/dotnet-claude-kit`
Default branch: `main`
Resolved commit: `9a9a91107596b3ac3ad1d0ad5ec5eef189e74515`
License: MIT
```

- [x] **Step 2: Record the provider-specific surfaces that are not Codex-native**

Call out the upstream surfaces that should stay out of the first Codex pack because they are Claude-specific or provider-specific:

```md
- `CLAUDE.md`
- `.claude-plugin/`
- `.codex/`
- `.cursor/`
- `.opencode/`
- `gemini-extension.json`
- `hooks/`
- `.mcp.json`
- `mcp-configs/`
- slash-command workflows under `skills/` such as `/tdd` and `/verify`
```

- [x] **Step 3: Keep the provenance claim narrow**

State that the proposal is a source intake and selection artifact, not a repackaging or endorsement of the full upstream kit.

### Task 2: Select the Codex-native first subset

**Files:**
- Modify: `provenance/dotnet-claude-kit.md`

- [x] **Step 1: Keep the technical foundation skills**

Select the skills that are broadly useful, low-risk to adapt, and not tied to Claude-only command plumbing:

```md
- `modern-csharp`
- `vertical-slice`
- `clean-architecture`
- `ddd`
- `ef-core`
- `testing`
```

- [x] **Step 2: Record why each skill belongs in the first slice**

Use this selection logic:

```md
- `modern-csharp`: baseline C# 14 language guidance with minimal provider coupling.
- `vertical-slice`: architecture and feature-folder guidance that transfers cleanly to Codex.
- `clean-architecture`: project-boundary guidance that stays valuable after provider adaptation.
- `ddd`: tactical domain modeling guidance that is still portable when trimmed of Claude-specific workflow text.
- `ef-core`: durable persistence guidance that is directly useful in .NET repos.
- `testing`: high-value test guidance that maps cleanly to Codex-native repo work.
```

- [x] **Step 3: Record the adaptation boundary for each kept skill**

Note the rewrite requirements:

```md
- Remove `CLAUDE.md`-specific setup language.
- Remove slash-command assumptions.
- Remove hook and plugin-install instructions.
- Rewrite any MCP or command-routing assumptions into Codex-neutral guidance.
```

- [x] **Step 4: Defer the workflow orchestrators explicitly**

Mark `tdd` and `verify` as deferred for the first Codex subset because they are workflow orchestrators with strong Claude command and validation-pipeline assumptions.

### Task 3: Recommend the next child issue shape

**Files:**
- Modify: `provenance/dotnet-claude-kit.md`

- [x] **Step 1: Name the likely target surfaces for MARK-166**

Recommend that the repack child create:

```md
- a new marketplace plugin root under `codex-marketplace/plugins/dotnet-kit/`
- matching canonical source custody under `sources/first_party/skills/dotnet-kit/`
- a source/provenance map that ties each imported skill back to the upstream commit and this proposal
```

- [x] **Step 2: State the subset boundary for the repack child**

Tell MARK-166 to repack only the six selected technical skills first, and to leave workflow orchestrators (`tdd`, `verify`) for a later Codex-native workflow decision.

- [x] **Step 3: Add the compatibility warning**

Record that upstream `CLAUDE.md`, slash-command workflows, hooks, and MCP-install assumptions must be stripped or rewritten instead of copied as-is.

### Task 4: Validate the proposal text

**Files:**
- None

- [x] **Step 1: Search for false originality claims**

Run:

```bash
rg -n "original work|authored here|first-party origin" provenance/dotnet-claude-kit.md
```

Expected: only the explicit provenance-safe boundaries and no claim that upstream kit content is original to this repo.

- [x] **Step 2: Run the repo validation that applies to docs-only changes**

Run:

```bash
py -3 tools/validate_marketplace.py
git diff --check
```

Expected: validation passes; diff check reports no whitespace or patch-format issues.
