# `mark-skill-authoring` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Add a repository-local `mark-skill-authoring` skill that scaffolds and validates ordinary, vendored-source, and citation-only skills without modifying third-party authoring skills or treating the local skill as marketplace custody.

**Architecture:** Keep `mark-skill-authoring` tracked under `.agents/skills/mark-skill-authoring/`. Put its repeatable scaffolding behavior in one Python implementation with real Bash and PowerShell entrypoints. Let marketplace refresh tooling preserve the generic `mark-*` local lane, while marketplace-custodied output remains under `sources/first_party/skills/` and follows the existing projection pipeline.

**Tech Stack:** Python 3.13-compatible standard library, PyYAML already used by repository tooling, Bash, PowerShell, Markdown, YAML, existing marketplace generators and validators, pytest.

## Global Constraints

- Local skills use the reserved `mark-*` prefix and live under `.agents/skills/`; marketplace refresh must preserve them and exclude them from `.agents/skills/.provenance.json`.
- Marketplace-custodied skills use normal domain names and live under `sources/first_party/skills/<skill-name>/`.
- The three authoring lanes are exactly `first_party`, `skills-with-source`, and `skills-with-citation`.
- Source-backed authority evidence lives under `assets/authority/`; ordinary runtime routing must not link agents into that cold evidence by default.
- `skills-with-source` may contain `assets/authority/reference-source/` only after human redistribution approval; `skills-with-citation` must not contain vendored source text.
- `skills-with-citation` uses first-party clean-room synthesis with scholarly citations in `CITATIONS.md`; operational prose does not use inline citations by default.
- `mark-skill-authoring` is local custody: do not add it to `sources/first_party/`, `codex-marketplace/`, `custody-pack-registry.json`, or a plugin's `agents/openai.yaml`.
- Do not modify or overlay `superpowers-plus:writing-skills`.
- The scaffolder must refuse to overwrite an existing target, support read-only `--check`, and use LF-normalized UTF-8 output.
- The scaffolder must not download sources, make licensing decisions, add plugin registry entries, or regenerate marketplace projections.
- Freshness is manual in this implementation. Do not add network access or a CI-failing freshness check.
- Use TDD ordering: write each failing test, run it red, implement the smallest change, run it green, then commit the task.
- Design specs remain ignored under `.agents/superpowers/specs/`; this tracked plan is the durable implementation handoff.

## File Structure

| File | Responsibility |
| --- | --- |
| `.agents/skills/mark-skill-authoring/SKILL.md` | Local routing, lane selection, custody boundaries, composition with `writing-skills`, and cold-source rule |
| `.agents/skills/mark-skill-authoring/references/source-grounded-authoring.md` | Scholarly source use, clean-room synthesis, authority evidence, decomposition, and manual refresh |
| `.agents/skills/mark-skill-authoring/references/local-and-marketplace-custody.md` | Local `mark-*` versus marketplace source placement and handoff rules |
| `.agents/skills/mark-skill-authoring/templates/skill/SKILL.md` | Ready-to-fill skill template for all custody targets |
| `.agents/skills/mark-skill-authoring/templates/authority/authority.yaml` | Ready-to-fill authority manifest template |
| `.agents/skills/mark-skill-authoring/templates/authority/source-map.yaml` | Ready-to-fill source-section decomposition template |
| `.agents/skills/mark-skill-authoring/templates/authority/CITATIONS.md` | Scholarly citation and clean-room review template |
| `.agents/skills/mark-skill-authoring/scripts/new_skill.py` | Portable scaffolder implementation and CLI |
| `.agents/skills/mark-skill-authoring/scripts/new-skill.sh` | Bash argument-preserving entrypoint |
| `.agents/skills/mark-skill-authoring/scripts/new-skill.ps1` | PowerShell parameter-preserving entrypoint |
| `tools/install_agent_skills.py` | Preserve and validate local `mark-*` skills during marketplace refresh |
| `tools/validate_authority_assets.py` | Validate cold authority manifests, maps, citations, and lane/source shape |
| `.agents/skills/AGENTS.md` | Route the two skill-tree custody lanes |
| `.agents/doctrine/skill-standards-policy.md` | Marketplace-specific standards plus local-skill pointer |
| `.agents/guides/skill-authoring-guide.md` | Local authoring commands and handoff route |
| `tests/test_install_agent_skills.py` | Installer no-op and local-lane preservation regression tests |
| `tests/test_mark_skill_authoring_contract.py` | Local skill shape, lane, template, and scaffolder contract tests |
| `tests/test_validate_authority_assets.py` | Authority schema and lane validation tests |
| `tests/INDEX.md`, `.agents/skills/INDEX.md`, other mesh indexes | Generated navigation only |

