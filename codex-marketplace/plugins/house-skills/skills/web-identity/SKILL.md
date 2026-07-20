---
name: web-identity
description: Use when selecting OAuth 2.0 / OIDC flows, validating tokens, or integrating identity providers. Do not use when the work is bespoke session management or platform-specific IAM policy.
metadata:
  source-id: web-identity
  source-path: sources/first_party/skills/web-identity/SKILL.md
  provenance-name: Web Identity first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: OAuth 2.0 / OIDC flow selection, token validation, and identity-provider integration
  use_when:
  - Use when selecting OAuth 2.0 / OIDC flows
  - Use when validating access, refresh, or ID tokens
  - Use when integrating identity providers or designing client consent
  do_not_use_when:
  - Do not use when building bespoke session management
  - Do not use when configuring platform-specific IAM policy
license: MIT
---

# Web Identity

Use this skill when choosing or reviewing authentication and authorization boundaries for web applications and APIs.

## When to Use

- Selecting an OAuth 2.0 grant type for a client.
- Validating JWT-shaped access or ID tokens.
- Integrating an identity provider and mapping claims to application identity.
- Deciding how and where to store refresh tokens.
- Reviewing consent scopes and token lifetime boundaries.

Do not use this skill for custom session cookies, password hashing, or cloud IAM policy details. Route those to a platform-specific or security-review skill.

## Core Patterns

Prefer the authorization-code flow for server-side and single-page applications that can keep a client secret or use PKCE. Use client credentials for machine-to-machine calls without a user present. Use device code for input-constrained clients such as TVs or IoT devices.

ID tokens carry identity claims and are meant for the client. Access tokens grant access to a resource and are validated by the resource server. Refresh tokens are long-lived secrets stored and rotated with care; never expose them to browsers or mobile code that cannot protect them.

Validate tokens by checking signature, issuer, audience, expiration, and intended use. Verify that scopes in the access token match the requested operation. Ask your human partner before choosing implicit or resource-owner-password flows; they are discouraged in modern practice.

## Common Mistakes

- Confusing ID tokens with access tokens. ID tokens prove who the user is; access tokens prove permission to act.
- Storing refresh tokens in client-side code. Keep them on a server or secure device storage.
- Ignoring PKCE for public clients such as mobile and SPA apps.
- Requesting overly broad scopes. Ask for the smallest scope that satisfies the feature.
