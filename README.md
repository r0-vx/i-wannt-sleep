# ForwardCheck AI

ForwardCheck AI is an evidence-grounded investigation product for suspicious forwarded content. It decomposes content into atomic claims, retrieves public evidence, validates model citations against stored passages, presents a per-claim report, maps records in TruthGraph, and explains manipulative rhetoric separately through Bait Index.

This repository currently contains the first production slice: **pasted text → Gemini extraction → Brave discovery → safe public-page retrieval → Gemini verification → citation validation → persisted report/TruthGraph**. ForwardCheck AI is website-only. It is not yet the complete multimodal product described in the master brief. See [TASKS.md](TASKS.md) and [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).

## Live evaluation deployment

- Website: <https://forwardcheck-ai.vercel.app>
- API readiness: <https://forwardcheck-api-production.up.railway.app/health/ready>

The live deployment supports the real pasted-text workflow. Image, screenshot, audio, PDF, and direct-URL submission are still explicitly preview/validation-only. See [DEPLOYMENT.md](DEPLOYMENT.md) and [LIVE_TEST_REPORT.md](LIVE_TEST_REPORT.md) for hosting details and the verified boundary.

## Local setup on Windows

Prerequisites: Node.js 20.9+, Python 3.12+, Docker Desktop (for the container stack), a Gemini API key, and a Brave Search API key.

```powershell
Copy-Item .env.example .env
# Edit .env and set GEMINI_API_KEY, BRAVE_SEARCH_API_KEY, and strong local secrets.

cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. API documentation is available at `http://localhost:8000/docs`.

Without provider keys, creation and persistence still work, but verification stops with `provider_not_configured`. This is intentional: the app never invents a verdict or citation.

## Container stack

```powershell
Copy-Item .env.example .env
docker compose up --build
```

The Compose stack starts the frontend, API, PostgreSQL, Redis, and private-object-storage infrastructure. The current pipeline still executes through FastAPI background tasks; the Redis-backed durable worker is a recorded release blocker.

## Verification commands

```powershell
cd frontend
npm run lint
npm run build

cd ..\backend
.\.venv\Scripts\python.exe -m ruff check app tests
.\.venv\Scripts\python.exe -m pytest --cov=app
```

Read [SECURITY.md](SECURITY.md), [PRIVACY.md](PRIVACY.md), and [DEPLOYMENT.md](DEPLOYMENT.md) before exposing the application to untrusted users.

