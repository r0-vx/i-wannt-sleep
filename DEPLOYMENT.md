# Deployment and operations

## Current production deployment

Deployed and live as of 2026-10-12:

- Web application: `https://forwardcheck-ai.vercel.app`
- FastAPI service: `https://forwardcheck-api-production.up.railway.app`
- API readiness check: `https://forwardcheck-api-production.up.railway.app/health/ready`
- Frontend host: Vercel, Next.js framework preset, production and preview API origins configured.
- Backend host: Railway, containerized FastAPI with Alembic migrations applied at startup and Railway's dynamic `PORT` respected.
- Database: Railway managed PostgreSQL, connected through a private service reference.
- Providers: Gemini and Brave credentials are server-side Railway variables and are not present in the frontend bundle or repository.
- CORS: production frontend origin is explicitly allowed and the public preflight check passes.

The deployed text workflow was exercised end to end in a real browser. It created a persistent investigation, streamed progress, extracted a claim, discovered and retrieved a public source, produced a citation-backed report, and rendered the stored TruthGraph and Evidence Library record. See `LIVE_TEST_REPORT.md` for the exact verification boundary.

## Supported shape

- Frontend: Node.js server running the Next.js production build.
- API and worker: separate containers built from the same Python package.
- State: managed PostgreSQL, managed Redis, and private S3-compatible object storage.
- Edge: HTTPS reverse proxy with explicit CORS and CSP, request/body limits, and provider egress rules.

## Production-hardening work still required

1. Implement and test the durable worker and object-storage upload lifecycle.
2. Replace guest bearer IDs with signed sessions/account auth and implement CSRF controls where cookies are used.
3. Configure support/security contacts, legal entity, custom domain, and a dedicated production secrets-management policy. Provider secrets, allowed origins, and managed TLS are configured on the current hosts.
4. Run expanded isolation, deletion, backup, and restore tests against managed PostgreSQL. Migrations are applied automatically at API startup.
5. Run the controlled E2E suite, supported-modality live suite, dependency/secret scans, accessibility audits, and load tests.
6. Deploy staging, run `/health/live`, `/health/ready`, provider smoke tests, citation resolution, upload lifecycle, worker, and deletion checks.

## Rollback

Retain the previous immutable frontend/API images. Back up PostgreSQL before a migration. If a release fails, stop new jobs, deploy the prior images, and use the migration's explicit downgrade only after reviewing whether new writes occurred. Object lifecycle changes require a separate reversible plan.

The current hosted release is suitable for hands-on evaluation of the text investigation workflow. It is not yet hardened for sensitive or high-volume production use because guest identity is browser-scoped and background jobs are not backed by a durable queue.

