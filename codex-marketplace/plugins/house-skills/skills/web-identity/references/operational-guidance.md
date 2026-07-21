# Web Identity Operational Guidance

## OAuth 2.0 Flows

- **Authorization code**: Use for server-side web apps, SPAs with a backend, and mobile apps. Pair public clients with PKCE to prevent authorization-code interception.
- **Client credentials**: Use for machine-to-machine or daemon services where no user is present.
- **Device code**: Use for input-constrained devices such as smart TVs, printers, or IoT hardware.
- Avoid the implicit and resource-owner-password flows unless your human partner explicitly accepts the risk.

## OIDC ID Tokens and Claims

- ID tokens are OIDC artifacts that carry identity claims (`sub`, `iss`, `aud`, `exp`, `iat`) and are intended for the client application.
- Claims should be validated against the expected issuer and audience.
- Do not use an ID token to authorize access to a resource API.

## Token Types

- **Access token**: Grants access to a resource server. Validate signature, issuer, audience, expiration, and scopes.
- **Refresh token**: Long-lived secret used to obtain new access tokens. Store in server-side or secure device storage and rotate on use.
- **ID token**: Proves authentication to the client. Validate and consume only on the client side.

## Client Types and Consent

- Confidential clients can store secrets; public clients cannot and must use PKCE.
- Keep consent scopes minimal. Request only the claims and scopes the feature needs.
- Present a clear consent screen when user authorization is required.

## Identity Providers and JWT Validation

- Integrate identity providers by trusting their discovery or JWKS endpoint.
- Validate JWTs with the issuer's public key, check `alg` restrictions, and reject tokens with unexpected algorithms.
- Match `aud` to your application's client ID and `iss` to the provider's issuer URL.

## When to Involve Your Human Partner

- Before selecting a discouraged or legacy flow.
- When choosing a platform-specific identity SDK or vendor configuration.
- When changing token lifetimes, rotation policy, or consent scopes for production systems.
