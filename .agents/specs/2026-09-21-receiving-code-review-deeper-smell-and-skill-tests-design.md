# Receiving Code Review Deeper-Smell and Skill Tests Design

> **Status:** Proposed for human review.

## Problem

The current `receiving-code-review` skill stops after it verifies feedback,
evaluates the suggestion, implements the reported correction, and tests that
correction. That is sufficient for literal review satisfaction, but it does not
prompt the receiver to inspect whether a correct finding exposes a repeatable
failure mechanism in the repository. A competent agent can therefore repair one
manifest entry, unsafe call site, or duplicated check while leaving the
condition that will produce the same class of defect again.

The marketplace's skill-testing custody is also inconsistent. The repository
policy currently requires pressure scenarios at `assets/pressure-tests.md`,
which makes maintainer verification look like behavioural input to an invoked
skill. Other skill-owned tests sit at a skill root, while `iterative-review`
already keeps its test code and fixtures under `tests/`. The Agent Skills
specification permits additional directories but does not define a canonical
`tests/` lane. This repository needs its own explicit convention.

## Goal

Make code-review reception include one bounded deeper-smell inspection after a
finding is verified as correct, and prove that new behaviour with a blinded
RED/GREEN exercise in a fresh local Git repository.

At the same time, establish `tests/` at a skill root as this marketplace's
maintainer-facing verification lane, move existing misplaced test material
into that lane, and prevent new pressure-test material from returning to
`assets/` or a skill root.

## Success criteria

- A receiving agent still verifies feedback before acting and still fixes the
  reported instance correctly.
- When repository evidence exposes a repeatable mechanism, the agent inspects
  it and chooses the smallest justified response: in-scope prevention or an
  evidence-backed follow-up when prevention is consequential.
- The new guidance does not turn isolated mistakes into speculative redesign.
- A blinded baseline run demonstrates the current failure: correct local repair
  and verification followed by an unjustified stop at the specimen.
- A blinded treatment run on an identical fixture demonstrates transfer to a
  defect class other than manifest drift.
- Skill-owned tests, fixtures, rubrics, and stable evaluation inputs live under
  `<skill>/tests/`, ship with the skill, and remain outside ordinary skill
  invocation.
- Existing misplaced skill test material is relocated without reclassifying
  behavioural references or operational assets as tests.

## Design decisions

### 1. Add a structural deeper-smell step

The response pattern in the canonical
`codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/SKILL.md`
will add an explicit inspection between technical evaluation and response:

```text
READ -> UNDERSTAND -> VERIFY -> EVALUATE -> INSPECT -> RESPOND -> IMPLEMENT -> VERIFY
```

`INSPECT` asks whether the verified finding reveals a deeper smell. The
governing test is:

> Could another competent implementer, using the repository's current
> interfaces, workflow, and guidance, plausibly make the same class of mistake?

The skill will define three branches:

1. **No credible deeper smell:** correct and verify the reported instance.
2. **Credible, small, in-scope prevention:** correct the instance, add the
   smallest durable prevention, and prove the prevention addresses the defect
   class rather than only the reported specimen.
3. **Credible but consequential or out of scope:** make the independently safe
   local correction, report the evidenced mechanism, and propose a concrete
   follow-up instead of silently expanding authority.

The smell must be a causal mechanism supported by repository evidence, not an
imagined future risk. Representative indicators include duplicated truth,
unenforced invariants, incomplete multi-surface operations, unsafe interfaces,
unclear ownership, and missing boundary or postcondition checks. Preferred
prevention removes the opportunity, mechanically detects the class, or makes
the correct action the easy action. Prose reminders are the fallback when the
rule genuinely requires judgment.

The skill's common-mistakes table will name the existing failure directly:
fixing only the reviewed specimen without checking for an evidenced repeatable
mechanism. One compact example will use manifest drift to explain the concept,
but the behavioural proof will use a different defect class.

### 2. Define the clean RED before authoring the guidance

The clean RED is not a generally poor review response. It is competent literal
review satisfaction:

1. The feedback is correct and understood.
2. The agent verifies it against the repository.
3. The agent makes a technically sound local correction.
4. The agent adds or runs focused verification for that correction.
5. The repository contains reasonably discoverable evidence of a repeatable
   mechanism behind the defect.
6. The agent stops without investigating or naming that mechanism.

A run is not a valid RED if the agent misunderstands the reviewer, applies an
incorrect patch, omits ordinary verification, cannot reasonably discover the
mechanism, or notices the smell but lawfully declines a consequential redesign.
If the unmodified skill already produces the desired deeper-smell behaviour,
the fixture has not established RED and must not be used to justify the change.

### 3. Use a different defect class for transfer