### Task 1: Reserve and protect the `mark-*` local skill lane

**Files:**

- Modify: `tools/install_agent_skills.py:1-305`
- Modify: `.agents/skills/AGENTS.md:1-60`
- Modify: `tests/test_install_agent_skills.py`

**Interfaces:**

- Add `LOCAL_SKILL_PREFIX = "mark-"`.
- Add `_is_local_skill_dir(skill_dir: Path) -> bool`.
- Add `_validate_local_skill_dirs() -> list[Path]`.
- `_clean_orphan_skills(...)` must skip every directory for which `_is_local_skill_dir` is true.
- `main()` must validate local skills before any install or orphan-cleanup mutation and return `1` with an actionable error when a `mark-*` directory lacks a valid `SKILL.md`.

**Expected interim state:** The installer tests may be red until the orphan-cleanup guard is added. No marketplace skill content or provenance should change during this task.

- [x] **Step 1: Write the failing local-lane tests.**

Append these tests to `tests/test_install_agent_skills.py`, reusing the module import pattern already present there:

```python
def test_clean_orphan_skills_preserves_mark_skill(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    local_skill = skills_path / "mark-example"
    local_skill.mkdir(parents=True)
    (local_skill / "SKILL.md").write_text(
        "---\nname: mark-example\ndescription: Use when testing local skill custody.\n---\n\n# Example\n",
        encoding="utf-8",
    )

    with patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", skills_path):
        assert install_agent_skills._clean_orphan_skills([], synced_skill_names=set()) is False

    assert local_skill.is_dir()


def test_validate_local_skill_dirs_rejects_mark_skill_without_skill_md(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    (skills_path / "mark-invalid").mkdir(parents=True)

    with patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", skills_path):
        invalid = install_agent_skills._validate_local_skill_dirs()

    assert invalid == [skills_path / "mark-invalid"]
```

- [x] **Step 2: Run the focused tests and verify failure.**

Run:

```text
py -3 -m pytest tests/test_install_agent_skills.py::test_clean_orphan_skills_preserves_mark_skill tests/test_install_agent_skills.py::test_validate_local_skill_dirs_rejects_mark_skill_without_skill_md -q
```

Expected: FAIL because `mark-*` directories are currently treated as orphan skills and `_validate_local_skill_dirs` does not exist.

- [x] **Step 3: Implement the local-lane guard.**

Add the following imports and helpers to `tools/install_agent_skills.py`:

```python
from skill_zip_artifacts import validate_skill_markdown_frontmatter

LOCAL_SKILL_PREFIX = "mark-"


def _is_local_skill_dir(skill_dir: Path) -> bool:
    return skill_dir.is_dir() and skill_dir.name.startswith(LOCAL_SKILL_PREFIX)


def _validate_local_skill_dirs() -> list[Path]:
    if not AGENTS_SKILLS_PATH.is_dir():
        return []

    invalid: list[Path] = []
    for skill_dir in sorted(AGENTS_SKILLS_PATH.iterdir()):
        if not _is_local_skill_dir(skill_dir):
            continue
        try:
            validate_skill_markdown_frontmatter(skill_dir)
        except (FileNotFoundError, UnicodeDecodeError, ValueError) as exc:
            print(f"ERROR: local skill {skill_dir.relative_to(ROOT)} is invalid: {exc}")
            invalid.append(skill_dir)
    return invalid
```

Call `_validate_local_skill_dirs()` in `main()` after parsing arguments and before the installed-plugin early return:

```python
invalid_local_skills = _validate_local_skill_dirs()
if invalid_local_skills:
    return 1
```

