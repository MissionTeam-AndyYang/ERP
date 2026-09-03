# BOM Product Structure Tree Frontend Implementation Report

- Work item: ERP2-BOM-PRODUCT-STRUCTURE-RO-EXEC-001-UX-001
- Authorization: ERP2-CIO-BOM-PRODUCT-STRUCTURE-RO-EXEC-001
- Execution mode: bounded non-production Frontend / UX implementation
- Project: ERP-2.0
- Branch: main
- Route: `/bom`
- Date: 2026-09-03

## Scope

Implemented the Frontend / UX portion of the read-only finished-product-root Product Structure tree inside BOM Center.

This implementation preserves the accepted boundary:

- Product Structure is a read-only structural product composition view.
- Finished product is the root.
- Root identity uses `PRODUCT_NO + PRODUCT_VERSION` where available.
- WIP / semi-finished, raw material / material, and direct finished-product-to-material children are supported by the tree view model.
- Relationship-level quantity, weight, UOM, version, status, warnings, empty, not-found, partial, loading, and error states are represented.
- No write, edit, approval, mutation, release, planning, costing, inventory, traceability expansion, Production, migration, Source-of-Truth transition, Engineering Pull, Cutover, or Go-Live behavior was added.

## Files Changed

- `src/types/bom.ts`
  - Added `BomProductStructureData`, `BomProductStructureNode`, and `BomProductStructureWarning`.
- `src/services/bom-api.ts`
  - Added Product Structure API client for `GET /api/v2/bom/product-structure/{productNo}`.
  - Added recursive API-to-view-model mapping.
  - Preserved no silent mock fallback in API mode.
- `src/mock/bom.ts`
  - Added explicit Product Structure mock fixtures for manual mock mode only.
- `src/app/bom/page.tsx`
  - Replaced the prior detail-derived temporary product tree with a Product Structure tree view.
  - Added product-root selector, recursive expand/collapse, loading, warning, partial, not-found, empty, and error states.
- `docs/spec/api-proposal/planned_screen_list_naming.md`
  - Added `BOMProductStructureTreeView` to the BOM Center screen roadmap.

## API Client Alignment

The frontend now calls:

`GET /api/v2/bom/product-structure/{product_no}`

Supported query parameters:

- `productVersion`
- `depth`
- `effectiveDate`

The API client accepts a Product-oriented response and maps it into the frontend view model. The frontend does not depend on database table names, ORM names, SQL query shapes, or raw database column names.

## UX States Implemented

- Finished product root display.
- Product version selector from BOM linked products.
- Expand / collapse for all tree levels.
- WIP / semi-finished child display.
- Raw material / material child display.
- Direct material child display when returned by the API.
- Relationship quantity and weight display.
- UOM display.
- Version / status label display.
- Loading state while Product Structure API is pending.
- Empty state when no linked product exists.
- Not-found state when the Product Structure API returns no root.
- Partial / warning state when the API returns `isPartial` or warnings.
- Error state when API mode cannot retrieve Product Structure data.

## Mock Fixture Treatment

Mock Product Structure data is only used when the operator manually selects `示範資料`.

In API mode, API failure remains visible and does not silently show mock data.

## Real Backend Status

Backend / API completed and pushed:

- commit: `49242d6 Implement BOM product structure API`
- route: `GET /api/v2/bom/product-structure/{product_no}`
- backend classification: `PRODUCT_STRUCTURE_READ_ONLY_API_IMPLEMENTED_COMPATIBILITY_PRESERVED_TESTS_PASS_SHARED_DEV_SMOKE_PASS`

Frontend mapping was aligned to the confirmed backend contract:

- `payload.rootProduct` is rendered as the finished-product root node.
- `payload.children[]` is rendered recursively as Product Structure children.
- `relationshipQuantity`, `relationshipWeight`, and `unit` are rendered as parent-child relationship attributes.
- `structureStatusCode`, `versionStateCode`, and `warningCode` are converted to user-facing Traditional Chinese labels in the frontend.
- `payload.warnings[]` is rendered as visible warning state; no mock rows are inserted.

This frontend session attempted to reach `http://127.0.0.1:5025/api/v2/bom/product-structure/PRD-001?productVersion=2&depth=3`, but no service was listening on `127.0.0.1:5025` at that time. Final real-backend browser validation remains pending a reopened backend service window.

## Validation

- `npm run lint`: PASS
- `npm run build`: PASS
- `npm run test`: NOT AVAILABLE

Browser smoke result:

- `/bom` renders successfully.
- Manual mock mode displays the Product Structure tree.
- Product selector displays `P-00018 / V5` and `P-00021 / V2`.
- Finished product root, WIP child, raw material child, relationship quantity, weight, and UOM are visible.
- API mode error state remains visible when backend/API access is unavailable, and mock Product Structure content is not silently inserted.
- No browser console errors were captured during smoke validation.

## Limitations

- Real-backend validation is pending Backend / API delivery of the Product-oriented endpoint and response evidence.
- The project still has no `test` script in `package.json`; this remains `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP`.

## Final Classification

Frontend implementation PASS with real-backend browser validation pending service-window availability.

The bounded read-only Product Structure UX is implemented, aligned to the confirmed backend route and contract, preserves mock/API separation, and updates the screen roadmap. Final UX real-backend classification can move to PASS after the backend service window is available to the frontend session and `/bom` is browser-validated against `GET /api/v2/bom/product-structure/{product_no}`.
