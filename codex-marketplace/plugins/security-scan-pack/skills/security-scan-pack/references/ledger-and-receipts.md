# Ledger and Receipts

The pack keeps a deterministic coverage ledger so that each candidate scan can be
replayed and audited.

## Coverage ledger fields

Each candidate row should record:

- `candidate_id`
- `surface`
- `path_or_image`
- `tool`
- `command`
- `output_path`
- `receipt_path`
- `exit_code`
- `finding_count`
- `highest_severity`
- `baseline_or_ignore`
- `status`
- `notes`

## Receipt posture

- Every candidate gets a receipt, even when no findings are present.
- A receipt is valid only when the command and output path are explicit.
- A receipt should make it obvious whether the result is authoritative,
  advisory, or blocked by missing tooling.

## Suggested statuses

- `scanned`
- `scanned_no_findings`
- `blocked_tooling`
- `blocked_scope`
- `advisory_only`

## Minimal JSON shape

```json
{
  "candidate_id": "gitleaks-repo",
  "tool": "gitleaks",
  "command": "gitleaks git <path>",
  "output_path": "artifacts/gitleaks.json",
  "receipt_path": "artifacts/receipts/gitleaks-repo.md",
  "exit_code": 0,
  "finding_count": 0,
  "status": "scanned_no_findings"
}
```

## Notes

- Keep the ledger sorted by candidate_id or scan order and do not reshuffle it
  after the fact.
- If a scan is repeated, record the new run instead of overwriting the old receipt.