Add the local-skill skip before the orphan condition in `_clean_orphan_skills`:

```python
        if _is_local_skill_dir(skill_dir):
            continue

        if skill_dir.name not in synced_skill_names:
```

- [x] **Step 4: Update `.agents/skills/AGENTS.md`.**

Replace the opening purpose/source-of-truth language with a two-lane contract:

```markdown
## Purpose

This directory contains two custody lanes:

- marketplace-derived skills copied from plugins with `INSTALLED_BY_DEFAULT`
  policy; and
- tracked repository-local skills under the reserved `mark-*` prefix.

Marketplace-derived skills are generated output. `mark-*` skills are authored
local custody and are not part of marketplace provenance.
```

Add this rule to the installation section:

```markdown
The installer validates and preserves every valid `mark-*` directory. It
never copies marketplace content over a `mark-*` name and never removes a
`mark-*` directory as an orphan.
```

- [x] **Step 5: Run the focused tests and the existing no-op regression.**

Run:

```text
py -3 -m pytest tests/test_install_agent_skills.py -q
```

Expected: PASS, including the existing forced byte-identical refresh test.

- [x] **Step 6: Commit the custody-lane change.**

```text
git add tools/install_agent_skills.py .agents/skills/AGENTS.md tests/test_install_agent_skills.py
git commit -m "fix: preserve repository-local mark skills"
```

### Task 2: Add the custody-aware scaffolder and local skill contract

**Files:**

- Create: `.agents/skills/mark-skill-authoring/SKILL.md`
- Create: `.agents/skills/mark-skill-authoring/references/source-grounded-authoring.md`
- Create: `.agents/skills/mark-skill-authoring/references/local-and-marketplace-custody.md`
- Create: `.agents/skills/mark-skill-authoring/templates/skill/SKILL.md`
- Create: `.agents/skills/mark-skill-authoring/templates/authority/authority.yaml`
- Create: `.agents/skills/mark-skill-authoring/templates/authority/source-map.yaml`
- Create: `.agents/skills/mark-skill-authoring/templates/authority/CITATIONS.md`
- Create: `.agents/skills/mark-skill-authoring/scripts/new_skill.py`
- Create: `.agents/skills/mark-skill-authoring/scripts/new-skill.sh`
- Create: `.agents/skills/mark-skill-authoring/scripts/new-skill.ps1`
- Create: `tests/test_mark_skill_authoring_contract.py`

**Interfaces:**

- CLI: `new_skill.py --name NAME --custody {local,marketplace} --lane {first_party,skills-with-source,skills-with-citation} [--check] [--allow-shared-checkout]`.
- `validate_request(name: str, custody: str, lane: str) -> None`.
- `destination_for(repo_root: Path, name: str, custody: str) -> Path`.
- `render_scaffold(name: str, custody: str, lane: str) -> dict[str, str]` where keys are relative output paths and values are LF-terminated UTF-8 content.
- `scaffold(repo_root: Path, name: str, custody: str, lane: str, check: bool) -> int`.

**Naming and output contract:**

| Request | Destination | Required output |
| --- | --- | --- |
| `--custody local --name mark-example --lane first_party` | `.agents/skills/mark-example/` | `SKILL.md`, no authority directory |
| `--custody marketplace --name ddd --lane skills-with-source` | `sources/first_party/skills/ddd/` | `SKILL.md`, `references/`, `assets/authority/` including `reference-source/` placeholder directory only if the user later adds approved source files |
| `--custody marketplace --name owasp --lane skills-with-citation` | `sources/first_party/skills/owasp/` | `SKILL.md`, `references/`, `assets/authority/` without `reference-source/` |

The scaffolder must reject a local name that does not start with `mark-`, reject a marketplace name that starts with `mark-`, reject unsupported lanes/custody values, reject invalid skill names, and refuse an existing destination. It must not write a registry entry or source file.

- [x] **Step 1: Write failing contract tests.**

Create `tests/test_mark_skill_authoring_contract.py` with tests for:

