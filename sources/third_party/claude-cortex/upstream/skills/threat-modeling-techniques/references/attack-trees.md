# Attack Trees

Hierarchical diagrams show attack paths from goals to methods.

## Structure

```text
[Root: Attack Goal]
| +-- [OR] Method 1
| |   +-- [AND] Step 1.1
| |   +-- [AND] Step 1.2
| +-- [OR] Method 2
|     +-- [AND] Step 2.1
```

## Key Concepts

- `OR` nodes: alternative attack methods, any one can succeed;
- `AND` nodes: required steps, all must succeed;
- leaf nodes: atomic attack actions; and
- the root node: the attacker’s ultimate goal.

## Example

```text
[Goal: Access Customer Database]
| +-- [OR] Exploit SQL Injection
| |   +-- [AND] Find vulnerable input field
| |   +-- [AND] Craft malicious SQL payload
| |   +-- [AND] Extract data from database
| +-- [OR] Steal Admin Credentials
| |   +-- [AND] Phishing attack on admin
| |   +-- [AND] Bypass 2FA
| |   +-- [AND] Login with stolen credentials
| +-- [OR] Exploit Misconfigured Access Controls
    +-- [AND] Enumerate API endpoints
    +-- [AND] Find unprotected endpoint
    +-- [AND] Access data without authentication
```

## Creating Attack Trees

1. define the attacker’s goal;
2. identify alternative attack methods;
3. break each method into required steps;
4. assign cost, skill, detection, and impact attributes;
5. analyze the most likely paths; and
6. prioritize mitigations for the highest-risk paths.

