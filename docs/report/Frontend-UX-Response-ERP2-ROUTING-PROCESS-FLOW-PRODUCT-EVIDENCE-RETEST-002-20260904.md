# Frontend UX Response - ERP2 Routing / Process Flow Product Evidence Retest 002

- Work item: ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-002
- Authorization: ERP2-CIO-ROUTING-PROCESS-FLOW-SHARED-DEV-DATA-SURFACE-001
- Date: 2026-09-04
- Scope: bounded non-production Frontend / UX real Backend acceptance retest for `/routing`

## Retest Baseline

Latest Backend evidence consumed:

- Commit: `a3bf25b Support routing Shared DEV test surface fallback`
- Report: `docs/report/Backend-API-Response-ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-002-20260904-001.md`
- Backend classification: `PASS - REAL SHARED DEV DB-BACKED ROUTING API RETEST COMPLETED THROUGH BOUNDED TEST-SUPPORT READONLY SURFACE`

Backend preserved the formal Routing API path when formal tables are present. When formal Routing tables are absent but Engineering B's read-only test-support views are present, Backend reads the support surface and preserves the public API response shape while exposing `sourceCode = test_support` and `warningCode = test_support_only`.

## Runtime Setup Used

| Item | Value |
|---|---|
| Backend service | Local non-production restserver started through Engineering B read-only wrapper |
| Backend URL | `http://127.0.0.1:5041` |
| Frontend URL | `http://localhost:3000/routing` |
| Frontend API base | `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5041` |
| Frontend API token | Non-production read validation token passed through frontend env |
| Raw secret exposure | 0 |

Frontend / UX did not access the database directly. All Product Evidence validation was performed through Backend HTTP APIs.

## Real Backend API Evidence

| Probe | Result | Evidence |
|---|---|---|
| `GET /api/v2/routing/dashboard?effectiveDate=1700000000` | PASS | HTTP 200; `routingVersionCount=1`; `routingVersionId=TS-ROUTE-SD-001`; `itemNo=PRD-SD-001`; `stepCount=2`; `warningCodes=["test_support_only"]` |
| `GET /api/v2/routing/products/PRD-SD-001/versions?effectiveDate=1700000000` | PASS | HTTP 200; version list contains `TS-ROUTE-SD-001` |
| `GET /api/v2/routing/versions/TS-ROUTE-SD-001/steps?effectiveDate=1700000000` | PASS | HTTP 200; steps `TS-STEP-SD-001`, `TS-STEP-SD-002`; source lineage and warnings returned |
| `GET /api/v2/routing/products/PRD-SD-001/current?effectiveDate=1700000000` | PASS | HTTP 200; current route returns the same two ordered steps |
| `POST /api/v2/routing/dashboard` | PASS | HTTP 405; read-only route boundary preserved |

Returned Product evidence:

- Product: `PRD-SD-001`
- Product name: `Shared DEV Product Fixture A`
- Routing Version: `TS-ROUTE-SD-001`
- Ordered steps: `TS-STEP-SD-001`, `TS-STEP-SD-002`
- Step labels: `Synthetic material preparation visibility step`, `Synthetic product composition visibility step`
- Recipe reference: `BOM-SD-001`, version `1`
- Source lineage includes `test_support`, `product_spec`, `product_bom_spec`, and `not_recorded`
- Controlled warnings include `test_support_only`, `resource_eligibility_not_governed`, `missing_process_master`, and `missing_standard_performance`

## Frontend Browser Evidence

Browser validation was completed against `/routing` while the frontend was connected to the real Backend service at `http://127.0.0.1:5041`.

