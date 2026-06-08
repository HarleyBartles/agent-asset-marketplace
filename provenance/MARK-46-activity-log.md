# MARK-46 Activity Log

## Start Posture

- Date: 2026-06-07
- Branch start: `main`
- Starting main SHA: `21894a1699d122688d25173397a36a52c49376de`
- Upstream inspected: `jeremylongshore/claude-code-plugins-plus-skills` at `e773501f1dfb409fc71fccdaf6ac2898fedf66d6`
- Source guard: inspected the pinned upstream tree under `sources/vendor/jeremylongshore/claude-code-plugins-plus-skills/e773501f1dfb409fc71fccdaf6ac2898fedf66d6/`
- Marketplace route used: `codex-marketplace/plugins/` plus `.agents/plugins/marketplace.json`

## Outcome Summary

Wrapped the compatible upstream installable bundles as Codex marketplace plugins:

- `codex-marketplace/plugins/fullstack-starter-pack`
- `codex-marketplace/plugins/ai-experiment-logger`
- `codex-marketplace/plugins/conversational-api-debugger`
- `codex-marketplace/plugins/design-to-code`
- `codex-marketplace/plugins/domain-memory-agent`
- `codex-marketplace/plugins/lumera-agent-memory`
- `codex-marketplace/plugins/pr-to-spec`
- `codex-marketplace/plugins/project-health-auditor`
- `codex-marketplace/plugins/slack-channel`
- `codex-marketplace/plugins/workflow-orchestrator`
- `codex-marketplace/plugins/x-bug-triage-plugin`

Each wrapper carries a `.codex-plugin/plugin.json`, an `assets/icon.svg`, and a
`SOURCE.md` with upstream path and commit evidence.

## Non-Codex-Compatible / Not Wrapped

- `ai-ml-engineering-pack`
- `creator-studio-pack`
- `devops-automation-pack`
- `security-pro-pack`

Concrete blocker: no clean wrapper source root was present in the pinned tree
during inspection, so there was no package boundary to vendor as a Codex
marketplace asset.

## Registry Updates

- `codex-marketplace/manifest.json`
- `.agents/plugins/marketplace.json`
- `tools/marketplace_utils.py`
- `tools/validate_marketplace.py`

## Validation

Pending. Run the repo validation commands after the edits are finalized and
before publication.

## MARK-60 Standalone Testing Skill Pack

## Start Posture

- Date: 2026-06-08
- Branch start: `mark-46-codex-wrappers`
- Starting main SHA: `e5aace1cb02e975e345744c35f28ee3d3936a858`
- Branch created: `mark-46-standalone-testing-skill-pack`
- Upstream inspected: `jeremylongshore/claude-code-plugins-plus-skills` at `e773501f1dfb409fc71fccdaf6ac2898fedf66d6`
- Source guard: inspected `plugins/saas-packs/skill-databases/replit/` as the standalone skill root and cross-checked `plugins/saas-packs/replit-pack/`
- Marketplace route used: `codex-marketplace/plugins/testing-skill-pack/` plus `.agents/plugins/marketplace.json`

## Outcome Summary

Created a new Codex marketplace plugin pack:

- `codex-marketplace/plugins/testing-skill-pack`

The pack imports 28 standalone Replit skill docs into per-skill directories
and records the two out-of-scope docs in the bundle manifest and source note:

- imported: `28`
- skipped: `2`
- blocked: `0`

## Skipped / Out of Scope

- `plugins/saas-packs/skill-databases/replit/replit-bounty-hunting.md`
- `plugins/saas-packs/skill-databases/replit/replit-edu-classroom.md`

Concrete reason: adjacent growth / education skills, not part of the testing and
operations proof slice.

## Registry Updates

- `codex-marketplace/manifest.json`
- `.agents/plugins/marketplace.json`
- `tools/marketplace_utils.py`
- `tools/validate_marketplace.py`

## Validation

Pending. Run the repo validation commands after the edits are finalized and
before publication.
