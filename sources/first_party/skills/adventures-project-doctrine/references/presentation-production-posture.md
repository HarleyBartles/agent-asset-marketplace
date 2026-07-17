# Presentation production posture

For issue-to-PPTX work, the repo-indexed end-to-end PPTX production playbook owns orchestration. Discover it through
`playbooks/INDEX.md`.

A proof run is a full live run, not a weaker mode. If a mandatory gate fails, report Red or Amber at that gate and
stop unless your human partner explicitly approves a mode change.

Image generation credits are scarce production capacity. For proof/full/final-candidate body-slide scene art, image
generation is mandatory only at the proper playbook image stage unless your human partner explicitly starts storyboard/draft mode.
Do not spend credits during issue ingestion, planning, prompt boards, QA, repair planning, contact sheets, asset-sheet
compilation, receipts, repo comments, or policy work.

For GPT-side direct image calls, generate images only after issue ingestion, frame/deck planning, image planning, visual-intent gate, Patch preflight,
reference inspection, and resource-discipline checks.

After a GPT-side generation call, stop. If your human partner asks for QA, run Patch or Adventures image QA and return
accepted/edit_required/regenerate_required/blocked. Do not automatically edit or regenerate from QA. GPT-side image generation
and editing are single-use authorized actions: generate -> stop; QA request -> QA decision and repair guidance ->
stop; separate explicit generate/edit request -> one new image tool call -> stop.

PIG production jobs are different. A bounded PIG job may include generation, PIG self-QA, and bounded regeneration inside the assigned job. PIG output still returns as candidate material until GPT, your human partner, or project QA accepts it. Do not treat PIG self-QA as accepted image inventory for proof/full/final decks.

Build PPTX only after the accepted generated scene-image inventory is complete.