```python
def test_local_request_requires_mark_prefix():
    with pytest.raises(ValueError, match="local custody requires the mark- prefix"):
        new_skill.validate_request("ddd", "local", "first_party")


def test_marketplace_request_rejects_mark_prefix():
    with pytest.raises(ValueError, match="marketplace custody cannot use the mark- prefix"):
        new_skill.validate_request("mark-ddd", "marketplace", "skills-with-source")


def test_render_scaffold_uses_lane_specific_authority_shape():
    source_files = new_skill.render_scaffold("ddd", "marketplace", "skills-with-source")
    citation_files = new_skill.render_scaffold("owasp", "marketplace", "skills-with-citation")
    assert "assets/authority/authority.yaml" in source_files
    assert "assets/authority/CITATIONS.md" in source_files
    assert "assets/authority/reference-source/.gitkeep" in source_files
    assert "assets/authority/reference-source/.gitkeep" not in citation_files


def test_scaffold_check_does_not_write(tmp_path: Path):
    assert new_skill.scaffold(tmp_path, "mark-example", "local", "first_party", check=True) == 0
    assert not (tmp_path / ".agents/skills/mark-example").exists()
```

The test module must import the script by adding the skill’s `scripts/` directory to `sys.path`, matching existing repository tool tests.

- [x] **Step 2: Run the contract tests and verify failure.**

Run:

```text
py -3 -m pytest tests/test_mark_skill_authoring_contract.py -q
```

Expected: FAIL because the local skill and `new_skill.py` do not yet exist.

- [x] **Step 3: Implement the Python scaffolder.**

Implement `new_skill.py` with these exact behaviors:

```python
LANES = {"first_party", "skills-with-source", "skills-with-citation"}
CUSTODIES = {"local", "marketplace"}
LOCAL_PREFIX = "mark-"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def destination_for(repo_root: Path, name: str, custody: str) -> Path:
    if custody == "local":
        return repo_root / ".agents" / "skills" / name
    return repo_root / "sources" / "first_party" / "skills" / name
```

`validate_request` must enforce the table above and a maximum name length of 64 characters. `render_scaffold` must render the skill name, custody, and lane into frontmatter and templates without introducing `agents/openai.yaml`. `scaffold` must call the Git-derived repository and shared-checkout guard before writing, print every planned path in `--check` mode, create parent directories, and write each new file with `open(..., "x", encoding="utf-8", newline="\n")` so races cannot overwrite existing files. `--check` is read-only and may run against a temporary non-Git root in unit tests; write mode must use the full Git guard.

The Git guard must run `git rev-parse --show-superproject-working-tree` first, reject a non-empty result, compare absolute `--git-dir` and `--git-common-dir`, refuse a shared main checkout unless `--allow-shared-checkout` is present, and print a warning when that override is used.

- [x] **Step 4: Add real Bash and PowerShell entrypoints.**

`new-skill.sh` must resolve its own directory and `exec` the Python core with `"$@"`. `new-skill.ps1` must expose `-Name`, `-Custody`, `-Lane`, `-Check`, and `-AllowSharedCheckout`, construct the equivalent argument list, invoke `py -3 new_skill.py`, and exit with `$LASTEXITCODE`.

- [x] **Step 5: Write the local skill and templates.**

The local `SKILL.md` must:

- trigger on creating, reviewing, or refreshing a skill;
- require composition with `superpowers-plus:writing-skills`;
- route to the relevant lane and custody reference;
- state that `references/` is operational and `assets/authority/` is cold;
- state the no-inline-citation default;
- state the manual freshness boundary; and
- instruct the agent to use the scaffolder before authoring files.

The authority templates must contain the required keys `schema_version`, `lane`, `authority.title`, `authority.canonical_url`, `authority.pinned_source_url`, `authority.latest_check_url`, `authority.revision`, `authority.retrieved_at`, `authority.content_sha256`, `authority.license`, `authority.license_url`, `decomposition.reconciled_against`, and `decomposition.references`. `CITATIONS.md` must include scholarly citation, derivation boundary, attribution, and human review sections without inline citations in operational skill text.

- [x] **Step 6: Run core and entrypoint tests.**

Run:

