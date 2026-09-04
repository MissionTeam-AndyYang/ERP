# Frontend UX Response - ERP2 CP1 Product / WIP 360 Shared DEV Retest

Date: 2026-09-04  
Work item: `ERP2-CP1-PRODUCT-WIP-360-RO-IMPL-001`  
Frontend route: `/product-360`  
Backend endpoint: `GET /api/v2/product-wip-360/overview`  
Runtime boundary: Bounded non-production Shared DEV / controlled TEST only

## Scope

Retested Product / WIP 360 frontend API mode against the implemented backend endpoint using Engineering Office B governed Shared DEV DB credential injection.

This retest does not add Product write, Production, migration, Source-of-Truth transition, Cutover, or Go-Live behavior.

## Runtime Setup

| Item | Value |
| --- | --- |
| DB access method | Governed wrapper child-process environment injection |
| Wrapper | `20_Engineering_Workspace/Runtime_Connectivity/ERP2-SHARED-DEV-DB-ENDPOINT-A1-ACT-001/tools/invoke_shared_dev_item_transitem_db_access.ps1` |
| Shared DEV DB endpoint | `172.20.10.3:3307` |
| Shared DEV DB | `erp2_shared_dev_item_transitem_np` |
| Backend service window | `http://127.0.0.1:5062` |
| Frontend service window | `http://127.0.0.1:3039/product-360` |
| Token treatment | `TOKEN_ENABLED=1` in backend child process; frontend supplied `x-auth-token` |
| Raw secret exposure | 0 raw secret values printed, copied, persisted, or committed |

## Direct Backend API Evidence

| Query | HTTP/API Result | Evidence |
| --- | --- | --- |
| Product `PRD-SD-001`, category `5` | 200 / code 0 | Returned `Shared DEV Product Fixture A`, transaction item `TI-CUST-SD-001`, customer `Shared DEV Customer A`, BOM `BOM-SD-001`, material `MAT-SD-001`, routing `TS-ROUTE-SD-001` |
| WIP `INP-SD-001`, category `4` | 200 / code 0 | Returned `Shared DEV Inproduct Fixture A`, unavailable transaction item, partial BOM / Recipe governance warnings, unavailable Routing |
| Not found `NO-SUCH-ITEM`, category `5` | Controlled error | Returned `record not found` with empty payload |
| Invalid category `1` | Controlled error | Returned `invalid itemCategory` with empty payload |

## Frontend Contract Alignment

| Area | Result |
| --- | --- |
| WIP default API query | Aligned to Shared DEV WIP fixture `INP-SD-001` |
| `subject.sourceCode` | PASS - displayed as source context |
| `transactionContext.transactionItems[].companyName` | PASS - displayed as customer / supplier context |
| `sourceLineage` object payload | PASS - mapped without `[object Object]` |
| BOM detail payload | PASS - mapped `rootProduct`, `bomEvidence`, nested `children`, and relationship quantity / weight |
| Recipe detail payload | PASS - mapped `recipeVersions`, `inputs`, `output`, and warning codes |
| Routing detail payload | PASS - mapped nested `routingVersion`, `sourceLineage.routingVersionSourceCode`, nested step references, and `test_support_only` warnings |
| Transaction Item Context section | PASS - Product API mode displays transaction item, customer, contract, unit, and price |

## Browser Retest Evidence

| Check | Result |
| --- | --- |
| Product identity | PASS - screen displayed `PRD-SD-001` and `Shared DEV Product Fixture A` |
| Product module composition | PASS - Item, Transaction Item, Warehouse / Inventory, BOM / Product Structure, Recipe / Formula, Routing / Process Flow shown |
| Product transaction context | PASS - displayed `TI-CUST-SD-001`, `Shared DEV Customer A`, and `CTR-SALE-SD-001` |
| Product BOM / Recipe | PASS - displayed `BOM-SD-001` and `MAT-SD-001` |
| Product Routing test-support caveat | PASS - displayed `TS-ROUTE-SD-001` and `test_support_only` boundary |
| WIP identity | PASS - screen displayed `INP-SD-001` and `Shared DEV Inproduct Fixture A` |
| WIP partial / unavailable states | PASS - displayed missing transaction item, partial BOM / Recipe warnings, and unavailable Routing state |
| No silent mock fallback | PASS - API mode displayed real backend data and did not inject mock rows |
| Manual mock toggle | PASS - mock data appeared only after selecting `示範資料` |
| Domain navigation | PASS - item, warehouse, batch, BOM, recipe, routing, and traceability drill-down links available |
| Write controls | PASS - no create, edit, approve, release, or operational action buttons |
| Browser console errors | PASS - no browser console errors captured |

## Automated Tests

| Test | Result |
| --- | --- |
| Frontend lint | PASS - `npm run lint` |
| Frontend build | PASS - `npm run build`, route `/product-360` included |
| Backend Product / WIP 360 pytest | PASS - `9 passed` |
| Related v2 regression pytest | PASS - `50 passed` |

## Notes

Warehouse module returned `module_unavailable` for the Shared DEV Product and WIP queries while the overall Product / WIP 360 endpoint returned HTTP 200 and preserved module-level warning state. Frontend rendered this as a controlled module warning and did not treat it as a page failure.

Standalone WIP Routing remains unavailable in the current Shared DEV data surface. The frontend renders the unavailable state and does not infer Routing steps.

## Disposition

```text
FRONTEND_UX_PRODUCT_WIP_360_SHARED_DEV_REAL_BACKEND_RETEST_PASS
```
