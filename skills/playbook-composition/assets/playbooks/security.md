# Security concern

Use this guidance whenever work changes trust boundaries, identity, permissions, sensitive data, network exposure, or execution of supplied input.

Identify which actors and inputs are trusted, what they can reach, and what a successful attack would expose or change. Preserve least privilege and validate untrusted input at the boundary where it enters. Avoid logging secrets or expanding access for convenience. Check how errors, generated artifacts, and external integrations affect the same boundary. If the risk is material or uncertain, route it to the repository's security owner and record the decision.

Security work is complete when the relevant boundary and mitigations are clear, remaining risk has an explicit disposition, and evidence supports the claims made.