```text
py -3 -m pytest tests/test_mark_skill_authoring_contract.py -q
bash .agents/skills/mark-skill-authoring/scripts/new-skill.sh --name mark-shell-example --custody local --lane first_party --check
powershell -NoProfile -File .agents/skills/mark-skill-authoring/scripts/new-skill.ps1 -Name mark-powershell-example -Custody local -Lane first_party -Check
```

Expected: PASS; both shell entrypoints print the same planned output shape and create no files in check mode.

- [x] **Step 7: Commit the local skill and scaffolder.**

```text
git add .agents/skills/mark-skill-authoring tests/test_mark_skill_authoring_contract.py
git commit -m "feat: add local skill authoring scaffolder"
```

### Task 3: Validate authority evidence without adding freshness networking

**Files:**

- Create: `tools/validate_authority_assets.py`
- Create: `tests/test_validate_authority_assets.py`
- Modify: `tools/check_marketplace.py:1-48`
- Modify: `tools/AGENTS.md` in the validation command inventory

**Interfaces:**

- `discover_authority_assets(root: Path) -> list[Path]`.
- `validate_authority_skill(skill_root: Path) -> list[str]`.
- `validate_authority_assets(root: Path) -> int`.
- CLI: `py -3 tools/validate_authority_assets.py` performs a read-only validation and returns `0` when all discovered authority assets are valid.

**Expected interim state:** The standalone validator and its tests can be added before it is wired into `check_marketplace.py`. During that interval, the standalone test must pass; the aggregate checker is expected to lack the new validation call until Step 5.

- [x] **Step 1: Write failing validator tests.**

Create fixtures under `tmp_path` rather than the repository’s real skill trees. Cover:

```python
def write_authority_fixture(root: Path, *, lane: str) -> Path:
    skill = root / "skill"
    authority = skill / "assets/authority"
    authority.mkdir(parents=True)
    (authority / "authority.yaml").write_text(
        "schema_version: 1\n"
        f"lane: {lane}\n"
        "authority:\n"
        "  title: Example Authority\n"
        "  canonical_url: https://example.com/authority\n"
        "  pinned_source_url: https://example.com/authority/v1\n"
        "  latest_check_url: https://example.com/authority\n"
        "  revision: v1\n"
        "  retrieved_at: '2026-07-20'\n"
        "  content_sha256: example-hash\n"
        "  license: CC-BY-4.0\n"
        "  license_url: https://creativecommons.org/licenses/by/4.0/\n"
        "decomposition:\n"
        "  reconciled_against: v1\n"
        "  references:\n"
        "    - path: references/example.md\n"
        "      source_sections: [Example]\n"
        "      content_mode: first_party_synthesis\n"
        "      load_when: [example topic]\n",
        encoding="utf-8",
    )
    (authority / "source-map.yaml").write_text(
        "schema_version: 1\n"
        "reconciled_against: v1\n"
        "references:\n"
        "  - path: references/example.md\n"
        "    source_sections: [Example]\n"
        "    content_mode: first_party_synthesis\n"
        "    load_when: [example topic]\n",
        encoding="utf-8",
    )
    (authority / "CITATIONS.md").write_text("# Citations\n\n## Human review\n", encoding="utf-8")
    return skill
```

```python
def test_source_lane_requires_reference_source(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-source")
    errors = validator.validate_authority_skill(skill)
    assert any("reference-source" in error for error in errors)


def test_citation_lane_rejects_vendored_source(tmp_path: Path):
    skill = write_authority_fixture(tmp_path, lane="skills-with-citation")
    (skill / "assets/authority/reference-source").mkdir(parents=True)
    (skill / "assets/authority/reference-source/source.pdf").write_bytes(b"source")
    errors = validator.validate_authority_skill(skill)
    assert any("must not contain" in error for error in errors)


def test_valid_source_and_citation_lanes_pass(tmp_path: Path):
    source_skill = write_authority_fixture(tmp_path / "source", lane="skills-with-source")
    (source_skill / "assets/authority/reference-source/source.txt").write_text("approved source", encoding="utf-8")
    citation_skill = write_authority_fixture(tmp_path / "citation", lane="skills-with-citation")
    assert validator.validate_authority_skill(source_skill) == []
    assert validator.validate_authority_skill(citation_skill) == []
```

