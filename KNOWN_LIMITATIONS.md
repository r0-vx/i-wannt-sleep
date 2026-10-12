# Known limitations

The repository is **not complete against the master definition of done**.

- Only pasted-text ingestion reaches the backend. Image/screenshot, audio, PDF, and URL tabs provide honest local preview or validation, but their processors are not implemented.
- Claim extraction, search, and verification require real Gemini and Brave credentials. A live run completed with `Cannot Confirm`; a later run failed twice at Gemini extraction with provider `ServerError`. Live reliability is therefore not established.
- Source extraction uses a bounded BeautifulSoup adapter; the specified Scrapling pipeline, robots/license registry, Google Fact Check connector, and provenance/independence scoring remain.
- Background work is in-process, not Redis-durable. Retry ceilings, cross-process cancellation, idempotency keys, and crash recovery remain.
- SQLite is the verified local database. PostgreSQL migration and concurrency verification remain.
- Guest session ownership is not production authentication. Accounts, share links, revocation, full export/deletion, and retention enforcement remain.
- TruthGraph includes search, verdict/evidence filters, list fallback, inspector, branch collapse, fit/reset controls, and persistent-record edges. Timeline, saved layout, keyboard graph traversal, and large-graph performance evidence remain.
- English/Hindi/Marathi generated explanation translation, rebuttal generation, PDF export, and print QA remain.
- The required 30-case authentic investigation set, live six-modality tests, cross-browser Playwright suite, accessibility audit, security/load tests, and post-deployment smoke tests remain.
- No hosted deployment exists. Legal entity, support/security contacts, domain, credentials, and hosting access are unconfigured.
- Dockerfiles and Compose syntax validate, but image builds were not verified because the local Docker Desktop Linux engine was not running.

