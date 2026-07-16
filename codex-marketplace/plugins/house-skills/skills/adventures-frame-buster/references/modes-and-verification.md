# Modes and Verification

Read this reference when running interactive frame creation/refinement with Harley, or when only
checking whether an existing issue/comment already contains a usable green frame.

## Contents

- Interactive mode
- Internal verification mode

## Interactive mode


Inherit visible queue mechanics from `buster-framework`. Present unresolved frame decisions
conversationally, normally up to five items at a time.

Use interactive mode whenever the frame must be created, selected, materially changed, repaired, or
extended. Do not let GPT privately choose among legitimate worlds, stories, characters,
environments, or asset-reuse paths. Do not queue items where the issue or Harley has already decided
the answer; instead verify whether the written answer is green.

Typical Adventures Frame Buster items:

- Which world best carries the lesson?
- What is Patch trying to accomplish in that world?
- Who gives Patch the mission, blocks unsafe progress, supplies missing context, verifies success,
  and receives the handoff?
- What makes the mission fail before the lesson is applied?
- What environments does Patch move through, and what does each place represent?
- Which existing assets, if any, naturally belong in this frame, and which should stay out?
- What new character, environment, prop, or visual grammar assets should be created instead of forcing reuse?
- What objects represent the abstract concepts?
- What changes from slide to slide, and why does the order matter?
- What is the memorable thesis?
- What must the deck avoid so the analogy does not misteach?
## Internal verification mode


Use internal mode only to verify an already explicit source-written or Harley-approved frame, or to
classify a blocker. Internal mode must not create, choose, repair, or materially extend the frame.

Allowed internal actions:

- read issue/comments and classify `green_as_written`, `amber_advisory_stop`, `red`, or `blocked`;
- check whether a prior green frame comment contains actors, environments, progression, stakes,
  boundaries, and asset posture;
- carry forward a Harley-approved frame exactly as approved;
- mark missing details as amber rather than filling them privately.

Disallowed internal actions:

- choosing between multiple legitimate worlds or analogies;
- inventing the main story, cast, or environment path;
- deciding cross-context asset reuse without Harley;
- turning a thin issue into a green frame by adding GPT-created details during an end-to-end run.

Examples:

- Harley says in the issue/comments: "Mission Control is the frame; Patch is given an impossible
  mission; the client is the mission sponsor; the control room blocks unsafe launch; the simulator
  reveals missing constraints; the debrief proves the corrected mission worked." Verify whether this
  is green as written. If actors or progression are missing, return amber advisory stop rather than
  filling them privately.
- A database issue explicitly contains a green Club DB frame comment with door staff,
  member/requester roles, rooms, queue/entry path, verification moments, progression, and asset
  posture. Verify and proceed if complete.
- An issue only hints "maybe club?" or "could be mission control". Do not choose. Start interactive Frame Buster.
