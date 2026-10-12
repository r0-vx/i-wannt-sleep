# ForwardCheck AI delivery tracker

Updated: 2026-10-12 (Asia/Calcutta)

Legend: **done** = implemented and locally verified; **partial** = real implementation exists but acceptance coverage is incomplete; **blocked** = needs credentials/external access; **not started** = no production implementation.

| Feature | Status | Implementation and evidence | Remaining work / blocker |
|---|---|---|---|
| Product audit and design system | done | Approved railway-investigation direction implemented with Space Grotesk, DM Sans, IBM Plex Mono, exact Blurple/amber/semantic tokens, coded cinematic surfaces, and reduced-motion support | Generated mockups and `design-system/forwardcheck-ai/MASTER.md` are the visual source of truth |
| Text investigation create/persist | done | Versioned FastAPI endpoint, validation, guest ownership, SQLAlchemy records; API tests | Rate limiting and signed server session cookies |
| Gemini claim and Bait extraction | partial | Current Google GenAI SDK adapter with Pydantic response schema and span validation; hosted production completion with `gemini-3.5-flash-lite` | Provider availability can vary; multilingual evaluation not run |
| Brave discovery | partial | Real Brave API adapter and configurable source count; hosted production run retained a public passage | Broader live retrieval evaluation and Google Fact Check connector not implemented |
| Public source retrieval | partial | Redirect/DNS rechecks, private IP blocking, size/time limits, passage persistence | Replace initial BeautifulSoup adapter with Scrapling; robots/license policy registry |
| Evidence verification | partial | Evidence-ID allowlist, citation requirement, exact verdict enum | Live provider evaluation and contradictory-source review |
| Bait Index | partial | Five categories, deterministic severity points, per-category cap, duplicate suppression tests | Calibration dataset and model-span live evaluation |
| SSE progress | done | Browser-verified persisted backend events, missing-provider error, cancellation state, reconnect guidance | Redis durable worker and process-safe cancellation |
| Report | partial | Per-claim verdicts, passages, links, retrieval dates, Bait breakdown | localization, correction/rebuttal, export/print |
| TruthGraph | partial | React Flow + ELK layout from persistent records; edges, inspector, search, filters, branch collapse, fit/reset, and list fallback browser-verified | timeline, keyboard graph traversal, saved layouts, large-graph performance tests |
| Dashboard/history/evidence/settings | partial | Session-derived statistics; search/filter/delete; evidence library; metadata export | rename UI, full-data export/delete, retention enforcement, accounts |
| Public/legal pages | partial | Cinematic landing plus methodology, About, FAQ, Privacy, Terms, Support, 404/error; desktop/mobile Chromium inspection complete | legal/support identities deliberately unconfigured |
| Image/screenshot OCR | not started | — | OCR + bounding boxes + Vision + upload safety |
| Audio transcription | not started | — | decoding, faster-whisper, timestamps, playback seeking |
| PDF extraction | not started | — | PyMuPDF, scanned-page OCR, preview, bounds |
| URL direct ingestion | not started | Safe retrieval exists only inside discovery | canonical metadata review and new-investigation URL UI |
| Image context matching | not started | — | approved real provider and authentic evaluation corpus |
| Accounts/auth/share | not started | Guest owner boundary only | secure sign-in, opt-in expiring share links, revocation |
| Durable queue/storage | not started | Postgres/Redis/MinIO infrastructure defined | worker, idempotency, object lifecycle, presigned uploads |
| Deployment | partial | Vercel frontend, Railway FastAPI, managed PostgreSQL, startup migrations, provider secrets, CORS, health checks, route sweep, and hosted end-to-end browser run verified | Durable worker/object storage, account auth, retention, legal contacts, custom domain, and production load/security testing |

## Feature verification matrix

| Feature | Route/component | Backend/service | Provider | Automated evidence | Live result | Status |
|---|---|---|---|---|---|---|
| Create text investigation | `/investigations/new` | `POST /api/v1/investigations` | none | `test_create_and_owner_scoping` | not required | done |
| Ownership isolation | History/report/status | owner-scoped SQL queries | none | cross-session 404 assertion | same-session hosted persistence verified; cross-session PostgreSQL test pending | partial |
| Claim extraction | processing | `GeminiProvider.extract` | Gemini | schema and API failure paths | hosted production completion with `gemini-3.5-flash-lite`; 3.8 demand failure surfaced safely | partial |
| Evidence search | processing | `BraveSearchProvider.search` | Brave Search | adapter construction/failure path | hosted discovery, retrieval, and stored passage verified | partial |
| SSRF guard | processing | `SafePageFetcher` | public web | add dedicated DNS/redirect suite | not run | partial |
| Citation validation | report/graph | `GeminiProvider.verify` | Gemini | unknown-ID and missing-citation tests needed | hosted report cited the retained source passage | partial |
| Bait scoring | report | `score_bait_spans` | Gemini spans + Python scoring | 3 passing rubric tests | hosted calm claim scored 0/100 | partial |
| TruthGraph integrity | graph | `build_graph` | none | persistent record/edge integrity test passed | hosted stored graph, source node selection, and inspector browser-verified | partial |

