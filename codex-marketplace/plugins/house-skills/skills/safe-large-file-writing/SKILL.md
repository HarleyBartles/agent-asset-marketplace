---
name: safe-large-file-writing
description: Use when writing or editing large text files and you need to avoid editor OOM paths or unsafe partial writes.
metadata:
  source-id: safe-large-file-writing-v1
  source-path: sources/first_party/skills/safe-large-file-writing/SKILL.md
  provenance-name: MARK-302 safe large file writing first-party skill
license: "MIT"
---

# Safe Large File Writing

Use this skill when a text write may be large enough to make a normal editor write path brittle.

## Core rule

Estimate the write before you write it.

If the payload is small, a normal temp-file write is fine.
If the payload is large, switch to a chunked temp-file write path before any bytes are written.
Validate the temp file after the write completes, then atomically replace the target.

Do not write the whole payload to the temp file first and decide later.

## Pre-composition context pressure

Before composing a large document, decide whether the composition itself will exceed the session's remaining context budget.

Treat a write as context-risky when either of these is true:

- the output is likely to exceed about 300 lines;
- the session has already accumulated significant subagent output, research, or file reads in context.

When context-risky:

1. Do not compose the whole document as one inline string in the main session.
2. Prefer a clean-context worker/subagent write with only the required inputs.
3. Or generate the document in bounded sections with sequential append calls, keeping each section below the existing large-write threshold.
4. Still apply the existing chunked/temp-file write mechanics inside the chosen path.

## Large-write threshold

Treat a write as large when either of these is true:

- more than 300 lines;
- more than 256 KB of UTF-8 text.

The exact threshold can be adjusted for a repository, but the decision must happen before the write starts.

## Safe sequence

1. Estimate line count and byte size from the content in memory.
2. Choose the write path before opening the temp file.
3. For small payloads, write the whole content to a temp file in one shot.
4. For large payloads, write the temp file in chunks or append loops.
5. Re-open and validate the completed temp file.
6. Atomically replace the target only after validation passes.

## Python pattern

```python
from pathlib import Path


def iter_text_chunks(text: str, chunk_size: int = 8192):
    for start in range(0, len(text), chunk_size):
        yield text[start:start + chunk_size]


def write_large_text(target: Path, text: str) -> None:
    lines = text.splitlines()
    byte_size = len(text.encode("utf-8"))
    is_large = len(lines) > 300 or byte_size > 256_000

    tmp = target.with_suffix(target.suffix + ".tmp")

    if is_large:
        with tmp.open("w", encoding="utf-8", newline="\n") as handle:
            for chunk in iter_text_chunks(text):
                handle.write(chunk)
    else:
        tmp.write_text(text, encoding="utf-8", newline="\n")

    completed = tmp.read_text(encoding="utf-8")
    if completed != text:
        raise RuntimeError("temp file validation failed")
    if len(completed.splitlines()) != len(lines):
        raise RuntimeError("line count validation failed")
    if tmp.stat().st_size != byte_size:
        raise RuntimeError("byte size validation failed")

    tmp.replace(target)
```

## Windows notes

- Keep temp files on the same volume as the target so `Path.replace()` stays atomic.
- Prefer explicit `encoding="utf-8"` and `newline="\n"` for text generation.
- If a tool or editor has trouble with a very large file, route through a script instead of the interactive editor.
- If the repo has a safer existing helper for batch writes, use that helper instead of inventing a second path.

## Decision test

If you would be tempted to say "write first, check size later", stop and branch to the large-write path before any write starts.

If you would be tempted to compose a large document inline in the main session context, stop and route to a clean-context worker/subagent or section-by-section append path before composition starts.
