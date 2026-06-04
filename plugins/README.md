# plugins

Codex-facing plugin projections live here.

Each plugin should keep the expected shape:

```text
plugins/<plugin-name>/
  .codex-plugin/plugin.json
  skills/
  hooks/
  assets/
  README.md
```

MARK-2 keeps upstream asset identity in `sources/` and projection metadata in marketplace/plugin manifests so future regrouping is normal maintenance.
