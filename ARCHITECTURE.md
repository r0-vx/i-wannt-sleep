# Architecture

## Current data flow

```text
Website browser
  -> owner-scoped FastAPI v1 endpoint
  -> Investigation + persisted JobEvent
  -> Gemini structured claim and rhetoric extraction
  -> Brave targeted search
  -> DNS/redirect-checked public HTML retrieval
  -> persistent Source + Evidence passage
  -> Gemini verification using server-issued evidence IDs only
  -> citation allowlist validation
  -> Claim verdict + evidence stances
  -> report and TruthGraph built from the same database records
```

The frontend is Next.js App Router with TypeScript. Interactive provider-bound screens are small client components; static public copy remains server-rendered. The backend is one modular FastAPI application with SQLAlchemy models, Pydantic contracts, and replaceable provider classes.

## Trust boundaries

- `X-ForwardCheck-Session` is the current local guest capability. It is not a production authentication system.
- Uploaded or pasted text, scraped pages, model output, and URLs are untrusted.
- The model cannot create displayed sources. Sources and evidence IDs are allocated only after retrieval and persistence.
- TruthGraph is derived from foreign-key-linked records; layout metadata must never alter truth data.
- Search snippets are discovery hints, not evidence. A retrievable stored passage is required.

## Target production evolution

Move background work from in-process tasks to a Redis-backed durable worker with idempotent job records and cancellation checks. Use PostgreSQL in every shared environment, S3-compatible private storage with lifecycle expiry for uploads, and signed HttpOnly sessions or established OAuth/OIDC for accounts. Provider adapters remain isolated under `backend/app/services`.

