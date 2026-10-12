# Architecture decisions

## ADR-001: Modular monolith

Use one Next.js frontend, one FastAPI backend, one worker process, PostgreSQL, Redis, and S3-compatible storage. This keeps transactions and authorization understandable while allowing extraction and verification modules to evolve independently.

## ADR-002: No verdict without retrieved evidence

Search results alone are not evidence. A non-`Cannot Confirm` result requires at least one stored evidence assessment whose ID was issued by the backend. Unknown IDs reject the provider response.

## ADR-003: Model-assisted detection, deterministic Bait scoring

Gemini identifies exact rhetoric spans. Python assigns fixed severity points and caps each category at 20. The resulting 0–100 value communicates rhetoric intensity only.

## ADR-004: Guest-first, account-later

The first slice uses a random browser-held owner ID so access-control queries exist from the beginning. This is explicitly local/development semantics, not production authentication.

## ADR-005: Initial source extractor

The first slice uses a small safe HTTP + BeautifulSoup extractor to establish SSRF and citation boundaries. Scrapling remains required before declaring the discovery subsystem complete.

