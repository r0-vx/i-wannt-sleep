# API

FastAPI publishes interactive OpenAPI documentation at `/docs` and the schema at `/openapi.json`.

All private endpoints currently require `X-ForwardCheck-Session` (20–128 characters).

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/investigations` | Create a validated text investigation |
| GET | `/api/v1/investigations` | List owner-scoped investigations |
| PATCH | `/api/v1/investigations/{id}` | Rename an owned investigation |
| DELETE | `/api/v1/investigations/{id}` | Delete an inactive owned investigation |
| POST | `/api/v1/investigations/{id}/verify` | Queue verification |
| GET | `/api/v1/investigations/{id}/status` | Read status/failure details |
| GET | `/api/v1/investigations/{id}/events` | Stream persisted events as SSE |
| POST | `/api/v1/investigations/{id}/cancel` | Request cancellation |
| GET | `/api/v1/investigations/{id}/report` | Read stored report data |
| GET | `/api/v1/investigations/{id}/graph` | Read record-backed graph |
| GET | `/api/v1/evidence` | List owner-scoped evidence passages |
| GET | `/health/live` | Process liveness |
| GET | `/health/ready` | Database readiness |