The fixture must write complete YAML mappings for the required fields and create `source-map.yaml` and `CITATIONS.md`, so a passing test proves the actual schema rather than a missing-file shortcut.

- [x] **Step 2: Run the validator tests and verify failure.**

Run:

```text
py -3 -m pytest tests/test_validate_authority_assets.py -q
```

Expected: FAIL because the validator module and schema checks do not exist.

- [x] **Step 3: Implement the read-only validator.**

Use `yaml.safe_load` and these rules:

```python
LANES = {"skills-with-source", "skills-with-citation"}
CONTENT_MODES = {"first_party_synthesis", "licensed_adaptation", "verbatim_source"}
REQUIRED_AUTHORITY_FIELDS = {
    "title", "canonical_url", "pinned_source_url", "latest_check_url",
    "revision", "retrieved_at", "content_sha256", "license", "license_url",
}

def discover_authority_assets(root: Path) -> list[Path]:
    roots = [root / "sources/first_party/skills", root / ".agents/skills"]
    return sorted(
        authority.parent.parent.parent
        for skills_root in roots if skills_root.is_dir()
        for authority in skills_root.glob("*/assets/authority/authority.yaml")
    )
```

`validate_authority_skill` must require `authority.yaml`, `source-map.yaml`, and `CITATIONS.md`; require `schema_version: 1`; require `lane` to be one of the two source-backed lanes; require every field in `REQUIRED_AUTHORITY_FIELDS`; require `decomposition.reconciled_against` and a list-valued `decomposition.references`; require each reference entry to contain `path`, `source_sections`, `content_mode`, and `load_when`; and reject unsupported content modes.

For `skills-with-source`, require `reference-source/` to contain at least one non-hidden file. For `skills-with-citation`, reject any non-empty `reference-source/` directory. Do not fetch `canonical_url`, `pinned_source_url`, or `latest_check_url`; URL validity is limited to nonblank `http://` or `https://` strings. Print one error per invalid skill and return `1` if any errors exist.

- [x] **Step 4: Wire validation into the aggregate checker.**

Add this call in `tools/check_marketplace.py` before the final Git diff check:

```python
_run_tool("validate_authority_assets.py")
```

Document the command in `tools/AGENTS.md` as a non-mutating authority-shape check. State explicitly that it does not perform freshness networking and does not fail because a remote source has changed; it only validates recorded local evidence.

- [x] **Step 5: Run validator tests and the standalone command.**

Run:

```text
py -3 -m pytest tests/test_validate_authority_assets.py -q
py -3 tools/validate_authority_assets.py
```

Expected: PASS with no authority assets currently discovered until a future marketplace-custodied source-backed skill is added.

- [x] **Step 6: Commit authority validation.**

```text
git add tools/validate_authority_assets.py tests/test_validate_authority_assets.py tools/check_marketplace.py tools/AGENTS.md
git commit -m "feat: validate source-backed skill authority evidence"
```

### Task 4: Reconcile authoring guidance and metadata preservation tests

**Files:**

- Modify: `.agents/doctrine/skill-standards-policy.md`
- Modify: `.agents/guides/skill-authoring-guide.md`
- Create or modify: `tests/test_mark_skill_authoring_contract.py`
- Modify only if a regression test proves it necessary: `tools/normalize_first_party_skill_sources.py`

**Interfaces:**

- The local policy points to `.agents/skills/mark-skill-authoring/` for the authoring method.
- The local guide owns paths, commands, and publication handoff only.
- Existing normalizer behavior must preserve `metadata.use_with`; the current implementation already carries `use_with` through its optional metadata loop at `tools/normalize_first_party_skill_sources.py:272-274`.

**Expected interim state:** The guidance may temporarily contain both old and new routing text while the two documents are edited. The final task state must have one authoritative description of each rule and no stale `authoring-skills` path.

- [x] **Step 1: Write failing guidance and metadata tests.**

Add tests that assert:

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import normalize_first_party_skill_sources as normalize  # noqa: E402


