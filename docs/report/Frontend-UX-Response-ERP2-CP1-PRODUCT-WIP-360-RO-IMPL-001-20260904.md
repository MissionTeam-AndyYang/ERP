# Frontend UX Response - ERP2 CP1 Product / WIP 360 Read-Only Implementation

Date: 2026-09-04  
Work item: `ERP2-CP1-PRODUCT-WIP-360-RO-IMPL-001`  
Authority: `ERP2-CIO-CP1-PRODUCT-WIP-360-RO-IMPL-001`  
Screen: `ProductWip360OverviewScreen`  
Route: `/product-360`

## Scope

Implemented bounded non-production read-only frontend screen for Product / WIP 360 overview.

This implementation does not add Product write, create, edit, approve, release, Production, migration, Source-of-Truth transition, Cutover, or Go-Live controls.

## Changed Frontend Files

| File | Purpose |
| --- | --- |
| `src/app/product-360/page.tsx` | Runtime read-only Product / WIP 360 overview screen. |
| `src/services/product-wip-360-api.ts` | API client, payload mapper, empty-state handling, and manual mock mode support. |
| `src/hooks/use-product-wip-360.ts` | Screen data loading state for API / mock modes. |
| `src/types/product-wip-360.ts` | Typed frontend view model. |
| `src/mock/product-wip-360.ts` | Explicit manual mock data for Product and standalone WIP scenarios. |
| `src/layouts/app-layout.tsx` | Adds Product / WIP 360 navigation entry. |
| `src/i18n/dictionary.ts` | Adds navigation label key. |

## Required Evidence

| Required Evidence | Frontend Handling |
| --- | --- |
| Product / WIP identity | Header summary displays `itemNo`, `itemName`, identity type, item category, version, source, warehouse unit, and production unit. |
| Module composition | Module readiness grid displays Item, Transaction Item, Warehouse / Inventory, BOM / Product Structure, Recipe / Formula, and Routing / Process Flow statuses. |
| Partial / unavailable state | API mapper preserves `partial`, `unavailable`, `test_support`, `error`, and `not_applicable`; empty modules render controlled empty states. |
| Source / warning display | Right panel displays source lineage and warning messages without hiding source caveats. |
| Routing test-support caveat | Routing section shows explicit test-support caveat when source or warnings indicate `test_support_only`. |
| Domain-detail navigation | Domain navigation links route to `/items`, `/warehouse/inventory/lots`, `/batches`, `/bom`, `/recipe`, `/routing`, and `/traceability` with query context. |
| API error | API errors render a danger message and keep API source mode. |
| True empty state | Empty API arrays render empty states and do not inject mock rows. |
| No silent mock fallback | `getProductWip360Overview()` returns mock data only when user selects mock mode. API errors return empty API data with error text. |
| No write controls | Screen contains no create, edit, approve, release, POST, PUT, DELETE, Production, Cutover, or Go-Live controls. |

## API Contract Used

Candidate read-only endpoint:

```text
GET /api/v2/product-wip-360/overview?itemNo={itemNo}&itemCategory={4|5}
```

The endpoint is treated as pending backend runtime implementation. Frontend API mode is ready to consume it but will show a controlled error until the backend route is available.

## Boundary Verification

| Boundary | Result |
| --- | --- |
| No Product write | PASS |
| No create / edit controls | PASS |
| No approve / release controls | PASS |
| No Production / MES actions | PASS |
| No migration or Source-of-Truth transition | PASS |
| No Cutover / Go-Live indication | PASS |

## Test Verification

| Check | Result |
| --- | --- |
| Frontend lint | PASS - `npm run lint` |
| Frontend build | PASS - `npm run build`, route `/product-360` included |
| Browser smoke test - API mode | PASS - backend 404 renders controlled API error, no silent mock data injected |
| Browser smoke test - Product mock mode | PASS - Product identity, module composition, routing test-support caveat, and domain navigation visible |
| Browser smoke test - Standalone WIP mock mode | PASS - WIP identity, not-applicable transaction item, partial/unavailable modules, and no-inferred-routing message visible |
| Browser smoke test - write controls | PASS - no create, edit, approve, release, or operational action buttons |

## Known Limitation

Standalone WIP remains partial unless backend provides independent WIP root Product Structure / Recipe / Routing evidence. The screen must not imply standalone WIP Routing Version exists when backend evidence only shows WIP as an intermediate Product routing step or reference.

## Disposition

```text
FRONTEND_UX_PRODUCT_WIP_360_READ_ONLY_IMPLEMENTATION_COMPLETE_PENDING_BACKEND_RUNTIME_ENDPOINT
```
