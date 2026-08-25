# Frozen writing-style A/B campaign result

> **Protocol validity: invalid for causal or experimental proof.** After the
> blind judgment and map reveal, four evaluator files were temporarily changed
> to satisfy repository CLI contracts. Their exact pre-output bytes were
> restored and verified, but the prospective freeze had already been breached.
> The retained observations are diagnostic only; they cannot establish RED to
> GREEN causality.

## Verdict

**Product concern; no causal improvement claim.** The baseline RED and the
treatment majority-pass gates were met, but treatment GREEN was not. The blind
family-count median fell from 2 to 1, meeting the maximum ratio of 0.5 but not
the required reduction of 2. One treatment output omitted the explicit
no-outcome-data limit, violating the zero-hard-factual-fail gate. The frozen
deterministic evaluator returned no findings for any output, so its family
count and signal-density measures were non-discriminating.

This result is about this six-trial campaign only. It is not evidence of human
authorship, detector performance, or general writing quality.

## Prospective controls

- Campaign: `writing-style-adversarial-ab` v1.4.0.
- Before any output, all 12 campaign pins and all 8 evaluator-freeze pins
  matched; no output tree existed.
- Evaluator RED: 11 failed, 1 skipped because the engine and all three CLIs
  were absent.
- Evaluator GREEN before trials: 11 passed, 1 skipped; combined engine/profile
  suite 61 passed, 1 skipped; all help/default-validation/script-contract gates
  passed.
- Six fresh workers used the identical Codex MultiAgentV2 reviewer route,
  `gpt-5.6-terra`, high reasoning, `fork_turns: none`. Each attested only its
  arm's declared reads.
- Verbatim outputs were sealed and hashed before evaluation. Opaque copies and
  a separate arm map were created before the independent judgment.
- The judge attested only the hidden rubric and six anonymized files. Its
  judgment was fixed before the map was marked revealed.

The runtime uses instruction-and-attestation isolation on a shared filesystem,
not a per-agent OS ACL. No worker or judge attested an out-of-bound read.

## Revealed trial results

| Trial | Arm | Words | Frozen evaluator families | Blind families | Material | Fact | Clarity | Voice | Range |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| A / R4K9 | control | 216 | 0 | 3 | fail | fail | pass | fail | pass |
| C / U2H6 | control | 209 | 0 | 2 | pass | pass | pass | pass | pass |
| E / Y9P4 | control | 221 | 0 | 0 | fail | fail | pass | pass | fail |
| B / W5C1 | treatment | 202 | 0 | 1 | pass | pass | pass | pass | pass |
| D / Q7M2 | treatment | 192 | 0 | 2 | pass | pass | pass | pass | pass |
| F / T8V3 | treatment | 197 | 0 | 0 | fail | fail | pass | pass | pass |

The blind judge's counted families were:

- A: low-information affirmation, synthetic affect, voice flattening;
- C: low-information affirmation and synthetic affect;
- E: none, but word-range and factual-limit hard fails;
- B: low-information affirmation;
- D: low-information affirmation and synthetic affect;
- F: none, but a factual-limit hard fail.

The verbatim quoted evidence and reasons are retained in
`outputs/blind-judgment.json`.

## Threshold calculation

### Baseline RED

Control had 2 material failures out of 3. Required: at least 2. **Met.**

### Treatment GREEN

- Material passes: 2/3. Required at least 2. **Met.**
- Blind median family count: control 2; treatment 1. Ratio 0.5. Required no
  more than 0.5. **Met.**
- Median family-count reduction: 1. Required at least 2. **Not met.**
- Treatment hard factual failures: 1. Required 0. **Not met.**
- Secondary pass counts, treatment versus control: factual 2 versus 1;
  clarity 3 versus 3; authorised voice 3 versus 2; word range 3 versus 2.
  **No decline.**
- Frozen evaluator family medians: 0 and 0; density medians: 0 and 0. Ratio is
  undefined and reduction is 0. **Non-discriminating; cannot meet the primary
  improvement claim.**

Because every treatment-GREEN condition was required, the frozen verdict is a
product concern. The intervention improved the blind material-pass count in
this sample, but did not clear the predeclared effect size or factual-safety
gate. The engine also needs a separately designed, prospectively tested signal
contract before it can measure this campaign's softer contextual families.

## Retained evidence

- `evaluator-freeze.json`: exact pre-output evaluator and input pins.
- `outputs/provenance.json`: route and allowed-read attestations.
- `outputs/seal.json`: verbatim-output hashes and word counts.
- `outputs/evaluator-findings.json`: frozen deterministic results.
- `outputs/anonymized/`: opaque judge inputs.
- `outputs/blind-judgment.json`: fixed independent verdict.
- `outputs/arm-map.json`: mapping revealed only after judgment.

No skill, profile, evaluator rule, stimulus, rubric, campaign manifest, or
threshold was changed after the first worker output to improve the campaign.

## Protocol-deviation chronology

1. The evaluator reached focused GREEN and was sealed by eight hashes before
   any worker output. The exact bytes are preserved in commit
   `f0eda0943f03d2293cee5305a04d999fba4d1722`.
2. Six outputs were generated, sealed, evaluated, anonymized, and blindly
   judged. The map was revealed only after the verdict was fixed.
3. A post-output installed-projection check exposed missing CLI-contract and
   lint requirements. Four pinned scripts were temporarily edited. Although
   no scoring rule changed and scoring had already finished, this breached the
   artifact freeze and permanently invalidated the campaign for causal proof.
4. Those four files were restored byte-for-byte; all eight evaluator and all
   twelve campaign pins matched again. The campaign was not rerun.
5. Once the experimental record was closed as invalid, the final product
   engine received the minimal repository-required fixes: helper docstring,
   read-only help classification, `--check` readiness, and formatting. One
   test added the CLI contract. Signal tables, thresholds, preserve logic, and
   findings remain unchanged.

`evaluator-freeze.json` intentionally continues to pin the pre-output f0eda
artifacts. The final product diverges from six of those hashes: four scripts
and the CLI-contract test changed for product corrections, while the schema
differs only by repository-required EOF normalization. That divergence is
expected and does not rewrite the retained campaign inputs or scores.
