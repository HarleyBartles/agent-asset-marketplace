# Source route labels

Load this reference only when source route capability or route coverage matters to a Rooms claim.

## Principle

Label source routes by capability, not by fixed runtime tool name. Skills tell GPT what evidence capability is needed; GPT selects from the active runtime surface.

Do not treat the mere presence of a connector, uploaded file, source, or tool namespace as a reason to inspect routes. Choose a route only after the current task actually needs source evidence.

## Route-capability labels

- `exact-repository-read`: evidence came from a capability that can read a known current repository object, such as a named file path, issue, comment, commit, branch, pull request, or comparison.
- `indexed-repository-discovery`: evidence came from a capability that can search the target repository or repository set broadly for unknown files, stale terms, duplicate issues, or corpus-style matches.
- `uploaded-file-evidence`: evidence came from a user-provided file or file-library surface, not from current repository state.
- `local-worker-evidence`: evidence came from a local worker or disk report and remains reported unless independently observable in the current session.
- `report-evidence`: evidence came from a report, receipt, return, or status note rather than from the underlying source surface.
- `route-unavailable`: the needed route capability was not available in the current runtime.
- `route-failed`: the needed route capability was available but failed at runtime.
- `scope-mismatch`: a route existed but did not expose the needed repo, branch, issue, file set, or source family.

## Interpretation

Indexed discovery is useful for recall, stale-pattern sweeps, duplicate hunting, and finding unknown files or issues. It is not proof of absence unless the search scope is well defined and the response explicitly limits the claim to that scope.

Exact repository reads are useful for current state of known targets. They do not replace broad indexed discovery when the task requires a corpus-wide sweep.

Uploaded files and reports can be valuable mirrors or handoff artifacts. They do not become current repository truth unless the task is explicitly scoped to them or they are corroborated by an appropriate source route.

## Reporting route limits

When route capability materially affects confidence, state the capability used and what remains unverified. Do not name a runtime tool unless the user is debugging the active tool surface or the exact tool failure is the subject of the answer.
