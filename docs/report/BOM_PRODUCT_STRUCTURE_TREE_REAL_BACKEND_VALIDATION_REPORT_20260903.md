# BOM Product Structure Tree Real Backend Validation Report

- Work item: ERP2-BOM-PRODUCT-STRUCTURE-RO-EXEC-001-UX-REAL-BE-001
- Authorization: ERP2-CIO-BOM-PRODUCT-STRUCTURE-RO-EXEC-001
- Execution mode: bounded non-production Frontend / UX real-backend validation
- Project: ERP-2.0
- Branch: main
- Frontend route: `/bom`
- Backend service URL: `http://127.0.0.1:5027`
- Backend process evidence: pythonw PID 6192
- Backend evidence commit: `19e9204 Document BOM product structure service window`
- Frontend implementation commit under validation: `ed954fe Implement BOM product structure tree UX`
- Date: 2026-09-03

## Scope

This report records real-backend browser validation for the BOM Center read-only Product Structure tree. It validates only the bounded non-production Shared DEV service window and does not cover Product write, Recipe / Formula implementation, Production access, migration, Source-of-Truth transition, Engineering Pull, Cutover, or Go-Live.

No raw secrets or validation token values are recorded in this report.

## Backend Routes Consumed

- `GET /api/v2/bom/dashboard`
- `GET /api/v2/bom/{bom_no}/detail`
- `GET /api/v2/bom/product-structure/{product_no}`

Backend confirmed the Product Structure endpoint and existing BOM endpoints as PASS before UX validation. UX did not repeat POST/write checks; backend service-window evidence already confirmed POST negative control returned HTTP 405 read-only behavior.

## Direct API Sanity

Direct read-only API sanity against `http://127.0.0.1:5027` returned:

| Check | Result |
| --- | --- |
| Dashboard API code | `0` |
| Selected BOM | `BOM-SD-001` |
| Detail API code | `0` |
| Selected product root | `PRD-SD-001` |
| Selected product version | `1` |
| Product Structure API code | `0` |
| Root product | `PRD-SD-001` |
| Root structure status | `complete` |
| Root child count | `1` |
| Warning count | `0` |

## Browser Validation

Frontend was started with:

- `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5027`
- `NEXT_PUBLIC_API_TIMEZONE=Asia/Taipei`
- non-production API token supplied through local environment variable, value redacted
- frontend URL: `http://127.0.0.1:3027/bom`

Browser-visible result:

| Check | Result |
| --- | --- |
| `/bom` page loaded | PASS |
| Backend data source badge visible | PASS |
| Dashboard displayed real backend BOM `BOM-SD-001` | PASS |
| Detail panel displayed backend linked product `PRD-SD-001` | PASS |
| Product Structure section displayed backend tree | PASS |
| Finished-product root displayed | PASS |
| Relationship quantity and weight displayed | PASS |
| Status displayed | PASS |
| No API error during happy path | PASS |
| No silent mock fixture displayed in API mode | PASS |
| No development-stage copy displayed | PASS |
| No write/edit/approval controls displayed | PASS |
| Browser console errors | `0` |

Visible backend tree evidence included:

- root: `PRD-SD-001 · Shared DEV Product Fixture A`
- child: `MAT-SD-001 · Shared DEV Material Fixture A`
- relationship attributes: quantity, weight, and UOM displayed in the tree rows

## Error / No Silent Mock Fallback Validation

Frontend was restarted with an intentionally unavailable backend URL:

- `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5999`
- frontend URL: `http://127.0.0.1:3028/bom`

Browser-visible result:

| Check | Result |
| --- | --- |
| `/bom` page loaded | PASS |
| Dashboard API error state displayed | PASS |
| Error message states the page did not switch to mock data | PASS |
| Mock dashboard fixtures absent | PASS |
| Mock Product Structure fixtures absent | PASS |
| Browser console errors | `0` |

## Read-Only UI Confirmation

The frontend Product Structure tree exposes only read navigation and expand/collapse controls. No Product write, edit, save, delete, approval, release, Recipe / Formula mutation, costing, inventory, planning, traceability expansion, migration, cutover, or Go-Live controls were added or displayed.

## Validation Commands

- `npm run lint`: PASS
- `npm run build`: PASS
- `npm run test`: NOT AVAILABLE

The project still has no `test` script in `package.json`; this remains `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP`.

## Limitations

- Validation is limited to the Shared DEV formal fixture exposed through backend service window `http://127.0.0.1:5027`.
- Browser smoke covered the available fixture root `PRD-SD-001` and the explicit API failure path. Broader multi-product, partial/warning, not-found, and depth-limited real-backend browser cases should be validated when Backend provides additional formal fixtures for those states.

## Final Classification

**BOM_PRODUCT_STRUCTURE_UX_REAL_BACKEND_VALIDATION_PASS_SHARED_DEV_READONLY_NO_SILENT_MOCK_FALLBACK**

The BOM Product Structure UX consumed the confirmed backend route, rendered the real finished-product-root tree, preserved read-only boundaries, displayed no silent mock fallback, and passed lint/build/browser smoke for the active non-production service window.
