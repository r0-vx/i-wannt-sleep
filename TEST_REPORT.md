# Test report

Date: 2026-10-12 (Asia/Calcutta)

## Unit / controlled local

- Backend Pytest: 8 tests passed in the final run; total backend coverage is 63%. Graph construction reached 100%, Bait scoring 100%, schemas 98%, and models 100%. The overall release gate of 80% is not met because provider and pipeline paths remain under-tested.
- Bait tests prove an urgent message can score high independently of truth, a calm message can score zero, and duplicate spans are not double-counted.
- API tests cover create/list owner scoping, cross-session denial, validation, and explicit failure when provider credentials are absent.
- Backend Ruff: passed. Backend MyPy is included in the final verification pass after resolving provider and pipeline type errors.
- Frontend ESLint, TypeScript production build, and production dependency audit: passed after the cinematic investigation redesign; 18 routes were generated and `npm audit --omit=dev` reported 0 vulnerabilities.
- Alembic initial schema upgrade and downgrade: passed against a fresh SQLite validation database. PostgreSQL migration verification remains.
- Docker Compose configuration: passed. Container image build was attempted but could not start because the Docker Desktop Linux engine was not running (`dockerDesktopLinuxEngine` pipe absent).

## Live integration

Gemini and Brave are configured only as server-side Railway variables. The deployed production flow completed a real text investigation using Gemini `gemini-3.5-flash-lite`, Brave discovery, safe public-page retrieval, PostgreSQL persistence, SSE progress, citation validation, report rendering, and TruthGraph construction. An earlier attempt against `gemini-3.8-flash` returned a provider `503 UNAVAILABLE`; the UI persisted and surfaced the failure without fabricating a report. See `LIVE_TEST_REPORT.md`.

Vercel served all 12 primary public and application routes with HTTP 200. Railway `/health/live` returned `ok`, `/health/ready` returned `ready`, and the production-origin CORS preflight returned HTTP 200 with the exact allowed origin. The public deployment is `https://forwardcheck-ai.vercel.app`.

## Manual browser

Playwright CLI drove real Chromium sessions against the running Next.js and FastAPI applications at 360, 390, 768, 1024, 1440, and 1920 pixel desktop/mobile breakpoints.

- The coded railway landing composition, mobile navigation, application shell, all six input tabs, text validation, honest unsupported-processor states, persisted SSE progress, dashboard empty states, settings persistence, report rendering, and TruthGraph selection/inspector interactions were exercised.
- The TruthGraph connector defect found during QA was fixed by adding explicit React Flow handles. A clean rerun rendered both edges with zero console errors and zero warnings.
- Reduced-motion preference was enabled, saved, reloaded, and confirmed active on the document root. Keyboard Tab navigation reached the first branded link and navigation controls expose accessible names and expanded state.
- Browser testing discovered and fixed a `127.0.0.1` versus `localhost` CORS defect and Next.js navigation/smooth-scroll warnings.
- Current redesign captures include `output/playwright/cinematic-landing-desktop-final.png`, `output/playwright/cinematic-landing-mobile.png`, `output/playwright/cinematic-landing-360.png`, `output/playwright/cinematic-dashboard-desktop.png`, `output/playwright/cinematic-dashboard-mobile.png`, `output/playwright/cinematic-new-investigation.png`, `output/playwright/cinematic-progress-complete.png`, `output/playwright/cinematic-truthgraph-desktop.png`, `output/playwright/cinematic-truthgraph-inspector.png`, `output/playwright/cinematic-truthgraph-mobile.png`, `output/playwright/cinematic-report-desktop.png`, `output/playwright/cinematic-investigations.png`, `output/playwright/cinematic-evidence.png`, and `output/playwright/cinematic-settings.png`.
- No page-level horizontal overflow remained at the tested breakpoints. The 360px pass found and fixed a CSS specificity issue that had kept the public-header CTA visible below its intended breakpoint.
- No fixture result was presented as live. Unsupported file and URL processors remain visibly disabled after real local preview/validation.

## Hosted browser verification

- Desktop production landing, new-investigation submission, persisted progress, report, TruthGraph, source inspector, dashboard, investigation history, and Evidence Library were inspected through Playwright.
- The live mobile dashboard at 390 x 844 had `scrollWidth` equal to `clientWidth` and its navigation drawer opened and exposed all application destinations.
- The browser recorded zero console errors. Two non-blocking Next.js CSS preload warnings appeared during route transitions.
- Hosted captures: `output/playwright/live-vercel-landing.png`, `output/playwright/live-vercel-report.png`, `output/playwright/live-vercel-truthgraph.png`, `output/playwright/live-vercel-truthgraph-inspector.png`, and `output/playwright/live-vercel-dashboard-mobile.png`.

