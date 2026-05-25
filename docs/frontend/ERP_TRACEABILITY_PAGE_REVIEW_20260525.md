# ERP Traceability Page Review

Date: 2026-05-25
Scope: Traceability V1 frontend UX refinement and API-readiness review.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-05-25 |
| Reviewer | Codex |
| Page / route | Traceability / `/traceability` |
| Related API endpoint | `GET /api/v1/traceability/dashboard` |
| Data source during review | `mock` with service-layer API fallback |
| Frontend commit / branch | `main` / `96f682f Refine traceability UX interactions` |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pass | Browser smoke opened `/traceability` successfully. |
| No compile/schema error | Pass | Lint and production build completed after UX refinement. |
| Loading state is stable | Pass | Page renders mock fallback while service checks API availability. |
| API failure falls back or shows controlled empty/error state | Pass | `useTraceabilityDashboard` returns mock data and exposes a warning message when API is unavailable. |
| Desktop layout has no overlap | Pass | Browser smoke found no page-level horizontal overflow. |
| Primary action is usable | Pass | Header `查詢` action switches to the batch-chain view. |
| Navigation/sidebar behavior is usable | Pass | Traceability remains reachable through shared app layout. |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern | Pass | Supports batch/item/order/work-order lookup, upstream/downstream trace chain, recall scope and document completeness. |
| Highest-priority risk is visible without drilling down | Pass | KPI strip, trace status and document view expose missing documents and broken-chain risks. |
| Status tones are understandable | Pass | Uses shared `StatusBadge` tones for trace status, chain nodes and documents. |
| Main cards/tables use practical labels | Pass | Table surfaces query/batch, item, direction, source, work/order, quantity, impact scope and status. |
| Empty or missing data does not mislead the user | Pass with notes | Search-filtered empty states now show controlled messages; API-empty partial datasets still fall back to mock per current service policy. |
| User can identify next action or owner where relevant | Pass | Detail panel exposes document owners and trace chain context. |

## UX Refinement Completed

| Item | Result |
| --- | --- |
| Search behavior | Header search now filters trace records by batch, item, supplier, customer, document, work order, sales order, warehouse, status and risk. |
| Detail synchronization | If the selected trace record does not match the current view/search, the detail panel derives the first matching record. |
| Query entry | Header action now switches to `批號鏈路`, making it a clear view navigation action. |
| Placeholder action clarity | Advanced filter remains a V1 placeholder with tooltip guidance until API filter fields are confirmed. |
| Empty state | Search-filtered empty results show controlled messages instead of blank panels. |

## Decision

Decision:

```txt
accepted_with_notes
```

Reason:

The Traceability page is suitable for V1 API validation as a read-only trace and recall-scope workspace. It preserves the agreed boundary: investigation and document visibility, not corrective-action mutation.

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
| Backend engineer | Confirm whether batch trace records include upstream and downstream relationships. | High | Before implementing `/api/v1/traceability/dashboard` |
| Backend engineer | Confirm joins across purchase receipt, work order, inventory and shipping order. | High | During Traceability API implementation |
| Backend engineer | Confirm traceability document source and owner fields. | High | During Traceability API implementation |
| Backend engineer | Confirm whether recall scope is stored or derived by API aggregation. | High | During Traceability API implementation |
| Frontend | Revisit empty-array fallback policy after real API returns controlled empty datasets. | Medium | After first Traceability API runtime report |
| Frontend | Move stable Traceability static labels into `src/i18n/dictionary.ts`. | Medium | After Traceability API mapping stabilizes |
