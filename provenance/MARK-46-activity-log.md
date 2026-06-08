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

Validation completed after the pack import and repo-index refresh.

## MARK-61 Supabase Platform Pack

## Start Posture

- Date: 2026-06-08
- Branch start: `mark-46-continue-upstream-drain-and-worker-doctrine`
- Starting main SHA: `8e04f6dd82938464e61cc62c70dc0ed327876c82`
- Branch created: `mark-46-continue-upstream-drain-and-worker-doctrine`
- Upstream inspected: `jeremylongshore/claude-code-plugins-plus-skills` at `e773501f1dfb409fc71fccdaf6ac2898fedf66d6`
- Source guard: inspected `plugins/saas-packs/skill-databases/supabase/` as the candidate inventory root and vendored the functional `plugins/saas-packs/supabase-pack/skills/` root
- Marketplace route used: `codex-marketplace/plugins/supabase-platform-pack/` plus `.agents/plugins/marketplace.json`

## Outcome Summary

Created a new Codex marketplace plugin pack:

- `codex-marketplace/plugins/supabase-platform-pack`

The pack imports 30 standalone Supabase skill docs into per-skill directories
and records the bundle ledger in the bundle manifest and source note:

- imported: `30`
- skipped: `0`
- blocked: `0`

## Registry Updates

- `codex-marketplace/manifest.json`
- `.agents/plugins/marketplace.json`
- `tools/marketplace_utils.py`
- `tools/validate_marketplace.py`

## Validation

Validation completed after the pack import and repo-index refresh.

## MARK-61 Vercel, Sentry, and OpenRouter Pack Tranche

## Start Posture

- Date: 2026-06-08
- Branch start: `mark-61-vercel-sentry-openrouter-pack-drain`
- Starting main SHA: `cd5ee21db1663a910af45e2fcfc5effc7c9aebfe`
- Branch created: `mark-61-vercel-sentry-openrouter-pack-drain`
- Upstream inspected: `jeremylongshore/claude-code-plugins-plus-skills` at `e773501f1dfb409fc71fccdaf6ac2898fedf66d6`
- Source guard: inspected `plugins/saas-packs/vercel-pack/`, `plugins/saas-packs/sentry-pack/`, and `plugins/saas-packs/openrouter-pack/` as the functional pack roots and used the corresponding `plugins/saas-packs/skill-databases/{vercel,sentry,openrouter}/` trees only as cross-check evidence
- Marketplace route used: `codex-marketplace/plugins/vercel-pack/`, `codex-marketplace/plugins/sentry-pack/`, and `codex-marketplace/plugins/openrouter-pack/` plus `.agents/plugins/marketplace.json`

## Outcome Summary

Created three new Codex marketplace plugin packs:

- `codex-marketplace/plugins/vercel-pack`
- `codex-marketplace/plugins/sentry-pack`
- `codex-marketplace/plugins/openrouter-pack`

Each pack imports 30 standalone skill docs into per-skill directories and records
the bundle ledger in the bundle manifest and source note:

- imported: `30` each
- skipped: `0` each
- blocked: `0` each

OpenRouter support-file correction:

- `codex-marketplace/plugins/openrouter-pack/skills/openrouter-compliance-review/references/openrouter-integration-security-questionnaire.md`
  - recreated locally because the pinned upstream tree referenced a missing support file path

## Registry Updates

- `codex-marketplace/manifest.json`
- `.agents/plugins/marketplace.json`
- `tools/marketplace_utils.py`
- `tools/validate_marketplace.py`

## Validation

Validation completed after the pack import and repo-index refresh:

- `py -3 tools/generate_marketplace.py` wrote `.agents/plugins/marketplace.json`
  and `codex-marketplace/manifest.json`
- `py -3 tools/validate_marketplace.py` passed
- `git diff --check HEAD~1 HEAD` passed

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

## MARK-63 Final Skill-Pack Drain Addendum

The remaining upstream standalone skill-pack families are now also preserved as
marketplace plugin packs:

- imported: `100` remaining `plugins/saas-packs/*-pack` families
- skipped: `0`
- blocked: `0`

Residual upstream skill-pack inventory after MARK-63:

- `0`

The next upstream drain step should move to plugin-package tranches only.
