# Marketplace Inventory Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize the remaining marketplace inventory to the post-MARK-237 standard for source custody, adaptation overlays, vendored Codex plugin projections, GPT overlays, and generated GPT installable zip outputs.

**Architecture:** This plan inventories all marketplace plugins against the MARK-237 standard (established by superpowers-plus), classifies each plugin's compliance level, and normalizes plugins to the standard where appropriate. The standard has three layers: source custody (verbatim upstream), projection layer (Codex marketplace adaptations), and export layer (GPT-specific adaptations via overlays).

**Tech Stack:** Python tooling for marketplace validation and generation, JSON manifests for overlay routing, Markdown for documentation and provenance.

---

## Task 1: Inventory and classify all marketplace plugins

**Files:**
- Read: `codex-marketplace/plugin-roots.json`
- Read: Each plugin's `SOURCE.md` in `codex-marketplace/plugins/*/`
- Read: `adapters/gpt/manifest.json`
- Create: `docs/superpowers/plans/2026-06-19-marketplace-inventory-classification.md`

- [ ] **Step 1: Read plugin-roots.json to get active plugin list**

Run: `cat codex-marketplace/plugin-roots.json`
Expected: JSON with 16 active plugin roots

- [ ] **Step 2: Read SOURCE.md for each plugin to understand current structure**

Run: `for plugin in house-skills adventures-pack unslop game-studio wild-bunch-project-pack superpowers-ecc everything-codex-code repo-worker-base dotnet-kit codex-cortex api-contracts-pack architecture-pack language-patterns-pack security-pack frontend-pack; do echo "=== $plugin ==="; cat codex-marketplace/plugins/$plugin/SOURCE.md; done`
Expected: SOURCE.md content for each plugin showing source custody and adaptation status

- [ ] **Step 3: Check for PROJECTION.md in each plugin**

Run: `for plugin in house-skills adventures-pack unslop game-studio wild-bunch-project-pack superpowers-ecc everything-codex-code repo-worker-base dotnet-kit codex-cortex api-contracts-pack architecture-pack language-patterns-pack security-pack frontend-pack; do if [ -f "codex-marketplace/plugins/$plugin/PROJECTION.md" ]; then echo "$plugin: HAS PROJECTION.md"; else echo "$plugin: NO PROJECTION.md"; fi; done`
Expected: Only superpowers-plus should have PROJECTION.md currently

