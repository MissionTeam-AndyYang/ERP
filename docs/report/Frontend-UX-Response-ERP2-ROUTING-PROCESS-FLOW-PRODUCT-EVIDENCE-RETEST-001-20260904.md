# Frontend UX Response - ERP2 Routing / Process Flow Product Evidence Retest

- Work item: ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-001
- Authorization: ERP2-CIO-ROUTING-PROCESS-FLOW-ACCEPTANCE-RETEST-001
- Date: 2026-09-04
- Scope: bounded non-production Frontend / UX acceptance retest for `/routing`

## Retest Target

This retest covers the implemented read-only `/routing` surface against the confirmed Routing / Process Flow Backend API route family.

Accepted routes:

- `GET /api/v2/routing/dashboard`
- `GET /api/v2/routing/products/{item_no}/versions`
- `GET /api/v2/routing/versions/{routing_version_id}/steps`
- `GET /api/v2/routing/products/{item_no}/current`

The retest does not cover Routing write, approval, release, freeze, Product write, Production execution, migration, Source-of-Truth transition, Engineering Pull, Cutover, or ERP2.0 Go-Live.

## Runtime Setup Used

| Item | Value |
|---|---|
| Backend service | Local non-production restserver window |
| Backend URL | `http://127.0.0.1:5031` |
| Frontend URL | `http://localhost:3000/routing` |
| Frontend API base | `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5031` |

No existing Backend service window was listening on ports previously used by earlier retests. A local restserver window was started for this retest.

## Backend HTTP Probe

| Probe | Result | Notes |
|---|---|---|
| `GET /api/v2/routing/dashboard?count=5` | BLOCKED, HTTP 400 | Backend route was reachable, but DB-backed request failed because the local runtime attempted to connect to unavailable `localhost` DB. |
| `POST /api/v2/routing/dashboard` | PASS, HTTP 405 | Read-only route boundary is preserved. |

The Backend implementation report already classifies Shared DEV Routing DB-backed smoke as pending fixture/schema readiness because the Shared DEV database lacks Routing source tables such as `product_process`. This run additionally confirms the current local process does not have a usable DB-backed Routing service window available for full Product/WIP evidence validation.

## Frontend Browser Smoke

Browser validation was run against `http://localhost:3000/routing` with the frontend pointing to the Backend service at `http://127.0.0.1:5031`.

| Check | Result |
|---|---|
| `/routing` page opens | PASS |
| Data source badge changes to error after Backend 400 | PASS |
| Error message is visible | PASS |
| API mode avoids silent mock fallback | PASS |
| User can manually switch to mock data | PASS |
| Switching back to API removes mock rows and returns to error state | PASS |
| Browser console error/warning check | PASS, no page console error captured |

Observed frontend error text:

`Routing / Process Flow 資料取得失敗，畫面未改用示範資料。API request failed: 400`

Mock/API toggle evidence:

- Mock mode displayed demo Routing rows.
- API mode after switching back did not retain demo Routing rows.
- API mode displayed the Backend error state instead of substituting mock data.

## Acceptance Item Status

| Item | Status |
|---|---|
| Product / WIP selector | PASS for mock mode and empty/error rendering; real DB-backed data pending service readiness |
| Routing Version display | PASS for frontend mapping and mock mode; real DB-backed data pending service readiness |
| Ordered process flow | PASS for frontend mapping and mock mode; real DB-backed data pending service readiness |
| Stage / group | PASS for frontend mapping and mock mode; real DB-backed data pending service readiness |
| Process identity / label | PASS for frontend mapping and mock mode; real DB-backed data pending service readiness |
| Recipe reference where established | PASS for frontend mapping and mock mode; real DB-backed data pending service readiness |
| Non-Recipe step | PASS for frontend mapping and mock mode; real DB-backed data pending service readiness |
| Packaging context where established | PASS for frontend mapping and mock mode; real DB-backed data pending service readiness |
| Resource eligibility where governed | PASS for frontend mapping and mock mode; real DB-backed data pending service readiness |
| Standard performance where governed | PASS for frontend mapping and mock mode; real DB-backed data pending service readiness |
| Source lineage | PASS for frontend mapping and empty/error rendering; real DB-backed data pending service readiness |
| Warnings | PASS for frontend mapping and empty/error rendering; real DB-backed data pending service readiness |
| Empty / error state | PASS |
| No silent mock fallback | PASS |
| No write / edit / approve / release controls | PASS |

## Automated Validation

| Check | Result |
|---|---|
| `npm run lint` | PASS |
| `npm run build` | PASS |
| Routing Backend pytest | PASS, 6 passed |
| `npm run test` | NOT AVAILABLE |

The frontend project still has no `test` script in `package.json`; this remains `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP`.

## Final Classification

**ROUTING_PROCESS_FLOW_FRONTEND_UX_ERROR_STATE_AND_CONTRACT_PASS_REAL_DB_SERVICE_WINDOW_PENDING**

The `/routing` frontend is aligned to the accepted read-only Routing Backend API contract, preserves API/mock separation, displays API failure without silent mock fallback, and exposes no write/edit/approve/release controls. Full real DB-backed Product/WIP evidence validation remains pending a ready Shared DEV Routing service window with the required Routing source tables and credential injection.