| Check | Result |
|---|---|
| `/routing` opens | PASS |
| Data source displays Backend/API mode | PASS |
| Real Backend route appears | PASS; screen shows `TS-ROUTE-SD-001` |
| Product appears | PASS; screen shows `PRD-SD-001` and `Shared DEV Product Fixture A` |
| Mock route absent in API mode | PASS; no `ROUTE-LEMON-001` / `PRD-LEMON-001` shown |
| Ordered steps appear | PASS; both synthetic step labels shown |
| Stage / group appear | PASS; `test_support` boundary displayed |
| Process identity / label appears | PASS; labels display; process no correctly remains empty / not provided by support surface |
| Recipe reference appears | PASS; `BOM-SD-001`, Recipe Version `1` shown |
| Non-Recipe / missing governed evidence indicators | PASS; controlled warnings show missing Process Master / Standard Performance where not governed |
| Packaging context | PASS with support-surface limitation; no Packaging Context card data returned, source lineage still shows `product_bom_spec` boundary |
| Resource eligibility | PASS with limitation; displayed as not governed / pending governance |
| Standard performance | PASS with limitation; displayed as not governed / pending standard performance |
| Source lineage appears | PASS |
| `test_support_only` warning appears | PASS; frontend shows non-production test-support read-only surface warning text |
| Empty state | PASS; nonexistent search keyword shows empty Product / WIP state without mock rows |
| Error state | PASS; backend unavailable state shows error and does not substitute mock |
| API/mock toggle | PASS; mock mode shows demo rows only after user selection; switching back to API restores `TS-ROUTE-SD-001` and removes mock rows |
| Browser console | PASS after remediation; clean tab reported 0 warn/error logs |
| No write / edit / approve / release controls | PASS |

Observed final browser checks:

- `hasBackendStatus=true`
- `hasRealRoute=true`
- `hasProduct=true`
- `hasMockRoute=false`
- `hasSteps=true`
- `hasRecipe=true`
- `hasTestSupportWarningText=true`
- `hasError=false`
- `logCount=0`

After switching mock mode back to API:

- `hasRealRoute=true`
- `hasMockRoute=false`
- `hasError=false`
- `logCount=0`

## Frontend Remediation Completed During Retest

Three small UX/quality fixes were applied during the retest:

1. Repeated warning rows now use a unique React key, because real Backend data can return the same warning code/refNo for multiple steps.
2. `test_support_only` now renders as explicit user-visible text: `目前資料來自非正式 Shared DEV test-support read-only surface。`
3. Switching data source now clears the previous selection/detail state, preventing stale mock-selected items from triggering unnecessary API detail requests after returning to API mode.

These changes preserve the accepted read-only Product contract and do not introduce write behavior.

## WIP Coverage Limitation

The current Engineering B support surface provides Product route evidence for `PRD-SD-001`.

WIP currently appears as intermediate step/reference evidence in the support surface, but it is not available as an independent WIP Routing Version fixture. This limitation is not hidden and should remain tracked if CTO/CIO later requires explicit standalone WIP route acceptance evidence.

## Automated Validation

| Check | Result |
|---|---|
| `npm run lint` | PASS |
| `npm run build` | PASS |
| `restserver/tests/test_routing_process_flow_api.py` | PASS, 7 passed |
| Full Backend test suite | PASS by Backend evidence, 93 passed |
| `npm run test` | NOT AVAILABLE |

The frontend project still has no `test` script in `package.json`; this remains `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP`.

## Boundary Confirmation

Frontend / UX did not implement Routing write, Product write, Process Master write, Production execution, migration, Source-of-Truth transition, Engineering Pull, Cutover, or ERP2.0 Go-Live behavior.

## Final Classification

**ROUTING_PROCESS_FLOW_PRODUCT_EVIDENCE_RETEST_002_FRONTEND_UX_PASS_WITH_WIP_FIXTURE_LIMITATION**

The `/routing` frontend successfully consumed the real Backend Routing API through the bounded Shared DEV test-support read-only surface, displayed Product route evidence, ordered steps, Recipe reference, source lineage, controlled warnings including `test_support_only`, and preserved API/mock separation with no silent mock fallback. The only retained limitation is that standalone WIP Routing Version fixture evidence is not present in the current Engineering B support surface.
