# Source partitioning

Load this reference to label what kind of support a Rooms, Mostly claim has and to prevent evidence from being laundered into a stronger truth lane.

This reference defines source-basis labels and partitioning posture. Do not select source routes or inspect connectors from this file alone.

## Route-capability labels

Load the route-capability labels below only when route capability matters, such as when the response must distinguish exact source reads, indexed search discovery, uploaded-file evidence, local evidence, unavailable routes, route failures, or source-coverage limits.

- `exact-repository-read`: evidence came from a capability that can read a known current repository object, such as a named file path, issue, comment, commit, branch, pull request, or comparison.
- `indexed-repository-discovery`: evidence came from a capability that can search the target repository or repository set broadly for unknown files, stale terms, duplicate issues, or corpus-style matches.
- `uploaded-file-evidence`: evidence came from a user-provided file or file-library surface, not from current repository state.
- `local-worker-evidence`: evidence came from a local worker or disk report and remains reported unless independently observable in the current session.
- `report-evidence`: evidence came from a report, receipt, return, or status note rather than from the underlying source surface.
- `route-unavailable`: the needed route capability was not available in the current runtime.
- `route-failed`: the needed route capability was available but failed at runtime.
- `scope-mismatch`: a route existed but did not expose the needed repo, branch, issue, file set, or source family.

Indexed discovery is useful for recall, stale-pattern sweeps, duplicate hunting, and finding unknown files or issues. It is not proof of absence unless the search scope is well defined and the response explicitly limits the claim to that scope.

Exact repository reads are useful for current state of known targets. They do not replace broad indexed discovery when the task requires a corpus-wide sweep.

Uploaded files and reports can be valuable mirrors or handoff artifacts. They do not become current repository truth unless the task is explicitly scoped to them or they are corroborated by an appropriate source route.

Do not treat the mere presence of a connector, uploaded file, source, or tool namespace as a reason to inspect routes. Choose a route only after the current task actually needs source evidence.

## Source-basis labels

- `verbatim`: directly quoted or copied from source.
- `source_fact`: directly stated by an inspected source.
- `partial`: source is incomplete or only partly inspected.
- `inferred`: reasoning from inspected evidence; not directly stated.
- `report-derived`: from a report or receipt; report is not underlying truth.
- `canon-derived`: from canon/world surfaces.
- `manuscript-derived`: from manuscript/prose surfaces.
- `conversation-derived`: from chat context, not canon, archive, or publication proof.
- `known-empty`: inspected and known absent or empty in scope.
- `unavailable`: source could not be accessed.
- `search-only`: found or not found by search only; not repo-grounded unless the located source content was inspected.
- `not repo-grounded`: no relevant repo file was inspected.

## Rules

Do not let a label launder a claim. If a response mixes evidence and synthesis, partition them explicitly.

Historical reports may preserve old paths as evidence of history, not active authority.

Do not infer global repo unavailability from one source route failing. Distinguish unavailable indexed discovery, exact source-read failure, permission failure, source-scope mismatch, and runtime/tool failure when route capability matters. Use the route-capability labels above for those cases.

When route capability materially affects confidence, state the capability used and what remains unverified. Do not name a runtime tool unless the user is debugging the active tool surface or the exact tool failure is the subject of the answer.

## No-Shit / custody partitioning

When cleanup, anti-bloat, cold-store, governed-trash, or deletion claims appear, partition the source basis before accepting the claim. Separate current repo evidence, worker-reported local state, reports, receipts, manifests, conversation claims, inference, and unavailable source routes.

A report that something was deleted is not current-tree absence proof. A governed-trash sentinel is custody inventory, not deletion authority. A cold-store move preserves retained custody and must not be collapsed into cleanup success without source basis.

If protected archive, canon/world, manuscript, ProjectDB, machine-truth, publication-proof, or ambiguity-bearing surfaces are implicated, mark the claim as protected or routed rather than treating it as ordinary residue.

## Retrospective and doctrine-capture partitioning

When extracting lessons, doctrine proposals, or workflow followups, partition the source basis before making the takeaway. Separate commit or diff evidence, issue comments, worker returns, reports, receipts, conversation-derived material, current repo state, inference, and unavailable routes.

A commit message can be intent evidence, but not proof that validation ran. A worker return can describe local output, but remains reported unless corroborated by a source route. An issue comment can record closure posture, but does not by itself prove source-controlled state.

Use one or two evidence-grounded takeaways at most. If the inspected change is trivial housekeeping, label it as such rather than inventing a lesson.
