# Security

## Implemented in the first slice

- Every investigation read/write query is owner-scoped.
- Public-page retrieval permits only HTTP/HTTPS, resolves and rejects non-global IPs, rechecks each redirect, limits redirect count, response type, bytes, and timeout.
- Scraped and uploaded content is marked untrusted in provider prompts.
- Non-`Cannot Confirm` model output requires stored evidence assessments; unknown evidence IDs are rejected.
- Provider secrets are server-side environment variables and are excluded from source control.

## Release blockers

- Guest IDs are bearer capabilities in browser storage, not signed HttpOnly server sessions.
- No production auth, CSRF design, per-user rate limiter, malware scanner, object-store quarantine, secret manager, CSP report endpoint, or audit log exists yet.
- In-process background execution is not durable and cancellation is cooperative between claim iterations.
- Dependency audit findings must be resolved or risk-accepted before deployment.

Do not expose this build publicly until the blockers above are addressed and tenant isolation is verified against PostgreSQL.

