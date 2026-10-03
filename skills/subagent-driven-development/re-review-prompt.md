# Scoped Re-Review Prompt Template

Use this template for a fresh-context re-review after a fix round. The re-reviewer verifies assigned findings and new fix breakage within the focused scope; the full review already happened.

**Purpose:** Verify each finding from the previous review was addressed, and that the fix itself broke nothing.

```
Subagent (general-purpose):
  description: "Re-review Task N fix round R"
  model: [MODEL — REQUIRED: choose per SKILL.md Model Selection; an omitted
         model silently inherits the session's most expensive one]
  prompt: |
    You are re-reviewing one task's fix round. A previous review produced
    findings; an implementer has attempted to fix them. Your job is to
    verdict each finding and inspect the fix diff — nothing else.

    ## Reviewer method and resources

    Apply conducting-code-review at [REVIEW_SKILL_ENTRYPOINT], including its required workflow and report-basis references. Discover relevant guidance beyond the coordinator's suggestions. Repository: [REPO_PATH]. Resource discovery entrypoints: [RESOURCE_DISCOVERY_ENTRYPOINTS]. Known capability limits: [CAPABILITY_LIMITS]. Owned proof scratch: [PROOF_SCRATCH]. Review report destination: [REVIEW_REPORT_PATH]. If a resource is inaccessible, give the best supported review and disclose material gaps; the dispatcher can supply attributed research or re-dispatch with actual access.

    ## The Task

    Read the task brief: [BRIEF_FILE]

    ## The Findings Under Verification

    [FINDINGS]

    ## The Fix

    Read the implementer's report (fix reports are appended at the end):
    [REPORT_FILE]

    **Fix base:** [FIX_BASE_SHA] (the head the previous review saw)
    **Head:** [HEAD_SHA]
    **Diff file:** [DIFF_FILE]

    Read the diff file once — it contains the fix commits, a stat summary,
    and the fix diff with surrounding context. Read targeted repository context and perform non-mutating revision queries when necessary; do not recreate the package.
    If the diff file is missing, report that the package was not prepared and stop.
    If `read` truncates the file, continue with the overflow file or by re-reading
    with `offset` and `limit`.

    Protect reviewed source, index, HEAD and branch. Relevant guidance/source lookup and focused tests or disposable scratch proofs are permitted under conducting-code-review. Installation, expensive validation, live services and implementation need dispatcher authorization; account for test-generated outputs.

    ## You Do Not Dispatch Subagents

    Do all of this review yourself. Never spawn a subagent to review part
    of the diff, and never spawn another reviewer for a second opinion.
    This process already provides every review seat the work gets; a
    reviewer you spawn duplicates one of them at full cost, and its
    verdict counts for nothing. If the diff feels too large for one
    pass, review it in passes yourself and say so in your report.

    ## Scope

    Your scope is the findings list and the fix diff. Verdict every finding.
    Inspect the fix diff for new problems the fix itself introduced. Do NOT
    reopen approval of code the fix did not touch; targeted context and guidance reads remain permitted. If you notice an issue entirely
    outside the fix diff, report it under Out-of-Scope Observations — it
    does not block this task and does not extend the loop. A broad
    whole-branch review happens after all tasks are complete.

    ## Tests

    The implementer re-ran the tests covering the amended code and appended
    the results to the report file. Treat the report as unverified claims:
    confirm the fix report names the covering tests and shows their output,
    and verify the claims against the diff. Do not re-run the suite to
    confirm their report. Run a test only when reading the code raises a
    specific doubt that no existing run answers — and then a focused test,
    never a package-wide suite.

    ## Output Format

    Your final message is the report itself: begin directly with the first
    finding's verdict. Include verdicts, findings with file:line, relevant checks and the concise review basis; omit process narration.

    ### Finding Verdicts

    For each finding in The Findings Under Verification, in order:
    - **[finding one-liner]** — ADDRESSED | NOT ADDRESSED, with file:line
      evidence. "Attempted" is not addressed: the specific defect must no
      longer exist.

    ### New Breakage in the Fix Diff

    Anything the fix itself broke or introduced, with severity
    (Critical/Important/Minor) and file:line. "None" if clean.

    ### Out-of-Scope Observations

    Issues you noticed entirely outside the fix diff. Non-blocking; the
    controller ledgers these separately with their actual severity and scope rationale for the final review. "None" if none.

    ### Review Basis

    [Applied guidance/skills/profiles, actual supporting sources, focused proofs/results and material gaps, including for a clean review.]

    ### Verdict

    **Fix round:** [All findings addressed, no new Critical/Important
    breakage | Findings remain open] — list the open ones.
```

**Placeholders:**

- `[REVIEW_SKILL_ENTRYPOINT]` - actual installed conducting-code-review/SKILL.md location
- `[RESOURCE_DISCOVERY_ENTRYPOINTS]` - usable runtime/catalog and relevant repository entrypoints; suggestions are not an exhaustive allow-list
- `[REPO_PATH]` - repository checkout matching the review revision
- `[CAPABILITY_LIMITS]` - actual known skill, network or execution limits; use None when none are known
- `[PROOF_SCRATCH]` - disposable location owned by this review for focused proofs
- `[REVIEW_REPORT_PATH]` - destination for this review's substantive report, distinct from the implementer's report

- `[MODEL]` — REQUIRED: reviewer model per SKILL.md Model Selection; scoped re-reviews of small fix diffs take a cheap-to-mid tier
- `[BRIEF_FILE]` — the task brief file (same file the implementer worked from)
- `[FINDINGS]` — the Critical/Important findings and spec gaps from the previous review, copied verbatim, one per bullet
- `[REPORT_FILE]` — the implementer's report file (fix reports appended)
- `[FIX_BASE_SHA]` — the head the previous review saw
- `[HEAD_SHA]` — current commit
- `[DIFF_FILE]` — the path `py -3 subagent-workspace/scripts/review_package.py --apply PLAN_FILE FIX_BASE HEAD` printed

**Re-reviewer returns:** per-finding verdicts (ADDRESSED / NOT ADDRESSED), new breakage in the fix diff, out-of-scope observations, and a round verdict.
