# ECC Skills Inventory Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Inventory every upstream ECC skill under `skills/`, classify its agent-first relevance, and record the result as one concise repo-resident report.

**Architecture:** Pull the upstream skill list and metadata from the live `affaan-m/ECC` `main` branch, generate a concise markdown report under `docs/inventory/`, then add a matching implementation record and validation evidence in the repo. Keep the work read-only with respect to upstream source and avoid any projection/import changes.

**Tech Stack:** PowerShell, Python 3, Markdown, Git

---

### Task 1: Inspect upstream ECC skills and derive inventory data

**Files:**
- Read: `.tmp/ecc-upstream/skills/**/SKILL.md`
- Read: `docs/AGENTS.md`
- Read: `README.md`

- [x] **Step 1: Confirm the upstream `main` SHA and skill count**

Run:

```powershell
git ls-remote https://github.com/affaan-m/ECC.git refs/heads/main
py -3 - <<'PY'
import json, pathlib
root = pathlib.Path('.tmp/ecc-upstream/skills')
print(len(list(root.rglob('SKILL.md'))))
PY
```

- [x] **Step 2: Extract per-skill descriptions from front matter**

Run a small Python parser against the upstream `SKILL.md` files and store the results in a temp JSON summary for report generation.

- [x] **Step 3: Classify skills into the required relevance buckets**

Use the upstream names/descriptions plus the issue cues to separate `today`, `tomorrow`, `next-week`, `maybe-later`, and `probably-not`.

### Task 2: Write the repo-resident inventory report

**Files:**
- Add: `docs/inventory/ecc-agent-first-workflow-skills.md`

- [x] **Step 1: Build the markdown inventory report**

Include the upstream repo, inspected commit, total skill count, one row per skill, the classification bucket, rationale, likely custody/home, overlap notes, and a top-10 shortlist.

- [x] **Step 2: Keep the report concise and reviewer-friendly**

Prefer a compact table and short summary blocks over long prose. Do not paste upstream skill bodies.

### Task 3: Record validation and publication evidence

**Files:**
- Add: `docs/superpowers/records/2026-06-18-mark-235-record-ecc-skills-as-agent-first-workflow-drain-target.md`

- [x] **Step 1: Write the implementation record**

Capture the upstream commit inspected, the report path, the classification counts, the top-10 shortlist, and the validation commands/results.

- [x] **Step 2: Validate the repo change**

Run:

```powershell
git diff --check
```

- [x] **Step 3: Commit, push, and open the draft PR**

Commit the scoped report/record change set on `harleydbartles/mark-235-record-ecc-skills-as-agent-first-workflow-drain-target`, push it, and open a draft PR against `main`.