The pressure fixture will model a small Python command-line package with
several command wrappers. Existing wrappers independently infer subprocess
success from output or error text rather than the process return code. The PR
under review adds another wrapper by following that existing pattern. A
reviewer correctly reports that the new wrapper can claim success when its
subprocess exits non-zero without diagnostic text.

The literal correction is intentionally straightforward: check the return code
in the reviewed wrapper and add a focused regression test. The deeper smell is
that subprocess-success semantics are duplicated across sibling wrappers. The
smallest durable prevention is a shared checked-execution boundary with one
class-level regression test and migration of the small wrapper family to that
boundary. The fixture will contain no unrelated subprocess concerns such as
retries, timeouts, telemetry, or a general execution framework.

This scenario proves transfer because the skill may use manifest drift as an
explanatory example while the examination requires recognition of duplicated
process-result semantics.

### 4. Materialize an ordinary local PR repository

The committed fixture is a recipe, not a nested repository. It will live at:

```text
codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/
└── tests/
    └── deeper-smell/
        ├── README.md
        ├── materialize.py
        ├── review-comment.md
        ├── rubric.md
        ├── feature.patch
        └── seed/
```

`materialize.py` will default to a read-only check and require an explicit
apply mode, empty destination, and skill-source path before it writes. It will
create a neutral, ordinary-looking project such as
`signal-exporter`, initialize Git, commit the base state on `main`, install the
selected `receiving-code-review` skill into the fixture's base tree, create a
feature branch, apply and commit `feature.patch`, and leave a clean PR-head
working tree. The installed skill is part of both base and feature history, so
`git diff main...HEAD` shows only the implementation under review.

The materializer is maintainer test code. It must be deterministic apart from
irrelevant Git timestamps, fail closed on a non-empty destination, avoid remote
configuration, and expose no network or external connector surface. Generated
repositories and run output live under the repository's resolved off-repo
scratch root and are removed after the campaign.

The subagent receives a fresh context, the fixture repository as its working
directory, an instruction to read the installed `receiving-code-review` skill,
and one blocking inline-review comment naming the changed file and line. It is
not shown the fixture recipe, rubric, RED/GREEN terminology, prior conversation,
or expected deeper smell.

### 5. Compare the existing and candidate skills on the same recipe

The RED repository is materialized from the current skill before the behavioural
addition. Its subagent patch, test output, searches, and final report are kept
only as transient scratch evidence for the current change. The run record names
the fixture-recipe digest, baseline-skill digest, base commit, PR-head commit,
model/profile selection, and rubric version without retaining a full transcript.

After the RED is confirmed, the minimal skill addition is authored. GREEN uses
a newly materialized repository from the same seed and feature patch, with only
the installed skill content changed to the candidate version. Model, reasoning,
prompt, tools, repository shape, review comment, and scoring rubric stay equal.
Its run record captures the corresponding candidate-skill digest and fixture
identities so the comparison can prove that the skill content was the sole
intentional treatment difference.

GREEN requires observable evidence that the agent:

- fixes and verifies the reported wrapper defect;
- inspects sibling uses of the same success-detection pattern;
- names duplicated process-result semantics as the repeatable mechanism;
- implements only the shared checked-execution prevention;
- adds proof at the shared invariant boundary; and
- avoids unrelated subprocess redesign.

Mentioning a possible systemic issue without inspecting it is not GREEN.
Redesigning the command framework is also not GREEN. One bounded paired
pressure proof is sufficient unless it exposes a concrete wording or fixture
failure; any such failure returns the change to refinement and re-proof.

Stable prompts, fixture inputs, and the rubric remain tracked. Full model
transcripts, score directories, copied model metadata, and generated Git
repositories do not become repository evidence.

### 6. Establish the marketplace `tests/` convention

`.agents/doctrine/skill-standards-policy.md` will add `tests/` to this
repository's skill-directory convention:

```text
tests/  # Optional: maintainer verification, fixtures, rubrics, and evaluations
```

The policy will state:

- `tests/` is permitted but undefined by the Agent Skills specification; this
  repository defines its meaning locally.
- It contains verification of the skill itself, including automated tests,
  evaluation scenarios, fixture recipes, rubrics, and stable expected results.
- It is shipped with canonical and installed skill directories so maintainers
  can test the skill in the environment where it is installed.
- It is not part of the skill's behavioural interface. Ordinary invocation
  must not require or direct the agent to load `tests/`.
- Transient run outputs and generated test repositories remain off-repo.
- `assets/` remains for resources used during ordinary skill execution;
  `references/` remains on-demand behavioural knowledge; `scripts/` remains
  runtime capability code.

The pressure-testing section of that policy and `tests/pressure/README.md` will
replace `assets/pressure-tests.md` with skill-root `tests/` custody. The GREEN
instructions will load the candidate `SKILL.md` and its behavioural resources,
not the rubric or expected result. Maintainer orchestration may read the
skill-root test recipe and rubric.