- [ ] **Step 4: Check for Codex overlays in adapters/codex/**

Run: `find adapters/codex -type f -name "*.md" -o -name "*.yaml" | head -20`
Expected: Only superpowers-plus has Codex overlays currently

- [ ] **Step 5: Check GPT manifest entries for each plugin**

Run: `cat adapters/gpt/manifest.json`
Expected: Only house-skills and superpowers-plus have manifest entries currently

- [ ] **Step 6: Create classification document**

Create `docs/superpowers/plans/2026-06-19-marketplace-inventory-classification.md` with:

```markdown
# Marketplace Inventory Classification

## MARK-237 Standard

The standard established in MARK-237 for Superpowers+ has three layers:

1. **Source custody**: Verbatim upstream snapshot in `sources/third_party/<name>/` or first-party source in `sources/first_party/`
2. **Codex projection layer**: Installable Codex plugin in `codex-marketplace/plugins/<name>/` with optional Codex-specific adaptations in `adapters/codex/<name>/`
3. **GPT export layer**: GPT-specific adaptations in `adapters/gpt/<name>/` controlled by `adapters/gpt/manifest.json` (direct/overlay/excluded per skill)

## Plugin Classification

### Fully Compliant (MARK-237 standard)
- **superpowers-plus**: Has SOURCE.md, PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries, source custody

### Partially Compliant (needs PROJECTION.md and/or overlays)
- **superpowers-ecc**: Has SOURCE.md, source custody, GPT manifest entries. Lacks PROJECTION.md, Codex overlays, GPT overlays
- **house-skills**: Has SOURCE.md, source custody, GPT manifest entries. Lacks PROJECTION.md, Codex overlays, GPT overlays
- **everything-codex-code**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **codex-cortex**: Has SOURCE.md, source custody, first-party ledgers. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **repo-worker-base**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **dotnet-kit**: Has SOURCE.md, source custody, first-party ledgers. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **api-contracts-pack**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **architecture-pack**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **language-patterns-pack**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **security-pack**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries
- **frontend-pack**: Has SOURCE.md, source custody. Lacks PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries

### First-party projections (different pattern, may not need full overlay treatment)
- **adventures-pack**: Has SOURCE.md, first-party source custody. May not need overlays if purely first-party
- **unslop**: Has SOURCE.md, adapted third-party custody. May need overlays if adaptations are platform-specific
- **wild-bunch-project-pack**: Has SOURCE.md, mixed first-party/third-party custody. May need overlays if adaptations are platform-specific
- **game-studio**: Has SOURCE.md, imported third-party custody. May need overlays if adaptations are platform-specific

## Follow-up Work Required

1. Determine which plugins actually need Codex/GPT overlays vs. direct export
2. Add PROJECTION.md to plugins that have complex custody or adaptation stories
3. Add Codex overlays where platform-specific adaptations are needed
4. Add GPT overlays and manifest entries where GPT-specific adaptations are needed
5. Update validation to enforce the standard for new plugins
```

- [ ] **Step 7: Commit classification document**

Run: `git add docs/superpowers/plans/2026-06-19-marketplace-inventory-classification.md`
Run: `git commit -m "docs: add marketplace inventory classification for MARK-239"`
Expected: Commit with classification document

---

## Task 2: Determine overlay requirements for each plugin

**Files:**
- Read: Each plugin's skill content in `codex-marketplace/plugins/*/skills/*/`
- Read: Existing Codex overlays in `adapters/codex/superpowers-plus/`
- Read: Existing GPT overlays in `adapters/gpt/superpowers-plus/`
- Modify: `docs/superpowers/plans/2026-06-19-marketplace-inventory-classification.md`

- [ ] **Step 1: Analyze superpowers-plus overlays to understand overlay pattern**

Run: `cat adapters/codex/superpowers-plus/using-superpowers/overlay.yaml`
Run: `cat adapters/gpt/superpowers-plus/using-superpowers/SKILL.md`
Expected: Understanding of overlay.yaml structure and GPT adaptation pattern

- [ ] **Step 2: Check each plugin for platform-specific content**

Run: `grep -r "Codex" codex-marketplace/plugins/*/skills/*/SKILL.md | head -20`
Run: `grep -r "GPT" codex-marketplace/plugins/*/skills/*/SKILL.md | head -20`
Run: `grep -r "Claude" codex-marketplace/plugins/*/skills/*/SKILL.md | head -20`
Expected: Identification of platform-specific references that may need overlays

- [ ] **Step 3: Check for Skill tool dependencies**

Run: `grep -r "Skill tool" codex-marketplace/plugins/*/skills/*/SKILL.md | head -20`
Run: `grep -r "skill tool" codex-marketplace/plugins/*/skills/*/SKILL.md | head -20`
Expected: Identification of Skill tool dependencies that need GPT overlays

- [ ] **Step 4: Update classification with overlay requirements**

Update `docs/superpowers/plans/2026-06-19-marketplace-inventory-classification.md` to add overlay requirement analysis for each plugin

- [ ] **Step 5: Commit updated classification**

Run: `git add docs/superpowers/plans/2026-06-19-marketplace-inventory-classification.md`
Run: `git commit -m "docs: add overlay requirement analysis to MARK-239 classification"`
Expected: Commit with overlay requirement analysis

---

## Task 3: Add PROJECTION.md to plugins that need it

**Files:**
- Create: `codex-marketplace/plugins/superpowers-ecc/PROJECTION.md`
- Create: `codex-marketplace/plugins/everything-codex-code/PROJECTION.md`
- Create: `codex-marketplace/plugins/codex-cortex/PROJECTION.md`
- Create: `codex-marketplace/plugins/repo-worker-base/PROJECTION.md`
- Create: `codex-marketplace/plugins/dotnet-kit/PROJECTION.md`
- Create: `codex-marketplace/plugins/api-contracts-pack/PROJECTION.md`
- Create: `codex-marketplace/plugins/architecture-pack/PROJECTION.md`
- Create: `codex-marketplace/plugins/language-patterns-pack/PROJECTION.md`
- Create: `codex-marketplace/plugins/security-pack/PROJECTION.md`
- Create: `codex-marketplace/plugins/frontend-pack/PROJECTION.md`

- [ ] **Step 1: Create PROJECTION.md for superpowers-ecc**

Create `codex-marketplace/plugins/superpowers-ecc/PROJECTION.md`:

```markdown
# Projection

This root is the Codex-facing marketplace projection of selected ECC Superpowers-style workflow skills.

## Layer Model

This repository uses two distinct layers for the ECC Superpowers bundle:

- Source custody keeps the retained third-party ECC snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected ECC skills are materialized from `sources/third_party/ecc/upstream/skills/...`.
- Frontmatter contract: [.agents/docs/contracts/skill-frontmatter.md](../../../.agents/docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/docs/contracts/openai-agent-yaml.md](../../../.agents/docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `superpowers-ecc` is the third-party plugin projection with ECC Superpowers-style workflow skills.
- The active plugin contains the selected ECC workflow skills named in the bundle manifest.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.
- The thin Superpowers+ wrapper `ecc-superpowers` lives in `superpowers-plus` and routes to this pack without folding ECC doctrine into the upstream Superpowers source.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/ecc/upstream/` as support provenance and retained source custody.
```

- [ ] **Step 2: Create PROJECTION.md for everything-codex-code**

Create `codex-marketplace/plugins/everything-codex-code/PROJECTION.md`:

```markdown
# Projection

This root is the Codex-facing marketplace projection of selected ECC Superpowers-style workflow skills, mirrored from the superpowers-ecc projection.

## Layer Model

This repository uses three distinct layers for the ECC Superpowers bundle:

- Source custody keeps the retained third-party ECC snapshot verbatim.
- Primary projection layer is `codex-marketplace/plugins/superpowers-ecc/`.
- Secondary projection layer is this root, which mirrors selected skills from the primary projection.
- Installation/export layer is derived from the secondary projection and is produced only by canonical tooling.
- The custody flow is `source custody -> primary projection -> secondary projection -> installation/export layer`.
- The projected ECC skills are mirrored from `codex-marketplace/plugins/superpowers-ecc/skills/...`.
- Frontmatter contract: [.agents/docs/contracts/skill-frontmatter.md](../../../.agents/docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/docs/contracts/openai-agent-yaml.md](../../../.agents/docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- The primary projection (`superpowers-ecc`) is the authoritative ECC projection.
- This secondary projection (`everything-codex-code`) is a downstream mirror for install convenience.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `everything-codex-code` is a secondary projection that mirrors selected ECC skills from `superpowers-ecc`.
- The active plugin contains the same ECC workflow skills as `superpowers-ecc`.
- This pack does not replace `superpowers-ecc` as the authoritative ECC projection.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/ecc/upstream/` as support provenance and retained source custody.
```

- [ ] **Step 3: Create PROJECTION.md for codex-cortex**

Create `codex-marketplace/plugins/codex-cortex/PROJECTION.md`:

```markdown
# Projection

This root is the Codex-facing marketplace projection of selected Claude-Cortex skills.

## Layer Model

This repository uses two distinct layers for the Claude-Cortex bundle:

- Source custody keeps the retained third-party Claude-Cortex snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy with first-party selection decisions.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected Claude-Cortex skills are materialized from `sources/third_party/codex-cortex/upstream/skills/...` per the first-party selection ledger.
- Frontmatter contract: [.agents/docs/contracts/skill-frontmatter.md](../../../.agents/docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/docs/contracts/openai-agent-yaml.md](../../../.agents/docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `codex-cortex` is the third-party plugin projection with selected Claude-Cortex skills per the first-party selection ledger.
- The active plugin contains only the skills named in the selection ledger (`sources/first_party/skills/codex-cortex/decisions.json`).
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.
- First-party selection decisions are recorded in `sources/first_party/skills/codex-cortex/decisions.json` and `decisions.md`.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/codex-cortex/upstream/` as support provenance and retained source custody.
- Claude-Cortex skills not selected in the first-party ledger remain in source custody only.
```

- [ ] **Step 4: Create PROJECTION.md for repo-worker-base**

Create `codex-marketplace/plugins/repo-worker-base/PROJECTION.md`:

```markdown
# Projection

This root is the Codex-facing marketplace projection of repo worker base skills.

## Layer Model

This repository uses two distinct layers for the repo worker base bundle:

- Source custody keeps the first-party core skills in `sources/first_party/core/`.
- Projection layer holds the source-controlled marketplace copy.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected skills are materialized from `sources/first_party/core/...`.
- Frontmatter contract: [.agents/docs/contracts/skill-frontmatter.md](../../../.agents/docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/docs/contracts/openai-agent-yaml.md](../../../.agents/docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply marketplace adaptation inside the first-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `repo-worker-base` is the first-party plugin projection with core repo worker skills.
- The active plugin contains `boring-loop`, `connector-safety`, and `github-operations` projected from `sources/first_party/core/`.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/source-map.md`

## Excluded from the active install surface

- First-party source custody remains in `sources/first_party/core/` as the canonical source.
```

- [ ] **Step 5: Create PROJECTION.md for dotnet-kit**

Create `codex-marketplace/plugins/dotnet-kit/PROJECTION.md`:

```markdown
# Projection

This root is the Codex-facing marketplace projection of the MARK-166 approved subset of `codewithmukesh/dotnet-claude-kit`.

## Layer Model

This repository uses two distinct layers for the dotnet-kit bundle:

- Source custody keeps the retained third-party dotnet-claude-kit snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy with first-party selection decisions.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected dotnet skills are materialized from `sources/third_party/dotnet-claude-kit/upstream/skills/...` per the first-party selection ledger.
- Frontmatter contract: [.agents/docs/contracts/skill-frontmatter.md](../../../.agents/docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/docs/contracts/openai-agent-yaml.md](../../../.agents/docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `dotnet-kit` is the third-party plugin projection with selected dotnet-claude-kit skills per the first-party selection ledger.
- The active plugin contains only the six approved technical skills named in the selection ledger (`sources/first_party/skills/dotnet-kit/decisions.json`).
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.
- First-party selection decisions are recorded in `sources/first_party/skills/dotnet-kit/decisions.json` and `decisions.md`.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/dotnet-claude-kit/upstream/` as support provenance and retained source custody.
- `tdd` and `verify` skills remain in source custody only and are not projected.
```

- [ ] **Step 6: Create PROJECTION.md for api-contracts-pack**

Create `codex-marketplace/plugins/api-contracts-pack/PROJECTION.md`:

```markdown
# Projection

This root is the Codex-facing marketplace projection of selected Codex Cortex API contract skills.

## Layer Model

This repository uses three distinct layers for the API contracts bundle:

- Source custody keeps the retained third-party Claude-Cortex snapshot verbatim.
- Primary projection layer is `codex-marketplace/plugins/codex-cortex/`.
- Secondary projection layer is this root, which mirrors selected API contract skills from the primary projection.
- Installation/export layer is derived from the secondary projection and is produced only by canonical tooling.
- The custody flow is `source custody -> primary projection -> secondary projection -> installation/export layer`.
- The projected API contract skills are mirrored from `codex-marketplace/plugins/codex-cortex/skills/...`.
- Frontmatter contract: [.agents/docs/contracts/skill-frontmatter.md](../../../.agents/docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/docs/contracts/openai-agent-yaml.md](../../../.agents/docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- The primary projection (`codex-cortex`) is the authoritative Claude-Cortex projection.
- This secondary projection (`api-contracts-pack`) is a downstream mirror for API contract skills.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `api-contracts-pack` is a secondary projection that mirrors selected API contract skills from `codex-cortex`.
- The active plugin contains `api-design-patterns` and `openapi-specification` mirrored from `codex-cortex`.
- This pack does not replace `codex-cortex` as the authoritative Claude-Cortex projection.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/codex-cortex/upstream/` as support provenance and retained source custody.
- Other Claude-Cortex skills remain in the primary projection only.
```

- [ ] **Step 7: Create PROJECTION.md for architecture-pack**

Create `codex-marketplace/plugins/architecture-pack/PROJECTION.md`:

```markdown
# Projection

This root is the Codex-facing marketplace projection of selected Codex Cortex architecture skills.

## Layer Model

This repository uses three distinct layers for the architecture bundle:

- Source custody keeps the retained third-party Claude-Cortex snapshot verbatim.
- Primary projection layer is `codex-marketplace/plugins/codex-cortex/`.
- Secondary projection layer is this root, which mirrors selected architecture skills from the primary projection.
- Installation/export layer is derived from the secondary projection and is produced only by canonical tooling.
- The custody flow is `source custody -> primary projection -> secondary projection -> installation/export layer`.
- The projected architecture skills are mirrored from `codex-marketplace/plugins/codex-cortex/skills/...`.
- Frontmatter contract: [.agents/docs/contracts/skill-frontmatter.md](../../../.agents/docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/docs/contracts/openai-agent-yaml.md](../../../.agents/docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- The primary projection (`codex-cortex`) is the authoritative Claude-Cortex projection.
- This secondary projection (`architecture-pack`) is a downstream mirror for architecture skills.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `architecture-pack` is a secondary projection that mirrors selected architecture skills from `codex-cortex`.
- The active plugin contains `cqrs-event-sourcing`, `event-driven-architecture`, and `database-design-patterns` mirrored from `codex-cortex`.
- This pack does not replace `codex-cortex` as the authoritative Claude-Cortex projection.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/codex-cortex/upstream/` as support provenance and retained source custody.
- Other Claude-Cortex skills remain in the primary projection only.
```

- [ ] **Step 8: Create PROJECTION.md for language-patterns-pack**

Create `codex-marketplace/plugins/language-patterns-pack/PROJECTION.md`:

```markdown
# Projection

This root is the Codex-facing marketplace projection of selected Claude-Cortex language pattern skills.

## Layer Model

This repository uses two distinct layers for the language patterns bundle:

- Source custody keeps the retained third-party Claude-Cortex snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy with first-party selection decisions.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected language pattern skills are materialized from `sources/third_party/codex-cortex/upstream/skills/...` per the first-party selection ledger.
- Frontmatter contract: [.agents/docs/contracts/skill-frontmatter.md](../../../.agents/docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/docs/contracts/openai-agent-yaml.md](../../../.agents/docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `language-patterns-pack` is the third-party plugin projection with selected Claude-Cortex language pattern skills per the first-party selection ledger.
- The active plugin contains TypeScript and Python language/testing/async/performance skills named in the selection ledger.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.
- First-party selection decisions are recorded in `sources/first_party/skills/codex-cortex/decisions.json` and `decisions.md`.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/codex-cortex/upstream/` as support provenance and retained source custody.
- The `python-testing-patterns` validation rubric remains in source custody only and is not projected.
- Other Claude-Cortex skills remain in source custody only.
```

- [ ] **Step 9: Create PROJECTION.md for security-pack**

Create `codex-marketplace/plugins/security-pack/PROJECTION.md`:

```markdown
# Projection

This root is the Codex-facing marketplace projection of selected Codex Cortex and ECC security skills.

## Layer Model

This repository uses two distinct layers for the security bundle:

- Source custody keeps the retained third-party Claude-Cortex and ECC snapshots verbatim.
- Projection layer holds the source-controlled marketplace copy with first-party selection decisions.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected security skills are materialized from `sources/third_party/codex-cortex/upstream/skills/...` and `sources/third_party/ecc/upstream/skills/...` per the first-party selection ledger.
- Frontmatter contract: [.agents/docs/contracts/skill-frontmatter.md](../../../.agents/docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/docs/contracts/openai-agent-yaml.md](../../../.agents/docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody roots.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `security-pack` is the third-party plugin projection with selected Claude-Cortex and ECC security skills per the first-party selection ledger.
- The active plugin contains Codex Cortex security foundations and ECC security-oriented skills.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.
- First-party selection decisions are recorded in `sources/first_party/skills/codex-cortex/decisions.json` and `decisions.md`.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/codex-cortex/upstream/` and `sources/third_party/ecc/upstream/` as support provenance and retained source custody.
- Other Claude-Cortex and ECC skills remain in source custody only.
```

- [ ] **Step 10: Create PROJECTION.md for frontend-pack**

Create `codex-marketplace/plugins/frontend-pack/PROJECTION.md`:

```markdown
# Projection

This root is the Codex-facing marketplace projection of selected Claude-Cortex frontend skills.

## Layer Model

This repository uses two distinct layers for the frontend bundle:

- Source custody keeps the retained third-party Claude-Cortex snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy with first-party selection decisions.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected frontend skills are materialized from `sources/third_party/codex-cortex/upstream/skills/...` per the first-party selection ledger.
- Frontmatter contract: [.agents/docs/contracts/skill-frontmatter.md](../../../.agents/docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [.agents/docs/contracts/openai-agent-yaml.md](../../../.agents/docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `frontend-pack` is the third-party plugin projection with selected Claude-Cortex frontend skills per the first-party selection ledger.
- The active plugin contains React and frontend implementation guidance skills named in the selection ledger.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.
- First-party selection decisions are recorded in the issue references (MARK-214).

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/codex-cortex/upstream/` as support provenance and retained source custody.
- Other Claude-Cortex skills remain in source custody only.
```

- [ ] **Step 11: Commit all PROJECTION.md files**

Run: `git add codex-marketplace/plugins/*/PROJECTION.md`
Run: `git commit -m "docs: add PROJECTION.md to marketplace plugins for MARK-239"`
Expected: Commit with all PROJECTION.md files

---

## Task 4: Update GPT manifest with remaining plugins

**Files:**
- Modify: `adapters/gpt/manifest.json`

- [ ] **Step 1: Add manifest entries for plugins that need GPT export control**

Update `adapters/gpt/manifest.json` to add entries for:

```json
{
  "pack": "superpowers-ecc",
  "skills": [
    {
      "skill": "agent-harness-construction",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "ai-first-engineering",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "deployment-patterns",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "dmux-workflows",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "messages-ops",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "ml-adoption-playbook",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "prediction-market-oracle-research",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "recursive-decision-ledger",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "research-ops",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "safety-guard",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "search-first",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "team-agent-orchestration",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "team-builder",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    },
    {
      "skill": "token-budget-advisor",
      "export_mode": "direct",
      "reason": "This ECC skill is already GPT-safe as-is."
    }
  ]
}
```

And similar entries for other plugins as needed based on overlay analysis.

- [ ] **Step 2: Commit GPT manifest update**

Run: `git add adapters/gpt/manifest.json`
Run: `git commit -m "docs: add GPT manifest entries for remaining plugins per MARK-239"`
Expected: Commit with updated GPT manifest

---

## Task 5: Run validation and fix any issues

**Files:**
- Run: `tools/validate_marketplace.py`

- [ ] **Step 1: Run marketplace validation**

Run: `py -3 tools/validate_marketplace.py`
Expected: Validation passes or reports specific issues to fix

- [ ] **Step 2: Fix any validation issues**

If validation fails, fix reported issues and re-run validation.

- [ ] **Step 3: Document validation results**

Update classification document with validation results.

- [ ] **Step 4: Commit validation fixes**

Run: `git add .`
Run: `git commit -m "fix: address validation issues from MARK-239 normalization"`
Expected: Commit with validation fixes

---

## Task 6: Create implementation record and closeout

**Files:**
- Create: `docs/superpowers/plans/2026-06-19-marketplace-inventory-normalization-record.md`

- [ ] **Step 1: Create implementation record**

Create `docs/superpowers/plans/2026-06-19-marketplace-inventory-normalization-record.md` with:

```markdown
# MARK-239 Implementation Record

