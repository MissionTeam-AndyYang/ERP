# Frontend UX Response - ERP2 CP1 Product / WIP 360 Read-Only Bounded Retest

Date: 2026-09-04  
Work item: `ERP2-CP1-PRODUCT-WIP-360-RO-IMPL-001`  
Retest scope: Frontend `/product-360` against implemented backend endpoint  
Frontend route: `/product-360`  
Backend endpoint: `GET /api/v2/product-wip-360/overview`

## Scope

Performed a bounded non-production retest after backend implementation commit `b37e057 Implement CP1 product WIP 360 overview API`.

This retest verifies that the frontend attempts the real backend endpoint in API mode, does not silently fall back to mock data, preserves Product / WIP read-only boundaries, and keeps manual mock mode explicit.

No Product write, Production, migration, Source-of-Truth transition, Cutover, or Go-Live controls were added.

## Frontend Contract Alignment

| Area | Result |
| --- | --- |
| `subject.sourceCode` | Aligned. Frontend now accepts backend `subject.sourceCode` as the source label. |
| `transactionContext.transactionItems[].companyName` | Aligned. Frontend now accepts backend `companyName` when `companyDisplayName` is not provided. |
| `sourceLineage` object payload | Aligned. Frontend now accepts backend object form such as `module -> { sourceCode, sourceRefNo }` without rendering `[object Object]`. |

## Backend Runtime Check

Local Flask development server started at:

```text
http://127.0.0.1:5056
```

Direct endpoint checks:

| Check | Result |
| --- | --- |
| Without token | PASS route exists; backend returned controlled `missing token parameter`, not 404 |
| With token, Product query | BLOCKED by local DB: `mariadb.OperationalError Can't connect to server on 'localhost' (10061)` |
| With token, WIP query | BLOCKED by local DB: `mariadb.OperationalError Can't connect to server on 'localhost' (10061)` |
| Backend targeted pytest | PASS - `9 passed` |

The local environment cannot complete real DB-backed payload validation because MariaDB is not reachable on `localhost:3306`.

## Frontend Browser Retest

Frontend was started with:

```text
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5056
NEXT_PUBLIC_API_TOKEN=token
NEXT_PUBLIC_API_TIMEZONE=Asia/Taipei
```

Browser route:

```text
http://127.0.0.1:3036/product-360
```

| Check | Result |
| --- | --- |
| API mode calls implemented backend endpoint | PASS - frontend received `API request failed: 400` from Flask backend, not Next.js 404 |
| No silent mock fallback | PASS - API error state stayed in API mode and did not display mock Product or WIP rows |
| True empty state on API failure | PASS - empty module, batch, lineage, and warning states rendered without injected mock rows |
| Product/WIP manual mock mode | PASS - mock data appears only after selecting `示範資料` |
| Standalone WIP boundary | PASS - WIP mock shows partial / unavailable modules and no-inferred-routing wording |
| Write controls | PASS - no create, edit, approve, release, or operational action buttons |
| Browser console errors | PASS - no browser console errors captured |

## Blocker

Real DB-backed Product / WIP payload validation remains blocked in this local runtime because MariaDB is not reachable:

```text
mariadb.OperationalError Can't connect to server on 'localhost' (10061)
```

The frontend API-mode integration path is verified against the actual Flask route up to the controlled backend DB error response. Full real-data verification should be repeated in the engineer Shared DEV environment where MariaDB is available.

## Disposition

```text
FRONTEND_UX_PRODUCT_WIP_360_BOUNDED_RETEST_COMPLETE_WITH_LOCAL_DB_RUNTIME_BLOCKER
```
