# Manpage Generation

Manpages for `cortex` are **auto-generated** from the CLI argparse definitions.

## 📄 Generated Files

- `cortex.1` - Main command reference
- `cortex-tui.1` - TUI subcommand reference
- `cortex-workflow.1` - Workflow subcommand reference

## 🔄 Regeneration

Manpages are automatically regenerated:

1. **During installation** - `just install` or `./scripts/deprecated/install.sh`
2. **Manual generation** - `just generate-manpages` or `python3 scripts/generate-manpages.py`
3. **Pre-commit hook** - When `claude_ctx_py/cli.py` is modified (optional)

## 🔧 Setup Pre-commit Hook

To automatically regenerate manpages when CLI changes:

```bash
git config core.hooksPath .githooks
```

## 📝 Editing

**Do NOT manually edit the `.1` files** - they will be overwritten.

Instead:
1. Update CLI help text in `claude_ctx_py/cli.py`
2. Modify the generator in `scripts/generate-manpages.py`
3. Run `just generate-manpages` to regenerate

## 🧪 Testing

View generated manpages:

```bash
# After generation
man docs/reference/cortex.1

# After installation
man cortex
```

## 📅 Version & Date

- **Version**: Extracted from `pyproject.toml`
- **Date**: Set to generation date (YYYY-MM-DD format)