def test_local_guidance_routes_to_mark_skill_authoring():
    standards = (ROOT / ".agents/doctrine/skill-standards-policy.md").read_text(encoding="utf-8")
    guide = (ROOT / ".agents/guides/skill-authoring-guide.md").read_text(encoding="utf-8")
    assert "mark-skill-authoring" in standards
    assert "mark-skill-authoring" in guide
    assert "authoring-skills" not in standards
    assert "authoring-skills" not in guide


def test_first_party_normalizer_preserves_use_with(tmp_path: Path):
    skill_md = tmp_path / "sample" / "SKILL.md"
    skill_md.parent.mkdir(parents=True)
    skill_md.write_text(
        "---\n"
        "name: sample\n"
        "description: Use when testing metadata preservation.\n"
        "metadata:\n"
        "  scope: metadata test\n"
        "  use_when:\n"
        "    - Use when testing metadata preservation.\n"
        "  do_not_use_when:\n"
        "    - Do not use when the test is unrelated.\n"
        "  use_with:\n"
        "    - superpowers-plus:writing-skills\n"
        "license: MIT\n"
        "---\n\n# Sample\n",
        encoding="utf-8",
    )
    assert normalize._normalize_skill(skill_md, write=False) is False
```

The test must import `normalize_first_party_skill_sources` using the repository’s existing `tools/` path insertion pattern. Do not change the normalizer merely to move or rename an already-preserved field.

- [x] **Step 2: Run the guidance and metadata tests and verify the expected failure.**

Run:

```text
py -3 -m pytest tests/test_mark_skill_authoring_contract.py -q
```

Expected: the guidance assertions fail until the two local documents are routed to `mark-skill-authoring`; the normalizer regression passes against the existing implementation.

- [x] **Step 3: Update `.agents/doctrine/skill-standards-policy.md`.**

Keep marketplace standards authoritative for first-party source custody, frontmatter, projection metadata, word limits, and marketplace validation. Add this routing paragraph near the opening standards section:

```markdown
Use the local [`mark-skill-authoring`](../.agents/skills/mark-skill-authoring/SKILL.md)
skill with `superpowers-plus:writing-skills` when creating or reviewing a
skill. It owns the authoring lanes, custody-aware scaffolding, authority
evidence, scholarly citations, and clean-room boundaries. This policy remains
the authority for marketplace paths, projection metadata, and repository
validation.
```

Add a local-skill subsection defining `.agents/skills/mark-*` as tracked local custody, requiring normal local skill frontmatter, and excluding it from marketplace provenance. Do not duplicate the source decomposition or citation workflow in this policy.

- [x] **Step 4: Update `.agents/guides/skill-authoring-guide.md`.**

Replace its generic authoring workflow with this local route:

````markdown
## Authoring route

1. Use `writing-skills` for general skill TDD and discovery quality.
2. Use `mark-skill-authoring` when the skill needs lane selection, custody
   placement, source decomposition, scholarly citations, or scaffolding.
3. Use this guide for repository paths, commands, generated-surface rules, and
   publication handoff.

Scaffold a local skill with:

```text
bash .agents/skills/mark-skill-authoring/scripts/new-skill.sh --name mark-example --custody local --lane first_party
```

Scaffold a marketplace-custodied source-backed skill with:

```text
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name ddd --custody marketplace --lane skills-with-source
```
````

Keep the existing local rebuild, check, and publication commands, but remove copied explanations of authority custody and decomposition.

- [x] **Step 5: Run guidance, normalizer, and stale-reference checks.**

Run:

```text
py -3 -m pytest tests/test_mark_skill_authoring_contract.py -q
rg -n "authoring-skills|sources/first_party/skills/authoring-skills|repo-worker-pack/skills/authoring-skills" docs .agents tools tests
```

Expected: tests pass; the stale-reference search returns no active-document matches. References inside the ignored superseded spec are not implementation surfaces and are not a failure condition.

- [x] **Step 6: Commit guidance reconciliation.**

```text
git add .agents/doctrine/skill-standards-policy.md .agents/guides/skill-authoring-guide.md tests/test_mark_skill_authoring_contract.py
git commit -m "docs: route skill authoring through local mark skill"
```

### Task 5: Regenerate mesh, run the full validation stack, and publish the plan

**Files:**

- Modify only generated outputs written by repository generators, especially `.agents/skills/INDEX.md` and `tests/INDEX.md`.
- Create: `.agents/superpowers/plans/2026-07-20-mark-skill-authoring.md` (this plan)

**Interfaces:**

- `py -3 tools/generate_index_mesh.py` writes the repository mesh.
- `py -3 tools/rebuild_marketplace.py` runs the canonical local regeneration stack and must preserve `mark-*` local skills.
- `py -3 tools/check_marketplace.py` is the final non-mutating repository gate.

**Expected interim state:** Adding the local skill and test files makes generated indexes stale until the mesh generator runs. That stale state is expected only between the file-add and regeneration steps; the final committed state must have no generated drift.

- [x] **Step 1: Regenerate the local mesh.**

Run:

```text
py -3 tools/generate_index_mesh.py
```

Expected: `.agents/skills/INDEX.md`, `tests/INDEX.md`, and any other affected indexes include the new tracked files. Do not hand-edit an index.

- [x] **Step 2: Prove local skills survive the canonical rebuild.**

Run:

```text
py -3 tools/rebuild_marketplace.py
```

Expected: the default-installed marketplace skills refresh as usual, `mark-skill-authoring` remains present and byte-identical, no local skill appears in `.agents/skills/.provenance.json`, and generated marketplace surfaces remain current. If the rebuild reports a `mark-*` orphan or deletes a local skill, stop and fix Task 1 before continuing.

- [x] **Step 3: Run all required validation.**

Run:

```text
py -3 -m pytest tests/test_install_agent_skills.py tests/test_mark_skill_authoring_contract.py tests/test_validate_authority_assets.py -q
py -3 -m pytest tests/ -x
py -3 tools/check_marketplace.py
git diff --check
```

Expected: all tests pass, authority validation reports no invalid assets, the aggregate checker passes, and `git diff --check` is clean.

- [x] **Step 4: Perform the plan/spec coverage review.**

Verify the implementation against every approved design decision:

```text
rg -n "mark-skill-authoring|skills-with-source|skills-with-citation|assets/authority|CITATIONS.md|mark-\*|latest_check_url|no inline" .agents/skills/mark-skill-authoring docs .agents/guides tools tests
```

Confirm that no implementation file introduces a network freshness check, inline runtime citations, `agents/openai.yaml` for the local skill, a marketplace registry entry for `mark-skill-authoring`, or deletion of a `mark-*` directory.

- [x] **Step 5: Commit generated surfaces and the completed plan.**

```text
git add .agents/superpowers/plans/2026-07-20-mark-skill-authoring.md .agents/skills/INDEX.md tests/INDEX.md
git commit -m "docs: add mark skill authoring implementation plan"
```

- [x] **Step 6: Publish and verify the plan commit.**

```text
git push origin codex/authoring-skills-design
gh pr view 204 --json headRefOid,url,isDraft,state
```

Expected: the existing draft PR points to the pushed head SHA and includes the tracked plan. PR readiness and merge remain separate lifecycle steps after implementation and fresh-eyes review.

## Execution Confidence Assessment

**8/10.** The custody targets, lane values, scaffolder interface, installer guard, authority schema, local guidance ownership, validation commands, and expected generated-surface behavior are specified against current repository paths and tooling. Confidence is below 9 because the exact local frontmatter wording and the final authority-template prose still require implementation-time writing judgment, but the file paths, interfaces, safety boundaries, tests, and integration commands are concrete enough for task-by-task execution.

## Plan Self-Review

- **Spec coverage:** The plan covers local custody, three lanes, cold authority assets, scholarly citations, no-inline runtime behavior, manual freshness, scaffolding, Bash/PowerShell parity, metadata preservation, guidance ownership, mesh regeneration, and publication.
- **Placeholder scan:** The plan contains no deferred implementation step or unresolved task handoff. Fill-in fields exist only inside the generated authority templates, where they are the intended authoring surface.
- **Type consistency:** The named Python functions and CLI options are used consistently across tasks and tests.
- **Interim state:** Expected stale-index and pre-wiring validation states are explicitly documented; no task treats them as final success.
