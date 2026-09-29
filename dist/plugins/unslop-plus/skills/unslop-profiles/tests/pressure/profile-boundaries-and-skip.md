# Profile boundaries, justified terminology, and skip behavior

## Scenario

The runtime has Unslop+ and its bundled generic profiles. The current task is a tiny behavior-preserving Python edit, with no plan, public API, UI, documentation, or test-design work. No adopted Unslop standard or consumer-owned profile is present.

```python
def display_name(record):
    item = record["name"]
    return item.strip()
```

In a separate review request, the user asks whether this sentence needs editing: “Robustness here means the parser accepted all 1,000 generated inputs and rejected all 1,000 malformed inputs.” The user also asks that the title “Robust Recovery” remain unchanged because it is quoted from the source document.

## Prompt

First, rename `item` to `name_value` in the function, preserving behavior. Then assess the sentence and quoted title against applicable profile guidance. Report any edits with the exact observed text or code decision that supports them.

## Expected behavior

- Skip profile application for the narrow variable rename when no bundled profile fits its scope; do not force a generic profile onto unrelated work.
- For the separate prose review, read the matching generic profile before applying it.
- Preserve the measured use of “Robustness” and the quoted title because the metric and quotation give those terms a precise, task-relevant meaning.
- Make no mechanical word replacement and cite the specific sentence and title as the evidence for leaving them intact.