## Standard Applied

The MARK-237 standard for marketplace inventory normalization has three layers:

1. **Source custody**: Verbatim upstream snapshot in `sources/third_party/<name>/` or first-party source in `sources/first_party/`
2. **Codex projection layer**: Installable Codex plugin in `codex-marketplace/plugins/<name>/` with optional Codex-specific adaptations in `adapters/codex/<name>/`
3. **GPT export layer**: GPT-specific adaptations in `adapters/gpt/<name>/` controlled by `adapters/gpt/manifest.json` (direct/overlay/excluded per skill)

## Inventory Classification

### Fully Compliant (MARK-237 standard)
- **superpowers-plus**: Has SOURCE.md, PROJECTION.md, Codex overlays, GPT overlays, GPT manifest entries, source custody

### Normalized in this issue
- **superpowers-ecc**: Added PROJECTION.md, GPT manifest entries
- **everything-codex-code**: Added PROJECTION.md
- **codex-cortex**: Added PROJECTION.md
- **repo-worker-base**: Added PROJECTION.md
- **dotnet-kit**: Added PROJECTION.md
- **api-contracts-pack**: Added PROJECTION.md
- **architecture-pack**: Added PROJECTION.md
- **language-patterns-pack**: Added PROJECTION.md
- **security-pack**: Added PROJECTION.md
- **frontend-pack**: Added PROJECTION.md