Repository-root `tests/pressure/` remains the home for shared campaign
orchestration, generic run instructions, and repository-wide validation of
pressure artifacts. Skill-root `tests/` is the portable source of a particular
skill's fixture, prompt inputs, rubric, and deterministic assertions. A
repo-root campaign adapter may point to those skill-owned files, but it must not
duplicate or become a second source of truth for them.

Focused repository contract tests will assert the new doctrine and reject the
retired `assets/pressure-tests.md` convention. Packaging/projection validation
will prove that a tracked skill-root `tests/` tree survives marketplace
generation and installed-skill refresh byte-for-byte. The tests lane will not
be added to runtime skill discovery or automatic skill loading.

### 7. Normalize existing test-material custody

The repository-wide inventory found 84 declared skill directories across all
19 active plugin roots, with no missing or undeclared skill directories. Six
tracked files in two skills require relocation:

```text
using-playwright-mcp/assets/pressure-tests.md
  -> using-playwright-mcp/tests/pressure-tests.md

systematic-debugging/test-academic.md
  -> systematic-debugging/tests/scenarios/academic.md

systematic-debugging/test-pressure-1.md
  -> systematic-debugging/tests/scenarios/pressure-1.md

systematic-debugging/test-pressure-2.md
  -> systematic-debugging/tests/scenarios/pressure-2.md

systematic-debugging/test-pressure-3.md
  -> systematic-debugging/tests/scenarios/pressure-3.md

systematic-debugging/CREATION-LOG.md
  -> systematic-debugging/tests/evidence/creation-log.md
```

`iterative-review/tests/` already conforms and remains unchanged.

Similarly named behavioural material remains in place: the subagent-selection
pressure scenarios are runtime decision guidance; the `writing-skills`
methodology and worked example teach skill authors; DeepWiki golden questions,
Linear golden-gate guidance, writing-profile goldens, and testing profiles are
runtime references or data rather than tests of their containing skills.

## Source and generated surfaces

Authored changes belong in canonical plugin skill trees and repository doctrine.
Installed `.agents/skills/` copies, marketplace manifests, indexes, and mesh
surfaces remain generated outputs. Normal regeneration must preserve complete
skill directories, including the new `tests/` lane; no installed projection is
edited by hand.

Expected authored surfaces include:

- `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/`
- `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/`
- `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/`
- `.agents/doctrine/skill-standards-policy.md`
- `tests/pressure/README.md`
- focused repository contract or marketplace-projection tests.

Generated surfaces include the installed skill projections, marketplace
inventory/manifests, and mesh/index files owned by repository commands.

## Failure handling

- If the fixture cannot produce the defined competent-local-fix RED, stop. Do
  not weaken the rubric or claim the new guidance is necessary from that run.
- If GREEN fixes only the specimen, refine the minimal skill wording against
  the observed omission and rerun the paired proof.
- If GREEN overreaches, tighten the evidence and authority branches rather than
  accepting deeper-smell recognition alone.
- If RED and GREEN differ in anything besides the skill content, discard the
  comparison and rematerialize both sides.
- If packaging drops, mutates, or runtime-loads `tests/`, treat that as a
  convention implementation failure and repair the owning generator or
  validator before publication.

## Validation

Validation will include:

- deterministic tests of the fixture materializer's branch, commit, diff,
  cleanliness, and refusal of non-empty destinations;
- a clean RED recorded before editing the skill;
- one bounded clean GREEN after the minimal skill edit;
- focused repository assertions for the `tests/` doctrine and retirement of
  `assets/pressure-tests.md`;
- projection checks proving skill-root tests survive canonical marketplace and
  installed-skill generation;
- focused tests for any changed helper or validator;
- the repository's normal staged hooked commit gate on the final tree; and
- self-review of the complete change before Ready status.

## Non-goals

- Mandatory root-cause analysis for every review comment.
- Turning typos or unique mistakes into architecture work.
- Giving review feedback authority to expand implementation scope silently.
- Building a general-purpose evaluation service or permanent GitHub fixture
  repository.
- Loading test recipes or rubrics during ordinary skill invocation.
- Moving behavioural references merely because their names contain `test`,
  `pressure`, `golden`, or `scenario`.
- Retaining full model transcripts or generated fixture repositories in Git.
- Backfilling test suites for every marketplace skill in this change.

## Planning handoff

The implementation plan should preserve this order of authority: establish the
fixture and observe the current clean RED before changing the skill; make the
minimal behavioural addition; prove GREEN on a newly materialized equivalent
repository; then complete the convention migration, projection proof, generated
refresh, and repository gate. The plan must not treat the proposed skill wording
in this design as pre-implemented source or skip the observed RED requirement.
