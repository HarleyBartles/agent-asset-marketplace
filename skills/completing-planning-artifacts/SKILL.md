---
name: completing-planning-artifacts
description: Use when a repository adopts completed-artifact-custody or explicitly asks to apply that lifecycle while plans, specifications, roadmaps, or checkpoints are being completed or a new slice starts.
metadata:
  source-id: completing-planning-artifacts
  source-path: skills/completing-planning-artifacts/SKILL.md
  provenance-name: Completing Planning Artifacts first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Optional semantic completion and retirement guidance for planning artifacts.
  use_when:
    - the repository's standards record selects completed-artifact-custody.
    - a human explicitly asks to apply this lifecycle.
  do_not_use_when:
    - the repository has not adopted this lifecycle and no human requests it.
license: MIT
---

# Completing Planning Artifacts

Use this lifecycle only when the repository explicitly adopts `completed-artifact-custody` or a human requests it. An installed skill, visible marker, or another standard does not create that subscription. Otherwise, follow the repository's own planning-artifact policy.

The standard keeps plans, specifications, roadmaps, checkpoints, and similar files as in-flight execution artifacts through the PR that completes their work. Their completion and later retirement are separate decisions: the completing PR records canonical history; the first substantive successor slice retires eligible artifacts from its current base.

## Classify the whole artifact

At slice completion and successor-slice entry, inspect planning locations declared by the repository and artifacts linked from the active plan, issue, PR, or roadmap. Follow links to related artifacts when they clarify scope. Use markers and checkboxes as clues to investigate, not as the discovery gate or decision.

For each artifact, classify its full governed scope as **complete**, **active or mixed**, **explicitly abandoned**, or **uncertain**. Compare the artifact's obligations with repository evidence such as current implementation, tests, accepted delivery records, linked issues, and future obligations. A merged PR is useful evidence, but verify that it delivered the artifact's full scope.

- A plan can be complete even when its checkboxes remain unchecked or its completion marker is absent, if evidence shows the entire governed scope shipped.
- Checked boxes, a `complete` state, or `completed-awaiting-retirement` do not prove completion when implementation, test, issue, or delivery evidence contradicts them.
- Classify a child plan against its own scope. A completed child may be retired while its parent roadmap remains active; keep the parent and future plans that still govern work.
- Treat abandonment as an explicit decision. Inactivity, rejected scratch work, or a deletion request alone does not establish abandonment.
- If the evidence leaves the artifact's actual state uncertain, or durable-content custody is unclear, do not retire it yet. Use `cleanup-custody` to resolve that specific uncertainty. When the evidence clearly shows missing delivery or active blocked work, classify it as active or mixed and preserve it.

## Completing-slice lane

Before handing off a substantially complete PR:

1. Verify implementation, required tests, review, and delivery evidence against each artifact's whole scope.
2. Promote any enduring architecture decisions to the repository's ADR home and operating rules to current doctrine, runbooks, or playbooks.
3. Update an artifact's state or checkboxes only as needed to make its record accurate. A marker can help later discovery, but it is optional and never substitutes for semantic discovery.
4. Keep the planning artifacts that governed the work in the completing PR through merge. Under squash merge, deleting them before merge loses them from canonical Git history.

## Successor-slice ingress lane

After refreshing the required base and before substantive edits:

1. Confirm the repository adopted this standard or that the human requested it. Read the local certification and follow its declared route and safeguards.
2. Inspect the declared planning locations and linked artifacts. Classify each artifact semantically; do not require a marker or keyword to find a candidate.
3. Retire only artifacts whose full scope is complete or explicitly abandoned, whose durable knowledge has been promoted, and which are present in the successor slice's current base. Verify that the base is current `main`; branch-only files remain in their completing PR. If the completing PR is already merged and its artifact is in this successor's current base, retire eligible artifacts in this slice's first substantive commit. If this PR is completing the artifact, keep it through merge and defer retirement to a later successor slice.
4. Preserve active or mixed-scope artifacts, including a parent roadmap with future stages. A completed child plan can be retired independently when it no longer governs active work.
5. Remove stale links and generated indexes in the same retirement change. Make retirement the first substantive commit in the successor slice's eventual PR; do not create a cleanup-only PR.

If no later substantive slice occurs, completed artifacts may remain tracked without regaining authority. If concurrent successors target the same artifacts, the first merged PR retires them; later slices refresh their base and drop redundant deletions. Follow repository policy for optional convenience copies and scratch custody.

## Common mistakes

| Mistake                                                                 | Correct action                                                                                                    |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| “The plan has unchecked boxes, so the work is unfinished.”              | Compare the full obligations with implementation and delivery evidence; unchecked boxes are a cue, not a verdict. |
| “The marker says complete, so it is safe to delete.”                    | Verify the whole scope; contradictory source, tests, or delivery evidence blocks retirement.                      |
| “The roadmap is still active, so every completed child plan must stay.” | Assess each artifact's own scope; preserve the live roadmap and retire an eligible child independently.           |
| “This skill is installed, so the repo uses the standard.”               | Confirm explicit adoption or a human request, then follow local policy.                                           |
| “The PR asks for cleanup before Ready.”                                 | Follow the adopted lifecycle and preserve completing-slice artifacts through merge.                               |

The standard does not require a repository to install this skill, create markers, adopt a checker, or maintain any particular plan inventory. It requires the adopter to self-certify its route, semantic classification practice, promotion, and drift safeguards.