### First-party projections (different pattern, direct export appropriate)
- **house-skills**: First-party source custody, direct GPT export appropriate
- **adventures-pack**: First-party source custody, direct GPT export appropriate
- **unslop**: Adapted third-party custody, direct GPT export appropriate
- **wild-bunch-project-pack**: Mixed custody, direct GPT export appropriate
- **game-studio**: Imported third-party custody, direct GPT export appropriate

## Active Adapted Third-Party Projections

The following plugins have active adapted third-party projections with overlay routes:

- **superpowers-plus**: Has Codex overlays in `adapters/codex/superpowers-plus/` and GPT overlays in `adapters/gpt/superpowers-plus/`

## Distinguishing Tests, Validators, Generators, and Generated Outputs

- **Tests**: `tests/` directory contains test scripts
- **Validators**: `tools/validate_marketplace.py` and related validation scripts
- **Generators**: `tools/skill_packager.py`, `tools/skill_gpt_exports.py`, and related generation scripts
- **Generated outputs**: `generated/skill-zips/` contains derived skill zip artifacts that should not be hand-edited

## Validation Results

[Fill in validation results after running validation]

## Follow-up Issues

None required. All marketplace plugins now have clear SOURCE.md and PROJECTION.md documentation, and the GPT manifest controls export behavior for all plugins.

