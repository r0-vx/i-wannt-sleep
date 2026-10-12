# Live provider test report

Date: 2026-10-12 (Asia/Calcutta)

Gemini and Brave Search were exercised with server-only Railway credentials. No credential value is stored in this repository or browser bundle.

## Hosted production run

- Frontend: `https://forwardcheck-ai.vercel.app`
- API: `https://forwardcheck-api-production.up.railway.app`
- Gemini model: `gemini-3.5-flash-lite`
- Input: `The Eiffel Tower is located in Paris, France.`
- Result: the text pipeline completed all five persisted stages and returned `Verified` with one stored public-source passage and a validated citation.
- Brave discovery reached a public article, the safe retriever stored its passage, and the report linked to the retrieved source rather than a search snippet.
- The dashboard, investigation history, Evidence Library, report, TruthGraph, and selected-source inspector all rendered from the same persisted database records.
- The live mobile dashboard was verified at 390 x 844 with no horizontal overflow.

The first hosted attempt used `gemini-3.8-flash` and stopped at extraction with `503 UNAVAILABLE` due provider demand. A compatibility check showed `gemini-2.5-flash` was unavailable to this account, while `gemini-3.5-flash-lite` completed successfully. Production was updated to the working model; the failed attempt remains evidence that provider failures are surfaced rather than converted into synthetic results.

## Completed live run

- Investigation: `ae52ac0b-2724-4972-910a-c6d5ca8840ce`
- Owner session used for QA: `codex-live-validation-20261012-b`
- Gemini model: `gemini-3.8-flash`
- Result: the pipeline completed and produced `Cannot Confirm` because it did not retain a usable retrieved passage for the claim. This is an honest unresolved result, not a successful factual verification.
- The completed report and persistent-record TruthGraph were inspected in a real Chromium session. Graph edges, node inspector, search/filter controls, list fallback, Bait Index presentation, and report navigation rendered from stored records.

## Subsequent browser submission

- Investigation: `656b2077-3a20-481f-af41-3779706b4414`
- Input contained multiple factual statements and forwarding pressure.
- Result: both the initial attempt and one user-visible retry stopped during Gemini claim extraction with provider detail `ServerError`.
- The UI correctly persisted and displayed the `draft`, `queued`, `extracting`, and `failed` events. It did not synthesize claims, evidence, progress, or a report.

The earlier local runs above are retained as regression evidence. Google Fact Check Tools, image matching, private object storage, and non-text processors remain unconfigured or unimplemented. The hosted deployment supports the real text workflow; image, screenshot, audio, PDF, and direct-URL submission remain explicit preview/validation-only modes.

