# .agents/plugins

Codex-facing marketplace metadata lives here.

- `marketplace.json` is the private marketplace index consumed by Codex-style plugin installers.
- Plugin source paths must be local `./plugins/<plugin-name>` paths that stay inside this repository.
- Marketplace entries carry policy, category, projection, provenance, license, quality, and localization metadata.

Validate with:

```sh
python3 tools/validate_marketplace.py
```