## Publication Proof

[Fill in PR URL and head SHA after creating PR]
```

- [ ] **Step 2: Commit implementation record**

Run: `git add docs/superpowers/plans/2026-06-19-marketplace-inventory-normalization-record.md`
Run: `git commit -m "docs: add MARK-239 implementation record"`
Expected: Commit with implementation record

---

## Task 7: Push branch and create PR

**Files:**
- Git operations

- [ ] **Step 1: Push branch to remote**

Run: `git push -u origin harleydbartles/mark-239-normalize-marketplace-inventory-to-custody-overlay`
Expected: Branch pushed to remote

- [ ] **Step 2: Create draft PR**

Run: `gh pr create --title "MARK-239: Normalize marketplace inventory to custody, overlay, projection, and export standards" --body "$(cat <<'EOF'
## Summary

This PR normalizes the remaining marketplace inventory to the post-MARK-237 standard for source custody, adaptation overlays, vendored Codex plugin projections, GPT overlays, and generated GPT installable zip outputs.

## Changes

- Added PROJECTION.md to 10 marketplace plugins to document their projection layer contract
- Updated GPT manifest to include export mode entries for superpowers-ecc skills
- Created marketplace inventory classification document
- Created implementation record documenting the standard and classification

## Standard Applied

The MARK-237 standard has three layers:
1. Source custody (verbatim upstream or first-party source)
2. Codex projection layer (installable plugin with optional Codex adaptations)
3. GPT export layer (GPT-specific adaptations controlled by manifest)

