# MARK-373 workflow pressure campaign

`campaign.json` and `prompts/` are reusable pressure-test inputs. The runner
executes each trial from an immutable head in a fresh detached worktree using
only `read-only` or `workspace-write`; publication and connector scenarios stop
before external effects.

Raw output belongs under ignored `runs/` and is disposable. Do not commit run
metadata, model scores, hashes of unavailable traces, or narrative result
receipts. `pressure-scan-decisions.json` retains human adjudication of current
static candidates. `ci-parity.md` and `workflow-inventory.md` describe current
checked controls rather than historical executions.
