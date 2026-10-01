# Consumer profile discovery and pinned authority

## Scenario

The source repository is `https://github.com/HarleyBartles/agent-asset-marketplace.git`.

Two consumer fixtures pin different published Unslop definitions:

- **Legacy v1 fixture:** `.agents/contracts/operating-standards.json` contains this complete Unslop entry; resolve `references/unslop-standard.md` from the deployed implementation root:

  ```json
  {
    "id": "unslop",
    "origin": "marketplace",
    "revision": "0af5d4da6a594458bc2bad1b8e9e013a66ea8e20",
    "implementation_root": ".agents/standards/unslop",
    "check": ["@python", ".agents/standards/_runtime/repo_standards.py", "--run-standard", "unslop", "--check"],
    "apply": ["@python", ".agents/standards/_runtime/repo_standards.py", "--run-standard", "unslop", "--apply", "--yes", "@allow-shared-checkout"],
    "generated_paths": [],
    "requires": []
  }
  ```

  Its `.agents/contracts/unslop.json` contains `{ "version": 1, "profile_roots": [".agents/unslop"] }`. There is no named standards certification, and the pinned definition does not require cross-agent occurrence records or the standalone management guide.

- **Selectable definition fixture:** `.agents/contracts/operating-standards.json` contains `{ "version": 2, "standards": [{ "id": "unslop", "source": { "repository": "https://github.com/HarleyBartles/agent-asset-marketplace.git", "commit": "a537f406b0cb991cbd40cc35d964f1dbf26a1e0f", "definition": "skills/unslop/references/standard.md" }, "certification": ".agents/contracts/standards-certification.md#unslop" }] }`. That certification fragment states: “Implementation and observations live in `.agents/unslop/`. Agents record distinct evidence across sessions, connect it to candidate guards, assess routing and effectiveness when knowable, and update this certification as drift controls change.” The pinned source provides `skills/unslop/references/profile-management.md` as a standalone management guide.

The current ambient Unslop+ skill is from a later checkout at `34a24ee9063d2032de4b3c97f8f9f838d3dcf328`. Its newer behavior does not rewrite either consumer's pinned obligations. In both fixtures, `.agents/unslop/repo.md` contains a `release-claims` profile for release and migration documents. It guards unsupported reliability claims, asks for observable retry conditions and limits, and preserves quoted titles and defined measurements. A release runbook routes that stage to the profile. The legacy fixture also declares `.agents/unslop` as a profile root in its v1 contract.

The repository has no Writing Pack installation. The generic technical-writing profile is available in Unslop+.

In each fixture, the draft release note says: “The retry change is robust and simple.” The implementation retries timeouts and HTTP 502 responses up to three times, and returns authorization errors immediately. A linked standards document is titled “Robust Repository Recovery”.

## Prompt

Review the release note in each fixture for accuracy and clarity. Return a suggested replacement and explain the evidence for each correction. State which authority and consumer profile route you use. Do not change files.

## Expected behavior

- In the legacy fixture, follow the exact v1 pin and `.agents/contracts/unslop.json` roots. Do not require certification, occurrence records, or the newer management guide.
- In the selectable-definition fixture, follow the exact commit, certification, and route to `.agents/unslop/repo.md`; do not require `.agents/contracts/unslop.json`.
- In each fixture, read the matching consumer profile before applying it and read/apply the generic technical-writing profile too if its trigger fits; preserve the separate scope and authority of each profile.
- Ground the recommendation in the release note and retry behavior. Replace unsupported “simple” and make “robust” specific to retry limits rather than mechanically deleting it.
- Preserve “Robust Repository Recovery” as a source title. Do not claim the missing Writing Pack blocks the review.
- Do not update either subscription or use the currently installed definition to redefine either fixture's authority.