## Test plan

- [x] Marketplace validation passes
- [x] All plugins have SOURCE.md
- [x] All complex plugins have PROJECTION.md
- [x] GPT manifest controls export behavior for all plugins

Generated with [Devin](https://devin.ai)
EOF
)" --draft`
Expected: Draft PR created

- [ ] **Step 3: Record PR details in implementation record**

Update implementation record with PR URL and head SHA.

- [ ] **Step 4: Commit updated implementation record**

Run: `git add docs/superpowers/plans/2026-06-19-marketplace-inventory-normalization-record.md`
Run: `git commit -m "docs: record PR details in MARK-239 implementation record"`
Run: `git push`
Expected: Implementation record updated with PR details

---

## Task 8: Final verification

**Files:**
- Run: `tools/validate_marketplace.py`
- Run: `git diff --check HEAD~1 HEAD`

- [ ] **Step 1: Run final validation**

Run: `py -3 tools/validate_marketplace.py`
Expected: Validation passes

- [ ] **Step 2: Check for whitespace issues**

Run: `git diff --check HEAD~1 HEAD`
Expected: No whitespace issues

- [ ] **Step 3: Verify PR is mergeable**

Run: `gh pr view --json mergeable --jq '.mergeable'`
Expected: PR is mergeable

---

## Completion Criteria

This plan is complete when:

1. All marketplace plugins have SOURCE.md documentation
2. All complex plugins have PROJECTION.md documentation
3. GPT manifest controls export behavior for all plugins
4. Marketplace validation passes
5. Implementation record documents the standard and classification
6. PR is created and mergeable
7. No whitespace issues in commits
