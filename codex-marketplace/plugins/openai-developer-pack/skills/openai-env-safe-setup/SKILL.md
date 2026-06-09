# OpenAI Safe Environment Setup

Use this skill when you need local environment-variable setup for OpenAI development without exposing secrets or replicating proprietary key-creation flows.

## Default posture

- Prefer local environment variables for development.
- Keep secrets out of git history.
- Keep the setup script boring and reversible.
- Do not document or automate the proprietary platform-connector flow in this pack.

## Local setup pattern

### PowerShell

```powershell
$env:OPENAI_API_KEY = "your-key-here"
```

### Bash

```bash
export OPENAI_API_KEY="your-key-here"
```

### `.env` file

```env
OPENAI_API_KEY=your-key-here
```

## Checks

- Confirm the variable is present in the current shell.
- Confirm the value is not committed.
- Confirm the app reads configuration from the environment at startup.
- Confirm any optional provider keys follow the same local-only rule.

## Good habits

- Keep key names consistent across docs and code.
- Fail fast if required configuration is missing.
- Use a secret manager or vault for shared environments.
- Rotate keys when a credential is moved between environments.

