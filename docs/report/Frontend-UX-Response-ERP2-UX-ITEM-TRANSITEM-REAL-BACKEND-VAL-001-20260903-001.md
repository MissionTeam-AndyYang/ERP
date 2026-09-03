# Frontend UX Real Backend Validation Report

- Work item: ERP2-UX-ITEM-TRANSITEM-REAL-BACKEND-VAL-001
- Authorization: ERP2-CIO-SHARED-DEV-DB-PRIVATE-ACT-001
- Project: ERP-2.0
- Participant: Frontend UX Refinement session
- Branch: main
- Frontend route under validation: `/items`
- Backend service consumed: `http://127.0.0.1:5025`
- Backend credential handling: non-production request header was supplied through local environment variable and is intentionally redacted from this report.
- Code baseline validated: `4d1817d Document UX backend service window`
- Validation date: 2026-09-03

## Scope

This validation covers read-only frontend UX integration for Item Center and Transaction Item Master flows against the bounded Shared DEV backend service window. It does not cover Production UX, Production API, database direct access, write flows, migrations, Engineering Pull, Cutover, or Go-Live.

## API Response Validation

### Item Center Dashboard

- Endpoint: `GET /api/v2/items/dashboard`
- Result: PASS
- Response summary:
  - `code`: `0`
  - `total`: `5`
  - first item: `MAT-SD-002`
  - first item name: `Shared DEV Material Fixture B`

### Item Detail Drilldown

- Endpoint: `GET /api/v2/items/MAT-SD-002/detail`
- Result: PASS
- Response summary:
  - `code`: `0`
  - `itemNo`: `MAT-SD-002`
  - `bomUsage` count: `0`
  - `recentBatches` count: `0`
- Frontend behavior: real empty arrays are rendered as empty states. No mock detail rows are inserted.

### Transaction Item Dashboard

- Endpoint: `GET /api/v2/transitems/dashboard`
- Result: PASS
- Response summary:
  - `code`: `0`
  - `total`: `2`
  - first company: `CUST-SD-001`
  - first company name: `Shared DEV Customer A`
  - first transaction item: `TI-SUP-SD-001`
  - first transaction item name: `Supplier Material Transaction Fixture`

### Company Detail Drilldown

- Endpoint: `GET /api/v2/transitems/companies/CUST-SD-001/detail`
- Result: PASS
- Response summary:
  - `code`: `0`
  - `companyNo`: `CUST-SD-001`
  - transaction item count: `1`
  - contract count: `1`

### Transaction Item Detail Drilldown

- Endpoint: `GET /api/v2/transitems/transitems/TI-SUP-SD-001/detail`
- Result: PASS
- Response summary:
  - `code`: `0`
  - `transactionItemNo`: `TI-SUP-SD-001`
  - linked item count: `1`
  - contract count: `1`

## Browser UX Validation

Frontend dev server was started with:

- `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5025`
- `NEXT_PUBLIC_API_TIMEZONE=Asia/Taipei`
- non-production API token supplied by local environment variable, value redacted
- frontend URL: `http://127.0.0.1:3025/items`

Validated browser-visible behavior:

- Item Center dashboard displays Shared DEV backend data.
- The page shows the backend/API data source state.
- Item dashboard does not show mock fixture data such as `RM-001`.
- Item detail panel opens successfully for `MAT-SD-002`.
- Item detail panel shows real empty states for empty `bomUsage` and `recentBatches`.
- Transaction Item dashboard displays `Supplier Material Transaction Fixture` and `TI-SUP-SD-001`.
- Transaction Item detail panel displays linked material item `MAT-SD-002`.
- Customer/Supplier dashboard displays `Shared DEV Customer A` and `CUST-SD-001`.
- Customer/Supplier detail panel displays transaction item and contract sections, including `Shared DEV Sales Contract Fixture`.
- No browser console errors were captured during the happy-path validation.
- Removed development copy remains absent; `Local Candidate` was not found in the rendered page.

## API Error Handling Validation

Frontend dev server was restarted with an intentionally unavailable backend URL:

- `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5999`
- frontend URL: `http://127.0.0.1:3026/items`

Validated browser-visible behavior:

- Result: PASS
- The page displays an API error state.
- The page does not silently fall back to mock data.
- Mock fixture strings such as `RM-001`, `TI-001`, `中區量販`, `綠田食品`, and `包裝紙箱` were not found in the rendered error state.

## Build And Lint

- `npm run build`: PASS
- `npm run lint`: PASS
- `npm run test`: NOT AVAILABLE

The project currently has no `test` script in `package.json`. This is recorded as `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP` and should be handled as a frontend test workflow standardization task, not as a blocker for this bounded validation.

## Defects And Blockers

- No UX real-backend validation blocker found for the covered read-only Item Center and Transaction Item Master flows.
- Non-blocking gap: `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP`.

## Final Classification

PASS with non-blocking test workflow gap.

The covered frontend read-only flows can consume the Shared DEV backend service window at `http://127.0.0.1:5025`, render real backend data, render real empty arrays as empty states, and avoid silent mock fallback when the API is unavailable.
